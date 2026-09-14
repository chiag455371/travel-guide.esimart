import os, sys
sys.path.insert(0, r'C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo')
os.chdir(r'C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo')

import daily_generator_v3 as gen
import subprocess
import shutil

# Generate articles
gen.main()

# Update sitemap
print("\n[2/3] Updating sitemap...")
exec(open('update_sitemap.py', encoding='utf-8').read())

# Build and deploy
print("\n[3/3] Building and deploying...")
dist = 'dist'
if os.path.exists(dist):
    shutil.rmtree(dist)
os.makedirs(f'{dist}/articles', exist_ok=True)
os.makedirs(f'{dist}/assets', exist_ok=True)

for f in ['index.html', 'sitemap.xml', 'robots.txt', '.nojekyll']:
    if os.path.exists(f):
        shutil.copy2(f, f'{dist}/{f}')
shutil.copytree('articles', f'{dist}/articles', dirs_exist_ok=True)
shutil.copytree('assets', f'{dist}/assets', dirs_exist_ok=True)

env = os.environ.copy()
env['CLOUDFLARE_API_TOKEN'] = 'ENV_CF_TOKEN'
result = subprocess.run(
    ['npx', 'wrangler', 'pages', 'deploy', dist, '--project-name', 'travel-guide-esimart', '--branch', 'main', '--commit-dirty=true'],
    env=env, capture_output=True, text=True
)
print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
if result.returncode != 0:
    print(f"Deploy failed: {result.stderr[:200]}")
else:
    print("Deployment successful!")

# Git commit and push
subprocess.run(['git', 'add', '-A'], check=False)
subprocess.run(['git', 'commit', '-m', f'daily: {gen.TODAY} - articles generated'], check=False, capture_output=True)
subprocess.run(['git', 'push', 'origin', 'main'], check=False, capture_output=True)

print("\nDone!")

