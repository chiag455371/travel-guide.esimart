# -*- coding: utf-8 -*-
import re, glob, pathlib, sys
SITE = 'https://travel-guide-esimart.pages.dev'
STD_NAV = '''<nav class="topnav">
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
for f in glob.glob('guides/*-food.html'):
    p = pathlib.Path(f)
    t = p.read_text(encoding='utf-8')
    m = re.search(r'<body[^>]*>', t)
    pos = m.end()
    # remove any existing breadcrumb nav that sits as the very first child
    m2 = re.search(r'\s*<nav aria-label=\"breadcrumb\".*?</nav>', t[pos:], re.S)
    if m2:
        t = t[:pos] + t[pos+m2.end():]
        pos = m.end()
    t = t[:pos] + '\n  ' + STD_NAV + t[pos:]
    p.write_text(t, encoding='utf-8')
    n += 1
print('food pages got topnav:', n)
