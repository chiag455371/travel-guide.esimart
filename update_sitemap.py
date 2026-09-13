# -*- coding: utf-8 -*-
import os, datetime

BASE = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"
ARTICLES = BASE + r"\articles"
TODAY = datetime.date.today().isoformat()

urls = []
urls.append(("https://chiag455371.github.io/travel-guide.esimart/", TODAY, "daily", "1.0"))
urls.append(("https://chiag455371.github.io/travel-guide.esimart/articles/", TODAY, "daily", "0.9"))
for region in ["jp", "kr", "tw", "eu", "oce"]:
    urls.append((f"https://chiag455371.github.io/travel-guide.esimart/articles/{region}.html", TODAY, "weekly", "0.8"))

for fn in sorted(os.listdir(ARTICLES)):
    if fn.endswith(".html") and fn != "index.html":
        slug = fn.replace(".html", "")
        if slug.startswith("jp"): p, cf = "0.7", "weekly"
        elif slug.startswith("kr"): p, cf = "0.7", "weekly"
        elif slug.startswith("tw"): p, cf = "0.7", "weekly"
        elif slug.startswith("eu"): p, cf = "0.6", "weekly"
        elif slug.startswith("oce"): p, cf = "0.6", "weekly"
        else: p, cf = "0.5", "weekly"
        urls.append((f"https://chiag455371.github.io/travel-guide.esimart/articles/{slug}.html", TODAY, cf, p))

xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, date, freq, prio in urls:
    xml_lines.append(f"  <url>")
    xml_lines.append(f"    <loc>{loc}</loc>")
    xml_lines.append(f"    <lastmod>{date}</lastmod>")
    xml_lines.append(f"    <changefreq>{freq}</changefreq>")
    xml_lines.append(f"    <priority>{prio}</priority>")
    xml_lines.append("  </url>")
xml_lines.append("</urlset>")

with open(BASE + r"\sitemap.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml_lines))
print(f"Sitemap generated: {len(urls)} URLs")
