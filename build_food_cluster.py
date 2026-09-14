# -*- coding: utf-8 -*-
"""建立 5 國「美食與市場」集群頁: 收錄該區美食/咖啡/夜市相關文章
- 生成 guides/{region}-food.html
- 內鏈到美食文章卡片 + 回指南頁 + 麵包屑 Schema
- 冪等: 已存在則跳過
"""
import os, re, glob, json, hashlib
_IMG_CACHE = {}
try:
    _IMG_CACHE = json.load(open('image_cache.json', encoding='utf-8'))
except Exception:
    pass
_REGION_T = {}
for _k, _v in _IMG_CACHE.items():
    _t = _v.get('thumb') or _v.get('url')
    if _t: _REGION_T.setdefault(_k.split('-')[0], []).append(_t), json

SITE = 'https://travel-guide-esimart.pages.dev'
REGION_NAMES = {'jp': '日本', 'kr': '韓國', 'tw': '台灣', 'eu': '歐洲', 'oce': '大洋洲'}
FOOD_KW = ['food', '夜', 'market', 'ramen', 'gyoza', 'bingsu', 'bibimbap',
           '寿司', 'street', 'coffee', 'cafe', 'café', '小吃', '咖啡']
TITLE_DATA = {
    'jp': ('日本美食與咖啡全攻略：從拉麵到甜點的必吃地點',
           '日本美食怎麼吃？整理了東京、大阪、福岡等城市的必吃拉麵、咖啡、甜點與夜市推薦，搭配 eSIM 邊玩邊搜，落地即吃。'),
    'kr': ('韓國美食與咖啡全攻略：從烤豬肉到韓式甜點的必吃地點',
           '韓國美食怎麼吃？整理了首爾、釜山、濟州島的必吃烤豬肉、韓式甜點、咖啡街與夜市推薦，搭配 eSIM 邊玩邊搜。'),
    'tw': ('台灣美食與夜市全攻略：從小吃到咖啡的必吃地點',
           '台灣美食怎麼吃？整理了台北、台南、花蓮等城市的必吃夜市、小吃、咖啡與甜點推薦，搭配 eSIM 邊玩邊搜。'),
    'eu': ('歐洲美食與咖啡館全攻略：從甜點到市場餐廳的必吃地點',
           '歐洲美食怎麼吃？整理了巴黎、羅馬、阿姆斯特丹等城市的必吃甜點、咖啡館、市場與餐廳推薦，搭配 eSIM 邊玩邊搜。'),
    'oce': ('澳洲美食與咖啡全攻略：從早午餐到咖啡文化的必吃地點',
           '澳洲美食怎麼吃？整理了悉尼、墨爾本、阿德萊德的必吃早午餐、咖啡、市場與餐廳推薦，搭配 eSIM 邊玩邊搜。'),
}


def food_articles(region):
    out = []
    for f in sorted(glob.glob(f'articles/{region}-*.html')):
        c = open(f, encoding='utf-8').read()
        if 'http-equiv' in c and len(c) < 500:
            continue
        slug = os.path.basename(f)[:-5]
        m = re.search(r'<title>([^<]+)</title>', c)
        t = (m.group(1) if m else slug)
        hay = slug + t
        if any(k.lower() in hay.lower() for k in FOOD_KW):
            tm = re.search(r'og:image" content="([^"]+)"', c)
            out.append({'slug': slug, 'title': t.split('｜')[0].strip(), 'img': tm.group(1) if tm else ''})
    return out


