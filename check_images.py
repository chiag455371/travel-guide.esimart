#!/usr/bin/env python3
import os, re

ARTICLES_DIR = r'C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo\articles'
files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.html') and f not in {'index.html','jp.html','kr.html','tw.html','eu.html','oce.html'}]

bad_src = 0
bad_multi_q = 0
total_imgs = 0
for f in files:
    content = open(os.path.join(ARTICLES_DIR, f), encoding='utf-8').read()
    if 'src="src="' in content:
        bad_src += 1
    imgs = re.findall(r'src="(https://loremflickr[^"]+)"', content)
    total_imgs += len(imgs)
    for img in imgs:
        if img.count('?') > 1:
            bad_multi_q += 1

print(f'Files checked: {len(files)}')
print(f'Total article images: {total_imgs}')
print(f'src="src=" bugs: {bad_src}')
print(f'Multi-query ? issues: {bad_multi_q}')

# Also check index.html
idx = open(os.path.join(ARTICLES_DIR, 'index.html'), encoding='utf-8').read()
idx_imgs = re.findall(r'src="(https://loremflickr[^"]+)"', idx)
print(f'index.html images: {len(idx_imgs)}')
idx_bad = sum(1 for img in idx_imgs if img.count('?') > 1)
print(f'index.html multi-query issues: {idx_bad}')
