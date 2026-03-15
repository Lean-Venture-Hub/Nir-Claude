# Folder Reorganization Plan (v2 — audited)

**TL;DR:** Split monorepo into 6 repos. Each maps to a server, data pipeline, app, or command center.

**Total current repo:** ~6GB. Biggest culprits: `Dentists/` (2.9GB, includes venv), `US Dentists/` (1.0GB), `clinic_portal/` (894MB), `dashboard_admin/` (676MB), `templates/` (322MB).

---

## Target Repos

| # | Repo | Purpose | Server | Status |
|---|------|---------|--------|--------|
| 1 | `scalefox-ai` | Dana landing pages | scalefox.ai (52.58.164.186) | DONE |
| 2 | `scalefox-lp` | Templates, galleries, proposals, generated sites, builder tools | lp.scalefox.ai (18.184.97.242) | TODO |
| 3 | `scalefox-leads` | CSVs, Python scripts, city data, outreach | none (offline) | TODO |
| 4 | `scalefox-workspace` | Command center: .claude/, skills, design, strategy, research | none | Current repo — clean |
| 5 | `scalefox-clinic-portal` | Next.js clinic portal | localhost:3001 | TODO |
| 6 | `scalefox-dashboard` | Next.js admin dashboard | localhost:3000 | TODO |

---

## Repo 1: `scalefox-ai` — DONE

No changes needed.

---

## Repo 2: `scalefox-lp` — everything on lp.scalefox.ai

```
scalefox-lp/
├── SERVER.md                       ← from servers/lp-scalefox-ai.md
├── gallery.html                    ← main template gallery
│
├── templates/
│   ├── dentists/
│   │   ├── website/template-{1-25}/
│   │   └── images/                 ← KEEP images with vertical (server path match)
│   ├── auto-repair/
│   │   ├── website/template-{1-26}/
│   │   └── images/
│   ├── landscaping/website/template-{1-13}/
│   ├── veterinarians/website/template-{1-10}/
│   ├── med-spas/website/template-{1-10}/
│   └── hvac/website/template-{1-10}/
│
├── proposals/
│   ├── gallery.html
│   └── template-{1-20}-{name}.html
│
├── sites/                          ← generated per-business websites
│   ├── directory/index.html
│   ├── dentists-il/                ← 60 sites from Dentists/reports/output/
│   └── dentists-us/                ← 27 sites from US Dentists/1 Reports/output/
│
├── tools/
│   ├── section-scanner.js
│   └── builder/
│       ├── index.html
│       ├── editor.html
│       └── sections-data.js        ← generated
│
└── feedback-api/                   ← gallery feedback backend
    ├── app.py
    ├── deploy.sh
    ├── feedback-api.service
    └── migrate-existing.py
```

### Source → destination mapping

| From (current repo) | To (scalefox-lp) | Notes |
|---------------------|-------------------|-------|
| `templates/gallery.html` | `gallery.html` | |
| `templates/{vertical}/website/` | `templates/{vertical}/website/` | |
| `templates/{vertical}/images/` | `templates/{vertical}/images/` | **CHANGED: keep images with templates** |
| `templates/proposals/` | `proposals/` | |
| `Dentists/reports/output/` (60 folders) | `sites/dentists-il/` | |
| `US Dentists/1 Reports/output/` (27 folders) | `sites/dentists-us/` | |
| `tools/builder/` | `tools/builder/` | |
| `tools/section-scanner.js` | `tools/section-scanner.js` | |
| `servers/lp-scalefox-ai.md` | `SERVER.md` | |
| `feedback-api/` | `feedback-api/` | **ADDED: was missing** |

### Changes from v1
- **Images stay with templates** — v1 moved images to separate `images/` dir. This breaks relative paths in templates (`../images/...`) and mismatches server structure (`gallerywebsite/{vertical}/images/`).
- **feedback-api/ added** — was completely missing from v1. It's the gallery feedback backend (Flask app with systemd service).
- **Removed PLACEHOLDER_CONTRACT.md, INDEX.md, section-taxonomy.md** — these are skill reference docs used by workspace skills. They stay in workspace (see Repo 4).

