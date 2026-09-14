# -*- coding: utf-8 -*-
"""Normalize seed assignment: every page that references a slug gets that slug's
og:image seed. Article files keep their own og:image seed; only the card grids
and the in-page card sections change."""
import re, glob, os, collections

BASE = 'https://travel-guide-esimart.pages.dev'

# 1. slug -> og:image seed (from each article file)
seed_of = {}
for f in sorted(glob.glob('articles/*.html')):
    slug = os.path.basename(f)[:-5]
    c = open(f, encoding='utf-8').read()
    m = re.search(r'<meta property="og:image" content="https://picsum\.photos/seed/([0-9A-Za-z\-]+)/', c)
    if m:
        seed_of[slug] = m.group(1)

# 2. rewrite every card link block that references /articles/<slug>.html
IMG = re.compile(
    r'(<a href="' + BASE + r'/articles/([a-z0-9\-]+)\.html" class="article-card">\s*'
    r'<div class="card-img-wrapper"><img class="card-img" src="https://picsum\.photos/seed/)[0-9A-Za-z\-]+'
    r'(/\d+/\d+"[^>]*>)',
    re.S)

changed = 0
touched = []
files = sorted(glob.glob('articles/*.html')) + ['index.html']
for f in files:
    c = open(f, encoding='utf-8').read()
    orig = c

    def repl(m):
        global changed
        slug = m.group(2)
        seed = seed_of.get(slug)
        if not seed:
            return m.group(0)
        changed += 1
        return m.group(1) + seed + m.group(3)

    c = IMG.sub(repl, c)
    if c != orig:
        open(f, 'w', encoding='utf-8').write(c)
        touched.append(f)

print('rewritten card images:', changed)
print('files touched:', len(touched))

# 3. re-audit
refs = collections.defaultdict(set)
for f in files:
    c = open(f, encoding='utf-8').read()
    for m in re.finditer(
        r'/articles/([a-z0-9\-]+)\.html"[^>]*>\s*<div class="card-img-wrapper">'
        r'<img class="card-img" src="https://picsum\.photos/seed/([0-9A-Za-z\-]+)/', c):
        refs[m.group(1)].add(m.group(2))
dups = {k: sorted(v) for k, v in refs.items() if len(v) > 1}
print('remaining slug-seed mismatches:', len(dups))
for k, v in list(dups.items())[:5]:
    print(' ', k, v)
missing = [k for k in refs if k not in seed_of]
print('slugs with no og:image seed found:', len(missing), missing[:5])
