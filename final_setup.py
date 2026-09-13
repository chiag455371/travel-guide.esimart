# -*- coding: utf-8 -*-
"""Final setup - add all templates and verify."""
import re, os

for path in ['daily_generator_v2.py', 'daily_articles.py']:
    content = open(path, encoding='utf-8').read()
    if 'EXTRA_TEMPLATES_8' not in content:
        content = content.replace(
            'from extra_templates_7 import EXTRA_TEMPLATES_7',
            'from extra_templates_7 import EXTRA_TEMPLATES_7\nfrom extra_templates_8 import EXTRA_TEMPLATES_8'
        )
        content = content.replace(
            'EXTRA_TEMPLATES_7',
            'EXTRA_TEMPLATES_7 + EXTRA_TEMPLATES_8'
        )
        open(path, 'w', encoding='utf-8').write(content)
        print(f'{path}: updated')

# Count templates
from extra_templates import EXTRA_TEMPLATES as ET1
from extra_templates_2 import EXTRA_TEMPLATES_2
from extra_templates_3 import EXTRA_TEMPLATES_3
from extra_templates_4 import EXTRA_TEMPLATES_4
from extra_templates_5 import EXTRA_TEMPLATES_5
from extra_templates_6 import EXTRA_TEMPLATES_6
from extra_templates_7 import EXTRA_TEMPLATES_7
from extra_templates_8 import EXTRA_TEMPLATES_8
total = 6 + len(ET1) + len(EXTRA_TEMPLATES_2) + len(EXTRA_TEMPLATES_3) + len(EXTRA_TEMPLATES_4) + len(EXTRA_TEMPLATES_5) + len(EXTRA_TEMPLATES_6) + len(EXTRA_TEMPLATES_7) + len(EXTRA_TEMPLATES_8)
print(f'Total template pool: {total}')

files = [f for f in os.listdir('articles') if f.endswith('.html')]
used = len(files)
remaining = total - used
print(f'Articles: {used}, Remaining: {remaining}')
print(f'Days of generation: ~{remaining // 20}')
