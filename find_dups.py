# -*- coding: utf-8 -*-
import re, glob, pathlib
# find near-duplicate slugs: same prefix-second-part pairs
slugs = sorted(f[:-5] for f in glob.glob('articles/*.html'))
print('total slugs:', len(slugs))
from collections import defaultdict
pairs = defaultdict(list)
for s in slugs:
    parts = s.split('-')
    if len(parts) >= 3:
        pairs[(parts[0], parts[1])].append(s)
    else:
        pairs[(parts[0], parts[1] if len(parts)>1 else '')].append(s)
dups = {k:v for k,v in pairs.items() if len(v)>1}
print('groups with >1:', len(dups))
# heuristic: check title similarity among same-group
import difflib
flagged = []
for k, v in dups.items():
    if len(v) < 2: continue
    titles = []
    for s in v:
        try:
            c = pathlib.Path('articles/%s.html' % s).read_text(encoding='utf-8')
            m = re.search(r'<title>([^<]+)</title>', c)
            titles.append((s, m.group(1) if m else s))
        except: pass
    # pair up
    for i in range(len(titles)):
        for j in range(i+1, len(titles)):
            ratio = difflib.SequenceMatcher(None, titles[i][1], titles[j][1]).ratio()
            if ratio > 0.7:
                flagged.append((k, titles[i][0], titles[j][0], round(ratio,2)))
for f in flagged[:40]:
    print(f)
print('flagged count:', len(flagged))
