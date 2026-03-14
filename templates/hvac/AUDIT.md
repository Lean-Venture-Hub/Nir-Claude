# HVAC Templates Audit Report

**Date:** 2026-03-13 | **Templates audited:** 10 | **Base path:** `templates/hvac/website/template-{N}/`

## TL;DR

All 10 templates pass every check. All have correct image references (10/10 images), working before/after sliders (mousedown/touchstart), GSAP+ScrollTrigger, Lenis smooth scroll, prefers-reduced-motion support, JSON-LD structured data, mobile navigation, all 10 required sections, and are 25KB+ in size. No issues found.

---

## Audit Results

| # | Size (KB) | Images | B/A Slider | GSAP | Lenis | Motion | JSON-LD | Mobile | Sections | Issues |
|---|-----------|--------|------------|------|-------|--------|---------|--------|----------|--------|
| 1 | 45 | ✅ 10/10 | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ hamburger | ✅ 10/10 | None |
| 2 | 55 | ✅ 10/10 | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ hamburger | ✅ 10/10 | None |
| 3 | 43 | ✅ 10/10 | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ hamburger | ✅ 10/10 | None |
| 4 | 54 | ✅ 10/10 | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ burger | ✅ 10/10 | None |
| 5 | 50 | ✅ 10/10 | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ hamburger | ✅ 10/10 | None |
| 6 | 48 | ✅ 10/10 | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ hamburger | ✅ 10/10 | None |
| 7 | 53 | ✅ 10/10 | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ menu-toggle | ✅ 10/10 | None |
| 8 | 50 | ✅ 10/10 | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ nav-toggle | ✅ 10/10 | None |
| 9 | 56 | ✅ 10/10 | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ burger | ✅ 10/10 | None |
| 10 | 63 | ✅ 10/10 | ✅ mousedown/touch | ✅ | ✅ | ✅ | ✅ | ✅ hamburger | ✅ 10/10 | None |

### Legend
- **Images**: hero.jpg, team.jpg, ac-install.jpg, furnace-repair.jpg, ductwork.jpg, thermostat.jpg, maintenance.jpg, emergency.jpg, commercial.jpg, heat-pump.jpg
- **B/A Slider**: Interactive before/after with mousedown/touchstart event handlers
- **GSAP**: GSAP CDN + ScrollTrigger
- **Lenis**: Lenis smooth scroll CDN
- **Motion**: `prefers-reduced-motion` media query
- **JSON-LD**: `application/ld+json` structured data
- **Mobile**: Hamburger/toggle menu for mobile
- **Sections**: nav, hero, services, before/after, about, gallery, testimonials, process, contact, footer

## Image Coverage Detail

| # | hero | team | ac-install | furnace-repair | ductwork | thermostat | maintenance | emergency | commercial | heat-pump |
|---|------|------|------------|----------------|----------|------------|-------------|-----------|------------|-----------|
| 1 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 3 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 4 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 5 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 6 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 7 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 8 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 9 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 10 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## Slider Implementation Variants

| Method | Templates |
|--------|-----------|
| `mousedown`/`touchstart` drag | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 |

## Broken Image Paths

None found. All image references use the correct `../../images/template-images/` path.

---

## Templates Needing Fixes

**None.** All 10 templates pass every check.
