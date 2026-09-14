# -*- coding: utf-8 -*-
import pathlib
p = pathlib.Path('daily_pipeline.py')
s = p.read_text(encoding='utf-8')
old = '''# 4.5 圖片管道: 處理新文章封面圖(替換 picsum 為 Wikimedia 真實景點照)
if new_slugs and os.path.exists('image_pipeline.py'):
    print(f'--- Running image pipeline for {len(new_slugs)} new articles')
    run([sys.executable, 'image_pipeline.py'])'''
new = '''# 4.5 圖片管道: 為新文章抓取 Pixabay 專屬封面 + 套用全站圖片
if new_slugs and os.path.exists('fetch_pixabay_fill.py'):
    print(f'--- Running Pixabay fill for {len(new_slugs)} new articles')
    run([sys.executable, 'fetch_pixabay_fill.py'])
if os.path.exists('apply_pix_articles.py'):
    run([sys.executable, 'apply_pix_articles.py'])'''
assert old in s, 'block not found'
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
print('daily_pipeline updated to use Pixabay')
