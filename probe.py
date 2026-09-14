# -*- coding: utf-8 -*-
import re, json, pathlib
cache = json.load(open('image_cache.json', encoding='utf-8'))
t = pathlib.Path('articles/jp.html').read_text(encoding='utf-8')
m = re.findall(r'src=\"(https://[^\"]*80/80[^\"]*)\"', t)
print('80/80 in jp region page:', len(m), m[:2])
m2 = re.findall(r'src=\"(https://[^\"]*600/400[^\"]*)\"', t)
print('600/400:', len(m2))
sizes = set()
for v in cache.values():
    sm = re.search(r'/(\d+)px-', v.get('thumb',''))
    sizes.add(sm.group(1) if sm else '?')
print('cache thumb sizes:', sizes)
# sample thumb URL
print([v.get('thumb') for v in cache.values()][0])
