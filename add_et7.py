# -*- coding: utf-8 -*-
"""Add EXTRA_TEMPLATES_7 to all generators."""
import re

for path in ['daily_generator_v2.py', 'daily_articles.py']:
    content = open(path, encoding='utf-8').read()
    if 'EXTRA_TEMPLATES_7' not in content:
        content = content.replace(
            'from extra_templates_6 import EXTRA_TEMPLATES_6',
            'from extra_templates_6 import EXTRA_TEMPLATES_6\nfrom extra_templates_7 import EXTRA_TEMPLATES_7'
        )
        content = content.replace(
            'EXTRA_TEMPLATES_5 + EXTRA_TEMPLATES_6',
            'EXTRA_TEMPLATES_5 + EXTRA_TEMPLATES_6 + EXTRA_TEMPLATES_7'
        )
        open(path, 'w', encoding='utf-8').write(content)
        print(f'{path}: updated')
    else:
        print(f'{path}: already up to date')

# Count templates
from extra_templates import EXTRA_TEMPLATES as ET1
from extra_templates_2 import EXTRA_TEMPLATES_2
from extra_templates_3 import EXTRA_TEMPLATES_3
from extra_templates_4 import EXTRA_TEMPLATES_4
from extra_templates_5 import EXTRA_TEMPLATES_5
from extra_templates_6 import EXTRA_TEMPLATES_6
from extra_templates_7 import EXTRA_TEMPLATES_7
total = 6 + len(ET1) + len(EXTRA_TEMPLATES_2) + len(EXTRA_TEMPLATES_3) + len(EXTRA_TEMPLATES_4) + len(EXTRA_TEMPLATES_5) + len(EXTRA_TEMPLATES_6) + len(EXTRA_TEMPLATES_7)
print(f'\nTotal template pool: {total}')

import os
files = [f for f in os.listdir('articles') if f.endswith('.html')]
used = len(files)
remaining = total - used
print(f'Articles: {used}, Remaining: {remaining}')
print(f'Days of generation: ~{remaining // 20}')
