# -*- coding: utf-8 -*-
import urllib.request, socket, re
socket.setdefaulttimeout(30)
req = urllib.request.Request('https://incredible-malasada-0583f9.netlify.app/articles/jp.html',
                             headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36'})
r = urllib.request.urlopen(req)
t = r.read().decode('utf-8', errors='replace')
print('status', r.status, 'len', len(t))
open('_ref_jp.html', 'w', encoding='utf-8').write(t)
print('stylesheets:', re.findall(r'href=\"([^\"]*\.css[^\"]*)\"', t))
print('style tags:', len(re.findall(r'<style', t)))
m = re.search(r'<title>([^<]+)</title>', t)
print('title:', m.group(1) if m else None)
print('flag chars:', [ch for ch in t if ord(ch) > 0x1F000][:10])
