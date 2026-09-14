# -*- coding: utf-8 -*-
"""Add breadcrumbs to all article files that don't already have them,
and to the 6 region index files."""
import re, glob, os

BASE = 'https://travel-guide-esimart.pages.dev'
REGION_NAMES = {
    'jp': '日本攻略', 'kr': '韓國攻略', 'tw': '台灣攻略',
    'eu': '歐洲攻略', 'oce': '大洋洲攻略',
}

def get_title(slug):
    try:
        c = open(f'articles/{slug}.html', encoding='utf-8').read()
    except FileNotFoundError:
        return slug
    m = re.search(r'<title>([^<]+)</title>', c)
    t = m.group(1) if m else slug
    return t.split('｜')[0].strip()[:30]

def breadcrumb_html(slug):
    region = slug.split('-')[0]
    region_name = REGION_NAMES.get(region, region)
    region_link = f'{BASE}/articles/{region}.html'
    title = get_title(slug)
    return (
        f'<nav aria-label="breadcrumb" class="breadcrumb-nav">\n'
        f'  <ol class="breadcrumb">\n'
        f'    <li><a href="{BASE}/">首頁</a></li>\n'
        f'    <li><a href="{region_link}">{region_name}</a></li>\n'
        f'    <li aria-current="page">{title}</li>\n'
        f'  </ol>\n'
        f'</nav>\n')

# --- Articles ---
inserted = 0
skipped = 0
for f in sorted(glob.glob('articles/*.html')):
    slug = os.path.basename(f)[:-5]
    if slug in ('index', 'jp', 'kr', 'tw', 'eu', 'oce'):
        continue
    c = open(f, encoding='utf-8').read()
    if 'class="breadcrumb"' in c:
        skipped += 1
        continue
    # insert right after <h1>...</h1>
    m = re.search(r'(<h1>[^<]+</h1>)', c)
    if m:
        pos = m.end()
        c = c[:pos] + '\n' + breadcrumb_html(slug) + c[pos:]
    else:
        c += '\n' + breadcrumb_html(slug)
    open(f, 'w', encoding='utf-8').write(c)
    inserted += 1

print(f'articles: inserted={inserted} already-had={skipped}')

# --- Region index files ---
for region in ['jp', 'kr', 'tw', 'eu', 'oce', 'index']:
    fname = f'articles/{region}.html'
    c = open(fname, encoding='utf-8').read()
    if 'class="breadcrumb"' in c:
        print(region, 'already has breadcrumb')
        continue
    region_name = REGION_NAMES.get(region, '全部攻略')
    if region == 'index':
        crumb = (f'<nav aria-label="breadcrumb" class="breadcrumb-nav">\n'
                 f'  <ol class="breadcrumb">\n'
                 f'    <li><a href="{BASE}/">首頁</a></li>\n'
                 f'    <li aria-current="page">全部攻略</li>\n'
                 f'  </ol>\n</nav>\n')
    else:
        crumb = (f'<nav aria-label="breadcrumb" class="breadcrumb-nav">\n'
                 f'  <ol class="breadcrumb">\n'
                 f'    <li><a href="{BASE}/">首頁</a></li>\n'
                 f'    <li><a href="{BASE}/articles/index.html">全部攻略</a></li>\n'
                 f'    <li aria-current="page">{region_name}</li>\n'
                 f'  </ol>\n</nav>\n')
    m = re.search(r'(<h1>[^<]+</h1>)', c)
    if m:
        pos = m.end()
        c = c[:pos] + '\n' + crumb + c[pos:]
    else:
        c += '\n' + crumb
    open(fname, 'w', encoding='utf-8').write(c)
    print(region, 'breadcrumb added')
