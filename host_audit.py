# -*- coding: utf-8 -*-
import re, glob, pathlib
from collections import Counter
c = Counter()
for f in glob.glob('articles/*.html') + glob.glob('guides/*.html'):
    t = pathlib.Path(f).read_text(encoding='utf-8')
    for u in re.findall(r'src=\"(https?://[^\"]+)\"', t):
        host = re.match(r'https?://([^/]+)', u)
        c[host.group(1)] += 1
print('img src hosts:', c.most_common())
# region pages vs articles
for r in ['jp','kr','tw','eu','oce']:
    t = pathlib.Path('articles/%s.html' % r).read_text(encoding='utf-8')
    imgs = re.findall(r'card-img\" src=\"([^\"]+)\"', t)
    hosts = Counter((re.match(r'https?://([^/]+)', x).group(1) for x in imgs))
    print(r, 'cards:', len(imgs), hosts.most_common(2))
