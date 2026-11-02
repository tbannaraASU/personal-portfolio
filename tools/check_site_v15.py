#!/usr/bin/env python3
"""Static local quality checks. Does not replace Lighthouse, axe, or a real browser."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGES = ('index.html', 'projects.html', 'project.html', 'photography.html', 'tag.html', 'album.html', '404.html')

class Inspect(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs=[]; self.no_alt=[]; self.meta=set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'img' and 'alt' not in attrs: self.no_alt.append(self.getpos()[0])
        if tag == 'meta' and attrs.get('name') == 'description': self.meta.add('description')
        if tag in ('script', 'img', 'link', 'a'):
            ref = attrs.get('src') or attrs.get('href')
            if ref: self.refs.append((ref, self.getpos()[0]))

def main():
    warnings=[]; checked=0
    for name in PAGES:
        file=ROOT/name
        if not file.is_file():
            warnings.append(f'{name}: missing'); continue
        checked+=1; parser=Inspect(); parser.feed(file.read_text(encoding='utf-8'))
        if 'description' not in parser.meta: warnings.append(f'{name}: missing meta description')
        for lineno in parser.no_alt: warnings.append(f'{name}:{lineno}: image without alt attribute')
        for ref, lineno in parser.refs:
            url=urlsplit(ref)
            if url.scheme or url.netloc or ref.startswith(('//', '#', 'mailto:', 'tel:', 'data:')): continue
            path=unquote(url.path)
            if not path or path.endswith('/'): continue
            # JS-created/project dynamic links are not checked by this static parser.
            target=(file.parent/path).resolve()
            if not target.is_relative_to(ROOT.resolve()):
                warnings.append(f'{name}:{lineno}: path outside repository: {path}')
            elif target.suffix in ('.html','.css','.js','.png','.svg','.webp','.jpg','.jpeg','.ico') and not target.exists():
                warnings.append(f'{name}:{lineno}: missing local asset: {path}')
    required=['README.md','sitemap.xml','assets/v15-site.css','assets/v15-site.js','assets/v15-analytics-config.js']
    for file in required:
        if not (ROOT/file).is_file(): warnings.append(f'Missing V15 file: {file}')
    print(f'Checked {checked} HTML pages')
    if warnings:
        for msg in warnings: print('WARNING:', msg)
        print('Review warnings; some may be acceptable on a partially installed project.')
        return 1
    print('PASS: no missing static references or alt/description gaps detected in HTML source.')
    print('Note: rendered HTML and dynamic image data still need browser/Lighthouse testing.')
    return 0

if __name__=='__main__': sys.exit(main())
