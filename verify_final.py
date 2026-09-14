# -*- coding: utf-8 -*-
"""Final verification of the website."""
import os, re

ARTICLES_DIR = 'articles'
files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.html')]

print("=" * 50)
print("WEBSITE STATUS REPORT")
print("=" * 50)
print(f"Total articles: {len(files)}")

# Count by region
for r, name in [('jp', '日本'), ('kr', '韓國'), ('tw', '台灣'), ('eu', '歐洲'), ('oce', '澳洲')]:
    c = len([f for f in files if f.startswith(r + '-')])
    print(f"  {name}: {c}")

# Check sitemap
sm = open('sitemap.xml', encoding='utf-8').read()
urls = sm.count('<loc>')
print(f"\nSitemap URLs: {urls}")

# Check suspicious images
suspicious = 0
all_files = files + ['index.html']
for f in all_files:
    path = f if f == 'index.html' else os.path.join(ARTICLES_DIR, f)
    c = open(path, encoding='utf-8').read()
    imgs = re.findall(r'(?:src|content)="(https://loremflickr[^"]+)"', c)
    for img in imgs:
        m = re.search(r'lock=(\d+)', img)
        if m and int(m.group(1)) >= 9000:
            suspicious += 1
print(f"Suspicious images (lock>=9000): {suspicious}")

# Check distributor links
missing = 0
for f in files:
    c = open(os.path.join(ARTICLES_DIR, f), encoding='utf-8').read()
    if 'travel-guide.esimart.cc/goods' not in c:
        missing += 1
print(f"Missing distributor links: {missing}")

# Check OG images
c = open('index.html', encoding='utf-8').read()
og = re.findall(r'og:image[^>]+content="(https://loremflickr[^"]+)"', c)
print(f"\nOG images in index.html: {len(og)}")
for o in og:
    m = re.search(r'lock=(\d+)', o)
    lock = m.group(1) if m else '?'
    print(f"  lock={lock}")

# Check card images
imgs = re.findall(r'src="(https://loremflickr[^"]+)"', c)
print(f"Card images in index.html: {len(imgs)}")
suspicious_cards = 0
for i in imgs:
    m = re.search(r'lock=(\d+)', i)
    if m and int(m.group(1)) >= 9000:
        suspicious_cards += 1
print(f"Suspicious card images: {suspicious_cards}")

print("\n" + "=" * 50)
if suspicious == 0 and missing == 0:
    print("ALL CHECKS PASSED!")
else:
    print("ISSUES FOUND - needs fixing")
print("=" * 50)
