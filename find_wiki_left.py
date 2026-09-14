# -*- coding: utf-8 -*-
import re, pathlib, sys
for f in ['articles/jp.html','articles/kr.html','articles/eu.html','articles/eu.html']:
    t = pathlib.Path(f).read_text(encoding='utf-8')
    for m in re.finditer(r'wikimedia', t):
        ctx = t[max(0,m.start()-110):m.start()+50].replace(chr(10),' ')
        sys.stdout.buffer.write((f + ' :: ' + ctx + chr(10)).encode('utf-8','replace'))
