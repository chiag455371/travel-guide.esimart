# -*- coding: utf-8 -*-
import re, pathlib
from collections import Counter
t = pathlib.Path('articles/kr.html').read_text(encoding='utf-8')
c = Counter(re.findall(r'card-img\" src=\"([^\"]+)\"', t))
print('top 6:')
for k, n in c.most_common(6):
    print('  x%d  %s' % (n, k[-45:]))
# check pixel_cache pid uniqueness for kr
import json
p = json.load(open('pixel_cache.json',encoding='utf-8'))
kr_covers = {}
for k,v in p.items():
    if k.startswith('kr-') and '__card' not in k:
        kr_covers[k] = v.get('pid')
from collections import defaultdict
bypid = defaultdict(list)
for k,pid in kr_covers.items():
    if pid: bypid[pid].append(k)
dups = {pid:slugs for pid,slugs in bypid.items() if len(slugs)>1}
print('kr pid dup groups:', len(dups))
for pid,sl in list(dups.items())[:5]:
    print('  pid', pid, '->', sl)
