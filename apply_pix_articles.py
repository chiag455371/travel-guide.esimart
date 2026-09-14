# -*- coding: utf-8 -*-
import json, re, os, glob, pathlib, html

BASE = pathlib.Path(__file__).parent
PIX = json.loads((BASE / 'pixel_cache.json').read_text(encoding='utf-8'))
SITE = 'https://travel-guide-esimart.pages.dev'

def pix_url(slug):
    v = PIX.get(slug)
    if not v or not v.get('url'):
        return None
    u = v['url']
    w = v.get('width') or 1600
    # pixabay CDN resize param
    if w > 1600:
        h = int(1000 * 1600 / w)
        u += '&w=1600'
    return u

# 1) article pages: og:image + each in-body <img>
def patch_article(slug, fp):
    cover = pix_url(slug)
    if not cover:
        return False
    t = pathlib.Path(fp).read_text(encoding='utf-8')
    orig_imgs = re.findall(r'<img[^>]*>', t)
    # find all img src (article hero + related cards). Replace the FIRST real article img (hero)
    # and any related-card imgs that are the same wiki photo
    new = t
    # og:image
    new = re.sub(r'(<meta property=\"og:image\" content=\")[^\"]*(\")', lambda m: m.group(1)+cover+m.group(2), new, count=1)
    # main hero image: first <img ...> that is not in nav
    hero_done = False
    extra = [pix_url(slug + '__card%d' % i) for i in range(1, 5)]
    extra = [e for e in extra if e]
    # replace all img srcs with unique pix photos in order
    imgs = list(re.finditer(r'<img[^>]*src=\"[^\"]+\"[^>]*>', new))
    idx = 0
    for m in imgs:
        tag = m.group(0)
        newsrc = cover if idx == 0 else extra[idx-1] if idx-1 < len(extra) else extra[0] if extra else cover
        if newsrc:
            newtag = re.sub(r'src=\"[^\"]*\"', 'src=\"%s\"' % html.escape(newsrc, quote=True), tag, count=1)
            new = new[:m.start()] + newtag + new[m.end():]
            # recompute remaining matches positions
            imgs = list(re.finditer(r'<img[^>]*src=\"[^\"]+\"[^>]*>', new[new[:m.start()].count('<img')+new[:m.start()].count('<meta')+0:]))
            break
    # simpler: replace ALL img src in this article with unique photos sequentially, re-scanning each time
    return new

# The above got complicated; use a cleaner sequential replace:
def patch_article2(slug, fp):
    cover = pix_url(slug)
    if not cover:
        return None
    extra = [pix_url(slug + '__card%d' % i) for i in range(1, 5)]
    extra = [e for e in extra if e]
    seq = [cover] + extra
    if not extra:
        seq = [cover] * 8
    t = pathlib.Path(fp).read_text(encoding='utf-8')
    count = {'i': 0}
    def repl(m):
        tag = m.group(0)
        i = count['i']
        count['i'] += 1
        src = seq[i] if i < len(seq) else seq[-1]
        return re.sub(r'src=\"[^\"]*\"', 'src=\"%s\"' % html.escape(src, quote=True), tag, count=1)
    new = re.sub(r'<img[^>]*src=\"[^\"]+\"[^>]*>', repl, t)
    new = re.sub(r'(<meta property=\"og:image\" content=\")[^\"]*(\")', lambda m: m.group(1)+html.escape(cover, quote=True)+m.group(2), new, count=1)
    return new

n_done = 0
for f in glob.glob('articles/*.html'):
    slug = os.path.basename(f)[:-5]
    if slug in ('index',) or slug in ('jp','kr','eu','tw','oce'):
        continue
    r = patch_article2(slug, f)
    if r:
        pathlib.Path(f).write_text(r, encoding='utf-8')
        n_done += 1
print('articles patched:', n_done, '/', len(glob.glob('articles/*.html')))
