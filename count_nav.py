# -*- coding: utf-8 -*-
import pathlib, glob
css = pathlib.Path('assets/style.css').read_text(encoding='utf-8')
for cls in ['site-header','site-logo','header-links']:
    print(cls, 'in css:', cls in css)
sh = 0; tn = 0
shfiles = []
for f in glob.glob('guides/*.html') + glob.glob('articles/*.html') + ['index.html']:
    t = pathlib.Path(f).read_text(encoding='utf-8')
    if 'site-header' in t:
        sh += 1; shfiles.append(f)
    if 'topnav' in t:
        tn += 1
print('pages w/ site-header:', sh)
for x in shfiles: print('  ', x)
print('pages w/ topnav:', tn)
