#!/usr/bin/env python3
"""Record a video walkthrough of home, blog, and article pages for each dentist."""

import os, shutil, sys, time
from playwright.sync_api import sync_playwright

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
VIDEO_FILENAME = sys.argv[1] if len(sys.argv) > 1 else "site-walkthrough2.webm"
SCROLL_PAUSE = 0.8
PAGE_PAUSE = 2.0


def smooth_scroll(page, step=300, pause=0.05):
    """Scroll down the full page in small increments."""
    total_height = page.evaluate("document.body.scrollHeight")
    current = 0
    while current < total_height:
        current += step
        page.evaluate(f"window.scrollTo(0, {current})")
        page.wait_for_timeout(int(pause * 1000))
    # Pause at bottom
    page.wait_for_timeout(int(SCROLL_PAUSE * 1000))
    # Scroll back to top
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(500)


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


def record_dentist(pw, dentist_dir, dentist_name):
    """Record a walkthrough video for one dentist."""
    video_dest = os.path.join(dentist_dir, VIDEO_FILENAME)
    if os.path.exists(video_dest):
        print(f"    already exists, skipping")
        return True

    tmp_video_dir = os.path.join(dentist_dir, "_tmp_video")
    os.makedirs(tmp_video_dir, exist_ok=True)

    browser = pw.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        record_video_dir=tmp_video_dir,
        record_video_size={"width": 1440, "height": 900},
    )
    page = context.new_page()

    try:
        # 1. Home page
        home_html = os.path.join(dentist_dir, "index.html")
        if os.path.exists(home_html):
            page.goto(f"file://{home_html}", wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(int(PAGE_PAUSE * 1000))
            smooth_scroll(page)

        # 2. Blog page
        blog_html = os.path.join(dentist_dir, "blog.html")
        if os.path.exists(blog_html):
            page.goto(f"file://{blog_html}", wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(int(PAGE_PAUSE * 1000))
            smooth_scroll(page)

        # 3. Article page
        article_html = find_article(dentist_dir)
        if article_html:
            page.goto(f"file://{article_html}", wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(int(PAGE_PAUSE * 1000))
            smooth_scroll(page)

        # Final pause
        page.wait_for_timeout(1000)

    except Exception as e:
        print(f"    ERROR during recording: {e}")

    # Close context to finalize video
    video_path = page.video.path()
    context.close()
    browser.close()

    # Move video to destination
    if os.path.exists(video_path):
        shutil.move(video_path, video_dest)
        # Cleanup tmp dir
        shutil.rmtree(tmp_video_dir, ignore_errors=True)
        return True
    else:
        shutil.rmtree(tmp_video_dir, ignore_errors=True)
        return False


def main():
    dentists = sorted([
        d for d in os.listdir(OUTPUT_DIR)
        if os.path.isdir(os.path.join(OUTPUT_DIR, d))
    ])
    print(f"Recording walkthroughs for {len(dentists)} dentists...\n")

    with sync_playwright() as pw:
        for i, dentist in enumerate(dentists):
            ddir = os.path.join(OUTPUT_DIR, dentist)
            print(f"[{i+1}/{len(dentists)}] {dentist}...", end=" ", flush=True)
            ok = record_dentist(pw, ddir, dentist)
            print("OK" if ok else "FAILED")

    print(f"\nDone! Videos saved as {VIDEO_FILENAME} in each dentist folder.")


if __name__ == "__main__":
    main()
