# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, json, sys
KEY = '39894189-8822531df0830fb07f58a9a69'
params = {'q': 'Seoul Namsan tower', 'per_page': 2, 'image_type': 'photo', 'category': 'nature'}
url = 'https://pixabay.com/api/?key=' + KEY + '&' + urllib.parse.urlencode(params)
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
d = json.loads(urllib.request.urlopen(req, timeout=25).read())
h = d['hits'][0]
for k in h:
    sys.stdout.buffer.write(('%-22s %s\n' % (k, str(h[k])[:90])).encode('utf-8','replace'))
