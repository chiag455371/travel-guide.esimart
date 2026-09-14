# -*- coding: utf-8 -*-
import urllib.request, re
def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode('utf-8'), r.status
for page in ['articles/jp.html','articles/kr.html','articles/eu.html','articles/tw.html','articles/oce.html','articles/eu-brno-castle.html','guides/jp-esim-guide.html','index.html']:
    try:
        t, st = get('https://travel-guide-esimart.pages.dev/' + page)
        print(page, st, '| broken:', len(re.findall(r'loremflickr|picsum', t)))
    except Exception as e:
        print(page, 'ERR', str(e)[:50])
