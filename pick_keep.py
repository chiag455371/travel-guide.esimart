# -*- coding: utf-8 -*-
import re, pathlib, sys, json
def text_of(slug):
    c = pathlib.Path(slug + '.html').read_text(encoding='utf-8')
    c = re.sub(r'<script.*?</script>|<style.*?</style>', '', c, flags=re.S)
    c = re.sub(r'<[^>]+>', ' ', c)
    return re.sub(r'\s+', ' ', c)
def wordcount(slug):
    return len(text_of(slug).split())
pairs = [('articles/jp-himeji','articles/jp-himeji-castle'),('articles/jp-takamatsu-garden','articles/jp-takamatsu-rittoru')]
for a,b in pairs:
    wa, wb = wordcount(a), wordcount(b)
    print(a, wa, 'words  |  ', b, wb, 'words  |  keep:', a if wa>=wb else b)
    # also check h2s
    def h2s(s):
        c = pathlib.Path(s + '.html').read_text(encoding='utf-8')
        return re.findall(r'<h2[^>]*>([^<]+)</h2>', c)
    sys.stdout.buffer.write(('  A h2s: '+repr(h2s(a))+chr(10)).encode('utf-8','replace'))
    sys.stdout.buffer.write(('  B h2s: '+repr(h2s(b))+chr(10)).encode('utf-8','replace'))
    print()
