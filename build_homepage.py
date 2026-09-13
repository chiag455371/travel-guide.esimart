# -*- coding: utf-8 -*-
"""Build index.html with dynamic article previews."""
import os, re, html

BASE = 'https://chiag455371.github.io/travel-guide.esimart'
FILES = [f for f in os.listdir('articles') if f.endswith('.html')]
regions_order = ['jp', 'kr', 'tw', 'eu', 'oce']
region_flags = {'jp': '🇯🇵', 'kr': '🇰🇷', 'tw': '🇹🇼', 'eu': '🇪🇺', 'oce': '🇦🇺'}
region_names = {'jp': '日本', 'kr': '韓國', 'tw': '台灣', 'eu': '歐洲', 'oce': '澳洲'}

# Latest 4 articles per region (by mtime)
region_articles = {r: [] for r in regions_order}
for f in sorted(FILES, key=lambda x: os.path.getmtime('articles/' + x), reverse=True):
    m = re.match(r'^(jp|kr|tw|eu|oce)-', f)
    if m:
        r = m.group(1)
        if len(region_articles[r]) < 4:
            region_articles[r].append(f.replace('.html', ''))

# Totals
region_counts = {}
for r in regions_order:
    region_counts[r] = len([f for f in FILES if f.startswith(r + '-')])
total = len(FILES)


def make_card(slug):
    fpath = 'articles/' + slug + '.html'
    content = open(fpath, encoding='utf-8').read()
    m = re.search(r'<title>(.*?)</title>', content)
    title_raw = m.group(1).strip() if m else slug
    title = re.sub(r'\s*[｜-]\s*旅遊通.*$', '', title_raw).strip()
    m2 = re.search(r'<meta name="description" content="(.*?)">', content)
    desc = (m2.group(1)[:100] + '...') if m2 else title[:50]
    m3 = re.search(r'<img[^>]+src="(https://loremflickr[^"]+)"', content)
    img = m3.group(1) if m3 else ''
    t = html.escape(title)
    d = html.escape(desc)
    url = BASE + '/articles/' + slug + '.html'
    return (
        '      <a href="' + url + '" class="article-card">\n'
        '        <div class="card-img-wrapper"><img class="card-img" src="' + img
        + '" alt="' + t + '" loading="lazy"></div>\n'
        '        <div class="card-body">\n'
        '          <span class="card-title">' + t + '</span>\n'
        '          <span class="card-desc">' + d + '</span>\n'
        '          <div class="card-meta"><span class="card-meta-dot"></span>'
        '<span>約 8 分鐘閱讀</span></div>\n'
        '        </div>\n'
        '      </a>'
    )


region_sections = ''
for r in regions_order:
    items = region_articles[r]
    cards = '\n'.join(make_card(s) for s in items)
    region_sections += (
        '  <div class="region-section">\n'
        '    <div class="region-header">\n'
        '      <div class="region-icon">' + region_flags[r] + '</div>\n'
        '      <h2>' + region_names[r] + '旅遊攻略</h2>\n'
        '      <a href="' + BASE + '/articles/' + r + '.html">'
        + '查看全部 ' + str(region_counts[r]) + ' 篇 &#8594;</a>\n'
        '    </div>\n'
        '    <div class="card-grid">\n'
        + cards + '\n'
        '    </div>\n'
        '  </div>\n'
    )

# Read current index.html
content = open('index.html', encoding='utf-8').read()

# Replace region sections: from first <div class="region-section"> to <hr class="divider">
start_idx = content.find('  <div class="region-section">')
end_idx = content.find('<hr class="divider">')
if start_idx >= 0 and end_idx >= 0:
    new_content = content[:start_idx] + region_sections + content[end_idx:]
else:
    print('ERROR: Could not find region sections in index.html')
    print('start:', start_idx, 'end:', end_idx)
    new_content = content

# Also update region card counts in the quick-nav section
for r in regions_order:
    old_count = re.search(
        r'(<div class="region-card-count">' + region_names[r] + r'</div>[\s\S]*?'
        r'<div class="region-card-count">)(\d+)\s*篇',
        content)
    if old_count:
        new_content = re.sub(
            r'(region-card-count">)' + region_names[r] + r'([^<]*)篇',
            lambda m, r=r: m.group(1) + region_names[r] + str(region_counts[r]) + ' 篇',
            new_content)

open('index.html', 'w', encoding='utf-8').write(new_content)
print('index.html updated: total=' + str(total) + ' articles')
for r in regions_order:
    print(f'  {r}: {region_counts[r]} total, previews: {region_articles[r]}')
