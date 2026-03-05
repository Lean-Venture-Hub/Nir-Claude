# Local Development Projects — Server Reference

All projects under `/Users/nirkosover/Library/Mobile Documents/com~apple~CloudDocs/Mine/Development/`.
Base path abbreviated as `~/Dev/` below.

---

## Dentist Platform (Claude code/)

| Project | Port | Command | Description |
|---------|------|---------|-------------|
| **Dashboard Admin** | 3000 | `npm run dev` | Internal admin dashboard — clinic management, content pipelines, budgets, system status |
| **Clinic Portal** | 3001 | `npm run dev` | Client-facing portal — clinic owners approve stories/reels/SEO, manage settings, view AI visibility |

**Static galleries** (no server — open HTML directly or `python3 -m http.server 8080`):

| Gallery | Path |
|---------|------|
| Website Templates | `~/Dev/Claude code/Dentists/s4-templates/gallery.html` |
| Proposal Templates | `~/Dev/Claude code/Dentists/reports/proposals/templates_new/gallery.html` |

---

## Personal Assistant (Projects/personal-assistant/)

| Project | Port | Command | Description |
|---------|------|---------|-------------|
| **Dana Hub** (Mission Control) | 3009 | `npm run dev` | Central dashboard — personal assistant hub, task management, life OS |
| **Maia Website** | 3002 | `npm run dev` | Portfolio/landing site — Framer Motion + Three.js animations, i18n (he/en) |

---

## Nadlan (Projects/nadlan/)

| Project | Port | Command | Description |
|---------|------|---------|-------------|
| **Nadlan Hub** | 3005 | `npm run dev` | Real estate analysis — neighborhoods, prices, rent, mortgage calcs for Tel Aviv. Express + Puppeteer |

---

## PM Frameworks (Projects/PM frames/)

| Project | Port | Command | Description |
|---------|------|---------|-------------|
| **PM Frameworks** | 3030 | `npm run dev` | Interactive PM frameworks explorer — Google Generative AI integration, Zustand state |

---

## AntiGravity Experiments (AntiGravity/)

| Project | Port | Command | Description |
|---------|------|---------|-------------|
| **Stocks App** | 3003 | `npm run dev` | Financial dashboard — stock data, Recharts visualizations |
| **Unstatic** | 5173 | `npm run dev` | 3D interactive UI — Vite + Three.js + React Router |
| **Product Lab** | 5173 | `npm run dev` | PM visualization lab — Vite + Chart.js |

---

## Quick-Start Cheat Sheet

```bash
# Dentist platform (both)
cd ~/Dev/"Claude code"/dashboard_admin && npm run dev &
cd ~/Dev/"Claude code"/clinic_portal && npm run dev &

# Personal assistant
cd ~/Dev/Projects/personal-assistant/hub && npm run dev &

# Nadlan
cd ~/Dev/Projects/nadlan && npm run dev &

# Galleries (static)
cd ~/Dev/"Claude code"/Dentists/s4-templates && python3 -m http.server 8080 &
```

## Port Map

| Port | Project |
|------|---------|
| 3000 | Dashboard Admin |
| 3001 | Clinic Portal |
| 3002 | Maia Website |
| 3003 | Stocks App |
| 3005 | Nadlan Hub |
| 3009 | Dana Hub (Mission Control) |
| 3030 | PM Frameworks |
| 5173 | Unstatic / Product Lab (Vite) |
| 8080 | Static galleries (manual) |
