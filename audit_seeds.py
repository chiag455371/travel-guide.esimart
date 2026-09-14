# -*- coding: utf-8 -*-
"""Audit: do different pages use the same cover image for different articles?"""
import re, glob, collections

refs = collections.defaultdict(set)   # slug -> seeds used for it on card grids
cover = {}                            # seed -> slugs it was assigned to
for f in sorted(glob.glob('articles/*.html')) + ['index.html']:
    c = open(f, encoding='utf-8').read()
    for m in re.finditer(
        r'/articles/([a-z0-9\-]+)\.html"[^>]*>\s*<div class="card-img-wrapper">'
        r'<img class="card-img" src="https://picsum\.photos/seed/([0-9A-Za-z\-]+)/', c):
        refs[m.group(1)].add(m.group(2))
        cover.setdefault(m.group(2), set()).add(m.group(1))

multi = {k: sorted(v) for k, v in cover.items() if len(v) > 1}
print('cover seeds shared across different slugs:', len(multi))
for k, v in list(multi.items())[:10]:
    print(' ', k, v)

dups = {k: sorted(v) for k, v in refs.items() if len(v) > 1}
print('slugs where different pages use different seeds for the same article:', len(dups))
for k, v in list(dups.items())[:10]:
    print(' ', k, v)

# also: article-file-internal cover seed vs grid cover seed for the same slug
mismatch = 0
for slug, seeds in refs.items():
    try:
        c = open(f'articles/{slug}.html', encoding='utf-8').read()
    except FileNotFoundError:
        continue
    own = re.search(r'<meta property="og:image" content="https://picsum\.photos/seed/([0-9A-Za-z\-]+)/', c)
    body = re.findall(r'<img class="card-img" src="https://picsum\.photos/seed/([0-9A-Za-z\-]+)/', c)
    for s in set(body) | (seeds - {own.group(1)} if own else set(body)):
        if own and s != own.group(1) and s in body:
            mismatch += 1
            break
print('article files whose in-page card images differ from their og:image seed:', mismatch)
