# -*- coding: utf-8 -*-
"""Fetch distinct cover images from Pixabay API so no two cards share a photo.
Populates pixel_cache.json (slug -> {url, width, height, pid, user, license}).
Resumable: skips slugs already in cache. Rate-limited with backoff."""
import json, os, re, time, urllib.parse, urllib.request, sys, glob, pathlib

KEY = '39894189-8822531df0830fb07f58a9a69'
BASE = pathlib.Path(__file__).parent
CACHE = BASE / 'pixel_cache.json'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) travel-guide-bot/1.0'}

# --- keyword map: slug -> pixabay search query (English, place-specific) ---
CITY = {
 'jp': {'tokyo':'Tokyo','kyoto':'Kyoto','osaka':'Osaka','nara':'Nara','hokkaido':'Hokkaido Sapporo',
        'sapporo':'Sapporo','okawa':'Okinawa','okinawa':'Okinawa','fukuoka':'Fukuoka','hiroshima':'Hiroshima',
        'kamakura':'Kamakura','kanazawa':'Kanazawa','takayama':'Takayama Gifu','takamatsu':'Takamatsu Kagawa',
        'awaji':'Awaji Island','tottori':'Tottori','himeji':'Himeji Castle','nikko':'Nikko Lake Chuzenji',
        'hakone':'Hakone Mt Fuji','yokohama':'Yokohama','matsumoto':'Matsumoto Castle','toyama':'Toyama',
        'shimane':'Shimane Mt Mijimayama','gifu':'Gifu Castle','nagoya':'Nagoya Castle','kobe':'Kobe Port',
        'akita':'Akita Mt Chausu','beppu':'Beppu Onsen','shizuoka':'Shizuoka Izu','mie':'Mie Mt Iide',
        'shiga':'Biwako Lake','shizuoka-izu':'Izu Shizuoka'},
 'kr': {'seoul':'Seoul','busan':'Busan','jeju':'Jeju Seongsan Ilchulbong','gwangju':'Gwangju',
        'daejeon':'Daejeon','incheon':'Incheon','bucheon':'Bucheon','gyeongju':'Gyeongju','gyeongbuk':'Gyeongju Bulguksa',
        'andong':'Andong Hahoe Village','gangneung':'Gangneung','pohang':'Pohang','ulsan':'Ulsan',
        'cheongju':'Cheongju','cheonan':'Cheonan'},
 'eu': {'paris':'Paris Eiffel Tower','london':'London Tower Bridge','rome':'Rome Colosseum','barcelona':'Barcelona Sagrada Familia',
        'amsterdam':'Amsterdam Canals','venice':'Venice Canals','munich':'Munich New Town Hall','berlin':'Berlin Brandenburg Gate',
        'lisbon':'Lisbon Tram','madrid':'Madrid Royal Palace','prague':'Prague Charles Bridge','vienna':'Vienna St Stephen Cathedral',
        'zrich':'Zurich','stuttgart':'Stuttgart','hamburg':'Hamburg Harbor','geneva':'Geneva Mont Blanc','lucerne':'Lucerne Chapel Bridge',
        'nice':'Nice Promenade','naples':'Naples Castel dell Ovo','salzburg':'Salzburg Fortress','florence':'Florence Duomo',
        'amalfi':'Amalfi Coast Positano','santorini':'Santorini Oia','athens':'Athens Acropolis','bruges':'Bruges Canal','gent':'Ghent Canal'},
 'tw': {'taipei':'Taipei 101','taoyuan':'Taoyuan','hsinchu':'Hsinchu','miaoli':'Miaoli','taichung':'Taichung',
        'gaoxiong':'Kaohsiung Love River','hualien':'Hualien Coast','yilan':'Yilan','kaiting':'Yilan','tancheng':'Yilan',
        'pingtung':'Pingtung','chiayi':'Chiayi','taichung-lan':'Lanli','taichung-chen':'Chenyu','yunlin':'Yunlin',
        'kaohsiung':'Kaohsiung','linch':'Lin','nantou':'Nantou'},
 'oce': {'sydney':'Sydney Opera House','melbourne':'Melbourne Flinders St','queenstown':'Queenstown New Zealand',
         'brisbane':'Brisbane Story Bridge','darwin':'Darwin Litchfield','canberra':'Canberra','perth':'Perth',
         'auckland':'Auckland Sky Tower','wellington':'Wellington','adelaide':'Adelaide Barossa','gold':'Gold Coast',
         'busan':'Busan','busselton':'Busselton','tasmania':'Tasmania Cradle Mountain','mel':'Melbourne','nsw':'Sydney Blue Mountains'},
}
GENERIC = {
 'jp':'Japan mountain temple','kr':'Korea hanok village','eu':'Europe medieval town','tw':'Taiwan countryside','oce':'Australia coast'
}

