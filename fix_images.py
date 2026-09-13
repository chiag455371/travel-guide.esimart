#!/usr/bin/env python3
"""Fix all broken image URLs in articles."""
import os, re

ARTICLES_DIR = r'C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo\articles'

def fix_url(url):
    """Clean up loremflickr URL."""
    # Remove non-ASCII chars (Chinese, etc)
    url = re.sub(r'[^\x00-\x7F]', '', url)
    # Fix double ??
    while '??' in url:
        url = url.replace('??', '?')
    # Fix multiple ? - keep only first
    parts = url.split('?')
    if len(parts) > 2:
        url = parts[0] + '?' + '&'.join(parts[1:])
    # Replace spaces with +
    url = url.replace(' ', '+')
    return url

files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.html') and f != 'index.html']
fixed_count = 0

for f in files:
    path = os.path.join(ARTICLES_DIR, f)
    content = open(path, encoding='utf-8').read()
    orig = content
    
    # Fix src="..." URLs
    content = re.sub(
        r'src="(https://loremflickr[^"]+)"',
        lambda m: 'src="' + fix_url(m.group(1)) + '"',
        content
    )
    # Fix content="..." URLs (og:image, twitter:image, json ld)
    content = re.sub(
        r'content="(https://loremflickr[^"]+)"',
        lambda m: 'content="' + fix_url(m.group(1)) + '"',
        content
    )
    
    if content != orig:
        with open(path, 'w', encoding='utf-8') as fp:
            fp.write(content)
        fixed_count += 1

print(f'Fixed {fixed_count}/{len(files)} article files')

# Collect all unique URLs and count
all_urls = set()
for f in files:
    content = open(os.path.join(ARTICLES_DIR, f), encoding='utf-8').read()
    for m in re.finditer(r'https://loremflickr\.com/[^\s"<>]+', content):
        all_urls.add(m.group(0))

print(f'Total unique image URLs: {len(all_urls)}')

# Check for remaining issues
issues = 0
for url in all_urls:
    if re.search(r'[^\x00-\x7F]', url):
        print(f'  STILL HAS NON-ASCII: {url[:80]}')
        issues += 1
    if '??' in url:
        print(f'  STILL HAS DOUBLE ?: {url[:80]}')
        issues += 1
    if url.count('?') > 1:
        print(f'  STILL HAS MULTIPLE ? : {url[:80]}')
        issues += 1

print(f'Remaining issues: {issues}')
