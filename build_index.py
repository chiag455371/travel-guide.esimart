#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重建 articles/index.html — 全量收錄「核心頁」，消滅孤兒頁。

修正紀錄（2026-10-31）：
1. 卡片 URL 一律不帶 .html（Pages 會把 /x.html 308 轉到 /x，
   帶 .html 的內鏈等於把 534 個轉址種回索引頁）。
2. 只列核心頁（tier_content.py 的 core），noindex 變體頁不列，
   避免把低差異頁面推給 Google。
3. CSS 路徑修正為 /assets/style.css（原本寫死舊子目錄，樣式會 404）。
4. sitemap 交給 update_sitemap.py 產生，本檔不再寫 sitemap。
"""
import os
import re
import html

from tier_content import build_plan

ARTICLES_DIR = 'articles'
BASE = 'https://travel-guide-esimart.pages.dev'
DISTRIBUTOR = 'https://travel-guide.esimart.cc/goods'

EXCLUDE = {'index.html', 'jp.html', 'kr.html', 'tw.html', 'eu.html', 'oce.html'}

FLAG = {'jp': '🇯🇵', 'kr': '🇰🇷', 'tw': '🇹🇼', 'eu': '🇪🇺', 'oce': '🇦🇺', 'esim': '📡'}
REGION_NAME = {'jp': '日本', 'kr': '韓國', 'tw': '台灣', 'eu': '歐洲', 'oce': '澳洲', 'esim': 'eSIM 全球上網'}


def region_of(slug):
    for r in ('jp', 'kr', 'tw', 'eu', 'oce', 'esim'):
        if slug.startswith(r + '-'):
            return r
    return 'other'


def read_article(slug):
    path = os.path.join(ARTICLES_DIR, slug + '.html')
    content = open(path, encoding='utf-8').read()
    m = re.search(r'<title>(.*?)</title>', content)
    title_raw = m.group(1).strip() if m else slug
    title = re.sub(r'\s*[｜|]\s*.*$', '', title_raw).strip() or title_raw
    m2 = re.search(r'<meta name="description" content="(.*?)">', content)
    desc = m2.group(1) if m2 else title
    m3 = re.search(r'<img[^>]+src="(https://[^"]+)"', content)
    img = m3.group(1) if m3 else ''
    return {'slug': slug, 'title': title, 'desc': desc, 'img': img, 'region': region_of(slug)}


def card_html(a):
    t = html.escape(a['title'])
    d = html.escape(a['desc'][:100] + ('...' if len(a['desc']) > 100 else ''))
    img = a['img'] or f'https://loremflickr.com/600/400/{a["region"]},travel?lock=9999'
    url = f'{BASE}/articles/{a["slug"]}'
    return f'''      <a href="{url}" class="article-card">
        <div class="card-img-wrapper"><img class="card-img" src="{img}" alt="{t}" loading="lazy"></div>
        <div class="card-body">
          <span class="card-title">{t}</span>
          <span class="card-desc">{d}</span>
          <div class="card-meta"><span class="card-meta-dot"></span><span>約 8 分鐘閱讀</span></div>
        </div>
      </a>'''


def main():
    plan = build_plan()
    core = plan['core']
    articles = [read_article(s) for s in core]
    articles = [a for a in articles if a['region'] != 'other']

    regions = {r: [] for r in FLAG.keys()}
    for a in articles:
        regions[a['region']].append(a)

    region_sections = ''
    for r in ('jp', 'kr', 'tw', 'eu', 'oce'):
        items = regions[r]
        if items:
            cards = '\n'.join(card_html(a) for a in items)
            region_sections += f'''  <div class="region-section">
    <div class="region-header">
      <div class="region-icon">{FLAG[r]}</div>
      <h2>{REGION_NAME[r]}旅遊攻略</h2>
      <a href="{BASE}/articles/{r}">查看全部 {len(items)} 篇 &#8594;</a>
    </div>
    <div class="card-grid">
{cards}
    </div>
  </div>
'''

    # eSIM 区块（放在最后，靠近 CTA）
    esim_items = regions.get('esim', [])
    if esim_items:
        esim_cards = '\n'.join(card_html(a) for a in esim_items)
        region_sections += f'''  <div class="region-section">
    <div class="region-header">
      <div class="region-icon">{FLAG['esim']}</div>
      <h2>📡 eSIM 上網攻略</h2>
      <a href="{DISTRIBUTOR}">查看所有 eSIM 方案 &#8594;</a>
    </div>
    <div class="card-grid">
{esim_cards}
    </div>
  </div>
'''

    chips = ''
    for r in ('jp', 'kr', 'tw', 'eu', 'oce'):
        count = len(regions.get(r, []))
        if count > 0:
            chips += (
                f'    <a href="{BASE}/articles/{r}" style="padding:14px 20px;background:var(--panel);'
                f'border:1px solid var(--panel-border);border-radius:var(--radius-sm);font-weight:600;'
                f'text-align:center;min-width:120px">{FLAG[r]} {REGION_NAME[r]} ({count}篇)</a>\n'
            )
    # eSIM chip
    if esim_items:
        chips += (
            f'    <a href="{DISTRIBUTOR}" target="_blank" style="padding:14px 20px;background:#0070f8;'
            f'color:#fff;border:1px solid #0070f8;border-radius:var(--radius-sm);font-weight:600;'
            f'text-align:center;min-width:120px">{FLAG["esim"]} eSIM 方案 ({len(esim_items)}篇分析)</a>\n'
        )

    html_content = f'''<!doctype html>
<html lang="zh-Hant">
<head>
  <link rel="stylesheet" href="/assets/style.css">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>旅遊攻略總覽｜日本韓國歐洲台灣澳洲 eSIM｜旅遊通</title>
  <meta name="description" content="旅遊通整理日本、韓國、歐洲、台灣、澳洲 {len(regions.get('jp',[]))} 篇日本攻略、{len(regions.get('kr',[]))} 篇韓國攻略、{len(regions.get('tw',[]))} 篇台灣攻略，以及 {len(esim_items)} 篇 eSIM 全球上網方案比較。">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{BASE}/articles/">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="zh_TW">
  <meta property="og:title" content="旅遊攻略總覽｜旅遊通 eSIM">
  <meta property="og:description" content="共 {len(articles)} 篇旅遊攻略，涵蓋日本、韓國、歐洲、台灣、澳洲。">
  <meta property="og:url" content="{BASE}/articles/">
</head>
<body>
<nav class="topnav">
  <a class="brand" href="{BASE}/"><em>旅遊通</em> eSIM</a>
  <button class="menu-toggle" onclick="document.querySelector('.nav-links').classList.toggle('active')">&#9776;</button>
  <div class="nav-links">
    <a href="{BASE}/">首頁</a>
    <a href="{BASE}/articles/">全部攻略</a>
    <a href="{BASE}/articles/jp">&#127471;&#127476; 日本</a>
    <a href="{BASE}/articles/kr">&#127450;&#127462; 韓國</a>
    <a href="{BASE}/articles/tw">&#127488;&#127463; 台灣</a>
    <a href="{BASE}/articles/eu">&#127466;&#127480; 歐洲</a>
    <a href="{BASE}/articles/oce">&#127462;&#127480; 澳洲</a>
    <a class="btn-nav" href="{DISTRIBUTOR}" target="_blank" rel="noopener">&#128722; eSIM 方案</a>
  </div>
</nav>
<div class="wrap">
  <h1 style="font-size:1.8rem;font-weight:900;margin-bottom:8px">&#128214; 旅遊攻略總覽</h1>
  <p style="color:var(--text-soft);margin-bottom:12px;font-size:1.05rem">以下 {len(articles)} 篇由旅遊通編輯團隊整理，每篇包含景點重點、交通方式、預算估算與 eSIM 上網建議。</p>
  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:40px">
{chips}  </div>
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

    out = os.path.join(ARTICLES_DIR, 'index.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f'articles/index.html written: {len(articles)} 篇（核心頁）')
    for r in ('jp', 'kr', 'tw', 'eu', 'oce', 'esim'):
        print(f'  {r}: {len(regions.get(r, []))} 篇')


if __name__ == '__main__':
    main()
