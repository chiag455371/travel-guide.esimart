# -*- coding: utf-8 -*-
"""
Daily article generator with image verification.
Generates 20+ travel guide articles per run, verifies images, updates sitemap & index.
"""
import os, random, datetime, re, html as html_mod
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

BASE = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"
ARTICLES_DIR = os.path.join(BASE, "articles")
DISTRIBUTOR = "https://travel-guide.esimart.cc/goods"
SITE_BASE = "https://travel-guide-esimart.pages.dev"
TODAY = datetime.date.today().isoformat()

# Image keywords per region
IMG_KEYWORDS = {
    "jp": ["japan", "tokyo", "kyoto", "osaka", "japanese temple", "sushi", "cherry blossom", " Mt fuji", "japanese street"],
    "kr": ["korea", "seoul", "korean food", "korean street", "korean temple", "korean castle"],
    "tw": ["taiwan", "taipei 101", "night market", "taiwanese food", "taiwan street", "taroko"],
    "eu": ["europe", "paris", "rome", "european cathedral", "european street", "european canal"],
    "oce": ["australia", "sydney", "new zealand", "australian beach", "outback", "kangaroo"],
}

REGIONS = {
    "jp": {"flag": "\U0001f1ef\U0001f1f5", "name": "日本", "keyword": "japan"},
    "kr": {"flag": "\U0001f1f0\U0001f1f7", "name": "韓國", "keyword": "korea"},
    "tw": {"flag": "\U0001f1f9\U0001f1fc", "name": "台灣", "keyword": "taiwan"},
    "eu": {"flag": "\U0001f1ea\U0001f1fa", "name": "歐洲", "keyword": "europe"},
    "oce": {"flag": "\U0001f1e6\U0001f1fa", "name": "澳洲", "keyword": "australia"},
}


def is_image_valid(url, timeout=8):
    """Check if a loremflickr image URL returns a valid response."""
    try:
        req = Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        resp = urlopen(req, timeout=timeout)
        return resp.status == 200
    except (URLError, HTTPError, OSError, ValueError):
        return False


def get_valid_image_url(region, lock_base):
    """Get a working loremflickr URL for the given region."""
    keywords = IMG_KEYWORDS.get(region, ["travel"])
    for kw in keywords:
        url = f"https://loremflickr.com/600/400/{kw.strip()}?lock={lock_base}&w=1200&h=600&fit=crop"
        if is_image_valid(url):
            return url
    # Fallback: just try the first keyword
    return f"https://loremflickr.com/600/400/{keywords[0]}?lock={lock_base}&w=1200&h=600&fit=crop"


def get_valid_hero_url(region, lock_base):
    """Get a working hero/large image URL."""
    keywords = IMG_KEYWORDS.get(region, ["travel"])
    for kw in keywords:
        url = f"https://loremflickr.com/1200/630/{kw.strip()}?lock={lock_base}&w=1920&h=1080&fit=crop"
        if is_image_valid(url):
            return url
    return f"https://loremflickr.com/1200/630/{keywords[0]}?lock={lock_base}&w=1920&h=1080&fit=crop"


