# -*- coding: utf-8 -*-
import urllib.request, socket
socket.setdefaulttimeout(20)
def get(u):
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'})
    return urllib.request.urlopen(req)
for u in ['https://incredible-malasada-0583f9.netlify.app/',
          'https://incredible-malasada-0583f9.netlify.app/articles/jp.html']:
    try:
        r = get(u)
        body = r.read().decode('utf-8', errors='replace')
        print('OK', u, r.status, len(body))
        fn = '_ref_' + u.split('/')[-2 if '/' in u.split('/')[-1] is None else -1] + '.html'
        open('_ref_page.html', 'w', encoding='utf-8').write(body)
        break
    except Exception as e:
        print('ERR', u, str(e)[:60])