### section-scanner.js update needed
After move, update paths in scanner:
- `TEMPLATES_DIR` → `path.join(ROOT, 'templates')` (stays same)
- `OUTPUT_FILE` → `path.join(ROOT, 'tools', 'builder', 'sections-data.js')` (stays same)
- Structure unchanged — scanner runs from within this repo

---

## Repo 3: `scalefox-leads` — data & scripts

```
scalefox-leads/
├── .env                            ← API keys
├── .gitignore                      ← ignore venv/, large CSVs if needed
├── scripts/
│   └── scan_smb.py
│
├── dentists-il/
│   ├── *.csv (gush-dan, labeled, outreach, reviews, reclassified)
│   ├── *.py (enrich, scrape, generate — 8 scripts)
│   ├── *.md (apify-pipeline-plan, outreach-*, segment-*, lost-revenue-*, dental-clinic-*)
│   ├── copy/                       ← outreach messages (cold-outreach, lost-revenue-report-design, outreach-by-segment)
│   ├── reports/                    ← audit scripts + batch CSVs (NOT output/)
│   │   ├── Old/                    ← old proposals/s1-s4 reports
│   │   ├── *.py, *.csv
│   ├── israel-dental-research/
│   ├── Specific Research/
│   └── Dr_Andy_Audit/
│
├── dentists-us/
│   ├── CLAUDE.md                   ← local context file
│   ├── *.md (outreach strategy, segment playbooks, instagram-flows, next-markets)
│   ├── Atlanta/, Austin/, Charlotte/, Denver/, DFW/, Houston/
│   ├── LasVegas/, Nashville/, NY/, Phoenix/, Tampa/
│   ├── 1 Reports/                  ← scripts + Inbox_list (NOT output/)
│   └── combined-analysis/
│
├── auto-repair/
│   ├── *.csv, *.py
│   ├── proposals/output/
│   ├── research/
│   └── PLAN.md
│
├── landscaping/
│   ├── *.csv (atlanta, dallas)
│   └── PLAN.md
│
└── med-spas/
    ├── Atlanta/, Charlotte/, DFW/, Houston/, NYC/, Phoenix/
    ├── strategy/
    └── med-spa-market-analysis.md
```

### Source → destination mapping

