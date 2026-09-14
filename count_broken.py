# -*- coding: utf-8 -*-
import re, glob, pathlib, urllib.request
from collections import Counter
# 1) find all loremflickr / picsum usages per page type
by_file = {}
for f in glob.glob('articles/*.html'):
    txt = pathlib.Path(f).read_text(encoding='utf-8')
    m = re.findall(r'src=\"(https?://[^\"]+)\"', txt)
    if any(('loremflickr' in u or 'picsum' in u) for u in m):
        by_file[os.path.basename(f) if 'import os' in '' else f.split(chr(92))[-1]] = sum(1 for u in m if 'loremflickr' in u or 'picsum' in u)
import os
print('article files w/ broken src:', len(by_file), 'total imgs:', sum(by_file.values()))
# 2) check region pages + guides + food cluster pages
for pat in ['articles/jp.html','articles/kr.html','articles/eu.html','articles/tw.html','articles/oce.html']:
    p = pathlib.Path(pat)
    if p.exists():
        t = p.read_text(encoding='utf-8')
        n = len(re.findall(r'loremflickr|picsum', t))
        print(pat, n)
