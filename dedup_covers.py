# -*- coding: utf-8 -*-
import json, urllib.request, urllib.parse, time, pathlib, re, sys, random
from collections import defaultdict

KEY = '39894189-8822531df0830fb07f58a9a69'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) travel-guide-bot/1.0'}
PIX = json.loads(pathlib.Path('pixel_cache.json').read_text(encoding='utf-8'))

# find pids used by more than 1 slug
by_pid = defaultdict(list)
for k, v in PIX.items():
    if '__card' not in k and v.get('pid'):
        by_pid[v['pid']].append(k)
dup_pids = [pid for pid, slugs in by_pid.items() if len(slugs) > 1]
print('dup pid groups:', len(dup_pids), '| slugs affected:', sum(len(v) for v in by_pid.values() if len(v)>1))

# fetch replacement distinct photos for each dup group
def search(q, tries=4):
    for i in range(tries):
        params = {'q': q, 'per_page': 25, 'image_type': 'photo', 'orientation': 'landscape'}
        url = 'https://pixabay.com/api/?key=%s&%s' % (KEY, urllib.parse.urlencode(params))
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read())
        except Exception as e:
            if i == 3:
                return None
            time.sleep(2)

unused = set(v.get('pid') for k, v in PIX.items() if '__card' in k and v.get('pid'))
unused -= set(dup_pids)

fixed = 0
for pid, slugs in [(pid, s) for pid, s in by_pid.items() if len(s) > 1]:
    for idx, slug in enumerate(slugs):
        q = PIX[slug].get('query') or slug
        d = search(q)
        cand = None
        if d:
            for h in d.get('hits', []):
                if h['id'] in unused or h['id'] in unused_pids if False else False:
                    pass
                if h.get('id') not in unused and (h.get('imageWidth') or 0) >= 800 and h.get('id') != pid:
                    cand = h
                    break
        if not cand:
            # fallback: any landscape photo of generic region, distinct
            d2 = search({'jp':'Japan mountain','kr':'Korea town','eu':'Europe town','tw':'Taiwan town','oce':'Australia town'}.get(slug.split('-')[0], 'travel landscape'))
            for h in (d2 or {}).get('hits', []):
                if h['id'] not in unused and (h.get('imageWidth') or 0) >= 800:
                    cand = h
                    break
        if cand:
            PIX[slug] = {'url': cand.get('largeImageURL') or cand.get('webformatURL'),
                         'pid': cand['id'], 'width': cand.get('imageWidth'), 'query': q, 'license': 'Pixabay Content License'}
            unused.add(cand['id'])
            fixed += 1
            # also refresh its card extras
            for k in range(1, 5):
                ck = slug + '__card%d' % k
                if ck in PIX and PIX[ck].get('pid') in by_pid and len(by_pid[PIX[ck].get('pid')]) > 1:
                    pass
        time.sleep(0.4)

pathlib.Path('pixel_cache.json').write_text(json.dumps(PIX, ensure_ascii=False, indent=1), encoding='utf-8')
print('fixed duplicate covers:', fixed)
# re-check
by_pid2 = defaultdict(list)
for k, v in PIX.items():
    if '__card' not in k and v.get('pid'):
        by_pid2[v['pid']].append(k)
still = {pid: s for pid, s in by_pid2.items() if len(s) > 1}
print('remaining dup pid groups:', len(still))
for pid, s in list(still.items())[:5]:
    print('  ', pid, s)
