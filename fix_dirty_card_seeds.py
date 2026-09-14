# -*- coding: utf-8 -*-
"""修正地區頁殘留的舊卡片種子(完整掃描版)"""
import re, glob, os

seed_map = {}
for f in glob.glob('articles/*.html'):
    c = open(f, encoding='utf-8').read()
    m = re.search(r'seed/(\d+)/', c)
    if m:
        seed_map[os.path.basename(f)] = m.group(1)

fixed = 0
for f in ['index.html'] + glob.glob('articles/*.html'):
    if f in seed_map:
        continue
    c = open(f, encoding='utf-8').read()
    orig = c
    for m in re.finditer(r'href="[^"]*articles/([a-z0-9\-]+\.html)"[^>]*>.*?seed/(\d+)/80/80', c, re.S):
        slug, seed = m.group(1), m.group(2)
        if slug in seed_map and seed_map[slug] != seed:
            c = c.replace(f'seed/{seed}/80/80', f'seed/{seed_map[slug]}/80/80', 1)
    if c != orig:
        open(f, 'w', encoding='utf-8').write(c)
        fixed += 1
        print(f"fixed {f}")
print(f"total fixed: {fixed}")
