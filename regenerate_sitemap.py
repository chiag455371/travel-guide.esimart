# -*- coding: utf-8 -*-
"""Regenerate sitemap with new Cloudflare domain."""
import re, glob, datetime

new_base = 'https://travel-guide-esimart.pages.dev'
urls = []
urls.append(new_base + '/')
urls.append(new_base + '/articles/')

region_files = ['jp', 'kr', 'tw', 'eu', 'oce']
for r in region_files:
    urls.append(new_base + '/articles/' + r + '.html')

for path in sorted(glob.glob('articles/*.html')):
    name = path.replace('articles/', '').replace('.html', '')
    if name in region_files:
        continue
    urls.append(new_base + '/articles/' + name + '.html')

lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
today = datetime.date.today().isoformat()
for i, url in enumerate(urls):
    priority = '1.0' if i == 0 else ('0.9' if i == 1 else '0.8')
    changefreq = 'daily' if i < 2 else 'weekly'
    lines.append('  <url>')
    lines.append('    <loc>' + url + '</loc>')
    lines.append('    <lastmod>' + today + '</lastmod>')
    lines.append('    <changefreq>' + changefreq + '</changefreq>')
    lines.append('    <priority>' + priority + '</priority>')
    lines.append('  </url>')
lines.append('</urlset>')

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')
print('Sitemap updated with ' + str(len(urls)) + ' URLs')
