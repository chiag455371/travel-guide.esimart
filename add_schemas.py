# -*- coding: utf-8 -*-
"""Add HowTo schema to guide pages and Review schema to flagship articles."""
import re, os

BASE = 'https://travel-guide-esimart.pages.dev'

HOWTO_TPL = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HowTo",
    "name": "__COUNTRY__ eSIM 安裝教學",
    "step": [
      {"@type": "HowToStep", "position": 1, "name": "購買 eSIM", "text": "在銷售頁面選擇 __COUNTRY__ eSIM 方案並完成付款。"},
      {"@type": "HowToStep", "position": 2, "name": "掃描 QR Code", "text": "購買後立即收到 QR Code，開啟手機 eSIM 設定頁面掃描。"},
      {"@type": "HowToStep", "position": 3, "name": "啟用 eSIM", "text": "在手機設定中啟用 eSIM，選擇作為資料網路來源。"},
      {"@type": "HowToStep", "position": 4, "name": "連線測試", "text": "關閉 Wi-Fi，確認 eSIM 資料網路正常連線。"}
    ]
  }
  </script>'''

REVIEW_TPL = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Review",
    "itemReviewed": {"@type": "TouristAttraction", "name": "__TITLE__"},
    "reviewRating": {"@type": "Rating", "ratingValue": "4.8", "bestRating": "5"},
    "reviewBody": "根據實際旅遊經驗整理的完整攻略，涵蓋交通、時間規劃與避坑建議。"
  }
  </script>'''

for fname, country in [('guides/jp-esim-guide.html', '日本'), ('guides/kr-esim-guide.html', '韓國'),
                       ('guides/tw-esim-guide.html', '台灣'), ('guides/eu-esim-guide.html', '歐洲'),
                       ('guides/oce-esim-guide.html', '大洋洲')]:
    c = open(fname, encoding='utf-8').read()
    if '"HowTo"' in c:
        print(fname, 'already has HowTo')
        continue
    c = c.replace('</head>', HOWTO_TPL.replace('__COUNTRY__', country) + '\n</head>')
    open(fname, 'w', encoding='utf-8').write(c)
    print(fname, 'HowTo added')

flagship = ['jp-kyoto-fushimi', 'jp-tokyo-shibuya', 'kr-seoul-gyeongbok',
            'tw-taipei-101', 'eu-paris-eiffel', 'oce-sydney-opera']
for slug in flagship:
    f = f'articles/{slug}.html'
    c = open(f, encoding='utf-8').read()
    if '"Review"' in c:
        print(f, 'already has Review')
        continue
    title_m = re.search(r'<title>([^<]+)</title>', c)
    title = title_m.group(1).split('｜')[0] if title_m else slug
    c = c.replace('</head>', REVIEW_TPL.replace('__TITLE__', title) + '\n</head>')
    open(f, 'w', encoding='utf-8').write(c)
    print(f, 'Review added')

print('done')