def slug_query(slug):
    parts = slug.split('-')
    region = parts[0]
    city = '-'.join(parts[1:]) if len(parts) > 1 else ''
    m = CITY.get(region, {})
    # longest prefix match
    for key in sorted(m, key=len, reverse=True):
        if city.startswith(key):
            return m[key]
    return GENERIC.get(region, region + ' travel landscape')

def load_cache():
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding='utf-8'))
    return {}

def save_cache(c):
    CACHE.write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding='utf-8')

def search_pixabay(query, tries=4):
    for i in range(tries):
        params = {'q': query, 'per_page': 20, 'image_type': 'photo', 'orientation': 'landscape'}
        url = 'https://pixabay.com/api/?key=%s&%s' % (KEY, urllib.parse.urlencode(params))
        try:
            req = urllib.request.Request(url, headers=UA)
            d = json.loads(urllib.request.urlopen(req, timeout=25).read())
            return d
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(2 + 2 * i)

def is_good(h):
    w, ht = h.get('imageWidth') or 0, h.get('imageHeight') or 0
    return w >= 800 and ht >= 500 and w > ht  # landscape

def pick_url(h):
    base = h.get('largeImageURL') or h.get('webformatURL') or h.get('mediumURL') or ''
    return base
    # standard pixabay direct pattern
    u = h.get('largeImageURL') or h.get('webformatURL') or ''
    return u

def main(limit=None):
    cache = load_cache()
    existing_pids = {v.get('pid') for v in cache.values() if v.get('pid')}
    slugs = []
    for f in sorted(glob.glob('articles/*.html')):
        s = os.path.basename(f)[:-5]
        if s in ('index',) or s in ('jp','kr','eu','tw','oce'):
            continue
        slugs.append(s)
    todo = [s for s in slugs if s not in cache]
    if limit:
        todo = todo[:limit]
    print('total slugs', len(slugs), '| cached', len(slugs) - len([s for s in slugs if s not in cache]), '| todo', len(todo), flush=True)
    i = 0
    for slug in todo:
        i += 1
        q = slug_query(slug)
        try:
            d = search_pixabay(q)
        except Exception as e:
            print('search fail', slug, q, str(e)[:60], flush=True)
            continue
        hits = [h for h in d.get('hits', []) if is_good(h)]
        if not hits:
            print('no hits', slug, q, flush=True)
            continue
        used = 0
        recs = []
        for h in hits:
            if h.get('id') in existing_pids:
                continue
            u = pick_url(h)
            if not u:
                continue
            recs.append({'url': u, 'pid': h['id'], 'width': h.get('imageWidth'), 'height': h.get('imageHeight'),
                         'user': h.get('user'), 'query': q, 'license': 'Pixabay Content License'})
            existing_pids.add(h['id'])
            if len(recs) >= 4:
                break
        # store: cover = recs[0], extra cards recs[1:]
        cache[slug] = recs[0] if recs else {'url': None, 'pid': None, 'query': q}
        if len(recs) > 1:
            for k, r in enumerate(recs[1:], 1):
                cache[slug + '__card%d' % k] = r
        save_cache(cache)
        if i % 10 == 0:
            print('progress', i, '/', len(todo), '| cache now', len([k for k in cache if not k.endswith('__card1')]), flush=True)
        time.sleep(0.6)
    print('DONE. cache entries:', len(cache), flush=True)

if __name__ == '__main__':
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    main(lim)


