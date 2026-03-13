---
name: web-design-research
description: Research modern web design inspiration — find top sites, capture hero screenshots, analyze design patterns (typography, animation, layout, color), and update the design-inspiration folder with new findings. Use when looking for website design inspiration, updating the design playbook, or adding new reference sites before building templates.
---

# Web Design Research

Discover and analyze modern website designs, capture screenshots, and maintain a living design inspiration library. Each run ADDS to the existing collection — it never starts from scratch.

## Trigger

- "Find more design inspiration"
- "Research modern website designs"
- "Update the design playbook"
- "Add design inspiration for [topic/style]"
- "Find sites with [specific pattern — e.g., dark hero, scroll animation, bento grid]"

## Prerequisites
- None — this skill runs independently

## Inputs

| Input | Required | Default |
|-------|----------|---------|
| Focus area | No | General modern design |
| Number of new sites | No | 10-15 |
| Specific platforms to search | No | All from inspiration-sources.md |

---

## Step 1: Review Existing Collection

Read current state:
1. `design-inspiration/sites.csv` — what's already collected
2. `design-inspiration/web-design-playbook.md` — current playbook
3. `design-inspiration/inspiration-sources.md` — platforms to search

Count existing sites. The goal is to ADD new ones, not duplicate.

---

## Step 2: Research New Sites

### Search Sources (in priority order)

Use `perplexity_search` and `perplexity_research` to find new sites from:

1. **Godly** — godly.website (curated modern sites)
2. **Awwwards** — awwwards.com (SOTD/SOTY winners)
3. **CSSDA** — cssdesignawards.com (scored awards)
4. **Land-book** — land-book.com (landing pages)
5. **SiteInspire** — siteinspire.com (editorial/minimal)
6. **Httpster** — httpster.net (clean modern)
7. **Supahero** — supahero.io (hero sections)
8. **Dribbble** — dribbble.com/search/hero-section (visual concepts)
9. **frontend.horse** — trend analysis articles
10. **slashdev.io** — design education lists

### Search Queries (adapt to focus area)
- "best website design [year]"
- "awwwards site of the day [month] [year]"
- "[focus area] website design inspiration"
- "best [pattern] websites" (e.g., "best scroll animation websites")
- "[platform] featured sites [year]"

### For Each New Site, Capture:
- URL (must be real and verified)
- Business/project name
- Category (SaaS, Agency, Portfolio, E-commerce, Product, etc.)
- Source platform where found
- Hero type (video, 3D, animated text, split, fullscreen image, interactive, parallax)
- Color palette description
- Typography approach
- Animation techniques used
- Key sections worth studying
- 1-sentence "why it's notable"

### Quality Filters
- Must be from 2024 or newer
- No generic WordPress/Squarespace templates
- No major corporation sites unless design is exceptional
- Must have real design merit (not just famous brand)

---

## Step 3: Capture Screenshots

For each new site, use Playwright:

### Desktop (1440x900)
```
1. mcp__playwright__browser_resize → 1440x900
2. mcp__playwright__browser_navigate → site URL
3. Wait 3s for animations to settle
4. mcp__playwright__browser_take_screenshot → design-inspiration/screenshots/{domain}/desktop-hero.png
```

### Mobile (375x812)
```
1. mcp__playwright__browser_resize → 375x812
2. mcp__playwright__browser_take_screenshot → design-inspiration/screenshots/{domain}/mobile-hero.png
```

### Key Section (optional — if site has standout section)
```
1. Scroll to notable section
2. mcp__playwright__browser_take_screenshot → design-inspiration/screenshots/{domain}/section-{name}.png
```

**Screenshot batching:** When capturing screenshots, use batches of 3 sites maximum per agent to avoid JSON encoding errors. Process all sites but in small batches.

**If a site fails to load:** Skip it, note the failure, move to the next.

---

## Step 4: Update sites.csv

Append new rows to `design-inspiration/sites.csv`. CSV columns:
```
url,domain,name,category,source,hero_type,color_palette,typography,animations,key_sections,notable_element,date_added
```

- Do NOT overwrite existing rows
- Check for duplicates before adding (match on domain)
- Set date_added to today's date

---

## Step 5: Update Playbook (if new patterns found)

Read `design-inspiration/web-design-playbook.md`. If the new sites reveal patterns NOT already in the playbook:

1. Add new font pairings discovered
2. Add new animation techniques
3. Add new hero patterns
4. Update color palette archetypes
5. Add new section layout patterns
6. Update anti-patterns if needed

**Do NOT rewrite the playbook** — only append new findings or update specific sections.

---

## Step 6: Analyze Focus Area (if specific focus given)

If user asked about a specific pattern (e.g., "find sites with great scroll animations"):

1. Filter the full sites.csv for that pattern
2. Write a focused analysis to `design-inspiration/analyses/{focus-area}.md`
3. Include: top 5 examples, common techniques, CSS/JS code patterns, what makes them work

---

## Output Summary

Print to chat:
```
Design inspiration updated.

Added: {X} new sites to sites.csv (total now: {Y})
Screenshots: {X} desktop + {X} mobile saved
Playbook: {updated sections, if any}

Top finds this run:
- {Site 1} — {why notable}
- {Site 2} — {why notable}
- {Site 3} — {why notable}
```

---

## Error Handling

- **Playwright not available:** Skip screenshots, do research + CSV update only
- **Site blocks scraping:** Note in CSV, skip screenshot
- **Duplicate site found:** Skip, don't re-add
- **Focus area too narrow:** Broaden search, note limited results
- **CSV doesn't exist yet:** Create it with header row first
