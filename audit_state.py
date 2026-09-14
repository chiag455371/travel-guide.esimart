# -*- coding: utf-8 -*-
import pathlib, re, glob, collections
mr = []
for f in glob.glob('articles/*.html'):
    c = pathlib.Path(f).read_text(encoding='utf-8')
    if 'http-equiv' in c and len(c) < 500:
        mr.append(f)
print('meta-refresh redirects:', len(mr))
bc = 0; total = 0
for f in glob.glob('articles/*.html'):
    c = pathlib.Path(f).read_text(encoding='utf-8')
    if 'http-equiv' in c and len(c) < 500: continue
    total += 1
    if 'breadcrumb' in c: bc += 1
print('breadcrumbs:', bc, '/', total)
rel = 0
for f in glob.glob('articles/*.html'):
    c = pathlib.Path(f).read_text(encoding='utf-8')
    if 'http-equiv' in c and len(c) < 500: continue
    if re.search(r'related', c, re.I): rel += 1
print('related sections:', rel, '/', total)
sc = collections.Counter()
for f in glob.glob('articles/*.html') + glob.glob('guides/*.html'):
    c = pathlib.Path(f).read_text(encoding='utf-8')
    for m in re.findall(r'\"@type\":\s*\"([A-Za-z]+)\"', c):
        sc[m] += 1
print('schema types:', dict(sc))
