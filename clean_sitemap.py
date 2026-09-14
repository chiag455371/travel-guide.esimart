# -*- coding: utf-8 -*-
import re, pathlib
SITE = 'https://travel-guide-esimart.pages.dev'
MERGED = ['jp-hiroshima-itsukushima','jp-hiroshima-miatu','jp-hiroshima-okunoshima',
          'jp-hiroshima-peace','jp-fukuoka-food','jp-kamakura-buddha','jp-himeji-castle']
p = pathlib.Path('sitemap.xml')
t = p.read_text(encoding='utf-8')
removed = 0
for slug in MERGED:
    # remove both <loc>...</loc> with/without scheme
    t = re.sub(r'<url><loc>%s/articles/%s\.html</loc>.*?</url>\n?' % (re.escape(SITE), slug), '', t, flags=re.S)
    t = re.sub(r'<url>\s*<loc>.*?/articles/%s\.html</loc>\s*.*?</url>\s*' % re.escape(slug), '', t, flags=re.S)
    removed += 1
p.write_text(t, encoding='utf-8')
# verify
left = 0
for slug in MERGED:
    left += len(re.findall(re.escape(slug), t))
print('entries removed (matches):', removed, '| still mentioned:', left)
for m in re.finditer(r'<url>.*?</url>', t, re.S):
    if any(s in m.group(0) for s in MERGED):
        print('LEAK:', m.group(0)[:100])
# sanity: main pages still in sitemap
for s in ['jp-hiroshima.html','jp-fukuoka.html','jp-kamakura.html','jp-himeji.html']:
    print(s, 'in sitemap:', s in t)
