# -*- coding: utf-8 -*-
import re, glob, pathlib, sys
from difflib import SequenceMatcher
real = {}
for f in glob.glob('articles/*.html'):
    c = pathlib.Path(f).read_text(encoding='utf-8')
    if c.count(chr(10)) < 10 and 'refresh' in c:
        continue
    m = re.search(r'<title>([^<]+)</title>', c)
    if m:
        real[f] = m.group(1)
items = list(real.items())
flagged = []
for i in range(len(items)):
    for j in range(i+1, len(items)):
        f1, t1 = items[i]
        f2, t2 = items[j]
        r = SequenceMatcher(None, t1, t2).ratio()
        if r > 0.93:
            flagged.append((round(r,3), f1, f2, t1))
flagged.sort(key=lambda x: -x[0])
for r, f1, f2, t in flagged:
    sys.stdout.buffer.write(('%0.3f  %s  ->  %s\n   %s\n' % (r, f1, f2, t)).encode('utf-8','replace'))
sys.stdout.buffer.write(('TOTAL real-content dup pairs: %d\n' % len(flagged)).encode())
