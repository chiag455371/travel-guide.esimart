# -*- coding: utf-8 -*-
"""Replace all broken Unsplash URLs with working loremflickr URLs."""
import os, re, glob

BASE = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"
ARTICLES = BASE + r"\articles"

# Region-specific loremflickr mappings with lock IDs for consistency
# lock ID ensures same image appears every time
IMAGE_MAP = {
    # Japan
    "jp-tokyo": ("japan,tokyo", 6001),
    "jp-tokyo-tower": ("japan,tokyo,tower", 6002),
    "jp-tokyo-shibuya": ("japan,tokyo,shibuya", 6003),
    "jp-tokyo-asakusa": ("japan,tokyo,temple", 6004),
    "jp-tokyo-disney": ("japan,tokyo,disney", 6005),
    "jp-tokyo-harajuku": ("japan,tokyo,fashion", 6006),
    "jp-tokyo-skytree": ("japan,tokyo,skyline", 6007),
    "jp-tokyo-shinjuku": ("japan,tokyo,night", 6008),
    "jp-osaka": ("japan,osaka", 6009),
    "jp-osaka-doton": ("japan,osaka,food", 6010),
    "jp-osaka-usida": ("japan,osaka,castle", 6011),
    "jp-fuji-hiking": ("japan,fti,mountain", 6012),
    "jp-hakone-onsen": ("japan,onsen,hot spring", 6013),
    "jp-hokkaido-onsen": ("japan,hokkaido,onsen", 6014),
    "jp-hokkaido-snow": ("japan,hokkaido,snow", 6015),
    "jp-sapporo": ("japan,sapporo", 6016),
    "jp-nara": ("japan,nara,deer", 6017),
    "jp-nara-deer": ("japan,nara,deer,park", 6018),
    "jp-nara-kofukuji": ("japan,nara,temple", 6019),
    "jp-kyoto": ("japan,kyoto", 6020),
    "jp-kyoto-fushimi": ("japan,kyoto,inari", 6021),
    "jp-kyoto-arashiyama": ("japan,kyoto,bamboo", 6022),
    "jp-kyoto-kinkakuji": ("japan,kyoto,temple", 6023),
    "jp-kyoto-sannenzaka": ("japan,kyoto,street", 6024),
    "jp-nikko": ("japan,nikko,shrine", 6025),
    "jp-nikko-tobu": ("japan,nikko,torii", 6026),
    "jp-kanazawa": ("japan,kanazawa", 6027),
    "jp-kamakura": ("japan,kamakura,buddha", 6028),
    "jp-fukuoka": ("japan,fukuoka", 6029),
    "jp-hiroshima": ("japan,hiroshima", 6030),
    "jp-hiroshima-itsukushima": ("japan,hiroshima,torii", 6031),
    "jp-hiroshima-okunoshima": ("japan,hiroshima,island", 6032),
    "jp-okinawa": ("japan,okinawa,beach", 6033),
    "jp-okinawa-miyako": ("japan,okinawa,coral", 6034),
    "jp-kochi": ("japan,kochi", 6035),
    "jp-kiso-valley": ("japan,kiso,valley", 6036),
    "jp-sapporo-tv": ("japan,sapporo,tv tower", 6037),
    "jp-osaka-usida": ("japan,osaka,usida", 6038),
    # Korea
    "kr-seoul": ("korea,seoul", 7001),
    "kr-seoul-naksan": ("korea,seoul,namsan", 7002),
    "kr-seoul-mydong": ("korea,seoul,shopping", 7003),
    "kr-seoul-deoksugung": ("korea,seoul,palace", 7004),
    "kr-bukchon": ("korea,hanok,village", 7005),
    "kr-gwangjang": ("korea,market,food", 7006),
    "kr-busan": ("korea,busan", 7007),
    "kr-busan-haeundae": ("korea,busan,beach", 7008),
    "kr-jeju": ("korea,jeju", 7009),
    "kr-jeju-hallasan": ("korea,jeju,volcano", 7010),
    "kr-jeju-cafe": ("korea,cafe,jeju", 7011),
    "kr-jeju-city": ("korea,jeju,city", 7012),
    "kr-jeju-jungmun": ("korea,jeju,sea", 7013),
    "kr-gyeongju": ("korea,gyeongju", 7014),
    "kr-bucheon": ("korea,bucheon", 7015),
    # Taiwan
    "tw-taipei": ("taiwan,taipei", 8001),
    "tw-taipei-101": ("taiwan,taipei,101", 8002),
    "tw-taipei-cafe": ("taiwan,taipei,cafe", 8003),
    "tw-kaohsiung": ("taiwan,kaohsiung", 8004),
    "tw-kaohsiung-food": ("taiwan,food,night market", 8005),
    "tw-kaohsiung-night": ("taiwan,kaohsiung,night", 8006),
    "tw-tainan": ("taiwan,tainan", 8007),
    "tw-tainan-old": ("taiwan,tainan,old street", 8008),
    "tw-taichung": ("taiwan,taichung", 8009),
    "tw-taichung-farm": ("taiwan,taichung,farm", 8010),
    "tw-pinchia": ("taiwan,night market,fengchia", 8011),
    "tw-yilan": ("taiwan,yilan", 8012),
    "tw-yangmingshan": ("taiwan,yangmingshan", 8013),
    "tw-nan-tou": ("taiwan,nantou", 8014),
    "tw-nantou-clear": ("taiwan,nantou,lake", 8015),
    "tw-nantou-lalu": ("taiwan,nantou,lantern", 8016),
    "tw-chiayi": ("taiwan,chiayi", 8017),
    "tw-hualien": ("taiwan,hualien", 8018),
    "tw-taitung": ("taiwan,taitung", 8019),
    "tw-taitung-sea": ("taiwan,taitung,sea", 8020),
    "tw-lanyu": ("taiwan,lanyu,orchid", 8021),
    "tw-luye": ("taiwan,luye,balloon", 8022),
    "tw-luye-balloon": ("taiwan,luye,balloon", 8023),
    "tw-gaomei": ("taiwan,gateway sunset", 8024),
    "tw-gaomei-sunset": ("taiwan,gateway sunset", 8025),
    "tw-masp": ("taiwan,maleshe,old street", 8026),
    "tw-miaoli": ("taiwan,miaoli", 8027),
    "tw-nyasan": ("taiwan,nyasan", 8028),
    "tw-pu-lu": ("taiwan,puluo", 8029),
    "tw-sanyi": ("taiwan,sanyi", 8030),
    "tw-sanyi-crape": ("taiwan,sanyi,crape myrtle", 8031),
    "tw-shilin": ("taiwan,shilin,night market", 8032),
    "tw-shilin-night": ("taiwan,shilin,night", 8033),
    "tw-shilin-old": ("taiwan,shilin,old street", 8034),
    "tw-pingtung": ("taiwan,pingtung", 8035),
    "tw-pingtung-ranch": ("taiwan,pingtung,ranch", 8036),
    "tw-pingtung-orchid": ("taiwan,orchid,island", 8037),
    "tw-taruco": ("taiwan,taroko", 8038),
    "tw-tri-culture": ("taiwan,triangle,culture", 8039),
    "tw-ari-san-rail": ("taiwan,arysan,rail", 8040),
    # Europe
    "eu-paris": ("paris,eiffel tower", 9001),
    "eu-london": ("london,big ben", 9002),
    "eu-london-british": ("london,british museum", 9003),
    "eu-london-covent": ("london,covent garden", 9004),
    "eu-rome": ("rome,colosseum", 9005),
    "eu-rome-colosseum": ("rome,italy,colosseum", 9006),
    "eu-barcelona": ("barcelona,sagrada familia", 9007),
    "eu-amsterdam": ("amsterdam,canal", 9008),
    "eu-amsterdam-canals": ("amsterdam,netherlands canal", 9009),
    "eu-berlin": ("berlin,germany", 9010),
    "eu-berlin-wall": ("berlin,wall,memorial", 9011),
    # Oceania
    "oce-sydney": ("sydney,australia opera house", 10001),
    "oce-mel": ("melbourne,australia", 10002),
}

