#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_esim_pages.py — 產生 eSIM 高意圖專題頁（轉換入口）
目標：填補旅遊站「eSIM 購買/推薦」高意圖頁的空缺，每篇內文都帶情境化 CTA 指向
      https://travel-guide.esimart.cc/goods（本站自有金流，TapPay 收款）。

用法：python gen_esim_pages.py
產出：articles/esim-*.html（由部署流程接手 canonical / sticky CTA / sitemap / index）
"""
import os, json, datetime

ART = "articles"
SITE = "https://travel-guide-esimart.pages.dev"
GOODS = "https://travel-guide.esimart.cc/goods"
TODAY = datetime.date.today().isoformat()

CTA_BOX = f'''
<div class="cta-box" style="margin:1.8rem 0;padding:1.3rem 1.5rem;background:#111827;color:#fff;border-radius:14px">
  <h3 style="margin:0 0 .5rem;color:#fff">📶 立刻選購 eSIM 上網方案</h3>
  <p style="margin:0 0 .9rem;color:#cbd5e1">旅遊通 eSIM 支援日本、韓國、泰國、歐洲等多地，線上刷卡秒開通，到機場就能用。</p>
  <a class="cta" href="{GOODS}" target="_blank" rel="sponsored noopener" style="display:inline-block;background:#f59e0b;color:#111;font-weight:700;padding:.7rem 1.4rem;border-radius:9px;text-decoration:none">前往選購 eSIM 方案 →</a>
</div>
'''

def page(slug, title, desc, keywords, body_inner):
    head = f'''<!doctype html>
<html lang="zh-Hant">
<head>
  <link rel="stylesheet" href="/assets/style.css">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{keywords}">
  <meta name="author" content="旅遊通 eSIM 編輯團隊">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{SITE}/articles/{slug}">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="zh_TW">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{SITE}/articles/{slug}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="date_published" content="{TODAY}">
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":{json.dumps(title)},"description":{json.dumps(desc)},"datePublished":"{TODAY}","dateModified":"{TODAY}","author":{{"@type":"Organization","name":"旅遊通 eSIM"}},"publisher":{{"@type":"Organization","name":"旅遊通 eSIM","url":"{SITE}"}},"mainEntityOfPage":{{"@type":"WebPage","@id":"{SITE}/articles/{slug}"}}}}</script>
</head>
<body>
<nav class="topnav">
  <a class="brand" href="{SITE}/"><em>旅遊通</em> eSIM</a>
  <button class="menu-toggle" onclick="document.querySelector('.nav-links').classList.toggle('active')">&#9776;</button>
  <div class="nav-links">
    <a href="{SITE}/">首頁</a>
    <a href="{SITE}/articles/">全部攻略</a>
    <a href="{GOODS}" target="_blank" rel="sponsored noopener">選購 eSIM</a>
  </div>
</nav>
<main class="post">
<article>
  <header class="post-header">
    <h1>{title}</h1>
    <p class="post-meta">最後更新：{TODAY} ｜ 旅遊通 eSIM 編輯團隊</p>
  </header>
{body_inner}
{CTA_BOX}
</article>
</main>
</body></html>'''

    path = os.path.join(ART, slug + ".html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(head)
    print("written", path)

PAGES = {}

PAGES["esim-what-is"] = dict(
    title="eSIM 是什麼？一篇搞懂：原理、優缺點、適合誰",
    desc="eSIM 是內嵌式 SIM 卡，免實體卡即可上網。本文說明 eSIM 原理、與實體 SIM/漫遊的差異、啟用方式與常見疑問。",
    keywords="eSIM是什麼,eSIM原理,eSIM優缺點,eSIM教學,嵌入式SIM",
    body='''<p>eSIM（Embedded SIM，嵌入式 SIM 卡）是一種直接焊在手機主機板上的虛擬 SIM 晶片，不需要插拔實體卡片，只要掃描 QR Code 或透過 App 下載設定檔，就能啟用電信方案上網與通話。</p>
<h2>eSIM 怎麼運作？</h2>
<p>傳統 SIM 卡把門號資訊存在實體晶片；eSIM 則把這份資訊存在手機內的 eUICC 晶片，由電信商以「遠端配置」方式寫入。一台支援 eSIM 的手機通常可存放多組設定檔，出行前先買好目的地的 eSIM 方案，落地即開通。</p>
<h2>eSIM 的優點</h2>
<ul>
<li><strong>免換卡、免寄送：</strong>線上購買後幾分鐘內收到 QR Code，掃描即啟用，適合臨時決定出國的人。</li>
<li><strong>雙卡雙待：</strong>多數 eSIM 手機可同時保留原門號（實體 SIM 收簡訊/來電）＋ eSIM 上網，不怕收不到銀行簡訊。</li>
<li><strong>價格透明：</strong>事先看清楚流量與天數，避免漫遊帳單驚喜。</li>
</ul>
<h2>eSIM 的缺點與限制</h2>
<ul>
<li>舊款手機可能不支援（iPhone XS 以後、近幾年 Android 多數支援）。</li>
<li>部分方案為「單次使用」，用完或到期後設定檔會失效，無法儲值延長。</li>
<li>少數國家電信會綁定設備，更換手機需重新申請。</li>
</ul>
<h2>eSIM 適合誰？</h2>
<p>自由行旅客、短期出差、留學交換、以及想在保留原門號同時省漫遊費的人，都是 eSIM 的最佳使用者。下一步可參考各國推薦方案，或直接到選購頁挑目的地。</p>''',
)

PAGES["esim-japan"] = dict(
    title="日本 eSIM 推薦與購買指南 2026：流量、天數、價格怎麼選",
    desc="去日本自由行該買哪種 eSIM？本文比較日本 eSIM 的流量方案、有效期、開通方式，並附購買步驟與實用提醒。",
    keywords="日本eSIM,日本上網卡,日本eSIM推薦,日本旅遊上網,東京上網",
    body='''<p>日本是中華圈旅客最愛的行程之一，選對 eSIM 能讓你 Google 地圖導航、查券、傳照片都不卡。以下針對日本常見需求給建議。</p>
<h2>日本 eSIM 怎麼挑？</h2>
<ul>
<li><strong>城市觀光（東京/大阪 5–7 天）：</strong>3–5GB 足夠日常導航與社群，若常看影片建議 10GB。</li>
<li><strong>深度旅遊（10–14 天）：</strong>10–20GB 或「不限流量（公平使用）」方案較安心。</li>
<li><strong>多人共享：</strong>eSIM 綁裝置，無法熱點共享給同行者太久，多人建議各自購買或加買一張。</li>
</ul>
<h2>開通前檢查清單</h2>
<ul>
<li>確認手機支援 eSIM 且已解鎖（無鎖機）。</li>
<li>出發前先買、先掃 QR，但<strong>抵達日本連上當地網路後再點「啟用」</strong>，避免提早計時。</li>
<li>保留 QR Code 截圖，萬一重設可再掃。</li>
</ul>
<h2>在日本常用的上網情境</h2>
<p>Google Maps 離線導航、Tabelog/Google 評論找餐廳、Suica 綁 Apple Wallet 搭車、翻譯 App 點餐——這些都吃流量但不大，3GB 以上都夠。若你要每天直播或大量上傳雲端，直接選 10GB 起。</p>
<h2>購買步驟</h2>
<p>線上選目的地「日本」→ 選流量與天數 → 刷卡（支援信用卡）→ 收到 QR Code → 到日本啟用。旅遊通的日本 eSIM 支援主流方案，可到選購頁直接挑。</p>''',
)

PAGES["esim-korea"] = dict(
    title="韓國 eSIM 推薦 2026：首爾釜山自由行上網方案怎麼買",
    desc="韓國 eSIM 推薦與購買教學：涵蓋首爾、釜山行程的流量建議、開通方式與常見問題，出國前一次看懂。",
    keywords="韓國eSIM,韓國上網卡,首爾eSIM,釜山上網,韓國旅遊上網",
    body='''<p>韓國網速快、咖啡廳與地鐵幾乎全覆蓋，eSIM 讓你一下飛機就能用 Naver Map、Kakao Map 找路、叫外送。</p>
<h2>韓國上網需求特點</h2>
<ul>
<li>韓國主要用 <strong>Naver Map / Kakao Map</strong> 而非 Google Maps（Google 在韓國地形資料受限），兩者都吃流量。</li>
<li>地鐵站內也有網路，但轉乘大站人多時會慢，建議下載離線地圖備用。</li>
<li>追星、看直播需求高，10GB 以上更順。</li>
</ul>
<h2>怎麼選方案</h2>
<ul>
<li>3–5 天首爾市區：3–5GB。</li>
<li>7–10 天含釜山/濟州：10GB 或無限流量（公平使用）。</li>
</ul>
<h2>開通提醒</h2>
<p>韓國部分 eSIM 需在抵達後連上當地網路再啟用；購買後保留 QR Code，並確認手機已解鎖。若要用 Kakao / Naver 帳號，記得原門號收簡訊，建議用 eSIM 上網＋實體 SIM 收簡訊的雙卡模式。</p>
<h2>購買</h2>
<p>到選購頁選「韓國」，挑合適流量與天數，線上刷卡後即收到 QR Code，落地啟用。</p>''',
)

PAGES["esim-thailand"] = dict(
    title="泰國 eSIM 推薦 2026：曼谷清邁普吉上網方案與購買教學",
    desc="泰國 eSIM 怎麼買最划算？本文整理曼谷、清邁、普吉行程的流量建議與開通步驟，附實用避雷提醒。",
    keywords="泰國eSIM,泰國上網卡,曼谷eSIM,普吉上網,泰國旅遊上網",
    body='''<p>泰國是東南亞自由行首選，eSIM 讓你在機場、夜市、小島都能即時查 Google 翻譯、抓 Grab 計程車。</p>
<h2>泰國上網情境</h2>
<ul>
<li>曼谷塞車嚴重，Grab 叫車必備，吃流量。</li>
<li>離島（普吉、蘇梅）部分海域訊號弱，選全國漫遊方案較穩。</li>
<li>夜市、商場 Wi-Fi 多但不一定安全，自備 eSIM 上網更安心。</li>
</ul>
<h2>方案選擇</h2>
<ul>
<li>城市 5–7 天：5–10GB。</li>
<li>海島 10 天以上：10–15GB 或無限流量（公平使用）。</li>
</ul>
<h2>避雷提醒</h2>
<ul>
<li>避免落地才在機場櫃檯買實體卡，價格常偏高；線上先買 eSIM 更便宜。</li>
<li>確認方案是否含通話；多數旅遊 eSIM 僅上網，要通話請選含語音方案或用 VoIP。</li>
</ul>
<h2>購買步驟</h2>
<p>選購頁選「泰國」→ 選流量/天數 → 刷卡 → 收 QR Code → 抵泰啟用。旅遊通泰國 eSIM 支援主要電信，落地即用。</p>''',
)

PAGES["esim-europe"] = dict(
    title="歐洲 eSIM 推薦 2026：多國通用方案、申根出差留學怎麼選",
    desc="去歐洲多國怎麼買 eSIM 最省？本文說明歐洲跨國 eSIM、區域方案與單國方案的差異，附購買與啟用建議。",
    keywords="歐洲eSIM,歐洲上網卡,申根eSIM,多國eSIM,歐洲旅遊上網",
    body='''<p>歐洲跨國移動頻繁，一張「區域型 eSIM」就能在法國、德國、義大利、西班牙等多國使用，省去每國買卡的麻煩。</p>
<h2>兩種方案</h2>
<ul>
<li><strong>歐洲區域方案：</strong>覆蓋 30+ 國，適合法國→義大利→瑞士這類多國行程，一次購買全程用。</li>
<li><strong>單國方案：</strong>只在單一國家長住（如倫敦、巴黎）可選當地方案，單價可能更低。</li>
</ul>
<h2>流量與天數</h2>
<ul>
<li>2–3 週多國：建議 10–20GB 或無限（公平使用）。</li>
<li>留學/長期：選可儲值延長的方案，或當地門號型 eSIM。</li>
</ul>
<h2>注意</h2>
<ul>
<li>英國已脫歐，部分「歐洲方案」不含英國，買前確認覆蓋國家清單。</li>
<li>跨國移動時，手機會自動選網，eSIM 設定檔無須更換。</li>
</ul>
<h2>購買</h2>
<p>選購頁選「歐洲」區域方案，挑流量與天數，線上刷卡後收 QR Code，首站落地啟用即可跨國使用。</p>''',
)

PAGES["esim-compare"] = dict(
    title="eSIM vs 漫遊 vs 租機：出國上網三種方式怎麼選最划算",
    desc="出國上網該用 eSIM、國際漫遊還是租 Wi-Fi 機？本文從價格、便利、網速三面向實測比較，幫你選對方案。",
    keywords="eSIM比較,國際漫遊,租wifi機,出國上網,上網方式比較",
    body='''<p>出國上網常見三種方式：eSIM、國際漫遊、租 Wi-Fi 機（Wi-Fi Egg）。以下比較。</p>
<h2>價格</h2>
<ul>
<li><strong>eSIM：</strong>通常最便宜，日本 5GB/7天約數百台幣起，線上買即享。</li>
<li><strong>國際漫遊：</strong>便利但貴，日租型常破百台幣/日，適合極短期或不想麻煩的人。</li>
<li><strong>租 Wi-Fi 機：</strong>按天計費＋押金，多人分攤才划算，但要多帶一台、每天充電。</li>
</ul>
<h2>便利度</h2>
<ul>
<li>eSIM：手機直接上網，不需取還機，雙卡還能收原門號簡訊。</li>
<li>漫遊：免設定最方便，但貴。</li>
<li>Wi-Fi 機：需領還、充電、且多人共享會搶頻寬。</li>
</ul>
<h2>網速與穩定</h2>
<p>三者實際網速都取決當地電信。eSIM 多接當地主流電信，速度與在地 SIM 相當；漫遊可能被限速；Wi-Fi 機則看機器與電信。</p>
<h2>結論</h2>
<p>多數自由行選 <strong>eSIM</strong> 最平衡：便宜、免取還、可雙卡。極短期或不想設定才考慮漫遊；多人且不在意多帶設備才租機。</p>''',
)

PAGES["esim-buy-guide"] = dict(
    title="eSIM 怎麼買、啟用與常見問題：從購買到上網一次搞懂",
    desc="eSIM 購買與啟用完整教學：支援手機清單、QR Code 掃描步驟、啟用時機、熱點分享與疑難排解。",
    keywords="eSIM購買,eSIM啟用,eSIM教學,eSIM常見問題,eSIM設定",
    body='''<p>第一次買 eSIM 最容易卡在「怎麼啟用」。以下 step by step。</p>
<h2>第一步：確認手機支援</h2>
<ul>
<li>iPhone：XS/XS Max/XR 以後多數支援（設定→一般→關於本機→有「可新增 eSIM」即支援）。</li>
<li>Android：近幾年旗艦多支援，設定→連線→SIM 卡管理確認。</li>
<li>手機需「解鎖（無鎖機）」才能用其他電信 eSIM。</li>
</ul>
<h2>第二步：購買</h2>
<p>到選購頁選目的地與方案 → 線上刷卡 → 立刻收到 QR Code（或 App 直裝）。</p>
<h2>第三步：啟用</h2>
<ol>
<li>手機連 Wi-Fi（啟用時需要網路）。</li>
<li>相機掃 QR，或設定→加入 eSIM／行動方案。</li>
<li><strong>抵達目的地、連上當地網路後再點「啟用/打開」</strong>，避免提早計時。</li>
</ol>
<h2>常見問題</h2>
<ul>
<li><strong>可以開熱點嗎？</strong>多數 eSIM 可熱點分享，但流量會共用，注意用量。</li>
<li><strong>啟用失敗？</strong>確認掃對 QR、網路穩定、設定檔未被佔滿（多數手機限存數組）。</li>
<li><strong>用完怎麼辦？</strong>單次方案到期失效；若要續用請買新方案或選可儲值型。</li>
</ul>
<h2>最後提醒</h2>
<p>出發前先買先掃、保留 QR 截圖、確認雙卡模式能收原門號簡訊。準備好就到選購頁挑方案吧。</p>''',
)

if __name__ == "__main__":
    os.makedirs(ART, exist_ok=True)
    for slug, d in PAGES.items():
        # 跳過已存在（避免覆寫手動調整）
        if os.path.exists(os.path.join(ART, slug + ".html")):
            print("skip exists", slug)
            continue
        page(slug, d["title"], d["desc"], d["keywords"], d["body"])
    print("done", len(PAGES), "pages")
