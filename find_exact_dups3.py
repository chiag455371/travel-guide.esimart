# -*- coding: utf-8 -*-
import re, glob, pathlib, sys
from difflib import SequenceMatcher
redirect_files = set()
for f in glob.glob('articles/*.html'):
    c = pathlib.Path(f).read_text(encoding='utf-8')
    if 'http-equiv' in c and len(c) < 600:
        redirect_files.add(f)
print('redirect stubs:', len(redirect_files))
real = {}
for f in glob.glob('articles/*.html'):
    if f in redirect_files:
        continue
    c = pathlib.Path(f).read_text(encoding='utf-8')
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
        if r > 0.9:
            flagged.append((round(r,3), f1, f2, t1))
flagged.sort(key=lambda x: -x[0])
for r, f1, f2, t in flagged:
    sys.stdout.buffer.write(('%0.3f  %s  ->  %s\n' % (r, f1, f2)).encode())
    sys.stdout.buffer.write(('   ' + t + chr(10)).encode('utf-8','replace'))
sys.stdout.buffer.write(('TOTAL: %d\n' % len(flagged)).encode())
