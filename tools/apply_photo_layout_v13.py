#!/usr/bin/env python3
"""Update V13 homepage Photography layout without changing Gallery/Admin/database.

Run from the project's root: python3 tools/apply_photo_layout_v13.py
Creates backups in ignored local/photo-layout-backups/ before writing.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
JS = ROOT / 'portfolio.js'
CSS = ROOT / 'portfolio-site.css'

START = "    }else if(sec.kind==='photography'){"
END = "    }else if(sec.kind==='contact'){"
ORIGINAL_CSS = ".featured-photo-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:23px}"
NEW_CSS = ".featured-photo-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:0}"
CSS_MARKER = '/* V13 homepage Photography: featured images above a simple See More Photos link. */'

NEW_BLOCK = '''    }else if(sec.kind==='photography'){
      // Show just the Admin-selected photographs above a gallery link.
      // No content or Featured Photo selections are changed in Local Admin.
      const featuredPhotos=(window.PORTFOLIO_GALLERY?.featured_photos||[]).slice(0,3);
      const imgUrl=src=>/^photos\\/[a-zA-Z0-9_-]+\\.(?:jpg|jpeg|png|webp)$/i.test(src||'')||/^photos\\/thumbs\\/[a-zA-Z0-9_-]+\\.webp$/i.test(src||'')?src:'';
      const cards=featuredPhotos.map(p=>{
        const thumb=imgUrl(p.thumb)||imgUrl(p.src),original=imgUrl(p.src);
        if(!thumb||!original)return '';
        return `<a class="featured-photo" href="photography.html" aria-label="Explore photography: ${line(p.title)}"><img src="${escapeHtml(thumb)}" data-full-src="${escapeHtml(original)}" alt="${line(p.alt)}" loading="lazy" decoding="async" width="640" height="640"><span>${line(p.title)}</span></a>`;
      }).filter(Boolean).join('');
      inner=`${cards?`<div class="featured-photo-grid" aria-label="Featured photographs">${cards}</div>`:''}<div class="photography-view-more"><a class="button button-primary" href="photography.html">See More Photos →</a></div>`;
'''

CSS_APPEND = '''
''' + CSS_MARKER + '''
.photography-view-more{display:flex;justify-content:center;margin-top:24px}
.photography-view-more .button{display:inline-flex;align-items:center;justify-content:center;min-height:48px;max-width:100%}
@media(max-width:520px){.photography-view-more .button{width:100%}}
'''


def main():
    if not JS.is_file() or not CSS.is_file():
        raise RuntimeError('Cannot find portfolio.js and portfolio-site.css. Run in the Portfolio project with the V13 files installed.')

    js = JS.read_text(encoding='utf-8')
    css = CSS.read_text(encoding='utf-8')

    if 'class="photography-view-more"' in js and CSS_MARKER in css:
        print('Photography layout is already updated. No changes made.')
        return
    if 'class="photography-view-more"' in js or CSS_MARKER in css:
        raise RuntimeError('A partial photo layout update was detected. No files changed; inspect existing files first.')
    if js.count(START) != 1 or js.count(END) != 1:
        raise RuntimeError('V13 Photography section was not found exactly once. No files changed.')
    a = js.index(START)
    b = js.index(END, a)
    original_section = js[a:b]
    if not ('featuredPhotos' in original_section and 'featured-photo-grid' in original_section):
        raise RuntimeError('Photography section differs from expected V13. No files changed.')
    if ORIGINAL_CSS not in css:
        raise RuntimeError('Featured Photo CSS differs from expected V13. No files changed.')

    modified_js = js[:a] + NEW_BLOCK + js[b:]
    modified_css = css.replace(ORIGINAL_CSS, NEW_CSS, 1) + CSS_APPEND

    backup_dir = ROOT / 'local' / 'photo-layout-backups' / datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(JS, backup_dir / JS.name)
    shutil.copy2(CSS, backup_dir / CSS.name)
    JS.write_text(modified_js, encoding='utf-8')
    CSS.write_text(modified_css, encoding='utf-8')
    print('Updated homepage Photography layout.')
    print(' - Featured Photos first (up to 3, from existing Gallery Admin)')
    print(' - See More Photos button below')
    print(' - Removed homepage Photography introduction banner only')
    print(' - Gallery Admin and SQLite unchanged')
    print('Backups:', backup_dir)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('ERROR:', exc, file=sys.stderr)
        sys.exit(1)
