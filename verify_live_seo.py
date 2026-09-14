# -*- coding: utf-8 -*-
import urllib.request, re

BASE = 'https://travel-guide-esimart.pages.dev'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=HEADERS)).read().decode('utf-8', 'replace')

art = get(BASE + '/articles/jp-kyoto-fushimi.html')
print('related cards in jp-kyoto-fushimi:', len(re.findall(r'related-card', art)))
print('breadcrumb in article:', 'breadcrumb' in art)

jp = get(BASE + '/articles/jp.html')
print('breadcrumb in jp.html:', 'breadcrumb' in jp)
print('popular list in jp.html:', 'popular-list' in jp)

g = get(BASE + '/guides/jp-esim-guide.html')
print('guide FAQPage:', 'FAQPage' in g)
print('guide CTA:', 'travel-guide.esimart.cc/goods' in g)

sm = get(BASE + '/sitemap.xml')
print('sitemap guide urls:', sm.count('/guides/'))
