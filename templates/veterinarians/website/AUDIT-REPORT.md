# Veterinarian Templates Audit Report

**Date:** 2026-03-14
**Templates audited:** 1, 2, 3, 5, 7, 9

## Summary

Templates 1, 2, 3, 5, 9 are mostly solid. Template 7 has a critical Lenis-ScrollTrigger sync issue. No templates have empty content, broken layouts, or zero-height sections. All 6 templates have populated service cards with real text. The main issues are missing Lenis sync (T7) and a deprecated Lenis package URL (T5).

---

## Template-1: Warm/Organic (DM Serif + DM Sans)

**Sections present:** Hero, Trust, Services, Before-After, About, Gallery, Testimonials, Process, Footer/Contact -- ALL 10 PRESENT

**Issues found:**
- NONE CRITICAL. This template is clean.
- Lenis: Initialized correctly (`new Lenis()`), synced with ScrollTrigger (`lenis.on('scroll', ScrollTrigger.update)` + `gsap.ticker.add`)
- `gsap.registerPlugin(ScrollTrigger)` -- present
- Hero: `min-height: 100dvh` -- good
- `overflow-x: hidden` on body only -- correct, won't block scroll
- All content populated, no empty divs

---

## Template-2: Tech/Grid (Space Grotesk + Inter)

**Sections present:** Hero, Trust, Services, Before-After, About, Gallery, Testimonials, Process, Footer/Contact -- ALL 10 PRESENT

**Issues found:**
- NONE CRITICAL. This template is clean.
- Lenis: Initialized inside try/catch block, synced with ScrollTrigger
- `gsap.registerPlugin(ScrollTrigger)` -- present
- Hero: `min-height: 100vh` -- good
- Mobile menu: `position: fixed; height: 100vh` but `display: none` by default -- correct
- All content populated

---

## Template-3: Playful/Rounded (Baloo 2 + Nunito)

**Sections present:** Hero, Trust, Services, Before-After (id="results"), About, Gallery, Testimonials, Process, Footer/Contact -- ALL 10 PRESENT

**Issues found:**
- NONE CRITICAL.
- Lenis: Loaded from CDN in `<head>`, initialized correctly, synced with ScrollTrigger
- `gsap.registerPlugin(ScrollTrigger)` -- present
- Hero: `min-height: 100vh` -- good
- `overflow-x: hidden` on body -- correct
- All content populated

---

## Template-5: Luxury/Dark (Cormorant Garamond + Inter)

**Sections present:** Hero, Trust, Services, Before-After (id="beforeafter"), About, Gallery, Testimonials, Process, Footer/Contact + CTA band -- ALL 10 PRESENT

**Issues found:**
1. **MEDIUM: Deprecated Lenis CDN package** -- Uses `@studio-freight/lenis@1.0.42` (line 825). Studio Freight renamed to `lenis` package. This URL may stop working. Other templates use `lenis@1.0.42` or `lenis@1.1.18`.
2. **LOW: Two fixed overlay elements with high z-index** -- `.grain` (z-index: 9998) and `.vignette` (z-index: 9997) are `position: fixed; inset: 0`. Both have `pointer-events: none` so they won't block interaction, but they add visual noise and GPU cost.
- Lenis: Initialized correctly inside try/catch, synced with ScrollTrigger
- `gsap.registerPlugin(ScrollTrigger)` -- present
- Hero: `height: 100vh; min-height: 700px` -- good
- All content populated

---

## Template-7: Emergency/Bold (Oswald + Inter)

**Sections present:** Hero, Trust, Services, Before-After (id="results"), About, Gallery, Testimonials (id="reviews"), Process, Footer/Contact -- ALL 10 PRESENT

**Issues found:**
1. **CRITICAL: Missing Lenis-ScrollTrigger sync** -- Lenis is initialized (`new Lenis(...)`) and has its own `requestAnimationFrame` loop, but there is NO `lenis.on('scroll', ScrollTrigger.update)` and NO `gsap.ticker.add(time => lenis.raf(time * 1000))`. This means ScrollTrigger animations will be jittery/delayed because ScrollTrigger doesn't know about Lenis scroll position. Every other template has this sync code.
2. **MEDIUM: Lenis `smooth` option (deprecated)** -- Uses `smooth: true` (line 1011) which was renamed to `smoothWheel` in newer Lenis versions. Combined with the older `lenis@1.0.42` it may still work but is fragile.
3. **LOW: Lightbox has `position: fixed; inset: 0; z-index: 9999`** but starts with `display: none` and `background: rgba(0,0,0,0.95)` -- this is correct behavior (opens on click).
- Hero: `height: 100vh` -- good
- `gsap.registerPlugin(ScrollTrigger)` -- present
- `overflow-x: hidden` on body -- correct
- All content populated with real text

---

## Template-9: Neon/Cyberpunk (Orbitron + Inter)

**Sections present:** Hero, Trust, Services, Before-After (id="results"), About, Gallery, Testimonials (id="reviews"), Process, Footer/Contact -- ALL 10 PRESENT

**Issues found:**
- NONE CRITICAL.
- Lenis: Initialized correctly (inside `!prefersReducedMotion` check), synced with ScrollTrigger
- `gsap.registerPlugin(ScrollTrigger)` -- present
- Hero: `height: 100vh` -- good
- `overflow-x: hidden` on body -- correct
- All content populated with real text

---

## Cross-Template Summary Table

| Issue | T1 | T2 | T3 | T5 | T7 | T9 |
|-------|----|----|----|----|----|----|
| Lenis initialized | OK | OK | OK | OK | OK | OK |
| Lenis-ScrollTrigger sync | OK | OK | OK | OK | **MISSING** | OK |
| gsap.registerPlugin(ST) | OK | OK | OK | OK | OK | OK |
| Hero 100vh | OK | OK | OK | OK | OK | OK |
| All 10 sections present | OK | OK | OK | OK | OK | OK |
| Content populated | OK | OK | OK | OK | OK | OK |
| No blocking overflow | OK | OK | OK | OK | OK | OK |
| No blocking fixed elements | OK | OK | OK | OK | OK | OK |
| Deprecated Lenis CDN | -- | -- | -- | **YES** | -- | -- |

## Fixes Needed (Priority Order)

1. **Template-7:** Add Lenis-ScrollTrigger sync after `requestAnimationFrame(raf)`:
   ```js
   lenis.on('scroll', ScrollTrigger.update);
   gsap.ticker.add(time => lenis.raf(time * 1000));
   gsap.ticker.lagSmoothing(0);
   ```
2. **Template-5:** Update Lenis CDN from `@studio-freight/lenis@1.0.42` to `lenis@1.1.18`
