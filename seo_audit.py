#!/usr/bin/env python3
"""
SEO Audit Script - Checks all articles for SEO/GEO best practices.
Usage: python seo_audit.py [--fix]
"""
import os, re, argparse, json

REPO = r'C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo'
ARTICLES_DIR = os.path.join(REPO, 'articles')
BASE = 'https://chiag455371.github.io/travel-guide.esimart'

# E-E-A-T scoring rubric
SCORES = {}
ISSUES = []

def audit_article(slug, content):
    """Audit a single article for SEO and E-E-A-T."""
    issues = []
    score = 100
    
    # 1. Title check
    title_match = re.search(r'<title>(.*?)</title>', content)
    if not title_match:
        issues.append(('CRITICAL', 'Missing <title> tag'))
        score -= 20
    else:
        title = title_match.group(1)
        if len(title) < 30:
            issues.append(('WARNING', f'Title too short: {len(title)} chars'))
            score -= 5
        if '旅遊通 eSIM' not in title:
            issues.append(('INFO', 'Title missing brand name'))
    
    # 2. Meta description
    meta_match = re.search(r'<meta name="description" content="(.*?)">', content)
    if not meta_match:
        issues.append(('CRITICAL', 'Missing meta description'))
        score -= 15
    elif len(meta_match.group(1)) < 120:
        issues.append(('WARNING', f'Meta description too short: {len(meta_match.group(1))} chars'))
        score -= 5
    
    # 3. Canonical URL
    canonical = re.search(r'<link rel="canonical" href="(.*?)">', content)
    if not canonical:
        issues.append(('CRITICAL', 'Missing canonical URL'))
        score -= 10
    
    # 4. Open Graph tags
    og_title = re.search(r'<meta property="og:title" content="(.*?)">', content)
    og_desc = re.search(r'<meta property="og:description" content="(.*?)">', content)
    og_image = re.search(r'<meta property="og:image" content="(.*?)">', content)
    if not og_title:
        issues.append(('WARNING', 'Missing og:title'))
        score -= 5
    if not og_image:
        issues.append(('WARNING', 'Missing og:image'))
        score -= 5
    
    # 5. Schema.org structured data
    if 'application/ld+json' not in content:
        issues.append(('CRITICAL', 'Missing JSON-LD structured data'))
        score -= 15
    
    # 6. Image alt text
    imgs = re.findall(r'<img[^>]+alt="(.*?)"', content)
    empty_alts = [a for a in imgs if not a.strip()]
    if empty_alts:
        issues.append(('WARNING', f'{len(empty_alts)} images missing alt text'))
        score -= len(empty_alts) * 2
    
    # 7. Loading lazy on images
    lazy_imgs = len(re.findall(r'loading="lazy"', content))
    total_imgs = len(re.findall(r'<img[^>]+src=', content))
    if total_imgs > 0 and lazy_imgs < total_imgs:
        issues.append(('INFO', f'{total_imgs - lazy_imgs} images missing loading="lazy"'))
    
    # 8. Content quality - check for placeholder text
    placeholder_patterns = ['Lorem ipsum', 'lorem ipsum', 'placeholder', 'FILLER']
    for pat in placeholder_patterns:
        if pat.lower() in content.lower():
            issues.append(('WARNING', f'Contains placeholder text: "{pat}"'))
            score -= 10
    
    # 9. Internal linking to eSIM distributor
    if 'travel-guide.esimart.cc/goods' not in content:
        issues.append(('WARNING', 'Missing eSIM affiliate link'))
        score -= 10
    
    # 10. Reading time estimate
    read_time = re.search(r'約 (\d+) 分鐘閱讀', content)
    if not read_time:
        issues.append(('INFO', 'Missing estimated read time'))
    
    # 11. Author/Expertise signal
    if '編輯團隊' not in content and '作者' not in content:
        issues.append(('INFO', 'No author attribution found'))
    
    # 12. FAQ section (good for featured snippets)
    if '<details>' not in content and '<FAQ' not in content.upper():
        issues.append(('INFO', 'No FAQ section - missing featured snippet opportunity'))
        score -= 5
    
    return max(0, score), issues

def main():
    parser = argparse.ArgumentParser(description='SEO Audit for travel guide articles')
    parser.add_argument('--fix', action='store_true', help='Auto-fix issues')
    args = parser.parse_args()
    
    files = sorted([f for f in os.listdir(ARTICLES_DIR) if f.endswith('.html') and f != 'index.html'])
    total_score = 0
    critical_count = 0
    warning_count = 0
    
    print(f'Auditing {len(files)} articles...\n')
    
    for f in files:
        slug = f.replace('.html', '')
        content = open(os.path.join(ARTICLES_DIR, f), encoding='utf-8').read()
        score, issues = audit_article(slug, content)
        total_score += score
        
        if any(sev == 'CRITICAL' for sev, _ in issues):
            critical_count += 1
        if any(sev == 'WARNING' for sev, _ in issues):
            warning_count += 1
        
        if issues:
            print(f'  [{score:3d}/100] {slug}')
            for sev, msg in issues:
                icon = {'CRITICAL': '❌', 'WARNING': '⚠️', 'INFO': 'ℹ️'}[sev]
                print(f'       {icon} {msg}')
    
    avg_score = total_score / len(files) if files else 0
    print(f'\n{"="*50}')
    print(f'SUMMARY')
    print(f'  Total articles: {len(files)}')
    print(f'  Average SEO score: {avg_score:.1f}/100')
    print(f'  Articles with critical issues: {critical_count}')
    print(f'  Articles with warnings: {warning_count}')
    print(f'{"="*50}')
    
    # Save audit report
    report = {
        'total_articles': len(files),
        'average_score': round(avg_score, 1),
        'critical_count': critical_count,
        'warning_count': warning_count,
        'audited_at': os.popen('date /T').read().strip()
    }
    with open(os.path.join(REPO, 'seo_audit_report.json'), 'w', encoding='utf-8') as fp:
        json.dump(report, fp, ensure_ascii=False, indent=2)
    print(f'\nReport saved to: seo_audit_report.json')

if __name__ == '__main__':
    main()
