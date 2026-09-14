# -*- coding: utf-8 -*-
import urllib.request, re
def get(u):
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, timeout=20).read().decode('utf-8', errors='replace')
t = get('https://incredible-malasada-0583f9.netlify.app/articles/jp.html')
open('_ref_jp.html', 'w', encoding='utf-8').write(t)
print('stylesheets:', re.findall(r'href=\"([^\"]*\.css[^\"]*)\"', t))
print('inline <style> count:', len(re.findall(r'<style', t)))
m = re.search(r'<title>([^<]+)</title>', t)
print('title:', m.group(1) if m else None)
i = t.find('<body')
print(t[i:i+600])