def generate_article(template, existing_slugs):
    """Generate a single article HTML file."""
    region = REGIONS[template["region"]]
    slug = template["slug"]
    if slug in existing_slugs:
        return None

    lock = region.get("lock_base", 3001) + abs(hash(slug)) % 100
    card_img = get_valid_image_url(template["region"], lock)
    hero_img = get_valid_hero_url(template["region"], lock)

    h2_content = ""
    for title, content in template["h2s"]:
        h2_content += f"<h2>{title}</h2>\n<p>{content}</p>\n"

    tags_html = "".join(f'<span class="tag">{html_mod.escape(t)}</span>' for t in template["tags"])

    html = f'''<!doctype html>
<html lang="zh-Hant">
<head>
  <link rel="stylesheet" href="/travel-guide.esimart/assets/style.css">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html_mod.escape(template['title'])}｜{region['name']}旅遊攻略｜旅遊通 eSIM</title>
  <meta name="description" content="{html_mod.escape(template['desc'])}">
  <meta name="keywords" content="{', '.join(template['tags'])}, {region['name']}旅遊, {region['name']}攻略, {region['name']}eSIM">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{SITE_BASE}/articles/{slug}.html">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="zh_TW">
  <meta property="og:title" content="{html_mod.escape(template['title'])}｜{region['name']}旅遊攻略｜旅遊通 eSIM">
  <meta property="og:description" content="{html_mod.escape(template['desc'])}">
  <meta property="og:image" content="{hero_img}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:url" content="{SITE_BASE}/articles/{slug}.html">
  <meta property="og:site_name" content="旅遊通 eSIM">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html_mod.escape(template['title'])}｜{region['name']}旅遊攻略">
  <meta name="twitter:description" content="{html_mod.escape(template['desc'])}">
  <meta name="twitter:image" content="{hero_img}">
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{html_mod.escape(template['title'])}","description":"{html_mod.escape(template['desc'])}","image":"{hero_img}","datePublished":"{TODAY}","dateModified":"{TODAY}","author":{{"@type":"Organization","name":"旅遊通 eSIM"}},"publisher":{{"@type":"Organization","name":"旅遊通 eSIM","url":"{DISTRIBUTOR}"}}}}</script>
</head>
<body>
<nav class="topnav">
  <a class="brand" href="{SITE_BASE}/"><em>旅遊通</em> eSIM</a>
  <button class="menu-toggle" onclick="document.querySelector('.nav-links').classList.toggle('active')">&#9776;</button>
  <div class="nav-links">
    <a href="{SITE_BASE}/">首頁</a>
    <a href="{SITE_BASE}/articles/">全部攻略</a>
    <a href="{SITE_BASE}/articles/jp.html">{REGIONS['jp']['flag']} 日本</a>
    <a href="{SITE_BASE}/articles/kr.html">{REGIONS['kr']['flag']} 韓國</a>
    <a href="{SITE_BASE}/articles/tw.html">{REGIONS['tw']['flag']} 台灣</a>
    <a href="{SITE_BASE}/articles/eu.html">{REGIONS['eu']['flag']} 歐洲</a>
    <a href="{SITE_BASE}/articles/oce.html">{REGIONS['oce']['flag']} 澳洲</a>
    <a class="btn-nav" href="{DISTRIBUTOR}" target="_blank" rel="noopener">&#128722; eSIM 方案</a>
  </div>
</nav>

<div class="wrap">
  <div class="breadcrumb">
    <a href="{SITE_BASE}/">首頁</a> <span>&#8250;</span>
    <a href="{SITE_BASE}/articles/">全部攻略</a> <span>&#8250;</span>
    <a href="{SITE_BASE}/articles/{template['region']}.html">{region['flag']} {region['name']}</a> <span>&#8250;</span>
    <span>{html_mod.escape(template['title'])}</span>
  </div>

  <article class="article-page">
    <div class="article-header">
      <div class="article-tags">{tags_html}</div>
      <h1>{html_mod.escape(template['title'])}</h1>
      <div class="article-meta">
        <span>&#128197; {TODAY}</span>
        <span>&#128104; 旅遊通 eSIM 編輯團隊</span>
        <span>&#9201; {region['name']}</span>
      </div>
    </div>

    <div class="article-featured-img">
      <img src="{card_img}" alt="{html_mod.escape(template['title'])}" loading="lazy">
    </div>

    <div class="article-body">
      <p class="lead">{html_mod.escape(template['desc'])}</p>
      {h2_content}

      <div class="esim-cta-box">
        <h3>&#128241; 前往 {region['name']} 旅行，記得準備 eSIM！</h3>
        <p>到達 {region['name']} 後立即連上网，隨時分享你的旅遊點滴。旅遊通提供 {region['name']} 及全球 58 國 eSIM 方案，QR Code 掃描即可安裝，落地即連網。</p>
        <a class="btn-esim" href="{DISTRIBUTOR}" target="_blank" rel="noopener">查看 {region['name']} eSIM 方案 &#8594;</a>
      </div>

      <h2>常見問題</h2>
      <h3>如何安裝 eSIM？</h3>
      <p>購買後會收到 QR Code，在手機設定中掃描即可安裝。支援 iOS 12.1+ 和 Android 9.0+ 的 eSIM 裝置。</p>
      <h3>eSIM 可以與實體 SIM 並用嗎？</h3>
      <p>可以！大部分雙卡手機都支援 eSIM + 實體 SIM 同時使用，方便保留原號碼收簡訊。</p>
      <h3>網路速度如何？</h3>
      <p>旅遊通 eSIM 提供 4G/LTE 高速網路，速度依當地電信商而定，通常可支援影片串流和視訊通話。</p>
    </div>
  </article>

  <div class="article-nav">
    <a href="{SITE_BASE}/articles/{template['region']}.html" class="btn-back">&#8592; 返回 {region['name']} 攻略</a>
    <a href="{DISTRIBUTOR}" target="_blank" rel="noopener" class="btn-esim">查看 {region['name']} eSIM 方案 &#8594;</a>
  </div>
</div>

<footer class="site-footer">
  <div class="wrap">
    <p>&#169; 2024 旅遊通 eSIM ｜全球 58 國 eSIM 方案與旅遊攻略</p>
    <p><a href="{DISTRIBUTOR}" target="_blank" rel="noopener">查看所有 eSIM 方案</a></p>
  </div>
</footer>
</body>
</html>'''

    filepath = os.path.join(ARTICLES_DIR, slug + ".html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    return slug


def main():
    print("=" * 60)
    print("DAILY ARTICLE GENERATOR")
    print("=" * 60)
    print(f"Date: {TODAY}")

    # Load all templates
    print("\n[1] Loading templates...")
    from extra_templates import EXTRA_TEMPLATES as EXTRA_1
    from extra_templates_2 import EXTRA_TEMPLATES_2
    from extra_templates_3 import EXTRA_TEMPLATES_3
    from extra_templates_4 import EXTRA_TEMPLATES_4
    from extra_templates_5 import EXTRA_TEMPLATES_5
    from extra_templates_6 import EXTRA_TEMPLATES_6
    from extra_templates_7 import EXTRA_TEMPLATES_7
    from extra_templates_8 import EXTRA_TEMPLATES_8
    from extra_templates_9 import EXTRA_TEMPLATES_9

BASE_TEMPLATES = [
        {"slug": "jp-hiroshima-peace", "region": "jp", "title": "廣島和平紀念公園全攻略", "desc": "廣島是日本重要的和平教育基地。", "h2s": [("最佳參觀時間", "建議上午9點前抵達。"), ("必訪景點", "原爆圓頂館是1945年原子彈爆炸後殘留的建築。")], "tags": ["廣島", "和平紀念"]},
        {"slug": "jp-okinawa-beach", "region": "jp", "title": "沖繩海灘天堂全攻略", "desc": "沖繩是日本最著名的度假勝地。", "h2s": [("美之海水族館", "日本最大的水族館之一。"), ("萬座毛", "沖繩最著名的海岸景觀。")], "tags": ["沖繩", "海灘"]},
        {"slug": "kr-seoul-tower", "region": "kr", "title": "首爾N塔全攻略", "desc": "南山N塔是首爾的地標。", "h2s": [("觀景台", "118公尺高的觀景台。"), ("告白鎖", "情侶必訪的浪漫景點。")], "tags": ["首爾", "N塔"]},
        {"slug": "tw-kiang", "region": "tw", "title": "基隆廟口夜市全攻略", "desc": "基隆廟口是台灣最著名的夜市之一。", "h2s": [("美食推薦", "正生香菇筋麵線是必吃美食。"), ("營業時間", "晚上6點到凌晨2點。")], "tags": ["基隆", "廟口", "夜市"]},
        {"slug": "eu-paris-eiffel", "region": "eu", "title": "巴黎鐵塔全攻略", "desc": "艾菲爾鐵塔是巴黎最具代表性的地標。", "h2s": [("門票資訊", "成人票約18歐元。"), ("最佳觀賞時間", "日落後燈光點亮最美。")], "tags": ["巴黎", "艾菲爾鐵塔"]},
        {"slug": "oce-sydney-opera", "region": "oce", "title": "雪梨歌劇院全攻略", "desc": "雪梨歌劇院是世界著名建築。", "h2s": [("導覽資訊", "官方導覽約120分鐘。"), ("周邊景點", "皇家植物園和海港大橋相鄰。")], "tags": ["雪梨", "歌劇院"]},
    ]

    all_templates = BASE_TEMPLATES + EXTRA_1 + EXTRA_TEMPLATES_2 + EXTRA_TEMPLATES_3 + EXTRA_TEMPLATES_4 + EXTRA_TEMPLATES_5 + EXTRA_TEMPLATES_6 + EXTRA_TEMPLATES_7 + EXTRA_TEMPLATES_8 + EXTRA_TEMPLATES_9
    print(f"  Total templates: {len(all_templates)}")

    # Get existing slugs
    print("\n[2] Scanning existing articles...")
    existing = set()
    for f in os.listdir(ARTICLES_DIR):
        if f.endswith(".html"):
            existing.add(f.replace(".html", ""))
    print(f"  Existing articles: {len(existing)}")

    # Filter available templates
    available = [t for t in all_templates if t["slug"] not in existing]
    print(f"  Available templates: {len(available)}")

    if len(available) == 0:
        print("\nNo new templates available. Shutting down.")
        return

    # Generate up to 20 articles
    num_to_generate = min(20, len(available))
    selected = random.sample(available, num_to_generate)
    generated = []
    failed = 0

    print(f"\n[3] Generating {num_to_generate} articles...")
    for i, tmpl in enumerate(selected, 1):
        slug = generate_article(tmpl, existing)
        if slug:
            generated.append(slug)
            existing.add(slug)
        else:
            failed += 1
        if i % 5 == 0:
            print(f"  Generated {i}/{num_to_generate}...")

    print(f"\n  Generated: {len(generated)}, Failed: {failed}")

    # Update sitemap
    print("\n[4] Updating sitemap...")
    from update_sitemap import main as update_sitemap_main
    update_sitemap_main()

    # Update articles index
    print("\n[5] Updating articles index...")
    try:
        from build_index import main as build_index_main
        build_index_main()
    except Exception as e:
        print(f"  Note: build_index.py not found, skipping")

    # Update homepage
    print("\n[6] Updating homepage...")
    try:
        from build_homepage import main as build_homepage_main
        build_homepage_main()
    except Exception as e:
        print(f"  Note: build_homepage.py not found, using inline update")
        # Inline homepage update
        update_homepage_index(existing)

    print("\n" + "=" * 60)
    print(f"COMPLETE: {len(generated)} new articles, {len(existing)} total")
    print("=" * 60)


def update_homepage_index(existing_slugs):
    """Update index.html with latest article counts and previews."""
    import re
    content = open("index.html", encoding="utf-8").read()

    # Count per region
    counts = {"jp": 0, "kr": 0, "tw": 0, "eu": 0, "oce": 0}
    for slug in existing_slugs:
        for r in counts:
            if slug.startswith(r + "-"):
                counts[r] += 1

    # Fix quick-nav counts
    fixes = [
        ("日本", str(counts["jp"])),
        ("韓國", str(counts["kr"])),
        ("台灣", str(counts["tw"])),
        ("歐洲", str(counts["eu"])),
        ("澳洲", str(counts["oce"])),
    ]
    for name, count in fixes:
        content = re.sub(
            rf'(region-card-count">\s*{re.escape(name)}\s*)(\d+)\s*(篇攻略)',
            lambda m, c=count: m.group(1) + c + m.group(3),
            content
        )

    open("index.html", "w", encoding="utf-8").write(content)
    print("  Homepage updated")


if __name__ == "__main__":
    main()
