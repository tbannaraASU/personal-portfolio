#!/usr/bin/env python3
"""Optional, guarded cleanup of obsolete root-level version READMEs."""
import argparse
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OBSOLETE=[
    'README_PORTFOLIO_ONLY_TH.md',
    'README_V9_TH.md',
    'README_V10_TH.md',
    'README_V12_PROJECTS_TH.md',
    'README_V13_TH.md',
]


def git(*args):
    return subprocess.run(['git',*args], cwd=ROOT, text=True, capture_output=True)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Stage removal of checked obsolete README files')
    a=parser.parse_args()
    existing=[n for n in OBSOLETE if (ROOT/n).is_file() and git('ls-files','--error-unmatch','--',n).returncode==0]
    print('Tracked legacy README files:')
    for n in existing: print('  ',n)
    if not existing: print('  (none)');return 0
    dirty=[n for n in existing if git('status','--porcelain','--',n).stdout.strip()]
    # Look for inbound mentions in other tracked files, excluding the files being removed.
    references=[]
    tracked=git('ls-files','-z').stdout.split('\0')
    for name in tracked:
        if not name or name in existing or name == 'tools/cleanup_readmes_v15.py': continue
        path=ROOT/name
        if not path.is_file() or path.stat().st_size>500_000 or path.suffix.lower() not in {'.md','.html','.js','.py','.txt','.json'}:continue
        try: s=path.read_text(encoding='utf-8')
        except (UnicodeDecodeError,OSError):continue
        for old in existing:
            if old in s: references.append(f'{name} references {old}')
    for issue in references:print('REFERENCE:',issue)
    for name in dirty:print('CHANGED LOCALLY:',name)
    if dirty or references:
        print('Stopped: resolve references/local changes before removal.')
        return 2
    if not a.apply:
        print('Preview only. To stage these deletions: python tools/cleanup_readmes_v15.py --apply')
        return 0
    result=git('rm','--',*existing)
    if result.returncode:
        print('git rm failed:',result.stderr.strip());return result.returncode
    print('Staged deletion of',len(existing),'outdated README files. Nothing pushed or merged.')
    return 0

if __name__=='__main__':raise SystemExit(main())
