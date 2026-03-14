---
name: website-from-template-audit
description: Audit a generated website against its content.md for accuracy, completeness, visual quality, and layout correctness. Use when verifying a website built from a template — checks for generic/placeholder content, missing data, broken layout, and visual issues.
---

# Website From Template — Audit

Verify that a generated website is production-ready: no generic content, no layout issues, all data matches content.md exactly, and no `{{PLACEHOLDER}}` tokens remain.

## Trigger

User provides a path to:
- A **generated website** folder (e.g., `{Vertical}/reports/output/{business-folder}/`)
- A **template** folder (e.g., `templates/{vertical}/website/template-{N}/`)
- A live URL on the server

## Prerequisites
- For generated websites: `create-website-from-template` → generated website folder with `index.html` and `content.md` must exist
- For templates: the template HTML must exist (audits demo content quality instead of content.md matching)

## Inputs

1. **Website**: Either a local `index.html` path or a live URL (e.g., `https://lp.scalefox.ai/{path}`)
2. **Content file**: The `content.md` in the same folder (auto-detected if in standard output folder)

---

## Step 1: Load Content Source of Truth

Read the `content.md` file and extract ALL data fields. The structure may vary by vertical and language, but typically includes:

| Field | Examples |
|-------|---------|
| Business name (full + short) | Name / brand name |
| Owner/professional name | Doctor, technician, owner name |
| Category/vertical | Type of business |
| Address | Full street address |
| Phone | Phone number |
| Rating | Google rating / review score |
| Hero headline + subtitle | Main heading and subheading |
| About text | About section paragraph(s) |
| Services list | Bullet list of services offered |
| Blog articles (if any) | Titles + body text |
| Reviews/testimonials | Reviewer name, stars, text |

**Save these as your checklist. Every single field must appear in the HTML.**

### Placeholder Token Check (CRITICAL)
Reference `templates/PLACEHOLDER_CONTRACT.md` for the full list of `{{PLACEHOLDER}}` tokens. Scan the generated HTML for ANY remaining `{{...}}` tokens — if even one remains, the audit is an automatic FAIL.

---

## Step 2: Content Accuracy Audit (CRITICAL)

Use Playwright to load the website (`mcp__playwright__browser_navigate`), then `mcp__playwright__browser_snapshot` to get the full DOM.

**Check EVERY field from content.md against the rendered page:**

### 2a: Hero Section
- [ ] Headline matches `כותרת` from content.md exactly (word for word)
- [ ] Subtitle matches `תת-כותרת` exactly
- [ ] Business/owner name appears correctly
- [ ] No placeholder text remaining (check against `templates/PLACEHOLDER_CONTRACT.md` tokens)

### 2b: About Section
- [ ] About paragraph matches content.md `אודות` section exactly
- [ ] Owner/professional name mentioned correctly (not template placeholder)
- [ ] No generic filler like "Lorem ipsum" or template default about text

### 2c: Services Section
- [ ] Services listed match `שירותים` from content.md
- [ ] Service descriptions are specific to this business (not generic template text)
- [ ] Number of service cards matches number of services in content.md
- [ ] No duplicate services

### 2d: Testimonials/Reviews Section
- [ ] Every review from content.md appears on the page
- [ ] Reviewer NAMES match exactly (including Hebrew names, spaces, quotes)
- [ ] Star ratings match (★ count matches content.md)
- [ ] Review TEXT matches exactly (no truncation, no rewording)
- [ ] No template placeholder reviews ("John D.", "Happy Patient", etc.)

### 2e: Contact/CTA Section
- [ ] Phone number matches `טלפון` from content.md
- [ ] Address matches `כתובת` if displayed
- [ ] Phone link (`tel:`) is correctly formatted

### 2f: Navigation & Footer
- [ ] Business name in navbar/logo matches
- [ ] Footer business name matches
- [ ] No template brand name or placeholder tokens remaining

### 2g: Blog Pages (if applicable)
- [ ] Blog article titles match content.md
- [ ] Blog article body text matches content.md
- [ ] Blog links from main page work

**CRITICAL: Flag ANY text that doesn't match content.md. Even a single wrong name or placeholder is a fail.**

---

## Step 3: Visual & Layout Audit

Use `mcp__playwright__browser_take_screenshot` at multiple viewports.

