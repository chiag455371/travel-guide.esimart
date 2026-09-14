# -*- coding: utf-8 -*-
import re, urllib.request

BASE = "https://travel-guide-esimart.pages.dev/"

def fetch(p):
    req = urllib.request.Request(BASE + p, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "ignore")

for region in ['jp', 'kr', 'tw', 'eu', 'oce']:
    p = f"guides/{region}-food.html"
    c = fetch(p)
    cards = c.count('class="card"')
    bc = "BreadcrumbList" in c
    ok = "OK" if cards >= 1 and bc else "CHECK"
    print(f"{ok} {p}: cards={cards}, breadcrumb={bc}")
