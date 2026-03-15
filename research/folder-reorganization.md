# Folder Reorganization Proposal

**TL;DR:** The current root has 50+ items mixing 4 distinct concerns: (1) deployable web assets, (2) lead data & scripts, (3) Scalefox product/strategy docs, and (4) Claude Code workspace config. Split into 3 repos + clean up the main workspace.

---

## Current State: What's Here

| Category | Folders | Size | Notes |
|----------|---------|------|-------|
| **Website templates** | `templates/` (6 verticals + proposals + gallery) | 319MB | Deployed to lp.scalefox.ai |
| **Generated websites** | `Dentists/reports/output/` (60 sites), `US Dentists/1 Reports/output/` (27 sites) | ~3.9GB | Built from templates, deployed to lp.scalefox.ai |
| **Lead data & scripts** | `Dentists/*.py`, `Dentists/*.csv`, `Auto Repair/*.py/*.csv`, `Landscaping/*.csv`, `Med Spas/*/`, `US Dentists/*/` | ~1.2GB | CSVs, Python scripts, city folders |
| **Design system** | `design-inspiration/` | 11MB | Playbook, screenshots, sites.csv |
| **Research** | `research/` (25 files) | 404KB | Vertical research, self-improvement |
| **Scalefox product** | `scalefox3.0/`, `Scalefox_Product/`, `Scalefox Inner Frameworks/`, `Scalefox Marketing/`, `Assistant/` | ~1.5MB | Product specs, marketing, agent architecture |
| **Apps (Next.js)** | `clinic_portal/`, `dashboard_admin/`, `dashboard/` | 1.5GB | Running apps with node_modules |
| **Strategy/marketing** | `strategy/`, `Linkedin Strategy/`, `Meta Ad Strategy/`, `content/`, `creative/`, `Blog Content/` | ~1MB | Old plans, playbooks |
| **Loose files** | 8 jpegs, 2 mp4s, old CLAUDE versions, lovable-prompting.md | ~40MB | Junk in root |
| **Config** | `.claude/`, `servers/`, CLAUDE.md, PLAN.md, SESSIONS.md | ~200KB | Workspace orchestration |

---

## Proposed Structure: 3 Repos

### Repo 1: `scalefox-templates` (NEW — what goes on lp.scalefox.ai)
Everything that gets deployed to lp.scalefox.ai. This is a **deployable artifact repo**.

```
scalefox-templates/
├── gallery.html                    ← main gallery page
├── PLACEHOLDER_CONTRACT.md
├── INDEX.md
├── section-taxonomy.md
├── proposals/                      ← proposal templates + gallery
├── dentists/
│   ├── images/
│   └── website/
│       ├── template-1/
│       └── ...template-25/
├── auto-repair/
├── landscaping/
├── veterinarians/
├── med-spas/
├── hvac/
└── sites/                          ← generated per-business websites
    ├── dentists-il/                ← from Dentists/reports/output/
    │   ├── 1-mrpat-shynyym-dr-pvks/
    │   └── ...60 folders
    └── dentists-us/                ← from US Dentists/1 Reports/output/
        ├── abraham-esses-dds/
        └── ...27 folders
```

**Why separate repo:**
- These are pure static HTML — no scripts, no data, no secrets
- Deployable independently (rsync to server)
- 4GB+ and growing — would bloat the main workspace
- Can set up CI/CD: push → auto-deploy to lp.scalefox.ai
- Different collaborators might access this vs the data/strategy repo

---

### Repo 2: `scalefox-leads` (NEW — data, scripts, outreach)
All lead generation data, scraping scripts, enrichment, and outreach materials.

```
scalefox-leads/
├── .env                            ← API keys for Apify, etc.
├── scripts/                        ← shared utilities
│   ├── scrape_gmaps.py
│   ├── enrich_reviews.py
│   └── scan_smb.py
├── dentists-il/                    ← Israeli dentists
│   ├── gush-dan-clinics.csv
│   ├── labeled-dentals.csv
│   ├── outreach-leads.csv
│   ├── reviews.csv
│   ├── enrich_dental_clinics.py
│   ├── scrape_dental_clinics.py
│   └── reports/                    ← audit reports, analysis (NOT website output)
│       ├── audit_reports.py
│       └── first_batch_tlv.csv
├── dentists-us/                    ← US dentists
│   ├── Atlanta/
│   ├── Houston/
│   ├── ...12 city folders
│   ├── combined-analysis/
│   └── segment1-outreach-strategy.md
├── auto-repair/                    ← Auto repair leads
│   ├── houston-tx.csv
│   ├── phoenix-az.csv
│   ├── s4-leads-enriched.csv
│   ├── enrich_reviews.py
│   └── outreach-strategy.md
├── landscaping/
│   ├── atlanta-ga.csv
│   └── dallas-tx.csv
├── med-spas/
│   ├── Atlanta/
│   ├── Houston/
│   └── ...6 city folders
└── research/                       ← vertical market research
    ├── dentists-il/
    ├── auto-repair.md
    ├── landscaping.md
    └── next-vertical-analysis.md
```

**Why separate repo:**
- Contains sensitive data (leads, emails, phone numbers)
- Heavy CSVs that bloat git
- Python scripts with their own dependencies (venv)
- Different access control needs
- Can use `.gitignore` for large CSVs, keep only scripts in git
- Consider git-lfs for large data files

---

### Repo 3: `scalefox-workspace` (CLEANED — this repo, slimmed down)
The command center: orchestration, strategy, product docs, design system, running apps.

