import os, datetime
base = 'https://chiag455371.github.io/travel-guide.esimart'
today = datetime.date.today().isoformat()
urls = []
urls.append('<url><loc>' + base + '/</loc><priority>1.0</priority><lastmod>' + today + '</lastmod></url>')
for f in sorted(os.listdir('articles')):
    if f.endswith('.html') and f != 'index.html':
        slug = f.replace('.html','')
        urls.append('<url><loc>' + base + '/articles/' + slug + '.html</loc><priority>0.8</priority><lastmod>' + today + '</lastmod></url>')
urls.append('<url><loc>' + base + '/articles/</loc><priority>0.9</priority><lastmod>' + today + '</lastmod></url>')
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>'
with open('sitemap.xml', 'w', encoding='utf-8') as fp:
    fp.write(xml)
print('Written', len(urls), 'URLs')
