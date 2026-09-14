# -*- coding: utf-8 -*-
import re, glob, os, pathlib, json, html as htmlmod
BASE = pathlib.Path(__file__).parent
PIX = json.loads((BASE / 'pixel_cache.json').read_text(encoding='utf-8'))
def pix(slug):
    v = PIX.get(slug) or {}
    u = v.get('url')
    if not u:
        p = slug.rsplit('-',1)[0]
        u = (PIX.get(p) or {}).get('url')
    return u

fixed = 0
for f in glob.glob('articles/*.html'):
    slug = os.path.basename(f)[:-5]
    if slug in ('index','jp','kr','eu','tw','oce'):
        continue
    url = pix(slug)
    if not url:
        continue
    p = pathlib.Path(f)
    t = p.read_text(encoding='utf-8')
    new = t
    new = re.sub(r'(<meta name="twitter:image" content=")[^"]*(")', lambda m: m.group(1)+htmlmod.escape(url,quote=True)+m.group(2), new)
    new = re.sub(r'("image":\s*")[^"]*wikimedia[^"]*(")', lambda m: m.group(1)+htmlmod.escape(url,quote=True)+m.group(2), new)
    # remaining img srcs to wiki
    def imgrepl(m):
        global url
        return m.group(1)+htmlmod.escape(url,quote=True)+m.group(2)
    new = re.sub(r'(<img[^>]*src=")[^"]*wikimedia[^"]*(")', imgrepl, new)
    if new != t:
        p.write_text(new, encoding='utf-8')
        fixed += 1
print('articles cleaned:', fixed)
tot = 0
for f in glob.glob('articles/*.html') + glob.glob('guides/*.html') + ['index.html']:
    t = pathlib.Path(f).read_text(encoding='utf-8')
    n = len(re.findall(r'wikimedia', t))
    if n:
        print(f, n)
    tot += n
print('total wikimedia remaining:', tot)
