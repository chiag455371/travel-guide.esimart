# -*- coding: utf-8 -*-
"""線上驗證: 抽樣確認圖片已替換為 Wikimedia Commons"""
import re, urllib.request

BASE = "https://travel-guide-esimart.pages.dev/"

def fetch(p):
    req = urllib.request.Request(BASE + p, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "ignore")

samples = [
    "articles/jp-tokyo-asakusa.html",
    "articles/kr-jeju.html",
    "articles/eu-rome-colosseum.html",
    "articles/tw-taipei-101.html",
    "articles/oce-sydney-opera.html",
    "index.html",
    "articles/kr.html",
]

total_wiki = 0
total_picsum = 0
for s in samples:
    c = fetch(s)
    wiki = c.count("wikimedia.org")
    picsum = c.count("picsum.photos")
    total_wiki += wiki
    total_picsum += picsum
    ok = "PASS" if wiki > 0 and picsum == 0 else "FAIL"
    print(f"{ok} {s}: wikimedia_refs={wiki}, picsum_refs={picsum}")

print(f"\n總計: wikimedia={total_wiki}, picsum={total_picsum}")
print("結論: " + ("全部替換完成" if total_picsum == 0 else "仍有 picsum 殘留"))
