# -*- coding: utf-8 -*-
"""Final comprehensive verification."""
import os, re, urllib.request

print('=== FINAL VERIFICATION ===')
print('')

base = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"
articles_dir = base + r"\articles"

# 1. Article count
files = [f for f in os.listdir(articles_dir) if f.endswith('.html')]
article_files = [f for f in files if f != 'index.html']
print('1. Articles: ' + str(len(article_files)) + ' total')

# 2. Region distribution
regions = {'jp': [], 'kr': [], 'tw': [], 'eu': [], 'oce': []}
for fn in article_files:
    prefix = fn.split('-')[0]
    if prefix in regions:
        regions[prefix].append(fn)
for r, arts in regions.items():
    print('   ' + r.upper() + ': ' + str(len(arts)) + ' articles')

# 3. Image verification
print('')
print('2. Image verification (sampling 30 articles)...')
broken_imgs = 0
total_imgs = 0
samples = article_files[:30]
for fn in samples:
    with open(os.path.join(articles_dir, fn), 'r', encoding='utf-8') as f:
        c = f.read()
    urls = re.findall(r'src="(https://loremflickr\.com/[^"]+)"', c)
    for url in urls:
        total_imgs += 1
        try:
            resp = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=8)
            data = resp.read()
            if resp.status != 200 or len(data) < 1000:
                broken_imgs += 1
        except:
            broken_imgs += 1
print('   Checked: ' + str(total_imgs) + ' images, Broken: ' + str(broken_imgs))

# 4. SEO elements
print('')
print('3. SEO elements check...')
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
print('   Missing JSON-LD: ' + str(missing_jsonld))
print('   Missing OG image: ' + str(missing_og))
print('   Missing eSIM link: ' + str(missing_esim))

# 5. Sitemap
print('')
print('4. Sitemap...')
with open(base + r"\sitemap.xml", 'r', encoding='utf-8') as f:
    sm = f.read()
loc_count = sm.count('<loc>')
print('   URLs in sitemap: ' + str(loc_count))

# 6. Files with spaces
print('')
print('5. Filename check...')
spaces = [f for f in files if ' ' in f]
print('   Files with spaces: ' + (str(spaces) if spaces else 'None'))

# 7. Template count
print('')
print('6. Template pool...')
import sys
sys.path.insert(0, base)
try:
    from daily_articles import TEMPLATES
    from extra_templates import EXTRA_TEMPLATES
    from extra_templates_2 import EXTRA_TEMPLATES_2
    total = len(TEMPLATES) + len(EXTRA_TEMPLATES) + len(EXTRA_TEMPLATES_2)
    print('   Total templates: ' + str(total))
except Exception as e:
    print('   Template check failed: ' + str(e))

print('')
print('=== VERIFICATION COMPLETE ===')
