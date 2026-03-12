# Self-Improvement Recommendations for Claude Code Setup

**TL;DR:** You have 28 agents but only 1 skill. The biggest wins are: (1) converting your repeatable workflows into skills (report generation, Apify scraping, EC2 deploy), (2) installing community skills from the Anthropic skills repo and SkillsMP marketplace, (3) adding project-specific CLAUDE.md files in subfolders, and (4) using the built-in `/batch` and `/simplify` slash commands you may not be using yet. Your orchestrator is solid but your CLAUDE.md is too generic -- it needs dental-SaaS-specific context.

---

## Current Friction Points

| Problem | Impact | Root Cause |
|---------|--------|------------|
| Only 1 skill (reviews collector) despite 5+ repeatable workflows | You re-explain the same tasks every session | No skills for report gen, template creation, deployment, outreach |
| CLAUDE.md has zero domain context | Claude doesn't know your stack, business model, or client pipeline | Generic instructions only cover style/format |
| No subfolder CLAUDE.md files | Dashboard Admin and Clinic Portal lack project-specific conventions | Best practice is per-project CLAUDE.md |
| Agents are content/marketing focused | Missing: deployer, scraper-ops, template-builder agents | 28 agents but none for your technical workflows |
| Context window fills fast on large tasks | Orchestrator spawns agents that re-read everything | No use of Task tool for parallel sub-agents with scoped context |

## New Tools & Features Available (March 2026)

### Already in Claude Code (may not be using)
- **`/batch`** -- orchestrates large-scale codebase changes in parallel (useful for updating all report templates at once)
- **`/simplify`** -- spawns 3 review agents to check code reuse, quality, efficiency on recent changes
- **`/rewind`** -- now supports code-only or conversation-only rollback
- **Task tool** -- spawn sub-agents with isolated context windows for parallel work (your orchestrator should use this)

### Skill Ecosystem
- **Anthropic official skills repo:** `github.com/anthropics/skills` -- includes `skill-creator` skill that generates new skills from a description
- **SkillsMP.com** -- 400K+ skills, searchable by category. Look for: deployment, Apify, report-generation, SEO audit
- **awesome-claude-skills** (`github.com/travisvn/awesome-claude-skills`) -- curated list of high-quality skills
- **VoltAgent subagents** (`github.com/VoltAgent/awesome-claude-code-subagents`) -- 100+ specialized subagent templates

### Orchestration Frameworks
- **Claude Flow** -- multi-agent coordination with shared memory (overkill for now, but worth watching)
- Skills now auto-trigger based on context (no slash command needed) -- your reviews-collector skill already works this way

## Actionable Recommendations (Priority Order)

### P0: Create 4 Missing Skills (1-2 hours)

Use the `skill-creator` skill from Anthropic's repo to generate these:

1. **`report-generator`** -- Generate S4-style client reports (HTML + images) from clinic data. You already have ~50 report templates to reference.
2. **`ec2-deployer`** -- SSH into EC2, pull latest, restart services. Codify your deploy steps.
3. **`apify-scraper-safe`** -- Wraps Apify calls with: cost estimation, batch-by-batch execution, local save after each batch. Enforces your `lessonslearned.md` rule automatically.
4. **`proposal-builder`** -- Generate client proposals from your existing templates in `Dentists/reports/proposals/templates_new/`.

### P1: Enrich CLAUDE.md with Domain Context (30 min)

Add to your root CLAUDE.md:
- Stack: Next.js dashboard (port 3000), React clinic portal (3001), EC2 deployment, Apify for scraping
- Business model: dental/med spa marketing SaaS, ~50 clinic clients, Hebrew + English
- Key data paths: `Dentists/reports/`, `Dentists/s4-templates/`, `dashboard_admin/`, `clinic_portal/`
- Common tasks: generate reports, scrape reviews, build templates, deploy to EC2, create outreach content

### P2: Add Per-Project CLAUDE.md Files (20 min)

Create `CLAUDE.md` in:
- `dashboard_admin/CLAUDE.md` -- component patterns, API routes, state management conventions
- `clinic_portal/CLAUDE.md` -- auth flow, clinic data schema, i18n setup
- `Dentists/CLAUDE.md` -- report structure, template conventions, naming rules

### P3: Install Community Skills (15 min)

Browse and install from `github.com/anthropics/skills`:
- `skill-creator` -- meta-skill to build new skills faster
- Any SEO audit or content generation skills relevant to dental marketing

### P4: Update Orchestrator to Use Task Tool (30 min)

Your orchestrator delegates to agents but doesn't use the Task tool for parallel execution with isolated context. Update `orchestrator.md` to explicitly use `TaskCreate` for spawning parallel work, which prevents context window bloat.

### P5: Add a `deployer` Agent (15 min)

Create `.claude/agents/deployer.md` -- handles EC2 SSH, git pull, service restart, health checks. Currently no agent covers infrastructure.

---

## Quick Reference Links

- Anthropic skills repo: `github.com/anthropics/skills`
- Skill authoring best practices: `platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices`
- Skills marketplace: `skillsmp.com`
- Awesome claude skills: `github.com/travisvn/awesome-claude-skills`
- Claude Code best practices: `code.claude.com/docs/en/best-practices`
