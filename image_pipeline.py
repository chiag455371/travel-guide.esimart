# -*- coding: utf-8 -*-
"""圖片管道 v2: 用 Wikimedia Commons 搜尋真實景點照,替換 picsum
- 批次搜尋,快取結果
- 替換所有 picsum 引用(封面 600/400、卡片 80/80、og:image)
"""
import json, os, re, glob, sys, time, urllib.request, urllib.parse

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

CITY_KEYWORDS = {
    # 日本
    'tokyo': ['Tokyo Tower', 'Shibuya Crossing', 'Senso-ji Temple'],
    'kyoto': ['Fushimi Inari', 'Bamboo Grove Arashiyama', 'Kinkaku-ji'],
    'osaka': ['Dotonbori', 'Osaka Castle', 'Shinsekai'],
    'sapporo': ['Sapporo Snow Festival', 'Sapporo Beer Hall'],
    'hokkaido': ['Lake Toya', 'Rusutsu', 'Furano Lavender'],
    'hiroshima': ['Miyajima Shrine', 'Itsukushima', 'Hiroshima Peace Memorial'],
    'fukuoka': ['Yatai', 'Ohori Park', 'Hakata'],
    'kamakura': ['Great Buddha Kamakura', 'Hase-dera'],
    'nara': ['Nara Deer Park', 'Todai-ji Temple'],
    'kanazawa': ['Kenroku-en', 'Kanazawa Castle'],
    'takayama': ['Takayama Jinya', 'Hida Beef'],
    'matsuyama': ['Matsuyama Castle', 'Dogo Hot Spring'],
    'shizuoka': ['Mount Fuji', 'Atami'],
    'miyajima': ['Miyajima Shrine', 'Miyajima Island'],
    'kobe': ['Kobe Harbor', 'Kobe Port Tower'],
    'kagoshima': ['Kagoshima Sakurajima', 'Kagoshima Castle'],
    'kiso': ['Kiso Valley', 'Karuizawa Japan'],
    'himeji': ['Himeji Castle', 'Himeji Japan'],
    'kochi': ['Kochi Castle', 'Kochi Japan'],
    'kurashiki': ['Kurashiki Canal', 'Kurashiki Japan'],
    'nagano': ['Nagano Japan', 'Nagano Snow'],
    'miyagi': ['Miyagi Japan', 'Miyagi Sendai'],
    'akita': ['Akita Japan', 'Akita Kanto'],
    'aomori': ['Aomori Japan', 'Aomori Nebuta'],
    'awaji': ['Awaji Island', 'Awaji Japan'],
    'fuji': ['Mount Fuji', 'Fuji Japan'],
    'nagasaki': ['Nagasaki Peace', 'Nagasaki Japan'],
    'naoshima': ['Naoshima Island', 'Naoshima Art'],
    'nikko': ['Nikko Japan', 'Nikko Shrine'],
    'okayama': ['Okayama Japan', 'Okayama Crowd'],
    'okinawa': ['Okinawa Beach', 'Okinawa Churaumi'],
    'oshu': ['Oshu Fujiwara', 'Oshu Hiraizumi'],
    'sendai': ['Sendai Japan', 'Sendai Miyagi'],
    'shikoku': ['Shikoku Temple', 'Shikoku Japan'],
    'shiretoko': ['Shiretoko Peninsula', 'Shiretoko Hokkaido'],
    'takada': ['Takada Castle', 'Takada Japan'],
    'takamatsu': ['Takamatsu Japan', 'Takamatsu Garden'],
    'tohoku': ['Tohoku Onsen', 'Tohoku Japan'],
    'tottori': ['Tottori Sand Dunes', 'Tottori Japan'],
    'ushiku': ['Ushiku Daibutsu', 'Ushiku Japan'],
    'oyama': ['Oyama Shrine', 'Oyama Tokyo'],
    # 韓國
    'seoul': ['Gyeongbokgung', 'Changdeokgung', 'Namsan Tower', 'Myeongdong', 'Bukchon', 'Cheonggyecheon'],
    'busan': ['Gamcheon', 'Haeundae Beach', 'Gwangan Bridge'],
    'jeju': ['Hallasan', 'Jeju Olle', 'Jeju Black Beach', 'Jeju Caves'],
    'gyeongju': ['Bulguksa', 'Gyeongju'],
    'bucheon': ['Bucheon Korea', 'Bucheon Train'],
    'buchon': ['Bucheon Korea', 'Bucheon Train'],
    'bukchon': ['Bukchon Seochon', 'Seoul Bukchon'],
    'chuncheon': ['Chuncheon Korea', 'Chuncheon Lake'],
    'dongbaek': ['Dongbaek Island', 'Dongbaek Korea'],
    'gangnam': ['Gangnam Korea', 'Gangnam Seoul'],
    'gimje': ['Gimje Bulsa', 'Gimje Korea'],
    'gwangjang': ['Gwangjang Market', 'Seoul Gwangjang'],
    'gwangju': ['Gwangju Korea', 'Gwangju Hanok'],
    'jeonju': ['Jeonju Hanok', 'Jeonju Bibimbap'],
    'namsan': ['Namsan Tower', 'Seoul Namsan'],
    'pocha': ['Pocha Street', 'Seoul Pocha'],
    'poji': ['Poji Korea', 'Poji History'],
    'sokcho': ['Sokcho Korea', 'Sokcho Beach'],
    'suwon': ['Suwon Hwaseong', 'Suwon Korea'],
    'ulsan': ['Ulsan Dongmi', 'Ulsan Korea'],
    'yeosu': ['Yeosu Korea', 'Yeosu Flower'],
    'autumn': ['Korea Autumn', 'Fall Korea'],
    'spring': ['Korea Spring', 'Cherry Korea'],
    'andong': ['Andong Samgyeop', 'Andong Korea'],
    # 歐洲
    'paris': ['Eiffel Tower', 'Louvre', 'Montmartre', 'Notre-Dame'],
    'london': ['Big Ben', 'Buckingham Palace', 'British Museum', 'London Eye'],
    'barcelona': ['Sagrada Familia', 'Park Guell', 'Las Ramblas'],
    'amsterdam': ['Amsterdam Canals', 'Rijksmuseum', 'Vondelpark'],
    'brussels': ['Grand Place Brussels', 'Manneken Pis'],
    'lisbon': ['Lisbon Tram 28', 'Belem Tower', 'Lisbon Castle'],
    'rome': ['Colosseum', 'Vatican', 'Trevi Fountain', 'Pantheon'],
    'florence': ['Duomo Florence', 'Uffizi', 'Ponte Vecchio'],
    'venice': ["St. Mark's Square", 'Gondola', 'Venice Canal'],
    'prague': ['Charles Bridge', 'Prague Castle', 'Old Town Prague'],
    'berlin': ['Brandenburg Gate', 'East Side Gallery', 'Reichstag'],
    'munich': ['Marienplatz', 'Neuschwanstein', 'Munich Castle'],
    'athens': ['Acropolis', 'Athens Greece', 'Parthenon'],
    'bern': ['Bern Switzerland', 'Bern Old Town'],
    'copenhagen': ['Copenhagen Denmark', 'Copenhagen Harbor'],
    'edinburgh': ['Edinburgh Castle', 'Edinburgh Scotland'],
    'flanders': ['Flanders Belgium', 'Bruges Belgium'],
    'bruges': ['Bruges Belgium', 'Bruges Canal'],
    'budapest': ['Budapest Hungary', 'Budapest Castle'],
    'iceland': ['Iceland Waterfall', 'Iceland Glacier'],
    'ireland': ['Ireland Cliffs', 'Ireland Dublin'],
    'lubljana': ['Ljubljana Slovenia', 'Ljubljana Castle'],
    'lucerne': ['Lucerne Switzerland', 'Lucerne Chapel'],
    'milan': ['Duomo Milan', 'Milan Italy'],
    'norway': ['Norway Fjord', 'Norway Waterfall'],
    'porto': ['Porto Portugal', 'Porto Bridge'],
    'rhine': ['Rhine River', 'Rhine Castle'],
    'santorini': ['Santorini Greece', 'Santorini Blue'],
    'swiss': ['Swiss Alps', 'Swiss Mountain'],
    'alps': ['Swiss Alps', 'Swiss Mountain'],
    'tuscany': ['Tuscany Italy', 'Tuscany Hills'],
    'vienna': ['Vienna Austria', 'Vienna Castle'],
    'vilnius': ['Vilnius Old Town', 'Vilnius Lithuania'],
    'zurich': ['Zurich Switzerland', 'Zurich Lake'],
    'amalfi': ['Amalfi Coast', 'Sorrento Italy'],
    'holland': ['Holland Tulip', 'Netherlands Tulip'],
    # 澳洲
    'sydney': ['Sydney Opera House', 'Sydney Harbour Bridge', 'Bondi Beach'],
    'melbourne': ['Melbourne Lanes', 'Royal Botanic Gardens Melbourne'],
    'queenstown': ['Queenstown Lake', 'Milford Sound'],
    'perth': ['Perth Kangaroo', 'Perth Swan'],
    'adelaide': ['Adelaide Barossa', 'Adelaide Hills'],
    'canberra': ['Canberra Parliament', 'Canberra Australia'],
    'darwin': ['Darwin Australia', 'Darwin Kakadu'],
    'kangaroo': ['Kangaroo Island', 'Kangaroo Australia'],
    'christchurch': ['Christchurch New Zealand', 'Christchurch Botanic'],
    'curling': ['Curling New Zealand', 'Curling Sport'],
    'mel': ['Melbourne Lanes', 'Melbourne Arts'],
    'sunshine': ['Sunshine Coast Australia', 'Sunshine Coast Beach'],
    'tasmania': ['Tasmania Fox', 'Tasmania Australia'],
    'whakaari': ['Whakaari White Island', 'Whakaari Geothermal'],
    'roto': ['Rotorua New Zealand', 'Rotorua Geothermal'],
    'wellington': ['Wellington New Zealand', 'Wellington Museum'],
    'auckland': ['Auckland New Zealand', 'Auckland Rangitoto'],
    'hobart': ['Hobart Tasmania', 'Hobart Market'],
    # 台灣
    'taipei': ['Taipei 101', 'Ximending', 'Shilin Night', 'Yangmingshan'],
    'kaohsiung': ['Kaohsiung Love River', 'Kaohsiung Fish'],
    'tainan': ['Tainan Old', 'Tainan Night'],
    'hualien': ['Hualien Coast', 'Hualien Beach'],
    'chiayi': ['Chiayi Pine', 'Chiayi Coffee'],
    'yilan': ['Yilan Hot', 'Yilan Beach'],
    'taitung': ['Taitung Hot', 'Taitung Sea'],
    'penghu': ['Penghu Island', 'Penghu Bridge'],
    'kinmen': ['Kinmen War', 'Kinmen Park'],
    'matsu': ['Matsu Island', 'Matsu Beach'],
    'nantou': ['Nantou Taiwan', 'Nantou Clear'],
    'yehliu': ['Yehliu Geopark', 'Yehliu Taiwan'],
    'lantou': ['Lantou Taiwan', 'Lantou Clear'],
    'puli': ['Puli Hot Spring', 'Puli Taiwan'],
    'pu': ['Pu Village', 'Pu Taiwan'],
    'pu-lu': ['Pu Village', 'Pu Taiwan'],
    'jiji': ['Jiji Brook', 'Jiji Snake'],
    'gaomei': ['Gaomei Sunset', 'Gaomei Lake'],
    'pingtung': ['Penglai Orchid', 'Penglai Ranch'],
    'ari': ['Ari San Railway', 'Ari Taiwan'],
    'chia': ['Chia Yi Food', 'Chia Yi Taiwan'],
    'chieh': ['Chieh Lan', 'Chieh Taiwan'],
    'dadaocheng': ['Dadaocheng Coffee', 'Dadaocheng Taiwan'],
    'genghis': ['Genghis Khan', 'Genghis Food'],
    'guanxi': ['Guanxi Rice', 'Guanxi Taiwan'],
    'hengchun': ['Hengchun Kerama', 'Hengchun Strait'],
    'hsinchu': ['Hsinchu Bamboo', 'Hsinchu Taiwan'],
    'jiufen': ['Jiufen Night Lantern', 'Jiufen A-Song'],
    'kiang': ['Kiang Village', 'Kiang Taiwan'],
    'kiunghua': ['Kiunghua Village', 'Kiunghua Taiwan'],
    'lanyu': ['Lanyu Island', 'Lanyu Taiwan'],
    'liuqiu': ['Liuqiu Penguin', 'Liuqiu Island'],
    'luceat': ['Luceat Village', 'Luceat Taiwan'],
    'lukang': ['Lukang Temple', 'Lukang History'],
    'luku': ['Luku Geopark', 'Luku Taiwan'],
    'luye': ['Luye Balloon', 'Luye Taiwan'],
    'masp': ['Masp Village', 'Masp Taiwan'],
    'mazu': ['Mazu Beibing', 'Mazu Islet'],
    'miaoli': ['Miaoli Bamboo', 'Miaoli Taiwan'],
    'nan': ['Nan Village', 'Nan Taiwan'],
    'north': ['North Kimberley', 'North Coast'],
    'nyasan': ['Nyasan Mountain', 'Nyasan Taiwan'],
    'pacific': ['Pacific Coast', 'Pacific Coast Taiwan'],
    'pincha': ['Pincha Village', 'Pincha Taiwan'],
    'sanyi': ['Sanyi Crape', 'Sanyi Culture'],
    'shilin': ['Shilin Night', 'Shilin Old'],
    'silver': ['Silver Nitrate', 'Silver Taiwan'],
    'taichung': ['Taichung Farm', 'Taichung Taiwan'],
    'taruco': ['Taruc Village', 'Taruc Taiwan'],
    'tri': ['Tri Culture', 'Tri Village'],
    'yangming': ['Yangming Shuang', 'Yangmingshan'],
    'yangmingshan': ['Yangmingshan', 'Yangmingshan Park'],
}

