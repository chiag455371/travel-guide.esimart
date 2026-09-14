# -*- coding: utf-8 -*-
import re, pathlib, sys
for s in ['articles/jp-takamatsu-garden','articles/jp-takamatsu-rittoru','articles/jp-himeji','articles/jp-himeji-castle']:
    c = pathlib.Path(s + '.html').read_text(encoding='utf-8')
    m = re.search(r'<main.*?</main>', c, re.S)
    body = m.group(0) if m else ''
    # strip html tags to compare raw text
    text = re.sub(r'<[^>]+>', ' ', body)
    text = re.sub(r'\s+', ' ', text)
    print(s, 'text-len', len(text))
    print('  ', text[:120])
    print()
# check himeji vs himeji-castle full text equality
a = re.sub(r'\s+',' ', re.sub(r'<[^>]+>',' ', pathlib.Path('articles/jp-himeji.html').read_text(encoding='utf-8')))
b = re.sub(r'\s+',' ', re.sub(r'<[^>]+>',' ', pathlib.Path('articles/jp-himeji-castle.html').read_text(encoding='utf-8')))
print('himeji == himeji-castle?', a == b, 'len diff', abs(len(a)-len(b)))
g = re.sub(r'\s+',' ', re.sub(r'<[^>]+>',' ', pathlib.Path('articles/jp-takamatsu-garden.html').read_text(encoding='utf-8')))
r = re.sub(r'\s+',' ', re.sub(r'<[^>]+>',' ', pathlib.Path('articles/jp-takamatsu-rittoru.html').read_text(encoding='utf-8')))
print('takamatsu-garden == takamatsu-rittoru?', g == r)
