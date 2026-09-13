#!/usr/bin/env python3
"""Find and fix remaining broken image URLs."""
import os, re

ARTICLES_DIR = r'C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo\articles'

def is_broken(url):
    """Check if URL has issues."""
    if re.search(r'[\u4e00-\u9fff]', url):
        return True, 'has_chinese'
    if '??' in url:
        return True, 'double_question'
    if url.count('?') > 1:
        return True, 'multiple_questions'
    return False, None

def fix_url(url):
    """Fix broken URL."""
    url = re.sub(r'[\u4e00-\u9fff]+', '', url)  # Remove Chinese
    while '??' in url:
        url = url.replace('??', '?')
    parts = url.split('?')
    if len(parts) > 2:
        url = parts[0] + '?' + '&'.join(parts[1:])
    return url

files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.html') and f != 'index.html']
total_fixed = 0

for f in files:
    path = os.path.join(ARTICLES_DIR, f)
    content = open(path, encoding='utf-8').read()
    orig = content
    
    # Find all loremflickr URLs
    for m in re.finditer(r'(https://loremflickr[^"\s<>]+)', content):
        url = m.group(1)
        broken, reason = is_broken(url)
        if broken:
            fixed = fix_url(url)
            content = content.replace(url, fixed)
    
    if content != orig:
        with open(path, 'w', encoding='utf-8') as fp:
            fp.write(content)
        total_fixed += 1
        print(f'Fixed: {f}')

print(f'\nTotal files fixed: {total_fixed}/{len(files)}')

# Final check
remaining = 0
for f in files:
    content = open(os.path.join(ARTICLES_DIR, f), encoding='utf-8').read()
    for m in re.finditer(r'https://loremflickr[^"\s<>]+', content):
        url = m.group(0)
        broken, reason = is_broken(url)
        if broken:
            print(f'  STILL BROKEN [{reason}]: {url[:80]}')
            remaining += 1

print(f'Remaining broken URLs: {remaining}')
