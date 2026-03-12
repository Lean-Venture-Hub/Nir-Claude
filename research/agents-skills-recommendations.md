# Agents & Skills Audit + Recommendations

## TL;DR

You have 28 project agents, 3 global agents, 32 global skills, and 1 project skill. Most of the setup is bloated boilerplate that never fires in practice. Cut agents from 28 to ~10 focused ones, delete 25+ generic global skills you didn't write, and move domain-specific workflows (dentist reviews, report generation) into project-level skills where they belong.

---

## Current State

### Project Agents (28 in `.claude/agents/`)

| Category | Agents | Notes |
|----------|--------|-------|
| Core workflow | orchestrator, analyst, critic, editor | Actually useful routing/QA chain |
| Marketing | b2b-marketer, b2c-marketer, meta-advertiser, linkedin-ads-strategist, promoter | Meta + LinkedIn are well-built (75-88 lines with real playbook refs); others are 11-line stubs |
| Content | writer, copywriter, content-strategist, hook-master, seo-specialist, editor | Massive overlap - 6 agents that all "write things" |
| Research | deep-researcher, market-researcher, trend-forecaster | Researcher + market-researcher do the same job |
| Thinking | strategist, product-manager, monetization-guru, idea-generator | Rarely used; strategist + PM overlap |
| Creative/review | creative-spark, devils-advocate, simplifier, audience-simulator | Novelty agents, low usage |
| UX | ux-expert, ux-inconsistency-spotter | Two agents for one job |
| Other | prompt-engineer | Redundant with global skill 08 |

### Global Agents (3 in `~/.claude/agents/`)
- **agent-performance-auditor** - 100+ lines, well-structured, useful for periodic reviews
- **CEO** - 3 lines, literally just the tagline from CLAUDE.md. Useless.
- **lovable-prompt-expert** - Detailed but niche. Only relevant when using Lovable.

### Global Skills (32 in `~/.claude/skills/`)
- **01-30**: Generic frontend/product/design reference docs (React, CSS, forms, accessibility, etc.). These are textbook-style reference material, 100-486 lines each. Total ~7,000 lines of context.
- **last30days**: Actually useful research skill with real tool orchestration (WebSearch, Bash, Read).
- **remotion-best-practices**: Useful if you use Remotion for video content.

### Project Skill (1)
- **31-dentist-reviews-collector**: Excellent. Real workflow with Apify + Playwright tool orchestration, specific actor names, field mapping, error handling. This is what a skill should look like.

---

## Problems

1. **Agent bloat**: 28 project agents, but 15+ are 9-13 line stubs that just say "be good at X, output to /folder/file.md". They add no value over a single-line instruction in the orchestrator prompt.
2. **Massive overlap**: writer/copywriter/content-strategist/hook-master/editor all produce written content. deep-researcher/market-researcher are near-identical. ux-expert/ux-inconsistency-spotter should be one agent.
3. **Global skills are generic noise**: Skills 01-30 are generic web dev/product reference docs (React hooks, Prisma ORM, CSS systems). You deploy to EC2 with Supabase - you don't need 486 lines on "content creation suite" templates or "accessibility WCAG" sitting in context. These were likely bulk-generated, not curated.
4. **CEO global agent is dead weight**: 3 lines duplicating CLAUDE.md.
5. **No domain-specific skills**: Your business is dental/med spa marketing. The reviews collector is great, but there should be skills for report generation, competitor analysis, website template creation - the things you actually do daily.
6. **Orchestrator references agents that don't pull their weight**: The verification chain (critic -> editor -> seo-specialist -> analyst) sounds good but most of these agents have zero actionable instructions.

---

## Recommendations

### Agents: Keep vs Merge vs Remove

| Action | Agents | Rationale |
|--------|--------|-----------|
| **Keep as-is** | orchestrator, meta-advertiser, linkedin-ads-strategist | Well-built, have real playbook references |
| **Keep + beef up** | analyst, critic | Core QA chain but need specific evaluation criteria |
| **Merge into "writer"** | writer, copywriter, hook-master, editor, content-strategist | One agent with mode flags (draft/edit/hooks/strategy) |
| **Merge into "researcher"** | deep-researcher, market-researcher, trend-forecaster | One agent, different output templates |
| **Merge into "ux-reviewer"** | ux-expert, ux-inconsistency-spotter | One agent |
| **Merge into "strategist"** | strategist, product-manager, monetization-guru | One agent for all strategic thinking |
| **Remove** | CEO (global), prompt-engineer, creative-spark, devils-advocate, simplifier, audience-simulator, promoter, idea-generator, b2b-marketer, b2c-marketer, seo-specialist | Stubs with no real instructions; use ad-hoc prompting instead |
| **Keep (global)** | agent-performance-auditor, lovable-prompt-expert | Useful when needed |

**Target: 28 agents -> 9 agents** (orchestrator, writer, researcher, analyst, critic, strategist, ux-reviewer, meta-advertiser, linkedin-ads-strategist)

### Skills: Keep vs Remove

| Action | Skills | Rationale |
|--------|--------|-----------|
| **Keep** | last30days, remotion-best-practices, 31-dentist-reviews-collector | Real tool orchestration, domain-specific |
| **Delete all** | Skills 01-30 | Generic reference docs. If you need React help, Claude already knows React. These just waste context window. |
| **Create new** | See below | Domain-specific workflows you actually use |

### New Skills to Create (Project-Level)

1. **dentist-competitor-report** - Scrape competitor websites, extract pricing/services/reviews, output comparison table
2. **clinic-website-generator** - Template-based website generation for dental/med spa clients using your existing templates
3. **client-report-generator** - Generate the S4-style reports with images, metrics, and Hebrew content
4. **outreach-sequence-builder** - Cold email/LinkedIn sequences for dental clinic prospecting
5. **supabase-deploy** - Your specific EC2 + Supabase deployment checklist/automation

### Structural Improvements

- **Naming**: Use verb-noun format for skills (`collect-reviews`, `generate-report`) and role names for agents (`writer`, `researcher`)
- **Agent minimum standard**: Every agent must have at least: (1) specific evaluation criteria, (2) output format spec, (3) tool usage instructions if applicable. Delete anything under 20 lines.
- **Orchestrator update**: Reduce the agent list it references to match the consolidated 9. Update the verification chain to use the merged names.

---

## Priority Actions

1. **Delete global skills 01-30** - Zero effort, removes ~7K lines of noise from context
2. **Delete CEO.md global agent** - Duplicate of CLAUDE.md
3. **Merge content agents** (writer/copywriter/hook-master/editor/content-strategist) into one `writer.md` with mode sections
4. **Merge research agents** (deep-researcher/market-researcher/trend-forecaster) into one `researcher.md`
5. **Remove 11 stub agents** that have <15 lines of generic instructions
6. **Update orchestrator.md** to reference the consolidated agent list
7. **Create `clinic-website-generator` skill** - highest-frequency task in your business
8. **Create `client-report-generator` skill** - automate the S4 report pipeline
9. **Beef up analyst + critic** with specific rubrics (not just "be brutally honest")
10. **Create `dentist-competitor-report` skill** using Apify + Playwright pattern from reviews collector
