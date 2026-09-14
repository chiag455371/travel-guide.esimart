# -*- coding: utf-8 -*-
import re, pathlib, json, sys
c = json.load(open('pixel_cache.json',encoding='utf-8'))
for r in ['jp','kr','eu','tw','oce']:
    t = pathlib.Path('articles/%s.html' % r).read_text(encoding='utf-8')
    for m in re.finditer(r'src=\"https://thumb\.wikimedia[^\"]+\"', t):
        seg = t[max(0,m.start()-700):m.start()]
        hrefs = re.findall(r'/articles/([a-z0-9\-]+)\.html', seg)
        slug = hrefs[-1] if hrefs else 'NOHREF'
        sys.stdout.buffer.write(('%s exact=%s prefix=%s\n' % (slug, bool((c.get(slug) or {}).get('url')), bool((c.get(slug.rsplit('-',1)[0]) or {}).get('url')))).encode('utf-8','replace'))
