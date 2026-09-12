#!/usr/bin/env python3
"""Verify and fix all image URLs across the entire site."""
import os, re, urllib.request, json

REPO = r'C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo'
ARTICLES_DIR = os.path.join(REPO, 'articles')

def fix_loremflickr_url(url):
    """Ensure a loremflickr URL is properly formatted."""
    if 'loremflickr' not in url:
        return url
    # Replace literal spaces with +
    url = url.replace(' ', '+')
    # Fix double query strings: ?lock=X?w=Y -> ?lock=X&w=Y
    while '??' in url:
        url = url.replace('??', '&')
    # If there are multiple ? in the URL (after the first), merge them
    q_count = url.count('?')
    if q_count > 1:
        first_q = url.index('?')
        rest = url[first_q+1:]
        next_q = rest.find('?')
        if next_q >= 0:
            before = rest[:next_q]
            after = rest[next_q+1:]
            url = url[:first_q+1] + before + '&' + after
    return url

def process_file(filepath):
    """Fix all image URLs in an HTML file."""
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix src="src=" pattern
    content = content.replace('src="src="', 'src="')
    
    # Fix all loremflickr image URLs in src="..."
    def fix_src(match):
        full = match.group(0)
        url = match.group(1)
        fixed = fix_loremflickr_url(url)
        return full.replace(url, fixed)
    content = re.sub(r'src="(https://loremflickr[^"]+)"', fix_src, content)
    
    # Fix og:image content="..." and twitter content="..."
    def fix_content(match):
        full = match.group(0)
        url = match.group(1)
        fixed = fix_loremflickr_url(url)
        return full.replace(url, fixed)
    content = re.sub(r'content="(https://loremflickr[^"]+)"', fix_content, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Process all HTML files
all_files = []
for root, dirs, files in os.walk(ARTICLES_DIR):
    for f in files:
        if f.endswith('.html'):
            all_files.append(os.path.join(root, f))

changed = []
for filepath in all_files:
    if process_file(filepath):
        changed.append(os.path.basename(filepath))

print(f'Processed {len(all_files)} files, fixed {len(changed)}:')
for c in changed:
    print(f'  {c}')

# Now verify all image URLs
print('\n--- Verifying images ---')
all_urls = set()
for filepath in all_files:
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    for match in re.finditer(r'(https://loremflickr\.com/[^\s"<>]+)', content):
        all_urls.add(match.group(1))

print(f'Total unique image URLs: {len(all_urls)}')

# Test a sample
tested = 0; ok = 0; failed = []
for url in sorted(all_urls)[:30]:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        resp = urllib.request.urlopen(req, timeout=8)
        if resp.status == 200:
            ok += 1
        else:
            failed.append((resp.status, url[:70]))
    except Exception as e:
        failed.append((str(e)[:40], url[:70]))
    tested += 1

print(f'Tested {tested}: OK={ok}, Failed={len(failed)}')
for status, url in failed[:10]:
    print(f'  FAIL: {status} | {url}')
