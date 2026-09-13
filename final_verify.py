# -*- coding: utf-8 -*-
import os, re, urllib.request, ssl

BASE = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"
ARTICLES = BASE + r"\articles"
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

all_urls = set()
all_files = []
for fn in os.listdir(ARTICLES):
    if not fn.endswith(".html"): continue
    all_files.append(fn)
    fp = os.path.join(ARTICLES, fn)
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()
    for m in re.finditer(r'(?:src|content)="(https://loremflickr\.com/[^"]+)"', c):
        all_urls.add(m.group(1))
for idx in ["index.html", "articles/index.html"]:
    fp = os.path.join(BASE, idx)
    if os.path.exists(fp):
        with open(fp, "r", encoding="utf-8") as f:
            c = f.read()
        for m in re.finditer(r'(?:src|content)="(https://loremflickr\.com/[^"]+)"', c):
            all_urls.add(m.group(1))

print(f"=== FINAL IMAGE VERIFICATION ===")
print(f"Total HTML files: {len(all_files) + 2}")
print(f"Total unique image URLs: {len(all_urls)}")

errors = 0
for url in sorted(all_urls):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=8, context=ssl_ctx)
        if resp.status not in (200, 301, 302):
            print(f"  BAD [{resp.status}]: {url[:80]}")
            errors += 1
    except Exception as e:
        print(f"  ERROR: {url[:80]} - {type(e).__name__}")
        errors += 1

print(f"\nResult: {'ALL IMAGES OK - No broken images!' if errors == 0 else f'{errors} BROKEN IMAGES FOUND'}")

# Check for broken patterns
print("\n=== BROKEN PATTERN CHECK ===")
broken_patterns = []
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
    for fn in files:
        if not fn.endswith(".html"): continue
        fp = os.path.join(root, fn)
        with open(fp, "r", encoding="utf-8") as f:
            c = f.read()
        if "unsplash.com/photo-" in c:
            broken_patterns.append((fn, "unsplash.com/photo-"))
        if "https://https://" in c:
            broken_patterns.append((fn, "double-https"))
        if "loremflickr.com/600x400" in c or "loremflickr.com/1200x630" in c:
            broken_patterns.append((fn, "wrong-format"))
        if "tw-yilan-hot spring" in c:
            broken_patterns.append((fn, "space-in-slug"))

if broken_patterns:
    print(f"Broken patterns found: {len(broken_patterns)}")
    for fn, pat in broken_patterns[:10]:
        print(f"  {fn}: {pat}")
else:
    print("No broken patterns found!")

# Count templates
with open(BASE + r"\daily_articles.py", "r", encoding="utf-8") as f:
    dc = f.read()
template_slugs = re.findall(r'"slug":\s*"([^"]+)"', dc)
print(f"\n=== DAILY ARTICLES GENERATOR ===")
print(f"Total templates: {len(template_slugs)}")
print(f"Unique slugs: {len(set(template_slugs))}")
print(f"Duplicates: {len(template_slugs) - len(set(template_slugs))}")
