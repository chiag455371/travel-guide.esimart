# -*- coding: utf-8 -*-
"""Full daily pipeline: generate -> patch new -> regenerate region pages ->
re-apply region enhancements -> sitemap -> commit -> deploy.
Idempotent; safe to run repeatedly."""
import os, sys, re, glob, datetime, subprocess

BASE = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"
os.chdir(BASE)
sys.path.insert(0, BASE)
SITE = 'https://travel-guide-esimart.pages.dev'
REGION_NAMES = {'jp': '日本攻略', 'kr': '韓國攻略', 'tw': '台灣攻略',
                'eu': '歐洲攻略', 'oce': '大洋洲攻略'}

def run(cmd, env=None):
    print(f"\n--- {cmd}\n")
    r = subprocess.run(cmd, shell=True, cwd=BASE, env=env or os.environ.copy())
    if r.returncode != 0:
        print(f"ERROR: {cmd} exited {r.returncode}")
        sys.exit(1)

# 1. generate articles
import daily_generator_v3
daily_generator_v3.main()

# 2. collect today's new real articles
new_slugs = []
for f in glob.glob('articles/*.html'):
    st = os.stat(f)
    if datetime.datetime.fromtimestamp(st.st_mtime).date() != datetime.date.today():
        continue
    c = open(f, encoding='utf-8').read()
    if 'http-equiv' not in c or len(c) > 500:
        new_slugs.append(os.path.basename(f)[:-5])
print(f"\nNew articles today: {len(new_slugs)} -> {new_slugs}")

# 3. build title/seed index from all real (non-redirect) articles
titles = {}
for f in glob.glob('articles/*.html'):
    slug = os.path.basename(f)[:-5]
    c = open(f, encoding='utf-8').read()
    if 'http-equiv' in c and len(c) < 500:
        continue
    m = re.search(r'<title>([^<]+)</title>', c)
    t = (m.group(1) if m else slug).split('｜')[0].strip()
    og = re.search(r'og:image" content="https://picsum\.photos/seed/(\d+)/', c)
    titles[slug] = (t, og.group(1) if og else None)

def related_for(slug, n=4):
    prefix = slug.split('-')[0]
    if not prefix:
        return []
    second = slug.split('-')[1] if len(slug.split('-')) >= 2 else ''
    same_tag = [s for s in titles
                if s != slug and s.startswith(prefix + '-')
                and s.split('-')[1] == second and second != '']
    others = [s for s in titles if s != slug and s.startswith(prefix + '-') and s not in same_tag]
    picked = same_tag[:n]
    rest = [s for s in others if s not in picked]
    while len(picked) < n and rest:
        picked.append(rest.pop(0))
    return picked[:n]

# 4. patch new articles: related section + breadcrumb
for slug in new_slugs:
    f = f'articles/{slug}.html'
    if not os.path.exists(f):
        continue
    c = open(f, encoding='utf-8').read()
    region = slug.split('-')[0]

    if 'related-section' not in c:
        rel = related_for(slug)
        if rel:
            cards = []
            for s in rel:
                t, seed = titles.get(s, (s, None))
                seed = seed or '100000'
                cards.append(
                    f'      <a href="{SITE}/articles/{s}.html" class="related-card">'
                    f'<div class="card-img-wrapper"><img class="card-img" '
                    f'src="https://picsum.photos/seed/{seed}/600/400" alt="{t}" loading="lazy"></div>'
                    f'<div class="card-body"><span class="card-title">{t}</span></div></a>')
            section = ('\n<div class="related-section">\n  <h2>延伸閱讀</h2>\n'
                       '  <div class="related-grid">\n' + '\n'.join(cards) + '\n  </div>\n</div>\n')
            c = c.replace('</body>', section + '</body>')

    if 'breadcrumb' not in c and region:
        m = re.search(r'<title>([^<]+)</title>', c)
        title = (m.group(1) if m else slug).split('｜')[0][:30]
        crumb = (
            f'<nav aria-label="breadcrumb" class="breadcrumb-nav"><ol class="breadcrumb">'
            f'<li><a href="{SITE}/">首頁</a></li>'
            f'<li><a href="{SITE}/articles/{region}.html">{REGION_NAMES.get(region, region)}</a></li>'
            f'<li aria-current="page">{title}</li></ol></nav>')
        bm = re.search(r'<h1>[^<]+</h1>', c)
        if bm:
            c = c[:bm.end()] + '\n' + crumb + c[bm.end():]

    open(f, 'w', encoding='utf-8').write(c)
print('new articles patched (related + breadcrumb)')

# 4.5 圖片管道: 處理新文章封面圖(替換 picsum 為 Wikimedia 真實景點照)
if new_slugs and os.path.exists('image_pipeline.py'):
    print(f'--- Running image pipeline for {len(new_slugs)} new articles')
    run([sys.executable, 'image_pipeline.py'])

# 5. regenerate region pages
run('python generate_region_pages.py')

# 6. re-apply region enhancements
run('python add_breadcrumbs.py')
run('python add_popular_lists.py')
run('python add_guide_cta.py')

# 6.5 build food cluster pages (idempotent)
if os.path.exists('build_food_cluster.py'):
    print('--- python build_food_cluster.py')
    run([sys.executable, 'build_food_cluster.py'])

# 7. sitemap: add new article URLs
sm = open('sitemap.xml', encoding='utf-8').read()
lines = sm.rstrip().split('\n')
added = 0
for slug in new_slugs:
    url = f'{SITE}/articles/{slug}.html'
    if url not in sm:
        lines.insert(len(lines) - 1,
                     f'<url><loc>{url}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod></url>')
        added += 1
open('sitemap.xml', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print(f'sitemap: added {added} new URLs')

# 8. commit
subprocess.run(['git', 'add', '-A'], check=False)
subprocess.run(['git', 'commit', '-m',
                f'daily: {datetime.date.today()} - pipeline ({len(new_slugs)} new)'],
               check=False, capture_output=True)

# 9. deploy
env = os.environ.copy()
env['CLOUDFLARE_API_TOKEN'] = os.environ.get('CLOUDFLARE_API_TOKEN', '')
if env['CLOUDFLARE_API_TOKEN']:
    run('npx wrangler pages deploy . --project-name=travel-guide-esimart', env=env)
else:
    print('\nWARN: CLOUDFLARE_API_TOKEN not set - deploy skipped. '
          'Set the env var before running for auto-deploy.')

print('\n=== Pipeline complete ===')
