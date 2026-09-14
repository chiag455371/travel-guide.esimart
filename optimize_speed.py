# -*- coding: utf-8 -*-
"""Compress CSS (strip comments/blank lines/extra spaces) and limit homepage cards to 6."""
import re, os

# 1. Compress style.css
css = open('assets/style.css', encoding='utf-8').read()
before = len(css)
# remove /* */ comments
css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
# remove blank lines
css = '\n'.join(line for line in css.split('\n') if line.strip())
# collapse multiple spaces
css = re.sub(r'  +', ' ', css)
after = len(css)
open('assets/style.css', 'w', encoding='utf-8').write(css)
print(f'CSS compressed: {before} -> {after} bytes ({(100 - after/before*100):.1f}% reduction)')

# 2. Limit homepage to 6 cards
c = open('index.html', encoding='utf-8').read()
# find all card blocks
card_pat = re.compile(
    r'(<a href="https://travel-guide-esimart\.pages\.dev/articles/[a-z0-9\-]+\.html" '
    r'class="article-card">.*?</a>\s*)', re.S)
matches = list(card_pat.finditer(c))
print(f'found {len(matches)} cards in index.html')

if len(matches) > 6:
    # remove cards after the 6th, keeping the section structure
    # find the section containing the cards
    first_end = matches[5].end()
    # Find the container div close tag after the last card
    # Remove all remaining card blocks
    remaining = matches[6:]
    for m in reversed(remaining):
        c = c[:m.start()] + c[m.end():]
    # Clean up extra whitespace
    c = re.sub(r'\n{3,}', '\n\n', c)
    open('index.html', 'w', encoding='utf-8').write(c)
    remaining2 = len(re.findall(r'article-card', c))
    print(f'index.html now has {remaining2} cards')
else:
    print('index.html already has <= 6 cards, no change')

print('done')
