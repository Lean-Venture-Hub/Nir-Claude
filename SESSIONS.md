# Active Sessions

> Each Claude Code session updates this file on start (read) and at milestones (write).
> When a session ends or context compacts, it logs its final state here so another session can continue.

---

## Current Sessions

| ID | Started | Focus | Status | Last Action | Next Step |
|----|---------|-------|--------|-------------|-----------|
| 7 | 2026-03-15 | CRM rebuild | Done | Full CRM rebuild: sidebar nav, kanban board, lead modal, list/card views, purple/blue theme, deployed to lp.scalefox.ai/crm/ | Polish CRM: drag-and-drop kanban cards, bulk actions, email template compose |

### 2026-03-15 (session 6 — sales agent planning)
- Designed full autonomous sales agent system (outreach → conversation → closing)
- Researched tool stack: Instantly.ai (cold email), Retell.ai (voice), Twilio (SMS/WhatsApp), Claude API (brain)
- Created `sales-agent/PLAN.md` with architecture, 4-phase build plan, cost estimates (~$260-440/mo)
- Key decisions locked: email-first flows, named persona, English only, CSV input, configurable flow engine
- Scope boundary: agent does NOT own lead pipeline/proposals/websites — reads from CRM
- Research saved to `research/ai-sales-agent-stack-deep-brief.md`
- Updated master PLAN.md Phase 5 to reflect sales agent scope
- Saved scope boundary to memory (`project_sales_agent_scope.md`)

---

## Recently Completed Work (not yet in PLAN.md)

### 2026-03-15 (session 5 — repo split planning)
- Audited v1 folder-reorganization plan against actual repo structure
- Found 15+ missing items (Scalefox_Product/, feedback-api/, Dentists/venv, *.md files, etc.)
- Fixed 3 design issues (images stay with templates, vertical research stays in workspace, skill ref docs stay)
- Wrote v2 plan with complete source mapping table (every item → destination)
- Added skill path breakage risk analysis

### 2026-03-15 (session 4 — feedback auto-sync)
- Built Flask feedback API (`feedback-api/app.py`) — multi-user likes/comments/ratings/bugs with file locking
- Deployed API to EC2 with systemd service + nginx reverse proxy at `/api/`
- Updated gallery.html: user identification modal, auto-sync to API, aggregate like counts, commenter names, sync indicator
- Updated section builder: same user badge + auto-sync pattern for ratings/bugs
- Migrated existing Nir feedback (7 likes, 15 comments) to multi-user format on server
- Updated `template-creator` skill to rsync feedback from server before reading
- Updated `servers/lp-scalefox-ai.md` with Feedback API docs
- Updated `feedback/README.md` with auto-sync workflow

### 2026-03-15 (session 3)
- Built CSS `@scope` isolation for cross-template section swaps in Template Editor
- Absolutified HTML/CSS URLs per section basePath for cross-template image resolution
- Rewrote editor toolbar: moved from parent overlay to in-iframe postMessage system
- Updated section scanner for 6 verticals (766 sections, 18.8MB data)
- Deployed gallery + builder tools + proposal templates to lp.scalefox.ai
- Fixed proposal gallery 404 at `/gallerywebsite/proposals/` (was only at `/galleryproposal/`)
- Created `/templates` → `gallerywebsite` symlink on server for basePath resolution

### 2026-03-15 (session 2)
- Fixed 15 auto-repair templates from gallery feedback (opacity:0, placeholders, layout)
- Generated 12 missing auto-repair images, deployed all to server
- Updated template-creator + audit skills with 7 new rules

### 2026-03-15 (session 1)
- Created `end-session` skill, committed + pushed all prior work (234 files)
- Full audit: CLAUDE.md refs valid, PLAN.md counts match

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
