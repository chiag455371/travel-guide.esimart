import re
from pathlib import Path
from difflib import SequenceMatcher

articles_dir = Path('articles')
files = list(articles_dir.glob('*.html'))

missing_bc = []
for f in files:
    text = f.read_text(encoding='utf-8')
    if 'class="breadcrumb"' not in text:
        missing_bc.append(f.name)
print('Missing breadcrumbs:', missing_bc)

titles = {}
for f in files:
    text = f.read_text(encoding='utf-8')
    m = re.search(r'<title>(.*?)</title>', text)
    if m:
        titles[f.name] = m.group(1).strip()
print(f'Total titles: {len(titles)}')

by_region = {}
for name, title in titles.items():
    region = name.split('-')[0]
    by_region.setdefault(region, []).append((name, title))

for region, items in by_region.items():
    for i in range(len(items)):
        for j in range(i+1, len(items)):
            n1, t1 = items[i]
            n2, t2 = items[j]
            ratio = SequenceMatcher(None, t1.lower(), t2.lower()).ratio()
            if ratio > 0.7:
                print(f'SIMILAR ({ratio:.2f}): {n1} | {n2}')
