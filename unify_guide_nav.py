# -*- coding: utf-8 -*-
import re, glob, pathlib
SITE = 'https://travel-guide-esimart.pages.dev'
STD_NAV = '''  <nav class="topnav">
  <a class="brand" href="{SITE}/"><em>旅遊通</em> eSIM</a>
  <button class="menu-toggle" onclick="document.querySelector('.nav-links').classList.toggle('active')">&#9776;</button>
  <div class="nav-links">
    <a href="{SITE}/">首頁</a>
    <a href="{SITE}/articles/">全部攻略</a>
    <a href="{SITE}/articles/jp.html">日本</a>
    <a href="{SITE}/articles/kr.html">韓國</a>
    <a href="{SITE}/articles/tw.html">台灣</a>
    <a href="{SITE}/articles/eu.html">歐洲</a>
    <a href="{SITE}/articles/oce.html">澳洲</a>
    <a class="btn-nav" href="https://travel-guide.esimart.cc/goods" target="_blank" rel="noopener">eSIM 方案</a>
  </div>
</nav>'''.format(SITE=SITE)
n = 0
for f in glob.glob('guides/*.html'):
    p = pathlib.Path(f)
    t = p.read_text(encoding='utf-8')
    m = re.search(r'<nav class="site-header">.*?</nav>', t, re.S)
    if m:
        t = t.replace(m.group(0), STD_NAV)
        p.write_text(t, encoding='utf-8')
        n += 1
print('guide pages normalized to topnav:', n)
