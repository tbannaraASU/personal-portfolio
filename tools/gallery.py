#!/usr/bin/env python3
"""Import your OWN Instagram JSON export or a manually curated CSV into SQLite.

Then publish only caption/tag/photo metadata as data/gallery.json + gallery-data.js.
Requires only Python 3 stdlib. Optional Pillow: normalize and strip photo EXIF.
"""
from __future__ import annotations
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import re
import shutil
import sqlite3
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / 'local' / 'gallery.sqlite'
MEDIA = ROOT / 'photos'
SCHEMA = Path(__file__).with_name('schema.sql')
SUPPORTED = {'.jpg', '.jpeg', '.png', '.webp'}
MAX_IMAGE_SIZE = 30 * 1024 * 1024
TAG_PATTERN = re.compile(r'(?<![\w])#([\w]+)', re.UNICODE)


def db_connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    con.execute('PRAGMA foreign_keys=ON')
    con.executescript(SCHEMA.read_text(encoding='utf-8'))
    return con


def tags_from_caption(caption, extra=''):
    seen = set()
    tags = []
    for raw in [*TAG_PATTERN.findall(caption or ''), *TAG_PATTERN.findall(extra or '')]:
        tag = '#' + raw.casefold()
        if tag not in seen:
            seen.add(tag)
            tags.append(tag)
    return tags


def clean_title(caption, timestamp=''):
    parts = [x.strip() for x in (caption or '').splitlines() if x.strip()]
    candidate = next((line for line in parts if not line.startswith('#')), '')
    candidate = TAG_PATTERN.sub('', candidate).strip(' -\t')
    return candidate[:75] if candidate else ('Photo set · ' + timestamp[:10] if timestamp else 'Photo set')


def valid_permalink(value):
    value = (value or '').strip()
    if not value:
        return ''
    parsed = urlparse(value)
    return value if parsed.scheme == 'https' and parsed.netloc.lower() in {'instagram.com','www.instagram.com'} else ''


def store_post(con, post):
    con.execute('INSERT INTO posts(id,caption,title,published_at,permalink) VALUES(?,?,?,?,?) '
                'ON CONFLICT(id) DO UPDATE SET caption=excluded.caption,title=excluded.title,'
                'published_at=excluded.published_at,permalink=excluded.permalink',
                (post['id'], post['caption'], post['title'], post['published_at'], post['permalink']))
    con.execute('DELETE FROM photos WHERE post_id=?', (post['id'],))
    con.execute('DELETE FROM post_hashtags WHERE post_id=?', (post['id'],))
    for pos, photo in enumerate(post['photos']):
        con.execute('INSERT INTO photos(post_id,position,path,alt_text) VALUES (?,?,?,?)',
                    (post['id'], pos, photo, post['title']))
    for tag in post['hashtags']:
        con.execute('INSERT OR IGNORE INTO hashtags(tag) VALUES(?)', (tag,))
        con.execute('INSERT OR IGNORE INTO post_hashtags(post_id,hashtag_id) '
                    'SELECT ?,id FROM hashtags WHERE tag=?', (post['id'],tag))


def public_path(filename):
    return 'photos/' + filename


def safe_image_write(raw, key, position, suffix):
    """Preserves usable image, strips EXIF if Pillow exists. No other media uploaded."""
    if suffix.lower() not in SUPPORTED or len(raw) > MAX_IMAGE_SIZE or not raw:
        return None
    MEDIA.mkdir(exist_ok=True)
    name = f'{key}-{position:02d}{suffix.lower()}'
    path = MEDIA / name
    try:
        from PIL import Image, ImageOps
        image = Image.open(io.BytesIO(raw))
        image = ImageOps.exif_transpose(image)
        output = io.BytesIO()
        image_format = 'JPEG' if suffix.lower() in {'.jpg', '.jpeg'} else suffix.lower().lstrip('.').upper()
        if image_format == 'JPEG' and image.mode not in ('L','RGB'):
            image = image.convert('RGB')
        image.save(output, format=image_format, quality=90 if image_format == 'JPEG' else None)
        raw = output.getvalue()
    except ImportError:
        raise RuntimeError('Pillow is required to remove private EXIF/GPS metadata. Install: python3 -m pip install Pillow')
    except Exception as exc:
        print(f'Warning: could not process image {name}: {exc}. Skipping.', file=sys.stderr)
        return None
    path.write_bytes(raw)
    return public_path(name)


