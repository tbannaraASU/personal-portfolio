#!/usr/bin/env python3
"""Local-only photography gallery manager. No Instagram or cloud access.

Start: python3 tools/admin_server.py
Visit: http://127.0.0.1:8765/admin
The editor saves in SQLite, updates static gallery-data.js, and strips EXIF from uploads.
"""
from __future__ import annotations

from datetime import date
from email.parser import BytesParser
from email.policy import default
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import io
import json
from pathlib import Path
import re
import secrets
import sys
from urllib.parse import urlsplit
from uuid import uuid4
import sqlite3

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from gallery import ROOT, db_connect, build, store_post, tags_from_caption, safe_image_write, valid_permalink, clean_title
import portfolio as cms

HOST = '127.0.0.1'
PORT = 8765
TOKEN = secrets.token_urlsafe(32)
MAX_BODY = 80 * 1024 * 1024
MAX_FILES = 12
MAX_FILE = 20 * 1024 * 1024
ALLOWED = {'.jpg', '.jpeg', '.png', '.webp'}


def parse_tags(s):
    """Support '#street #film' or 'street, film' or mixed hashtags in caption."""
    normalized = []
    for raw in re.split(r'[,\s]+', s or ''):
        raw = raw.strip().lstrip('#')
        if raw and re.fullmatch(r'[\w]+', raw, re.UNICODE):
            normalized.append('#'+raw)
    return tags_from_caption(' '.join(normalized))[:40]


def maybe_date(v):
    v = str(v or '').strip()
    if not v:
        return ''
    return date.fromisoformat(v).isoformat()


def all_posts():
    with db_connect() as con:
        con.row_factory = __import__('sqlite3').Row
        rows = con.execute('SELECT id,title,caption,published_at,permalink FROM posts ORDER BY published_at DESC,id').fetchall()
        result = []
        for row in rows:
            tags = con.execute('SELECT h.tag FROM hashtags h JOIN post_hashtags ph ON ph.hashtag_id=h.id WHERE ph.post_id=? ORDER BY h.tag',(row['id'],)).fetchall()
            pics = con.execute('SELECT path FROM photos WHERE post_id=? ORDER BY position',(row['id'],)).fetchall()
            result.append({**dict(row),'hashtags':[x[0] for x in tags],
                           'photo_count':len(pics),'preview':pics[0][0] if pics else ''})
        return result


def all_albums():
    with db_connect() as con:
        con.row_factory = sqlite3.Row
        rows = con.execute('SELECT * FROM albums ORDER BY sort_order,title COLLATE NOCASE').fetchall()
        return [{**dict(a), 'post_ids':[p[0] for p in con.execute(
            'SELECT post_id FROM album_posts WHERE album_id=? ORDER BY position,post_id',(a['id'],))]}
            for a in rows]


def all_tags():
    with db_connect() as con:
        return [{'tag':tag,'count':cnt} for tag,cnt in con.execute("""SELECT h.tag,COUNT(ph.post_id) FROM hashtags h LEFT JOIN post_hashtags ph
             ON ph.hashtag_id=h.id GROUP BY h.id ORDER BY COUNT(ph.post_id) DESC,h.tag""")]


def normalized_tag(value):
    raw = str(value or '').strip().lstrip('#').casefold()
    if not raw or len(raw)>70 or not re.fullmatch(r'[\w]+',raw,re.UNICODE):
        raise ValueError('Hashtag must contain 1–70 letters, numbers or underscores.')
    return '#'+raw


def update_album_assignments(con, post_id, album_ids):
    """Membership is user-curated, not inferred from tags."""
    if not isinstance(album_ids,list) or len(album_ids)>200 or any(not isinstance(x,str) for x in album_ids):
        raise ValueError('Invalid album selections.')
    album_ids = list(dict.fromkeys(album_ids))
    existing = {a[0] for a in con.execute('SELECT id FROM albums')}
    if any(x not in existing for x in album_ids):
        raise ValueError('Album no longer exists. Refresh the manager.')
    con.execute('DELETE FROM album_posts WHERE post_id=?',(post_id,))
    for album_id in album_ids:
        next_pos = con.execute('SELECT COALESCE(MAX(position),-1)+1 FROM album_posts WHERE album_id=?',(album_id,)).fetchone()[0]
        con.execute('INSERT INTO album_posts(album_id,post_id,position) VALUES(?,?,?)',(album_id,post_id,next_pos))


