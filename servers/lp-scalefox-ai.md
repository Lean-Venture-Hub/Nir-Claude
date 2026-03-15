# lp.scalefox.ai — Server Reference

## TL;DR

Production server hosting template galleries, proposal galleries, a clinic directory, and ~88 individual dentist landing pages. AWS EC2 + nginx + Let's Encrypt SSL.

## Connection

- **SSH:** `ssh -i ~/.ssh/test_env_ec2.pem ubuntu@18.184.97.242`
- **Web root:** `/var/www/lp.scalefox.ai/`
- **Nginx config:** `/etc/nginx/sites-available/lp.scalefox.ai`

## Deploy Commands

```bash
# 1. Fix ownership (before rsync)
ssh -i ~/.ssh/test_env_ec2.pem ubuntu@18.184.97.242 "sudo chown -R ubuntu:ubuntu /var/www/lp.scalefox.ai/{target}/"

# 2. Rsync files
rsync -avz -e "ssh -i ~/.ssh/test_env_ec2.pem" local_dir/ ubuntu@18.184.97.242:/var/www/lp.scalefox.ai/{target}/

# 3. Restore ownership (after rsync)
ssh -i ~/.ssh/test_env_ec2.pem ubuntu@18.184.97.242 "sudo chown -R www-data:www-data /var/www/lp.scalefox.ai/{target}/ && sudo chmod -R 755 /var/www/lp.scalefox.ai/{target}/"
```

## Directory Structure

```
/var/www/lp.scalefox.ai/
├── gallerywebsite/                    → lp.scalefox.ai/gallerywebsite/
│   ├── gallery.html                   — main gallery page (tabs per vertical)
│   ├── index.html                     — redirect/landing
│   ├── auto-repair/
│   │   └── website/template-{1-26}/   — 26 auto-repair templates
│   ├── dentists/
│   │   └── website/template-{1-25}/   — 25 dentist templates
│   └── landscaping/
│       └── website/template-{1-13}/   — 13 landscaping templates
│
├── galleryproposal/                   → lp.scalefox.ai/galleryproposal/
│   ├── gallery.html                   — proposal gallery
│   └── template-{1-20}-{name}.html    — 20 proposal templates (1-10 HE+EN dental, 11-20 EN auto repair)
│
├── directory/                         → lp.scalefox.ai/directory/
│   └── index.html                     — clinic directory page
│
└── {clinic-slug}/                     — ~88 individual dentist landing pages
    ├── index.html                     — landing page
    ├── blog.html                      — blog listing
    ├── blog/{article-slug}/           — blog articles
    └── images/                        — template-images/ + blog-images/
```

## Gallery Details

**URL:** `https://lp.scalefox.ai/gallerywebsite/gallery.html`

- 3 vertical tabs: Dentists (default), Auto-Repair, Landscaping
- Filter buttons per vertical (light/dark/editorial/bold/etc.)
- Language toggle (HE/EN) for dentists
- Each card links to the template's `template_example-{N}.html`
- Gallery config is inline JS in `gallery.html` — template list defined in `verticals` object

**Template file convention:**
- `template_example-{N}.html` — viewable example (Hebrew RTL)
- `template_example-{N}-en.html` — English version (dentists only)
- `template-{N}.html` — base template with `{{PLACEHOLDER}}` tokens
- Images: `../../images/template-images/` relative path

## Local ↔ Server Path Mapping

| Local | Server |
|-------|--------|
| `templates/gallery.html` | `/gallerywebsite/gallery.html` |
| `templates/{vertical}/website/template-{N}/` | `/gallerywebsite/{vertical}/website/template-{N}/` |
| `templates/{vertical}/images/` | `/gallerywebsite/{vertical}/images/` |
| `templates/proposals/gallery.html` | `/galleryproposal/gallery.html` |

## Current Template Count (as of 2026-03-13)

| Vertical | Templates | Last Updated |
|----------|-----------|-------------|
| Dentists | 25 | 2026-03-13 |
| Auto-repair | 26 | 2026-03-14 |
| Landscaping | 13 | 2026-03-13 |
| Proposals | 20 | 2026-03-14 |
| Individual sites | ~88 | — |
