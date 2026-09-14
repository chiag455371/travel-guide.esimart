# -*- coding: utf-8 -*-
import re, pathlib, sys
t = pathlib.Path('articles/jp.html').read_text(encoding='utf-8')
for m in re.finditer(r'wikimedia', t):
    sys.stdout.buffer.write((t[max(0,m.start()-260):m.start()+40].replace(chr(10),' ') + chr(10)+'---'+chr(10)).encode('utf-8','replace'))
