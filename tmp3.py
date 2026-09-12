import urllib.request, re
req = urllib.request.Request('https://www.letsgojp.com/tokyo', headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
h = urllib.request.urlopen(req, timeout=40).read().decode('utf-8','ignore')
print('LEN', len(h))
m2 = re.findall(r'href=["\x27](https?://www\.letsgojp\.com/[^"\x27\s]*)["\x27]', h)
seen = []
for u in m2:
    if u not in seen:
        seen.append(u)
print(len(seen))
for u in seen[:40]:
    print(u)
