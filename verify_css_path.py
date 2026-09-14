# -*- coding: utf-8 -*-
import urllib.request, re
def get(u):
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, timeout=15).read().decode('utf-8', errors='replace')
for page in ['articles/jp.html','articles/kr.html','articles/tw.html','articles/eu.html','articles/oce.html']:
    t = get('https://travel-guide-esimart.pages.dev/' + page)
    css_link = re.search(r'href=\"([^\"]*style.css[^\"]*)\"', t)
    print(page, '| css:', css_link.group(1) if css_link else 'NONE')
    broken = len(re.findall(r'loremflickr|picsum', t))
    print('   broken imgs:', broken)
