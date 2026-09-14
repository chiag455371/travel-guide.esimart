# -*- coding: utf-8 -*-
import re, pathlib, sys
t = pathlib.Path('articles/jp.html').read_text(encoding='utf-8')
m = re.search(r'src=\"https://thumb\.wikimedia[^\"]+\"', t)
sys.stdout.buffer.write(t[m.start()-500:m.start()+120].encode('utf-8','replace'))
