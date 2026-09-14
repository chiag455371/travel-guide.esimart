# -*- coding: utf-8 -*-
import pathlib, re, sys
pat = re.compile(r'<h2 style="margin:1rem 0 \.5rem;font-size:1\.3rem;font-weight:900">.*?</ol>\s*', re.S)
for r in ['jp','kr','eu','tw','oce']:
    fp = 'articles/%s.html' % r
    t = pathlib.Path(fp).read_text(encoding='utf-8')
    new, n = pat.subn('', t, count=1)
    sys.stdout.buffer.write((r + ' stripped ' + str(n)).encode())
    pathlib.Path(fp).write_text(new, encoding='utf-8')
