# -*- coding: utf-8 -*-
"""檢查地區頁中所有 80/80 卡片種子是否與文章封面一致(完整版)"""
import re, glob, os

seed_map = {}
for f in glob.glob('articles/*.html'):
    c = open(f, encoding='utf-8').read()
    m = re.search(r'seed/(\d+)/', c)
    if m:
        seed_map[os.path.basename(f)] = m.group(1)

for f in ['index.html'] + glob.glob('articles/*.html'):
    if f in seed_map:
        continue
    c = open(f, encoding='utf-8').read()
    for m in re.finditer(r'href="[^"]*articles/([a-z0-9\-]+\.html)"[^>]*>.*?seed/(\d+)/80/80', c, re.S):
        slug, seed = m.group(1), m.group(2)
        if slug in seed_map and seed_map[slug] != seed:
            print(f"DIRTY {f}: {slug} card seed={seed} article seed={seed_map[slug]}")
print("check done")
