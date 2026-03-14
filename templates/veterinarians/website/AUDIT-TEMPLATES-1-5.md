# Veterinarian Templates 1-5 Audit Report

**Date:** 2026-03-14
**Scope:** Scroll/animation bugs + image issues across 10 checks

---

## Template 1 — "Warm Trust"

**BUG: Lenis double-raf (Check #3)**
- **Lines 801-805 + 810:** Both `requestAnimationFrame(raf)` loop AND `gsap.ticker.add()` call `lenis.raf()`. This double-drives Lenis, causing jank.
- **Fix:** Remove lines 801-805 (the manual rAF loop). Keep only:
  ```js
  gsap.ticker.add((time) => { lenis.raf(time * 1000); });
  ```

**BUG: opacity:0 + reduced-motion (Check #4)**
- **Lines 80-84:** The `@media(prefers-reduced-motion:reduce)` block does NOT override `opacity:0` for GSAP-animated elements. However, template 1 uses `fromTo` patterns (no CSS `opacity:0`), and the reduced-motion fallback at lines 982-985 manually sets `el.style.opacity='1'` for hero elements. Non-hero elements (service cards, gallery items, testimonials, process steps, footer columns) are NOT covered — if GSAP fails to load, they remain invisible.
- **Fix:** Add to the `else` block at line 980:
  ```js
  document.querySelectorAll('.service-card,.gallery-item,.testimonial-card,.process-step,.footer-grid > *,.ba-text,.ba-container,.about-content').forEach(el => { el.style.opacity = '1'; });
  ```

All other checks: **CLEAN**
- No pinned slides (Check #1 N/A)
- No SplitType (Check #2 N/A)
- No CSS `.visible` pattern (Check #5 N/A)
- No CSS animation initial states (Check #6 N/A)
- registerPlugin at line 808, before any ScrollTrigger usage (Check #7 OK)
- No overlapping slides (Check #8 N/A)
- Image paths all reference `../../images/template-images/{name}.jpg` — all 10 filenames exist (Check #9-10 OK)

---

## Template 2 — "Dark Precision"

**BUG: Lenis double-raf (Check #3)**
- **Lines 1662-1666 + 1670:** Same double-raf issue — both `requestAnimationFrame(raf)` loop AND `gsap.ticker.add()`.
- **Fix:** Remove lines 1662-1666.

**BUG: registerPlugin ORDER (Check #7)**
- **Line 1675:** `gsap.registerPlugin(ScrollTrigger)` appears AFTER ScrollTrigger is already used at line 1669 (`lenis.on('scroll', ScrollTrigger.update)`).
- **Fix:** Move `gsap.registerPlugin(ScrollTrigger);` to immediately after the script tags load, before the Lenis setup block (before line 1654).

**BUG: Manual `<span class="word">` + no SplitType conflict (Check #2)**
- **Lines 1284-1286:** Hero uses manual `<span class="word">` wrappers. No SplitType is loaded, so this is actually fine — no conflict. **CLEAN.**

**BUG: CSS `.visible` pattern not needed (Check #5)**
- Template uses GSAP `fromTo` for reveals, no IntersectionObserver with `.visible`. **CLEAN.**

All other checks: **CLEAN**
- No pinned slides (Check #1 N/A)
- Reduced motion handled at lines 1727-1731 (Check #4 OK — sets hero elements visible, and CSS comment at line 1231 says defaults visible for no-JS)
- Image paths all valid (Check #9-10 OK)

---

## Template 3 — "Playful Bounce"

**BUG: Lenis double-raf (Check #3)**
- **Lines 703-704 + 709:** Same double-raf: both `requestAnimationFrame(raf)` and `gsap.ticker.add()`.
- **Fix:** Remove lines 703-704.

**BUG: opacity:0 + reduced-motion (Check #4)**
- No reduced-motion fallback to set animated elements visible. Template uses `gsap.from()` which starts from `opacity:0`. If `prefersReduced` is true, the animations are skipped but there is NO fallback to show elements — service cards, gallery items, testimonials, process steps, about sections, and footer content could remain invisible.
- **Fix:** Add after line 788 (closing `}` of the animation block):
  ```js
  else {
    gsap.set('.trust-item,.service-card,.gallery-item,.testimonial-card,.process-step,.about-img-col,.about-text,.about-badge,.about-feature,.ba-wrapper,.footer-grid > *,.section-header > *', {opacity:1, y:0, x:0, scale:1, rotation:0});
  }
  ```

All other checks: **CLEAN**
- No pinned slides (Check #1 N/A)
- No SplitType (Check #2 N/A)
- registerPlugin at line 707, before ScrollTrigger usage (Check #7 OK)
- No `.visible` pattern (Check #5 N/A)
- Image paths all valid (Check #9-10 OK)

---

## Template 4 — "Architectural Calm"

**BUG: Lenis double-raf (Check #3)**
- **Lines 1037-1041 + 1044:** Same double-raf.
- **Fix:** Remove lines 1037-1041.

**BUG: registerPlugin ORDER (Check #7)**
- **Line 1049:** `gsap.registerPlugin(ScrollTrigger)` is AFTER `ScrollTrigger.update` is used at line 1043.
- **Fix:** Move `gsap.registerPlugin(ScrollTrigger);` before the Lenis block (before line 1030).

**BUG: hero `.line-inner` initial state (Check #6)**
- **Line 218:** `.hero-title .line-inner{transform:translateY(110%)}` — this CSS starts elements off-screen. The reduced-motion override at line 77 correctly sets `opacity:1!important;transform:none!important`. **CLEAN.**

**BUG: `.reveal` class used without CSS rule (Check #5)**
- Elements have class `reveal` in HTML (lines 669, 677, etc.) but there is NO CSS rule for `.reveal` (initial opacity, etc.). These rely purely on GSAP `fromTo`. The reduced-motion fallback at line 76 sets `.reveal` to `opacity:1!important`. **CLEAN.**

All other checks: **CLEAN**
- No pinned slides (Check #1 N/A)
- No SplitType (Check #2 N/A)
- Image paths all valid (Check #9-10 OK)

---

## Template 5 — "Dark Luxury"

**BUG: Lenis double-raf (Check #3)**
- **Lines 831-832 + 834:** Same double-raf.
- **Fix:** Remove lines 831-832.

**BUG: registerPlugin ORDER (Check #7)**
- **Line 839:** `gsap.registerPlugin(ScrollTrigger)` is AFTER `ScrollTrigger.update` at line 833.
- **Fix:** Move to before the Lenis block.

**BUG: CSS `.visible` pattern incomplete (Check #5)**
- **Line 989:** IntersectionObserver adds `.visible` class to `.reveal` elements. But there is NO CSS rule for `.reveal` (initial `opacity:0`) and NO `.reveal.visible` CSS rule. The observer is essentially doing nothing because no CSS is toggled.
- **Fix (option A):** Remove the IntersectionObserver block entirely (lines 986-989), since GSAP `fromTo` already handles all animation.
- **Fix (option B):** If keeping it as fallback, add CSS:
  ```css
  .reveal { opacity: 0; transform: translateY(40px); transition: opacity .6s, transform .6s; }
  .reveal.visible { opacity: 1; transform: none; }
  ```
  And add to reduced-motion media query: `.reveal { opacity: 1 !important; transform: none !important; }`

**BUG: opacity:0 CSS in service cards (Check #4)**
- **Lines 227, 229:** `.service-card p` and `.service-card .service-link` have `opacity:0` in CSS (revealed on hover). These are intentional hover effects, NOT scroll animations. **CLEAN** — no reduced-motion issue since they become visible on hover/focus.

**BUG: Hero pinned section (Check #1)**
- **Lines 879-884:** ScrollTrigger pins `.hero` with `pinSpacing:false`. Lines 899-909 fade `.hero-content` to `opacity:0` on scroll. No stacking slides that need z-index or explicit fade-out of other slides. **CLEAN** — single pin, not a multi-slide pin.

**BUG: Service card double animation (Check #6)**
- **Lines 957-961:** GSAP `fromTo` with `opacity:0,y:40` animates `.gsap-fade` elements.
- **Lines 1045-1055:** ALSO `gsap.from` on `.service-card` with `opacity:0`. Service cards have BOTH `.gsap-fade` AND separate `gsap.from` — causing double animation.
- **Fix:** Remove the second animation block (lines 1044-1055), since `.gsap-fade` already handles service cards.

All other checks: **CLEAN**
- No SplitType (Check #2 N/A)
- Image paths all valid (Check #9-10 OK)

---

## Summary Table

| Check | T1 | T2 | T3 | T4 | T5 |
|-------|----|----|----|----|-----|
| 1. Pinned slides fade-out | N/A | N/A | N/A | N/A | OK |
| 2. SplitType conflicts | N/A | OK | N/A | N/A | N/A |
| 3. Lenis double-raf | **BUG** | **BUG** | **BUG** | **BUG** | **BUG** |
| 4. opacity:0 + reduced-motion | **BUG** | OK | **BUG** | OK | OK |
| 5. CSS .visible pattern | N/A | N/A | N/A | OK | **BUG** |
| 6. Animation initial state | OK | OK | OK | OK | **BUG** |
| 7. registerPlugin order | OK | **BUG** | OK | **BUG** | **BUG** |
| 8. z-index overlapping slides | N/A | N/A | N/A | N/A | N/A |
| 9. Image paths reasonable | OK | OK | OK | OK | OK |
| 10. Broken image refs | OK | OK | OK | OK | OK |

**Total bugs:** 12 across 5 templates. Most common: Lenis double-raf (all 5), registerPlugin order (3 of 5).