def extract_photo_bytes(name, content):
    # Only read entries with normal relative paths and valid browser-readable formats.
    normalized = name.replace('\\', '/')
    parts = PurePosixPath(normalized).parts
    if not parts or '..' in parts or normalized.startswith('/'):
        return None
    suffix = Path(normalized).suffix.lower()
    if suffix not in SUPPORTED:
        return None
    if len(content) > MAX_IMAGE_SIZE:
        return None
    return suffix


def archive_member_lookup(names):
    # Some exports wrap all files in a username/timestamp folder.
    ordered = sorted((n for n in names if not n.startswith('__MACOSX/')), key=len)
    basenames = {}
    for filename in ordered:
        if Path(filename).suffix.lower() in SUPPORTED:
            basenames.setdefault(PurePosixPath(filename).name, []).append(filename)
    def lookup(uri):
        u = uri.replace('\\', '/').lstrip('./')
        if not u or '..' in PurePosixPath(u).parts:
            return None
        for filename in ordered:
            if filename == u or filename.endswith('/'+u):
                return filename
        # Some user-curated exports move media/posts/X.jpg to photos/photo/X.jpg.
        # Match a basename only when it uniquely identifies one image.
        alternatives = basenames.get(PurePosixPath(u).name, [])
        return alternatives[0] if len(alternatives) == 1 else None
    return lookup


def exported_caption(post):
    candidates = [post.get('title'), post.get('caption')]
    for media in post.get('media', []):
        if isinstance(media, dict):
            candidates.append(media.get('title'))
    return next((str(x) for x in candidates if isinstance(x,str) and x.strip()), '')


def timestamp_iso(value):
    if isinstance(value, (int,float)) and value > 0:
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat(timespec='seconds')
    if isinstance(value,str) and value:
        return value
    return ''


def import_instagram(archive, include_unlinked=False):
    count, copied, missing, orphan_count = 0, 0, 0, 0
    with ZipFile(archive) as zf, db_connect() as con:
        allnames = [z.filename for z in zf.infolist() if not z.is_dir() and not z.filename.startswith('__MACOSX/')]
        find_media = archive_member_lookup(allnames)
        used_media = set()
        candidates = [n for n in allnames if re.search(r'(?:^|/)(?:posts(?:_\d+)?\.json)$', n, re.I)]
        # posts.json commonly repeats posts_1.json but does not contain direct media.
        if any(re.search(r'(?:^|/)posts_\d+\.json$', n, re.I) for n in candidates):
            candidates = [n for n in candidates if re.search(r'(?:^|/)posts_\d+\.json$', n, re.I)]
        if not candidates:
            raise ValueError('Could not locate posts_1.json/posts.json. Instagram export must use JSON format and include Posts.')
        for name in sorted(candidates):
            try:
                raw = json.loads(zf.read(name).decode('utf-8-sig'))
            except (UnicodeError, ValueError) as exc:
                print(f'Skipped malformed JSON {name}: {exc}', file=sys.stderr)
                continue
            entries = raw if isinstance(raw,list) else raw.get('media_posts', raw.get('posts', [])) if isinstance(raw,dict) else []
            for entry in entries:
                if not isinstance(entry,dict):
                    continue
                media = entry.get('media') or ([entry] if entry.get('uri') else [])
                if not isinstance(media, list):
                    continue
                uris = [m.get('uri', '') for m in media if isinstance(m,dict) and isinstance(m.get('uri'),str)]
                if not uris:
                    continue
                stable = hashlib.sha256((uris[0] + '|' + str(entry.get('creation_timestamp',''))).encode('utf-8')).hexdigest()[:16]
                photo_paths = []
                for position, uri in enumerate(uris, 1):
                    member = find_media(uri)
                    if not member:
                        missing += 1
                        continue
                    info = zf.getinfo(member)
                    if info.file_size > MAX_IMAGE_SIZE:
                        continue
                    ext = Path(member).suffix.lower()
                    if ext not in SUPPORTED:
                        continue
                    data = zf.read(member)
                    if extract_photo_bytes(member, data) is None:
                        continue
                    saved = safe_image_write(data, stable, position, ext)
                    if saved:
                        used_media.add(member)
                        photo_paths.append(saved)
                        copied += 1
                if not photo_paths:
                    continue
                caption = exported_caption(entry)
                date = timestamp_iso(entry.get('creation_timestamp') or (media[0].get('creation_timestamp') if media and isinstance(media[0],dict) else None))
                permalink = valid_permalink(entry.get('permalink', ''))
                store_post(con, {'id':'ig-'+stable,'caption':caption,'title':clean_title(caption,date),
                                 'published_at':date,'permalink':permalink,'hashtags':tags_from_caption(caption),
                                 'photos':photo_paths})
                count += 1
        if include_unlinked:
            # Files present in a user-curated archive but not referenced by posts JSON.
            # Never guess hashtags, captions, dates, or locations for these photos.
            for filename in allnames:
                if filename in used_media or Path(filename).suffix.lower() not in SUPPORTED:
                    continue
                if zf.getinfo(filename).file_size > MAX_IMAGE_SIZE:
                    continue
                unique = hashlib.sha256(filename.encode('utf8')).hexdigest()[:16]
                saved = safe_image_write(zf.read(filename), unique, 1, Path(filename).suffix)
                if not saved:
                    continue
                store_post(con, {'id':'unlinked-'+unique,'caption':'','title':'Uncategorized photo',
                                 'published_at':'','permalink':'','hashtags':[], 'photos':[saved]})
                orphan_count += 1
        con.commit()
    print(f'Imported {count} Instagram photo sets with {copied} linked images. Missing references: {missing}.')
    if include_unlinked:
        print(f'Also imported {orphan_count} unlinked images into the Untagged collection.')
    if not count:
        print('No supported JPG/PNG/WebP images found. Check the export includes media and is JSON format.', file=sys.stderr)
    if missing:
        print('Tip: Re-export with high-quality media included, or add missing items using the CSV method.')
    print('For privacy: review imported photos before publishing. Pillow (pip install Pillow) strips EXIF.')


