# -*- coding: utf-8 -*-
"""Fix slug references and finalize."""
import os, re

base = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"

# Fix all template files for the renamed slug
for tpl_file in ['extra_templates.py', 'extra_templates_2.py']:
    fp = os.path.join(base, tpl_file)
    if os.path.exists(fp):
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('"jp-nagoya castle"', '"jp-nagoya-castle"')
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Fixed ' + tpl_file)

# Fix any references in articles
articles_dir = os.path.join(base, 'articles')
for fn in os.listdir(articles_dir):
    if not fn.endswith('.html'):
        continue
    fp = os.path.join(articles_dir, fn)
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'jp-nagoya castle' in content:
        content = content.replace('jp-nagoya castle', 'jp-nagoya-castle')
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Fixed reference in ' + fn)

# Update sitemap
os.system('python update_sitemap.py')

# Check final state
files = [f for f in os.listdir(articles_dir) if f.endswith('.html')]
article_count = len([f for f in files if f != 'index.html'])
print('')
print('Total articles: ' + str(article_count))
print('Total HTML: ' + str(len(files)))

# Verify no spaces in filenames
spaces = [f for f in files if ' ' in f]
print('Files with spaces: ' + (str(spaces) if spaces else 'None'))