# Fallback by region for uncategorized
REGION_FALLBACK = {
    "jp": "japan",
    "kr": "korea",
    "tw": "taiwan",
    "eu": "europe,paris",
    "oce": "australia,sydney",
}

def get_region(fn):
    if fn.startswith("jp-"): return "jp"
    if fn.startswith("kr-"): return "kr"
    if fn.startswith("tw-"): return "tw"
    if fn.startswith("eu-"): return "eu"
    if fn.startswith("oce-"): return "oce"
    return None

def make_loremflickr(keyword, lock_id, size="600x400"):
    """Create a loremflickr URL with specific lock ID."""
    # Clean keyword: replace spaces with +, remove special chars
    kw = keyword.replace(" ", "+")
    # Remove any non-alphanumeric except +
    kw = re.sub(r"[^a-zA-Z0-9+]", "", kw)
    return f"https://loremflickr.com/{size}/{kw}?lock={lock_id}"

def make_loremflickr_1200(keyword, lock_id):
    return f"https://loremflickr.com/1200/630/{keyword.replace(' ','+')}?lock={lock_id}"

def fix_file(filepath, is_index=False):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    filename = os.path.basename(filepath)
    region = get_region(filename) if not is_index else None
    
    # Determine default fallback image
    if is_index:
        default_kw = "travel,passport,airport"
        default_lock = 9999
    elif region and region in REGION_FALLBACK:
        parts = REGION_FALLBACK[region].split(",")
        default_kw = parts[0]
        default_lock = 8888 if region == "jp" else 7777 if region == "kr" else 6666 if region == "tw" else 5555
    else:
        default_kw = "travel"
        default_lock = 9999
    
    changed = False
    
    # First, try to match specific article/region mappings
    matched_keys = []
    for key in IMAGE_MAP:
        if key in filename or (is_index and key.replace("-","") in filename.replace("-","")):
            matched_keys.append(key)
    
    # For index pages, match by region flag in card hrefs
    if is_index:
        for key, (kw, lock) in IMAGE_MAP.items():
            # Check if this key appears in the file content
            if key in content:
                thumb = make_loremflickr(kw, lock, "600x400")
                full = make_loremflickr(kw, lock, "1200x630")
                # Find and replace loremflickr URLs that match the pattern
                # We look for the old broken unsplash or loremflickr URLs
                # Since we don't know the exact old URLs, replace by position
                # Actually, let's just find all loremflickr/unsplash URLs and replace systematically
                pass
    
    # Generic approach: replace all broken image URLs
    # Pattern 1: https://images.unsplash.com/photo-XXXX-XXXX?w=... (broken ones)
    # Pattern 2: https://loremflickr.com/... (old ones with Chinese keywords)
    
    # Step 1: Replace all Unsplash photo URLs with loremflickr fallbacks based on region
    def replace_unsplash(m):
        nonlocal changed
        url = m.group(0)
        if region and region in REGION_FALLBACK:
            parts = REGION_FALLBACK[region].split(",")
            kw = parts[0]
            lock = 8888 if region == "jp" else 7777 if region == "kr" else 6666 if region == "tw" else 5555
            if "1200/630" in url:
                return make_loremflickr_1200(kw, lock)
            else:
                return make_loremflickr(kw, lock, "600x400")
        return url
    
    new_content = re.sub(r"https://images\.unsplash\.com/photo-[\w-]+\?w=\d+&h=\d+&fit=crop", replace_unsplash, content)
    if new_content != content:
        changed = True
        content = new_content
    
    # Step 2: Replace any remaining loremflickr with broken Chinese keywords
    # These are the old ones that had spaces in keywords
    def fix_old_lorem(m):
        nonlocal changed
        url = m.group(0)
        # Extract the keyword part
        match = re.search(r"loremflickr\.com/\d+/\d+/([^?]+)", url)
        if match:
            kw = match.group(1)
            # If keyword has Chinese chars or weird formatting, replace with region default
            if any(ord(c) > 127 for c in kw) or "+" in kw:
                if region and region in REGION_FALLBACK:
                    parts = REGION_FALLBACK[region].split(",")
                    kw_clean = parts[0]
                    lock = 8888 if region == "jp" else 7777 if region == "kr" else 6666 if region == "tw" else 5555
                    if "1200/630" in url:
                        return make_loremflickr_1200(kw_clean, lock)
                    else:
                        return make_loremflickr(kw_clean, lock, "600x400")
        return url
    
    new_content = re.sub(r"https://loremflickr\.com/\d+/\d+/[^?\s\"'\x3c\x3e]+", fix_old_lorem, content)
    if new_content != content:
        changed = True
        content = new_content
    
    # Step 3: Catch-all - replace any remaining broken image URLs
    def catch_all_replace(m):
        nonlocal changed
        url = m.group(0)
        if region:
            parts = REGION_FALLBACK.get(region, ["travel"]).split(",")
            kw = parts[0]
            lock = 8888 if region == "jp" else 7777 if region == "kr" else 6666 if region == "tw" else 5555
            if "1200/630" in url or "600/400" not in url:
                return make_loremflickr_1200(kw, lock)
            else:
                return make_loremflickr(kw, lock, "600x400")
        return url
    
    new_content = re.sub(r"https://loremflickr\.com/\d+/\d+/\S+", catch_all_replace, content)
    if new_content != content:
        changed = True
        content = new_content
    
    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

