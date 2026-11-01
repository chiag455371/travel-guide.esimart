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

# 網址正規化：canonical / 內部連結一律無副檔名（Pages 會把 .html 308 轉址）
print("\n[2/4] Normalizing URLs...")
import normalize_urls
normalize_urls.main()

# Update sitemap
print("\n[3/4] Updating sitemap...")
exec(open('update_sitemap.py', encoding='utf-8').read())

# Build and deploy
print("\n[4/4] Building and deploying...")
dist = 'dist'
if os.path.exists(dist):
    shutil.rmtree(dist)
os.makedirs(f'{dist}/articles', exist_ok=True)
os.makedirs(f'{dist}/assets', exist_ok=True)

for f in ['index.html', 'sitemap.xml', 'robots.txt', '.nojekyll',
          'jp.html', 'kr.html', 'tw.html', 'eu.html', 'oce.html']:
    if os.path.exists(f):
        shutil.copy2(f, f'{dist}/{f}')
for d in ['articles', 'assets', 'guides', 'jp']:
    if os.path.isdir(d):
        shutil.copytree(d, f'{dist}/{d}', dirs_exist_ok=True)

env = os.environ.copy()
# CF token：優先環境變數，其次讀本機 token 檔（不可寫死在程式或排程參數裡）
if not env.get('CLOUDFLARE_API_TOKEN'):
    for _tp in (os.path.join(_REPO_DIR, '.cf-token'),
                r'C:\Users\User\Documents\網站製作\.cf-token'):
        if os.path.exists(_tp):
            with open(_tp, encoding='utf-8') as _fh:
                env['CLOUDFLARE_API_TOKEN'] = _fh.read().strip()
            break
npx_path = _abs('npx')
# 用 utf-8 + errors=replace 避免 Windows 預設 GBK 解碼中文字報 UnicodeDecodeError
result = subprocess.run(
    [npx_path, 'wrangler', 'pages', 'deploy', dist, '--project-name', 'travel-guide-esimart', '--branch', 'main', '--commit-dirty=true'],
    env=env, capture_output=True, text=True, encoding='utf-8', errors='replace'
)
out = result.stdout or ''
print(out[-500:] if len(out) > 500 else out)
deploy_ok = result.returncode == 0
if not deploy_ok:
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

# 部署失敗要讓排程看到非 0，否則會一直誤判為成功
if not deploy_ok:
    sys.exit(1)

