# -*- coding: utf-8 -*-
import json, pathlib, re, sys
from collections import Counter
PIX = json.loads(pathlib.Path('pixel_cache.json').read_text(encoding='utf-8'))
# verify: does jp.html actually show a dup image?
for r in ['jp','kr']:
    t = pathlib.Path('articles/%s.html' % r).read_text(encoding='utf-8')
    imgs = re.findall(r'src=\"(https://pixabay[^\"]+)\"', t)
    c = Counter(imgs)
    dup = {u: n for u, n in c.items() if n > 1}
    print(r, '| pix imgs:', len(imgs), '| distinct:', len(c), '| dup:', len(dup))
    for u, n in list(dup.items())[:5]:
        print('   x%d %s' % (n, u[-40:]))
        # which slugs use this url
        owners = [k for k, v in PIX.items() if v.get('url') == u]
        print('     owners:', owners[:6])
