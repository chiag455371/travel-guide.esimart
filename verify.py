import re
for r in ['jp','kr','eu','tw','oce']:
    with open('articles/'+r+'.html',encoding='utf-8') as f:
        html = f.read()
    cards = re.findall(r'<a href="https://[^"]+/articles/'+r+'-[^"]+" class="article-card">.*?</a>', html, re.DOTALL)
    bad = [c for c in cards if 'wikimedia' in c]
    pix = [c for c in cards if 'pixabay' in c]
    print(f'{r}.html: total={len(cards)} pixabay={len(pix)} broken(wikimedia)={len(bad)}')
    if bad:
        m = re.search(r'src="([^"]+)"', bad[0])
        print(f'  First bad src: {m.group(1)[:100] if m else "NONE"}')
