# -*- coding: utf-8 -*-
import glob, sys
from collections import Counter
c = Counter()
slugs = []
for f in glob.glob('articles/*.html'):
    import os
    s = os.path.basename(f)[:-5]
    c[s.split('-')[0]] += 1
    slugs.append(s)
sys.stdout.buffer.write(('region counts: ' + repr(dict(c)) + chr(10)).encode())
sys.stdout.buffer.write(('total slugs: %d\n' % len(slugs)).encode())
# sample a few slugs per region
import itertools
seen = set()
out = []
for s in slugs:
    r = s.split('-')[0]
    if r not in seen:
        seen.add(r)
        out.append(s)
sys.stdout.buffer.write(('sample: ' + repr(out) + chr(10)).encode('utf-8','replace'))
