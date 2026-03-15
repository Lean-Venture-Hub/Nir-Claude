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
│   ├── {vertical}/                    — one folder per vertical
│   │   ├── website/template-{N}/      — template HTML + blog/
│   │   └── images/template-images/    — shared images for all templates
│   │       (templates reference ../../images/template-images/ relative)
│   ├── auto-repair/    (26 templates, 30 images)
│   ├── dentists/       (25 templates, 18 images)
│   ├── landscaping/    (13 templates, 10 images)
│   ├── veterinarians/  (10 templates, 10 images)
│   ├── med-spas/       (10 templates, 10 images)
│   └── hvac/           (10 templates, 10 images)
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

- 6 vertical tabs: Dentists (default), Auto-Repair, Landscaping, Veterinarians, Med Spas, HVAC
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

## Deploy Mistakes to AVOID

| Mistake | What happens | Fix |
|---------|-------------|-----|
| `rsync templates/{v}/website/ → server/{v}/` (missing `website/`) | Templates land at `{v}/template-{N}/` instead of `{v}/website/template-{N}/` | Gallery iframe paths break — thumbnails show blank |
| Forgetting to deploy `images/` | All template images 404 on server | Always deploy images AND templates (2 separate rsyncs) |
| Using `--delete` on the vertical root | Deletes `images/` or `website/` dir | Only use `--delete` within `website/` or `images/` subdirs |

## Feedback API

Flask microservice on port 5111, proxied by nginx at `/api/`.

**Files:**
- App: `/opt/feedback-api/app.py`
- Service: `/etc/systemd/system/feedback-api.service`
- Data: `/var/www/lp.scalefox.ai/feedback/` (`gallery-feedback.json`, `sections-feedback.json`, `feedback-log.jsonl`)

**Endpoints:**
- `GET /api/feedback/health` — health check
- `GET /api/feedback/gallery` — all gallery feedback (likes, comments, summary)
- `GET /api/feedback/sections` — all section builder feedback (ratings, bugs, summary)
- `POST /api/feedback` — submit feedback `{tool, user, action, key, value}`

**Deploy:**
```bash
# Deploy API code
rsync -avz -e "ssh -i ~/.ssh/test_env_ec2.pem" feedback-api/app.py ubuntu@18.184.97.242:/opt/feedback-api/

# Restart service
ssh -i ~/.ssh/test_env_ec2.pem ubuntu@18.184.97.242 "sudo systemctl restart feedback-api"
```

**Nginx config addition** (`/etc/nginx/sites-available/lp.scalefox.ai`):
```nginx
location /api/ {
    proxy_pass http://127.0.0.1:5111/api/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

**Read feedback from Claude Code:**
```bash
ssh -i ~/.ssh/test_env_ec2.pem ubuntu@18.184.97.242 "cat /var/www/lp.scalefox.ai/feedback/gallery-feedback.json"
```

## Current Template Count (as of 2026-03-15)

| Vertical | Templates | Images | Last Updated |
|----------|-----------|--------|-------------|
| Dentists | 25 | 18 | 2026-03-13 |
| Auto-repair | 26 | 30 | 2026-03-15 |
| Landscaping | 13 | 10 | 2026-03-13 |
| Veterinarians | 10 | 10 | 2026-03-14 |
| Med Spas | 10 | 10 | 2026-03-14 |
| HVAC | 10 | 10 | 2026-03-14 |
| Proposals | 20 | — | 2026-03-14 |
| Individual sites | ~88 | — | — |
