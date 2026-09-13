# -*- coding: utf-8 -*-
import os, re, urllib.request, ssl, json

BASE = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"
ARTICLES = BASE + r"\articles"
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def check_url(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=8, context=ssl_ctx)
        return resp.status
    except Exception as e:
        return 0

# Collect all unique image URLs
all_urls = {}
for fn in os.listdir(ARTICLES):
    if not fn.endswith(".html"): continue
    with open(os.path.join(ARTICLES, fn), "r", encoding="utf-8") as f:
        c = f.read()
    for m in re.finditer(r"https://images\.unsplash\.com/[^\s\"'\x3c\x3e]+", c):
        url = m.group()
        if url not in all_urls:
            all_urls[url] = []
        all_urls[url].append(fn)
for idx in ["index.html", "articles/index.html"]:
    with open(os.path.join(BASE, idx), "r", encoding="utf-8") as f:
        c = f.read()
    for m in re.finditer(r"https://images\.unsplash\.com/[^\s\"'\x3c\x3e]+", c):
        url = m.group()
        if url not in all_urls:
            all_urls[url] = []
        all_urls[url].append(idx)

print(f"Total unique image URLs: {len(all_urls)}")
broken = []
ok_count = 0
for url, files in sorted(all_urls.items()):
    code = check_url(url)
    if code == 200:
        ok_count += 1
    else:
        broken.append((url, code, files[0]))
        print(f"  BROKEN [{code}]: {url[:70]}... (in {files[0]})")

print(f"\nOK: {ok_count}/{len(all_urls)}, Broken: {len(broken)}")
if broken:
    with open(BASE + r"\broken_images.txt", "w", encoding="utf-8") as f:
        for url, code, fn in broken:
            f.write(f"{code}\t{fn}\t{url}\n")
    print(f"Saved broken list to broken_images.txt")
