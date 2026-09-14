# -*- coding: utf-8 -*-
import pathlib
p = pathlib.Path('generate_region_pages.py')
s = p.read_text(encoding='utf-8')

# 1) add cache load after REGIONS def (insert before 'def generate_region_page')
cache_code = '''_IMGCACHE = {}
try:
    import json
    _IMGCACHE = json.load(open(os.path.join(base, 'image_cache.json'), encoding='utf-8'))
except Exception:
    pass
_REGION_FB = {}
for _k, _v in _IMGCACHE.items():
    _REGION_FB.setdefault := None
'''
# simpler: build per-region fallback list
cache_code = '''_IMGCACHE = {}
try:
    import json
    _IMGCACHE = json.load(open(os.path.join(base, 'image_cache.json'), encoding='utf-8'))
except Exception:
    pass
_REGION_THUMBS = {}
for _k, _v in _IMGCACHE.items():
    _t = _v.get('thumb') or _v.get('url')
    if _t:
        _REGION_THUMBS.setdefault(_k.split('-')[0], []).append(_t)
'''
anchor = 'def generate_region_page(region_code):'
assert anchor in s, 'anchor missing'
s = s.replace(anchor, cache_code + anchor, 1)

# 2) replace loremflickr card img line
old = "        img_url = \"https://loremflickr.com/600/400/\" + info['keyword'] + \"?lock=\" + str(lock)"
assert old in s, 'card img line missing'
new = '''        _v = _IMGCACHE.get(slug) or _IMGCACHE.get(slug.rsplit('-', 1)[0]) or {}
        img_url = _v.get('thumb') or _v.get('url') or (_REGION_THUMBS.get(info['keyword'][:2] if False else slug.split('-')[0], [None])[0] or 'https://upload.wikimedia.org/wikipedia/commons/4/4b/Amsterdam_-_48390199071.jpg')'''
s = s.replace(old, new, 1)

# 3) replace og:image loremflickr
old2 = """    html += '  <meta property="og:image" content="https://loremflickr.com/1200/630/' + info['keyword'] + '?lock=9999">\\n'"""
assert old2 in s, 'og:image line missing'
new2 = """    _og = (_REGION_THUMBS.get(region_code, [None])[0]) or 'https://upload.wikimedia.org/wikipedia/commons/4/4b/Amsterdam_-_48390199071.jpg'
    html += '  <meta property="og:image" content="' + _og + '">\\n'"""
s = s.replace(old2, new2, 1)

p.write_text(s, encoding='utf-8')
print('patched generate_region_pages.py')
