# scalefox.ai — Server Reference

## Connection

```bash
ssh -i ~/.ssh/test_env_ec2.pem ubuntu@52.58.164.186
```

## Server Details

| Field | Value |
|-------|-------|
| **IP** | 52.58.164.186 |
| **Hostname** | ip-172-31-47-14 |
| **Domain** | scalefox.ai / www.scalefox.ai |
| **OS** | Ubuntu (AWS EC2) |
| **Disk** | 6.8G total, 2.6G used, 4.2G free (38%) |
| **SSL** | Let's Encrypt (certbot-managed) |
| **Web server** | Nginx |
| **Web root** | `/var/www/html` |

## Nginx Routing

- `scalefox.ai/` → redirects to `/dana/en/dana2/`
- `scalefox.ai/dana` → redirects to `/dana/en/dana2/`
- All other paths → static file serving from `/var/www/html`
- HTTP → HTTPS redirect (certbot-managed)

## Site Structure

```
/var/www/html/
├── assets/
└── dana/
    ├── _next/                    ← Next.js static build chunks + CSS
    ├── favicon.png
    ├── en/
    │   ├── dana1/                ← Landing page variant 1
    │   ├── dana2/                ← Landing page variant 2 (ACTIVE — default redirect target)
    │   │   ├── privacy/index.html
    │   │   └── terms/index.html
    │   ├── dana3/                ← Landing page variant 3
    │   └── purple/               ← Purple theme variant
    └── he/
        ├── dana1/
        ├── dana2/
        │   ├── privacy/index.html
        │   └── terms/index.html
        ├── dana3/
        └── purple/
```

## Deployment

This is a **Next.js static export** served by Nginx. To deploy updates:

1. Build locally: `npm run build` (produces `out/` folder)
2. Upload: `scp -i ~/.ssh/test_env_ec2.pem -r out/* ubuntu@52.58.164.186:/var/www/html/dana/`
3. Or SSH in and edit static HTML files directly for small changes

## Key Files

| File | URL |
|------|-----|
| EN landing page | `/var/www/html/dana/en/dana2/index.html` → scalefox.ai/dana/en/dana2/ |
| HE landing page | `/var/www/html/dana/he/dana2/index.html` → scalefox.ai/dana/he/dana2/ |
| EN privacy | `/var/www/html/dana/en/dana2/privacy/index.html` → scalefox.ai/dana/en/dana2/privacy/ |
| EN terms | `/var/www/html/dana/en/dana2/terms/index.html` → scalefox.ai/dana/en/dana2/terms/ |
| HE privacy | `/var/www/html/dana/he/dana2/privacy/index.html` |
| HE terms | `/var/www/html/dana/he/dana2/terms/index.html` |
| Nginx config | `/etc/nginx/sites-enabled/default` |
| SSL certs | `/etc/letsencrypt/live/scalefox.ai/` |

## Change Log

| Date | File | Change |
|------|------|--------|
| 2026-03-15 | EN privacy page | Added 7 subsections under "Information We Collect": WhatsApp Messaging, Google Account Integration, AI Processing, Voice Messages, Personalization & Memory, Proactive Notifications, Data Deletion. Backup at `index.html.bak` |

## Notes

- This is a DIFFERENT server from lp.scalefox.ai (18.184.97.242)
- The privacy/terms pages are static Next.js HTML with embedded React hydration — can be edited directly but Next.js RSC payload at the bottom will still show old content until a full rebuild
- For text-only changes to privacy/terms, editing the visible HTML in the `<main>` tag works fine
