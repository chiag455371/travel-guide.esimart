# -*- coding: utf-8 -*-
"""Generate 5 country eSIM purchase guide pages with FAQ Schema and CTA."""
import os, json, re, glob

BASE = 'https://travel-guide-esimart.pages.dev'
GUIDES_DIR = 'guides'
os.makedirs(GUIDES_DIR, exist_ok=True)

# (filename, country_name, flag, eSIM tips, popular articles)
GUIDES = [
    ('jp-esim-guide.html', '日本', '🇯🇵',
     [
         ('日本 eSIM 選擇建議', '日本主要電信商 NTT docomo、KDDI (au) 與 SoftBank 均覆蓋 5G，eSIM 覆蓋率高。東京、大阪、京都等大城市訊號穩定， rural 地區建議選擇提供 4G 備用的方案。'),
         ('安裝時機', '建議在登機前 24 小時完成 eSIM 安裝，避免落地後找不到 Wi-Fi 或訊號不穩。日本多數機場可透過行李托運前 Wi-Fi 完成設定。'),
         ('常見問題', '部分舊款 iPhone (iPhone 6s 以下) 不支援 eSIM；建議使用 iPhone XS 或更新機型，或 Android 10 以上支援 eSIM 的機型。'),
     ],
     ['jp-tokyo-shibuya', 'jp-kyoto-arashiyama', 'jp-osaka-dotonbori', 'jp-hakone-onsen']),
    ('kr-esim-guide.html', '韓國', '🇰🇷',
     [
         ('韓國 eSIM 選擇建議', '韓國主要電信商 SK Telecom、KT、LG U+ 均提供 eSIM 服務，覆蓋 Seoul 全境與各大型城市。5G 覆蓋廣泛，eSIM 方案價格實惠。'),
         ('安裝時機', '建議在出发前完成安裝，落地後即可使用。Incheon 機場與 Gimhae 機場均有公共 Wi-Fi 可用。'),
         ('常見問題', ' Samsung 早期機型部分不支援 eSIM，請確認支援列表後再購買。'),
     ],
     ['kr-seoul-gyeongbok', 'kr-jeju', 'kr-busan', 'kr-seoul-mydong']),
    ('tw-esim-guide.html', '台灣', '🇹🇼',
     [
         ('台灣 eSIM 選擇建議', '台灣主要電信商中华電信、遠傳、台哥大均支援 eSIM，全境覆蓋率極高。短途遊建議 5 天 5GB 起跳，商務客可考慮 30 天無限量。'),
         ('安裝時機', '台北松山與桃園機場落地後即可啟用 eSIM，機場公共 Wi-Fi 穩定可用。'),
         ('常見問題', ' 大部分 eSIM 方案包含漫遊漫遊費，建議確認方案是否包含國際漫遊再選擇。'),
     ],
     ['tw-taipei-101', 'tw-yilan', 'tw-taitung-hot', 'tw-penghu']),
    ('eu-esim-guide.html', '歐洲', '🇪🇺',
     [
         ('歐洲 eSIM 選擇建議', '歐洲 27 國選擇多，建議選擇涵蓋所經國家數的多國方案，避免每次換國就要重裝。Deutsche Telekom、Vodafone、Orange 均提供全歐 eSIM。'),
         ('安裝時機', '建議在登機前安裝，落地後用機場 Wi-Fi 啟用。多數歐洲機場訊號覆蓋良好。'),
         ('常見問題', ' 部分方案有流量上限，超過後速度會降至 128kbps；建議每日监控用量避免中斷。'),
     ],
     ['eu-paris-eiffel', 'eu-rome-colosseum', 'eu-barcelona', 'eu-london', 'eu-venice-canals']),
    ('oce-esim-guide.html', '大洋洲', '🇦🇺',
     [
         ('大洋洲 eSIM 選擇建議', '澳洲 Telstra、Optus、Vodafone 覆蓋廣，New Zealand 由 Spark、Vodafone 主導。建議選擇含漫遊的太平洋多國方案，避免跨國時重新設定。'),
         ('安裝時機', '雪梨、墨爾本、奧克蘭機場均有公共 Wi-Fi，落地後即可啟用。'),
         ('常見問題', ' 澳洲部分偏遠地區 (如 Outback) 訊號薄弱，建議購買保險並確認方案是否含緊急通訊功能。'),
     ],
     ['oce-sydney-opera', 'oce-mel', 'oce-queenstown', 'oce-perth-kangaroo']),
]

