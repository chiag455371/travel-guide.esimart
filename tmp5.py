import urllib.request, re
req = urllib.request.Request('https://www.letsgojp.com/', headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
h = urllib.request.urlopen(req, timeout=40).read().decode('utf-8','ignore')
# dump all hrefs with counts
links = re.findall(r'href=["\x27]([^"\x27]+)["\x27]', h)
from collections import Counter
c = Counter()
for u in links:
    # normalize: keep first path segment
    m = re.match(r'(?:https?://[^/]+)?(/[^?#\x27" ]*)', u)
    p = m.group(1) if m else u
    segs = [s for s in p.split('/') if s][:2]
    c['/'.join(segs)] += 1
for k,v in c.most_common(40):
    print(v, k)
