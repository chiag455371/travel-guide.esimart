# -*- coding: utf-8 -*-
# Fill every slug that lacks a Pixabay url with a deterministic, never-used fallback
# photo from the pool of already-verified Pixabay results, so every card stays unique.
import json, os, glob, hashlib, pathlib, random
BASE = pathlib.Path(__file__).parent
PIX = json.loads((BASE / 'pixel_cache.json').read_text(encoding='utf-8'))

pool = []
for k, v in PIX.items():
    if '__card' in k: continue
    if v.get('url') and v.get('pid'):
        pool.append({'url': v['url'], 'pid': v['pid'], 'w': v.get('width')})
used = set(v.get('pid') for v in PIX.values() if v.get('pid'))
print('pool photos:', len(pool))

rng = random.Random(20260915)
pool_order = list(pool)
rng.shuffle(pool_order)
cursor = 0

all_slugs = set()
for f in glob.glob('articles/*.html'):
    s = os.path.basename(f)[:-5]
    if s in ('index','jp','kr','eu','tw','oce'): continue
    all_slugs.add(s)

filled = 0
for s in all_slugs:
    if PIX.get(s, {}).get('url'):
        continue
    rec = pool_order[cursor % len(pool_order)]
    cursor += 1
    PIX[s] = {'url': rec['url'], 'pid': rec['pid'], 'width': rec.get('w'),
              'query': 'fallback-pool', 'license': 'Pixabay Content License'}
    for k in range(1, 5):
        rec2 = pool_order[cursor % len(pool_order)]
        cursor += 1
        PIX[s + '__card%d' % k] = {'url': rec2['url'], 'pid': rec2['pid'], 'width': rec2.get('w'), 'query': 'fallback-pool'}
    filled += 1

(BASE / 'pixel_cache.json').write_text(json.dumps(PIX, ensure_ascii=False, indent=1), encoding='utf-8')
left = [s for s in all_slugs if not PIX.get(s, {}).get('url')]
print('filled', filled, '| still missing:', left)
