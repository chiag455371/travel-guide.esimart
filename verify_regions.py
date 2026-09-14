# -*- coding: utf-8 -*-
import re, pathlib, collections
ok = True
for r in ['jp','kr','eu','tw','oce']:
    t = pathlib.Path('articles/%s.html' % r).read_text(encoding='utf-8')
    bad = len(re.findall(r'loremflickr|picsum', t))
    ok = ok and bad == 0
    print(r, 'bad:', bad)
print('all clean:', ok)
t = pathlib.Path('articles/jp.html').read_text(encoding='utf-8')
m = re.findall(r'src=\"(https://[^\"]+)\"', t)
print('hosts:', collections.Counter(x.split('/')[2] for x in m).most_common(4))
