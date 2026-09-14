# -*- coding: utf-8 -*-
"""把 5 國美食集群頁加入 sitemap.xml"""
import datetime

SITE = 'https://travel-guide-esimart.pages.dev'
FOOD_PAGES = [f'{SITE}/guides/{r}-food.html' for r in ['jp','kr','tw','eu','oce']]

sm = open('sitemap.xml', encoding='utf-8').read()
lines = sm.rstrip().split('\n')
added = 0
for url in FOOD_PAGES:
    if url not in sm:
        lines.insert(len(lines) - 1,
                     f'<url><loc>{url}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod></url>')
        added += 1

open('sitemap.xml', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print(f'Added {added} new food cluster URLs to sitemap.xml')
