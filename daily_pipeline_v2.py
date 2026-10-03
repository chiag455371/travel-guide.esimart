import os, sys, shutil, subprocess
# 強制 stdout/stderr 用 UTF-8，避免 Windows console GBK 印不出 emoji/中文
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
# 使用 __file__ 絕對路徑避免排程任務 codepage 950 把 CJK 路徑寫壞
_REPO_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _REPO_DIR)
os.chdir(_REPO_DIR)

# 找到 npx / git 的絕對路徑（排程任務環境 PATH 沒有 node_modules 和 git）
NODE_DIR = r'C:\Program Files\nodejs'
def _abs(cmd):
    full = os.path.join(NODE_DIR, cmd + ('.cmd' if cmd in ('npx','npm','node') else '.exe'))
    return full if os.path.exists(full) else cmd

import daily_generator_v3 as gen

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
# CF token 用環境變數（排程任務設好）；若沒有則用 wrangler.toml 內建的 token
env.setdefault('CLOUDFLARE_API_TOKEN', 'ENV_CF_TOKEN')
npx_path = _abs('npx')
# 用 utf-8 + errors=replace 避免 Windows 預設 GBK 解碼中文字報 UnicodeDecodeError
result = subprocess.run(
    [npx_path, 'wrangler', 'pages', 'deploy', dist, '--project-name', 'travel-guide-esimart', '--branch', 'main', '--commit-dirty=true'],
    env=env, capture_output=True, text=True, encoding='utf-8', errors='replace'
)
out = result.stdout or ''
print(out[-500:] if len(out) > 500 else out)
if result.returncode != 0:
    err = result.stderr or ''
    print(f"Deploy failed: {err[:200]}")
else:
    print("Deployment successful!")

# Git commit and push
git_path = _abs('git')
subprocess.run([git_path, 'add', '-A'], check=False, capture_output=True)
subprocess.run([git_path, 'commit', '-m', f'daily: {gen.TODAY} - articles generated'], check=False, capture_output=True)
subprocess.run([git_path, 'push', 'origin', 'main'], check=False, capture_output=True)

print("\nDone!")

