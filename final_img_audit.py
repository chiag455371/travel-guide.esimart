# -*- coding: utf-8 -*-
import re, glob, pathlib
from collections import Counter
tot=0; hosts=Counter()
for f in glob.glob('articles/*.html')+glob.glob('guides/*.html')+['index.html']:
    t = pathlib.Path(f).read_text(encoding='utf-8')
    tot += len(re.findall(r'wikimedia', t))
    for u in re.findall(r'src=\"(https?://[^\"]+)\"', t):
        hosts[re.match(r'https?://([^/]+)', u).group(1)] += 1
print('total wikimedia remaining:', tot)
print('img src hosts:', dict(hosts.most_common()))
