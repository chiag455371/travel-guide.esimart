# -*- coding: utf-8 -*-
import re, glob, pathlib, collections
from difflib import SequenceMatcher
slugs = sorted(p[:-5] for p in glob.glob('articles/*.html'))
pairs = collections.defaultdict(list)
for s in slugs:
    parts = s.split('-')
    pairs['-'.join(parts[:2])].append(s)
out = []
for k, v in pairs.items():
    if len(v) < 2: continue
    titles = []
    for s in v:
        try:
            c = pathlib.Path(s + '.html').read_text(encoding='utf-8')
        except FileNotFoundError:
            continue
        m = re.search(r'<title>([^<]+)</title>', c)
        titles.append((s, (m.group(1) if m else s).split('\uFF5C')[0]))
    for i in range(len(titles)):
        for j in range(i+1, len(titles)):
            r = SequenceMatcher(None, titles[i][1], titles[j][1]).ratio()
            if r > 0.55:
                out.append((round(r,2), titles[i][0], titles[j][0]))
out.sort(reverse=True)
for row in out[:80]:
    print(row)
print('total flagged:', len(out))
