# -*- coding: utf-8 -*-
import json, urllib.request, urllib.parse, time, pathlib, re
from collections import defaultdict
KEY = '39894189-8822531df0830fb07f58a9a69'
UA = {'User-Agent': 'Mozilla/5.0 travel-bot'}
PIX = json.loads(pathlib.Path('pixel_cache.json').read_text(encoding='utf-8'))

by_pid = defaultdict(list)
for k, v in PIX.items():
    if v.get('pid'):
        by_pid[v['pid']].append(k)
dup = {pid: s for pid, s in by_pid.items() if len(s) > 1}
print('dup pid groups (incl cards):', len(dup), '| entries:', sum(len(v) for v in dup.values()))

all_pids = set(PIX[k]['pid'] for k in PIX if PIX[k].get('pid'))
region_q = {'jp':'Japan','kr':'Korea','eu':'Europe','tw':'Taiwan','oce':'Australia'}
def search(q):
    for i in range(4):
        params = {'q': q, 'per_page': 40, 'image_type': 'photo', 'orientation': 'landscape'}
        url = 'https://pixabay.com/api/?key=%s&%s' % (KEY, urllib.parse.urlencode(params))
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read())
        except Exception:
            time.sleep(2 + i)
    return {}

fixed = 0
for pid, slugs in dup.items():
    for k in slugs[1:]:
        r = k.split('-')[0]
        q = PIX[k].get('query') or region_q.get(r, 'travel')
        d = search(q)
        cand = None
        for h in d.get('hits', []):
            if h['id'] not in all_pids and (h.get('imageWidth') or 0) >= 800:
                cand = h; break
        if not cand:
            d2 = search(region_q.get(r, 'scenery'))
            for h in d2.get('hits', []):
                if h['id'] not in all_pids and (h.get('imageWidth') or 0) >= 800:
                    cand = h; break
        if cand:
            PIX[k] = {'url': cand.get('largeImageURL') or cand.get('webformatURL'), 'pid': cand['id'],
                      'width': cand.get('imageWidth'), 'query': q, 'license': 'Pixabay Content License'}
            all_pids.add(cand['id']); fixed += 1
        time.sleep(0.35)
pathlib.Path('pixel_cache.json').write_text(json.dumps(PIX, ensure_ascii=False, indent=1), encoding='utf-8')
print('fixed entries:', fixed)
by_pid2 = defaultdict(list)
for k, v in PIX.items():
    if v.get('pid'):
        by_pid2[v['pid']].append(k)
still = {pid: s for pid, s in by_pid2.items() if len(s) > 1}
print('remaining dup groups:', len(still))
