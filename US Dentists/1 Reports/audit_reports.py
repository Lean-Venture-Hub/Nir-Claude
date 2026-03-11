#!/usr/bin/env python3
"""Audit all generated US dentist report folders for quality issues.

Adapted from Dentists/reports/audit_reports.py for English/US dentists.

Checks:
  1. Generic/fake content (template placeholders left behind)
  2. Broken images and links
  3. Name duplication in hero section
  4. Weird/suspicious content (empty sections, garbled text)
  5. Video quality (file size checks)
  6. Screenshots exist
  7. content.md has real data
  8. proposal.html exists and is clean
"""

import csv, os, re, sys, json
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
CSV_PATH = os.path.join(SCRIPT_DIR, "Inbox_list", "first_batch.csv")
REVIEWS_PATH = os.path.join(SCRIPT_DIR, "Inbox_list", "reviews.json")

# ─── Known fake/placeholder content ──────────────────────────────────
FAKE_MARKERS = [
    'Smile Plus Dental', 'Smile Plus',
    'Dr. Michelle Levy', 'Michelle Levy', 'Dr. Levy',
    'Noa Cohen', 'Yossi Abraham', 'Shira David',  # fake reviewer names
    '03-555-1234',
    '45 Rothschild Blvd', '45 Rothschild',
    'Lorem ipsum', 'dolor sit amet',
]

FAKE_REVIEW_SNIPPETS = [
    'Dr. Levy changed my life',
    'I had dental implants at this clinic',
    'Amazing place! I came for the first time',
]

# Placeholder rating/review count
FAKE_RATING_PATTERNS = [
    r'>4\.9<',       # template default rating
    r'>187<',        # template default review count
    r'187\s*Reviews',
    r'187\+\s*Reviews',
]


def load_clinic_data():
    """Load real clinic data for cross-referencing."""
    clinics = {}
    if not os.path.exists(CSV_PATH):
        return clinics
    with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            clinics[row['name'].strip()] = row
    return clinics


