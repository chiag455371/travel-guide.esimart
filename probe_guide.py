# -*- coding: utf-8 -*-
import re, pathlib, sys
g = pathlib.Path('guides/tw-esim-guide.html').read_text(encoding='utf-8')
i = g.find('<body')
sys.stdout.buffer.write(g[i:i+700].encode('utf-8','replace'))
sys.stdout.buffer.write(b'\n\n=== CSS LINKS (all) ===\n')
for m in re.findall(r'<link[^>]*>', g):
    sys.stdout.buffer.write((m+chr(10)).encode())
