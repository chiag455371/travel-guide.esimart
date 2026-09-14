# -*- coding: utf-8 -*-
"""Second-round duplicate merges: 10 same-location pairs.
Rule: keep the longer/more complete article; merge the shorter into it."""
import os, re, glob

# (source -> target)  target = keep, source = becomes redirect
MERGES = {
    'kr-bucheon': 'kr-bukchon',            # bukchon = real Bukchon name; bucheon variant
    'eu-berlin': 'eu-berlin-wall',        # wall version longer
    'tw-pingtung-ranch': 'tw-pingtung-orchid',  # orchid longer
    'kr-jeju': 'kr-jeju-city',            # city longer
    'kr-jeju-cafe': 'kr-jeju-city',
    'kr-jeju-jungmun': 'kr-jeju-city',
    'tw-nantou-lalu': 'tw-nantou-clear',  # clear longer
    'tw-shilin-old': 'tw-shilin-night',   # night longer
    'tw-kaohsiung-food': 'tw-kaohsiung-night',  # night longer
    'eu-amsterdam': 'eu-amsterdam-canal', # canal longer
    'eu-venice-gondola': 'eu-venice-canals',    # canals longer
    'oce-wellington': 'oce-wellington-museum',  # museum longer
}
BASE = 'https://travel-guide-esimart.pages.dev'

# 1. write meta-refresh pages for sources
for src, tgt in MERGES.items():
    path = f'articles/{src}.html'
    html = (
        f'<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">'
        f'<meta http-equiv="refresh" content="0; url={BASE}/articles/{tgt}.html">'
        f'<link rel="canonical" href="{BASE}/articles/{tgt}.html">'
        f'<title>重定向中…</title></head>'
        f'<body><p>此文章已合併至 <a href="{BASE}/articles/{tgt}.html">{tgt}</a>。</p></body></html>')
    open(path, 'w', encoding='utf-8').write(html)
    print(f'{src}.html -> redirect to {tgt}.html')

# 2. remove sources from sitemap
sm = open('sitemap.xml', encoding='utf-8').read()
lines = sm.split('\n')
removed = 0
new_lines = []
for line in lines:
    if any(f'/articles/{s}.html' in line for s in MERGES):
        removed += 1
    else:
        new_lines.append(line)
open('sitemap.xml', 'w', encoding='utf-8').write('\n'.join(new_lines))
print(f'sitemap: removed {removed} URLs')

# 3. update internal links in all files
all_files = glob.glob('articles/*.html') + ['index.html']
updated = 0
for fname in all_files:
    c = open(fname, encoding='utf-8').read()
    orig = c
    for src, tgt in MERGES.items():
        c = c.replace(f'/articles/{src}.html', f'/articles/{tgt}.html')
    if c != orig:
        open(fname, 'w', encoding='utf-8').write(c)
        updated += 1
print(f'internal links updated in {updated} files')

# 4. append _redirects lines
with open('_redirects', 'a', encoding='utf-8') as f:
    for src, tgt in MERGES.items():
        f.write(f'/articles/{src}.html 301 /articles/{tgt}.html\n')
print('_redirects appended')
