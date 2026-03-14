# Auto Repair Templates Audit: 17, 18, 19
**Date:** 2026-03-14

## Summary

Templates 17 and 18 passed all critical checks. Template 19 had one critical issue (GSAP `.to()` with CSS `opacity:0` on hero elements) which has been fixed -- converted to `.from()` pattern so content is visible by default if JS fails.

---

## Template 17

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1 | CSS opacity:0 on content | PASS | Only on decorative elements (::before, overlays) |
| 2 | Lenis CDN version | PASS | `lenis@1.1.18` correct |
| 3 | Lenis-ScrollTrigger sync | PASS | All 3 lines present |
| 4 | `.lenis.lenis-smooth` override | PASS | Line 54 |
| 5 | No double lenis.raf() | PASS | No requestAnimationFrame loop |
| 6 | GSAP .from()/.fromTo() only | PASS | `.to()` used only for parallax & counters (legitimate) |
| 7 | Image paths correct | WARN | 13/18 unique images. Missing: service-engine, service-brakes, service-oil, service-tires, service-diagnostics |
| 8 | Mobile responsive | PASS | 11 @media queries |
| 9 | JSON-LD | PASS | AutoRepair schema present |
| 10 | 10+ sections | PASS | 10 sections + footer |

---

## Template 18

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1 | CSS opacity:0 on content | PASS | Only on decorative (grain overlay, quote marks, step numbers) |
| 2 | Lenis CDN version | PASS | `lenis@1.1.18` correct |
| 3 | Lenis-ScrollTrigger sync | PASS | All 3 lines present |
| 4 | `.lenis.lenis-smooth` override | PASS | Line 53 |
| 5 | No double lenis.raf() | PASS | No requestAnimationFrame loop |
| 6 | GSAP .from()/.fromTo() only | PASS | `.to()` used only for scroll progress, parallax, horizontal scroll (legitimate) |
| 7 | Image paths correct | WARN | 17/18 unique images. Missing: exterior.jpg |
| 8 | Mobile responsive | PASS | 12 @media queries |
| 9 | JSON-LD | PASS | AutoRepair schema present |
| 10 | 10+ sections | PASS | 10 sections + footer |

---

## Template 19

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1 | CSS opacity:0 on content | **FIXED** | Hero elements had `opacity:0` in CSS -- removed |
| 2 | Lenis CDN version | PASS | `lenis@1.1.18` correct |
| 3 | Lenis-ScrollTrigger sync | PASS | All 3 lines present (inside `waitForLibs` callback) |
| 4 | `.lenis.lenis-smooth` override | PASS | Line 39 |
| 5 | No double lenis.raf() | PASS | No requestAnimationFrame loop |
| 6 | GSAP .from()/.fromTo() only | **FIXED** | Hero used `.to()` with CSS `opacity:0` -- converted to `.from()`, removed `gsap.set()` |
| 7 | Image paths correct | WARN | 15/18 unique images. Missing: customer-handshake, exterior, oil-change |
| 8 | Mobile responsive | PASS | 3 breakpoints (1024, 768, 480) + reduced-motion |
| 9 | JSON-LD | PASS | Schema present (uses placeholders as expected for template) |
| 10 | 10+ sections | PASS | 10 sections + hero header + footer |

---

## Fixes Applied

**Template 19** (`template_example-19.html`):
1. Removed `opacity: 0` from CSS for `.hero-eyebrow`, `.hero-h1`, `.hero-sub`, `.hero-cta-wrap`, `.hero-proof`
2. Converted hero timeline from `gsap.to()` to `gsap.from()` pattern
3. Removed unnecessary `gsap.set()` call that pre-positioned hero elements
