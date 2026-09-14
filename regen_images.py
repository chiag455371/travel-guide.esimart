# -*- coding: utf-8 -*-
"""Fix: generate truly unique picsum seeds for every image URL."""
import re, glob, os, hashlib

def make_seed(filepath, occurrence):
    """Generate a unique seed from absolute file path + occurrence number."""
    data = f"{os.path.abspath(filepath)}|{occurrence}"
    h = hashlib.sha256(data.encode()).hexdigest()
    return 10000 + (int(h[:8], 16) % 90000)

def fix_file(path):
    """Replace all picsum URLs with unique seeds."""
    with open(path, encoding='utf-8') as f:
        content = f.read()
    
    # Match complete picsum URLs including the protocol
    pattern = re.compile(r'(https://picsum\.photos/seed/)(\d+)/(\d+)/(\d+)')
    
    occurrences = 0
    def replacer(m):
        nonlocal occurrences
        prefix = m.group(1)  # 'https://picsum.photos/seed/'
        w = m.group(3)       # width
        h = m.group(4)       # height
        seed = make_seed(path, occurrences)
        occurrences += 1
        return f'{prefix}{seed}/{w}/{h}'
    
    new_content = pattern.sub(replacer, content)
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return occurrences
    return 0

def main():
    print("Regenerating unique image seeds...")
    total_files = 0
    total_images = 0
    
    # Process all HTML files
    for path in sorted(glob.glob('**/*.html', recursive=True)):
        if 'dist/' in path or '__pycache__' in path:
            continue
        count = fix_file(path)
        if count > 0:
            total_files += 1
            total_images += count
            print(f"  {os.path.basename(path)}: {count} images -> unique seeds")
    
    print(f"\nTotal: {total_files} files, {total_images} images fixed")
    
    # Verify: no duplicates within any file
    print("\nVerifying uniqueness...")
    has_dupes = False
    for path in glob.glob('**/*.html', recursive=True):
        if 'dist/' in path: continue
        with open(path, encoding='utf-8') as f:
            c = f.read()
        seeds = re.findall(r'picsum\.photos/seed/(\d+)/', c)
        if len(seeds) != len(set(seeds)):
            dupes = [s for s in seeds if seeds.count(s) > 1]
            print(f"  DUPLICATE in {os.path.basename(path)}: {set(dupes)}")
            has_dupes = True
    
    if not has_dupes:
        print("All seeds unique within each file ✓")
    
    # Cross-file check
    all_seeds = {}
    for path in glob.glob('**/*.html', recursive=True):
        if 'dist/' in path: continue
        with open(path, encoding='utf-8') as f:
            c = f.read()
        seeds = re.findall(r'picsum\.photos/seed/(\d+)/', c)
        for s in seeds:
            if s not in all_seeds:
                all_seeds[s] = []
            all_seeds[s].append(os.path.basename(path))
    
    cross_dupes = {s: list(set(files)) for s, files in all_seeds.items() if len(set(files)) > 1}
    print(f"Seeds shared across files: {len(cross_dupes)} (acceptable)")

if __name__ == '__main__':
    main()
