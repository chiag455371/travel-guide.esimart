# -*- coding: utf-8 -*-
import pathlib, re
for r in ['jp','kr','eu','tw','oce']:
    fp = 'articles/%s.html' % r
    t = pathlib.Path(fp).read_text(encoding='utf-8')
    m = re.search(r'<h2 style=\"[^\"]*\">\s*\xF0\x9F\x94\xA5.*?</ol>\s*', t, re.S)
    if m:
        t = t[:m.start()] + t[m.end():]
        print(r, 'stripped popular list')
    pathlib.Path(fp).write_text(t, encoding='utf-8')
