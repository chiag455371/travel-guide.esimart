# -*- coding: utf-8 -*-
import json, urllib.request, urllib.parse, time, pathlib, sys
KEY = '39894189-8822531df0830fb07f58a9a69'
UA = {'User-Agent': 'Mozilla/5.0 travel-bot'}
params = {'q': 'Korea', 'per_page': 5, 'image_type': 'photo', 'orientation': 'landscape'}
url = 'https://pixabay.com/api/?key=%s&%s' % (KEY, urllib.parse.urlencode(params))
try:
    r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30)
    d = json.loads(r.read())
    sys.stdout.buffer.write(('status ok, totalHits: ' + str(d.get('totalHits')) + chr(10)).encode())
    for h in d.get('hits', [])[:3]:
        sys.stdout.buffer.write(('  pid %s w=%s %s\n' % (h.get('id'), h.get('imageWidth'), (h.get('largeImageURL') or h.get('webformatURL',''))[:70])).encode('utf-8','replace'))
except Exception as e:
    sys.stdout.buffer.write(('ERR: ' + str(e) + chr(10)).encode())
