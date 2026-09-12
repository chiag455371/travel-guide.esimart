#!/usr/bin/env python3
"""Full image verification + fix for all articles."""
import os, re, urllib.request

REPO = r'C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo'
ARTICLES_DIR = os.path.join(REPO, 'articles')

def fix_url(url):
    if 'loremflickr' not in url:
        return url
    url = url.replace(' ', '+')
    while '??' in url:
        url = url.replace('??', '&')
    q_count = url.count('?')
    if q_count > 1:
        first = url.index('?')
        rest = url[first+1:]
        next_q = rest.find('?')
        if next_q >= 0:
            url = url[:first+1] + rest[:next_q] + '&' + rest[next_q+1:]
    return url

def fix_file(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    orig = content
    content = content.replace('src="src="', 'src="')
    content = re.sub(r'src="(https://loremflickr[^"]+)"',
                     lambda m: m.group(0).replace(m.group(1), fix_url(m.group(1))), content)
    content = re.sub(r'content="(https://loremflickr[^"]+)"',
                     lambda m: m.group(0).replace(m.group(1), fix_url(m.group(1))), content)
    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Fix all files
changed = []
for root, dirs, files in os.walk(ARTICLES_DIR):
    for f in files:
        if f.endswith('.html'):
            if fix_file(os.path.join(root, f)):
                changed.append(f)
print(f'Fixed {len(changed)} files')

# Collect all URLs
all_urls = set()
for root, dirs, files in os.walk(ARTICLES_DIR):
    for f in files:
        if f.endswith('.html'):
            content = open(os.path.join(root, f), encoding='utf-8').read()
            for m in re.finditer(r'https://loremflickr\.com/[^\s"<>]+', content):
                all_urls.add(m.group(0))

print(f'Total unique image URLs: {len(all_urls)}')

# Verify each one
ok = fail = 0
failed = []
for url in sorted(all_urls):
    try:
        resp = urllib.request.urlopen(
            urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}),
            timeout=10)
        if resp.status == 200:
            ok += 1
        else:
            fail += 1
            failed.append((resp.status, url))
    except Exception as e:
        fail += 1
        failed.append((str(e)[:30], url))

print(f'Verified: OK={ok}, Failed={fail}')
for status, url in failed[:10]:
    print(f'  FAIL [{status}]: {url[:80]}')