```
scalefox-workspace/                 ← current "Claude code" repo, cleaned
├── .claude/                        ← skills, agents, hooks, settings
├── .env
├── CLAUDE.md
├── PLAN.md
├── SESSIONS.md
├── PROJECTS.md
├── lessonslearned.md
│
├── servers/                        ← server connection docs
│   ├── scalefox-ai.md
│   └── lp-scalefox-ai.md
│
├── design-inspiration/             ← stays here (used by skills)
│   ├── web-design-playbook.md
│   ├── sites.csv
│   ├── inspiration-sources.md
│   └── screenshots/
│
├── research/                       ← non-vertical research only
│   ├── self-improvement-recommendations.md
│   ├── claude-code-setup-best-practices.md
│   ├── geo-aio-llm-optimization-brief.md
│   └── ... (API guides, tool research)
│
├── product/                        ← merged from scalefox3.0 + Scalefox_Product + Assistant
│   ├── specs/                      ← from scalefox3.0/product-specs/
│   ├── agents/                     ← from scalefox3.0/product-agents/
│   ├── assistant/                  ← from Assistant/
│   ├── company-info.md
│   └── product-info.md
│
├── marketing/                      ← merged from multiple folders
│   ├── linkedin/                   ← from Linkedin Strategy/
│   ├── meta-ads/                   ← from Meta Ad Strategy/
│   ├── content/                    ← from content/ + Blog Content/ + creative/
│   └── campaigns/                  ← from Scalefox Marketing/
│
├── strategy/                       ← stays (dental outreach, verticals analysis)
│
├── apps/                           ← or keep as separate repos
│   ├── clinic-portal/              ← from clinic_portal/
│   └── dashboard-admin/            ← from dashboard_admin/
│
├── tools/                          ← stays
│   ├── builder/
│   └── section-scanner.js
│
└── memory/                         ← auto-memory (already exists)
```

---

## What Gets Deleted (junk in root)

| File | Action |
|------|--------|
| `audit-gallery.jpeg`, `audit-template-*.jpeg`, `t21-*.jpeg`, `template-21-*.jpeg` | Delete — temp audit screenshots |
| `Nova Dental UI UX Design.mp4`, `web-example2.mp4` | Delete or move to Google Drive — 35MB of video |
| `tmp-video-frames/` | Delete — temporary |
| `CLAUDE 2.md`, `Claude 3.md`, `Claude 4.md` | Delete — old CLAUDE.md versions (git has history) |
| `lovable-prompting.md` | Delete — 43KB, old reference |
| `scalefox-ad-brief.md` | Move to `marketing/meta-ads/` |
| `progress-log.md` | Delete — replaced by SESSIONS.md |
| `.claudignore.rtf` | Convert to `.claudeignore` (plain text) or delete |
| `configuration/` | Move to `marketing/meta-ads/` (Ad Score, Meta library) |
| `competitors analysis/` | Move to `marketing/competitive/` |
| `Inspiration/` | Merge into `design-inspiration/` |
| `Prompts/` | Delete or archive — 38 old prompt files |
| `Inbound_Emails/` | Archive — old email templates |
| `monday agencies/` | Archive — one-off research |
| `reviews/` | Move to leads repo |
| `products/instagram-dental/` | Move to `product/` |
| `feedback/` | Just a README — delete |
| `ideas/` | Move to `research/` |
| `analytics/` | Move to `product/` or `strategy/` |
| `audit-screenshots/` | Delete — empty |
| `Dentists/booking widget/` | Move to `product/` |
| `Dentists/customer_journey/` | Move to `product/` |
| `Dentists/Dr_Andy_Audit/` | Move to leads repo |
| `Dentists/image to be used/` | Move to templates repo |
| `Dentists/copy/` | Move to `marketing/content/` |

---

## Apps: Separate Repos vs Subfolder?

`clinic_portal/` (894MB) and `dashboard_admin/` (676MB) are full Next.js apps with `node_modules`. Options:

| Option | Pro | Con |
|--------|-----|-----|
| **Separate repos** (recommended) | Clean git history, independent deploys, no node_modules in workspace | More repos to manage |
| **Subfolder + gitignore** | Everything in one place | 1.5GB of noise, git performance |
| **Git submodules** | Reference without bloat | Submodules are painful |

**Recommendation:** Separate repos (`scalefox-clinic-portal`, `scalefox-dashboard`). They're independent apps with independent deploy cycles.

---

## Migration Order

1. **Quick wins first:** Delete junk files from root (jpegs, mp4s, old CLAUDE versions, tmp-video-frames)
2. **Create `scalefox-templates` repo:** Move `templates/` + generated site outputs
3. **Create `scalefox-leads` repo:** Move all CSVs, Python scripts, city folders
4. **Reorganize remaining workspace:** Merge scattered folders into `product/`, `marketing/`
5. **Consider splitting apps:** Move `clinic_portal/` and `dashboard_admin/` to own repos
6. **Update all references:** CLAUDE.md, PLAN.md, skills, server docs

---

## Summary

| Repo | Purpose | Size (est.) |
|------|---------|-------------|
| `scalefox-templates` | Deployable web assets → lp.scalefox.ai | ~4GB |
| `scalefox-leads` | Lead data, scripts, outreach | ~1.5GB |
| `scalefox-workspace` | Command center, config, strategy, design, research | ~15MB (without apps) |
| `scalefox-clinic-portal` | Clinic portal Next.js app | ~900MB |
| `scalefox-dashboard` | Admin dashboard Next.js app | ~700MB |
