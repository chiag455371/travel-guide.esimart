# -*- coding: utf-8 -*-
import urllib.request, re, socket, json
from collections import Counter
socket.setdefaulttimeout(30)
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125'}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read().decode('utf-8', errors='replace')
base = 'https://travel-guide-esimart.pages.dev'
for r in ['jp','kr','tw','eu','oce']:
    t = get(base + '/articles/' + r + '.html')
    cards = re.findall(r'card-img\" src=\"([^\"]+)\"', t)
    c = Counter(cards)
    dup = {k:v for k,v in c.items() if v>1}
    print(r, 'cards:', len(cards), 'unique:', len(c), '| dup groups:', len(dup), '| css:', bool(re.search(r'style\.css', t)), '| wiki:', len(re.findall(r'wikimedia', t)))
    for u,n in list(dup.items())[:3]:
        print('   DUP x%d %s' % (n, u[-40:]))
# guide nav + css
g = get(base + '/guides/tw-esim-guide.html')
print('--- guide ---')
print('topnav:', 'class=\"topnav\"' in g, '| site-header:', 'site-header' in g, '| css:', bool(re.search(r'style\.css', g)))
f = get(base + '/guides/tw-food.html')
print('food topnav:', 'class=\"topnav\"' in f)
# spot check a pixabay url serves
import random
m = re.findall(r'card-img\" src=\"(https://pixabay[^\"]+)\"', t)
random.seed(1)
u = random.choice(m)
try:
    req = urllib.request.Request(u, headers=UA)
    rr = urllib.request.urlopen(req, timeout=30)
    print('sample img serves:', rr.status, len(rr.read()))
except Exception as e:
    print('sample img ERR', str(e)[:50])
