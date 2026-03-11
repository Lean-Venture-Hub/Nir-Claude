#!/usr/bin/env python3
"""Record a screen-capture video of each dentist's website and blog."""

import os, time, shutil
from playwright.sync_api import sync_playwright

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
BASE_URL = "http://localhost:8787"

# Video settings
WIDTH = 1280
HEIGHT = 720
SCROLL_PAUSE = 0.8  # seconds between scroll steps
SCROLL_STEP = 300   # pixels per scroll step


def slow_scroll(page, pause=SCROLL_PAUSE, step=SCROLL_STEP):
    """Scroll down the page slowly, step by step."""
    total_height = page.evaluate("document.body.scrollHeight")
    current = 0
    while current < total_height:
        current += step
        page.evaluate(f"window.scrollTo({{top: {current}, behavior: 'smooth'}})")
        time.sleep(pause)
        # Re-check height (lazy-loaded content may extend the page)
        total_height = page.evaluate("document.body.scrollHeight")
    time.sleep(0.5)


def record_site(browser, slug, dest_folder):
    """Record video of a dentist's website + blog."""
    tmp_video_dir = os.path.join(SCRIPT_DIR, "_tmp_videos")
    os.makedirs(tmp_video_dir, exist_ok=True)

    context = browser.new_context(
        viewport={"width": WIDTH, "height": HEIGHT},
        record_video_dir=tmp_video_dir,
        record_video_size={"width": WIDTH, "height": HEIGHT},
    )
    page = context.new_page()

    try:
        # 1. Homepage — pause at top, then scroll
        page.goto(f"{BASE_URL}/{slug}/index.html", wait_until="networkidle", timeout=15000)
        time.sleep(2)
        slow_scroll(page)
        time.sleep(1)

        # 2. Blog listing
        page.goto(f"{BASE_URL}/{slug}/blog.html", wait_until="networkidle", timeout=15000)
        time.sleep(1.5)
        slow_scroll(page)
        time.sleep(1)

        # 3. Scroll back to top and pause
        page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
        time.sleep(1.5)

    except Exception as e:
        print(f"    Error during recording: {e}")

    # Close context to finalize video
    video_path = page.video.path()
    context.close()

    # Move video to the dentist's folder
    final_path = os.path.join(dest_folder, "site-walkthrough.webm")
    if os.path.exists(video_path):
        shutil.move(video_path, final_path)

    # Clean up tmp dir
    try:
        shutil.rmtree(tmp_video_dir, ignore_errors=True)
    except:
        pass

    return final_path


def main():
    folders = sorted([
        d for d in os.listdir(OUTPUT_DIR)
        if os.path.isdir(os.path.join(OUTPUT_DIR, d)) and not d.startswith('_')
    ])

    print(f"Recording videos for {len(folders)} dentists...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        for i, slug in enumerate(folders):
            dest = os.path.join(OUTPUT_DIR, slug)
            print(f"  [{i+1:2d}/{len(folders)}] {slug}...", end=" ", flush=True)
            video_path = record_site(browser, slug, dest)
            size_kb = os.path.getsize(video_path) // 1024 if os.path.exists(video_path) else 0
            print(f"done ({size_kb} KB)")

        browser.close()

    print(f"\nAll done! Videos saved as site-walkthrough.webm in each folder.")


if __name__ == "__main__":
    main()
