# -*- coding: utf-8 -*-
import re

BASE = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"

# Fix articles/index.html
fpath = BASE + r"\articles\index.html"
with open(fpath, 'r', encoding='utf-8') as f:
    c = f.read()

repls = {
    "fuji,mount,,japan": "https://images.unsplash.com/photo-1490806843957-31ef8fe7c526?w=600&h=400&fit=crop",
    "japan+ramen+street": "https://images.unsplash.com/photo-1590559844485-8d60b2e5c8e8?w=600&h=400&fit=crop",
    "hakone,onsen,japan": "https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=600&h=400&fit=crop",
    "hokkaido,snow,ski,japan": "https://images.unsplash.com/photo-1516483638261-f4dbaf036963?w=600&h=400&fit=crop",
    "kyoto,fushimi,inari,japan": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=600&h=400&fit=crop",
    "nara,deer,japan,temple": "https://images.unsplash.com/photo-1545569368-b94b46e177a5?w=600&h=400&fit=crop",
    "nikko,to-shogu,japan,unesco": "https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=600&h=400&fit=crop",
    "taipei,101+tower+taiwan": "https://images.unsplash.com/photo-1553812733-7c5cc5a75c57?w=600&h=400&fit=crop",
    "tainan,old+street+food+taiwan": "https://images.unsplash.com/photo-1553812733-7c5cc5a75c57?w=600&h=400&fit=crop",
    "yangmingshan,taipei+taiwan+volcano": "https://images.unsplash.com/photo-1553812733-7c5cc5a75c57?w=600&h=400&fit=crop",
    "paris,eiffel+tower+louvre+france": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=600&h=400&fit=crop",
    "london,big+ben+buckingham+uk": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=600&h=400&fit=crop",
    "rome,colosseum+vatican+italy": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=600&h=400&fit=crop",
    "amsterdam,canal+museum+netherlands": "https://images.unsplash.com/photo-1534146789009-76ca50606c63?w=600&h=400&fit=crop",
    "barcelona,sagrada+familia+spain": "https://images.unsplash.com/photo-1583422409516-2895a77efded?w=600&h=400&fit=crop",
    "sydney,opera+house+australia": "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=600&h=400&fit=crop",
    "melbourne,australia+coffee+laneway": "https://images.unsplash.com/photo-1523482580672-f109ba8cb9be?w=600&h=400&fit=crop",
    "seoul+tower+night+city": "https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?w=600&h=400&fit=crop",
    "korea,street+food+market+bbq": "https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?w=600&h=400&fit=crop",
    "korea,hanok+village+traditional": "https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?w=600&h=400&fit=crop",
    "jeju,hallasan": "https://images.unsplash.com/photo-1570197571499-166b36495c?w=600&h=400&fit=crop",
    "taiwan,night+market+food+stall": "https://images.unsplash.com/photo-1553812733-7c5cc5a75c57?w=600&h=400&fit=crop",
    "taiwan,coast+beach+sunrise": "https://images.unsplash.com/photo-1553812733-7c5cc5a75c57?w=600&h=400&fit=crop",
    "taiwan,old+street+blue+alley": "https://images.unsplash.com/photo-1553812733-7c5cc5a75c57?w=600&h=400&fit=crop",
}
for k, v in repls.items():
    c = c.replace("loremflickr.com/600/400/" + k, v)
    c = c.replace("loremflickr.com/1200/630/" + k.replace("+", ","), v.replace("600/400", "1200/630"))
# Catch-all fallback
fallback_600 = "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=600&h=400&fit=crop"
fallback_1200 = "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=1200&h=630&fit=crop"
c = re.sub(r"https://loremflickr\.com/600/400/[^\s\"'<>]+", fallback_600, c)
c = re.sub(r"https://loremflickr\.com/1200/630/[^\s\"'<>]+", fallback_1200, c)
with open(fpath, "w", encoding="utf-8") as f:
    f.write(c)
print(f"Fixed articles/index.html: loremflickr={('loremflickr' in c)}")

# Fix main index.html
fpath2 = BASE + r"\index.html"
with open(fpath2, "r", encoding="utf-8") as f:
    c2 = f.read()
repls2 = {
    "travel,passport airport": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=1200&h=630&fit=crop",
    "tokyo,japan+skyline+tower": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=600&h=400&fit=crop",
    "japan,ramen+street+food+night": "https://images.unsplash.com/photo-1590559844485-8d60b2e5c8e8?w=600&h=400&fit=crop",
    "japan,temple+ancient+zen+garden": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=600&h=400&fit=crop",
    "japan,deer+park+ancient+temple": "https://images.unsplash.com/photo-1545569368-b94b46e177a5?w=600&h=400&fit=crop",
    "japan,osaka+street+food+neon": "https://images.unsplash.com/photo-1590559844485-8d60b2e5c8e8?w=600&h=400&fit=crop",
    "korea,seoul+tower+night+city": "https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?w=600&h=400&fit=crop",
    "korea,street+food+market+bbq": "https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?w=600&h=400&fit=crop",
    "korea,hanok+village+traditional": "https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?w=600&h=400&fit=crop",
    "taiwan,night+market+food+stall": "https://images.unsplash.com/photo-1553812733-7c5cc5a75c57?w=600&h=400&fit=crop",
    "taiwan,coast+beach+sunrise": "https://images.unsplash.com/photo-1553812733-7c5cc5a75c57?w=600&h=400&fit=crop",
    "taiwan,old+street+blue+alley": "https://images.unsplash.com/photo-1553812733-7c5cc5a75c57?w=600&h=400&fit=crop",
    "paris,eiffel+tower+sunset": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=600&h=400&fit=crop",
    "melbourne,australia+coffee+laneway": "https://images.unsplash.com/photo-1523482580672-f109ba8cb9be?w=600&h=400&fit=crop",
}
for k, v in repls2.items():
    c2 = c2.replace("loremflickr.com/600/400/" + k, v)
    c2 = c2.replace("loremflickr.com/1200/630/" + k.replace("+", ","), v.replace("600/400", "1200/630"))
c2 = re.sub(r"https://loremflickr\.com/\d+/\d+/[^\s\"'<>]+", "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=600&h=400&fit=crop", c2)
with open(fpath2, "w", encoding="utf-8") as f:
    f.write(c2)
print(f"Fixed index.html: loremflickr={('loremflickr' in c2)}")
