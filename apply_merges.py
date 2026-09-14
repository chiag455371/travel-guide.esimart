# -*- coding: utf-8 -*-
"""Merge duplicate Hiroshima/Fukuoka/Kamakura articles into 301-style meta-refresh
redirects, update meta descriptions on main pages, clean sitemap + internal links."""
import os, re, glob, pathlib, html as htmlmod
from collections import Counter

SITE = 'https://travel-guide-esimart.pages.dev'

# (duplicate_slug, target_slug, redirect_title)
MERGES = [
    ('jp-hiroshima-itsukushima', 'jp-hiroshima', 'Hiroshima Itsukushima'),
    ('jp-hiroshima-miatu',       'jp-hiroshima', '廣島與宮島一日遊'),
    ('jp-hiroshima-okunoshima',  'jp-hiroshima', 'Hiroshima Okunoshima'),
    ('jp-hiroshima-peace',       'jp-hiroshima', '廣島和平紀念公園'),
    ('jp-fukuoka-food',          'jp-fukuoka',   '福岡美食攻略'),
    ('jp-kamakura-buddha',       'jp-kamakura',  '鎌倉一日遊'),
    # jp-himeji-castle already redirects to jp-himeji; verify target
]

# main-page meta descriptions
META = {
    'jp-hiroshima': '廣島旅遊全攻略：宮島嚴島神社、和平紀念公園、大久野島兔島一日遊詳細介紹。',
    'jp-fukuoka':   '福岡美食攻略：博多拉麵、屋台美食街、中洲川端夜生活完整指南。',
    'jp-kamakura':  '鎌倉一日遊：高德院大佛、鶴岡八幡宮、灌籃高手景點朝聖路線完整指南。',
}

def make_stub(slug, target_slug, title):
    return ('<!DOCTYPE html>\n<html lang="zh-Hant">\n<head>\n'
            '  <meta charset="UTF-8">\n'
            '  <meta http-equiv="refresh" content="0; url=%s/articles/%s.html">\n'
            '  <title>%s - 頁面已搬遷</title>\n'
            '  <meta name="robots" content="noindex">\n'
            '  <link rel="canonical" href="%s/articles/%s.html">\n'
            '  <meta name="description" content="此頁面已搬遷至%s。\n'
            '</head>\n<body>\n'
            '  <p>此頁面已搬遷至 <a href="%s/articles/%s.html">%s</a>。</p>\n'
            '</body>\n</html>\n') % (SITE, target_slug, title, SITE, target_slug,
                                      target_slug, SITE, target_slug, target_slug)

files_touched = []

# 1) create the redirect stubs (preserve any related-sections already added)
for slug, target, title in MERGES:
    p = pathlib.Path('articles/%s.html' % slug)
    if not p.exists():
        print('skip (missing):', slug)
        continue
    p.write_text(make_stub(slug, target, title), encoding='utf-8')
    files_touched.append(slug)
    print('redirect created:', slug, '->', target)

# 2) update meta descriptions on main pages
for slug, desc in META.items():
    p = pathlib.Path('articles/%s.html' % slug)
    if not p.exists():
        print('skip main (missing):', slug)
        continue
    t = p.read_text(encoding='utf-8')
    new = re.sub(r'<meta name="description" content="[^"]*">',
                 '<meta name="description" content="%s">' % htmlmod.escape(desc), t, count=1)
    if new == t:
        # description tag missing -> insert after <title>
        new = re.sub(r'(<title>[^<]*</title>)',
                     r'\1\n  <meta name="description" content="%s">' % htmlmod.escape(desc), t, count=1)
    p.write_text(new, encoding='utf-8')
    print('meta updated:', slug)

# 3) rewrite internal links: any link to a merged slug -> target slug
all_files = glob.glob('articles/*.html') + glob.glob('guides/*.html') + ['index.html', 'sitemap.xml']
link_fixes = 0
for f in all_files:
    p = pathlib.Path(f)
    t = p.read_text(encoding='utf-8')
    orig = t
    for slug, target, _ in MERGES:
        t = t.replace('%s/articles/%s.html' % (SITE, slug), '%s/articles/%s.html' % (SITE, target))
        t = t.replace('/articles/%s.html' % slug, '/articles/%s.html' % target)
    if t != orig:
        p.write_text(t, encoding='utf-8')
        link_fixes += 1
print('files relinked:', link_fixes)

# 4) remove merged slugs from sitemap
sm = pathlib.Path('sitemap.xml').read_text(encoding='utf-8')
lines = sm.split('\n')
kept, removed = [], 0
for line in lines:
    if any(('/articles/%s.html' % s) in line for s, _, _ in MERGES):
        removed += 1
        continue
    kept.append(line)
pathlib.Path('sitemap.xml').write_text('\n'.join(kept), encoding='utf-8')
print('sitemap entries removed:', removed)

print('DONE')
