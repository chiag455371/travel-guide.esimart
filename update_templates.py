# -*- coding: utf-8 -*-
"""Update generators to include extra_templates_4."""
import re

# Update daily_articles.py
path1 = 'daily_articles.py'
content1 = open(path1, encoding='utf-8').read()
if 'EXTRA_TEMPLATES_4' not in content1:
    content1 = content1.replace(
        'from extra_templates_3 import EXTRA_TEMPLATES_3\n',
        'from extra_templates_3 import EXTRA_TEMPLATES_3\nfrom extra_templates_4 import EXTRA_TEMPLATES_4\n'
    )
    content1 = content1.replace(
        'all_templates = TEMPLATES + EXTRA_TEMPLATES_SRC + EXTRA_TEMPLATES_2 + EXTRA_TEMPLATES_3',
        'all_templates = TEMPLATES + EXTRA_TEMPLATES_SRC + EXTRA_TEMPLATES_2 + EXTRA_TEMPLATES_3 + EXTRA_TEMPLATES_4'
    )
    open(path1, 'w', encoding='utf-8').write(content1)
    print(f'{path1}: updated')
else:
    print(f'{path1}: already up to date')

# Update daily_generator_v2.py
path2 = 'daily_generator_v2.py'
content2 = open(path2, encoding='utf-8').read()
if 'EXTRA_TEMPLATES_4' not in content2:
    content2 = content2.replace(
        'from extra_templates_3 import EXTRA_TEMPLATES_3\n',
        'from extra_templates_3 import EXTRA_TEMPLATES_3\n    from extra_templates_4 import EXTRA_TEMPLATES_4\n'
    )
    content2 = content2.replace(
        'all_templates = BASE_TEMPLATES + EXTRA_1 + EXTRA_TEMPLATES_2 + EXTRA_TEMPLATES_3',
        'all_templates = BASE_TEMPLATES + EXTRA_1 + EXTRA_TEMPLATES_2 + EXTRA_TEMPLATES_3 + EXTRA_TEMPLATES_4'
    )
    open(path2, 'w', encoding='utf-8').write(content2)
    print(f'{path2}: updated')
else:
    print(f'{path2}: already up to date')

# Count templates
from extra_templates import EXTRA_TEMPLATES as ET1
from extra_templates_2 import EXTRA_TEMPLATES_2
from extra_templates_3 import EXTRA_TEMPLATES_3
from extra_templates_4 import EXTRA_TEMPLATES_4
base = 6  # BASE_TEMPLATES in daily_generator_v2.py
total = base + len(ET1) + len(EXTRA_TEMPLATES_2) + len(EXTRA_TEMPLATES_3) + len(EXTRA_TEMPLATES_4)
print(f'\nTemplate pool: {total} templates')
print(f'  Base: {base}')
print(f'  Extra 1: {len(ET1)}')
print(f'  Extra 2: {len(EXTRA_TEMPLATES_2)}')
print(f'  Extra 3: {len(EXTRA_TEMPLATES_3)}')
print(f'  Extra 4: {len(EXTRA_TEMPLATES_4)}')
