# -*- coding: utf-8 -*-
import json, re, os

BASE = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"

# Load new templates from JSON
with open(BASE + r"\new_templates.json", "r", encoding="utf-8") as f:
    new_templates = json.load(f)

# Read current daily_articles.py
with open(BASE + r"\daily_articles.py", "r", encoding="utf-8") as f:
    content = f.read()

# Find all existing slugs in TEMPLATES
existing_slugs = set(re.findall(r'"slug":\s*"([^"]+)"', content))
available = [t for t in new_templates if t["slug"] not in existing_slugs]
print(f"New unique templates to add: {len(available)}")

if not available:
    print("All templates already exist!")
else:
    # Find insertion point - after the last template in TEMPLATES list
    templates_match = re.search(r"TEMPLATES = \[(.*?)\]\n\ndef ", content, re.DOTALL)
    if templates_match:
        old_list = templates_match.group(1)
        new_entries = []
        for t in available:
            tags_str = json.dumps(t["tags"], ensure_ascii=False)
            h2s_str = json.dumps(t["h2s"], ensure_ascii=False)
            entry = '    {"slug": "%s", "region": "%s", "title": %s, "desc": %s, "h2s": %s, "tags": %s},' % (
                t["slug"], t["region"],
                json.dumps(t["title"], ensure_ascii=False),
                json.dumps(t["desc"], ensure_ascii=False),
                h2s_str, tags_str
            )
            new_entries.append(entry)
        
        new_list = old_list.rstrip().rstrip(",") + "\n" + ",\n".join(new_entries) + "\n"
        new_content = content[:templates_match.start(1)] + new_list + content[templates_match.end(1):]
        
        with open(BASE + r"\daily_articles.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Added {len(available)} new templates to daily_articles.py")
    else:
        print("Could not find TEMPLATES list")
        print("Searching for TEMPLATES...")
        if "TEMPLATES = [" in content:
            print("Found TEMPLATES = [ marker")
        else:
            print("TEMPLATES = [ NOT found")
