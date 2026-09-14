# -*- coding: utf-8 -*-
import re, glob, os, json, pathlib
# which 6 articles have broken imgs, and what do they cover
for f in glob.glob('articles/*.html'):
    t = pathlib.Path(f).read_text(encoding='utf-8')
    m = re.findall(r'src=\"(https?://[^\"]+)\"', t)
    bad = [u for u in m if 'loremflickr' in u or 'picsum' in u]
    if bad:
        slug = os.path.basename(f).replace('.html','')
        og = re.search(r'og:image\" content=\"([^\"]+)', t)
        print(slug, '| imgs:', len(m), '| bad:', len(bad), '| og:', (og.group(1)[:60] if og else 'none'))