def save_album(con, obj, new=False):
    title = str(obj.get('title','')).strip()[:90]
    if not title:
        raise ValueError('Please enter an album title.')
    description=str(obj.get('description','')).strip()[:400]
    post_ids=obj.get('post_ids',[])
    if not isinstance(post_ids,list) or len(post_ids)>2000 or any(not isinstance(x,str) for x in post_ids):
        raise ValueError('Invalid photo set selection.')
    post_ids=list(dict.fromkeys(post_ids))
    known={p[0] for p in con.execute('SELECT id FROM posts')}
    if any(pid not in known for pid in post_ids):
        raise ValueError('A selected photo set no longer exists.')
    cover=str(obj.get('cover_post_id','')).strip()
    if cover and cover not in post_ids:
        raise ValueError('Choose an album cover from the selected photo sets.')
    aid='album-'+uuid4().hex[:16] if new else str(obj.get('id','')).strip()
    if new:
        order=con.execute('SELECT COALESCE(MAX(sort_order),-1)+1 FROM albums').fetchone()[0]
        con.execute('INSERT INTO albums(id,title,description,cover_post_id,sort_order) VALUES(?,?,?,?,?)',(aid,title,description,cover,order))
    else:
        cur=con.execute('UPDATE albums SET title=?,description=?,cover_post_id=? WHERE id=?',(title,description,cover,aid))
        if cur.rowcount==0:
            raise ValueError('Album not found.')
    con.execute('DELETE FROM album_posts WHERE album_id=?',(aid,))
    for pos,pid in enumerate(post_ids):
        con.execute('INSERT INTO album_posts(album_id,post_id,position) VALUES(?,?,?)',(aid,pid,pos))
    return aid


