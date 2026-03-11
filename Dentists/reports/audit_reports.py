#!/usr/bin/env python3
"""Audit all generated clinic report folders for quality issues.

Cross-references real clinic data from CSV to eliminate false positives.

Checks:
  1. Generic/fake content (template placeholders left behind)
  2. Broken images and links
  3. Name duplication in hero section (doctor name == clinic brand)
  4. Weird/suspicious content (empty sections, garbled text, wrong language)
  5. Video quality (file size check — tiny = corrupted/jittery)
  6. Screenshots exist and are non-empty
  7. content.md has real data
  8. proposal.html exists and is personalized

Severity levels:
  CRITICAL — must fix before sending (fake content in main site, broken images)
  WARNING  — should fix (fake content in blog articles, suspicious sizes)
  INFO     — cosmetic or expected (e.g. clinic actually has 4.9 rating)
"""

import csv, os, re, sys, json
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
CSV_PATH = os.path.join(BASE_DIR, "labeled-dentals.csv")
REVIEWS_PATH = os.path.join(BASE_DIR, "reviews.csv")

# ─── Known fake/placeholder content ──────────────────────────────────
FAKE_MARKERS_CRITICAL = [
    'מרפאת חיוך פלוס', 'חיוך פלוס',
    'ד״ר מיכל לוי', 'ד"ר מיכל לוי', 'מיכל לוי', 'ד״ר לוי', 'ד"ר לוי',
    '03-555-1234',
    'Lorem ipsum', 'dolor sit amet',
]

FAKE_REVIEWER_NAMES = ['נועה כהן', 'יוסי אברהם', 'שירה דויד']

FAKE_REVIEW_SNIPPETS = [
    'ד״ר לוי שינתה לי את החיים',
    'עברתי השתלת שיניים במרפאה — מהייעוץ הראשוני',
    'מקום מדהים! הגעתי בפעם הראשונה לטיפול שורש',
]

GUSH_DAN_CITIES = {"תל אביב", "בת ים", "בני ברק", "פתח תקווה", "רמת גן", "חולון", "גבעתיים", "קרית אונו", ""}
SEGMENTS = ("4a", "4b")
SKIP_CATEGORIES = {"לינה וארוחת בוקר", "מלון", "מסעדה", "קפה"}


def load_clinic_data():
    """Load real clinic data for cross-referencing, keyed by slug-friendly name."""
    clinics = {}
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if (row.get('city', '').strip() in GUSH_DAN_CITIES and
                row.get('segment', '').strip() in SEGMENTS and
                row.get('categories', '').strip() not in SKIP_CATEGORIES):
                clinics[row['name'].strip()] = row
    return clinics


