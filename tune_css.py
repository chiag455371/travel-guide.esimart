# -*- coding: utf-8 -*-
import pathlib
p = pathlib.Path('assets/style.css')
s = p.read_text(encoding='utf-8')
# 1) brighter, cleaner neutrals (softer cream, less muddy borders)
s = s.replace('--bg:#FFFDF9;', '--bg:#FFFEFC;')
s = s.replace('--bg-alt:#FFF8F3;', '--bg-alt:#FFF9F4;')
s = s.replace('--panel-border:#F5E6D8;', '--panel-border:#F3EDE6;')
s = s.replace('--text-soft:#5A5047;', '--text-soft:#5B5550;')
s = s.replace('--text-muted:#A09080;', '--text-muted:#9A9188;')
# 2) slightly warmer accent, cleaner hover
s = s.replace('--accent:#E06030;', '--accent:#E8622C;')
# 3) lift card shadow to feel crisper
s = s.replace('--shadow-card:0 2px 12px rgba(0,0,0,.06)', '--shadow-card:0 3px 14px rgba(0,0,0,.07)')
# 4) article img: add subtle border radius already there; ensure max-height removed so photo shows fully in hero card
p.write_text(s, encoding='utf-8')
print('done')
