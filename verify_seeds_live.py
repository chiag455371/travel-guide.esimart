# -*- coding: utf-8 -*-
"""線上驗證: 抽 5 篇文章 + 首頁卡片圖種子是否各自獨立"""
import re, urllib.request

BASE = "https://travel-guide-esimart.pages.dev/"
samples = [
    "articles/eu-amsterdam-canal.html",
    "articles/jp-nikko-tobu.html",
    "articles/tw-shilin-old.html",
    "articles/kr-jeju-cave.html",
    "articles/oce-wellington.html",
]

def fetch(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "ignore")

seeds = {}
for p in samples:
    c = fetch(p)
    m = re.search(r'seed/(\d+)/', c)
    status = "OK" if m else "MISSING SEED"
    seeds[p] = m.group(1) if m else None
    print(f"{p}: seed={seeds[p]} ({status})")

home = fetch("")
home_seeds = re.findall(r'seed/(\d+)/80/80', home)
home_cards = len(re.findall(r'class="card-img"', home))
print(f"\n首頁卡片數: {home_cards}, 首頁卡片種子數: {len(set(home_seeds))}, 重複: {len(home_seeds)-len(set(home_seeds))}")
overlap = set(home_seeds) & set(v for v in seeds.values() if v)
print(f"首頁與文章封面重複: {overlap if overlap else '無'}")

# 檢查 region 頁縮圖
kr = fetch("articles/kr.html")
kr_seeds = re.findall(r'seed/(\d+)/80/80', kr)
print(f"kr.html 卡片數: {len(re.findall(chr(99)+chr(97)+chr(114)+chr(100), kr)) if False else 'n/a'}, 種子: {kr_seeds[:8]}")