def load_reviews():
    """Load reviews grouped by clinic name."""
    reviews = {}
    if not os.path.exists(REVIEWS_PATH):
        return reviews
    with open(REVIEWS_PATH, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            cn = row['clinic_name'].strip()
            if cn not in reviews:
                reviews[cn] = []
            reviews[cn].append(row)
    return reviews


def find_clinic_for_folder(folder_name, clinic_data):
    """Find the clinic data row matching a folder by reading content.md."""
    # Best approach: read the clinic name directly from content.md
    md_path = os.path.join(OUTPUT_DIR, folder_name, "content.md")
    if os.path.exists(md_path):
        content = read_file(md_path)
        # content.md line: "- **שם:** CLINIC_NAME"
        m = re.search(r'\*\*שם:\*\*\s*(.+)', content)
        if m:
            real_name = m.group(1).strip()
            if real_name in clinic_data:
                return real_name, clinic_data[real_name]

    # Fallback: fuzzy slug matching
    slug = folder_name.replace('-', ' ').replace('_', ' ')
    slug_norm = slug.replace('"', '').replace('״', '').replace("'", '').lower()
    best_match = None
    best_score = 0
    for name, data in clinic_data.items():
        name_norm = name.replace('"', '').replace('״', '').replace("'", '').lower()
        name_words = set(name_norm.split())
        slug_words = set(slug_norm.split())
        overlap = len(name_words & slug_words)
        # Score by overlap relative to name length
        score = overlap / max(len(name_words), 1)
        if score > best_score:
            best_score = score
            best_match = (name, data)
    if best_match and best_score >= 0.5:
        return best_match
    return None, None


def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ''


# ─── Check functions ──────────────────────────────────────────────────

def check_fake_content(html, clinic_data, reviews_list, context="index"):
    """Check for leftover template/fake content. Uses real data to avoid false positives."""
    issues = []
    real_rating = clinic_data.get('rating', '') if clinic_data else ''
    real_review_count = clinic_data.get('review_count', '') if clinic_data else ''
    num_real_reviews = len(reviews_list) if reviews_list else 0

    # Critical: template placeholder names/phone
    for marker in FAKE_MARKERS_CRITICAL:
        if marker in html:
            issues.append(("CRITICAL", f"Template placeholder: \"{marker}\""))

    # Fake reviewer names — only critical in index.html testimonials, warning in blog articles
    severity = "CRITICAL" if context == "index" else "WARNING"
    for name in FAKE_REVIEWER_NAMES:
        if name in html:
            issues.append((severity, f"Fake reviewer name: \"{name}\""))

    # Fake review text — only flag if clinic has enough real reviews to replace all 3
    for i, snippet in enumerate(FAKE_REVIEW_SNIPPETS):
        if snippet in html:
            if num_real_reviews > i:
                # Clinic has enough real reviews — this shouldn't be here
                issues.append(("CRITICAL", f"Fake review text not replaced (have {num_real_reviews} real reviews): \"{snippet[:35]}...\""))
            else:
                # Clinic has fewer real reviews — expected that some template text remains
                issues.append(("INFO", f"Template review text (only {num_real_reviews} real reviews available): \"{snippet[:35]}...\""))

    # Rating patterns — only flag if clinic's actual rating is NOT 4.9
    if real_rating and real_rating.strip() != '4.9':
        if re.search(r'>4\.9<', html):
            issues.append(("CRITICAL", f"Leftover 4.9 rating (real: {real_rating})"))
        if re.search(r'4\.9\s*&#9733;', html):
            issues.append(("CRITICAL", f"Leftover 4.9★ badge (real: {real_rating})"))
        if re.search(r'דירוג 4\.9', html):
            issues.append(("CRITICAL", f"Leftover 'דירוג 4.9' (real: {real_rating})"))
        if re.search(r'4\.9\s*כוכבים', html):
            issues.append(("CRITICAL", f"Leftover '4.9 כוכבים' (real: {real_rating})"))

    # Review count 187 — only flag if real count is NOT 187
    if real_review_count and real_review_count.strip() != '187':
        if re.search(r'>187<', html):
            issues.append(("CRITICAL", f"Leftover 187 count (real: {real_review_count})"))
        if re.search(r'187\+?\s*ביקורות', html):
            issues.append(("CRITICAL", f"Leftover '187 ביקורות' (real: {real_review_count})"))

    return issues


def check_images_links(html, folder_path, context="index"):
    """Check for broken image references and links."""
    issues = []
    base_path = folder_path

    img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
    for src in img_srcs:
        if src.startswith('http') or src.startswith('data:'):
            continue
        img_path = os.path.normpath(os.path.join(base_path, src))
        if not os.path.exists(img_path):
            issues.append(("CRITICAL", f"Missing image: {src}"))

    hrefs = re.findall(r'href=["\']([^"\'#]+)["\']', html)
    for href in hrefs:
        if href.startswith(('http', 'mailto:', 'tel:', 'javascript:')):
            continue
        link_path = os.path.normpath(os.path.join(base_path, href))
        if not os.path.exists(link_path):
            if href.endswith('.html'):
                issues.append(("WARNING", f"Broken link: {href}"))

    return issues


def check_name_duplication(html):
    """Check for name appearing twice in hero section."""
    issues = []
    hero = html[:6000]
    titles = re.findall(r'<h[12][^>]*>(.*?)</h[12]>', hero, re.DOTALL)

    for title in titles:
        clean = re.sub(r'<[^>]+>', '|', title)
        parts = [p.strip() for p in clean.split('|') if p.strip() and len(p.strip()) > 2]

        for i in range(len(parts)):
            for j in range(i + 1, len(parts)):
                a, b = parts[i], parts[j]
                if len(a) > 3 and len(b) > 3:
                    if a == b:
                        issues.append(("CRITICAL", f"Exact duplicate in hero: \"{a}\""))
                    elif len(a) > 8 and len(b) > 8 and a in b and len(a) / len(b) > 0.7:
                        issues.append(("WARNING", f"Near-duplicate in hero: \"{a}\" inside \"{b}\""))

    # Check for same text block repeated 3+ times in hero
    hero_texts = re.findall(r'>([^<]{6,60})<', hero)
    seen = {}
    for t in hero_texts:
        t = t.strip()
        if t and not re.match(r'^[\s\d\.\,\-]+$', t):
            seen[t] = seen.get(t, 0) + 1
    for text, count in seen.items():
        if count >= 3:
            issues.append(("WARNING", f"Text repeated {count}x in hero: \"{text[:40]}\""))

    return issues


def check_weird_content(html, folder_path):
    """Detect weird/suspicious content."""
    issues = []

    if len(html) < 500:
        issues.append(("CRITICAL", f"Suspiciously short HTML ({len(html)} chars)"))

    template_tags = re.findall(r'\{\{[^}]+\}\}|\{%[^%]+%\}', html)
    for tag in template_tags[:3]:
        issues.append(("CRITICAL", f"Template tag in output: {tag[:30]}"))

    if '\ufffd' in html or '�' in html:
        issues.append(("WARNING", "Garbled characters (replacement char \ufffd) found"))

    # Long English blocks in Hebrew site (skip known-OK patterns)
    eng_blocks = re.findall(r'>([A-Za-z\s]{50,})<', html)
    skip_words = {'google', 'font', 'script', 'style', 'copyright', 'class',
                  'width', 'height', 'arial', 'helvetica', 'sans', 'serif',
                  'center', 'dental', 'hidden', 'block', 'none', 'flex'}
    for block in eng_blocks[:2]:
        text = block.strip()
        if not any(w in text.lower() for w in skip_words):
            issues.append(("WARNING", f"Long English text: \"{text[:40]}...\""))

    # Check for empty visible sections (div with only whitespace)
    empty_sections = re.findall(r'<section[^>]*>\s*</section>', html)
    if empty_sections:
        issues.append(("WARNING", f"{len(empty_sections)} empty <section> tag(s)"))

    return issues


def check_video(folder_path):
    """Video file exists and has reasonable size."""
    issues = []
    mp4 = os.path.join(folder_path, "site-walkthrough.mp4")
    webm = os.path.join(folder_path, "site-walkthrough.webm")

    if os.path.exists(mp4):
        size_mb = os.path.getsize(mp4) / (1024 * 1024)
        if size_mb < 0.05:
            issues.append(("CRITICAL", f"Video corrupted ({size_mb:.2f} MB)"))
        elif size_mb < 0.2:
            issues.append(("WARNING", f"Video very small ({size_mb:.2f} MB) — may be jittery"))
    elif os.path.exists(webm):
        size_mb = os.path.getsize(webm) / (1024 * 1024)
        if size_mb < 0.05:
            issues.append(("CRITICAL", f"Video corrupted ({size_mb:.2f} MB)"))
        elif size_mb < 0.2:
            issues.append(("WARNING", f"Video very small ({size_mb:.2f} MB) — may be jittery"))
        issues.append(("INFO", "Video is webm, not mp4 — needs conversion"))
    else:
        issues.append(("CRITICAL", "No video file"))

    return issues


def check_screenshots(folder_path):
    """All 3 screenshots exist and have reasonable size."""
    issues = []
    for shot in ['screenshot-home.png', 'screenshot-blog.png', 'screenshot-article.png']:
        path = os.path.join(folder_path, shot)
        if not os.path.exists(path):
            issues.append(("CRITICAL", f"Missing: {shot}"))
        else:
            size_kb = os.path.getsize(path) / 1024
            if size_kb < 5:
                issues.append(("CRITICAL", f"{shot} blank/broken ({size_kb:.0f} KB)"))
            elif size_kb < 20:
                issues.append(("WARNING", f"{shot} very small ({size_kb:.0f} KB)"))

    return issues


def check_content_md(folder_path):
    """content.md has real data."""
    issues = []
    md_path = os.path.join(folder_path, "content.md")
    if not os.path.exists(md_path):
        issues.append(("CRITICAL", "Missing content.md"))
        return issues

    content = read_file(md_path)
    if '**דירוג גוגל:** 0' in content or '**דירוג גוגל:** (0' in content:
        issues.append(("WARNING", "content.md has zero rating"))
    if 'אין ביקורות שנאספו' in content:
        issues.append(("WARNING", "content.md has no reviews"))

    return issues


def check_proposal(folder_path):
    """proposal.html exists and is personalized."""
    issues = []
    path = os.path.join(folder_path, "proposal.html")
    if not os.path.exists(path):
        issues.append(("CRITICAL", "Missing proposal.html"))
        return issues

    html = read_file(path)
    if len(html) < 500:
        issues.append(("CRITICAL", "proposal.html suspiciously short"))

    for marker in FAKE_MARKERS_CRITICAL[:6]:
        if marker in html:
            issues.append(("CRITICAL", f"Template placeholder in proposal: \"{marker}\""))

    return issues


# ─── Main ─────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("  CLINIC REPORT AUDITOR")
    print("=" * 70)

    clinic_data = load_clinic_data()
    reviews_data = load_reviews()

    folders = sorted([
        d for d in os.listdir(OUTPUT_DIR)
        if os.path.isdir(os.path.join(OUTPUT_DIR, d))
           and os.path.exists(os.path.join(OUTPUT_DIR, d, "index.html"))
    ])

    all_issues = {}  # folder -> [(severity, message), ...]
    severity_totals = {"CRITICAL": 0, "WARNING": 0, "INFO": 0}

    for folder_name in folders:
        folder_path = os.path.join(OUTPUT_DIR, folder_name)
        index_html = read_file(os.path.join(folder_path, "index.html"))

        # Match folder to real clinic data
        clinic_name, clinic_row = find_clinic_for_folder(folder_name, clinic_data)
        clinic_reviews = reviews_data.get(clinic_name, []) if clinic_name else []

        folder_issues = []

        # 1. Fake content in index.html
        folder_issues.extend(
            [(s, f"[FAKE] {m}") for s, m in check_fake_content(index_html, clinic_row, clinic_reviews, "index")])

        # 2. Broken images/links in index.html
        folder_issues.extend(
            [(s, f"[IMG/LINK] {m}") for s, m in check_images_links(index_html, folder_path)])

        # 3. Name duplication
        folder_issues.extend(
            [(s, f"[DUP NAME] {m}") for s, m in check_name_duplication(index_html)])

        # 4. Weird content
        folder_issues.extend(
            [(s, f"[WEIRD] {m}") for s, m in check_weird_content(index_html, folder_path)])

        # 5. Video
        folder_issues.extend(
            [(s, f"[VIDEO] {m}") for s, m in check_video(folder_path)])

        # 6. Screenshots
        folder_issues.extend(
            [(s, f"[SCREENSHOT] {m}") for s, m in check_screenshots(folder_path)])

        # 7. content.md
        folder_issues.extend(
            [(s, f"[CONTENT] {m}") for s, m in check_content_md(folder_path)])

        # 8. Proposal
        folder_issues.extend(
            [(s, f"[PROPOSAL] {m}") for s, m in check_proposal(folder_path)])

        # 9. Blog listing
        blog_path = os.path.join(folder_path, "blog.html")
        if os.path.exists(blog_path):
            blog_html = read_file(blog_path)
            folder_issues.extend(
                [(s, f"[FAKE blog] {m}") for s, m in check_fake_content(blog_html, clinic_row, clinic_reviews, "blog")])
            folder_issues.extend(
                [(s, f"[IMG/LINK blog] {m}") for s, m in check_images_links(blog_html, folder_path)])

        # 10. Blog articles
        blog_dir = os.path.join(folder_path, "blog")
        if os.path.isdir(blog_dir):
            for cat in os.listdir(blog_dir):
                cat_path = os.path.join(blog_dir, cat)
                if os.path.isdir(cat_path):
                    for f in os.listdir(cat_path):
                        if f.endswith('.html'):
                            art_html = read_file(os.path.join(cat_path, f))
                            folder_issues.extend(
                                [(s, f"[FAKE article:{cat}/{f}] {m}")
                                 for s, m in check_fake_content(art_html, clinic_row, clinic_reviews, "article")])

        if folder_issues:
            all_issues[folder_name] = folder_issues
            for sev, _ in folder_issues:
                severity_totals[sev] += 1

    # ─── Print report ─────────────────────────────────────────────────
    total = sum(severity_totals.values())
    clean = len(folders) - len(all_issues)

    print(f"\nAudited: {len(folders)} folders")
    print(f"Clean: {clean}")
    print(f"With issues: {len(all_issues)}")
    print()
    print(f"  CRITICAL: {severity_totals['CRITICAL']}")
    print(f"  WARNING:  {severity_totals['WARNING']}")
    print(f"  INFO:     {severity_totals['INFO']}")
    print()

    # Summary by check type
    type_counts = {"CRITICAL": {}, "WARNING": {}, "INFO": {}}
    for folder, issues in all_issues.items():
        for sev, msg in issues:
            itype = msg.split(']')[0] + ']'
            type_counts[sev][itype] = type_counts[sev].get(itype, 0) + 1

    for sev in ["CRITICAL", "WARNING", "INFO"]:
        if type_counts[sev]:
            print(f"{sev} breakdown:")
            for itype, count in sorted(type_counts[sev].items(), key=lambda x: -x[1]):
                print(f"  {itype}: {count}")
            print()

    # Detail — only show CRITICAL and WARNING by default
    critical_folders = {f: [(s, m) for s, m in issues if s in ("CRITICAL", "WARNING")]
                        for f, issues in all_issues.items()}
    critical_folders = {f: i for f, i in critical_folders.items() if i}

    if critical_folders:
        print(f"\n{'─' * 70}")
        print(f"  DETAILS (CRITICAL + WARNING only)")
        print(f"{'─' * 70}")
        for folder, issues in sorted(critical_folders.items()):
            print(f"\n  {folder}")
            for sev, msg in issues:
                icon = "!!" if sev == "CRITICAL" else "?"
                print(f"    [{icon}] {msg}")

    # Count INFO-only folders
    info_only = len(all_issues) - len(critical_folders)
    if info_only:
        print(f"\n  ({info_only} folders have INFO-level issues only — not shown)")

    print(f"\n{'=' * 70}")
    status = "PASS" if severity_totals["CRITICAL"] == 0 else "FAIL"
    print(f"  AUDIT {status} — {severity_totals['CRITICAL']} critical, "
          f"{severity_totals['WARNING']} warnings, {severity_totals['INFO']} info")
    print(f"{'=' * 70}")

    # Save JSON report
    report_path = os.path.join(SCRIPT_DIR, "audit-report.json")
    json_issues = {}
    for folder, issues in all_issues.items():
        json_issues[folder] = [{"severity": s, "message": m} for s, m in issues]

    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            "total_folders": len(folders),
            "clean": clean,
            "severity_totals": severity_totals,
            "details": json_issues,
        }, f, ensure_ascii=False, indent=2)
    print(f"\nFull report: {report_path}")

    return 1 if severity_totals["CRITICAL"] > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
