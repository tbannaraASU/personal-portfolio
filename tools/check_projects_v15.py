#!/usr/bin/env python3
"""Review public case study fields. Never invent missing outcomes or screenshots."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECOMMENDED = [
    ('summary', 'short project summary'),
    ('period', 'timeline'),
    ('role', 'your role / team'),
    ('skills', 'skills / technologies'),
    ('details', 'overview'),
    ('challenge', 'problem / challenge'),
    ('approach', 'approach / solution'),
    ('results', 'verified results / impact'),
    ('images', 'real screenshots'),
]

def main():
    path = ROOT / 'data/portfolio.json'
    if not path.is_file():
        print('data/portfolio.json missing. Run: python tools/portfolio.py build')
        return 1
    data = json.loads(path.read_text(encoding='utf-8'))
    projects = next((s.get('items', []) for s in data.get('sections', []) if s.get('kind') == 'projects'), [])
    visible = [p for p in projects if p.get('enabled', True)]
    print(f'Published project case studies: {len(visible)}')
    for p in visible:
        missing = [label for field, label in RECOMMENDED if not str(p.get(field) or '').strip()]
        print('\n' + str(p.get('title') or p.get('id') or '(untitled)'))
        print('  Featured:', str(p.get('featured', 'Not featured')))
        print('  Recommended fields populated:', str(len(RECOMMENDED) - len(missing)) + '/' + str(len(RECOMMENDED)))
        print('  Review:', ', '.join(missing) if missing else 'all recommended fields populated')
        if 'progress' in str(p.get('status', '')).lower():
            print('  Note: use verified milestones; do not claim finished results for work in progress.')
    print('\nSuggestions only. Update fields in Local Admin; no database changes were made.')
    return 0

if __name__ == '__main__': raise SystemExit(main())
