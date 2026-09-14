# -*- coding: utf-8 -*-
import pathlib, re, sys
t = pathlib.Path('articles/jp.html').read_text(encoding='utf-8')
i = t.find('popular-list')
seg = t[i-250:i+150]
sys.stdout.buffer.write(repr(seg).encode('utf-8'))
