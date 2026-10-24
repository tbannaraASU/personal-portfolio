#!/usr/bin/env python3
"""Read-only GitHub Pages availability checks. Does not modify remote repository."""
from urllib.request import Request,urlopen
from urllib.error import URLError,HTTPError
from urllib.parse import urljoin
import json
import sys
BASE=(sys.argv[1] if len(sys.argv)>1 else 'https://tbannaraasu.github.io/personal-portfolio/').rstrip('/')+'/'
paths=['index.html','photography.html','tag.html?tag=%23filmphotography','album.html?id=film-stories','portfolio.js','photography.js','data/gallery-data.js','data/portfolio-data.js']
failed=[]
for path in paths:
    url=urljoin(BASE,path)
    try:
        with urlopen(Request(url,headers={'User-Agent':'PortfolioQA/1.0'}),timeout=12) as resp:
            status=resp.status
            content=resp.read(3500000)
        label='PASS' if status==200 else 'FAIL'
        if status!=200:failed.append(path)
        if path.endswith('knowledge.json'):
            json.loads(content)
        print(f'{label:4s} {status} {path} ({len(content)}+ bytes sampled)')
    except (HTTPError,URLError,TimeoutError,ValueError) as exc:
        failed.append(path)
        print(f'FAIL {path}: {type(exc).__name__} {exc}')
print('\nNote: HTTP checks cannot prove that Next/Previous and popup buttons work. Click them in the browser.')
if failed:
    print('Missing or unreachable paths:',', '.join(failed))
    sys.exit(1)
print('Public asset URL checks passed.')
