# -*- coding: utf-8 -*-
import os, re, glob

BASE = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"
ARTICLES = os.path.join(BASE, "articles")
DISTRIBUTOR = "https://travel-guide.esimart.cc/goods"

UNSPLASH_MAP = {
    "jp-tokyo-tower": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=1200&h=630&fit=crop",
    "jp-tokyo-shibuya": "https://images.unsplash.com/photo-1542051841857-5f90071e7989?w=1200&h=630&fit=crop",
    "jp-osaka-doton": "https://images.unsplash.com/photo-1590559844485-8d60b2e5c8e8?w=1200&h=630&fit=crop",
    "jp-fuji-hiking": "https://images.unsplash.com/photo-1490806843957-31ef8fe7c526?w=1200&h=630&fit=crop",
    "jp-kyoto-fushimi": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=1200&h=630&fit=crop",
    "jp-nara-deer": "https://images.unsplash.com/photo-1545569368-b94b46e177a5?w=1200&h=630&fit=crop",
    "jp-hakone-onsen": "https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=1200&h=630&fit=crop",
    "jp-hokkaido-snow": "https://images.unsplash.com/photo-1516483638261-f4dbaf036963?w=1200&h=630&fit=crop",
    "kr-seoul-naksan": "https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?w=1200&h=630&fit=crop",
    "kr-busan-haeundae": "https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?w=1200&h=630&fit=crop",
    "kr-jeju-hallasan": "https://images.unsplash.com/photo-1570197571499-166b36495c?w=1200&h=630&fit=crop",
    "tw-taipei-101": "https://images.unsplash.com/photo-1553812733-7c5cc5a75c57?w=1200&h=630&fit=crop",
    "eu-paris": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1200&h=630&fit=crop",
    "eu-london": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1200&h=630&fit=crop",
    "eu-rome": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=1200&h=630&fit=crop",
    "eu-barcelona": "https://images.unsplash.com/photo-1583422409516-2895a77efded?w=1200&h=630&fit=crop",
    "eu-amsterdam": "https://images.unsplash.com/photo-1534146789009-76ca50606c63?w=1200&h=630&fit=crop",
    "oce-sydney": "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=1200&h=630&fit=crop",
    "oce-mel": "https://images.unsplash.com/photo-1523482580672-f109ba8cb9be?w=1200&h=630&fit=crop",
}

DEFAULT_IMAGES = {
    "jp": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=1200&h=630&fit=crop",
    "kr": "https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?w=1200&h=630&fit=crop",
    "tw": "https://images.unsplash.com/photo-1553812733-7c5cc5a75c57?w=1200&h=630&fit=crop",
    "eu": "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?w=1200&h=630&fit=crop",
    "oce": "https://images.unsplash.com/photo-1523482580672-f109ba8cb9be?w=1200&h=630&fit=crop",
}

def get_region(fn):
    if fn.startswith("jp-"): return "jp"
    if fn.startswith("kr-"): return "kr"
    if fn.startswith("tw-"): return "tw"
    if fn.startswith("eu-"): return "eu"
    if fn.startswith("oce-"): return "oce"
    return None

def fix_article(fp):
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    orig = content
    fn = os.path.basename(fp)
    region = get_region(fn)
    changed = False

    # Replace specific Unsplash images
    for pattern, url in UNSPLASH_MAP.items():
        if pattern in fn:
            thumb = url.replace("1200", "600").replace("h=630", "h=400")
            lf_600 = "https://loremflickr.com/600/400/"
            lf_1200 = "https://loremflickr.com/1200/630/"
            # Find and replace the first occurrence of each
            idx600 = content.find(lf_600)
            if idx600 >= 0:
                # Find end of URL
                end600 = content.find('"', idx600)
                content = content[:idx600] + thumb + content[end600:]
                changed = True
            idx1200 = content.find(lf_1200)
            if idx1200 >= 0:
                end1200 = content.find('"', idx1200)
                content = content[:idx1200] + url + content[end1200:]
                changed = True
            break

    # Fallback: replace all remaining loremflickr with region default
    if region and region in DEFAULT_IMAGES:
        default = DEFAULT_IMAGES[region]
        thumb = default.replace("1200", "600").replace("h=630", "h=400")
        new_content = re.sub(r'https://loremflickr\.com/600/400/[^\s"\'<>]+', thumb, content)
        new_content = re.sub(r'https://loremflickr\.com/1200/630/[^\s"\'<>]+', default, new_content)
        if new_content != content:
            content = new_content
            changed = True

    # Fix distributor eSIM links
    new_content = re.sub(r'href="(https://travel-guide\.esimart\.cc/goods/\d+)"', f'href="{DISTRIBUTOR}"', content)
    new_content = re.sub(r'href="(https://travel-guide\.esimart\.cc/goods[^"]*)"', f'href="{DISTRIBUTOR}"', new_content)
    if new_content != content:
        content = new_content
        changed = True

    if changed:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  FIXED: {fn}")
        return True
    return False

print("=== Fixing article images and links ===")
files = glob.glob(os.path.join(ARTICLES, "*.html"))
fixed = 0
for fpath in sorted(files):
    if fix_article(fpath): fixed += 1
print(f"Total fixed: {fixed}")
