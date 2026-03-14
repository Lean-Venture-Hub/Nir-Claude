# Master Plan

**Updated:** 2026-03-14 | **Cross-session state:** see `SESSIONS.md`

---

## Current Template Count

| Vertical | Templates | Images | Research | Gallery | Deployed |
|----------|-----------|--------|----------|---------|----------|
| Dentists | 25 | yes | yes | yes | yes |
| Auto Repair | 26 | 18 | yes | yes | yes |
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
- Gallery with likes, comments, export, responsive dropdown

---

## Active / Next Up

### Phase 4: Vertical Scout Skill (IN PROGRESS)
Build a skill to quickly evaluate new verticals before investing in templates.

| # | Task | Status |
|---|------|--------|
| 4.1 | Define segment criteria (1-5, 4a/4b) | DONE — saved to `memory/reference_lead_segments.md` |
| 4.2 | Estimate costs ($3-7 per quick check) | DONE |
| 4.3 | Build the `vertical-scout` skill | TODO |
| 4.4 | Test on 2-3 candidate verticals | TODO |

### Phase 5: Lead Pipeline (PLANNED)
End-to-end from vertical scout → scrape → classify → enrich emails → outreach.

| # | Task | Status |
|---|------|--------|
| 5.1 | Build email enrichment into vertical-scout | TODO |
| 5.2 | Create outreach templates per vertical | TODO |
| 5.3 | Test end-to-end on auto-repair (Houston data exists) | TODO |

### Phase 6: Polish & Scale (BACKLOG)

| # | Task | Status |
|---|------|--------|
| 6.1 | Gallery auto-discovery from folder structure (no hardcoded JS) | TODO |
| 6.2 | Screenshot capture in vertical-research (top 5 sites) | TODO |
| 6.3 | E2E test: create website for real business from CSV | TODO |
| 6.4 | Builder tools (Section Reviewer + Editor) updates for new verticals | TODO |

---

## Key References

| Resource | Path |
|----------|------|
| Gallery (live) | https://lp.scalefox.ai/gallerywebsite/gallery.html |
| Gallery (local) | http://localhost:8080/templates/gallery.html |
| Server reference | `lp-scalefox/server-reference.md` |
| Design playbook | `design-inspiration/web-design-playbook.md` |
| Placeholder contract | `templates/PLACEHOLDER_CONTRACT.md` |
| Lead segments | `memory/reference_lead_segments.md` |
| Session tracking | `SESSIONS.md` |
