# -*- coding: utf-8 -*-
import re, pathlib
from collections import Counter
for r in ['jp','kr','tw','eu','oce']:
    t = pathlib.Path('articles/%s.html' % r).read_text(encoding='utf-8')
    imgs = re.findall(r'card-img\" src=\"([^\"]+)\"', t)
    c = Counter(imgs)
    top = c.most_common(4)
    print(r, 'cards:', len(imgs), 'unique:', len(c), '| dup:', [(n, u.split('/')[-1][:40]) for u,n in top])
print('---')
t = pathlib.Path('guides/tw-esim-guide.html').read_text(encoding='utf-8')
print('guide css:', re.findall(r'href=\"([^\"]*style\.css[^\"]*)\"', t))
print('guide breadcrumb:', 'breadcrumb' in t.lower())
idx = pathlib.Path('index.html').read_text(encoding='utf-8')
print('index css:', re.findall(r'href=\"([^\"]*style\.css[^\"]*)\"', idx))
