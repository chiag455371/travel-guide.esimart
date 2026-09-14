# -*- coding: utf-8 -*-
import re, glob, pathlib, sys, json, collections
SITE = 'https://travel-guide-esimart.pages.dev'
MERGES = [
    ('jp-himeji-castle', 'jp-himeji'),
    ('jp-takamatsu-rittoru', 'jp-takamatsu-garden'),
]
# 1) rewrite the short one to a meta-refresh stub, using existing real-article schema + related cards
cache = json.load(open('image_cache.json', encoding='utf-8'))
def thumb(slug):
    v = cache.get(slug) or cache.get(slug.rsplit('-',1)[0]) or {}
    return v.get('thumb') or v.get('url')
# collect real articles for related (per region)
region_articles = collections.defaultdict(list)
for f in glob.glob('articles/*.html'):
    c = pathlib.Path(f).read_text(encoding='utf-8')
    if 'http-equiv' in c: continue
    s = f.split('/')[-1][:-5]
    region_articles[s.split('-')[0]].append(s)

import html as htmlmod
def make_stub(slug, keep_slug, title, desc, keep_img, related):
    rel_cards = []
    for rs, rtitle in related:
        rimg = thumb(rs) or 'https://upload.wikimedia.org/wikipedia/commons/4/4b/Amsterdam_-_48390199071.jpg'
        rel_cards.append(
          f'      <a href=\"{SITE}/articles/{rs}.html\" class=\"related-card\"><div class=\"card-img-wrapper\"><img class=\"card-img\" src=\"{rimg}\" alt=\"{htmlmod.escape(rtitle)}\" loading=\"lazy\"></div><div class=\"card-body\"><span class=\"card-title\">{rtitle}</span></div></a>'
        )
    related_html = chr(10).join(rel_cards)
    region = keep_slug.split('-')[0]
    region_name = {'jp':'日本','kr':'韓國','tw':'台灣','eu':'歐洲','oce':'大洋洲'}[region]
    redirect_url = SITE + '/articles/' + keep_slug + '.html'
    schema = '''{"@context":"https://schema.org","@type":"Article","headline":"''' + htmlmod.escape(title) + '''","description":"''' + htmlmod.escape(desc) + '''","image":"''' + keep_img + '''","dateModified":"2026-09-15","author":{"@type":"Organization","name":"旅遊通 eSIM"},"publisher":{"@type":"Organization","name":"旅遊通 eSIM","url":"https://travel-guide.esimart.cc"},"mainEntityOfPage":{"@type":"WebPage","@id":"''' + SITE + '/articles/' + slug + '.html"}}'''
    page = f'''<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={redirect_url}">
<link rel="canonical" href="{redirect_url}">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}/articles/{slug}.html">
<meta property="og:image" content="{keep_img}">
<meta property="og:type" content="article">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{schema}</script>
</head><body>
<p>此文章已合併至 <a href="{redirect_url}">{keep_slug}</a>。</p>
<div class="related-section">
  <h2>延伸閱讀｜{region_name}更多攻略</h2>
  <div class="related-grid">
{related_html}
  </div>
</div>
</body></html>'''
    return page

for slug, keep_slug in MERGES:
    keep = pathlib.Path(f'articles/{keep_slug}.html').read_text(encoding='utf-8')
    m = re.search(r'<title>([^<]+)</title>', keep)
    title = m.group(1) if m else keep_slug
    md = re.search(r'name="description" content="([^"]+)"', keep)
    desc = md.group(1) if md else title
    ogi = re.search(r'og:image" content="([^"]+)"', keep)
    keep_img = ogi.group(1) if ogi else 'https://upload.wikimedia.org/wikipedia/commons/4/4b/Amsterdam_-_48390199071.jpg'
    # 4 related, exclude both slugs
    region = keep_slug.split('-')[0]
    cands = [s for s in region_articles[region] if s not in (slug, keep_slug)]
    random = __import__('random')
    random.seed(hash(slug) & 0xFFFF)
    random.shuffle(cands)
    related = []
    for rs in cands[:4]:
        rc = pathlib.Path(f'articles/{rs}.html').read_text(encoding='utf-8')
        rt = re.search(r'<title>([^<]+)</title>', rc)
        related.append((rs, (rt.group(1) if rt else rs).split('｜')[0]))
    new_page = make_stub(slug, keep_slug, title, desc, keep_img, related)
    pathlib.Path(f'articles/{slug}.html').write_text(new_page, encoding='utf-8')
    print('merged', slug, '->', keep_slug)
    # remove from sitemap
    sm = pathlib.Path('sitemap.xml').read_text(encoding='utf-8')
    sm2 = re.sub(r'<url><loc>[^<]*' + re.escape(slug) + r'\.html</loc>.*?</url>\n?', '', sm, flags=re.S)
    pathlib.Path('sitemap.xml').write_text(sm2, encoding='utf-8')
    # rewrite any internal links pointing to the old slug
    for f in glob.glob('articles/*.html') + glob.glob('guides/*.html') + ['index.html']:
        c = pathlib.Path(f).read_text(encoding='utf-8')
        if f'/{slug}.html' in c:
            c2 = c.replace(f'/{slug}.html', f'/{keep_slug}.html')
            if c2 != c:
                pathlib.Path(f).write_text(c2, encoding='utf-8')
                print('  relinked', f)
print('done')
