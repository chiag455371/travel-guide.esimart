import urllib.request, re
req = urllib.request.Request('https://www.letsgojp.com/', headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
h = urllib.request.urlopen(req, timeout=40).read().decode('utf-8','ignore')
pat = r'href=["\x27]([^"\x27]*entry[^"\x27]*)["\x27]'
seen = []
for u in re.findall(pat, h):
    if u not in seen: seen.append(u)
print('entry-links:', len(seen))
for u in seen[:15]: print(u)
# also find article-like paths
pat2 = r'href=["\x27](/tokyo/[^"\x27]+|/jp/[^"\x27]+|/[a-z0-9\-]+-[a-z0-9\-]+/[^"\x27]+)["\x27]'
seen2 = []
for u in re.findall(pat2, h):
    if u not in seen2: seen2.append(u)
print('article-like:', len(seen2))
for u in seen2[:25]: print(u)
