# -*- coding: utf-8 -*-
import re, glob

rem = [f for f in glob.glob('articles/*.html') + ['index.html'] if 'picsum.photos' in open(f, encoding='utf-8').read()]
print('remaining picsum files:', len(rem))
for f in rem:
    print(' ', f)

print('\n=== og:image check ===')
for f in ['articles/jp-tokyo-asakusa.html', 'articles/kr-seoul-gyeongbok.html', 'articles/tw-taipei-night-market.html']:
    c = open(f, encoding='utf-8').read()
    m = re.search(r'og:image" content="([^"]+)"', c)
    print(f, '->', (m.group(1)[:70] if m else 'NONE'))
