#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把區域頁（articles/jp.html 等）漏掉的核心文章補進去。

問題：articles/jp.html 只列 87 篇，但日本核心頁有 105 篇；
      整站 528 篇裡有 213 篇完全沒有任何站內連結（孤兒頁），
      Google 只能從 sitemap 發現它們 → 發現率與評分都差。
做法：沿用區域頁原本的卡片樣式，只把缺的卡片補進 card-grid 尾端。
"""
import os
import re
import html

from tier_content import build_plan, redirect_sources

ARTICLES_DIR = 'articles'
BASE = 'https://travel-guide-esimart.pages.dev'
REGIONS = ('jp', 'kr', 'tw', 'eu', 'oce')

CARD_RE = re.compile(r'href="[^"]*/articles/([A-Za-z0-9%._~\-]+)"\s+class="article-card"')


def strip_redirect_cards(src, slugs):
    """移除指向 301 來源的卡片，避免使用者多跳一次轉址。"""
    removed = 0
    for s in slugs:
        pat = re.compile(
            r'\s*<a href="[^"]*/articles/' + re.escape(s) + r'" class="article-card">.*?</a>',
            re.S,
        )
        src, n = pat.subn('', src)
        removed += n
    return src, removed


def read_article(slug):
    content = open(os.path.join(ARTICLES_DIR, slug + '.html'), encoding='utf-8').read()
    m = re.search(r'<title>(.*?)</title>', content)
    title_raw = m.group(1).strip() if m else slug
    title = re.sub(r'\s*[｜|]\s*.*$', '', title_raw).strip() or title_raw
    m2 = re.search(r'<meta name="description" content="(.*?)">', content)
    desc = m2.group(1) if m2 else title
    m3 = re.search(r'<img[^>]+src="(https://[^"]+)"', content)
    return {'slug': slug, 'title': title, 'desc': desc, 'img': m3.group(1) if m3 else ''}


def card_html(a):
    t = html.escape(a['title'])
    d = html.escape(a['desc'][:100] + ('...' if len(a['desc']) > 100 else ''))
    img = a['img']
    url = f'{BASE}/articles/{a["slug"]}'
    img_tag = f'<div class="card-img-wrapper"><img class="card-img" src="{img}" alt="{t}" loading="lazy"></div>' if img else ''
    return f'''      <a href="{url}" class="article-card">
        {img_tag}
        <div class="card-body">
          <span class="card-title">{t}</span>
          <span class="card-desc">{d}</span>
          <div class="card-meta"><span class="card-meta-dot"></span><span>約 8 分鐘閱讀</span></div>
        </div>
      </a>'''


def main():
    plan = build_plan()
    core = plan['core']
    redir = redirect_sources()
    by_region = {r: [] for r in REGIONS}
    for s in core:
        for r in REGIONS:
            if s.startswith(r + '-'):
                by_region[r].append(s)
                break

    for r in REGIONS:
        path = os.path.join(ARTICLES_DIR, r + '.html')
        if not os.path.exists(path):
            print(f'[skip] {path} 不存在')
            continue
        src = open(path, encoding='utf-8').read()

        src, dropped = strip_redirect_cards(src, redir)
        if dropped:
            print(f'{r}: 移除 {dropped} 張指向轉址頁的卡片')

        have = set(CARD_RE.findall(src))
        missing = [s for s in by_region[r] if s not in have]

        if not missing:
            if dropped:
                open(path, 'w', encoding='utf-8').write(src)
            print(f'{r}: 已完整（{len(have)} 篇）')
            continue

        cards = '\n'.join(card_html(read_article(s)) for s in missing)

        anchor = 'class="card-grid">'
        pos = src.find(anchor)
        if pos < 0:
            print(f'[skip] {r}: 找不到 card-grid')
            continue
        insert_at = pos + len(anchor)
        new = src[:insert_at] + '\n' + cards + src[insert_at:]

        # 同步更新「查看全部 N 篇」與 chip 上的篇數
        total = len(have) + len(missing)
        new = re.sub(r'(查看全部\s*)\d+(\s*篇)', lambda m: f'{m.group(1)}{total}{m.group(2)}', new)

        open(path, 'w', encoding='utf-8').write(new)
        print(f'{r}: 補 {len(missing)} 篇 → 共 {total} 篇')


if __name__ == '__main__':
    main()
