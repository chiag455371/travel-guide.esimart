# -*- coding: utf-8 -*-
import json, pathlib, re
c = json.load(open('pixel_cache.json',encoding='utf-8'))
print('jp-kobe-Night in cache:', bool((c.get('jp-kobe-Night') or {}).get('url')))
t = pathlib.Path('articles/jp-kobe-Night.html').read_text(encoding='utf-8')
print('its img hosts:', re.findall(r'src=\"(https?://[^\"]{0,30})', t)[:3])
# check title
print('title:', re.search(r'<title>([^<]+)', t).group(1)[:40])
