# -*- coding: utf-8 -*-
import urllib.request, socket, re
socket.setdefaulttimeout(20)
def get(u):
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125'})
    return urllib.request.urlopen(req).read().decode('utf-8', errors='replace')
live_home = get('https://travel-guide-esimart.pages.dev/')
open('_live_home.html', 'w', encoding='utf-8').write(live_home)
live_css = get('https://travel-guide-esimart.pages.dev/assets/style.css')
open('_live_css.css', 'w', encoding='utf-8').write(live_css)
print('live home len', len(live_home))
print('live css len', len(live_css))
print('live css head:', live_css[:200])
