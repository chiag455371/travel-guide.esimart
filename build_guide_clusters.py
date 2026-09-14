# -*- coding: utf-8 -*-
"""為 5 國購買指南頁注入「地區攻略」內鏈清單,建立內容主題集群
- 從 articles 抓該區前 N 篇(依標題),插入指南頁的「延伸閱讀」區塊
- 若已有 related-section 則跳過(冪等)
"""
import os, re, glob, json, datetime

SITE = 'https://travel-guide-esimart.pages.dev'
REGION_NAMES = {'jp': '日本攻略', 'kr': '韓國攻略', 'tw': '台灣攻略',
                'eu': '歐洲攻略', 'oce': '大洋洲攻略'}
N = 8  # 每國列 8 篇


def titles_for(region):
    out = []
    for f in sorted(glob.glob(f'articles/{region}-*.html')):
        c = open(f, encoding='utf-8').read()
        if 'http-equiv' in c and len(c) < 500:  # redirect stub
            continue
        slug = os.path.basename(f)[:-5]
        m = re.search(r'<title>([^<]+)</title>', c)
        t = (m.group(1) if m else slug).split('｜')[0].strip()
        og = re.search(r'og:image" content="([^"]+)"', c)
        img = og.group(1) if og else ''
        out.append((slug, t, img))
    return out


def build_section(region):
    region = REGION_NAMES[region]
    items = []
    for slug, t, img in titles_for(region)[:N]:
        img_tag = (f'<div class="card-img-wrapper"><img class="card-img" '
                   f'src="{img}" alt="{t}" loading="lazy"></div>'
                   if img else '')
        items.append(
            f'      <a href="{SITE}/articles/{slug}.html" class="related-card">'
            f'{img_tag}'
            f'<div class="card-body"><span class="card-title">{t}</span></div></a>')
    return (
        '\n<div class="related-section">\n  <h2>相關旅遊攻略</h2>\n'
        '  <div class="related-grid">\n' + '\n'.join(items) + '\n  </div>\n</div>\n')


def add_jsonld_related(region):
    """Breadcrumbs + 集群結構化數據"""
    slug = f'{region}-esim-guide'
    region = REGION_NAMES[region]
    return (
        f'  <script type="application/ld+json">\n'
        f'  {{\n    "@context": "https://schema.org",\n    "@type": "BreadcrumbList",\n'
        f'    "itemListElement": [\n'
        f'      {{"@type": "ListItem", "position": 1, "name": "首頁", "item": "{SITE}/"}},\n'
        f'      {{"@type": "ListItem", "position": 2, "name": "{region}", "item": "{SITE}/guides/{slug}.html"}}\n'
        f'    ]\n  }}\n  </script>\n')


processed = []
for region in ['jp', 'kr', 'tw', 'eu', 'oce']:
    f = f'guides/{region}-esim-guide.html'
    if not os.path.exists(f):
        print(f'  skip {f} (not found)')
        continue
    c = open(f, encoding='utf-8').read()
    if '相關旅遊攻略' in c:
        print(f'  skip {f} (already has section)')
        continue
    sec = build_section(region)
    jld = add_jsonld_related(region)
    # 插入 JSON-LD 到 </head> 前
    if '<script type="application/ld+json">' in c and 'BreadcrumbList' not in c:
        c = c.replace('</head>', jld + '</head>')
    # 插入 related 區塊到 </body> 前
    c = c.replace('</body>', sec + '</body>')
    open(f, 'w', encoding='utf-8').write(c)
    processed.append(f)

print(f'\nProcessed: {processed}')
