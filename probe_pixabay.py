# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, json, sys
KEY = '39894189-8822531df0830fb07f58a9a69'
params = {'q': 'Seoul Namsan tower', 'per_page': 3, 'safesearch': 'true', 'image_type': 'photo', 'category': 'nature'}
url = 'https://pixabay.com/api/?key=' + KEY + '&' + urllib.parse.urlencode(params)
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    d = json.loads(urllib.request.urlopen(req, timeout=25).read())
    sys.stdout.buffer.write(('totalHits: ' + str(d.get('totalHits')) + chr(10)).encode())
    for h in d.get('hits', []):
        sys.stdout.buffer.write(('pid %s  %sx%s  %s\n' % (h.get('id'), h.get('imageWidth'), h.get('imageHeight'), (h.get('webformatURL') or h.get('largeImageURL',''))[:80])).encode())
except Exception as e:
    sys.stdout.buffer.write(('ERR: ' + str(e) + chr(10)).encode())