def load_reviews():
    """Load reviews from JSON."""
    if not os.path.exists(REVIEWS_PATH):
        return {}
    with open(REVIEWS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ''


def check_fake_content(html, folder_name):
    """Check 1: Find any leftover template/fake content."""
    issues = []
    for marker in FAKE_MARKERS:
        if marker in html:
            issues.append(f"Fake content found: \"{marker}\"")

    for snippet in FAKE_REVIEW_SNIPPETS:
        if snippet in html:
            issues.append(f"Fake review text: \"{snippet[:40]}...\"")

    for pattern in FAKE_RATING_PATTERNS:
        if re.search(pattern, html):
            issues.append(f"Fake rating/count pattern: {pattern}")

    return issues


def check_images_links(html, folder_path):
    """Check 2: Find broken image references and links."""
    issues = []

    img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
    for src in img_srcs:
        if src.startswith('http') or src.startswith('data:'):
            continue
        img_path = os.path.normpath(os.path.join(folder_path, src))
        if not os.path.exists(img_path):
            issues.append(f"Missing image: {src}")

    hrefs = re.findall(r'href=["\']([^"\'#]+)["\']', html)
    for href in hrefs:
        if href.startswith('http') or href.startswith('mailto:') or href.startswith('tel:'):
            continue
        if href.startswith('javascript:'):
            continue
        link_path = os.path.normpath(os.path.join(folder_path, href))
        if not os.path.exists(link_path):
            if href.endswith('.html') or '.' not in os.path.basename(href):
                issues.append(f"Broken link: {href}")

    return issues


def check_name_duplication(html, folder_name):
    """Check 3: Detect name appearing twice in hero section."""
    issues = []

    hero = html[:6000]
    titles = re.findall(r'<h[12][^>]*>(.*?)</h[12]>', hero, re.DOTALL)

    for title in titles:
        clean = re.sub(r'<[^>]+>', '|', title)
        parts = [p.strip() for p in clean.split('|') if p.strip()]

        for i in range(len(parts)):
            for j in range(i + 1, len(parts)):
                a, b = parts[i], parts[j]
                if len(a) > 3 and len(b) > 3:
                    if a == b:
                        issues.append(f"Exact duplicate in hero: \"{a}\"")
                    elif a in b and len(a) > 5 and len(a) / len(b) > 0.6:
                        issues.append(f"Near-duplicate in hero: \"{a}\" inside \"{b}\"")

    hero_text_blocks = re.findall(r'>([^<]{4,60})<', hero)
    seen = {}
    for block in hero_text_blocks:
        block = block.strip()
        if len(block) > 5 and not block.startswith('{') and not block.startswith('/*'):
            if block in seen:
                seen[block] += 1
            else:
                seen[block] = 1
    for text, count in seen.items():
        if count > 2 and not re.match(r'^[\s\d\.\,]+$', text):
            issues.append(f"Text repeated {count}x: \"{text[:40]}\"")

    return issues


def check_weird_content(html, folder_path):
    """Check 4: Detect weird/suspicious content."""
    issues = []

    if len(html) < 500:
        issues.append(f"Suspiciously short HTML ({len(html)} chars)")

    template_tags = re.findall(r'\{\{[^}]+\}\}|\{%[^%]+%\}', html)
    for tag in template_tags[:3]:
        issues.append(f"Template tag in output: {tag[:30]}")

    if '\ufffd' in html:
        issues.append("Garbled characters (replacement char) found")

    # Check for Hebrew text that shouldn't be there (template leftovers)
    hebrew_blocks = re.findall(r'[\u0590-\u05FF]{5,}', html)
    if hebrew_blocks:
        issues.append(f"Hebrew text found in English site ({len(hebrew_blocks)} blocks)")

    return issues


def check_video(folder_path, folder_name):
    """Check 5: Video files exist and have reasonable size."""
    issues = []

    for vname in ['site-walkthrough.mp4', 'site-walkthrough2.mp4', 'site-walkthrough3.mp4']:
        vpath = os.path.join(folder_path, vname)
        if not os.path.exists(vpath):
            issues.append(f"Missing: {vname}")
        else:
            size_mb = os.path.getsize(vpath) / (1024 * 1024)
            if size_mb < 0.05:
                issues.append(f"{vname} too small ({size_mb:.2f} MB) — likely corrupted")
            elif size_mb < 0.2:
                issues.append(f"{vname} suspiciously small ({size_mb:.2f} MB)")

    return issues


def check_screenshots(folder_path):
    """Check that all 3 screenshots exist and have reasonable size."""
    issues = []
    for shot in ['screenshot-home.png', 'screenshot-blog.png', 'screenshot-article.png']:
        path = os.path.join(folder_path, shot)
        if not os.path.exists(path):
            issues.append(f"Missing: {shot}")
        else:
            size_kb = os.path.getsize(path) / 1024
            if size_kb < 5:
                issues.append(f"{shot} too small ({size_kb:.0f} KB) — blank/broken?")

    return issues


def check_content_md(folder_path):
    """Check content.md has real data."""
    issues = []
    md_path = os.path.join(folder_path, "content.md")
    if not os.path.exists(md_path):
        issues.append("Missing content.md")
        return issues

    content = read_file(md_path)

    if 'Google Rating:** 0' in content or '(0 reviews)' in content:
        issues.append("content.md has zero rating/reviews")

    if '_No reviews scraped yet._' in content:
        issues.append("content.md has no reviews")

    # Check for fake markers in content.md too
    for marker in FAKE_MARKERS[:5]:
        if marker in content:
            issues.append(f"Fake content in content.md: \"{marker}\"")

    return issues


def check_proposal(folder_path):
    """Check proposal.html exists and has content."""
    issues = []
    path = os.path.join(folder_path, "proposal.html")
    if not os.path.exists(path):
        issues.append("Missing proposal.html")
    else:
        html = read_file(path)
        if len(html) < 500:
            issues.append("proposal.html is suspiciously short")
        for marker in FAKE_MARKERS[:5]:
            if marker in html:
                issues.append(f"Fake content in proposal: \"{marker}\"")

    return issues


def check_review_accuracy(folder_path):
    """Check that review counts in index.html match content.md."""
    issues = []
    md_path = os.path.join(folder_path, "content.md")
    index_path = os.path.join(folder_path, "index.html")

    if not os.path.exists(md_path) or not os.path.exists(index_path):
        return issues

    md = read_file(md_path)
    html = read_file(index_path)

    # Get real data from content.md
    match = re.search(r'Google Rating:\*\*\s*([\d.]+)\s*\((\d+)\s*reviews?\)', md)
    if not match:
        return issues

    real_rating = match.group(1)
    real_reviews = match.group(2)

    # Check hero badge for wrong count
    hero_match = re.search(r'[·]\s*(\d+)\s*Reviews', html)
    if hero_match and hero_match.group(1) != real_reviews:
        issues.append(f"Hero badge shows {hero_match.group(1)} reviews, real is {real_reviews}")

    # Check for remaining "187" in review/rating contexts (not phone numbers)
    # Remove phone numbers first, then check
    html_no_phones = re.sub(r'tel:[^"]+|[\d\-\(\)\+]{7,}', '', html)
    if re.search(r'187\s*Reviews|>187<|>\s*187\s*<', html_no_phones):
        issues.append("Still contains '187' in review context (likely template leftover)")

    return issues


def main():
    print("=" * 70)
    print("  US DENTIST REPORT AUDITOR")
    print("=" * 70)

    clinic_data = load_clinic_data()
    reviews_data = load_reviews()

    folders = sorted([
        d for d in os.listdir(OUTPUT_DIR)
        if os.path.isdir(os.path.join(OUTPUT_DIR, d))
    ])

    total_issues = 0
    results = {}

    for folder_name in folders:
        folder_path = os.path.join(OUTPUT_DIR, folder_name)
        index_path = os.path.join(folder_path, "index.html")

        if not os.path.exists(index_path):
            continue

        html = read_file(index_path)
        folder_issues = []

        # Run all checks
        folder_issues.extend(
            [f"[FAKE] {i}" for i in check_fake_content(html, folder_name)])
        folder_issues.extend(
            [f"[IMG/LINK] {i}" for i in check_images_links(html, folder_path)])
        folder_issues.extend(
            [f"[DUP NAME] {i}" for i in check_name_duplication(html, folder_name)])
        folder_issues.extend(
            [f"[WEIRD] {i}" for i in check_weird_content(html, folder_path)])
        folder_issues.extend(
            [f"[VIDEO] {i}" for i in check_video(folder_path, folder_name)])
        folder_issues.extend(
            [f"[SCREENSHOT] {i}" for i in check_screenshots(folder_path)])
        folder_issues.extend(
            [f"[CONTENT] {i}" for i in check_content_md(folder_path)])
        folder_issues.extend(
            [f"[PROPOSAL] {i}" for i in check_proposal(folder_path)])
        folder_issues.extend(
            [f"[ACCURACY] {i}" for i in check_review_accuracy(folder_path)])

        # Also audit blog.html
        blog_path = os.path.join(folder_path, "blog.html")
        if os.path.exists(blog_path):
            blog_html = read_file(blog_path)
            blog_fake = check_fake_content(blog_html, folder_name)
            folder_issues.extend([f"[FAKE blog] {i}" for i in blog_fake])
            blog_imgs = check_images_links(blog_html, folder_path)
            folder_issues.extend([f"[IMG/LINK blog] {i}" for i in blog_imgs])

        # Audit blog articles
        blog_dir = os.path.join(folder_path, "blog")
        if os.path.isdir(blog_dir):
            for cat in os.listdir(blog_dir):
                cat_path = os.path.join(blog_dir, cat)
                if os.path.isdir(cat_path):
                    for f in os.listdir(cat_path):
                        if f.endswith('.html'):
                            art_html = read_file(os.path.join(cat_path, f))
                            art_fake = check_fake_content(art_html, folder_name)
                            folder_issues.extend(
                                [f"[FAKE article:{cat}/{f}] {i}" for i in art_fake])

        if folder_issues:
            results[folder_name] = folder_issues
            total_issues += len(folder_issues)

    # ─── Print report ─────────────────────────────────────────────────
    clean_count = len(folders) - len(results)

    print(f"\nAudited: {len(folders)} folders")
    print(f"Clean: {clean_count}")
    print(f"With issues: {len(results)}")
    print(f"Total issues: {total_issues}")
    print()

    if results:
        # Group by issue type for summary
        type_counts = {}
        for folder, issues in results.items():
            for issue in issues:
                itype = issue.split(']')[0] + ']'
                type_counts[itype] = type_counts.get(itype, 0) + 1

        print("Issue breakdown:")
        for itype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"  {itype}: {count}")
        print()

        # Detail per folder
        for folder, issues in sorted(results.items()):
            print(f"\n{'─' * 50}")
            print(f"  {folder}")
            for issue in issues:
                print(f"   {issue}")

    print(f"\n{'=' * 70}")
    print(f"  AUDIT COMPLETE — {total_issues} issue(s) found across {len(results)} folder(s)")
    print(f"{'=' * 70}")

    # Save JSON report
    report_path = os.path.join(SCRIPT_DIR, "audit-report.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            "total_folders": len(folders),
            "clean": clean_count,
            "with_issues": len(results),
            "total_issues": total_issues,
            "details": results,
        }, f, ensure_ascii=False, indent=2)
    print(f"\nFull report saved: {report_path}")

    return 1 if total_issues > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
