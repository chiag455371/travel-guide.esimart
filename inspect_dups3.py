# -*- coding: utf-8 -*-
import re, pathlib, sys
for s in ['articles/jp-himeji','articles/jp-himeji-castle']:
    c = pathlib.Path(s + '.html').read_text(encoding='utf-8')
    sys.stdout.buffer.write(('=== ' + s + ' len=' + str(len(c)) + chr(10)).encode())
    # show first 600 chars of <body>
    m = re.search(r'<body.*', c, re.S)
    sys.stdout.buffer.write((m.group(0)[:700]).encode('utf-8','replace'))
    sys.stdout.buffer.write(b'\n\n')
