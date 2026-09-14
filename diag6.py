# -*- coding: utf-8 -*-
import re, pathlib, sys
for r in ['jp','kr','eu']:
    t = pathlib.Path('articles/%s.html' % r).read_text(encoding='utf-8')
    for m in re.finditer(r'wikimedia', t):
        seg = t[max(0,m.start()-500):m.start()]
        hrefs = re.findall(r'/articles/([a-z0-9\-]+)\.html', seg)
        sys.stdout.buffer.write((('near-href: ' + (hrefs[-1] if hrefs else 'NONE') + chr(10))).encode('utf-8','replace'))
