# -*- coding: utf-8 -*-
import re, glob, pathlib, sys
for f in glob.glob('guides/*-food.html'):
    t = pathlib.Path(f).read_text(encoding='utf-8')
    m = re.search(r'<body', t)
    seg = t[m.start():m.start()+600]
    nav = re.search(r'<nav[^>]*>.*?</nav>', seg, re.S)
    sys.stdout.buffer.write(((f + ' :: ' + (nav.group(0)[:120] if nav else 'NO NAV')) + chr(10)).encode('utf-8','replace'))
