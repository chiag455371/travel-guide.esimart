# -*- coding: utf-8 -*-
"""Re-add guide CTA links to region pages after generator overwrote them."""
import re

BASE = 'https://travel-guide-esimart.pages.dev'
for region in ['jp', 'kr', 'tw', 'eu', 'oce']:
    f = f'articles/{region}.html'
    c = open(f, encoding='utf-8').read()
    if f'guides/{region}-esim-guide.html' in c:
        print(region, 'already has guide link')
        continue
    m = re.search(r'<h1[^>]*>[^<]+</h1>', c)
    link = (
        f'\n<a href="{BASE}/guides/{region}-esim-guide.html" '
        f'class="guide-cta" style="display:inline-block;margin:0.5rem 0;padding:0.5rem 1rem;'
        f'background:#e63946;color:#fff;border-radius:8px;text-decoration:none;font-weight:700">'
        f'📶 {region.upper()} eSIM 購買指南 →</a>')
    if m:
        c = c[:m.end()] + link + c[m.end():]
    open(f, 'w', encoding='utf-8').write(c)
    print(region, 'guide link added')
