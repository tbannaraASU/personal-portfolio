#!/usr/bin/env python3
"""Build sitemap.xml from the public static pages and published portfolio/gallery exports."""
import json
import re
from pathlib import Path
from urllib.parse import quote, urlencode
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://tbannaraasu.github.io/personal-portfolio/'


def load_json(name):
    path = ROOT / 'data' / name
    try: return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError): return {}


def build():
    urls = []
    for name in ('index.html', 'projects.html', 'photography.html'):
        if (ROOT / name).exists(): urls.append(BASE + name)
    if (ROOT / 'project.html').exists():
        projects = next((s.get('items', []) for s in load_json('portfolio.json').get('sections', []) if s.get('kind') == 'projects' and s.get('enabled', True)), [])
        for p in projects:
            project_id = str(p.get('id', ''))
            if p.get('enabled', True) and re.fullmatch(r'item-[a-zA-Z0-9]+', project_id):
                urls.append(BASE + 'project.html?' + urlencode({'id': project_id}))
    gallery = load_json('gallery.json')
    if (ROOT / 'album.html').exists():
        for a in gallery.get('albums', []):
            if isinstance(a, dict) and a.get('id') and (a.get('posts') or a.get('post_ids') or a.get('photo_sets')):
                urls.append(BASE + 'album.html?' + urlencode({'id': str(a['id'])}))
    # Tag URLs are omitted automatically: tags may be generated dynamically and
    # no static HTML is rendered for each tag. They remain accessible via links.
    urls = list(dict.fromkeys(urls))
    body = '\n'.join('  <url><loc>' + escape(u) + '</loc></url>' for u in urls)
    text = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + '\n</urlset>\n'
    (ROOT / 'sitemap.xml').write_text(text, encoding='utf-8')
    print(f'Wrote sitemap.xml with {len(urls)} URLs')
    print('Submit:', BASE + 'sitemap.xml')
    print('Note: sitemap discovery is not an indexing guarantee.')

if __name__ == '__main__': build()
