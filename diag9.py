# -*- coding: utf-8 -*-
import re, pathlib
t = pathlib.Path('articles/eu.html').read_text(encoding='utf-8')
# find the exact src attribute containing both pix and wiki remnants
m = re.search(r'src=\"(https://pixabay\.com/get/[^\"]*Fotuna|https://pixabay\.com/get/[^\"]*Johannes)[^\"]*\"', t)
# simplest: replace the entire malformed src
t2 = re.sub(r'(<img class=\"card-img\" src=\")https://pixabay\.com/get/[^\"]*Johannes[^=]*=([^>]*wiki[^>]*)', r'PLACEHOLDER', t)
print('changed:', t2 != t)
# inspect precisely
idx = t.find('_1280.jpg\"%2C_Johannes')
print(repr(t[idx-20:idx+150]))
