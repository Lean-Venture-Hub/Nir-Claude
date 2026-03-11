#!/usr/bin/env python3
"""Take full-page screenshots of index.html, blog.html, and one article page for each dentist."""

import os, glob
from playwright.sync_api import sync_playwright

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def screenshot_file(page, html_path, png_path):
    """Open a local HTML file and take a full-page screenshot."""
    if not os.path.exists(html_path):
        print(f"    SKIP (not found): {html_path}")
        return False
    try:
        page.goto(f"file://{html_path}", wait_until="networkidle", timeout=15000)
        page.wait_for_timeout(500)
        page.screenshot(path=png_path, full_page=True)
        return True
    except Exception as e:
        print(f"    ERROR: {e}")
        return False


def find_article(dentist_dir):
    """Find the first article HTML file in the blog subdirectories."""
    blog_dir = os.path.join(dentist_dir, "blog")
    if not os.path.isdir(blog_dir):
        return None
    for root, dirs, files in os.walk(blog_dir):
        for f in files:
            if f.endswith(".html"):
                return os.path.join(root, f)
    return None


def main():
    dentists = sorted([
        d for d in os.listdir(OUTPUT_DIR)
        if os.path.isdir(os.path.join(OUTPUT_DIR, d))
    ])
    print(f"Taking screenshots for {len(dentists)} dentists...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=2,
        )
        page = context.new_page()

        for i, dentist in enumerate(dentists):
            ddir = os.path.join(OUTPUT_DIR, dentist)
            print(f"[{i+1}/{len(dentists)}] {dentist}")

            # Home page
            home_html = os.path.join(ddir, "index.html")
            home_png = os.path.join(ddir, "screenshot-home.png")
            if os.path.exists(home_png):
                print(f"    home: already exists, skipping")
            else:
                ok = screenshot_file(page, home_html, home_png)
                print(f"    home: {'OK' if ok else 'FAILED'}")

            # Blog page
            blog_html = os.path.join(ddir, "blog.html")
            blog_png = os.path.join(ddir, "screenshot-blog.png")
            if os.path.exists(blog_png):
                print(f"    blog: already exists, skipping")
            else:
                ok = screenshot_file(page, blog_html, blog_png)
                print(f"    blog: {'OK' if ok else 'FAILED'}")

            # Article page
            article_html = find_article(ddir)
            article_png = os.path.join(ddir, "screenshot-article.png")
            if os.path.exists(article_png):
                print(f"    article: already exists, skipping")
            elif article_html:
                ok = screenshot_file(page, article_html, article_png)
                print(f"    article: {'OK' if ok else 'FAILED'}")
            else:
                print(f"    article: no article HTML found")

        browser.close()

    print(f"\nDone! Screenshots saved in each dentist folder.")


if __name__ == "__main__":
    main()
