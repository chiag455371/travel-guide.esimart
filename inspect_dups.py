# -*- coding: utf-8 -*-
import re, pathlib, sys
def info(slug):
    c = pathlib.Path(slug + '.html').read_text(encoding='utf-8')
    m = re.search(r'<main.*?</main>', c, re.S)
    t = re.search(r'<title>([^<]+)</title>', c)
    return (len(m.group(0)) if m else 0, (t.group(1)[:55] if t else slug))
for s in ['articles/kr-jeju-cafe','articles/kr-jeju-jungmun','articles/kr-jeju',
          'articles/jp-takamatsu-garden','articles/jp-takamatsu-rittoru',
          'articles/jp-hiroshima-itsukushima','articles/jp-hiroshima-okunoshima','articles/jp-hiroshima',
          'articles/jp-himeji','articles/jp-himeji-castle']:
    try:
        ln, tt = info(s)
    except FileNotFoundError:
        ln, tt = 'MISSING', ''
    sys.stdout.buffer.write((s + ' | len ' + str(ln) + ' | ' + tt + chr(10)).encode('utf-8'))
