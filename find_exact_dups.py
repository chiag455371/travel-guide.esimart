# -*- coding: utf-8 -*-
import re, glob, pathlib, sys
# find ALL exact-title duplicates (>95% similar, same region+city)
from difflib import SequenceMatcher
files = sorted(glob.glob('articles/*.html'))
titles = {}
for f in files:
    c = pathlib.Path(f).read_text(encoding='utf-8')
    m = re.search(r'<title>([^<]+)</title>', c)
    if m:
        titles[f] = m.group(1)
flagged = []
items = list(titles.items())
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
sys.stdout.buffer.write(('TOTAL exact-title dup pairs: %d\n' % len(flagged)).encode())
