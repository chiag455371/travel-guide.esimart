# -*- coding: utf-8 -*-
import re, pathlib, json, sys
c = json.load(open('pixel_cache.json',encoding='utf-8'))
for r in ['jp','kr','eu','tw','oce']:
    t = pathlib.Path('articles/%s.html' % r).read_text(encoding='utf-8')
    blocks = re.findall(r'<a href=\"[^\"]*/articles/([a-z0-9\-]+)\.html\"[^>]*class=\"article-card\">.*?</a>', t, re.S)
    allb = re.findall(r'/articles/([a-z0-9\-]+)\.html\" class=\"article-card\">(.*?)(?=<a href|$)', t, re.S)
    for slug, body in allb:
        if 'wikimedia' in body:
            sys.stdout.buffer.write((('%s exact=%s prefix=%s\n' % (slug, bool((c.get(slug) or {}).get('url')), bool((c.get(slug.rsplit('-',1)[0]) or {}).get('url')))).encode('utf-8','replace')))