CACHE_FILE = "image_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)

def extract_city(slug):
    """從 slug 判斷城市(檢查全文)"""
    for key in CITY_KEYWORDS:
        if key in slug:
            return key
    return None

def search_wikimedia(query):
    api = "https://commons.wikimedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'generator': 'search',
        'gsrsearch': f"filetype:bitmap {query}",
        'gsrnamespace': '6',
        'gsrlimit': '5',
        'prop': 'imageinfo',
        'iiprop': 'url|extmetadata',
        'iiurlwidth': '800'
    }
    url = api + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (TravelGuideBot)"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.load(r)
    
    images = []
    if 'query' in data and 'pages' in data['query']:
        for page in data['query']['pages'].values():
            if 'imageinfo' in page:
                info = page['imageinfo'][0]
                if 'thumburl' in info:
                    license = info.get('extmetadata', {}).get('LicenseShortName', {}).get('value', 'Unknown')
                    artist = info.get('extmetadata', {}).get('Artist', {}).get('value', 'Unknown')
                    images.append({
                        'url': info['url'],
                        'thumb': info['thumburl'],
                        'license': license,
                        'artist': artist,
                        'query': query
                    })
    return images

def get_images_for_article(slug, cache, verbose=True):
    cache_key = f"{slug}"
    if cache_key in cache and cache[cache_key].get('thumb'):
        return cache[cache_key]
    
    city = extract_city(slug)
    if not city:
        if verbose:
            print(f"  {slug}: no city, skip")
        return None
    
    terms = CITY_KEYWORDS.get(city, [])
    if not terms:
        if verbose:
            print(f"  {slug}: no terms, skip")
        return None
    
    for term in terms:
        try:
            images = search_wikimedia(term)
            if images:
                result = {
                    'url': images[0]['url'],
                    'thumb': images[0]['thumb'],
                    'license': images[0]['license'],
                    'artist': images[0]['artist'],
                    'query': term
                }
                cache[cache_key] = result
                if verbose:
                    print(f"  OK {slug} -> {term} ({result['license'][:15]})")
                return result
        except Exception as e:
            err = str(e)
            if '429' in err or 'Too Many' in err:
                if verbose:
                    print(f"  {slug}: 429, backoff 15s")
                time.sleep(15)
                continue
            else:
                if verbose:
                    print(f"  {slug}: {term} failed: {e}")
                time.sleep(1)
                continue
    
    if verbose:
        print(f"  FAIL {slug}: no image")
    return None

