#!/usr/bin/env python3
"""Assign blog images to all 20 templates.

Each template gets a unique combination of 3 images (from 6 total).
Images are assigned to:
  - blog.html → blog card thumbnails (replace gradient divs)
  - article pages → hero image at top of article

C(6,3) = 20 combinations = exactly 20 templates!
"""

import os, re
from itertools import combinations

BASE = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = '../images/blog-images'

# Image files (numbered 1-6)
IMAGES = {
    1: '1-confident-smile.jpg',
    2: '2-modern-clinic.jpg',
    3: '3-oral-hygiene.jpg',
    4: '4-dentist-patient-consultation.jpg',
    5: '5-dental-implant-diagram.jpg',
    6: '6-happy-patient-thumbsup.jpg',
}

# Blog categories in order they appear in blog.html cards
# Card 1 = tipulim, Card 2 = briut-hapeh, Card 3 = sipurei-metuplim
CATEGORIES = ['tipulim', 'briut-hapeh', 'sipurei-metuplim']

ARTICLE_FILES = {
    'tipulim': 'blog/tipulim/hashtalat-shinayim-tel-aviv.html',
    'briut-hapeh': 'blog/briut-hapeh/tzviat-shinayim-nechona.html',
    'sipurei-metuplim': 'blog/sipurei-metuplim/hashtalat-shinayim-shinu-et-hayim-sheli.html',
}

# Generate all 20 unique 3-image combinations
all_combos = list(combinations(range(1, 7), 3))  # C(6,3) = 20

# Reorder for better visual variety (spread similar combos apart)
# Shuffle deterministically so treatments get implant/clinic images more often
COMBO_ORDER = [
    (3, 5, 6),  # oral-hygiene, implant, happy-patient
    (1, 4, 5),  # smile, consultation, implant
    (2, 3, 6),  # clinic, oral-hygiene, happy-patient
    (1, 2, 4),  # smile, clinic, consultation
    (3, 4, 5),  # oral-hygiene, consultation, implant
    (1, 5, 6),  # smile, implant, happy-patient
    (2, 4, 6),  # clinic, consultation, happy-patient
    (1, 3, 4),  # smile, oral-hygiene, consultation
    (2, 5, 6),  # clinic, implant, happy-patient
    (1, 2, 3),  # smile, clinic, oral-hygiene
    (4, 5, 6),  # consultation, implant, happy-patient
    (1, 3, 6),  # smile, oral-hygiene, happy-patient
    (2, 3, 4),  # clinic, oral-hygiene, consultation
    (1, 4, 6),  # smile, consultation, happy-patient
    (2, 3, 5),  # clinic, oral-hygiene, implant
    (1, 2, 6),  # smile, clinic, happy-patient
    (3, 4, 6),  # oral-hygiene, consultation, happy-patient
    (1, 2, 5),  # smile, clinic, implant
    (2, 4, 5),  # clinic, consultation, implant
    (1, 3, 5),  # smile, oral-hygiene, implant
]


def update_blog_html(tpl_dir, n, img_combo):
    """Replace gradient card images with actual photos in blog.html."""
    blog_path = os.path.join(tpl_dir, 'blog.html')
    if not os.path.exists(blog_path):
        return False

    with open(blog_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # The 3 blog cards use gradient classes: gradient-blue, gradient-green, gradient-orange
    # Replace each gradient div with an img-based div
    gradients = ['gradient-blue', 'gradient-green', 'gradient-orange']

    for i, gradient_class in enumerate(gradients):
        img_num = img_combo[i]
        img_file = IMAGES[img_num]
        img_path = f'../{IMAGES_DIR}/{img_file}'

        # Pattern: match the content between opening div and the badge span
        # Handles both SVG (first run) and img (re-run)
        pattern = (
            r'(<div class="blog-card-image '
            + re.escape(gradient_class)
            + r'">\s*)'
            + r'(?:<!--[^>]*-->\s*)?'  # optional comment
            + r'(?:<svg[^>]*>.*?</svg>|<img[^>]*>)'  # SVG or existing img
        )

        img_tag = (
            f'<img src="{img_path}" alt="" '
            f'style="width:100%;height:100%;object-fit:cover;position:absolute;top:0;left:0">'
        )

        html = re.sub(pattern, r'\1' + img_tag, html, flags=re.DOTALL)

    with open(blog_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return True


def update_article_html(tpl_dir, category, img_num):
    """Add hero image to article page."""
    rel_path = ARTICLE_FILES[category]
    article_path = os.path.join(tpl_dir, rel_path)
    if not os.path.exists(article_path):
        return False

    with open(article_path, 'r', encoding='utf-8') as f:
        html = f.read()

    img_file = IMAGES[img_num]
    # Articles are 3 levels deep: template-N/blog/category/article.html
    # Images are at: s4-templates/blog-images/file.jpg
    img_path = f'../../../{IMAGES_DIR}/{img_file}'

    # Add hero image after article-header, before article-layout
    hero_img_html = f'''
<!-- ── HERO IMAGE ──────────────────────────── -->
<div class="article-hero-image" style="max-width:var(--max-w,1280px);margin:0 auto;padding:0 48px">
  <img src="{img_path}" alt="" style="width:100%;max-height:460px;object-fit:cover;border-radius:var(--radius-lg,24px);display:block;margin-top:-20px;box-shadow:0 16px 48px rgba(0,0,0,.1)">
</div>
'''

    # Check if hero image already exists (idempotent)
    if 'article-hero-image' in html:
        # Replace existing block (from comment to closing div + newlines)
        html = re.sub(
            r'\n<!-- ── HERO IMAGE ──[^>]*-->\s*\n<div class="article-hero-image"[^>]*>\s*<img[^>]*>\s*</div>\s*\n',
            hero_img_html,
            html,
            flags=re.DOTALL
        )
    else:
        # Insert before article-layout comment (may say "ARTICLE LAYOUT" or "ARTICLE LAYOUT (2-col)" etc.)
        html = re.sub(
            r'(<!-- ── ARTICLE LAYOUT)',
            hero_img_html + r'\n\1',
            html,
            count=1
        )

    with open(article_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return True


def main():
    print('Assigning blog images to 20 templates...\n')

    for idx, n in enumerate(range(1, 21)):
        tpl_dir = os.path.join(BASE, f'template-{n}')
        if not os.path.isdir(tpl_dir):
            print(f'  ⚠ template-{n}: not found, skipping')
            continue

        combo = COMBO_ORDER[idx]
        img_names = [IMAGES[i].split('.')[0] for i in combo]

        # Update blog.html card thumbnails
        blog_ok = update_blog_html(tpl_dir, n, combo)

        # Update each article with its assigned image
        art_count = 0
        for cat_idx, category in enumerate(CATEGORIES):
            if update_article_html(tpl_dir, category, combo[cat_idx]):
                art_count += 1

        status = '✓' if blog_ok else '⚠'
        print(f'  {status} template-{n}: images [{combo[0]},{combo[1]},{combo[2]}] '
              f'→ blog:{"ok" if blog_ok else "skip"}, articles:{art_count}/3')

    print(f'\nDone! All templates updated with blog images.')
    print(f'Images folder: {IMAGES_DIR}/')


if __name__ == '__main__':
    main()
