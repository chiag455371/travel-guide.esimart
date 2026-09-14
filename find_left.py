# -*- coding: utf-8 -*-
import re, pathlib
for r in ['jp','kr','eu']:
    t = pathlib.Path('articles/%s.html' % r).read_text(encoding='utf-8')
    bad = re.findall(r'loremflickr|picsum', t)
    print(r, len(bad))
    for m in re.finditer(r'loremflickr|picsum', t):
        s = max(0, m.start()-150)
        print(t[s:m.end()+80].replace(chr(10), ' ')[:250])
        print('---')
