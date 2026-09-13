#!/usr/bin/env python3
"""Fix index.html and region page images."""
import os, re

REPO = r'C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo'
ARTICLES_DIR = os.path.join(REPO, 'articles')
BASE = 'https://chiag455371.github.io/travel-guide.esimart'

def fix_url(url):
    """Clean up loremflickr URL - remove non-ASCII, fix query params."""
    # Remove non-ASCII (Chinese, Japanese, Korean chars)
    url = re.sub(r'[^\x00-\x7F]', '', url)
    # Fix double ??
    while '??' in url:
        url = url.replace('??', '?')
    # Fix multiple ? - keep only first
    parts = url.split('?')
    if len(parts) > 2:
        url = parts[0] + '?' + '&'.join(parts[1:])
    # Add missing dimensions
    if '?lock=' in url and '&w=' not in url:
        # Extract lock value
        m = re.search(r'lock=(\d+)', url)
        if m:
            lock = m.group(1)
            url = url.replace(f'lock={lock}', f'lock={lock}&w=1200&h=600&fit=crop')
    return url

def fix_file(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    orig = content
    # Fix src URLs
    content = re.sub(
        r'src="(https://loremflickr[^"]+)"',
        lambda m: 'src="' + fix_url(m.group(1)) + '"',
        content
    )
    # Fix content= URLs
    content = re.sub(
        r'content="(https://loremflickr[^"]+)"',
        lambda m: 'content="' + fix_url(m.group(1)) + '"',
        content
    )
    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Fix index.html
fix_file(os.path.join(ARTICLES_DIR, 'index.html'))
print('Fixed articles/index.html')

# Fix region pages
for region in ['jp', 'kr', 'tw', 'eu', 'oce']:
    path = os.path.join(ARTICLES_DIR, f'{region}.html')
    if os.path.exists(path):
        if fix_file(path):
            print(f'Fixed articles/{region}.html')

# Final verification
print('\nFinal verification:')
all_urls = set()
for f in os.listdir(ARTICLES_DIR):
    if f.endswith('.html') and f != 'index.html':
        content = open(os.path.join(ARTICLES_DIR, f), encoding='utf-8').read()
        for m in re.finditer(r'https://loremflickr\.com/[^\s"<>]+', content):
            all_urls.add(m.group(0))

broken = 0
for url in all_urls:
    if re.search(r'[^\x00-\x7F]', url):
        broken += 1
        print(f'  BROKEN (non-ASCII): {url[:80]}')
    if '??' in url:
        broken += 1
        print(f'  BROKEN (double ?): {url[:80]}')
    if url.count('?') > 1:
        broken += 1
        print(f'  BROKEN (multiple ?): {url[:80]}')

print(f'Total unique URLs: {len(all_urls)}')
print(f'Broken URLs: {broken}')
