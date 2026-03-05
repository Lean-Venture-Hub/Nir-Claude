#!/usr/bin/env python3
"""
Inject service images into all 20 dental website templates.

Handles 4 card patterns:
  A) Icon-based (.service-icon → title): add <img> after icon div
  B) Already has images (templates 4, 11): swap src to blog-images
  C) Template 12 (.service-card-icon): add <img> after icon div
  D) Template 18 (feature-card): add <img> after icon div

Images are mapped to service slot 1-4, cycling from the service images bank.
"""
import os
import re
import glob

BASE = os.path.dirname(__file__)
BLOG_IMAGES = '../../images/blog-images'  # Relative from template folder

# Service images bank: maps to the 4 service slots per template
# We rotate different images per template so they look varied
SERVICE_IMAGES = [
    '7-teeth-whitening.jpg',
    '8-dental-implant.jpg',
    '9-porcelain-veneers.jpg',
    '10-invisible-aligners.jpg',
    '11-root-canal.jpg',
    '12-pediatric-dentistry.jpg',
    '13-gum-treatment.jpg',
    '14-crowns-bridges.jpg',
    '15-preventive-cleaning.jpg',
    '16-smile-design.jpg',
]

# CSS to inject for .service-img class
SERVICE_IMG_CSS = """.service-img{
  width:100%;
  height:160px;
  object-fit:cover;
  border-radius:calc(var(--radius, 16px) - 4px);
  margin-bottom:16px;
}
"""

# For templates with overlay images (4, 11) — just replace src
OVERLAY_IMG_CSS = ""  # They already have img styling


def get_images_for_template(template_num):
    """Return 4 image filenames, rotated by template number."""
    start = ((template_num - 1) * 4) % len(SERVICE_IMAGES)
    imgs = []
    for i in range(4):
        idx = (start + i) % len(SERVICE_IMAGES)
        imgs.append(SERVICE_IMAGES[idx])
    return imgs


def inject_css(html, css_block, marker='service-img'):
    """Inject CSS block before </style> if not already present."""
    if marker in html:
        return html  # Already injected
    # Insert before last </style>
    idx = html.rfind('</style>')
    if idx == -1:
        return html
    return html[:idx] + css_block + '</style>' + html[idx + len('</style>'):]


def process_icon_based(html, template_num):
    """Templates with .service-icon div → inject img after the closing </div> of icon."""
    imgs = get_images_for_template(template_num)
    html = inject_css(html, SERVICE_IMG_CSS)

    # Find each service-icon div's closing tag and inject img after it
    # Pattern: <div class="service-icon">...SVG...</div>\n  <h3
    slot = 0
    result = []
    lines = html.split('\n')
    inside_icon = False
    for i, line in enumerate(lines):
        result.append(line)
        if 'class="service-icon"' in line:
            inside_icon = True
        elif inside_icon and '</div>' in line.strip() and line.strip() == '</div>':
            inside_icon = False
            if slot < 4:
                img_path = f'{BLOG_IMAGES}/{imgs[slot]}'
                indent = '        '
                result.append(f'{indent}<img src="{img_path}" alt="" class="service-img" loading="lazy">')
                slot += 1

    return '\n'.join(result)


def process_icon_wrap_based(html, template_num):
    """Template 7 with .service-icon-wrap."""
    imgs = get_images_for_template(template_num)
    html = inject_css(html, SERVICE_IMG_CSS)

    slot = 0
    result = []
    lines = html.split('\n')
    inside_icon = False
    for i, line in enumerate(lines):
        result.append(line)
        if 'class="service-icon-wrap"' in line:
            inside_icon = True
        elif inside_icon and '</div>' in line.strip() and line.strip() == '</div>':
            inside_icon = False
            if slot < 4:
                img_path = f'{BLOG_IMAGES}/{imgs[slot]}'
                indent = '        '
                result.append(f'{indent}<img src="{img_path}" alt="" class="service-img" loading="lazy">')
                slot += 1

    return '\n'.join(result)


def process_card_icon_based(html, template_num):
    """Template 12 with .service-card-icon."""
    imgs = get_images_for_template(template_num)
    html = inject_css(html, SERVICE_IMG_CSS)

    slot = 0
    result = []
    lines = html.split('\n')
    inside_icon = False
    for i, line in enumerate(lines):
        result.append(line)
        if 'class="service-card-icon"' in line:
            inside_icon = True
        elif inside_icon and '</div>' in line.strip() and line.strip() == '</div>':
            inside_icon = False
            if slot < 4:
                img_path = f'{BLOG_IMAGES}/{imgs[slot]}'
                indent = '      '
                result.append(f'{indent}<img src="{img_path}" alt="" class="service-img" loading="lazy">')
                slot += 1

    return '\n'.join(result)


def process_feature_card(html, template_num):
    """Template 18 with .feature-card and icon div."""
    imgs = get_images_for_template(template_num)
    html = inject_css(html, SERVICE_IMG_CSS)

    slot = 0
    result = []
    lines = html.split('\n')
    inside_icon = False
    for i, line in enumerate(lines):
        result.append(line)
        # feature-card icon divs close then <h3>
        if 'class="feature-card' in line:
            inside_icon = True
        elif inside_icon and '</svg>' in line:
            # Next line should be </div> closing the icon
            pass
        elif inside_icon and '</div>' in line.strip() and line.strip() == '</div>':
            inside_icon = False
            if slot < 4:
                img_path = f'{BLOG_IMAGES}/{imgs[slot]}'
                indent = '      '
                result.append(f'{indent}<img src="{img_path}" alt="" class="service-img" loading="lazy">')
                slot += 1

    return '\n'.join(result)


def process_image_based(html, template_num):
    """Templates 4, 11 that already have <img> in service cards — swap src."""
    imgs = get_images_for_template(template_num)
    slot = 0

    def replace_src(match):
        nonlocal slot
        if slot < 4:
            img_path = f'{BLOG_IMAGES}/{imgs[slot]}'
            slot += 1
            return f'<img src="{img_path}" alt="{match.group(1)}"'
        return match.group(0)

    # Replace template images in service cards
    html = re.sub(
        r'<img src="[^"]*image\d+\.png" alt="([^"]*)"',
        replace_src,
        html
    )
    return html


def process_template(template_num):
    """Process a single template and its example file."""
    tdir = os.path.join(BASE, f'template-{template_num}')
    if not os.path.isdir(tdir):
        return False

    # Determine pattern
    if template_num in (4, 11):
        processor = process_image_based
    elif template_num == 7:
        processor = process_icon_wrap_based
    elif template_num == 12:
        processor = process_card_icon_based
    elif template_num == 18:
        processor = process_feature_card
    else:
        processor = process_icon_based

    # Process both template and example files
    for pattern in [f'template-{template_num}.html', f'template_example-{template_num}.html']:
        fpath = os.path.join(tdir, pattern)
        if not os.path.isfile(fpath):
            continue

        with open(fpath, 'r', encoding='utf-8') as f:
            html = f.read()

        if 'service-img' in html:
            print(f'  SKIP {pattern} (already has service-img)')
            continue

        new_html = processor(html, template_num)

        if new_html != html:
            tmp = fpath + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as f:
                f.write(new_html)
            os.replace(tmp, fpath)
            print(f'  Updated {pattern}')
        else:
            print(f'  NO CHANGE {pattern}')

    return True


def main():
    print('Injecting service images into templates...\n')
    for i in range(1, 21):
        print(f'Template {i}:')
        process_template(i)
    print('\nDone!')


if __name__ == '__main__':
    main()
