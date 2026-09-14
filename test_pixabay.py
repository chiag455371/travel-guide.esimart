# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, json
KEY = '39894189-8822531df0830fb07f58a9a69'
def search(q, n=3):
    url = 'https://pixabay.com/api/?key=' + KEY + '&' + urllib.parse.urlencode({'q': q, 'per_page': n, 'safesearch': 'true', 'lang': 'zh'})
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    d = json.loads(urllib.request.urlopen(req, timeout=20).read())
    return d
for q in ['Tokyo Shibuya', 'Seoul Namsan tower', 'Amsterdam canal']:
    d = search(q, 3)
    print('=== query:', q, '| total:', d.get('totalHits'))
    for hit in d.get('hits', [])[:3]:
        print('  pid', hit['id'], hit['width'], 'x', hit['height'], hit['url'][:70], '| user:', hit['user'])
