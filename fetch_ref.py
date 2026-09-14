# -*- coding: utf-8 -*-
import urllib.request, re
def get(u):
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, timeout=20).read().decode('utf-8')
t = get('https://incredible-malasada-0583f9.netlify.app/')
open('_netlify_ref.html', 'w', encoding='utf-8').write(t)
print('len:', len(t))
print('stylesheets:', re.findall(r'<link[^>]*stylesheet[^>]*>', t)[:5])
print('css files:', re.findall(r'href=\"([^\"]*\.css[^\"]*)\"', t)[:5])
m = re.search(r'<title>([^<]+)</title>', t)
print('title:', m.group(1) if m else None)
print('inline style blocks:', len(re.findall(r'<style', t)))
print('classes sample:', re.findall(r'class=\"([a-z\-]+)\"', t)[:20])
