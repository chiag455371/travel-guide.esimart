# -*- coding: utf-8 -*-
"""Patch today's 9 new articles: related sections, breadcrumbs; update sitemap."""
import os, glob, re

BASE = 'https://travel-guide-esimart.pages.dev'
NEW = ['kr-pocha-street', 'jp-tokyo-meiji-jingu', 'jp-osaka-namba', 'jp-tokyo-imperial',
       'oce-roto-geothermal', 'jp-shikoku-temple', 'tw-yehliu-geopark',
       'jp-okinawa-remm', 'jp-okinawa-yaeyama']

# titles + seeds for all non-redirect articles
titles = {}
for f in glob.glob('articles/*.html'):
    slug = os.path.basename(f)[:-5]
    c = open(f, encoding='utf-8').read()
    if 'http-equiv' in c and len(c) < 500:
        continue
    m = re.search(r'<title>([^<]+)</title>', c)
    t = (m.group(1) if m else slug).split('｜')[0].strip()
    og = re.search(r'og:image" content="https://picsum\.photos/seed/(\d+)/', c)
    titles[slug] = (t, og.group(1) if og else None)

def related_for(slug, n=4):
    prefix = slug.split('-')[0]
    parts = slug.split('-')
    same_tag = [s for s in titles if s != slug and s.split('-')[0] == prefix
                and len(s.split('-')) >= 2 and s.split('-')[1] == parts[1]]
    others = [s for s in titles if s != slug and s.split('-')[0] == prefix and s not in same_tag]
    picked = same_tag[:n]
    rest = [s for s in others if s not in picked]
    while len(picked) < n and rest:
        picked.append(rest.pop(0))
    return picked[:n]

REGION_NAMES = {'jp': '日本攻略', 'kr': '韓國攻略', 'tw': '台灣攻略', 'eu': '歐洲攻略', 'oce': '大洋洲攻略'}

patched = 0
for slug in NEW:
    f = f'articles/{slug}.html'
    c = open(f, encoding='utf-8').read()
    need_rel = 'related-section' not in c
    need_crumb = 'breadcrumb' not in c
    if not need_rel and not need_crumb:
        patched += 1
        continue

    if need_rel:
        rel = related_for(slug)
        cards = []
        for s in rel:
            t, seed = titles.get(s, (s, None))
            seed = seed or '100000'
            cards.append(
                f'      <a href="{BASE}/articles/{s}.html" class="related-card">'
                f'<div class="card-img-wrapper"><img class="card-img" '
                f'src="https://picsum.photos/seed/{seed}/600/400" alt="{t}" loading="lazy"></div>'
                f'<div class="card-body"><span class="card-title">{t}</span></div></a>')
        section = ('\n<div class="related-section">\n  <h2>延伸閱讀</h2>\n'
                  '  <div class="related-grid">\n' + '\n'.join(cards) + '\n  </div>\n</div>\n')
        c = c.replace('</body>', section + '</body>')

    if need_crumb:
        region = slug.split('-')[0]
        rn = REGION_NAMES.get(region, region)
        title = re.search(r'<title>([^<]+)</title>', c).group(1).split('｜')[0][:30]
        crumb = (
            f'<nav aria-label="breadcrumb" class="breadcrumb-nav"><ol class="breadcrumb">'
            f'<li><a href="{BASE}/">首頁</a></li>'
            f'<li><a href="{BASE}/articles/{region}.html">{rn}</a></li>'
            f'<li aria-current="page">{title}</li></ol></nav>')
        bm = re.search(r'<h1>[^<]+</h1>', c)
        if bm:
            c = c[:bm.end()] + '\n' + crumb + c[bm.end():]

    open(f, 'w', encoding='utf-8').write(c)
    patched += 1

print(f'new articles patched: {patched}/{len(NEW)}')

# sitemap update
sm = open('sitemap.xml', encoding='utf-8').read()
lines = sm.rstrip().split('\n')
added = 0
for slug in NEW:
    url = f'{BASE}/articles/{slug}.html'
    if url not in sm:
        lines.insert(len(lines) - 1, f'<url><loc>{url}</loc><lastmod>2026-09-14</lastmod></url>')
        added += 1
open('sitemap.xml', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print(f'sitemap: added {added} new URLs')