def get_title(slug):
    try:
        c = open(f'articles/{slug}.html', encoding='utf-8').read()
        m = re.search(r'<title>([^<]+)</title>', c)
        return (m.group(1) if m else slug).split('｜')[0].strip()
    except FileNotFoundError:
        return slug

def get_seed(slug):
    try:
        c = open(f'articles/{slug}.html', encoding='utf-8').read()
        m = re.search(r'og:image" content="https://picsum\.photos/seed/(\d+)/', c)
        return m.group(1) if m else None
    except FileNotFoundError:
        return None

FAQ_SCHEMA = {
    "faqs": [
        {"question": "eSIM 需要換 SIM 卡嗎？", "answer": "不需要。eSIM 直接嵌入手機內建晶片，透過 QR Code 掃描即可啟用，不用拆機、不用換實體卡。"},
        {"question": "eSIM 可以和其他 SIM 卡同時使用嗎？", "answer": "大部分 iPhone XS 以上機型可同時啟用 eSIM + 實體 SIM 雙卡；Android 多數機型也可同時使用，視機型支援情況而定。"},
        {"question": "購買後多久可以啟用？", "answer": "購買完成後立即收到 QR Code，隨時可啟用。建議至少提前 24 小時安裝，避免落地後無網可用。"},
        {"question": "流量用完了怎麼辦？", "answer": "大部分方案可加購流量包，不用重新安裝 eSIM；加購後自動生效。"},
    ]
}

def faq_html(faqs):
    out = ['<div class="faq-section"><h2>常見問題</h2><div class="faq-list">']
    for q, a in faqs:
        out.append(f'  <details><summary>{q}</summary><p>{a}</p></details>')
    out.append('</div></div>')
    return '\n'.join(out)

def popular_html(article_slugs):
    items = []
    for slug in article_slugs:
        title = get_title(slug)
        seed = get_seed(slug) or '100000'
        items.append(
            f'    <a href="{BASE}/articles/{slug}.html" class="popular-item">'
            f'<img class="popular-img" src="https://picsum.photos/seed/{seed}/80/80" '
            f'alt="{title}" loading="lazy" width="80" height="80">'
            f'<span class="popular-title">{title}</span></a>')
    return '\n'.join(items)

template = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>__COUNTRY__ eSIM 完整購買指南｜__GUIDE_TITLE__</title>
  <meta name="description" content="__DESC__">
  <meta property="og:title" content="__COUNTRY__ eSIM 購買指南">
  <meta property="og:description" content="__DESC__">
  <meta property="og:url" content="__GUIDE_URL__">
  <meta property="og:type" content="article">
  <meta property="og:image" content="__OG_IMG__">
  <link rel="canonical" href="__GUIDE_URL__">
  <link rel="stylesheet" href="__BASE__/assets/style.css">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {"@type": "Question", "name": "eSIM 需要換 SIM 卡嗎？",
       "acceptedAnswer": {"@type": "Answer", "text": "不需要。eSIM 直接嵌入手機內建晶片，透過 QR Code 掃描即可啟用，不用拆機、不用換實體卡。"}},
      {"@type": "Question", "name": "eSIM 可以和其他 SIM 卡同時使用嗎？",
       "acceptedAnswer": {"@type": "Answer", "text": "大部分 iPhone XS 以上機型可同時啟用 eSIM + 實體 SIM 雙卡；Android 多數機型也可同時使用，視機型支援情況而定。"}},
      {"@type": "Question", "name": "購買後多久可以啟用？",
       "acceptedAnswer": {"@type": "Answer", "text": "購買完成後立即收到 QR Code，隨時可啟用。建議至少提前 24 小時安裝，避免落地後無網可用。"}},
      {"@type": "Question", "name": "流量用完了怎麼辦？",
       "acceptedAnswer": {"@type": "Answer", "text": "大部分方案可加購流量包，不用重新安裝 eSIM；加購後自動生效。"}}
    ]
  }
  </script>
