import urllib.request, re
req = urllib.request.Request('https://www.letsgojp.com/archives/757613', headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
h = urllib.request.urlopen(req, timeout=40).read().decode('utf-8','ignore')
# strip scripts/styles
body = re.sub(r'<script.*?</script>', '', h, flags=re.S)
body = re.sub(r'<style.*?</style>', '', body, flags=re.S)
# extract heading structure
heads = re.findall(r'<h([1-4])[^>]*>(.*?)</h\1>', body, flags=re.S)
print('=== HEADINGS ===')
for lvl, txt in heads:
    t = re.sub(r'<[^>]+>', '', txt)
    t = re.sub(r'\s+', ' ', t).strip()
    if t:
        print('H'+lvl, t[:80])
# title
tt = re.search(r'<title>(.*?)</title>', h, re.S)
print('TITLE:', tt.group(1).strip() if tt else 'none')
# find main content container
sec = re.findall(r'<section[^>]*class="([^"]*)"[^>]*>', h)
print('SECTIONS:', sec[:10])
