# -*- coding: utf-8 -*-
import re, pathlib, sys
t = pathlib.Path('articles/jp-tokyo-shibuya.html').read_text(encoding='utf-8')
for m in re.finditer(r'<(img|meta)[^>]*src?=?\"?([^\"]*(?:wikimedia|picsum|pixabay)[^\"]*)\"', t):
    sys.stdout.buffer.write((m.group(0)[:140].encode('utf-8','replace')+b'\n'))
