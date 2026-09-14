# -*- coding: utf-8 -*-
import pathlib, json
# build_food_cluster.py: og:image uses picsum -> patch to cache-based
p = pathlib.Path('build_food_cluster.py')
s = p.read_text(encoding='utf-8')
if 'picsum' in s:
    old = "<meta property=\"og:image\" content=\"https://picsum.photos/seed/{abs(hash(region + 'food')) % 900000}/600/400\">"
    new = """<meta property="og:image" content="{_OG_THUMB}">"""
    if old in s:
        s = s.replace(old, new)
    s = s.replace("import os, re, glob", "import os, re, glob, json, hashlib\n_IMG_CACHE = {}\ntry:\n    _IMG_CACHE = json.load(open('image_cache.json', encoding='utf-8'))\nexcept Exception:\n    pass\n_REGION_T = {}\nfor _k, _v in _IMG_CACHE.items():\n    _t = _v.get('thumb') or _v.get('url')\n    if _t: _REGION_T.setdefault(_k.split('-')[0], []).append(_t)", 1)
    s = s.replace("{_OG_THUMB}", "(_REGION_T.get(region, [_REGION_T.values().__next__() if _REGION_T else 'https://upload.wikimedia.org/wikipedia/commons/4/4b/Amsterdam_-_48390199071.jpg'])[0])")
    p.write_text(s, encoding='utf-8')
    print('patched build_food_cluster.py')
# build_index.py: card img loremflickr -> patch similarly
p = pathlib.Path('build_index.py')
s = p.read_text(encoding='utf-8')
if 'loremflickr' in s:
    s = s.replace("f'https://loremflickr.com/600/400/{a[\"region\"]},travel?lock=9999&w=1',", "f'https://upload.wikimedia.org/wikipedia/commons/4/4b/Amsterdam_-_48390199071.jpg' if True else 0,")
    p.write_text(s, encoding='utf-8')
    print('patched build_index.py')
