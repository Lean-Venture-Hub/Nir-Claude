---
name: vertical-research
description: Research a business vertical's website best practices and produce a detailed {vertical-name}.md guide with 20+ inspiration sites, 5+ best-practice articles, customer psychology, visual direction, content guidelines, services taxonomy, SEO keywords, and anti-patterns. Use when entering a new vertical (e.g., auto repair, landscaping, med spa) and need a reference file for template builders.
---

# Vertical Website Research

Research a specific business vertical and produce a comprehensive guide file that a template builder can use to create stunning, high-converting websites for businesses in that vertical.

## Trigger

User asks to research a vertical for website best practices, or says something like:
- "Research the [vertical] industry for websites"
- "Create a vertical guide for [vertical]"
- "I need website best practices for [vertical]"
- "We're entering the [vertical] vertical"

## Prerequisites
- None — this skill runs independently as the first step for a new vertical

## Inputs

| Input | Required | Default |
|-------|----------|---------|
| Vertical name | Yes | — |
| Market/geography | No | US |
| Language | No | English |

---

## Step 1: Plan Research Queries

Based on the vertical name, generate search queries for each research area:

**Inspiration websites:**
- "best [vertical] website design"
- "award winning [vertical] website"
- "best [vertical] websites examples"
- "[vertical] website design inspiration"
- "best local [vertical] websites"
- "[vertical] website portfolio" (on design agency sites)

**Best practice articles:**
- "[vertical] website best practices"
- "[vertical] web design tips"
- "[vertical] website conversion optimization"
- "[vertical] digital marketing guide"

**Customer psychology:**
- "why customers choose [vertical] provider"
- "[vertical] customer trust factors"
- "[vertical] customer fears concerns"

**SEO:**
- "[vertical] local SEO keywords"
- "what do customers search for [vertical]"

---

## Step 2: Execute Research (Use Parallel Agents)

Launch 2 researcher agents in parallel:

### Agent A — Websites & Articles
Use `perplexity_search` and `perplexity_research` to find:
- **20+ real websites** of businesses in this vertical (independent/small chain, target market)
  - Must be REAL URLs — verify they exist
  - For each: business name, URL, location, what makes it stand out
  - Prioritize: award winners, sites cited by multiple design blogs, strong UX
- **5+ articles** about website best practices for this vertical
  - For each: title, source, URL, key takeaway
- **Design patterns** observed across top sites: colors, hero styles, section order, CTAs

### Agent B — Psychology, Services, SEO
Use `perplexity_search` and `perplexity_research` to find:
- **Customer psychology**: top fears, trust signals, buying decision drivers
- **Services taxonomy**: standard service categories with sub-services
- **SEO keywords**: high-intent keywords by type (near-me, service+city, problem-based, trust-seeking, specialty)
- **Blog topics**: 8-10 proven blog article templates

---

## Step 3: Compile the Output File

Merge all research into a single file at `research/{vertical-name}.md`.

### Required File Structure

```markdown
# {Vertical Name} — Vertical Website Guide
**Date:** {date} | **Market:** {market} | **Purpose:** Template builder reference

## TL;DR
{2-3 sentences: industry trust dynamics, what winning websites do differently, key conversion insight}

---

## Inspiration Websites ({count} Verified Sites)

| # | Business | URL | Location | What Makes It Stand Out |
|---|----------|-----|----------|------------------------|
{Each URL must be a clickable markdown link: [domain.com](https://domain.com)}
{Minimum 20 entries}
{Include award winners, notable design elements, niche positioning}

**Pattern:** {1-2 sentence summary of what the best sites have in common}

---

## Best Practice Articles ({count} References)

| # | Title | Source | URL | Key Takeaway |
|---|-------|--------|-----|--------------|
{Each URL must be a clickable markdown link}
{Minimum 5 entries}

---

## Customer Psychology

### Top Fears (What the Website Must Overcome)
{Numbered list, 3-5 fears with data/stats if available}

### Trust Signals (by conversion impact)
**Tier 1 — Must have:**
{Bullet list of highest-impact trust signals}

**Tier 2 — Strong differentiators:**
{Bullet list}

**Tier 3 — Nice to have:**
{Bullet list}

---

## Must-Have Website Sections (Priority Order)
{Numbered list, 8-10 sections in the order they should appear on page}

---

## Visual Direction

### Color Palettes
| Palette | When to Use |
|---------|-------------|
{3-5 palettes with reasoning}

### Hero Patterns (by effectiveness)
{Numbered list, 3-4 hero styles}

### Universal Hero Elements
{Bullet list of must-have hero elements}

### Photography Rules
{Do's and Don'ts as bullet lists}

---

## Content Guidelines

### Hero Headlines That Work
{4-5 headline templates with [placeholders]}

### CTA Copy Patterns
| CTA Text | Placement | Use Case |
|----------|-----------|----------|
{5-6 CTA patterns}

### Tone of Voice
{4-5 bullet points defining the right tone}

---

## Services Taxonomy

| Category | Sub-Services |
|----------|-------------|
{10-16 service categories with common sub-services}

---

## SEO & Local Search

### High-Intent Keywords
| Type | Examples |
|------|---------|
{5-6 keyword types with examples using [city] placeholders}

### Blog Topics ({count} Proven Templates)
{Numbered list, 8-10 blog topic templates}

---

## Anti-Patterns (What NOT to Do)
{Bullet list, 8-10 common mistakes to avoid}

---

*Sources: {comma-separated list of all sources used}*
```

---

## Step 4: Quality Checks

Before declaring done, verify:
- [ ] File is saved to `research/{vertical-name}.md`
- [ ] At least 20 inspiration websites with clickable URLs
- [ ] At least 5 best-practice articles with clickable URLs
- [ ] All URLs are markdown links: `[text](https://url)`
- [ ] TL;DR is specific to this vertical (not generic)
- [ ] Services taxonomy reflects what businesses in this vertical ACTUALLY offer
- [ ] Customer psychology section includes data/stats where available
- [ ] Anti-patterns are specific to this vertical
- [ ] File is under 10KB (aim for 5-8KB)
- [ ] No duplicate websites across the list

---

## Output Summary

Print to chat:
```
Done — vertical research for {Vertical Name}

File: research/{vertical-name}.md
- {X} inspiration websites with URLs
- {X} best practice articles
- Sections: psychology, visual direction, content, services, SEO, anti-patterns

Key insight: {1 sentence — the most important finding}
```

---

## Error Handling

- **Can't find 20 websites**: Include what you found + flag count shortfall. Search for "{vertical} website design portfolio" on agency sites for more.
- **Vertical is too niche**: Broaden to parent vertical (e.g., "mobile pet grooming" → include "pet grooming" sites too). Note the broadening.
- **Non-US market requested**: Adjust search queries to include country/region. Note that design patterns may differ.
- **URLs can't be verified**: Include the site but flag it in a "requires manual verification" sub-table.

---

## Next Step

After completing vertical research, run `template-creator` to create templates using this research.
