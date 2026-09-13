# -*- coding: utf-8 -*-
import os, re

BASE = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"
ARTICLES = BASE + r"\articles"

REGION_KW = {
    "jp": ("japan", 1001),
    "kr": ("korea", 1002),
    "tw": ("taiwan", 1003),
    "eu": ("europe", 1004),
    "oce": ("australia", 1005),
}

def get_region(fn):
    if fn.startswith("jp-"): return "jp"
    if fn.startswith("kr-"): return "kr"
    if fn.startswith("tw-"): return "tw"
    if fn.startswith("eu-"): return "eu"
    if fn.startswith("oce-"): return "oce"
    return None

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    filename = os.path.basename(filepath)
    is_index = filename == "index.html" or filepath.endswith(os.path.join("articles", "index.html"))
    region = get_region(filename) if not is_index else None
    
    # Fix the wrong URL format: https://loremflickr.com/600x400/... -> https://loremflickr.com/600/400/...
    content = re.sub(r"https://loremflickr\.com/600x400/", "https://loremflickr.com/600/400/", content)
    content = re.sub(r"https://loremflickr\.com/1200x630/", "https://loremflickr.com/1200/630/", content)
    
    # Also fix double https://
    content = content.replace("https://https://loremflickr", "https://loremflickr")
    
    # Replace remaining broken unsplash URLs
    def replace_unsplash(m):
        url = m.group(0)
        if region:
            kw, lock = REGION_KW[region]
            if "1200/630" in url:
                return f"https://loremflickr.com/1200/630/{kw}?lock={lock}"
            return f"https://loremflickr.com/600/400/{kw}?lock={lock}"
        return url
    
    content = re.sub(
        r"https://images\.unsplash\.com/photo-[\w-]+\?[^\s\"'\x3c\x3e]+",
        replace_unsplash,
        content
    )
    
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  FIXED: {os.path.relpath(filepath, BASE)}")
        return True
    return False

print("=== Fix URL format bugs ===")
fixed = 0
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
    for fn in files:
        if not fn.endswith(".html"): continue
        fp = os.path.join(root, fn)
        if fix_file(fp):
            fixed += 1
print(f"Total fixed: {fixed}")

# Verify all images
print("\n=== Verification ===")
import urllib.request, ssl
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

all_urls = set()
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
    for fn in files:
        if not fn.endswith(".html"): continue
        fp = os.path.join(root, fn)
        with open(fp, "r", encoding="utf-8") as f:
            c = f.read()
        # Only match img src and og:image content attributes
        for m in re.finditer(r'(?:src|content)="((?:https?://)?(?:loremflickr|unsplash|picsum)\.[^"]+)"', c):
            all_urls.add(m.group(1))

print(f"Total image URLs to check: {len(all_urls)}")
errors = 0
for url in sorted(all_urls):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=8, context=ssl_ctx)
        if resp.status not in (200, 301, 302):
            print(f"  BAD [{resp.status}]: {url[:70]}")
            errors += 1
    except Exception as e:
        print(f"  ERROR: {url[:70]} - {type(e).__name__}")
        errors += 1
print(f"\n{'ALL OK!' if errors == 0 else f'{errors} issues'}")
