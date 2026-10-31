# -*- coding: utf-8 -*-
"""產生 sitemap.xml。

規則（2026-10-31 由營運接管後改寫）：
- 唯一正式網域 = https://travel-guide-esimart.pages.dev
- 收錄 index、地區頁、guides/、articles/ 全部頁面
- lastmod 用檔案實際修改時間，不用固定日期（Google 才看得出內容有更新）
"""
import os
import datetime

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

# 2) 地區總覽頁（根目錄的 jp.html / kr.html ...）
for region in ["jp", "kr", "tw", "eu", "oce"]:
    f = os.path.join(BASE, region + ".html")
    if os.path.exists(f):
        urls.append((f"{SITE}/{region}.html", mtime(f), "daily", "0.9"))

# 3) 文章目錄頁
if os.path.exists(os.path.join(ARTICLES, "index.html")):
    urls.append((f"{SITE}/articles/", mtime(os.path.join(ARTICLES, "index.html")), "daily", "0.9"))

# 4) guides/
if os.path.isdir(GUIDES):
    for fn in sorted(os.listdir(GUIDES)):
        if fn.endswith(".html") and fn not in SKIP:
            urls.append((f"{SITE}/guides/{fn}", mtime(os.path.join(GUIDES, fn)), "weekly", "0.8"))

# 5) jp/ 子站
JP = os.path.join(BASE, "jp")
if os.path.isdir(JP):
    for fn in sorted(os.listdir(JP)):
        if fn.endswith(".html"):
            urls.append((f"{SITE}/jp/{fn}", mtime(os.path.join(JP, fn)), "weekly", "0.7"))

# 6) articles/ 全部文章
if os.path.isdir(ARTICLES):
    for fn in sorted(os.listdir(ARTICLES)):
        if not fn.endswith(".html") or fn in SKIP:
            continue
        slug = fn[:-5]
        if slug[:2] in ("jp", "kr", "tw"):
            p, cf = "0.7", "weekly"
        elif slug[:3] == "oce" or slug[:2] == "eu":
            p, cf = "0.6", "weekly"
        else:
            p, cf = "0.5", "weekly"
        urls.append((f"{SITE}/articles/{fn}", mtime(os.path.join(ARTICLES, fn)), cf, p))

# 去重（保留第一筆）
seen = set()
uniq = []
for u in urls:
    if u[0] in seen:
        continue
    seen.add(u[0])
    uniq.append(u)

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
