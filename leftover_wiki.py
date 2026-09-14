# -*- coding: utf-8 -*-
import re, glob, os, pathlib, json, html as htmlmod
from collections import Counter
BASE = pathlib.Path(__file__).parent
PIX = json.loads((BASE / 'pixel_cache.json').read_text(encoding='utf-8'))
def pix(slug):
    v = PIX.get(slug) or {}
    u = v.get('url')
    if not u:
        p = slug.rsplit('-',1)[0]
        u = (PIX.get(p) or {}).get('url')
    return u
# remaining wiki in region pages
for f in ['articles/jp.html','articles/kr.html','articles/eu.html','articles/tw.html','articles/oce.html']:
    p = pathlib.Path(f)
    t = p.read_text(encoding='utf-8')
    wiki = [u for u in re.findall(r'src=\"(https?://[^\"]+)\"', t) if 'wikimedia' in u]
    if wiki:
        print(f, 'wiki srcs:', len(wiki))
        for u in wiki[:3]:
            i = t.find(u)
            print('  context:', re.findall(r'articles/([a-z0-9\-]+)\.html', t[i-300:i])[-1] if re.findall(r'articles/([a-z0-9\-]+)\.html', t[i-300:i]) else '(no href near)')
# check guides food wiki srcs
for f in glob.glob('guides/*-food.html'):
    t = pathlib.Path(f).read_text(encoding='utf-8')
    wiki = [u for u in re.findall(r'src=\"(https?://[^\"]+)\"', t) if 'wikimedia' in u]
    if wiki:
        print(f, 'wiki:', len(wiki))
