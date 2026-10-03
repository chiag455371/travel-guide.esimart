import os, json, urllib.request, re, sys, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
apikey = 'gZOdbOKSx0urxyPaUGFxG6cRipjhl6WDUU7fdwkRHAlY8jGes2x3qVau'
cache_file = 'pexels_cache.json'
cache = {}
if os.path.exists(cache_file):
    with open(cache_file, 'r', encoding='utf-8') as f:
        cache = json.load(f)
print('loaded:', len(cache))

def get_pexels(kw):
    if kw in cache: return cache[kw]
    u='https://api.pexels.com/v1/search?query='+urllib.parse.quote(kw)+'&per_page=1'
    try:
        r=urllib.request.Request(u,headers={'Authorization':apikey})
        with urllib.request.urlopen(r,timeout=10) as resp:
            d=json.loads(resp.read())
            if d.get('photos'):
                img=d['photos'][0]['src']['large']; cache[kw]=img; return img
    except Exception as e:
        print(f'ERR {kw}: {e}',file=sys.stderr)
    return None
