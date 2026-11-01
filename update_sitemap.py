# -*- coding: utf-8 -*-
"""產生 sitemap.xml。

規則（2026-10-31 由營運接管後改寫，2026-10-31 二次修訂）：
- 唯一正式網域 = https://travel-guide-esimart.pages.dev
- 收錄：首頁、articles/ 目錄頁、5 個地區頁、**核心文章**
- **排除 noindex 頁面**：tier_content.py 判定為玩法變體／重複頁的文章
  會標成 noindex，這種頁面若還留在 sitemap，等於告訴 Google
  「我有一批不想被索引的網址」，會拉低整站信任度。
- **排除根目錄的 jp/kr/tw/eu/oce.html**：那 5 頁是 10KB 的空殼，
  內容重複 articles/{region}，已用 _redirects 301 導到正版頁。
- lastmod 用檔案實際修改時間，不用固定日期（Google 才看得出內容有更新）
"""
import os
import datetime
import re

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://travel-guide-esimart.pages.dev"
ARTICLES = os.path.join(BASE, "articles")
GUIDES = os.path.join(BASE, "guides")
TODAY = datetime.date.today().isoformat()

SKIP = {"404.html", "index.html", "_live_home.html", "template-product.html"}


def mtime(p):
    try:
        return datetime.date.fromtimestamp(os.path.getmtime(p)).isoformat()
    except OSError:
        return TODAY


def add(urls, loc, path, freq, prio):
    d = mtime(path) if path else TODAY
    urls.append((loc, max(d, TODAY) if d > TODAY else d, freq, prio))


urls = []

# 1) 首頁
urls.append((SITE + "/", mtime(os.path.join(BASE, "index.html")), "daily", "1.0"))

# 2) 文章目錄頁
if os.path.exists(os.path.join(ARTICLES, "index.html")):
    urls.append((f"{SITE}/articles/", mtime(os.path.join(ARTICLES, "index.html")), "daily", "0.9"))

# 3) 地區頁（articles/jp.html 這種，內容完整的版本）
for region in ["jp", "kr", "tw", "eu", "oce"]:
    f = os.path.join(ARTICLES, region + ".html")
    if os.path.exists(f):
        urls.append((f"{SITE}/articles/{region}", mtime(f), "daily", "0.8"))

# 4) guides/
if os.path.isdir(GUIDES):
    for fn in sorted(os.listdir(GUIDES)):
        if fn.endswith(".html") and fn not in SKIP:
            urls.append((f"{SITE}/guides/{fn}", mtime(os.path.join(GUIDES, fn)), "weekly", "0.7"))

# 5) articles/ 核心文章（排除 noindex）
NOINDEX_RE = re.compile(r'<meta\s+name="robots"\s+content="[^"]*noindex', re.I)
if os.path.isdir(ARTICLES):
    for fn in sorted(os.listdir(ARTICLES)):
        if not fn.endswith(".html") or fn in SKIP:
            continue
        path = os.path.join(ARTICLES, fn)
        head = open(path, encoding="utf-8", errors="ignore").read(4000)
        if NOINDEX_RE.search(head):
            continue
        slug = fn[:-5]
        if slug[:2] in ("jp", "kr", "tw"):
            p, cf = "0.7", "weekly"
        elif slug[:3] == "oce" or slug[:2] == "eu":
            p, cf = "0.6", "weekly"
        else:
            p, cf = "0.5", "weekly"
        urls.append((f"{SITE}/articles/{fn}", mtime(path), cf, p))

# 正規化：Cloudflare Pages 會把 /x.html 308 轉到 /x，
# sitemap 若仍寫 .html，Google 會判為「已重新導向」而不收錄。
def canon(loc):
    if loc.endswith("/index.html"):
        return loc[: -len("index.html")]
    if loc.endswith(".html"):
        return loc[: -len(".html")]
    return loc


seen = set()
uniq = []
for loc, date, freq, prio in urls:
    loc = canon(loc)
    if loc in seen:
        continue
    seen.add(loc)
    uniq.append((loc, date, freq, prio))

lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]
for loc, date, freq, prio in uniq:
    lines += [
        "  <url>",
        f"    <loc>{loc}</loc>",
        f"    <lastmod>{date}</lastmod>",
        f"    <changefreq>{freq}</changefreq>",
        f"    <priority>{prio}</priority>",
        "  </url>",
    ]
lines.append("</urlset>")

out = os.path.join(BASE, "sitemap.xml")
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Sitemap generated: {len(uniq)} URLs -> {out}")
