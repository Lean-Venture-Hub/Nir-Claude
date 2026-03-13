#!/usr/bin/env python3
"""Inject stretched-link CSS into all 20 blog.html files for full card clickability."""

import os
import re

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '')

STRETCHED_LINK_CSS = """\n.blog-card{position:relative}
.blog-card-link::after{content:'';position:absolute;inset:0;z-index:1}"""


def fix_blog_cards(template_num):
    blog_path = os.path.join(TEMPLATE_DIR, f'template-{template_num}', 'blog.html')
    if not os.path.isfile(blog_path):
        return False

    with open(blog_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip if already patched
    if 'blog-card-link::after' in html:
        print(f"  template-{template_num}: already patched, skipping")
        return True

    # Insert the stretched-link CSS right after .blog-card-link:hover{...}
    pattern = r'(\.blog-card-link:hover\{[^}]+\})'
    match = re.search(pattern, html)
    if not match:
        print(f"  template-{template_num}: WARNING — .blog-card-link:hover not found")
        return False

    insert_pos = match.end()
    html = html[:insert_pos] + STRETCHED_LINK_CSS + html[insert_pos:]

    with open(blog_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return True


def main():
    print("Fixing blog card clickability (stretched-link CSS)...")
    fixed = 0
    for n in range(1, 21):
        if fix_blog_cards(n):
            fixed += 1
            print(f"  template-{n}: OK")
    print(f"\nDone: {fixed}/20 templates patched.")


if __name__ == '__main__':
    main()
