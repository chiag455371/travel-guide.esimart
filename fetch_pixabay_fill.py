# -*- coding: utf-8 -*-
import json, re, os, glob, sys, urllib.request, urllib.parse, time, html, pathlib

BASE = pathlib.Path(__file__).parent
KEY = '39894189-8822531df0830fb07f58a9a69'
PIX = json.loads((BASE / 'pixel_cache.json').read_text(encoding='utf-8'))
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) travel-guide-bot/1.0'}

GENERIC = {'jp':'Japan mountain','kr':'Korea town','eu':'Europe old town','tw':'Taiwan town','oce':'Australia town'}

def q_for(slug):
    r = slug.split('-')[0]
    return GENERIC.get(r, r + ' travel town landscape')

used_pids = {v.get('pid') for v in PIX.values() if v.get('pid')}
slugs = sorted(s for s in PIX if s not in ('index',) and not s.split('-')[0] in ('jp','kr','eu','tw','oce') and s not in ('jp','kr','eu','tw','oce'))
missing = [s for s in slugs if s in PIX and not PIX[s].get('url')]
# also slugs not yet in cache at all
all_slugs = set()
for f in glob.glob('articles/*.html'):
    s = os.path.basename(f)[:-5]
    if s in ('index','jp','kr','eu','tw','oce'): continue
    all_slugs.add(s)
missing = [s for s in all_slugs if not PIX.get(s, {}).get('url')]
print('missing', len(missing))

for i, slug in enumerate(missing):
    q = q_for(slug)
    for attempt in range(4):
        try:
            params = {'q': q, 'per_page': 25, 'image_type': 'photo', 'orientation': 'landscape'}
            url = 'https://pixabay.com/api/?key=%s&%s' % (KEY, urllib.parse.urlencode(params))
            req = urllib.request.Request(url, headers=UA)
            d = json.loads(urllib.request.urlopen(req, timeout=25).read())
            break
        except Exception as e:
            if attempt == 3:
                print('fail', slug, str(e)[:50]); d = {}
            time.sleep(2)
    hits = [h for h in d.get('hits', []) if (h.get('imageWidth') or 0) >= 800 and h.get('id') not in used_pids]
    if not hits:
        print('no hits', slug, q); continue
    h = hits[0]
    PIX[slug] = {'url': h.get('largeImageURL') or h.get('webformatURL'), 'pid': h['id'],
                 'width': h.get('imageWidth'), 'query': q, 'license': 'Pixabay Content License'}
    used_pids.add(h['id'])
    for k in range(1, 5):
        h2 = hits[k] if k < len(hits) else None
        if h2:
            PIX[slug + '__card%d' % k] = {'url': h2.get('largeImageURL') or h2.get('webformatURL'), 'pid': h2['id'],
                                          'width': h2.get('imageWidth'), 'query': q}
            used_pids.add(h2['id'])
    if i % 15 == 0:
        print('progress', i, '/', len(missing))
        (BASE / 'pixel_cache.json').write_text(json.dumps(PIX, ensure_ascii=False, indent=1), encoding='utf-8')
    time.sleep(0.5)
(BASE / 'pixel_cache.json').write_text(json.dumps(PIX, ensure_ascii=False, indent=1), encoding='utf-8')
print('DONE missing fill')
