# -*- coding: utf-8 -*-
# Re-apply Pixabay covers to the 5 region pages, index.html, and guide pages.
# Each card <a .../articles/SLUG.html ...><img src=...> gets that slug's pix photo.
import re, json, os, glob, pathlib, html as htmlmod
from collections import Counter
BASE = pathlib.Path(__file__).parent
PIX = json.loads((BASE / 'pixel_cache.json').read_text(encoding='utf-8'))

def pix(slug):
    v = PIX.get(slug) or {}
    u = v.get('url')
    if not u:
        p = slug.rsplit('-', 1)[0]
        u = (PIX.get(p) or {}).get('url')
    return u

patched_files = []
for f in glob.glob('articles/jp.html') + glob.glob('articles/kr.html') + glob.glob('articles/eu.html') + glob.glob('articles/tw.html') + glob.glob('articles/oce.html') + ['index.html'] + glob.glob('guides/*.html'):
    p = pathlib.Path(f)
    t = p.read_text(encoding='utf-8')
    if 'pixabay' not in t and 'wikimedia' not in t:
        continue
    new = t
    # card blocks: <a ... articles/SLUG.html ... class=...article-card...><div...><img ...>
    def block_repl(m):
        block = m.group(0)
        imgm = re.search(r'<img[^>]*src=\"([^\"]*)\"', block)
        if not imgm:
            return block
        hrefm = re.search(r'/articles/([a-z0-9\-]+)\.html', block)
        if not hrefm:
            return block
        slug = hrefm.group(1)
        url = pix(slug)
        if not url:
            return block
        newimg = re.sub(r'src=\"[^\"]*\"', 'src=\"%s\"' % htmlmod.escape(url, quote=True), imgm.group(0), count=1)
        return block[:imgm.start() - 0]  # placeholder, replaced below
    # do it more safely with finditer over <a ... articles/SLUG.html
    out = []
    last = 0
    for m in re.finditer(r'<a href=\"[^\"]*/articles/([a-z0-9\-]+)\.html\"[^>]*>(.*?)</a>', new, re.S):
        slug = m.group(1)
        url = pix(slug)
        if not url:
            continue
        out.append(new[last:m.start()])
        seg = m.group(0)
        im = re.search(r'(<img[^>]*src=\")([^\"]*)(\")', seg)
        if im:
            seg = seg[:im.start(2)] + htmlmod.escape(url, quote=True) + seg[im.end(2):]
        out.append(seg)
        last = m.end()
    out.append(new[last:])
    new = ''.join(out)
    # og:image on region pages
    m = re.search(r'(<meta property=\"og:image\" content=\")[^\"]*(\")', new)
    if m:
        first_slug = re.search(r'/articles/([a-z0-9\-]+)\.html', new).group(1)
        new = new.replace(m.group(0), m.group(1) + (pix(first_slug) or m.group(2)[:-0]) + m.group(2), 1)
    p.write_text(new, encoding='utf-8')
    patched_files.append((f, Counter(re.findall(r'src=\"(https?://[^\"]+)\"', new).append(0) and [] or [])))

for f, c in patched_files:
    t = pathlib.Path(f).read_text(encoding='utf-8')
    hosts = Counter((re.match(r'https?://([^/]+)', u).group(1) for u in re.findall(r'src=\"(https?://[^\"]+)\"', t)))
    print(f, '| cards:', t.count('card-img'), '| hosts:', dict(hosts.most_common(4)))
