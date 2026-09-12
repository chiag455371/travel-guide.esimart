#!/usr/bin/env python3
"""Fix all image URLs across the site - ensure valid loremflickr URLs."""
import os, re

REPO = r'C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo'
ARTICLES_DIR = os.path.join(REPO, 'articles')

def fix_url(url):
    """Ensure loremflickr URL has exactly one query string with + for spaces."""
    if 'loremflickr' not in url:
        return url
    # Split on ? to find query parts
    parts = url.split('?')
    if len(parts) == 2:
        base = parts[0]
        query = parts[1]
        # Ensure dimensions are appended properly
        if 'w=' not in query or 'h=' not in query or 'fit=crop' not in query:
            # Add proper dimensions
            query = query.replace('&w=', '?w=')  # fix double ?
            if not query.startswith('w='):
                query = 'w=1200&h=600&fit=crop&' + query
            elif '?' in query:
                query = query.replace('?', '&')
            url = base + '?' + query
    # Replace spaces with +
    url = url.replace(' ', '+')
    # Fix double ? (multiple query strings)
    while '??' in url:
        url = url.replace('??', '?')
    # If there's a second ? after the first query, merge them
    question_count = url.count('?')
    if question_count > 1:
        idx = url.index('?')
        rest = url[idx+1:]
        next_q = rest.find('?')
        if next_q >= 0:
            url = url[:idx+1] + rest[:next_q] + '&' + rest[next_q+1:]
    return url

def process_file(filepath):
    """Fix image URLs in a file."""
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix src="src=" pattern
    content = content.replace('src="src="', 'src="')
    
    # Fix all loremflickr URLs
    def fix_img(match):
        full = match.group(0)
        url = match.group(1)
        fixed_url = fix_url(url)
        return full.replace(url, fixed_url)
    
    content = re.sub(r'src="(https://loremflickr[^"]+)"', fix_img, content)
    
    # Fix og:image URLs too
    content = re.sub(r'content="(https://loremflickr[^"]+)"', lambda m: m.group(0).replace(m.group(1), fix_url(m.group(1))), content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Process all HTML files
changed = []
all_files = []
for root, dirs, files in os.walk(ARTICLES_DIR):
    for f in files:
        if f.endswith('.html'):
            all_files.append(os.path.join(root, f))

for filepath in all_files:
    if process_file(filepath):
        changed.append(filepath)

print(f'Processed {len(all_files)} files, changed {len(changed)}:')
for c in changed:
    print(f'  {os.path.basename(c)}')
