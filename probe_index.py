# -*- coding: utf-8 -*-
import sys, pathlib
t = pathlib.Path('index.html').read_text(encoding='utf-8')
checks = {
 'hero section': 'class=\"hero\"' in t,
 'region-quick-nav': 'region-quick-nav' in t,
 'card-grid count': t.count('card-grid'),
 'featured/cta': 'cta' in t.lower(),
 'breadcrumbs': 'breadcrumb' in t.lower(),
 'total cards': t.count('article-card'),
}
for k, v in checks.items():
    sys.stdout.buffer.write((str(k)+': '+str(v)+chr(10)).encode())
