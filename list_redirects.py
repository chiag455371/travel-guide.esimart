# -*- coding: utf-8 -*-
import re, glob, pathlib, sys, json
redirects = []
for f in glob.glob('articles/*.html'):
    c = pathlib.Path(f).read_text(encoding='utf-8')
    if 'http-equiv' in c:
        redirects.append(f)
print('redirect stubs:', len(redirects))
if redirects:
    for f in redirects[:5]:
        c = pathlib.Path(f).read_text(encoding='utf-8')
        m = re.search(r'url=([^\"]+)', c)
        print(' ', f, '->', m.group(1).split('/')[-1] if m else '?', 'len', len(c))
