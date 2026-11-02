#!/usr/bin/env python3
"""Enable or disable optional Cloudflare Web Analytics. Token is public, not an API secret."""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'assets' / 'v15-analytics-config.js'

def main():
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--token', help='32-character site token provided by Cloudflare Web Analytics')
    g.add_argument('--disable', action='store_true')
    args = p.parse_args()
    token = '' if args.disable else args.token.strip()
    if token and not re.fullmatch(r'[a-fA-F0-9]{32}', token):
        p.error('Cloudflare site token must be 32 hexadecimal characters. Do not enter an API key or password.')
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text('/* Public Cloudflare Web Analytics site token; not an API secret. */\nwindow.PORTFOLIO_V15_CF_TOKEN = '+repr(token)+';\n', encoding='utf-8')
    print('Analytics:', 'disabled' if not token else 'configured (review files before publishing)')
    print('Updated:', TARGET.relative_to(ROOT))

if __name__ == '__main__': main()