def import_csv(path):
    total = 0
    with path.open('r',encoding='utf-8-sig',newline='') as fh, db_connect() as con:
        reader = csv.DictReader(fh)
        required = {'id','caption','images'}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError('CSV must contain columns: id, caption, images')
        for row in reader:
            rid = (row.get('id') or '').strip()
            if not rid:
                continue
            stable = hashlib.sha256(rid.encode()).hexdigest()[:16]
            files = [x.strip() for x in (row.get('images') or '').split(';') if x.strip()]
            copied = []
            for position, entry in enumerate(files,1):
                source = Path(entry).expanduser()
                if not source.is_absolute():
                    source = path.parent / source
                if not source.is_file():
                    print(f'Missing file: {source}', file=sys.stderr)
                    continue
                raw = source.read_bytes()
                if extract_photo_bytes(source.name,raw) is None:
                    print(f'Unsupported image: {source}', file=sys.stderr)
                    continue
                saved = safe_image_write(raw,stable,position,source.suffix)
                if saved:
                    copied.append(saved)
            if not copied:
                print(f'No valid photos for row id {rid}; skipped.',file=sys.stderr)
                continue
            caption = row.get('caption') or ''
            date = row.get('date') or ''
            store_post(con,{'id':'custom-'+stable,'caption':caption,'title':(row.get('title') or '').strip() or clean_title(caption,date),
                            'published_at':date,'permalink':valid_permalink(row.get('permalink','')),
                            'hashtags':tags_from_caption(caption,row.get('hashtags','')),'photos':copied})
            total += 1
        con.commit()
    print(f'Imported {total} curated photo sets from CSV.')


def build():
    """Publish photo sets, hashtag counts and curated albums for static GitHub Pages."""
    with db_connect() as con:
        con.row_factory = sqlite3.Row
        rows = con.execute('SELECT * FROM posts ORDER BY published_at DESC, id').fetchall()
        collection = []
        for row in rows:
            photos = con.execute('SELECT path,alt_text FROM photos WHERE post_id=? ORDER BY position',(row['id'],)).fetchall()
            photos = [{'src':p['path'],'alt':p['alt_text']} for p in photos if (ROOT / p['path']).is_file()]
            if not photos:
                continue
            tag_rows = con.execute('SELECT h.tag FROM hashtags h JOIN post_hashtags ph ON ph.hashtag_id=h.id WHERE ph.post_id=? ORDER BY h.tag',(row['id'],)).fetchall()
            collection.append({'id':row['id'],'title':row['title'],'caption':row['caption'],'published_at':row['published_at'],
                               'permalink':row['permalink'],'hashtags':[t['tag'] for t in tag_rows],'photos':photos})
        included = {p['id'] for p in collection}
        albums = []
        for album in con.execute('SELECT * FROM albums ORDER BY sort_order ASC,title COLLATE NOCASE ASC').fetchall():
            ids = [r['post_id'] for r in con.execute('SELECT post_id FROM album_posts WHERE album_id=? ORDER BY position,post_id',(album['id'],)).fetchall() if r['post_id'] in included]
            if not ids:
                continue  # Keep empty albums in admin, not in the public gallery
            cover = album['cover_post_id'] if album['cover_post_id'] in ids else ids[0]
            albums.append({'id':album['id'],'title':album['title'],'description':album['description'],
                           'cover_post_id':cover,'post_ids':ids})
    content = {'account':'foto_4th','posts':collection,'albums':albums}
    data = ROOT / 'data'
    data.mkdir(exist_ok=True)
    rendered = json.dumps(content,ensure_ascii=False,indent=2)
    (data/'gallery.json').write_text(rendered+'\n',encoding='utf-8')
    (data/'gallery-data.js').write_text('/* Built from SQLite. Do not edit by hand. */\nwindow.PORTFOLIO_GALLERY = '+rendered+';\n',encoding='utf-8')
    print(f'Built gallery for {len(collection)} photo sets and {len(albums)} populated albums.')


