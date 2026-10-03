def process(fp):
    print(f'Processing {fp}...')
    with open(fp, "r", encoding="utf-8") as f:
        html = f.read()
    pat =     pat = chr(60)+chr(34)+chr(105)+chr(109)+chr(103)+chr(32)+chr(99)+chr(108)+chr(97)+chr(115)+chr(115)+chr(61)+chr(34)+chr(99)+chr(97)+chr(114)+chr(100)+chr(45)+chr(105)+chr(109)+chr(103)+chr(34)+chr(93)+chr(94)+chr(62)+chr(93)+chr(43)+chr(34)+chr(97)+chr(108)+chr(116)+chr(61)+chr(34)+chr(40)+chr(92)+chr(34)+chr(41)+chr(43)+chr(34)+chr(34)+chr(93)+chr(94)+chr(62)+chr(93)+chr(42)+chr(34)+chr(115)+chr(114)+chr(99)+chr(61)+chr(34)+chr(40)+chr(92)+chr(34)+chr(41)+chr(43)+chr(34)+chr(34)
    ms = list(re.finditer(pat, html))
    print(f'  Found {len(ms)} cards')
    reps = []
    for m in ms:
        alt, old = m.group(1), m.group(2)
        kw = get_kw(alt)
        nw = get_pexels(kw)
        if nw and nw != old:
            reps.append((old, nw, kw))
            print(f'  [{kw}] OK')
        elif nw == old:
            print(f'  [{kw}] SAME')
        else:
            print(f'  [{kw}] NONE')
    for o, n, k in reps:
        html = html.replace(o, n)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(html)
    print(f'  Replaced {len(reps)}, saved')

for r in ["jp","kr","eu","tw","oce"]:
    p = os.path.join("articles", f'{r}.html')
    if os.path.exists(p):
        process(p)
    else:
        print(f'SKIP {p}')

with open(cache_file, "w", encoding="utf-8") as f:
    json.dump(cache, f, ensure_ascii=False, indent=2)
print(f'Done. Cache: {len(cache)} entries')
