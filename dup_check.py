# -*- coding: utf-8 -*-
import re, pathlib, json
from collections import Counter
# check whether dup pairs are cover vs card1 (expected, not a real dup)
for r in ['jp','kr']:
    t = pathlib.Path('articles/%s.html' % r).read_text(encoding='utf-8')
    imgs = re.findall(r'src=\"(https://pixabay[^\"]+)\"', t)
    c = Counter(imgs)
    for u, n in c.items():
        if n > 1:
            print(r, 'x%d' % n, u[-45:])