def seed_albums():
    """Optionally create starter albums from ACTUAL imported hashtags.

    Non-destructive: existing albums and their manually selected members are unchanged.
    """
    templates = [
        ('film-stories', 'Film Stories', 'Moments shot on film.', '#filmphotography'),
        ('fujifilm-frames', 'Fujifilm Frames', 'A collection of photographs tagged Fujifilm.', '#fujifilm'),
        ('panoramic-stories', 'Panoramic Stories', 'Wider frames and panoramic photo sets.', '#panoramicphotography'),
        ('monochrome', 'Black & White', 'Monochrome images and experiments.', '#blackwhitephotography'),
    ]
    created=0
    with db_connect() as con:
        for index,(aid,title,description,tag) in enumerate(templates):
            if con.execute('SELECT 1 FROM albums WHERE id=?',(aid,)).fetchone():
                continue
            ids=[p[0] for p in con.execute('SELECT ph.post_id FROM post_hashtags ph JOIN hashtags h ON h.id=ph.hashtag_id WHERE h.tag=? ORDER BY ph.post_id',(tag,))]
            if not ids:
                continue
            next_pos=con.execute('SELECT COALESCE(MAX(sort_order), -1)+1 FROM albums').fetchone()[0]
            con.execute('INSERT INTO albums(id,title,description,cover_post_id,sort_order) VALUES(?,?,?,?,?)',(aid,title,description,ids[0],next_pos))
            for pos,pid in enumerate(ids):
                con.execute('INSERT INTO album_posts(album_id,post_id,position) VALUES(?,?,?)',(aid,pid,pos))
            created+=1
        con.commit()
    build()
    print(f'Created {created} starter albums from actual tags; existing albums were preserved.')


def status():
    with db_connect() as con:
        for table in ['posts','photos','hashtags','post_hashtags','albums','album_posts']:
            print(f'{table}: {con.execute("SELECT COUNT(*) FROM "+table).fetchone()[0]}')
    print(f'Database stored locally at: {DB.relative_to(ROOT)}')


def main():
    parser=argparse.ArgumentParser(description='Manage the photo collection in SQLite and build static gallery data.')
    sub=parser.add_subparsers(dest='command',required=True)
    instagram=sub.add_parser('import-instagram',help='Import your own Instagram JSON export ZIP, with post media')
    instagram.add_argument('archive',type=Path)
    instagram.add_argument('--include-unlinked',action='store_true',help='Also include image files not linked by JSON (as untagged).')
    csv_parser=sub.add_parser('import-csv',help='Import manually curated photo sets from CSV')
    csv_parser.add_argument('csv_file',type=Path)
    sub.add_parser('build',help='Export SQL data to web-ready JSON and JS')
    sub.add_parser('status',help='Show saved SQL record counts')
    sub.add_parser('seed-albums',help='Create optional starter albums based on existing hashtags; keeps curated albums')
    args=parser.parse_args()
    try:
        if args.command=='import-instagram':import_instagram(args.archive, args.include_unlinked)
        elif args.command=='import-csv':import_csv(args.csv_file)
        elif args.command=='build':build()
        elif args.command=='status':status()
        elif args.command=='seed-albums':seed_albums()
    except (ValueError,FileNotFoundError,PermissionError,RuntimeError) as error:
        print(f'Error: {error}',file=sys.stderr)
        sys.exit(1)

if __name__=='__main__':main()