def build_page(region):
    name = REGION_NAMES[region]
    title, desc = TITLE_DATA[region]
    arts = food_articles(region)[:8]

    cards = []
    for a in arts:
        img = (f'<div class="card-img-wrapper"><img class="card-img" src="{a["img"]}" '
               f'alt="{a["title"]}" loading="lazy"></div>' if a['img'] else '')
        cards.append(
            f'      <a href="{SITE}/articles/{a["slug"]}.html" class="card">'
            f'{img}<div class="card-body"><span class="card-title">{a["title"]}</span></div></a>')

    rel_items = []
    for f in sorted(glob.glob(f'articles/{region}-*.html')):
        c0 = open(f, encoding='utf-8').read()
        if 'http-equiv' in c0 and len(c0) < 500:
            continue
        slug2 = os.path.basename(f)[:-5]
        m2 = re.search(r'<title>([^<]+)</title>', c0)
        t2 = (m2.group(1) if m2 else slug2).split('｜')[0].strip()[:40]
        rel_items.append((slug2, t2))
        if len(rel_items) >= 6:
            break
    rel_html = chr(10).join(
        f'      <a href="{SITE}/articles/{s}.html" class="related-card">'
        f'<div class="card-body"><span class="card-title">{t}</span></div></a>'
        for s, t in rel_items)

    bc_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首頁", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": name + "美食攻略", "item": f"{SITE}/guides/{region}-food.html"}
        ]
    }, ensure_ascii=False, indent=4)

    html = f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}｜旅遊通 eSIM</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{SITE}/guides/{region}-food.html">
  <meta property="og:type" content="article">
  <meta property="og:image" content="(_REGION_T.get(region, [_REGION_T.values().__next__() if _REGION_T else 'https://upload.wikimedia.org/wikipedia/commons/4/4b/Amsterdam_-_48390199071.jpg'])[0])">
  <link rel="canonical" href="{SITE}/guides/{region}-food.html">
  <link rel="stylesheet" href="{SITE}/assets/style.css">
  <script type="application/ld+json">
{bc_json}
  </script>
</head>
<body>
  <nav aria-label="breadcrumb" class="breadcrumb-nav"><ol class="breadcrumb">
    <li><a href="{SITE}/">首頁</a></li>
    <li><a href="{SITE}/guides/{region}-esim-guide.html">{name} eSIM 指南</a></li>
    <li aria-current="page">{name}美食攻略</li>
  </ol></nav>

  <main class="article">
    <h1>{title}</h1>
    <p class="lead">{desc}</p>

    <p>出遊{name}最怕網路中斷，買一份 <a href="{SITE}/guides/{region}-esim-guide.html">{name} eSIM</a> 落地即連網，邊看地圖邊找餐廳、邊上網比較評價。以下為精選{name}美食與咖啡相關攻略：</p>

    <h2>{name}美食與咖啡精選</h2>
    <div class="card-grid">
{chr(10).join(cards)}
    </div>

    <h2>出遊{name}的小提醒</h2>
    <ul>
      <li>多數店家支援信用卡與無接觸支付，但仍建議準備少量現金。</li>
      <li>熱門美食街週五到週日尖峰時段常大排長龍，可錯開 19:00–21:00 用餐時段。</li>
      <li>手機開啟「節約資料」模式，搭配 eSIM 省流量。</li>
    </ul>

    <div class="cta-box">
      <h3>出發前：先買 {name} eSIM</h3>
      <p>QR Code 安裝、免實體卡、落地即連網。</p>
      <a class="btn" href="{SITE}/guides/{region}-esim-guide.html">前往{name} eSIM 指南 →</a>
    </div>

    <div class="related-section">
      <h2>延伸閱讀：{name}其他攻略</h2>
      <div class="related-grid">
{rel_html}
      </div>
    </div>
  </main>
</body>
</html>
'''
    out_path = f'guides/{region}-food.html'
    open(out_path, 'w', encoding='utf-8').write(html)
    print(f'  wrote {out_path} ({len(arts)} food cards, {len(rel_items)} related)')


for region in ['jp', 'kr', 'tw', 'eu', 'oce']:
    if os.path.exists(f'guides/{region}-food.html'):
        print(f'skip {region}-food.html (exists)')
        continue
    build_page(region)
print('done')
