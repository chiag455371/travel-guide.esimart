# -*- coding: utf-8 -*-
"""Comprehensive image and site verification."""
import os, re, urllib.request

base = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"
articles_dir = base + r"\articles"

print("=" * 60)
print("網站完整性檢查")
print("=" * 60)

# 1. Article count
files = [f for f in os.listdir(articles_dir) if f.endswith('.html')]
article_files = [f for f in files if f != 'index.html']
print("\n1. 文章數量: " + str(len(article_files)) + " 篇")

# 2. Region distribution
regions = {'jp': [], 'kr': [], 'tw': [], 'eu': [], 'oce': []}
for fn in article_files:
    prefix = fn.split('-')[0]
    if prefix in regions:
        regions[prefix].append(fn)
for r, arts in regions.items():
    print("   " + r.upper() + ": " + str(len(arts)) + " 篇")

# 3. Image verification - collect all unique URLs
all_urls = set()
for fn in files:
    fp = os.path.join(articles_dir, fn) if fn != 'index.html' else base + r"\index.html"
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    urls = re.findall(r'src="(https://loremflickr\.com/[^"]+)"', content)
    all_urls.update(urls)

print("\n2. 圖片URL總數: " + str(len(all_urls)) + " 個唯一URL")

# 4. Test images (sample 30)
print("\n3. 圖片可用性測試（抽樣30張）:")
broken_urls = []
tested = 0
for url in sorted(all_urls):
    if tested >= 30:
        break
    tested += 1
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        resp = urllib.request.urlopen(req, timeout=10)
        data = resp.read()
        if resp.status == 200 and len(data) > 1000:
            print("   [OK] " + url[:80])
        else:
            print("   [BROKEN] " + url[:80] + " (status=" + str(resp.status) + ", size=" + str(len(data)) + ")")
            broken_urls.append(url)
    except Exception as e:
        print("   [ERROR] " + url[:80] + " -> " + str(e)[:50])
        broken_urls.append(url)

print("\n   破圖數量: " + str(len(broken_urls)))

# 5. SEO elements check
print("\n4. SEO元素檢查:")
missing_jsonld = 0
missing_og = 0
missing_esim = 0
for fn in article_files:
    with open(os.path.join(articles_dir, fn), 'r', encoding='utf-8') as f:
        c = f.read()
    if 'ld+json' not in c:
        missing_jsonld += 1
    if 'og:image' not in c:
        missing_og += 1
    if 'travel-guide.esimart.cc/goods' not in c:
        missing_esim += 1

print("   缺少JSON-LD: " + str(missing_jsonld))
print("   缺少OG Image: " + str(missing_og))
print("   缺少eSIM連結: " + str(missing_esim))

# 6. Sitemap
print("\n5. Sitemap:")
with open(base + r"\sitemap.xml", 'r', encoding='utf-8') as f:
    sm = f.read()
print("   URL數量: " + str(sm.count('<loc>')))

# 7. Files with spaces
spaces = [f for f in files if ' ' in f]
print("\n6. 檔案名稱檢查:")
print("   含空白的檔案: " + (str(spaces) if spaces else "無"))

print("\n" + "=" * 60)
print("檢查完成")
print("=" * 60)
