import urllib.request, re, sys
try:
    req = urllib.request.Request('https://www.letsgojp.com/', headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    h = urllib.request.urlopen(req, timeout=40).read().decode('utf-8','ignore')
except Exception as e:
    print('FETCH_FAIL', e)
    sys.exit(0)
print('LEN', len(h))
urls = re.findall(r'href=(["\'])(https?://www\.letsgojp\.com/[^"\']+)\1', h)
urls = [u for u,_ in urls]
seen = []
for u in urls:
    if u not in seen and ('/entry/' in u or '/tokyo/' in u or '/jp/' in u):
        seen.append(u)
for u in seen[:25]:
    print(u)
