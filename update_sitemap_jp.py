# -*- coding: utf-8 -*-
"""加入日文字站 URL 到 sitemap.xml"""
import datetime

SITE = 'https://travel-guide-esimart.pages.dev'
JP_PAGES = [f'{SITE}/jp/']

sm = open('sitemap.xml', encoding='utf-8').read()
lines = sm.rstrip().split('\n')
added = 0
for url in JP_PAGES:
    if url not in sm:
        lines.insert(len(lines) - 1,
                     f'<url><loc>{url}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod></url>')
        added += 1

open('sitemap.xml', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print(f'Added {added} JP URLs to sitemap.xml')
