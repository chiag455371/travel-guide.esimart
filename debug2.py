import re
with open('articles/jp.html',encoding='utf-8') as f:
    html = f.read()
# Find the first article-card block
block = re.search(r'<a href="https://[^"]+/articles/([^"]+)" class="article-card">.*?</a>', html, re.DOTALL)
if block:
    print(block.group(0)[:600])
    print()
    slug = block.group(1)
    print('Slug:', slug)
