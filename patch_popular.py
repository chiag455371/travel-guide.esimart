# -*- coding: utf-8 -*-
import pathlib, re
p = pathlib.Path('add_popular_lists.py')
s = p.read_text(encoding='utf-8')
# inject cache-based thumb resolution
old = '''def get_title_and_seed(slug):
    try:
        c = open(f'articles/{slug}.html', encoding='utf-8').read()
    except FileNotFoundError:
        return slug, None
    m = re.search(r'<title>([^<]+)</title>', c)
    t = (m.group(1) if m else slug).split('｜')[0].strip()
    og = re.search(r'og:image" content="https://picsum\\.photos/seed/(\\d+)/', c)
    return t, (og.group(1) if og else None)'''
new = '''import json, hashlib
_IMG_CACHE = {}
try:
    _IMG_CACHE = json.load(open('image_cache.json', encoding='utf-8'))
except Exception:
    pass
_REGION_THUMBS = {}
for _k, _v in _IMG_CACHE.items():
    _t = _v.get('thumb') or _v.get('url')
    if _t:
        _REGION_THUMBS.setdefault(_k.split('-')[0], []).append(_t)
_ALL_THUMBS = [t for lst in _REGION_THUMBS.values() for t in lst] or ['https://upload.wikimedia.org/wikipedia/commons/4/4b/Amsterdam_-_48390199071.jpg']

def thumb_for(slug, region):
    v = _IMG_CACHE.get(slug) or _IMG_CACHE.get(slug.rsplit('-', 1)[0]) or {}
    url = v.get('thumb') or v.get('url')
    if url:
        return url
    opts = _REGION_THUMBS.get(region, _ALL_THUMBS)
    i = int(hashlib.md5(slug.encode()).hexdigest(), 16) % len(opts)
    return opts[i]

def get_title_and_seed(slug, region):
    try:
        c = open(f'articles/{slug}.html', encoding='utf-8').read()
    except FileNotFoundError:
        return slug, thumb_for(slug, region)
    m = re.search(r'<title>([^<]+)</title>', c)
    t = (m.group(1) if m else slug).split('｜')[0].strip()
    return t, thumb_for(slug, region)'''
assert old in s, 'old block not found'
s = s.replace(old, new, 1)
# update call sites + img src
s = s.replace("title, seed = get_title_and_seed(slug)", "title, seed = get_title_and_seed(slug, region)")
s = s.replace("f'<img class=\"popular-img\" src=\"https://picsum.photos/seed/{seed}/80/80\" '", "f'<img class=\"popular-img\" src=\"{seed}\" '")
s = s.replace("seed = seed or '100000'", "")
p.write_text(s, encoding='utf-8')
print('patched add_popular_lists.py')
