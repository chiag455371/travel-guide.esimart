# -*- coding: utf-8 -*-
import re, glob, os
BASE = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"
fixed = 0
for fp in glob.glob(os.path.join(BASE, "articles/*.html")) + [os.path.join(BASE, "index.html"), os.path.join(BASE, "articles/index.html")]:
    if not os.path.exists(fp): continue
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()
    original = c
    # Fix malformed JSON-LD: duplicate/corrupted image URLs
    # Pattern: image":"https://loremflickr.com/600/400/japan?lock=8888 tower?lock=4320&w=1200&h=630&fit=crop"
    c = re.sub(
        r'"image"\s*:\s*"https://loremflickr\.com/\d+/\d+/[^\"]+\s+[^\"]+"',
        lambda m: '"image":"https://loremflickr.com/1200/630/japan?lock=9001"',
        c
    )
    # Fix any remaining double-URL patterns
    c = re.sub(
        r'"image"\s*:\s*"((?:https?://)[^\"]+)(?:\s+[^\"]+)"',
        r'"image":"\1"',
        c
    )
    # Fix og:image to use 1200x630
    c = re.sub(
        r'property="og:image" content="https://loremflickr\.com/600/400/',
        'property="og:image" content="https://loremflickr.com/1200/630/',
        c
    )
    if c != original:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(c)
        fixed += 1
        print(f"  FIXED: {os.path.basename(fp)}")
print(f"\nTotal fixed: {fixed}")
