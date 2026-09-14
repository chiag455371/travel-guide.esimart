# -*- coding: utf-8 -*-
"""Verify live site: first card in each region page matches that article's og:image seed."""
import urllib.request, re, time

BASE = 'https://travel-guide-esimart.pages.dev'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
CARD = re.compile(
    r'/articles/([a-z0-9\-]+)\.html" class="article-card">\s*'
    r'<div class="card-img-wrapper"><img class="card-img" src="https://picsum\.photos/seed/(\d+)/')
OG = re.compile(r'og:image" content="https://picsum\.photos/seed/(\d+)/')

checked = mismatch = 0
for region in ['kr.html', 'jp.html', 'tw.html', 'eu.html', 'oce.html', 'index.html']:
    req = urllib.request.Request(BASE + '/articles/' + region, headers=HEADERS)
    page = urllib.request.urlopen(req).read().decode('utf-8', 'replace')
    ms = CARD.findall(page)
    if not ms:
        print(region, 'NO CARDS FOUND')
        continue
    slug, card_seed = ms[0]
    req2 = urllib.request.Request(BASE + '/articles/' + slug + '.html', headers=HEADERS)
    own = OG.search(urllib.request.urlopen(req2).read().decode('utf-8', 'replace'))
    checked += 1
    match = own and own.group(1) == card_seed
    if not match:
        mismatch += 1
        print('MISMATCH', region, slug, 'card=' + card_seed, 'og=', own.group(1) if own else '?')
    time.sleep(0.3)
print(f'spot-checked {checked} pages, {mismatch} mismatches')
