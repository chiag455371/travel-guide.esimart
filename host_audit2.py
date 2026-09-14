# -*- coding: utf-8 -*-
import re, pathlib, sys
for f in ['articles/index.html','guides/tw-esim-guide.html','articles/jp.html']:
    t = pathlib.Path(f).read_text(encoding='utf-8')
    sys.stdout.buffer.write(('=== ' + f + chr(10)).encode())
    for m in re.finditer(r'src=\"(https?://[^\"]+)\"', t):
        pass
    import collections
    c = collections.Counter()
    for m in re.finditer(r'src=\"(https?://[^\"]+)\"', t):
        c[re.match(r'https?://([^/]+)', m.group(1)).group(1)] += 1
    sys.stdout.buffer.write((repr(c.most_common(3)) + chr(10)).encode())
