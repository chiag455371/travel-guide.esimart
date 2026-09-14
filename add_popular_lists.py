# -*- coding: utf-8 -*-
"""Add a compact '熱門文章' list (top 6, one per major sub-destination) to each
region index file, inserted right after the card grid section ends."""
import re, os, collections

BASE = 'https://travel-guide-esimart.pages.dev'

# Hand-picked: 1 canonical article per major spot, in order
POPULAR = {
    'jp': [
        ('jp-tokyo-shibuya', '東京'),
        ('jp-kyoto-arashiyama', '京都'),
        ('jp-osaka-dotonbori', '大阪'),
        ('jp-hokkaido-snow', '北海道'),
        ('jp-okinawa-beach', '沖繩'),
        ('jp-fuji-hiking', '富士山'),
    ],
    'kr': [
        ('kr-seoul-gyeongbok', '首爾'),
        ('kr-jeju', '濟州島'),
        ('kr-busan', '釜山'),
        ('kr-bucheon-aquarium', '富川'),
        ('kr-gyeongju', '慶州'),
        ('kr-seoul-mydong', '弘大'),
    ],
    'tw': [
        ('tw-taipei-101', '台北'),
        ('tw-shilin-night', '士林'),
        ('tw-yilan', '宜蘭'),
        ('tw-taitung-hot', '台東'),
        ('tw-penghu', '澎湖'),
        ('tw-hualien', '花蓮'),
    ],
    'eu': [
        ('eu-paris-eiffel', '巴黎'),
        ('eu-rome-colosseum', '羅馬'),
        ('eu-barcelona', '巴塞隆納'),
        ('eu-london', '倫敦'),
        ('eu-venice-canals', '威尼斯'),
        ('eu-amsterdam', '阿姆斯特丹'),
    ],
    'oce': [
        ('oce-sydney-opera', '雪梨'),
        ('oce-mel', '墨爾本'),
        ('oce-queenstown', '克倫伯'),
        ('oce-perth-kangaroo', '珀斯'),
        ('oce-adelaide', '阿德萊德'),
        ('oce-auckland-rangitoto', '奧克蘭'),
    ],
}

def get_title_and_seed(slug):
    try:
        c = open(f'articles/{slug}.html', encoding='utf-8').read()
    except FileNotFoundError:
        return slug, None
    m = re.search(r'<title>([^<]+)</title>', c)
    t = (m.group(1) if m else slug).split('｜')[0].strip()
    og = re.search(r'og:image" content="https://picsum\.photos/seed/(\d+)/', c)
    return t, (og.group(1) if og else None)

for region, popular in POPULAR.items():
    fname = f'articles/{region}.html'
    c = open(fname, encoding='utf-8').read()
    if 'popular-list' in c:
        print(region, 'already has popular list')
        continue

    items = []
    for slug, label in popular:
        title, seed = get_title_and_seed(slug)
        seed = seed or '100000'
        items.append(
            f'    <li><a href="{BASE}/articles/{slug}.html" class="popular-item">'
            f'<span class="popular-label">{label}</span>'
            f'<img class="popular-img" src="https://picsum.photos/seed/{seed}/80/80" '
            f'alt="{title}" loading="lazy" width="80" height="80">'
            f'<span class="popular-title">{title}</span></a></li>')

    block = (
        '\n  <h2 style="margin:1rem 0 .5rem;font-size:1.3rem;font-weight:900">'
        '🔥 熱門攻略</h2>\n'
        '  <ol class="popular-list">\n'
        + '\n'.join(items)
        + '\n  </ol>\n'
    )

    # insert before the CTA banner or before </main>
    m = re.search(r'(<div class="cta-banner"|</main>)', c)
    pos = m.start() if m else len(c)
    c = c[:pos] + block + c[pos:]
    open(fname, 'w', encoding='utf-8').write(c)
    print(region, 'popular list added,', len(items), 'items')
