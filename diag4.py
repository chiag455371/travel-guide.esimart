# -*- coding: utf-8 -*-
import json
c = json.load(open('pixel_cache.json',encoding='utf-8'))
v = c.get('jp-kobe-Night')
print('pix url for jp-kobe-Night:', v.get('url','MISSING')[:80] if v else 'no key')
import re, pathlib
t = pathlib.Path('articles/jp.html').read_text(encoding='utf-8')
i = t.find('Kobe_Port')
seg = t[i-100:i+200]
sys = __import__('sys')
sys.stdout.buffer.write(seg.encode('utf-8','replace'))
