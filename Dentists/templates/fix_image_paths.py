#!/usr/bin/env python3
"""
Fix all image paths after folder restructure.

Old structure:
  s4-templates/template-N/*.html  →  ../blog-images/, ../images/
  s4-templates/template-N/blog/*/*.html  →  ../../../blog-images/
  reports/proposals/templates_new/*.html  →  ../../image to be used/

New structure:
  templates/website/template-N/*.html  →  ../../images/blog-images/, ../../images/template-images/
  templates/website/template-N/blog/*/*.html  →  ../../../../images/blog-images/
  templates/proposals/*.html  →  ../images/template-images/

Also fixes Python scripts and gallery cross-links.
"""
import os
import re
import glob

BASE = os.path.dirname(__file__)
WEBSITE = os.path.join(BASE, 'website')
PROPOSALS = os.path.join(BASE, 'proposals')


def fix_file(fpath, replacements):
    """Apply a list of (old, new) string replacements to a file."""
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    for old, new in replacements:
        content = content.replace(old, new)

    if content != original:
        tmp = fpath + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            f.write(content)
        os.replace(tmp, fpath)
        return True
    return False


def fix_website_templates():
    """Fix paths in template-N/*.html files (direct children)."""
    count = 0
    for i in range(1, 21):
        tdir = os.path.join(WEBSITE, f'template-{i}')
        if not os.path.isdir(tdir):
            continue
        for fname in os.listdir(tdir):
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(tdir, fname)
            if fname.startswith('blog'):
                continue  # blog.html is also a direct child, handle same way
            replacements = [
                # blog-images (was 1 level up, now 2 levels up + images/)
                ('../blog-images/', '../../images/blog-images/'),
                # template images (was 1 level up, now 2 levels up + images/)
                ('../images/', '../../images/template-images/'),
            ]
            if fix_file(fpath, replacements):
                count += 1
                print(f'  Fixed {fname}')
    return count


def fix_blog_articles():
    """Fix paths in template-N/blog/*/*.html files (3 levels deep)."""
    count = 0
    for i in range(1, 21):
        blog_dir = os.path.join(WEBSITE, f'template-{i}', 'blog')
        if not os.path.isdir(blog_dir):
            continue
        for root, dirs, files in os.walk(blog_dir):
            for fname in files:
                if not fname.endswith('.html'):
                    continue
                fpath = os.path.join(root, fname)
                # Blog articles are at template-N/blog/category/article.html
                # Old: ../../../blog-images/  (3 up to s4-templates, then blog-images)
                # New: ../../../../images/blog-images/  (4 up to templates, then images/blog-images)
                # Also old: ../../../images/ for template images
                replacements = [
                    ('../../../blog-images/', '../../../../images/blog-images/'),
                    ('../../../images/', '../../../../images/template-images/'),
                ]
                if fix_file(fpath, replacements):
                    count += 1
    if count:
        print(f'  Fixed {count} blog articles')
    return count


def fix_blog_html_pages():
    """Fix paths in template-N/blog.html files."""
    count = 0
    for i in range(1, 21):
        blog_html = os.path.join(WEBSITE, f'template-{i}', 'blog.html')
        if not os.path.isfile(blog_html):
            continue
        replacements = [
            ('../blog-images/', '../../images/blog-images/'),
            ('../images/', '../../images/template-images/'),
        ]
        if fix_file(blog_html, replacements):
            count += 1
            print(f'  Fixed template-{i}/blog.html')
    return count


def fix_proposals():
    """Fix paths in proposal template HTML files."""
    count = 0
    for fname in os.listdir(PROPOSALS):
        if not fname.endswith('.html') or fname == 'gallery.html':
            continue
        fpath = os.path.join(PROPOSALS, fname)
        # Old: ../../image to be used/imageN.png  (2 up from templates_new to Dentists)
        # New: ../images/template-images/imageN.png  (1 up from proposals to templates)
        replacements = [
            ('../../image to be used/', '../images/template-images/'),
        ]
        if fix_file(fpath, replacements):
            count += 1
            print(f'  Fixed {fname}')
    return count


def fix_python_scripts():
    """Fix relative paths in Python scripts."""
    count = 0
    for fname in os.listdir(WEBSITE):
        if not fname.endswith('.py'):
            continue
        fpath = os.path.join(WEBSITE, fname)
        # Scripts reference blog-images and images relative to their location
        # They were in s4-templates/, now in templates/website/
        # Internal references like '../blog-images' → need to become paths to new location
        replacements = [
            ("'../blog-images/", "'../../templates/images/blog-images/"),
            ('"../blog-images/', '"../../images/blog-images/'),
            ("'../images/", "'../../templates/images/template-images/"),
            ('"../images/', '"../../images/template-images/'),
            # For BLOG_IMAGES constant used in inject_service_images.py
            ("BLOG_IMAGES = '../blog-images'", "BLOG_IMAGES = '../../images/blog-images'"),
        ]
        if fix_file(fpath, replacements):
            count += 1
            print(f'  Fixed {fname}')
    return count


def fix_gallery_crosslinks():
    """Fix cross-navigation links between the two galleries."""
    # Website gallery
    wg = os.path.join(WEBSITE, 'gallery.html')
    if os.path.isfile(wg):
        replacements = [
            # If it links to proposals gallery
            ('templates_new/gallery.html', '../proposals/gallery.html'),
            ('../../reports/proposals/templates_new/gallery.html', '../proposals/gallery.html'),
        ]
        if fix_file(wg, replacements):
            print('  Fixed website/gallery.html cross-links')

    # Proposals gallery
    pg = os.path.join(PROPOSALS, 'gallery.html')
    if os.path.isfile(pg):
        replacements = [
            # If it links to website gallery
            ('../../s4-templates/gallery.html', '../website/gallery.html'),
        ]
        if fix_file(pg, replacements):
            print('  Fixed proposals/gallery.html cross-links')


def main():
    print('=== Fixing website template paths ===')
    fix_website_templates()

    print('\n=== Fixing blog.html pages ===')
    fix_blog_html_pages()

    print('\n=== Fixing blog articles ===')
    fix_blog_articles()

    print('\n=== Fixing proposal templates ===')
    fix_proposals()

    print('\n=== Fixing Python scripts ===')
    fix_python_scripts()

    print('\n=== Fixing gallery cross-links ===')
    fix_gallery_crosslinks()

    print('\nDone!')


if __name__ == '__main__':
    main()
