#!/usr/bin/env python3
"""Build articles/index.html and sitemap.xml from all article files."""
import os, re, html

ARTICLES_DIR = 'articles'
BASE = 'https://chiag455371.github.io/travel-guide.esimart'
DISTRIBUTOR = 'https://travel-guide.esimart.cc/goods'

exclude = {'index.html', 'jp.html', 'kr.html', 'tw.html', 'eu.html', 'oce.html'}
files = sorted([f for f in os.listdir(ARTICLES_DIR) if f.endswith('.html') and f not in exclude])

articles = []
for f in files:
    path = os.path.join(ARTICLES_DIR, f)
    content = open(path, encoding='utf-8').read()
    m = re.search(r'<title>(.*?)</title>', content)
    title_raw = m.group(1).strip() if m else f.replace('.html', '')
    title = re.sub(r'\s*[｜-]\s*旅遊通.*$', '', title_raw).strip()
    m2 = re.search(r'<meta name="description" content="(.*?)">', content)
    desc = (m2.group(1)[:120] + '...') if m2 else (title[:40] + '...')
    m3 = re.search(r'<img[^>]+src="(https://loremflickr[^"]+)"', content)
    img = m3.group(1) if m3 else ''
    slug = f.replace('.html', '')
    region = 'jp' if slug.startswith('jp-') else 'kr' if slug.startswith('kr-') else 'tw' if slug.startswith('tw-') else 'eu' if slug.startswith('eu-') else 'oce' if slug.startswith('oce-') else 'other'
    articles.append({'slug': slug, 'title': title, 'desc': desc, 'img': img, 'region': region})

regions = {'jp':[], 'kr':[], 'tw':[], 'eu':[], 'oce':[]}
for a in articles:
    if a['region'] in regions:
        regions[a['region']].append(a)

FLAG = {'jp':'🇯🇵','kr':'🇰🇷','tw':'🇹🇼','eu':'🇪🇺','oce':'🇦🇺'}
REGION_NAME = {'jp':'日本','kr':'韓國','tw':'台灣','eu':'歐洲','oce':'澳洲'}

# Build article cards HTML
def card_html(a):
    t = html.escape(a['title'])
    d = html.escape(a['desc'][:100] + '...')
    img = a['img'] if a['img'] else f'https://loremflickr.com/600/400/{a["region"]},travel?lock=9999&w=1200&h=600&fit=crop'
    url = f'{BASE}/articles/{a["slug"]}.html'
    return f'''      <a href="{url}" class="article-card">
        <div class="card-img-wrapper"><img class="card-img" src="{img}" alt="{t}" loading="lazy"></div>
        <div class="card-body">
          <span class="card-title">{t}</span>
          <span class="card-desc">{d}</span>
          <div class="card-meta"><span class="card-meta-dot"></span><span>約 8 分鐘閱讀</span></div>
        </div>
      </a>'''

# Build region sections
region_sections = ''
for r in ['jp', 'kr', 'tw', 'eu', 'oce']:
    items = regions.get(r, [])
    if not items:
        continue
    cards = '\n'.join(card_html(a) for a in items)
    region_sections += f'''  <div class="region-section">
    <div class="region-header">
      <div class="region-icon">{FLAG[r]}</div>
      <h2>{REGION_NAME[r]}旅遊攻略</h2>
      <a href="{BASE}/articles/{r}.html">查看全部 {len(items)} 篇 &#8594;</a>
    </div>
    <div class="card-grid">
{cards}
    </div>
  </div>
'''

# Top filter chips
chips = ''
for r in ['jp', 'kr', 'tw', 'eu', 'oce']:
    count = len(regions.get(r, []))
    chips += f'    <a href="{BASE}/articles/{r}.html" style="padding:14px 20px;background:var(--panel);border:1px solid var(--panel-border);border-radius:var(--radius-sm);font-weight:600;text-align:center;min-width:120px">{FLAG[r]} {REGION_NAME[r]} ({count}篇)</a>\n'