### 3a: Desktop (1440px width)
- [ ] Hero image loads and covers viewport
- [ ] No horizontal scrollbar
- [ ] Services grid renders as 3 columns
- [ ] Testimonials grid renders as 3 columns
- [ ] All sections have proper spacing (no collapsed margins)
- [ ] Text is readable against backgrounds (contrast)

### 3b: Tablet (768px width)
Resize with `mcp__playwright__browser_resize` to 768x1024.
- [ ] Navigation hamburger menu appears
- [ ] Services stack to 1-2 columns
- [ ] No text overflow or clipping
- [ ] Images resize properly

### 3c: Mobile (375px width)
Resize to 375x812.
- [ ] Full mobile layout works
- [ ] Hero text doesn't overflow
- [ ] Buttons are tappable size (min 44px)
- [ ] No horizontal scroll
- [ ] Font sizes readable (min 14px body)

### 3d: Image Audit
For each image on the page, use Playwright evaluate to check:
```javascript
document.querySelectorAll('img').forEach(img => {
  console.log(img.src, img.naturalWidth, img.complete);
});
```
- [ ] All images load (naturalWidth > 0, complete === true)
- [ ] No broken image icons
- [ ] Images have appropriate alt text (not empty, not "image1")
- [ ] Hero background image loads

### 3e: Scroll & Animation Check (CRITICAL — must catch all patterns)

Use Playwright to scroll through the full page and verify animations work correctly.

**Basic scroll checks:**
- [ ] `.reveal` / `.animate-on-scroll` elements become `.visible` on scroll
- [ ] No layout jumps or shifts during scroll
- [ ] Lazy-loaded images load when scrolled into view
- [ ] Navbar becomes fixed/frosted on scroll

**Pinned section checks (stats, reviews, testimonials with ScrollTrigger pin):**
- [ ] Scroll through each pinned section slowly — each slide must appear AND disappear cleanly
- [ ] No overlapping text between slides at any scroll position
- [ ] Conclusion/summary slide appears only after all slides have exited
- [ ] Take a screenshot mid-transition between slides to verify no overlap

**Animation code audit (read the JS, not just visual):**
- [ ] **NO CSS opacity:0 on content**: Search for `opacity:0` or `opacity: 0` in CSS — content elements (headings, paragraphs, cards, sections) MUST NOT start hidden. GSAP `.from()` handles animation. Classes like `.gsap-fade{opacity:0}` are BANNED — they make content invisible if JS fails. FIX: remove `opacity:0` from CSS, let GSAP handle it via `.from({opacity:0})`
- [ ] **Subtitle not inside h1**: Verify subtitle/subheading text is in a `<p>` tag, NOT inside `<h1>`. Subtitle text inside `<h1>` renders at headline size
- [ ] **Hero word-break**: Hero headline CSS must include `word-break:keep-all` — words must never break mid-word
- [ ] If SplitType is used, verify no manual `<span class="word">` wrappers exist on the same element
- [ ] If Lenis is used, verify only ONE raf integration exists (gsap.ticker.add OR requestAnimationFrame, never both)
- [ ] If Lenis is used, verify `lenis.on('scroll', ScrollTrigger.update)` exists after Lenis init
- [ ] If Lenis is used, verify it's wrapped inside `if (!prefersReducedMotion)` — smooth scroll must not run for reduced-motion users
- [ ] Verify `gsap.registerPlugin(ScrollTrigger)` appears before any ScrollTrigger usage (including `ScrollTrigger.update` in Lenis sync)
- [ ] Verify all CSS selector blocks have closing `}` — scan for unclosed rules that silently break styles below

**Overlap detection (automated):**
Run this Playwright evaluate at multiple scroll positions through pinned sections:
```javascript
const visible = [...document.querySelectorAll('.stat-slide, .review-slide, [class*="slide"]')]
  .filter(el => getComputedStyle(el).opacity > 0.5);
if (visible.length > 1) console.error('OVERLAP: multiple slides visible simultaneously');
```

---

## Step 4: Technical Checks

### 4a: RTL/LTR Correctness
- [ ] Hebrew version has `dir="rtl"` on `<html>`
- [ ] English version (if exists) has `dir="ltr"`
- [ ] Text alignment follows direction (right-aligned for Hebrew)

