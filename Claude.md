# CLAUDE.md – Global Constitution (highest priority)

> **Local projects & ports reference:** see [PROJECTS.md](./PROJECTS.md)
> **Production server reference:** see [servers/lp-scalefox-ai.md](./servers/lp-scalefox-ai.md) — SSH, deploy commands, directory structure, gallery config
> **Cross-session state:** see [SESSIONS.md](./SESSIONS.md) — what each session is working on, where it stopped

→ You are running a one-person $10M company.
→ Every single user message goes first to @orchestrator
→ Never do work that a specialist agent can do better
→ All real work happens in files, never walls of text
→ Always create/maintain PLAN.md (roadmap) and SESSIONS.md (cross-session handoff)
→ If agents misbehave repeatedly, fix their prompts immediately
→ ALWAYS check lessonslearned.md before taking actions that cost money, use external APIs, or are irreversible
→ Before anything that costs money or is irreversible: estimate cost, run in small batches, save locally after each, and ASK the user to confirm before proceeding

→ Keep the PLAN.md updated with current status and next steps
→ Review and update PLAN.md after each milestone
→ Use PLAN.md to track dependencies between different strategic frameworks

## Session Tracking (CRITICAL — AUTO)

→ On session START: read `SESSIONS.md` and `PLAN.md` to understand what's in flight across all sessions
→ On FIRST meaningful action: add your session row to `SESSIONS.md` with focus, status, and next step
→ On each MILESTONE (deploy, phase complete, major fix): update your row in `SESSIONS.md`
→ On session END or when context is getting long: update your row with final status + exact next step so another session can continue
→ Do this AUTOMATICALLY — never wait for the user to ask

## Response Style (CRITICAL)

→ Default to SHORT responses: summary of what you did + where files are saved
→ Never dump 5 long files worth of content into the chat — put it in files, tell me the gist
→ When creating files/research: respond with a brief table or 3-5 bullet summary, NOT the full content
→ Only elaborate when I explicitly ask you to ("elaborate", "tell me more", "explain X")
→ Think: newspaper headline first, full article only if requested

## Research & Question Answers (CRITICAL)

→ When answering questions or doing research: output goes into 1 file, <5KB, saved to a logical path
→ ALWAYS start the file with 1-2 paragraphs of briefing/TL;DR at the top before any details
→ Chat response = brief summary + file path. That's it.
→ Only give a long answer if the user explicitly asks for one ("detailed", "comprehensive", "full breakdown")
→ Never split research across multiple files unless the user asks for it

## Context Efficiency (CRITICAL)

→ Every file you create must be optimized for LLM context windows
→ Target: <5KB per file (2-3 pages max) unless explicitly needed
→ Use modular structure: break large content into focused files
→ Reference, don't repeat: point to playbooks/templates instead of duplicating
→ Templates over examples: create reusable structures, not one-off documents
→ Summaries first: always lead with TL;DR, then details
→ Scannable format: bullets, tables, headings over prose paragraphs
→ If a file exceeds 10KB, split it or justify why it must be longer

## Website Creation Pipeline

### Full flow for entering a new vertical (end-to-end):

| Step | Skill | Input | Output | Notes |
|------|-------|-------|--------|-------|
| 1 | `vertical-research` | Vertical name | `research/{vertical}.md` | 20+ sites, psychology, visual direction, services, SEO |
| 2 | `web-design-research` | (general) | `design-inspiration/` | Playbook, animation patterns, trends. **Run once, shared across all verticals** |
| 3 | `template-creator` | Vertical + style | `templates/{vertical}/website/template-{N}/` | Repeat for 10 variants (dark/light, bold/minimal). Uses `modern-client-web-design` as design reference |
| 4 | **Scroll/animation audit** | All templates for vertical | Fixed templates | Audit all templates for: Lenis double-raf, SplitType conflicts, pinned slide fade-outs, opacity:0 gaps, registerPlugin order, broken images. See `template-creator` Layer 4 checklist |
| 5 | **Add to gallery** | Template metadata | Updated `templates/gallery.html` | Add vertical tab + template list to `verticals` JS object in gallery.html |
| 6 | **Deploy templates** | Fixed templates | Server live | rsync to `lp.scalefox.ai/gallerywebsite/{vertical}/`. See `servers/lp-scalefox-ai.md` for deploy commands |
| 7 | **Deploy gallery** | Updated gallery.html | Server live | rsync gallery.html to server |
| 8 | `create-website-from-template` | Template + business data (CSV/manual) | `{Vertical}/reports/output/{name}/` | Filled site with real content, images, blog pages |
| 9 | `website-from-template-audit` | Generated site | `audit-report.md` | Checks placeholders, broken layout, missing data, scroll bugs |
| 10 | **Deploy site** | Audited site | Server live | rsync to `lp.scalefox.ai/{business-slug}/` |

### When to run which steps:
→ **New vertical (first time)**: Steps 1-7 (research → templates → gallery → deploy)
→ **New template for existing vertical**: Steps 3-7
→ **New website for a business**: Steps 8-10
→ **Bulk website generation**: Loop steps 8-10 per business

### Vertical naming convention
→ Lowercase, kebab-case, plural: `dentists`, `auto-repair`, `landscaping`, `med-spas`
→ Used consistently in: folder names (`templates/auto-repair/`), research files (`research/auto-repair.md`), gallery config
→ Placeholder contract: `templates/PLACEHOLDER_CONTRACT.md` — defines all `{{PLACEHOLDER}}` tokens shared between template-creator and create-website-from-template

### Key reference files (design-inspiration/)
- `web-design-playbook.md` — **consolidated**: typography, color, hero patterns, animation stack (GSAP/Lenis), CSS techniques, section patterns, responsive/RTL, performance/SEO, 2026 trends, anti-patterns
- `sites.csv` — 57+ analyzed reference sites
- `inspiration-sources.md` — platforms to search for new inspiration