html_content = f'''<!doctype html>
<html lang="zh-Hant">
<head>
  <link rel="stylesheet" href="/travel-guide.esimart/assets/style.css">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>旅遊攻略｜旅遊通 eSIM</title>
  <meta name="description" content="旅遊通提供日本、韓國、歐洲、台灣、澳洲等地區的完整旅遊攻略，包含景點介紹、美食推薦和 eSIM 方案建議。共 {len(articles)} 篇深度攻略。">
  <link rel="canonical" href="{BASE}/articles/">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="zh_TW">
  <meta property="og:title" content="旅遊攻略｜旅遊通 eSIM">
  <meta property="og:description" content="共 {len(articles)} 篇深度旅遊攻略，涵蓋日本、韓國、歐洲、台灣、澳洲。">
  <meta property="og:url" content="{BASE}/articles/">
</head>
<body>
<nav class="topnav">
  <a class="brand" href="{BASE}/"><em>旅遊通</em> eSIM</a>
  <button class="menu-toggle" onclick="document.querySelector('.nav-links').classList.toggle('active')">&#9776;</button>
  <div class="nav-links">
    <a href="{BASE}/">首頁</a>
    <a href="{BASE}/articles/">全部攻略</a>
    <a href="{BASE}/articles/jp.html">&#127471;&#127476; 日本</a>
    <a href="{BASE}/articles/kr.html">&#127450;&#127462; 韓國</a>
    <a href="{BASE}/articles/tw.html">&#127488;&#127463; 台灣</a>
    <a href="{BASE}/articles/eu.html">&#127466;&#127480; 歐洲</a>
    <a href="{BASE}/articles/oce.html">&#127462;&#127480; 澳洲</a>
    <a class="btn-nav" href="{DISTRIBUTOR}" target="_blank" rel="noopener">&#128722; eSIM 方案</a>
  </div>
</nav>
<div class="wrap">
  <h1 style="font-size:1.8rem;font-weight:900;margin-bottom:8px">&#128214; 旅遊攻略</h1>
  <p style="color:var(--text-soft);margin-bottom:12px;font-size:1.05rem">以下文章由旅遊通編輯團隊撰寫，每篇都包含完整行程安排、預算估算和 eSIM 方案建議。</p>
  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:40px">
{chips}
  </div>
  <hr class="divider">
{region_sections.rstrip()}
  <hr class="divider">
  <div class="esim-cta">
    <h2>&#9992; 想出國玩，網路怎麼辦？</h2>
    <p>旅遊通 eSIM 覆蓋全球 58 國，QR Code 掃描安裝，落地立即連網。<br>支援 4G/LTE 高速，LINE、IG 隨時上傳，全程無隱藏費用。</p>
    <a class="btn" href="{DISTRIBUTOR}" target="_blank" rel="noopener">查看所有 eSIM 方案 &#8594;</a>
  </div>
</div>
<footer>
  <p>&#169; 2024-2026 旅遊通 eSIM｜全球 58 國流量卡</p>
  <p><a href="mailto:Service@esimart.com">Service@esimart.com</a>｜<a href="https://line.me/R/ti/p/@esimart_oa" target="_blank" rel="noopener">LINE: @esimart_oa</a></p>
</footer>
</body>
</html>
'''

with open(os.path.join(ARTICLES_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'articles/index.html written: {len(articles)} articles')
for r in ['jp','kr','tw','eu','oce']:
    print(f'  {r}: {len(regions.get(r,[]))} articles')

# Also update sitemap.xml
sitemap_urls = [
    f'  <url>\n    <loc>{BASE}/</loc>\n    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n  </url>',
    f'  <url>\n    <loc>{BASE}/articles/</loc>\n    <changefreq>daily</changefreq>\n    <priority>0.9</priority>\n  </url>',
]
for r in ['jp','kr','tw','eu','oce']:
    sitemap_urls.append(f'  <url>\n    <loc>{BASE}/articles/{r}.html</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>')
for a in articles:
    sitemap_urls.append(f'  <url>\n    <loc>{BASE}/articles/{a["slug"]}.html</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>')

sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemap_urls)}
</urlset>
'''
with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)

print(f'sitemap.xml written: {len(sitemap_urls)} URLs')
