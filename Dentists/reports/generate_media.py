#!/usr/bin/env python3
"""Generate screenshots and video walkthroughs for each clinic report folder.

For each folder in output/:
  - screenshot-home.png    (index.html full page screenshot)
  - screenshot-blog.png    (blog.html screenshot)
  - screenshot-article.png (first blog article screenshot)
  - site-walkthrough.mp4   (scrolling video of index.html)
"""

import os, time, glob
from playwright.sync_api import sync_playwright

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# Video settings
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
SCROLL_PAUSE = 0.03  # seconds between scroll steps
SCROLL_STEP = 3  # pixels per scroll step


def take_screenshot(page, html_path, output_path, wait_ms=1000):
    """Navigate to a local HTML file and take a full-page screenshot."""
    file_url = f"file://{os.path.abspath(html_path)}"
    try:
        page.goto(file_url, wait_until="networkidle", timeout=10000)
        page.wait_for_timeout(wait_ms)
        page.screenshot(path=output_path, full_page=True)
        return True
    except Exception as e:
        print(f"    Screenshot error: {e}")
        return False


def record_walkthrough(context_factory, html_path, output_path):
    """Record a scrolling video walkthrough of a page."""
    file_url = f"file://{os.path.abspath(html_path)}"
    try:
        context = context_factory(
            viewport={"width": VIDEO_WIDTH, "height": VIDEO_HEIGHT},
            record_video_dir=os.path.dirname(output_path),
            record_video_size={"width": VIDEO_WIDTH, "height": VIDEO_HEIGHT},
        )
        page = context.new_page()
        page.goto(file_url, wait_until="networkidle", timeout=10000)
        page.wait_for_timeout(800)

        # Get page height
        total_height = page.evaluate("document.body.scrollHeight")
        viewport_height = VIDEO_HEIGHT
        current = 0

        # Smooth scroll down
        while current < total_height - viewport_height:
            current += SCROLL_STEP
            page.evaluate(f"window.scrollTo(0, {current})")
            time.sleep(SCROLL_PAUSE)

        # Pause at bottom
        page.wait_for_timeout(1000)

        # Scroll back up quickly
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(500)

        # Close to finalize video
        page.close()
        context.close()

        # Rename the video file (Playwright generates a random name)
        video_dir = os.path.dirname(output_path)
        for f in os.listdir(video_dir):
            if f.endswith('.webm') and f != os.path.basename(output_path):
                src = os.path.join(video_dir, f)
                # Convert to the expected filename
                os.rename(src, output_path)
                break
        return True
    except Exception as e:
        print(f"    Video error: {e}")
        return False


def find_first_article(folder):
    """Find the first blog article HTML in a folder."""
    blog_dir = os.path.join(folder, "blog")
    if not os.path.isdir(blog_dir):
        return None
    for cat in sorted(os.listdir(blog_dir)):
        cat_path = os.path.join(blog_dir, cat)
        if os.path.isdir(cat_path):
            for f in sorted(os.listdir(cat_path)):
                if f.endswith('.html'):
                    return os.path.join(cat_path, f)
    return None


def main():
    folders = sorted([
        d for d in os.listdir(OUTPUT_DIR)
        if os.path.isdir(os.path.join(OUTPUT_DIR, d)) and
        os.path.exists(os.path.join(OUTPUT_DIR, d, "index.html"))
    ])

    print(f"Generating media for {len(folders)} clinics...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for i, folder_name in enumerate(folders):
            folder = os.path.join(OUTPUT_DIR, folder_name)
            print(f"[{i+1}/{len(folders)}] {folder_name}")

            # Create a simple context for screenshots
            context = browser.new_context(
                viewport={"width": 1280, "height": 900},
                locale="he-IL",
            )
            page = context.new_page()

            # 1. Screenshot: Home
            index_path = os.path.join(folder, "index.html")
            shot_home = os.path.join(folder, "screenshot-home.png")
            if take_screenshot(page, index_path, shot_home):
                print(f"    screenshot-home.png")

            # 2. Screenshot: Blog
            blog_path = os.path.join(folder, "blog.html")
            if os.path.exists(blog_path):
                shot_blog = os.path.join(folder, "screenshot-blog.png")
                if take_screenshot(page, blog_path, shot_blog):
                    print(f"    screenshot-blog.png")

            # 3. Screenshot: Article
            article_path = find_first_article(folder)
            if article_path:
                shot_article = os.path.join(folder, "screenshot-article.png")
                if take_screenshot(page, article_path, shot_article):
                    print(f"    screenshot-article.png")

            page.close()
            context.close()

            # 4. Video walkthrough
            video_path = os.path.join(folder, "site-walkthrough.webm")
            if record_walkthrough(
                lambda **kw: browser.new_context(**kw),
                index_path,
                video_path
            ):
                print(f"    site-walkthrough.webm")

        browser.close()

    print(f"\nDone! Media generated for {len(folders)} clinics.")


if __name__ == '__main__':
    main()
