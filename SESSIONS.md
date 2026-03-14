# Active Sessions

> Each Claude Code session updates this file on start (read) and at milestones (write).
> When a session ends or context compacts, it logs its final state here so another session can continue.

---

## Current Sessions

| ID | Started | Focus | Status | Last Action | Next Step |
|----|---------|-------|--------|-------------|-----------|
| — | — | Vertical Scout skill | Planning | Defined segment criteria (1-5, 4a/4b), estimated costs ($3-7/vertical) | Build the skill |

---

## Recently Completed Work (not yet in PLAN.md)

### 2026-03-14 (Session 2)
- **10 new auto repair templates (17-26)** — all with demo content + blog pages + 3 blog posts each
  - Styles: Midnight Garage, Warm Workshop, Neon Mechanic, Editorial Garage, Patriot Blue, Copper Industrial, Clean Minimalist, Vintage Garage, Speed Racing, Luxury Auto
  - 10 new auto repair images via Gemini (18 total in library)
  - Gallery updated with 26 auto repair templates + 3 new filter tags (Industrial, Luxury, Vintage)
  - All audited and deployed to lp.scalefox.ai
- **Template bug fixes:**
  - T15: Removed `.gsap-fade{opacity:0}` — hero was invisible
  - T14: Added `word-break:keep-all` — headline words were breaking mid-word
  - T25: Moved subtitle out of `<h1>` — was rendering at headline size
- **Skill updates (template-creator):**
  - Step 4 rewritten: demo content required, `{{PLACEHOLDER}}` tokens BANNED
  - Standard demo businesses defined per vertical
  - Blog + 3 blog posts now REQUIRED for every template
  - New Layer 1 rules: hero `word-break:keep-all`, subtitle must be `<p>` not inside `<h1>`
  - New Layer 4 rules: NO CSS `opacity:0` on content, `.gsap-fade{opacity:0}` banned
  - Self-review now starts with `grep -c '{{'` blocking gate
- **Skill updates (website-from-template-audit):**
  - Now accepts template folders (not just generated sites)
  - New checks: CSS opacity:0 on content, subtitle in h1, hero word-break
  - Template-specific audit section added

### 2026-03-14 (Session 1)
- 3 new verticals (vet/med-spa/hvac): 30 templates, 30 images, deployed
- Template fixes across 30 templates (Lenis, opacity, sync)
- Gallery: likes, comments, export, responsive dropdown
- Landscaping: 13 templates

### 2026-03-13
- Dentists: 25 templates, Auto-repair: 16 templates, Landscaping: 13 templates

---

## How to Use This File

**On session start:**
1. Read `SESSIONS.md` to see what's in flight
2. Read `PLAN.md` for the overall roadmap
3. Check `memory/MEMORY.md` for persistent facts

**During session:**
- Update your row's "Last Action" at milestones

**On session end / context compaction:**
- Update "Status" and "Next Step" so another session can continue
- Move completed work to "Recently Completed" section
- Keep the table clean — remove rows older than 7 days
