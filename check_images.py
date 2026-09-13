import os, re
BASE = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"
for fn in ["articles/jp-tokyo-tower.html", "articles/tw-taipei-101.html", "articles/eu-paris.html", "index.html", "articles/index.html"]:
    fp = os.path.join(BASE, fn)
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()
    imgs = re.findall(r"src=\"([^\"]+)\"", c)
    og_imgs = re.findall(r'og:image.*?content="([^"]+)"', c)
    all_imgs = imgs + og_imgs
    bad = [u for u in all_imgs if "unsplash.com/photo-" in u or "loremflickr.com/600x400" not in u and "loremflickr.com/1200/630" not in u and "loremflickr.com/600/400" not in u]
    lf = [u for u in all_imgs if "loremflickr.com" in u]
    print(f"{fn}: total={len(all_imgs)}, lf={len(lf)}, non_lf_bad={[u for u in all_imgs if 'loremflickr' not in u and 'unsplash' not in u and u.startswith('http')]}")
    if bad:
        for b in bad[:3]: print(f"  BAD: {b[:80]}")
