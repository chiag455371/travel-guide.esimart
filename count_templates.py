import re
with open(r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo\daily_articles.py", "r", encoding="utf-8") as f:
    c = f.read()
templates = re.findall(r'^\s+\{"slug":\s*"([^"]+)"', c, re.M)
print(f"Templates in daily_articles.py: {len(templates)}")
for t in templates:
    print(f"  {t}")
