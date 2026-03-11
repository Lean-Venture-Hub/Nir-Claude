#!/usr/bin/env python3
"""Fix hardcoded/wrong review counts and ratings in all generated index.html files.

Reads real data from content.md and patches all occurrences in index.html.
"""

import os, re

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def get_real_data(content_md_path):
    """Extract real rating and review count from content.md."""
    with open(content_md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    match = re.search(r'Google Rating:\*\*\s*([\d.]+)\s*\((\d+)\s*reviews?\)', text)
    if match:
        return match.group(1), match.group(2)
    return None, None


def fix_html(html, real_rating, real_reviews):
    """Replace all fake review counts/ratings with real data."""
    changes = 0

    # Pattern 1: "· NNN Reviews" in hero badge (e.g. "· 187 Reviews")
    new_html, n = re.subn(r'·\s*\d+\s*Reviews', f'· {real_reviews} Reviews', html)
    changes += n
    html = new_html

    # Pattern 2: ">NNN Reviews<" in tags like rating-count, badge-google-reviews, etc.
    new_html, n = re.subn(r'>\d+ Reviews<', f'>{real_reviews} Reviews<', html)
    changes += n
    html = new_html

    # Pattern 3: "(NNN Reviews)" in parenthetical
    new_html, n = re.subn(r'\(\d+ Reviews\)', f'({real_reviews} Reviews)', html)
    changes += n
    html = new_html

    # Pattern 4: ">NNN+ Reviews on Google<"
    new_html, n = re.subn(r'>\d+\+ Reviews on Google<', f'>{real_reviews}+ Reviews on Google<', html)
    changes += n
    html = new_html

    # Pattern 5: about-stat-number with review count (the div after "Reviews" label)
    # Match: <div class="about-stat-number">NNN</div>\n...Reviews
    new_html, n = re.subn(
        r'(<div class="about-stat-number">)\d+(</div>\s*<div class="about-stat-label">Reviews)',
        rf'\g<1>{real_reviews}\g<2>',
        html
    )
    changes += n
    html = new_html

    # Pattern 6: stat-number with review count (before "Reviews" label)
    new_html, n = re.subn(
        r'(<div class="stat-number">)\d+(</div>\s*<div class="stat-label">Reviews)',
        rf'\g<1>{real_reviews}\g<2>',
        html
    )
    changes += n
    html = new_html

    # Pattern 7: cta-stat-number with review count (before "Reviews" label)
    new_html, n = re.subn(
        r'(<div class="cta-stat-number">)\d+(</div>\s*<div class="cta-stat-label">Reviews)',
        rf'\g<1>{real_reviews}\g<2>',
        html
    )
    changes += n
    html = new_html

    # Pattern 8: about-stat-number with rating (before "Google Rating" label)
    new_html, n = re.subn(
        r'(<div class="about-stat-number">)[\d.]+(</(div)>\s*<div class="about-stat-label">Google Rating)',
        rf'\g<1>{real_rating}\g<2>',
        html
    )
    changes += n
    html = new_html

    # Pattern 9: rating-meta ">NNN Reviews<"
    new_html, n = re.subn(
        r'(<div class="rating-meta">)\d+ Reviews(</div>)',
        rf'\g<1>{real_reviews} Reviews\g<2>',
        html
    )
    changes += n
    html = new_html

    # Pattern 10: badge-happy-sub
    new_html, n = re.subn(
        r'(<div class="badge-happy-sub">)\d+ Reviews(</div>)',
        rf'\g<1>{real_reviews} Reviews\g<2>',
        html
    )
    changes += n
    html = new_html

    return html, changes


def main():
    dentists = sorted([
        d for d in os.listdir(OUTPUT_DIR)
        if os.path.isdir(os.path.join(OUTPUT_DIR, d))
    ])

    total_changes = 0
    for dentist in dentists:
        ddir = os.path.join(OUTPUT_DIR, dentist)
        content_md = os.path.join(ddir, "content.md")
        index_html = os.path.join(ddir, "index.html")

        if not os.path.exists(content_md) or not os.path.exists(index_html):
            print(f"  {dentist}: SKIP (missing files)")
            continue

        rating, reviews = get_real_data(content_md)
        if not rating or not reviews:
            print(f"  {dentist}: SKIP (no data in content.md)")
            continue

        with open(index_html, 'r', encoding='utf-8') as f:
            html = f.read()

        fixed_html, changes = fix_html(html, rating, reviews)

        if changes > 0:
            with open(index_html, 'w', encoding='utf-8') as f:
                f.write(fixed_html)
            print(f"  {dentist}: {changes} fixes (rating={rating}, reviews={reviews})")
            total_changes += changes
        else:
            print(f"  {dentist}: OK (no changes needed, rating={rating}, reviews={reviews})")

    print(f"\nDone! {total_changes} total fixes across {len(dentists)} dentists.")


if __name__ == "__main__":
    main()
