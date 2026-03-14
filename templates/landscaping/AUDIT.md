# Landscaping Templates Audit Report

**Date:** 2026-03-13 | **Templates audited:** 13 | **Base path:** `templates/landscaping/website/template-{N}/`

## TL;DR

All 13 templates pass every check. All have correct image references, working before/after sliders, GSAP+ScrollTrigger, Lenis smooth scroll, prefers-reduced-motion support, JSON-LD structured data, mobile navigation, all required sections, and are 25KB+ in size. No broken image paths found.

---

## Audit Results

| # | Size (KB) | Images | B/A Slider | GSAP | Lenis | Motion | JSON-LD | Mobile | Sections | Issues |
|---|-----------|--------|------------|------|-------|--------|---------|--------|----------|--------|
| 1 | 75 | ✅ | ✅ range input | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10/10 | None |
| 2 | 73 | ✅ | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10/10 | None |
| 3 | 44 | ✅ | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10/10 | None |
| 4 | 58 | ✅ | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ burger | ✅ 10/10 | None |
| 5 | 69 | ✅ | ✅ pointerdown | ✅ | ✅ | ✅ | ✅ | ✅ nav-toggle | ✅ 10/10 | None |
| 6 | 60 | ✅ | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10/10 | None |
| 7 | 60 | ✅ | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10/10 | None |
| 8 | 53 | ✅ | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10/10 | None |
| 9 | 56 | ✅ | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10/10 | None |
| 10 | 63 | ✅ | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10/10 | None |
| 11 | 56 | ✅ | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10/10 | None |
| 12 | 48 | ✅ | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10/10 | None |
| 13 | 55 | ✅ | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10/10 | None |

### Legend
- **Images**: hero.jpg, before.jpg, after.jpg, team.jpg, + ≥3 portfolio images
- **B/A Slider**: Interactive before/after with event handlers
- **GSAP**: GSAP CDN + ScrollTrigger.register
- **Lenis**: Lenis smooth scroll CDN
- **Motion**: `prefers-reduced-motion` media query
- **JSON-LD**: `application/ld+json` structured data
- **Mobile**: Hamburger/toggle menu for mobile
- **Sections**: nav, hero, services, before/after, portfolio, about, testimonials, process, CTA/contact, footer

## Image Coverage Detail

| # | hero | before | after | team | hardscape-patio | lawn-care | outdoor-living | landscape-lighting | irrigation | retaining-wall | Portfolio Count |
|---|------|--------|-------|------|-----------------|-----------|----------------|--------------------|-----------:|----------------|-----------------|
| 1 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 6/6 |
| 2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 6/6 |
| 3 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 6/6 |
| 4 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 6/6 |
| 5 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | 5/6 |
| 6 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | 5/6 |
| 7 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 6/6 |
| 8 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 6/6 |
| 9 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 6/6 |
| 10 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 6/6 |
| 11 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 6/6 |
| 12 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 6/6 |
| 13 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 6/6 |

> Templates 5 & 6 skip `irrigation.jpg` but still use 5 of 6 portfolio images (well above the 3 minimum).

## Slider Implementation Variants

| Method | Templates |
|--------|-----------|
| `mousedown`/`touchstart` drag | 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13 |
| `<input type="range">` with `input` event | 1 |
| `pointerdown` (Pointer Events API) | 5 |

## Broken Image Paths

None found. All image references use the correct `../../images/template-images/` path.

---

## Templates Needing Fixes

**None.** All 13 templates pass every check.

### Minor Notes (non-blocking)
- **Templates 5 & 6**: Don't reference `irrigation.jpg` as a portfolio image, but meet the ≥3 portfolio image minimum with 5 other images. Consider adding for completeness.
- **Template 1**: Uses `<input type="range">` instead of drag-based slider. Functionally equivalent but feels different from the other 12 templates.