print("=== Fixing all image URLs ===")
files_fixed = 0

# Fix all articles
for fn in sorted(os.listdir(ARTICLES)):
    if not fn.endswith(".html") or fn == "index.html":
        continue
    fp = os.path.join(ARTICLES, fn)
    if fix_file(fp):
        files_fixed += 1
        print(f"  FIXED: {fn}")

# Fix index pages
for idx in ["index.html", "articles/index.html"]:
    fp = os.path.join(BASE, idx)
    if os.path.exists(fp):
        if fix_file(fp, is_index=True):
            files_fixed += 1
            print(f"  FIXED INDEX: {idx}")

print(f"\nTotal files fixed: {files_fixed}")

# Verify no broken URLs remain
print("\n=== Verification ===")
import urllib.request, ssl
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

all_urls = set()
for root, dirs, files in os.walk(BASE):
    # Skip node_modules and .git
    dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
    for fn in files:
        if not fn.endswith(".html"): continue
        fp = os.path.join(root, fn)
        with open(fp, "r", encoding="utf-8") as f:
            c = f.read()
        for m in re.finditer(r"https://loremflickr\.com/\d+/\d+/[^\s\"'\x3c\x3e]+", c):
            all_urls.add(m.group())
        for m in re.finditer(r"https://images\.unsplash\.com/photo-[\w-]+\?[^\s\"'\x3c\x3e]+", c):
            all_urls.add(m.group())

print(f"Total image URLs: {len(all_urls)}")
broken = 0
for url in sorted(all_urls):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=8, context=ssl_ctx)
        if resp.status != 200 and resp.status != 302:
            print(f"  NON-200 [{resp.status}]: {url[:70]}")
            broken += 1
    except Exception as e:
        print(f"  ERROR: {url[:70]} - {type(e).__name__}")
        broken += 1

print(f"\nResult: {'ALL OK' if broken == 0 else f'{broken} issues found'}")
