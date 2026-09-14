# -*- coding: utf-8 -*-
"""Add a 'related-section' block to every article file: 3-5 related articles
from the same region (same country slug prefix), picked by filename similarity,
always including same-suburb/spot articles first. Inserted before the closing
</main> or before the CTA footer block."""
import re, glob, os, collections

BASE = 'https://travel-guide-esimart.pages.dev'
REGION_NAMES = {
    'jp': '日本', 'kr': '韓國', 'tw': '台灣', 'eu': '歐洲', 'oce': '大洋洲',
}

# slug -> (title, og_seed)
titles = {}
for f in glob.glob('articles/*.html'):
    slug = os.path.basename(f)[:-5]
    c = open(f, encoding='utf-8').read()
    m = re.search(r'<title>([^<]+)</title>', c)
    t = m.group(1) if m else slug
    t = t.split('｜')[0].strip()
    og = re.search(r'og:image" content="https://picsum\.photos/seed/(\d+)/', c)
    titles[slug] = (t, og.group(1) if og else None)

def related_for(slug, n=4):
    """Pick up to n related articles: same region, prefer same secondary tag
    (the part after the first dash), then any other same-region articles."""
    prefix = slug.split('-')[0]
    parts = slug.split('-')
    same_tag = [s for s in titles if s != slug and s.split('-')[0] == prefix
                and len(s.split('-')) >= 2 and s.split('-')[1] == parts[1]]
    others = [s for s in titles if s != slug and s.split('-')[0] == prefix
              and s not in same_tag]
    # same-tag first (deterministic order), fill with others
    picked = same_tag[:n]
    rest = [s for s in others if s not in picked]
    while len(picked) < n and rest:
        picked.append(rest.pop(0))
    return picked[:n]

def card_block(slug):
    t, seed = titles[slug]
    seed = seed or '100000'
    return (
        f'      <a href="{BASE}/articles/{slug}.html" class="related-card">'
        f'<div class="card-img-wrapper"><img class="card-img" '
        f'src="https://picsum.photos/seed/{seed}/600/400" alt="{t}" loading="lazy"></div>'
        f'<div class="card-body"><span class="card-title">{t}</span></div></a>')

def section_block(slug):
    rel = related_for(slug)
    if not rel:
        return None
    cards = '\n'.join(card_block(s) for s in rel)
    region = slug.split('-')[0]
    region_name = REGION_NAMES.get(region, region)
    return (f'\n<div class="related-section">\n'
            f'  <h2>延伸閱讀｜{region_name}更多攻略</h2>\n'
            f'  <div class="related-grid">\n{cards}\n  </div>\n</div>\n')

inserted = 0
skipped = 0
existing = 0
for f in sorted(glob.glob('articles/*.html')):
    slug = os.path.basename(f)[:-5]
    if slug in ('index', 'jp', 'kr', 'tw', 'eu', 'oce'):
        continue
    c = open(f, encoding='utf-8').read()
    if 'class="related-section"' in c:
        existing += 1
        continue
    block = section_block(slug)
    if not block:
        skipped += 1
        continue
    # insert before the CTA banner (the distributor purchase box) or before </main>
    m = re.search(r'(<div class="cta-banner"|<section class="cta-banner"|</main>)', c)
    if m:
        pos = m.start()
        c = c[:pos] + block + c[pos:]
    else:
        c += block
    open(f, 'w', encoding='utf-8').write(c)
    inserted += 1

print(f'inserted={inserted} skipped(no-articles)={skipped} already-had={existing}')

# spot check
sample = open('articles/jp-kyoto-fushimi.html', encoding='utf-8').read()
rel = re.findall(r'related-card"[^>]*href="[^"]*?articles/([a-z0-9\-]+)\.html', sample)
print('jp-kyoto-fushimi related:', rel)
