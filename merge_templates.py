# -*- coding: utf-8 -*-
"""Merge new templates into daily_articles.py"""
import json, re, os

BASE = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"

# Load new templates from JSON
with open(BASE + r"\new_templates.json", "r", encoding="utf-8") as f:
    new_templates = json.load(f)

# Read current daily_articles.py
with open(BASE + r"\daily_articles.py", "r", encoding="utf-8") as f:
    content = f.read()

# Find the TEMPLATES list and add new entries
# Look for the last template entry before the closing ]
# Pattern: find the last "slug" entry and add after it
last_slug_match = None
for m in re.finditer(r'"slug":\s*"([^"]+)"', content):
    last_slug_match = m

if last_slug_match:
    # Find the position after the last template (look for the next }, )
    insert_pos = last_slug_match.end()
    # Find the closing of that dict
    # We need to find the pattern }, ] or },\n]
    remaining = content[insert_pos:]
    # Find the end of the last dict
    brace_count = 0
    end_pos = 0
    for i, ch in enumerate(remaining):
        if ch == '{':
            brace_count += 1
        elif ch == '}':
            brace_count -= 1
            if brace_count == 0:
                end_pos = i
                break
    # Find the closing bracket
    after_dict = remaining[end_pos+1:]
    bracket_pos = after_dict.find(']')
    
    # Insert new templates before the closing ]
    new_entries = []
    for t in new_templates:
        # Convert to Python dict format
        tags_str = json.dumps(t["tags"], ensure_ascii=False)
        h2s_str = json.dumps(t["h2s"], ensure_ascii=False)
        entry = f'    {{"slug": "{t["slug"]}", "region": "{t["region"]}", "title": {json.dumps(t["title"], ensure_ascii=False)}, "desc": {json.dumps(t["desc"], ensure_ascii=False)}, "h2s": {h2s_str}, "tags": {tags_str}}},'
        new_entries.append(entry)
    
    new_content = content[:insert_pos+end_pos+1+bracket_pos] + "\n" + "\n".join(new_entries) + "\n" + content[insert_pos+end_pos+1+bracket_pos:]
    
    with open(BASE + r"\daily_articles.py", "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Added {len(new_templates)} new templates")
else:
    print("Could not find insertion point")
