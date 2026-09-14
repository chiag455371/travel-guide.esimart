# -*- coding: utf-8 -*-
"""Create _redirects for 301 merges of duplicate articles, remove from sitemap."""
import re, os

# (source, target)
REDIRECTS = [
    ('jp-hiroshima-okunoshima.html', '/articles/jp-hiroshima-itsukushima.html'),
    ('jp-hiroshima-itsukushima.html', '/articles/jp-hiroshima.html'),
    ('jp-hiroshima-okunoshima.html', '/articles/jp-hiroshima.html'),  # chain not used; direct
    ('jp-awaji-union.html', '/articles/jp-awaji.html'),
    ('jp-nikko-shrine.html', '/articles/jp-nikko-tobu.html'),
    ('eu-flanders-bruges.html', '/articles/eu-bruges.html'),
    ('tw-luku-geopark.html', '/articles/tw-luceat.html'),
]
# Keep only the first redirect for each source; build a clean map
source_to_target = {}
for src, tgt in REDIRECTS:
    source_to_target[src] = tgt

# Deduplicate: if source appears twice, keep the first
lines = []
for src, tgt in source_to_target.items():
    lines.append(f'/articles/{src} 301 {tgt}')

with open('_redirects', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

print('Created _redirects with', len(lines), 'rules:')
for l in lines:
    print(' ', l)

# Remove merged sources from sitemap
removed = 0
with open('sitemap.xml', encoding='utf-8') as f:
    sm = f.read()
for src in source_to_target:
    slug = src[:-5]
    pattern = re.compile(
        r'<url><loc>https://travel-guide-esimart\.pages\.dev/articles/' +
        re.escape(slug) + r'\.html</loc>[^<]*</url>\n?')
    sm, n = pattern.subn('', sm)
    removed += n
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print(f'removed {removed} URLs from sitemap')

# Update internal links in all articles + region pages
import glob
updated_files = 0
all_files = glob.glob('articles/*.html') + ['index.html']
for fname in all_files:
    c = open(fname, encoding='utf-8').read()
    orig = c
    for src, tgt in source_to_target.items():
        src_slug = src[:-5]
        c = c.replace(f'/articles/{src_slug}.html', tgt)
    if c != orig:
        open(fname, 'w', encoding='utf-8').write(c)
        updated_files += 1
print(f'updated internal links in {updated_files} files')
