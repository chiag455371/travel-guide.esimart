# -*- coding: utf-8 -*-
import re, pathlib, json, sys
c = json.load(open('pixel_cache.json',encoding='utf-8'))
for r in ['jp','kr','eu','tw','oce']:
    t = pathlib.Path('articles/%s.html' % r).read_text(encoding='utf-8')
    # find blocks with wiki img
    for m in re.finditer(r'<a href=\"[^\"]*/articles/([a-z0-9\-]+)\.html\"[^>]*class=\"article-card\">', t):
        start = m.start()
        seg = t[start:start+500]
        if 'wikimedia' in seg:
            s = m.group(1)
            sys.stdout.buffer.write((('%s | exact=%s prefix=%s\n' % (s, bool((c.get(s) or {}).get('url')), bool((c.get(s.rsplit('-',1)[0]) or {}).get('url')))).encode('utf-8','replace')))