</head>
<body>
  <nav class="site-header">
    <a href="__BASE__/" class="site-logo">旅遊通 eSIM</a>
    <div class="header-links">
      <a href="__BASE__/articles/">全部攻略</a>
      <a href="__BASE__/guides/jp-esim-guide.html">🇯🇵 日本</a>
      <a href="__BASE__/guides/kr-esim-guide.html">🇰🇷 韓國</a>
      <a href="__BASE__/guides/tw-esim-guide.html">🇹🇼 台灣</a>
      <a href="__BASE__/guides/eu-esim-guide.html">🇪🇺 歐洲</a>
      <a href="__BASE__/guides/oce-esim-guide.html">🇦🇺 大洋洲</a>
    </div>
  </nav>

  <nav aria-label="breadcrumb" class="breadcrumb-nav">
    <ol class="breadcrumb">
      <li><a href="__BASE__/">首頁</a></li>
      <li><a href="__BASE__/articles/__REGION__-esim-guide.html">eSIM 購買指南</a></li>
      <li aria-current="page">__COUNTRY__ eSIM 指南</li>
    </ol>
  </nav>

  <main class="container guide-page">
    <h1>__COUNTRY_FLAG__ __COUNTRY__ eSIM 購買指南</h1>
    <p class="guide-lead">出發前怎麼買、怎麼裝、怎麼用？__GUIDE_TITLE__ 幫你一次講清楚，落地即有訊號。</p>

    <div class="tips-grid">
__TIPS__
    </div>

    <div class="cta-banner">
      <h2>準備好了？立即購買 __COUNTRY__ eSIM</h2>
      <p>選擇方案、掃描 QR Code，3 分鐘完成安裝，落地即有網路。</p>
      <a class="btn" href="https://travel-guide.esimart.cc/goods" target="_blank" rel="noopener">➜ 前往購買 __COUNTRY__ eSIM</a>
    </div>

    <h2>__COUNTRY__ 必訪攻略推薦</h2>
    <div class="popular-grid">
__POPULAR__
    </div>

    __FAQ_HTML__

    <div class="related-section" style="margin-top:2rem">
      <h2>其他國家 eSIM 指南</h2>
      <div class="related-grid">
__OTHER_GUIDES__
      </div>
    </div>
  </main>

  <footer style="padding:1.5rem;text-align:center;font-size:.8rem;opacity:.6">
    © 旅遊通 eSIM｜__COUNTRY__ 旅遊網路攻略
  </footer>
</body>
</html>
"""

OTHER_GUIDES = []
for fname, country, flag, tips, arts in GUIDES:
    OTHER_GUIDES.append(
        f'        <a href="{BASE}/guides/{fname}" class="related-card">'
        f'<span class="card-title">{flag} {country} eSIM 指南</span></a>')

for fname, country, flag, tips, arts in GUIDES:
    guide_title = f'{country} eSIM 攻略與購買指南'
    desc = f'{country} eSIM 怎麼買？涵蓋選擇建議、安裝步驟、常見問題，並推薦{country}必訪景點，落地即有網路。'
    og_seed = get_seed(arts[0]) if arts else '100000'
    region = fname.split('-')[0]
    tips_html = '\n'.join(
        f'      <div class="tip-card"><h3>{h}</h3><p>{b}</p></div>' for h, b in tips)
    c = (template
         .replace('__COUNTRY__', country)
         .replace('__COUNTRY_FLAG__', flag)
         .replace('__GUIDE_TITLE__', guide_title)
         .replace('__DESC__', desc)
         .replace('__GUIDE_URL__', f'{BASE}/guides/{fname}')
         .replace('__OG_IMG__', f'https://picsum.photos/seed/{og_seed}/600/400')
         .replace('__BASE__', BASE)
         .replace('__REGION__', region)
         .replace('__TIPS__', tips_html)
         .replace('__POPULAR__', popular_html(arts))
         .replace('__FAQ_HTML__', faq_html(FAQ_SCHEMA['faqs']))
         .replace('__OTHER_GUIDES__', '\n'.join(OTHER_GUIDES)))
    open(os.path.join(GUIDES_DIR, fname), 'w', encoding='utf-8').write(c)
    print(fname, 'created')

# Add purchase guide link to region pages
for region in ['jp', 'kr', 'tw', 'eu', 'oce']:
    fname = f'articles/{region}.html'
    c = open(fname, encoding='utf-8').read()
    if 'guides/' in c:
        print(region, 'already has guide link')
        continue
    m = re.search(r'(<h1[^>]*>[^<]+</h1>)', c)
    link = (f'\n<a href="{BASE}/guides/{region}-esim-guide.html" '
            f'class="guide-cta" style="display:inline-block;margin:0.5rem 0;padding:0.5rem 1rem;'
            f'background:#e63946;color:#fff;border-radius:8px;text-decoration:none;font-weight:700">'
            f'📶 {region.upper()} eSIM 購買指南 →</a>')
    if m:
        pos = m.end()
        c = c[:pos] + link + c[pos:]
    open(fname, 'w', encoding='utf-8').write(c)
    print(region, 'guide link added')

print('done')
