#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
內容分級（Content Tiering）— 解決 Google「已檢索但未建立索引」的核心手段。

背景：
  旅遊站 528 篇文章中，有 137 篇是「同一景點 × 玩法變體」
  （amalfi-budget / amalfi-food / amalfi-photo ...），
  跨景點相似度也高達 0.67。Google 對這類「大量低差異頁面」的處理
  就是掛著不索引，並拖累整站品質評分。

做法：
  core    = 每個景點只留 1 篇主頁（無後綴優先）→ 正常 index、進 sitemap
  variant = 其餘變體 → meta robots 改 noindex,follow（頁面仍活著、仍可導流，但不進索引）
  dup     = 同景點重複頁（nara-deer vs nara-deer-park 這種）→ noindex,follow

  noindex 是可逆的：日後把變體頁改寫成真正不同的內容，把 slug 從
  VARIANTS 移除、重跑本腳本即可恢復索引。

用法：
  python tier_content.py            # 套用分級
  python tier_content.py --report   # 只看統計，不改檔
  python tier_content.py --restore  # 全部恢復 index（緊急用）
"""
import os
import re
import sys
import json
import glob

ARTICLES = 'articles'
EXCLUDE = {'index.html', 'jp.html', 'kr.html', 'tw.html', 'eu.html', 'oce.html'}
STATE = os.path.join(ARTICLES, '_tier.json')

# 玩法變體後綴（長字串優先，避免 -day-trip 被切成 -trip）
SUFFIXES = (
    '-day-trip', '-one-day', '-2day', '-3day',
    '-budget', '-family', '-food', '-onsen', '-photo',
    '-shopping', '-night', '-guide', '-tips', '-couple',
    '-solo', '-rain', '-cheap', '-luxury', '-kids',
    '-route', '-map',
)

# 同景點重複頁 → 保留左邊，右邊 noindex
DUP_PAIRS = [
    ('jp-nara-deer-park', 'jp-nara-deer'),
    ('jp-osaka-dotonbori', 'jp-osaka-doton'),
    ('jp-nagoya-castle', 'jp-nagoyaCastle'),
    ('jp-himeji-castle', 'jp-himeji'),
    ('jp-miyajima-shrine', 'jp-miyajima-torii'),
    ('jp-hiroshima-itsukushima', 'jp-miyajima-torii'),
]

# 主頁優先序：越前面越優先當主頁
PRIORITY = ('-guide', '-day-trip', '-budget', '-food', '-family', '-onsen', '-photo')


def base_of(slug):
    """去掉玩法變體後綴，取得景點 base slug。"""
    changed = True
    while changed:
        changed = False
        for suf in SUFFIXES:
            if slug.endswith(suf) and len(slug) - len(suf) >= 6:
                slug = slug[: -len(suf)]
                changed = True
    return slug


def all_slugs():
    out = []
    for p in glob.glob(os.path.join(ARTICLES, '*.html')):
        name = os.path.basename(p)[:-5]
        if os.path.basename(p) in EXCLUDE:
            continue
        out.append(name)
    return sorted(out)


def pick_primary(slugs):
    """同一 base 的多個 slug 中，挑一篇當主頁。"""
    bare = [s for s in slugs if s == base_of(s)]
    if bare:
        return bare[0]
    for suf in PRIORITY:
        for s in slugs:
            if s.endswith(suf):
                return s
    return sorted(slugs)[0]


def redirect_sources():
    """讀 _redirects，回傳被 301/302 的來源 slug（這些不該進索引，也不該進 sitemap）。

    注意：_redirects 格式是「來源 目的地 狀態碼」，舊檔寫成「來源 301 目的地」
    是錯的，會被 Pages 忽略（2026-10-31 已修正）。
    """
    path = '_redirects'
    if not os.path.exists(path):
        return set()
    out = set()
    for line in open(path, encoding='utf-8'):
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        p = s.split()
        if len(p) == 3 and p[2] in ('301', '302', '307', '308'):
            src = p[0]
            if src.startswith('/articles/'):
                out.add(src[len('/articles/'):])
    return out


def build_plan():
    slugs = all_slugs()
    groups = {}
    for s in slugs:
        groups.setdefault(base_of(s), []).append(s)

    core, variant = set(), set()
    for b, members in groups.items():
        if len(members) == 1:
            core.add(members[0])
        else:
            primary = pick_primary(members)
            core.add(primary)
            for m in members:
                if m != primary:
                    variant.add(m)

    dup = set()
    for keep, drop in DUP_PAIRS:
        if drop in core:
            core.discard(drop)
            variant.add(drop)
            dup.add(drop)

    # 被 _redirects 轉掉的頁面一律不進核心
    redir = redirect_sources()
    for s in list(core):
        if s in redir:
            core.discard(s)
            variant.add(s)

    return {'core': sorted(core), 'variant': sorted(variant), 'dup': sorted(dup)}


ROBOTS_RE = re.compile(r'<meta\s+name="robots"\s+content="[^"]*"\s*/?>', re.I)
HEAD_END = re.compile(r'</head>', re.I)


def set_robots(path, noindex):
    src = open(path, encoding='utf-8').read()
    tag = '<meta name="robots" content="noindex, follow">' if noindex else '<meta name="robots" content="index, follow">'
    if ROBOTS_RE.search(src):
        new = ROBOTS_RE.sub(tag, src, count=1)
    else:
        new = HEAD_END.sub('  ' + tag + '\n</head>', src, count=1)
    if new != src:
        open(path, 'w', encoding='utf-8').write(new)
        return True
    return False


def main():
    plan = build_plan()
    mode = '--report' in sys.argv
    restore = '--restore' in sys.argv

    if restore:
        n = 0
        for s in plan['variant'] + plan['dup']:
            p = os.path.join(ARTICLES, s + '.html')
            if os.path.exists(p) and set_robots(p, False):
                n += 1
        print(f'[restore] {n} 篇恢復 index')
        return

    total = len(plan['core']) + len(plan['variant'])
    print(f'總文章 {total}')
    print(f'  core    (index + sitemap) : {len(plan["core"])}')
    print(f'  variant (noindex, follow) : {len(plan["variant"])}')
    print(f'  dup     (noindex, follow) : {len(plan["dup"])}')

    if mode:
        print('\n[--report] 未修改任何檔案。')
        print('variant 前 15 筆:', plan['variant'][:15])
        return

    changed = 0
    for s in plan['variant'] + plan['dup']:
        p = os.path.join(ARTICLES, s + '.html')
        if os.path.exists(p) and set_robots(p, True):
            changed += 1
    for s in plan['core']:
        p = os.path.join(ARTICLES, s + '.html')
        if os.path.exists(p) and set_robots(p, False):
            changed += 1

    with open(STATE, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)

    print(f'\n[ok] 修改 {changed} 個檔案的 robots meta')
    print(f'[ok] 分級清單寫入 {STATE}')


if __name__ == '__main__':
    main()