class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,directory=str(ROOT),**kwargs)

    def _json(self, data, status=200):
        b=json.dumps(data,ensure_ascii=False).encode('utf8')
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(b)))
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.end_headers();self.wfile.write(b)

    def _host_ok(self):
        return self.headers.get('Host','') in {f'{HOST}:{PORT}', f'localhost:{PORT}'}

    def do_GET(self):
        if not self._host_ok():
            return self._json({'error':'Invalid host'},403)
        path=urlsplit(self.path).path
        if path in {'/admin','/admin/','/admin/portfolio','/admin/portfolio/'}:
            html=(ROOT/'tools'/('portfolio_admin.html' if path.startswith('/admin/portfolio') else 'photo_admin.html')).read_text(encoding='utf8')
            html=html.replace('__LOCAL_SESSION_TOKEN__',TOKEN)
            b=html.encode('utf8')
            self.send_response(200)
            self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header('Content-Length',str(len(b)))
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Frame-Options','DENY')
            self.end_headers(); self.wfile.write(b)
            return
        if path=='/api/portfolio':
            return self._json(cms.dump())
        if path=='/api/posts':
            return self._json({'posts':all_posts()})
        if path=='/api/albums':
            return self._json({'albums':all_albums()})
        if path=='/api/tags':
            return self._json({'tags':all_tags()})
        if path=='/api/status':
            posts=all_posts();return self._json({'posts':len(posts),'photos':sum(p['photo_count'] for p in posts)})
        if path.startswith(('/local/','/tools/','/.git','/.venv/')) or path in {'/.gitignore','/.env'}:
            return self.send_error(404)
        return super().do_GET()

    def do_POST(self):
        if not self._host_ok() or self.headers.get('X-Gallery-Token')!=TOKEN:
            return self._json({'error':'Not authorized; open the local /admin page.'},403)
        try:
            body_length=int(self.headers.get('Content-Length','0'))
            if body_length<=0 or body_length>MAX_BODY:
                raise ValueError('Upload too large (max 80 MB per request).')
            path=urlsplit(self.path).path
            if path.startswith('/api/portfolio/'):
                req=json.loads(self.rfile.read(body_length).decode('utf8'))
                if not isinstance(req,dict):
                    raise ValueError('Expected JSON object.')
                if path=='/api/portfolio/section/create':
                    ident=cms.save_section(req,new=True)
                elif path=='/api/portfolio/section/update':
                    ident=cms.save_section(req,new=False)
                elif path=='/api/portfolio/section/delete':
                    cms.delete_section(req.get('id'))
                    ident=req.get('id')
                elif path=='/api/portfolio/item/create':
                    ident=cms.save_item(req,new=True)
                elif path=='/api/portfolio/item/update':
                    ident=cms.save_item(req,new=False)
                elif path=='/api/portfolio/item/delete':
                    cms.delete_item(req.get('id'))
                    ident=req.get('id')
                elif path=='/api/portfolio/move':
                    cms.move('portfolio_sections' if req.get('type')=='section' else 'portfolio_items',str(req.get('id')),req.get('direction'))
                    ident=req.get('id')
                else:
                    return self._json({'error':'Unknown portfolio operation.'},404)
                return self._json({'ok':True,'id':ident})
            if path=='/api/add':
                ctype=self.headers.get('Content-Type','')
                if not ctype.startswith('multipart/form-data;'):
                    raise ValueError('Expected multipart form data.')
                # email parser handles quoted filenames and UTF-8 fields with stdlib.
                raw=(b'Content-Type: '+ctype.encode('utf8')+b'\r\nMIME-Version: 1.0\r\n\r\n'+self.rfile.read(body_length))
                msg=BytesParser(policy=default).parsebytes(raw)
                if not msg.is_multipart():
                    raise ValueError('Upload was not multipart form data.')
                fields={}; images=[]
                for part in msg.iter_parts():
                    if part.get_content_disposition()!='form-data':
                        continue
                    key=part.get_param('name',header='content-disposition')
                    data=part.get_payload(decode=True) or b''
                    if key=='photos':
                        filename=part.get_filename() or ''
                        suffix=Path(filename).suffix.lower()
                        if suffix not in ALLOWED:
                            raise ValueError('Photos must be JPG, PNG, or WebP.')
                        if len(data)>MAX_FILE or not data:
                            raise ValueError('One photo is empty or exceeds 20 MB.')
                        try:
                            with Image.open(io.BytesIO(data)) as im:
                                im.verify()
                        except Exception as e:
                            raise ValueError(f'Invalid image: {filename}') from e
                        images.append((suffix,data))
                    elif key in {'title','caption','hashtags','date','permalink','album_ids'}:
                        fields[key]=data.decode('utf8','replace')
                if not images or len(images)>MAX_FILES:
                    raise ValueError('Choose 1–12 images for one photo set.')
                title=fields.get('title','').strip()[:110]
                caption=fields.get('caption','').strip()[:3000]
                published_at=maybe_date(fields.get('date',''))
                tags=list(dict.fromkeys(tags_from_caption(caption)+parse_tags(fields.get('hashtags',''))))[:40]
                rid='custom-'+uuid4().hex[:18]
                saved=[]
                for position,(suffix,data) in enumerate(images,1):
                    image_path=safe_image_write(data,rid,position,suffix)
                    if image_path is None:
                        raise ValueError('Could not save uploaded image')
                    saved.append(image_path)
                with db_connect() as con:
                    store_post(con,{'id':rid,'title':title or clean_title(caption,published_at),
                                    'caption':caption,'published_at':published_at,
                                    'permalink':valid_permalink(fields.get('permalink','')),
                                    'photos':saved,'hashtags':tags})
                    chosen=json.loads(fields.get('album_ids','[]'))
                    update_album_assignments(con,rid,chosen)
                    con.commit()
                build()
                return self._json({'ok':True,'id':rid,'photos':len(saved),'hashtags':tags})
            if path=='/api/edit':
                req=json.loads(self.rfile.read(body_length).decode('utf8'))
                rid=str(req.get('id',''))
                with db_connect() as con:
                    con.row_factory=__import__('sqlite3').Row
                    row=con.execute('SELECT * FROM posts WHERE id=?',(rid,)).fetchone()
                    if not row:
                        raise ValueError('Photo set not found.')
                    current_images=[x[0] for x in con.execute('SELECT path FROM photos WHERE post_id=? ORDER BY position',(rid,)).fetchall()]
                    title=str(req.get('title','')).strip()[:110] or 'Untitled photo set'
                    caption=str(req.get('caption','')).strip()[:3000]
                    published_at=maybe_date(req.get('date',''))
                    # Explicit admin tags are authoritative; manual renames must not be undone
                    # by hashtags still present in the original Instagram caption.
                    tags=parse_tags(req.get('hashtags',''))[:40]
                    store_post(con,{'id':rid,'title':title,'caption':caption,'published_at':published_at,
                                    'permalink':valid_permalink(req.get('permalink','')),
                                    'photos':current_images,'hashtags':tags})
                    if 'album_ids' in req:
                        update_album_assignments(con,rid,req['album_ids'])
                    con.commit()
                build()
                return self._json({'ok':True,'id':rid,'hashtags':tags})
            if path in {'/api/album/create','/api/album/update','/api/album/delete',
                        '/api/tag/create','/api/tag/rename','/api/tag/delete'}:
                req=json.loads(self.rfile.read(body_length).decode('utf8'))
                if not isinstance(req,dict):
                    raise ValueError('Expected JSON object.')
                with db_connect() as con:
                    if path=='/api/album/create':
                        ident=save_album(con,req,new=True)
                    elif path=='/api/album/update':
                        ident=save_album(con,req)
                    elif path=='/api/album/delete':
                        ident=str(req.get('id',''))
                        cur=con.execute('DELETE FROM albums WHERE id=?',(ident,))
                        if cur.rowcount==0:raise ValueError('Album not found.')
                    elif path=='/api/tag/create':
                        ident=normalized_tag(req.get('tag'))
                        con.execute('INSERT OR IGNORE INTO hashtags(tag) VALUES(?)',(ident,))
                    elif path=='/api/tag/rename':
                        original=normalized_tag(req.get('old'))
                        ident=normalized_tag(req.get('new'))
                        source=con.execute('SELECT id FROM hashtags WHERE tag=?',(original,)).fetchone()
                        if not source:raise ValueError('Original tag not found.')
                        target=con.execute('SELECT id FROM hashtags WHERE tag=?',(ident,)).fetchone()
                        if target and target[0]!=source[0]:
                            # Merge assignments without losing existing tag-post relations.
                            con.execute('INSERT OR IGNORE INTO post_hashtags(post_id,hashtag_id) SELECT post_id,? FROM post_hashtags WHERE hashtag_id=?',(target[0],source[0]))
                            con.execute('DELETE FROM hashtags WHERE id=?',(source[0],))
                        else:
                            con.execute('UPDATE hashtags SET tag=? WHERE id=?',(ident,source[0]))
                    elif path=='/api/tag/delete':
                        ident=normalized_tag(req.get('tag'))
                        cur=con.execute('DELETE FROM hashtags WHERE tag=?',(ident,))
                        if cur.rowcount==0:raise ValueError('Hashtag not found.')
                    con.commit()
                build()
                return self._json({'ok':True,'id':ident})
            return self._json({'error':'Unknown action'},404)
        except (ValueError, OSError, RuntimeError, json.JSONDecodeError) as e:
            return self._json({'error':str(e)},400)
        except Exception as e:
            print(f'Server error: {e}', file=sys.stderr)
            return self._json({'error':'Unexpected error; see Terminal for details.'},500)


if __name__=='__main__':
    cms.build()
    print(f'Gallery Manager: http://{HOST}:{PORT}/admin')
    print(f'Portfolio Editor: http://{HOST}:{PORT}/admin/portfolio')
    print('Only accessible from this Mac. Stop with Control+C.')
    server=ThreadingHTTPServer((HOST,PORT),Handler)
    try:server.serve_forever()
    except KeyboardInterrupt:print('\nStopped.')
    finally:server.server_close()
