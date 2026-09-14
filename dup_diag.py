# -*- coding: utf-8 -*-
import json, urllib.request, urllib.parse, time, pathlib, sys
from collections import defaultdict, Counter
KEY = '39894189-8822531df0830fb07f58a9a69'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) travel-bot'}
PIX = json.loads(pathlib.Path('pixel_cache.json').read_text(encoding='utf-8'))
by_pid = defaultdict(list)
for k, v in PIX.items():
    if v.get('pid'):
        by_pid[v['pid']].append(k)
dup = {pid: s for pid, s in by_pid.items() if len(s) > 1}
# count distinct URLs among dup pids
urls = set()
for pid, slugs in dup.items():
    for k in slugs:
        urls.add(PIX[k].get('url'))
sys.stdout.buffer.write((('dup groups: %d | distinct URLs shared: %d\n' % (len(dup), len(urls))).encode()))
# sample
for pid, slugs in list(dup.items())[:3]:
    sys.stdout.buffer.write((('pid %s -> %s\n' % (pid, slugs[:5])).encode('utf-8','replace')))
    sys.stdout.buffer.write(('  urls: ' + repr({k: PIX[k].get('url','')[:50] for k in slugs[:3]}) + chr(10)).encode('utf-8','replace'))
