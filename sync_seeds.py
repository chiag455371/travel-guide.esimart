# -*- coding: utf-8 -*-
"""同步修正後種子到 region 頁、index、guides"""
import re, glob, os

seed_map = {}
for f in glob.glob('articles/*.html'):
    c = open(f, encoding='utf-8').read()
    m = re.search(r'seed/(\d+)', c)
    if m:
        seed_map[os.path.basename(f)] = m.group(1)

files = ['articles/eu.html', 'articles/jp.html', 'articles/kr.html', 'articles/tw.html', 'articles/oce.html',
         'articles/index.html', 'index.html'] + glob.glob('guides/*.html')
changed = 0
for f in files:
    if not os.path.exists(f):
        continue
    c = open(f, encoding='utf-8').read()
    orig = c
    for card_slug, new_seed in seed_map.items():
        # 替換所有指向該 slug 卡片的 80/80 縮圖種子
        pattern = re.compile(
            r'href="https://travel-guide-esimart\.pages\.dev/articles/' + re.escape(card_slug) + r'"'
            r'(?:[^>]*>\s*)?(?:<div class="card-img-wrapper">\s*)?<img[^>]*?seed/(\d+)/80/80'
        )
        for m in pattern.finditer(c):
            old = m.group(1)
            if old != new_seed:
                c = c.replace(f'seed/{old}/80/80', f'seed/{new_seed}/80/80', 1)
    if c != orig:
        open(f, 'w', encoding='utf-8').write(c)
        changed += 1
        print(f"updated {f}")
print(f"total changed: {changed}")

# 重新驗證: region/index 頁中 80/80 種子是否還與 articles 一致
mismatch = 0
for f in ['articles/eu.html', 'articles/jp.html', 'articles/kr.html', 'articles/tw.html', 'articles/oce.html', 'index.html']:
    if not os.path.exists(f):
        continue
    c = open(f, encoding='utf-8').read()
    for card_slug, new_seed in seed_map.items():
        m = re.search(re.escape(card_slug) + r'"[^>]*>\s*(?:<div class="card-img-wrapper">\s*)?<img[^>]*?seed/(\d+)/80/80', c)
        if m and m.group(1) != new_seed:
            mismatch += 1
            print(f"MISMATCH {f}: {card_slug} uses {m.group(1)}, expected {new_seed}")
print(f"mismatches: {mismatch}")
