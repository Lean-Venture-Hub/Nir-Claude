#!/usr/bin/env python3
"""
Generate blog pages for all 30 auto repair websites.
Copies blog.html + 3 blog articles from the assigned template,
replaces business name, city, phone, and image paths.
"""
import os, re, json, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
TEMPLATES_DIR = os.path.join(ROOT, "templates", "auto-repair", "website")
WEBSITES_DIR = os.path.join(BASE, "reports", "websites")
MANIFEST = os.path.join(BASE, "reports", "batch-manifest.json")

# Load manifest
with open(MANIFEST) as f:
    businesses = json.load(f)

def read_content_md(web_dir):
    """Extract key fields from content.md."""
    content_path = os.path.join(web_dir, "content.md")
    with open(content_path, "r") as f:
        text = f.read()

    data = {}
    # Parse fields
    for line in text.split("\n"):
        if line.startswith("- **Name:**"):
            data["name"] = line.split(":**")[1].strip()
        elif line.startswith("- **City:**"):
            data["city"] = line.split(":**")[1].strip()
        elif line.startswith("- **Phone:**"):
            data["phone"] = line.split(":**")[1].strip()
        elif line.startswith("- **Google Rating:**"):
            data["rating"] = line.split(":**")[1].strip().split(" ")[0]
        elif line.startswith("- **Category:**"):
            data["category"] = line.split(":**")[1].strip()

    # Derive short name
    name = data.get("name", "")
    # Common short name patterns
    short = name.split(" - ")[0].split(" | ")[0].split(",")[0].strip()
    if len(short) > 25:
        words = short.split()
        short = " ".join(words[:3])
    data["short_name"] = short

    return data

def replace_content(html, biz_data):
    """Replace template placeholder content with real business data."""
    name = biz_data.get("name", "")
    short = biz_data.get("short_name", name)
    city_state = biz_data.get("city", "")
    phone = biz_data.get("phone", "")
    rating = biz_data.get("rating", "")

    # Extract just city name (before comma/state)
    city = city_state.split(",")[0].strip() if "," in city_state else city_state

    # Replace business names
    html = html.replace("Precision Auto Care", name)
    html = html.replace("Precision Auto Works", name)
    html = html.replace("Precision Auto", short)

    # Replace cities
    html = html.replace("Austin, TX", city_state)
    html = html.replace("Austin, Texas", city_state)
    html = html.replace("in Austin", f"in {city}")
    html = html.replace("Austin TX", city_state.replace(",", ""))
    html = re.sub(r'(?<!\w)Austin(?!\w)', city, html)

    # Replace phone
    html = re.sub(r'\(555\)\s*\d{3}[- ]\d{4}', phone, html)
    html = re.sub(r'tel:\+?1?555\d{7}', f'tel:{phone_to_tel(phone)}', html)

    # Fix image paths - blog articles are 2 levels deep from images
    # blog.html is at same level as images/
    # blog/article/index.html needs ../../images/

    return html

def phone_to_tel(phone):
    """Convert display phone to tel: format."""
    digits = re.sub(r'[^\d]', '', phone)
    if len(digits) == 10:
        return f"+1{digits}"
    return f"+{digits}"

def process_blog_listing(template_dir, web_dir, biz_data):
    """Copy and customize blog.html listing page."""
    src = os.path.join(template_dir, "blog.html")
    if not os.path.exists(src):
        return False

    with open(src, "r") as f:
        html = f.read()

    html = replace_content(html, biz_data)

    # Fix image paths: ../../images/template-images/ → images/
    html = html.replace("../../images/template-images/", "images/")
    # Also fix ../images/ patterns
    html = html.replace("../images/template-images/", "images/")

    dst = os.path.join(web_dir, "blog.html")
    with open(dst, "w") as f:
        f.write(html)
    return True

def process_blog_articles(template_dir, web_dir, biz_data):
    """Copy and customize all blog article pages."""
    blog_src = os.path.join(template_dir, "blog")
    if not os.path.isdir(blog_src):
        return 0

    blog_dst = os.path.join(web_dir, "blog")
    os.makedirs(blog_dst, exist_ok=True)

    count = 0
    for article_dir in os.listdir(blog_src):
        article_src = os.path.join(blog_src, article_dir)
        if not os.path.isdir(article_src):
            continue

        article_dst = os.path.join(blog_dst, article_dir)
        os.makedirs(article_dst, exist_ok=True)

        # Process index.html
        src_file = os.path.join(article_src, "index.html")
        if os.path.exists(src_file):
            with open(src_file, "r") as f:
                html = f.read()

            html = replace_content(html, biz_data)

            # Blog articles are at blog/article-slug/index.html
            # Images are at images/ (root level)
            # So path from article to images is ../../images/
            html = html.replace("../../../../images/template-images/", "../../images/")
            html = html.replace("../../../images/template-images/", "../../images/")
            html = html.replace("../../images/template-images/", "../../images/")

            dst_file = os.path.join(article_dst, "index.html")
            with open(dst_file, "w") as f:
                f.write(html)
            count += 1

    return count

def main():
    print(f"Generating blogs for {len(businesses)} businesses...\n")

    for biz in businesses:
        slug = biz["slug"]
        template_num = biz["template"]
        template_dir = os.path.join(TEMPLATES_DIR, f"template-{template_num}")
        web_dir = os.path.join(WEBSITES_DIR, slug)

        # Read content.md for business data
        biz_data = read_content_md(web_dir)

        # Generate blog listing
        listing_ok = process_blog_listing(template_dir, web_dir, biz_data)

        # Generate blog articles
        article_count = process_blog_articles(template_dir, web_dir, biz_data)

        status = "✓" if listing_ok and article_count > 0 else "⚠"
        print(f"{status} {biz['idx']:2d}. {biz['name'][:40]:<42} blog.html + {article_count} articles (T{template_num})")

    print(f"\n✅ Blog generation complete!")

if __name__ == "__main__":
    main()
