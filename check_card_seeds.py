# -*- coding: utf-8 -*-
"""檢查 region 頁(index.html, kr.html 等)卡片種子是否與各文章封面種子一致"""
import re, glob, os

seed_map = {}
for f in glob.glob('articles/*.html'):
    c = open(f, encoding='utf-8').read()
    m = re.search(r'seed/(\d+)/', c)
    if m:
        seed_map[os.path.basename(f)] = m.group(1)

check_files = ['index.html', 'articles/index.html', 'articles/kr.html', 'articles/jp.html',
               'articles/tw.html', 'articles/eu.html', 'articles/oce.html', 'guides/index.html']
total_bad = 0
for f in check_files:
    if not os.path.exists(f):
        continue
    c = open(f, encoding='utf-8').read()
    # 找出所有卡片: <a href="...articles/SLUG.html"> ... seed/X/80/80
    for m in re.finditer(r'href="https://travel-guide-esimart\.pages\.dev/articles/([a-z0-9\-]+\.html)"[^>]*>\s*(?:<div class="card-img-wrapper">\s*)?<img[^>]*?seed/(\d+)/80/80', c, re.S):
        slug, seed = m.group(1), m.group(2)
        if slug in seed_map and seed_map[slug] != seed:
            total_bad += 1
            print(f"MISMATCH {f}: {slug} 卡片用 {seed}, 文章封面用 {seed_map[slug]}")
print(f"總不一致數: {total_bad}")
