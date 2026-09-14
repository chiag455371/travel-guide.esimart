# -*- coding: utf-8 -*-
import re, pathlib, sys
def h2s(slug):
    c = pathlib.Path(slug + '.html').read_text(encoding='utf-8')
    return re.findall(r'<h2[^>]*>([^<]+)</h2>', c)
for a,b in [('articles/jp-himeji','articles/jp-himeji-castle'),('articles/jp-takamatsu-garden','articles/jp-takamatsu-rittoru')]:
    sys.stdout.buffer.write(('== pair: '+a+' / '+b+chr(10)).encode())
    sys.stdout.buffer.write((' A h2s: '+repr(h2s(a))[:400]+chr(10)).encode('utf-8','replace'))
    sys.stdout.buffer.write((' B h2s: '+repr(h2s(b))[:400]+chr(10)).encode('utf-8','replace'))
    sys.stdout.buffer.write(b'\n')
