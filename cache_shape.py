# -*- coding: utf-8 -*-
import json, sys
c = json.load(open('image_cache.json', encoding='utf-8'))
sys.stdout.buffer.write(('cache entries: %d\n' % len(c)).encode())
# show the value shape
k = list(c.keys())[0]
sys.stdout.buffer.write((repr(c[k]) + chr(10)).encode('utf-8','replace'))
# how many have a 'pixabay' url
n = sum(1 for v in c.values() if 'pixabay' in (v.get('thumb') or v.get('url') or ''))
sys.stdout.buffer.write(('pixabay urls in cache: %d\n' % n).encode())
# sample keys
sys.stdout.buffer.write(('keys sample: ' + repr(list(c.keys())[:6]) + chr(10)).encode())
