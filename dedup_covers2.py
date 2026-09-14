# -*- coding: utf-8 -*-
import json, urllib.request, urllib.parse, time, pathlib, sys
from collections import defaultdict
KEY = '39894189-8822531df0830fb07f58a9a69'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) travel-guide-bot/1.0'}
PIX = json.loads(pathlib.Path('pixel_cache.json').read_text(encoding='utf-8'))

by_pid = defaultdict(list)
for k, v in PIX.items():
    if '__card' not in k and v.get('pid'):
        by_pid[v['pid']].append(k)
dup = {pid: s for pid, s in by_pid.items() if len(s) > 1}
print('dup groups now:', len(dup))

region_q = {'jp':'Japan temple','kr':'Korea street','eu':'Europe city','tw':'Taiwan mountain','oce':'Australia reef'}
all_pids = set(v.get('pid') for v in PIX.values() if v.get('pid'))

import random
def search(q):
    for i in range(4):
        params = {'q': q, 'per_page': 40, 'image_type': 'photo', 'orientation': 'landscape'}
        url = 'https://pixabay.com/api/?key=%s&%s' % (KEY, urllib.parse.urlencode(params))
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read())
        except Exception as e:
            time.sleep(2 + i)
    return {}

fixed = 0
for pid, slugs in dup.items():
    random.shuffle(slugs)
    # keep the first slug on this pid; reassign the rest
    for slug in slugs[1:]:
        r = slug.split('-')[0]
        q = PIX[slug].get('query') or region_q.get(r, 'travel landscape')
        d = search(q)
        cand = None
        for h in d.get('hits', []):
            if h['id'] not in all_pids and (h.get('imageWidth') or 0) >= 800:
                cand = h
                break
        if not cand:
            d2 = search(region_q.get(r, 'travel'))
            for h in d2.get('hits', []):
                if h['id'] not in all_pids and (h.get('imageWidth') or 0) >= 800:
                    cand = h
                    break
        if cand:
            PIX[slug] = {'url': cand.get('largeImageURL') or cand.get('webformatURL'),
                         'pid': cand['id'], 'width': cand.get('imageWidth'), 'query': q, 'license': 'Pixabay Content License'}
            all_pids.add(cand['id'])
            fixed += 1
        else:
            print('no cand', slug)
        time.sleep(0.4)

pathlib.Path('pixel_cache.json').write_text(json.dumps(PIX, ensure_ascii=False, indent=1), encoding='utf-8')
print('fixed:', fixed)
by_pid2 = defaultdict(list)
for k, v in PIX.items():
    if '__card' not in k and v.get('pid'):
        by_pid2[v['pid']].append(k)
still = {pid: s for pid, s in by_pid2.items() if len(s) > 1}
print('remaining dup groups:', len(still))