def replace_picsum(content, thumb_url):
    content = re.sub(r'https://picsum\.photos/seed/\d+/80/80', thumb_url, content)
    content = re.sub(r'https://picsum\.photos/seed/\d+/600/400', thumb_url, content)
    content = re.sub(r'https://picsum\.photos/seed/\d+', thumb_url, content)
    return content

def main():
    cache = load_cache()
    print("=== Image Pipeline v2: real landmark photos ===\n")
    
    articles = sorted(glob.glob('articles/*.html'))
    print(f"Total: {len(articles)}\n")
    
    processed = 0
    skipped = 0
    failed = 0
    
    for i, f in enumerate(articles):
        slug = os.path.basename(f)[:-5]
        c = open(f, encoding='utf-8').read()
        
        if 'picsum.photos' not in c:
            skipped += 1
            continue
        
        result = get_images_for_article(slug, cache, verbose=(i < 20 or i % 50 == 0))
        
        if result:
            new_c = replace_picsum(c, result['thumb'])
            open(f, 'w', encoding='utf-8').write(new_c)
            processed += 1
        else:
            failed += 1
        
        if (i + 1) % 50 == 0:
            save_cache(cache)
            print(f"Progress: {i+1}/{len(articles)}, processed {processed}, failed {failed}")
    
    save_cache(cache)
    print(f"\nDone: processed {processed}, failed {failed}, skipped {skipped}/{len(articles)}")

if __name__ == '__main__':
    main()