### 4b: Links
- [ ] All `href="#"` links are intentional (section anchors) or flagged as broken
- [ ] Phone `tel:` link works
- [ ] Google Maps link (if present) is correct
- [ ] Blog links resolve to existing pages

### 4c: Meta & SEO
- [ ] `<title>` contains business name
- [ ] `<meta name="description">` exists and mentions business
- [ ] `lang` attribute correct ("he" or "en")

### 4d: JSON-LD Schema Validation
- [ ] JSON-LD `@type` matches the vertical (e.g., `AutoRepair` for auto repair, `Dentist` for dentists, `LandscapingBusiness` for landscaping)
- [ ] JSON-LD `name`, `telephone`, `address` fields populated with real data (not placeholders)

---

## Step 5: Generate Audit Report

Output to `{website-folder}/audit-report.md`:

```markdown
# Audit Report — {Business Name}
**Date:** {date}
**Template:** {template number}
**Status:** PASS / FAIL / PASS WITH WARNINGS

## Content Accuracy
| Check | Status | Details |
|-------|--------|---------|
| Hero headline | ✅/❌ | ... |
| Hero subtitle | ✅/❌ | ... |
| Owner/professional name | ✅/❌ | ... |
| Placeholder tokens ({{...}}) | ✅/❌ | ... |
| JSON-LD schema type | ✅/❌ | ... |
| About text | ✅/❌ | ... |
| Services | ✅/❌ | ... |
| Reviews (X/Y matched) | ✅/❌ | ... |
| Phone number | ✅/❌ | ... |
| Address | ✅/❌ | ... |

## Visual Quality
| Check | Status | Details |
|-------|--------|---------|
| Desktop layout | ✅/❌ | ... |
| Tablet layout | ✅/❌ | ... |
| Mobile layout | ✅/❌ | ... |
| Images loading | ✅/❌ | X/Y loaded |
| Animations | ✅/❌ | ... |

## Technical
| Check | Status | Details |
|-------|--------|---------|
| RTL/LTR | ✅/❌ | ... |
| Links | ✅/❌ | ... |
| Meta tags | ✅/❌ | ... |

## Issues Found
1. [CRITICAL] ...
2. [WARNING] ...

## Recommendation
[SHIP / FIX THEN SHIP / REBUILD]
```

---

## Severity Levels

- **CRITICAL (blocks shipping):** Wrong business name, placeholder content, remaining `{{...}}` tokens, wrong phone number, wrong reviews, wrong JSON-LD schema type, broken layout on any viewport, overlapping content in pinned scroll sections, scroll animations that never trigger (opacity:1 initial state with .visible pattern), Lenis double-raf causing jittery scrolling
- **WARNING (fix but can ship):** Missing alt text, minor spacing issues, missing meta description
- **INFO:** Suggestions for improvement (better image compression, etc.)

---

## Template-Specific Audit (when auditing a template, not a generated site)

When the path points to a `templates/{vertical}/website/template-{N}/` folder (not a generated site), run these checks instead of content.md matching:

### Demo Content Check (CRITICAL — automatic FAIL if any remain)
```bash
grep -c '{{' template_example-{N}.html
```
- [ ] Count is **0** — no `{{PLACEHOLDER}}` tokens remain
- [ ] Business name is a real demo name (not "Business Name" or "{{BUSINESS_NAME}}")
- [ ] Phone number is a real demo number (not "000-000-0000" or "{{PHONE}}")
- [ ] Reviews have real names and text (not "Customer Name" or "Review text here")
- [ ] Services have real names (not "Service 1" or "{{SERVICE_1}}")
- [ ] About section has a real paragraph (not lorem ipsum or placeholder)

### File Structure Check
- [ ] `template_example-{N}.html` exists
- [ ] `template-manifest.json` exists
- [ ] `blog.html` exists with 3 article cards
- [ ] `blog/` folder exists with 3 subfolders, each containing `index.html`
- [ ] Blog pages match the template's design (same nav, footer, colors, fonts)

### Technical Checks (same as generated site)
- Run all Layer 4 animation checks (Lenis CDN, sync, opacity, etc.)
- Run responsive checks at 1440px, 768px, 375px
- Verify JSON-LD schema data uses demo values (not placeholders)
- Check all image paths resolve to files in the shared images folder
