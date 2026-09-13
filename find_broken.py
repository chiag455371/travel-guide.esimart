import os, re
BASE = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"
broken = []
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
    for fn in files:
        if not fn.endswith(".html"): continue
        fp = os.path.join(root, fn)
        with open(fp, "r", encoding="utf-8") as f:
            c = f.read()
        for m in re.finditer(r"https://images\.unsplash\.com/[^\s\"'\x3c\x3e]+", c):
            broken.append((os.path.relpath(fp, BASE), m.group()))
for fn, url in broken:
    print(f"{fn}: {url[:90]}")
print(f"\nTotal: {len(broken)} broken URLs")
