# -*- coding: utf-8 -*-
import urllib.request, re

BASE = 'https://travel-guide-esimart.pages.dev'
H = {'User-Agent': 'Mozilla/5.0'}

def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=H)).read().decode('utf-8', 'replace')

for slug in ['kr-jeju', 'eu-amsterdam', 'tw-shilin-old', 'oce-wellington']:
    c = get(BASE + '/articles/' + slug + '.html')
    m = re.search(r'meta http-equiv="refresh" content="0; url=[^"]*?/articles/([a-z0-9\-]+)\.html"', c)
    print(slug, '->', m.group(1) if m else 'NO REDIRECT')

t = get(BASE + '/articles/kr-jeju-city.html')
print('kr-jeju-city is full article:', len(t) > 5000)
