# -*- coding: utf-8 -*-
"""Replace merged-source files with meta-refresh redirect pages
(CF Pages in this project isn't honoring _redirects; meta-refresh always works)."""
import os

REDIRECTS = {
    'jp-hiroshima-okunoshima': 'jp-hiroshima',
    'jp-hiroshima-itsukushima': 'jp-hiroshima',
    'jp-awaji-union': 'jp-awaji',
    'jp-nikko-shrine': 'jp-nikko-tobu',
    'eu-flanders-bruges': 'eu-bruges',
    'tw-luku-geopark': 'tw-luceat',
}
BASE = 'https://travel-guide-esimart.pages.dev'

for src, tgt in REDIRECTS.items():
    path = f'articles/{src}.html'
    html = (
        f'<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">'
        f'<meta http-equiv="refresh" content="0; url={BASE}/articles/{tgt}.html">'
        f'<link rel="canonical" href="{BASE}/articles/{tgt}.html">'
        f'<title>重定向中…</title></head>'
        f'<body><p>此文章已合併至 <a href="{BASE}/articles/{tgt}.html">{tgt}</a>。</p></body></html>'
    )
    open(path, 'w', encoding='utf-8').write(html)
    print(f'{src}.html -> meta-refresh to {tgt}.html')

print('done, count=', len(REDIRECTS))
