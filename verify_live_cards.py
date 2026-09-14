# -*- coding: utf-8 -*-
"""線上驗證: 地區頁卡片/清單種子與文章封面一致"""
import re, urllib.request, collections

BASE = "https://travel-guide-esimart.pages.dev/"

def fetch(p):
    req = urllib.request.Request(BASE + p, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "ignore")

def card_seeds(html):
    """回傳 {slug: seed} 從卡片/清單縮圖"""
    out = {}
    for m in re.finditer(r'href="[^"]*articles/([a-z0-9\-]+\.html)"[^>]*>.*?seed/(\d+)/80/80', html, re.S):
        out.setdefault(m.group(1), m.group(2))
    return out

bad = 0
for page in ["articles/kr.html", "articles/jp.html", "articles/eu.html", "articles/tw.html", "articles/oce.html", ""]:
    html = fetch(page)
    cards = card_seeds(html)
    checked = 0
    for slug, card_seed in cards.items():
        try:
            art = fetch("articles/" + slug)
        except Exception as e:
            print(f"{page or 'index'} / {slug}: 404 {e}")
            bad += 1
            continue
        m = re.search(r'seed/(\d+)/', art)
        art_seed = m.group(1) if m else None
        checked += 1
        if art_seed != card_seed:
            bad += 1
            print(f"MISMATCH {page or 'index'} {slug}: 卡片={card_seed} 封面={art_seed}")
    print(f"{page or 'index'}: 檢查 {checked} 張卡片, 重複種子 {len(cards.values())-len(set(cards.values()))} 組")

print(f"\n總不一致: {bad}")
