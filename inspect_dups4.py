# -*- coding: utf-8 -*-
import re, pathlib, sys, hashlib
def text_of(slug):
    c = pathlib.Path(slug + '.html').read_text(encoding='utf-8')
    c = re.sub(r'<script.*?</script>', '', c, flags=re.S)
    c = re.sub(r'<style.*?</style>', '', c, flags=re.S)
    c = re.sub(r'<[^>]+>', ' ', c)
    return re.sub(r'\s+', ' ', c)
pairs = [
 ('articles/jp-himeji','articles/jp-himeji-castle'),
 ('articles/jp-takamatsu-garden','articles/jp-takamatsu-rittoru'),
]
for a,b in pairs:
    ta, tb = text_of(a), text_of(b)
    print(a, len(ta), hashlib.md5(ta.encode()).hexdigest())
    print(b, len(tb), hashlib.md5(tb.encode()).hexdigest())
    print()
    # check the main content difference
    import difflib
    sm = difflib.SequenceMatcher(None, ta, tb)
    print('ratio', sm.ratio())
