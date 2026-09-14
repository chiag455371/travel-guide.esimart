# -*- coding: utf-8 -*-
import re, pathlib, sys
t = pathlib.Path('_live_home.html').read_text(encoding='utf-8')
i = t.find('<nav'); j = t.find('</nav>')
sys.stdout.buffer.write(t[i:j+6].encode('utf-8'))