| From (current repo) | To (scalefox-leads) | Notes |
|---------------------|---------------------|-------|
| `Dentists/*.py`, `*.csv` | `dentists-il/` | 8 py scripts, 5 CSVs |
| `Dentists/*.md` | `dentists-il/` | **ADDED: 8 .md files were missing from v1** |
| `Dentists/copy/` | `dentists-il/copy/` | **ADDED: outreach message templates** |
| `Dentists/israel-dental-research/` | `dentists-il/israel-dental-research/` | |
| `Dentists/Specific Research/` | `dentists-il/Specific Research/` | |
| `Dentists/Dr_Andy_Audit/` | `dentists-il/Dr_Andy_Audit/` | |
| `Dentists/reports/` (NOT output/) | `dentists-il/reports/` | Includes `Old/` subdir |
| `US Dentists/` (NOT 1 Reports/output/) | `dentists-us/` | **ADDED: CLAUDE.md, Inbox_list/** |
| `Auto Repair/` | `auto-repair/` | |
| `Landscaping/` | `landscaping/` | |
| `Med Spas/` | `med-spas/` | |
| `scripts/scan_smb.py` | `scripts/` | |

### Changes from v1
- **Dentists/*.md files added** — v1 only listed `*.py` and `*.csv`. There are 8 markdown files (outreach strategy, pipeline plans, etc.)
- **Dentists/copy/ added** — 3 outreach message template files, essential for sales
- **Dentists/reports/Old/ noted** — contains historical proposals and s1-s4 reports
- **US Dentists/CLAUDE.md and 1 Reports/Inbox_list/ noted** — were missing
- **Vertical research files stay in workspace** — v1 moved `research/{vertical}.md` here. Wrong — skills reference these. See Repo 4.
- **reviews/ → delete** — only contains `gtm-playbook-critic.md` (one-off, stale)

### Delete (don't move)
| Item | Reason |
|------|--------|
| `Dentists/venv/` | **Python virtualenv — possibly ~500MB+. DELETE.** v1 missed this entirely |
| `Dentists/image to be used/` | **Stock images (11 files) — v1 missed. Move to scalefox-lp images or delete** |

---

## Repo 4: `scalefox-workspace` — cleaned current repo

```
scalefox-workspace/
├── .claude/                        ← skills, agents, hooks, settings
├── .env
├── .gitignore
├── CLAUDE.md
├── PLAN.md
├── SESSIONS.md
├── PROJECTS.md
├── lessonslearned.md
│
├── servers/                        ← connection docs (point to other repos)
│   ├── scalefox-ai.md
│   └── lp-scalefox-ai.md
│
├── templates/                      ← skill reference docs ONLY (no actual templates)
│   ├── PLACEHOLDER_CONTRACT.md     ← used by template-creator + create-website-from-template skills
│   ├── INDEX.md
│   └── section-taxonomy.md
│
├── design-inspiration/             ← used by template-creator, web-design-research skills
│   ├── web-design-playbook.md
│   ├── sites.csv
│   ├── inspiration-sources.md
│   └── screenshots/
│
├── research/                       ← ALL research stays here (vertical + general)
│   ├── auto-repair.md              ← vertical research (used by skills)
│   ├── landscaping.md
│   ├── landscaping-vertical-research.md
│   ├── landscaping-websites-list.md
│   ├── med-spas.md
│   ├── med-spa-vertical-deep-dive.md
│   ├── hvac.md
│   ├── veterinarians.md
│   ├── next-vertical-analysis.md
│   ├── folder-reorganization.md
│   ├── self-improvement-recommendations.md
│   ├── claude-code-setup-best-practices.md
│   ├── agents-skills-recommendations.md
│   ├── skill-animation-fixes.md
│   ├── SMBs/                       ← vertical selection framework, scoring
│   └── ... (API guides, tool briefs — 15+ files)
│
├── product/                        ← merged from 6 scattered folders
│   ├── specs/                      ← scalefox3.0/product-specs/ (4 files)
│   ├── agents/                     ← scalefox3.0/product-agents/ (10 files + subdir)
│   ├── assistant/                  ← Assistant/ (10 files + subdirs)
│   ├── app-screens/                ← Scalefox_Product/ (3 files) — **ADDED: was missing from v1**
│   ├── frameworks/                 ← Scalefox Inner Frameworks/ — **ADDED: was "merge into product" but no dest**
│   ├── company-info.md             ← scalefox3.0/company-info.md
│   ├── product-info.md             ← root product-info.md
│   ├── instagram-dental/           ← products/instagram-dental/
│   ├── booking-widget/             ← Dentists/booking widget/
│   └── customer-journey/           ← Dentists/customer_journey/
│
├── marketing/                      ← merged from 7 scattered folders
│   ├── linkedin/                   ← Linkedin Strategy/ + scalefox3.0/research/linkedin-strategy-analysis
│   ├── meta-ads/                   ← Meta Ad Strategy/ + configuration/ + scalefox-ad-brief.md
│   ├── content/                    ← content/ + Blog Content/ + creative/
│   ├── campaigns/                  ← Scalefox Marketing/
│   └── competitive/                ← competitors analysis/
│
├── strategy/
│   ├── dental-outreach-strategy.md
│   ├── linkedin-30-day-plan.md     ← also scalefox3.0/linkedin-1month-3k-plan.md (dedup)
│   └── new-verticals-analysis.md
│
├── memory/                         ← auto-memory (managed by Claude)
│
└── feedback/                       ← gallery feedback data
    └── gallery-feedback-2026-03-15.json
```

### Changes from v1
- **`templates/` dir kept for skill reference docs** — PLACEHOLDER_CONTRACT.md, INDEX.md, section-taxonomy.md stay here. Skills reference `templates/PLACEHOLDER_CONTRACT.md`. Moving them breaks skills.
- **Vertical research stays here** — v1 moved `research/{vertical}.md` to scalefox-leads. Wrong — `template-creator` and `vertical-research` skills read these files. ALL research stays in workspace.
- **Scalefox_Product/ → product/app-screens/** — v1 completely missed this folder (3 files: APP_SCREENS.md, content-system-suggestion.md, new_onboarding.md)
- **Scalefox Inner Frameworks/ → product/frameworks/** — v1 said "merge into product" but didn't specify destination
- **scalefox3.0/ fully mapped** — v1 didn't detail what happens to `gtm-playbook-example.md`, `linkedin-1month-3k-plan.md`, `performance-audit.md`, `README.md`, `research/` subdir, empty `user-flows/`
- **research/SMBs/ and research/tests/ noted** — v1 missed these subdirs
- **Duplicate linkedin strategy files noted** — `strategy/linkedin-30-day-plan.md` and `scalefox3.0/linkedin-1month-3k-plan.md` may overlap — dedup during merge
- **Blog Content/ explicitly mapped** — v1 mentioned it in passing but didn't list in mapping

### Post-move: Update references
After split, these files need path updates:
- `CLAUDE.md` — remove pipeline reference to `servers/lp-scalefox-ai.md` if it moves, update any template paths
- `PLAN.md` — update "Key References" table
- `.claude/skills/template-creator/` — references `templates/` and `design-inspiration/`
- `.claude/skills/create-website-from-template/` — references `templates/PLACEHOLDER_CONTRACT.md`
- `.claude/skills/web-design-research/` — references `design-inspiration/`
- `.claude/skills/vertical-research/` — references `research/`
- Memory files — `server_scalefox.md` needs update for new repo structure

---

## Repos 5 & 6: Apps

| Repo | From | Size | Notes |
|------|------|------|-------|
| `scalefox-clinic-portal` | `clinic_portal/` | 894MB | Independent Next.js app |
| `scalefox-dashboard` | `dashboard_admin/` | 676MB | Independent Next.js app |

**Note:** `dashboard/` (16KB) is separate from `dashboard_admin/` (676MB). Check if `dashboard/` is a stub/config or an older version before merging them.

---

## Delete from current repo

| Item | Size | Action |
|------|------|--------|
| `audit-gallery.jpeg`, `audit-template-*.jpeg`, `t21-*.jpeg`, `template-*.jpeg/png` | ~4MB | Delete (temp screenshots) |
| `Nova Dental UI UX Design.mp4`, `web-example2.mp4` | ~35MB | Move to Google Drive, then delete |
| `tmp-video-frames/` | 5MB | Delete |
| `CLAUDE 2.md`, `Claude 3.md`, `Claude 4.md` | 8KB | Delete (git has history) |
| `lovable-prompting.md` | 43KB | Delete (old reference) |
| `progress-log.md` | 5KB | Delete (replaced by SESSIONS.md) |
| `.claudignore.rtf` | 1KB | Delete (RTF format, stale) |
| `audit-screenshots/` | 0 | Delete (empty) |
| `Prompts/` | 912KB | Delete (38 old prompt files, git has them) |
| `Inbound_Emails/` | 872KB | Delete (old email templates) |
| `monday agencies/` | tiny | Delete (one-off) |
| `Content_Writer/` | tiny | Delete (old) |
| `ideas/` | 20KB | Merge into `research/`, then delete |
| `analytics/` | 36KB | Merge into `strategy/`, then delete |
| `Inspiration/` | tiny | Merge into `design-inspiration/`, then delete |
| `Dentists/venv/` | **~500MB+** | **DELETE (python virtualenv, massive)** — v1 MISSED THIS |
| `Dentists/image to be used/` | small | Move to scalefox-lp images OR delete |
| `reviews/` | tiny | Delete (one stale file: gtm-playbook-critic.md) |
| `templates/websiteGallery/` | 0 | Delete (empty untracked dir) |
| `templates/vercel.json` | 0 | Delete (empty untracked file) |
| `scalefox3.0/user-flows/` | 0 | Delete (empty dir) |
| `scalefox3.0/progress-log.md` | small | Delete (old, replaced) |
| `scalefox3.0/README.md` | small | Delete (old) |
| `scalefox3.0/PLAN.md` | small | Delete (superseded by root PLAN.md) |

---

## Complete source mapping (nothing forgotten)

Every top-level item in the current repo, with destination:

| Current | Destination | Repo |
|---------|-------------|------|
| `.claude/` | stays | workspace |
| `.claudignore.rtf` | DELETE | — |
| `.env` | stays | workspace |
| `.gitignore` | stays | workspace |
| `analytics/` | merge → `strategy/` | workspace |
| `Assistant/` | → `product/assistant/` | workspace |
| `audit-screenshots/` | DELETE | — |
| `audit-*.jpeg`, `t21-*.jpeg`, `template-*.jpeg/png` | DELETE | — |
| `Auto Repair/` | → `auto-repair/` | leads |
| `Blog Content/` | → `marketing/content/` | workspace |
| `CLAUDE.md` | stays (update refs) | workspace |
| `CLAUDE 2.md`, `Claude 3.md`, `Claude 4.md` | DELETE | — |
| `clinic_portal/` | whole dir | clinic-portal |
| `competitors analysis/` | → `marketing/competitive/` | workspace |
| `configuration/` | → `marketing/meta-ads/` | workspace |
| `content/` | → `marketing/content/` | workspace |
| `Content_Writer/` | DELETE | — |
| `creative/` | → `marketing/content/` | workspace |
| `dashboard/` | check if stub → merge or delete | dashboard |
| `dashboard_admin/` | whole dir | dashboard |
| `Dentists/booking widget/` | → `product/booking-widget/` | workspace |
| `Dentists/copy/` | → `dentists-il/copy/` | leads |
| `Dentists/customer_journey/` | → `product/customer-journey/` | workspace |
| `Dentists/Dr_Andy_Audit/` | → `dentists-il/Dr_Andy_Audit/` | leads |
| `Dentists/image to be used/` | move to lp images OR DELETE | lp or — |
| `Dentists/israel-dental-research/` | → `dentists-il/israel-dental-research/` | leads |
| `Dentists/reports/output/` (60 sites) | → `sites/dentists-il/` | lp |
| `Dentists/reports/` (scripts, Old/) | → `dentists-il/reports/` | leads |
| `Dentists/Specific Research/` | → `dentists-il/Specific Research/` | leads |
| `Dentists/venv/` | DELETE | — |
| `Dentists/*.py, *.csv, *.md` | → `dentists-il/` | leads |
| `design-inspiration/` | stays | workspace |
| `feedback/` | stays | workspace |
| `feedback-api/` | → `feedback-api/` | lp |
| `ideas/` | merge → `research/` | workspace |
| `Inbound_Emails/` | DELETE | — |
| `Inspiration/` | merge → `design-inspiration/` | workspace |
| `Landscaping/` | → `landscaping/` | leads |
| `lessonslearned.md` | stays | workspace |
| `Linkedin Strategy/` | → `marketing/linkedin/` | workspace |
| `lovable-prompting.md` | DELETE | — |
| `Med Spas/` | → `med-spas/` | leads |
| `Meta Ad Strategy/` | → `marketing/meta-ads/` | workspace |
| `monday agencies/` | DELETE | — |
| `Nova Dental UI UX Design.mp4` | Google Drive → DELETE | — |
| `PLAN.md` | stays (update) | workspace |
| `product-info.md` | → `product/product-info.md` | workspace |
| `products/instagram-dental/` | → `product/instagram-dental/` | workspace |
| `progress-log.md` | DELETE | — |
| `PROJECTS.md` | stays | workspace |
| `Prompts/` | DELETE | — |
| `research/` | stays (all of it) | workspace |
| `reviews/` | DELETE | — |
| `scalefox-ad-brief.md` | → `marketing/meta-ads/` | workspace |
| `Scalefox Inner Frameworks/` | → `product/frameworks/` | workspace |
| `Scalefox Marketing/` | → `marketing/campaigns/` | workspace |
| `Scalefox_Product/` | → `product/app-screens/` | workspace |
| `scalefox3.0/company-info.md` | → `product/company-info.md` | workspace |
| `scalefox3.0/gtm-playbook-example.md` | → `marketing/campaigns/` | workspace |
| `scalefox3.0/linkedin-1month-3k-plan.md` | dedup with strategy/ → `marketing/linkedin/` | workspace |
| `scalefox3.0/lovable-prompt-gtm-playbook.md` | → `marketing/campaigns/` | workspace |
| `scalefox3.0/performance-audit.md` | → `product/` | workspace |
| `scalefox3.0/product-agents/` | → `product/agents/` | workspace |
| `scalefox3.0/product-specs/` | → `product/specs/` | workspace |
| `scalefox3.0/research/` | → `marketing/linkedin/` (1 file) | workspace |
| `scalefox3.0/user-flows/` | DELETE (empty) | — |
| `scalefox3.0/PLAN.md`, `progress-log.md`, `README.md` | DELETE | — |
| `scripts/scan_smb.py` | → `scripts/` | leads |
| `servers/` | stays | workspace |
| `SESSIONS.md` | stays | workspace |
| `strategy/` | stays | workspace |
| `templates/gallery.html` | → `gallery.html` | lp |
| `templates/PLACEHOLDER_CONTRACT.md` | stays | workspace |
| `templates/INDEX.md` | stays | workspace |
| `templates/section-taxonomy.md` | stays | workspace |
| `templates/{vertical}/` | → `templates/{vertical}/` | lp |
| `templates/proposals/` | → `proposals/` | lp |
| `templates/websiteGallery/` | DELETE (empty) | — |
| `templates/vercel.json` | DELETE (empty) | — |
| `tmp-video-frames/` | DELETE | — |
| `tools/` | → `tools/` | lp |
| `US Dentists/1 Reports/output/` (27 sites) | → `sites/dentists-us/` | lp |
| `US Dentists/` (rest) | → `dentists-us/` | leads |
| `web-example2.mp4` | Google Drive → DELETE | — |

---

## Execution Order

| Step | Action | Status |
|------|--------|--------|
| 0 | Commit & push current repo (snapshot) | DONE |
| 1 | Create `scalefox-ai` repo | DONE |
| 2 | Delete junk first (venv, screenshots, videos, old CLAUDEs, empty dirs) | TODO — do this FIRST to shrink repo |
| 3 | Create `scalefox-lp` repo on GitHub | TODO |
| 4 | Move templates + sites + tools + feedback-api → `scalefox-lp`, commit & push | TODO |
| 5 | Create `scalefox-leads` repo on GitHub | TODO |
| 6 | Move Dentists + US Dentists + Auto Repair + Landscaping + Med Spas data → `scalefox-leads` | TODO |
| 7 | Merge scattered folders → `product/`, `marketing/` in workspace | TODO |
| 8 | Split Next.js apps to own repos (clinic_portal, dashboard_admin) | TODO |
| 9 | Update all references: CLAUDE.md, PLAN.md, skills, memory, server docs | TODO |
| 10 | Final commit of cleaned workspace | TODO |

---

## Risk: Skill path breakage

**Critical.** These skills read files by path. After split, verify each:

| Skill | References | After split |
|-------|-----------|-------------|
| `template-creator` | `templates/`, `design-inspiration/`, `research/{vertical}.md` | OK — all stay in workspace |
| `create-website-from-template` | `templates/PLACEHOLDER_CONTRACT.md` | OK — stays in workspace |
| `vertical-research` | `research/` | OK — stays |
| `web-design-research` | `design-inspiration/` | OK — stays |
| `website-from-template-audit` | output paths | OK — paths are passed as args |
| `section-scanner.js` | `templates/` dir | **BREAKS — moves to scalefox-lp** |
| CLAUDE.md pipeline table | `servers/lp-scalefox-ai.md` | OK — stays |
| Memory `server_scalefox.md` | deploy commands | **UPDATE — paths change** |

**Key insight:** Skills that create/reference templates will need the `scalefox-lp` repo checked out locally. Add to CLAUDE.md a "sibling repos" section with expected local paths.
