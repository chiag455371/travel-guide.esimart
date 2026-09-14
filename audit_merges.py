# -*- coding: utf-8 -*-
import os, re, glob, pathlib
targets = ['jp-hiroshima-itsukushima','jp-hiroshima-miatu','jp-hiroshima-okunoshima',
           'jp-hiroshima-peace','jp-fukuoka-food','jp-kamakura-buddha','jp-himeji-castle']
for s in targets:
    p = 'articles/%s.html' % s
    if not os.path.exists(p):
        print(s, 'MISSING')
        continue
    c = pathlib.Path(p).read_text(encoding='utf-8')
    kind = 'meta-refresh' if 'http-equiv' in c else 'full-article'
    m = re.search(r'url=([^"]+)', c)
    print(s, '|', kind, '|', m.group(1).split('/')[-1] if m else '')
for s in ['jp-hiroshima','jp-fukuoka','jp-kamakura','jp-himeji']:
    print(s, 'main exists:', os.path.exists('articles/%s.html' % s))
refs = {}
for f in glob.glob('articles/*.html') + glob.glob('guides/*.html') + ['index.html', 'sitemap.xml']:
    try:
        t = pathlib.Path(f).read_text(encoding='utf-8')
    except Exception:
        continue
    for s in targets:
        n = len(re.findall(re.escape(s) + r'\.html', t))
        if n:
            refs.setdefault(s, []).append((f, n))
for s in targets:
    print(s, 'referenced in:', refs.get(s, '(none)'))
