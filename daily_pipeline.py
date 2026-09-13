# -*- coding: utf-8 -*-
"""Daily article generator - full pipeline with verification."""
import os, sys, subprocess, datetime

BASE = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"
os.chdir(BASE)

print("=" * 50)
print("Daily Article Generator - " + datetime.date.today().isoformat())
print("=" * 50)

# Step 1: Generate new articles
print("\n[1/4] Generating articles...")
try:
    result = subprocess.run(
        [sys.executable, "daily_articles.py"],
        capture_output=True, text=True, encoding="utf-8"
    )
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr[:200])
except Exception as e:
    print("ERROR generating articles:", e)
    sys.exit(1)

# Step 2: Update sitemap
print("\n[2/4] Updating sitemap...")
try:
    result = subprocess.run(
        [sys.executable, "update_sitemap.py"],
        capture_output=True, text=True, encoding="utf-8"
    )
    print(result.stdout.strip())
except Exception as e:
    print("ERROR updating sitemap:", e)

# Step 3: Verify images
print("\n[3/4] Verifying images...")
import re, urllib.request
articles_dir = os.path.join(BASE, "articles")
broken = 0
total_imgs = 0
for fn in os.listdir(articles_dir):
    if not fn.endswith('.html'):
        continue
    with open(os.path.join(articles_dir, fn), 'r', encoding='utf-8') as f:
        content = f.read()
    urls = re.findall(r'src="(https://loremflickr\.com/[^"]+)"', content)
    for url in urls:
        total_imgs += 1
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            resp = urllib.request.urlopen(req, timeout=5)
            if resp.status != 200 or len(resp.read()) < 1000:
                broken += 1
        except:
            broken += 1

print(f"  Images checked: {total_imgs}, Broken: {broken}")

# Step 4: Commit and push
print("\n[4/4] Committing and pushing...")
try:
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(["git", "commit", "-m", f"daily articles {datetime.date.today().isoformat()}"], check=True, capture_output=True)
    result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if result.returncode == 0:
        print("  Pushed successfully!")
    else:
        print("  Push warning:", result.stderr[:100] if result.stderr else "no error")
except subprocess.CalledProcessError as e:
    print("Git error (may be no changes):", str(e)[:100])
except Exception as e:
    print("ERROR:", e)

print("\n" + "=" * 50)
print("Daily run complete!")
print("=" * 50)
