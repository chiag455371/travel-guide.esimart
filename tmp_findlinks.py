import urllib.request, re
req = urllib.request.Request('https://www.letsgojp.com/', headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req, timeout=30).read().decode('utf-8','ignore')
links = re.findall(r'href="(/entry/[^"]+)"', html)
seen = []
for u in links:
    if u not in seen: seen.append(u)
print('\n'.join(seen[:25]))
