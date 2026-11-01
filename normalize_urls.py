# -*- coding: utf-8 -*-
"""normalize_urls.py — 把所有對外網址正規化成「無副檔名」。

Cloudflare Pages 會把 /x.html 308 轉到 /x，若 canonical / sitemap 仍寫 .html，
Google 會把該網址判為「已重新導向」而不收錄。本腳本在部署前統一修正。

執行：python normalize_urls.py
"""
import glob
import os
import re

SITE = "https://travel-guide-esimart.pages.dev"
ROOT = os.path.dirname(os.path.abspath(__file__))

# 絕對網址：SITE/xxx.html -> SITE/xxx（index.html -> 目錄）
ABS_RE = re.compile(re.escape(SITE) + r"/([A-Za-z0-9%._~\-/]*?)\.html(?=[\"'<>\s?#]|$)")
# 相對連結：href="xxx.html" / href="../xxx.html"
REL_RE = re.compile(r'(href=")((?:\.\./|\./)?[A-Za-z0-9%._~\-/]*?)\.html(?=["?#])')


def strip_abs(m):
    path = m.group(1)
    if path.endswith("/index") or path == "index":
        return SITE + "/" + path[: -len("index")]
    if path == "":
        return SITE + "/"
    return SITE + "/" + path


def strip_rel(m):
    prefix, path = m.group(1), m.group(2)
    if path.endswith("index") or path == "index":
        return prefix + path[: -len("index")]
    return prefix + path


def normalize(text: str) -> str:
    out = ABS_RE.sub(strip_abs, text)
    out = REL_RE.sub(strip_rel, out)
    # 收尾：避免出現 // 或目錄結尾缺斜線造成的雙斜線
    out = out.replace(SITE + "//", SITE + "/")
    return out


def main():
    files = []
    for pat in ("*.html", "articles/*.html", "pages/**/*.html", "guides/*.html", "jp/*.html"):
        files += glob.glob(os.path.join(ROOT, pat), recursive=True)
    changed = 0
    for p in sorted(set(files)):
        src = open(p, encoding="utf-8", errors="ignore").read()
        out = normalize(src)
        if out != src:
            open(p, "w", encoding="utf-8").write(out)
            changed += 1
    print(f"normalize_urls: {changed} / {len(set(files))} 檔已修正")


if __name__ == "__main__":
    main()
