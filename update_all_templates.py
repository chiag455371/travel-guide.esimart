# -*- coding: utf-8 -*-
"""Update generators to include extra_templates_6."""
import re

for path in ['daily_articles.py', 'daily_generator_v2.py']:
    content = open(path, encoding='utf-8').read()
    if 'EXTRA_TEMPLATES_6' not in content:
        # Add import
        if 'extra_templates_5' in content:
            content = content.replace(
                'from extra_templates_5 import EXTRA_TEMPLATES_5',
                'from extra_templates_5 import EXTRA_TEMPLATES_5\nfrom extra_templates_6 import EXTRA_TEMPLATES_6'
            )
        else:
            content = content.replace(
                'from extra_templates_4 import EXTRA_TEMPLATES_4',
                'from extra_templates_4 import EXTRA_TEMPLATES_4\nfrom extra_templates_5 import EXTRA_TEMPLATES_5\nfrom extra_templates_6 import EXTRA_TEMPLATES_6'
            )
        # Add to all_templates line
        content = content.replace(
            'EXTRA_TEMPLATES_5',
            'EXTRA_TEMPLATES_5 + EXTRA_TEMPLATES_6'
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
total = 6 + len(ET1) + len(EXTRA_TEMPLATES_2) + len(EXTRA_TEMPLATES_3) + len(EXTRA_TEMPLATES_4) + len(EXTRA_TEMPLATES_5) + len(EXTRA_TEMPLATES_6)
print(f'\nTotal template pool: {total} templates')
print(f'  Base: 6')
print(f'  Extra 1: {len(ET1)}')
print(f'  Extra 2: {len(EXTRA_TEMPLATES_2)}')
print(f'  Extra 3: {len(EXTRA_TEMPLATES_3)}')
print(f'  Extra 4: {len(EXTRA_TEMPLATES_4)}')
print(f'  Extra 5: {len(EXTRA_TEMPLATES_5)}')
print(f'  Extra 6: {len(EXTRA_TEMPLATES_6)}')

import os
files = [f for f in os.listdir('articles') if f.endswith('.html')]
used = len(files)
remaining = total - used
print(f'\nArticles: {used}, Remaining templates: {remaining}')
print(f'Days of generation remaining: ~{remaining // 20}')
