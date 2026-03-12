---
name: website-from-template-audit
description: Audit a generated clinic website against its content.md for accuracy, completeness, visual quality, and layout correctness. Use when verifying a website built from a template — checks for generic/placeholder content, missing data, broken layout, and visual issues.
---

# Website From Template — Audit

Verify that a generated clinic website is production-ready: no generic content, no layout issues, all data matches content.md exactly.

## Trigger

User provides a path to a generated website folder (e.g., `Dentists/reports/output/35 - dr-pnsnkv-kvnstntyn/`) OR a live URL on the server.

## Inputs

1. **Website**: Either a local `index.html` path or a live URL (e.g., `https://lp.scalefox.ai/{path}`)
2. **Content file**: The `content.md` in the same folder (auto-detected if in standard output folder)

---

## Step 1: Load Content Source of Truth

Read the `content.md` file and extract ALL data fields:

| Field | Where to find in content.md |
|-------|---------------------------|
| Clinic name (full) | `## פרטי המרפאה` → `שם` |
| Clinic name (short) | `שם מקוצר` |
| Doctor name | `רופא/ה` |
| Category | `קטגוריה` |
| Address | `כתובת` |
| Phone | `טלפון` |
| Google rating | `דירוג גוגל` |
| Hero headline | `### Hero` → `כותרת` |
| Hero subtitle | `תת-כותרת` |
| About text | `### אודות` (full paragraph) |
| Services list | `### שירותים` (bullet list) |
| Blog articles | `## מאמרי בלוג` (titles + body) |
| Reviews | `## ביקורות גוגל אמיתיות` (reviewer name, stars, text) |

**Save these as your checklist. Every single field must appear in the HTML.**

---

## Step 2: Content Accuracy Audit (CRITICAL)

Use Playwright to load the website (`mcp__playwright__browser_navigate`), then `mcp__playwright__browser_snapshot` to get the full DOM.

**Check EVERY field from content.md against the rendered page:**

### 2a: Hero Section
- [ ] Headline matches `כותרת` from content.md exactly (word for word)
- [ ] Subtitle matches `תת-כותרת` exactly
- [ ] Doctor/clinic name appears correctly
- [ ] No placeholder text like "שם המרפאה", "Nova Dental", "Dr. Smith", or template default text

### 2b: About Section
- [ ] About paragraph matches content.md `אודות` section exactly
- [ ] Doctor name mentioned correctly (not template placeholder)
- [ ] No generic filler like "Lorem ipsum" or template default about text

### 2c: Services Section
- [ ] Services listed match `שירותים` from content.md
- [ ] Service descriptions are specific to this clinic (not generic template text)
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
- [ ] Clinic name in navbar/logo matches
- [ ] Footer clinic name matches
- [ ] No "Nova Dental" or template brand name remaining

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

### 3e: Scroll & Animation Check
Scroll through the full page with Playwright:
- [ ] `.reveal` elements become `.visible` on scroll
- [ ] No layout jumps or shifts during scroll
- [ ] Lazy-loaded images load when scrolled into view
- [ ] Navbar becomes fixed/frosted on scroll

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
- [ ] `<title>` contains clinic name
- [ ] `<meta name="description">` exists and mentions clinic
- [ ] `lang` attribute correct ("he" or "en")

---

## Step 5: Generate Audit Report

Output to `{website-folder}/audit-report.md`:

```markdown
# Audit Report — {Clinic Name}
**Date:** {date}
**Template:** {template number}
**Status:** PASS / FAIL / PASS WITH WARNINGS

## Content Accuracy
| Check | Status | Details |
|-------|--------|---------|
| Hero headline | ✅/❌ | ... |
| Hero subtitle | ✅/❌ | ... |
| Doctor name | ✅/❌ | ... |
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

- **CRITICAL (blocks shipping):** Wrong clinic name, placeholder content, wrong phone number, wrong reviews, broken layout on any viewport
- **WARNING (fix but can ship):** Missing alt text, minor spacing issues, missing meta description
- **INFO:** Suggestions for improvement (better image compression, etc.)
