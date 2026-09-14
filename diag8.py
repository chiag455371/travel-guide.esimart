# -*- coding: utf-8 -*-
import re, pathlib, sys
t = pathlib.Path('articles/eu.html').read_text(encoding='utf-8')
for m in re.finditer(r'wikimedia', t):
    seg = t[max(0,m.start()-300):m.start()]
    hrefs = re.findall(r'/articles/([a-z0-9\-]+)\.html', seg)
    sys.stdout.buffer.write((('hrefs: ' + repr(hrefs[-1]) + chr(10))).encode('utf-8','replace'))
