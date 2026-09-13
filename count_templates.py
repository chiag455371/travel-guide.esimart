# -*- coding: utf-8 -*-
"""Count templates and check generator."""
import re

from extra_templates import EXTRA_TEMPLATES as ET1
from extra_templates_2 import EXTRA_TEMPLATES_2
from extra_templates_3 import EXTRA_TEMPLATES_3
from extra_templates_4 import EXTRA_TEMPLATES_4
from extra_templates_5 import EXTRA_TEMPLATES_5
from extra_templates_6 import EXTRA_TEMPLATES_6

print(f'ET1: {len(ET1)}')
print(f'ET2: {len(EXTRA_TEMPLATES_2)}')
print(f'ET3: {len(EXTRA_TEMPLATES_3)}')
print(f'ET4: {len(EXTRA_TEMPLATES_4)}')
print(f'ET5: {len(EXTRA_TEMPLATES_5)}')
print(f'ET6: {len(EXTRA_TEMPLATES_6)}')
total = 6 + len(ET1) + len(EXTRA_TEMPLATES_2) + len(EXTRA_TEMPLATES_3) + len(EXTRA_TEMPLATES_4) + len(EXTRA_TEMPLATES_5) + len(EXTRA_TEMPLATES_6)
print(f'Total: {total}')

# Check what the generator counts
content = open('daily_generator_v2.py', encoding='utf-8').read()
# Find the line that calculates total templates
for m in re.finditer(r'.*template.*', content, re.IGNORECASE):
    print(m.group().strip())
