# -*- coding: utf-8 -*-
import re, pathlib, sys
t = pathlib.Path('articles/jp.html').read_text(encoding='utf-8')
i = t.find('jp-kobe-Night')
sys.stdout.buffer.write(('idx '+str(i)+chr(10)).encode())
sys.stdout.buffer.write((repr(t[i-30:i+90]) + chr(10)).encode('utf-8','replace'))
m = re.search(r'<a href=\"[^\"]*articles/jp-kobe-Night\.html\"[^>]*>', t)
sys.stdout.buffer.write(('match: ' + (m.group(0)[:80] if m else 'NONE') + chr(10)).encode('utf-8','replace'))
