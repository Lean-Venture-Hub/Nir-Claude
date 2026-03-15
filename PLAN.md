# Master Plan

**Updated:** 2026-03-15 (session 6) | **Cross-session state:** see `SESSIONS.md`

---

## Current Template Count

| Vertical | Templates | Images | Research | Gallery | Deployed |
|----------|-----------|--------|----------|---------|----------|
| Dentists | 25 | yes | yes | yes | yes |
| Auto Repair | 26 | 30 | yes | yes | yes |
| Landscaping | 13 | yes | yes | yes | yes |
| Veterinarians | 10 | 10 | yes | yes | yes |
| Med Spas | 10 | 10 | yes | yes | yes |
| HVAC | 10 | 10 | yes | yes | yes |

**Gallery:** https://lp.scalefox.ai/gallerywebsite/gallery.html (6 vertical tabs + responsive dropdown)

---

## Completed Phases

### Phase 1: Multi-Vertical Pipeline (DONE)
- Generalized all skills for any vertical (not just dentists)
- Placeholder contract (`templates/PLACEHOLDER_CONTRACT.md`)
- Template manifests, audit skill, vertical naming convention

### Phase 2: Reference Consolidation (DONE)
- Merged 4 overlapping design files → single `web-design-playbook.md`
- Updated skills to point to consolidated playbook

### Phase 3: 6 Verticals Live (DONE — 2026-03-14)
- Full pipeline for all 6 verticals: research → images → templates → gallery → deploy
- 94 total templates across 6 verticals
- Gallery with likes, comments, feedback export, responsive dropdown
- Template feedback system: gallery hearts/comments + sections builder export → feeds template-creator skill

### Phase 3.5: Feedback Auto-Sync (DONE — 2026-03-15)
- Flask API on EC2 (`/api/feedback`) — multi-user feedback with file locking + audit log
- Gallery + Section Builder auto-sync to server (no manual export)
- User identification (name modal), aggregate like counts, commenter attribution
- `template-creator` skill rsyncs feedback from server before reading
- localStorage offline fallback

---

## Active / Next Up

### Phase 4: Vertical Expansion (IN PROGRESS)
Evaluate new verticals and expand into the best ones.

| # | Task | Status |
|---|------|--------|
| 4.1 | Define segment criteria (1-5, 4a/4b) | DONE |
| 4.2 | Score 11 candidate verticals on 8 criteria | DONE — `strategy/new-verticals-analysis.md` |
| 4.3 | Consumer discovery research (how people find/book in each vertical) | DONE — Plumbers/Electricians/Roofers/Cleaning/Chiropractors |
| 4.4 | Recalculate scores with real data | DONE — Chiropractors dropped (90% have sites), Roofers moved up |
| 4.5 | Build `vertical-scout` skill for quick checks | TODO |
| 4.6 | Run `vertical-research` for Plumbers + Electricians | TODO — **next action** |
| 4.7 | Build 8-10 templates per new vertical | TODO |
| 4.8 | Generate 20 demo sites from Google Maps leads | TODO |
| 4.9 | Test outreach, measure reply rate | TODO |

**Launch order:** Plumbers+Electricians → Roofers → Cleaning → Pest Control

### Phase 5: Sales Agent System (IN PLANNING)
Autonomous AI sales agent: receives ready leads from CRM → multi-channel outreach → conversation → close.
**Detailed plan:** [`sales-agent/PLAN.md`](sales-agent/PLAN.md) | **Research:** `research/ai-sales-agent-stack-deep-brief.md`

| # | Task | Status |
|---|------|--------|
| 5.1 | Architecture + tool research | DONE — `sales-agent/PLAN.md` |
| 5.2 | Email outreach MVP (Instantly.ai + CSV import + flow engine) | TODO — **next action** |
| 5.3 | Conversation agent (Claude + LangGraph + tool use) | TODO |
| 5.4 | Multi-channel (Twilio SMS/WhatsApp + Retell.ai phone) | TODO |
| 5.5 | Closing engine (Stripe + onboarding triggers) | TODO |
| 5.6 | Production hardening + dashboard | TODO |

### Phase 5.5: Mini CRM (IN PROGRESS)
Single-file CRM at `lp.scalefox.ai/crm/` — tracks outreach to 117 leads across dentists + auto-repair.
**Source:** `Auto Repair/reports/crm-index.html` | **PRD:** `Auto Repair/reports/crm-prd.md`

| # | Task | Status |
|---|------|--------|
| 5.5.1 | Directory page duplicate + CRM PRD | DONE |
| 5.5.2 | Full CRM rebuild: sidebar nav, dashboard, kanban, contacts, lead modal | DONE |
| 5.5.3 | Design: dark charcoal theme, purple/blue accents, 2-col cards, list default | DONE |
| 5.5.4 | Deploy to lp.scalefox.ai/crm/ | DONE |
| 5.5.5 | Kanban drag-and-drop, bulk actions | TODO |
| 5.5.6 | Email template compose (P2 from PRD) | TODO |

### Phase 6: Polish & Scale (BACKLOG)

| # | Task | Status |
|---|------|--------|
| 6.1 | Gallery auto-discovery from folder structure (no hardcoded JS) | TODO |
| 6.2 | Screenshot capture in vertical-research (top 5 sites) | TODO |
| 6.3 | E2E test: create website for real business from CSV | TODO |
| 6.4 | Builder tools (Section Reviewer + Editor) updates for new verticals | DONE — 766 sections from 6 verticals, CSS @scope isolation |

---

## Key References

| Resource | Path |
|----------|------|
| Gallery (live) | https://lp.scalefox.ai/gallerywebsite/gallery.html |
| Gallery (local) | http://localhost:8080/templates/gallery.html |
| Server reference | `servers/lp-scalefox-ai.md` |
| Design playbook | `design-inspiration/web-design-playbook.md` |
| Placeholder contract | `templates/PLACEHOLDER_CONTRACT.md` |
| Lead segments | `memory/reference_lead_segments.md` |
| Session tracking | `SESSIONS.md` |
