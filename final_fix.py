# -*- coding: utf-8 -*-
"""Final fix: replace ALL remaining broken Unsplash URLs with loremflickr."""
import os, re

BASE = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"
ARTICLES = BASE + r"\articles"

# Region keyword mapping for fallback
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

def make_url(kw, lock, size):
    if size == "1200x630":
        return f"https://loremflickr.com/1200/630/{kw}?lock={lock}"
    return f"https://loremflickr.com/600/400/{kw}?lock={lock}"

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    filename = os.path.basename(filepath)
    # Determine if this is an index page or article
    is_index = filename in ("index.html",) or filepath.endswith(os.path.join("articles", "index.html"))
    region = get_region(filename) if not is_index else None
    
    # Find all unsplash URLs and replace them
    def replace_unsplash(m):
        url = m.group(0)
        if region:
            kw, lock = REGION_KW[region]
            if "1200/630" in url:
                return make_url(kw, lock, "1200x630")
            return make_url(kw, lock, "600x400")
        return url
    
    new_content = re.sub(
        r"https://images\.unsplash\.com/photo-[\w-]+\?[^\s\"'\x3c\x3e]+",
        replace_unsplash,
        content
    )
    
    # Also fix any remaining unsplash source URLs
    new_content = re.sub(
        r"https://images\.unsplash\.com/[^?\s\"'\x3c\x3e]+\?[^\s\"'\x3c\x3e]+",
        lambda m: make_url("travel", 9999, "600x400") if "1200/630" not in m.group() else make_url("travel", 9999, "1200x630"),
        new_content
    )
    
    if new_content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  FIXED: {os.path.relpath(filepath, BASE)}")
        return True
    return False

print("=== Final image fix ===")
fixed = 0
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
    for fn in files:
        if not fn.endswith(".html"): continue
        fp = os.path.join(root, fn)
        if fix_file(fp):
            fixed += 1
print(f"\nTotal fixed: {fixed}")

# Verify
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
        for m in re.finditer(r"https://\S+\.(com|org)/[^\s\"'\x3c\x3e]+", c):
            url = m.group()
            if any(x in url for x in ["unsplash", "loremflickr", "picsum"]):
                all_urls.add(url)

print(f"Total image URLs: {len(all_urls)}")
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
print(f"\n{'ALL OK - No broken images!' if errors == 0 else f'{errors} issues remain'}")
