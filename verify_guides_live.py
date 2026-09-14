# -*- coding: utf-8 -*-
import re, urllib.request

BASE = "https://travel-guide-esimart.pages.dev/"

def fetch(p):
    req = urllib.request.Request(BASE + p, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "ignore")

for region in ['jp', 'kr', 'tw', 'eu', 'oce']:
    p = f"guides/{region}-esim-guide.html"
    c = fetch(p)
    cards = len(re.findall(r'class="related-card"', c))
    wiki = c.count("wikimedia.org")
    bc = "BreadcrumbList" in c
    ok = cards >= 5 and bc
    print(f"{'OK' if ok else 'CHECK'} {p}: related_cards={cards}, breadcrumb={bc}, wiki_refs={wiki}")
