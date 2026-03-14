# Vet Templates 6-10 Audit Report

**Available images:** `boarding.jpg, cat-care.jpg, dental.jpg, emergency.jpg, exam-dog.jpg, grooming.jpg, hero.jpg, surgery.jpg, team.jpg, vaccination.jpg`

---

## Template 6 (Holistic/Organic) — 2 BUGS

| # | Check | Line | Issue | Fix |
|---|-------|------|-------|-----|
| 3 | **Lenis double-raf** | 1045-1049 | Uses `requestAnimationFrame` loop only. No `gsap.ticker.add`. | CLEAN |
| 4 | **opacity:0 + reduced-motion** | 77-88, 154 | `.fade-up` is set to `opacity:1` in CSS (line 154), and GSAP uses `fromTo` with `opacity:0`. Reduced-motion override at line 84 covers `.fade-up`. | CLEAN |
| 7 | **registerPlugin order** | 1053 | `gsap.registerPlugin(ScrollTrigger)` before any usage. | CLEAN |
| 9-10 | **Image paths** | All | All `src="../../images/template-images/..."` reference valid files. | CLEAN |
| 1 | **No pinned slides** | — | No ScrollTrigger pin used. | N/A |
| 2 | **No SplitType** | — | No SplitType used. | N/A |
| 5 | **No observer .visible pattern** | — | Not used. | N/A |

**BUG 1 — Missing Lenis+ScrollTrigger sync (line ~1050)**
- Lenis scroll events are not synced with ScrollTrigger. Missing `lenis.on('scroll', ScrollTrigger.update)` and `gsap.ticker.add`.
- **Fix:** After line 1049, add:
  ```js
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add(time => lenis.raf(time * 1000));
  gsap.ticker.lagSmoothing(0);
  ```
  And remove the `requestAnimationFrame(raf)` loop (lines 1045-1049).

**BUG 2 — Before/After slider clips wrong image (line 1237-1249)**
- `ba-after` image has CSS class `ba-after` with rule `clip-path:inset(0 50% 0 0)` (line 413), meaning the "after" image is clipped. JS then updates the "after" clip-path. But semantically the "before" should be the clipped overlay. The CSS has `.ba-after{clip-path:inset(0 50% 0 0)}` but JS clips the `.ba-after` element — this is internally consistent, just the naming is inverted (the element named "ba-after" is actually rendered as the "before" overlay). Not a visual bug, but confusing naming.
- **Verdict:** Works correctly, just confusing. CLEAN functionally.

**ACTUAL STATUS: 1 BUG (Lenis sync missing)**

---

## Template 7 (Emergency/Dark) — 2 BUGS

| # | Check | Status |
|---|-------|--------|
| 1-2, 5-6, 8 | N/A checks | CLEAN |
| 7 | registerPlugin order | Line 1019: `gsap.registerPlugin(ScrollTrigger)` — BUT ScrollTrigger is used at line 1015-1016 (`ScrollTrigger.update`, `lenis.on('scroll', ScrollTrigger.update)`) BEFORE registerPlugin. |
| 9-10 | Image paths | CLEAN — all reference valid files |

**BUG 1 — Lenis double-raf (line 1013-1016)**
- Line 1013: `requestAnimationFrame(raf)` loop drives Lenis.
- Line 1016: `gsap.ticker.add(time => lenis.raf(time * 1000))` ALSO drives Lenis.
- **Result:** Lenis `raf()` is called twice per frame, causing jittery/double-speed smooth scroll.
- **Fix:** Remove lines 1013-1014 (the `requestAnimationFrame` loop). Keep only the `gsap.ticker.add` approach.

**BUG 2 — registerPlugin AFTER ScrollTrigger usage (lines 1015 vs 1019)**
- Line 1015: `lenis.on('scroll', ScrollTrigger.update)` — references ScrollTrigger.
- Line 1019: `gsap.registerPlugin(ScrollTrigger)` — registered AFTER first reference.
- ScrollTrigger is already loaded as a global from the CDN, so `.update` exists. But the plugin is not formally registered with GSAP until line 1019, which can cause issues with GSAP's internal plugin tracking.
- **Fix:** Move `gsap.registerPlugin(ScrollTrigger)` to line 1011 (before any ScrollTrigger usage).

**BUG 3 — No reduced-motion check for Lenis (line 1012)**
- Lenis is initialized unconditionally (line 1012). The `prefersReduced` check (line 1021) only gates GSAP animations.
- **Fix:** Wrap Lenis initialization in `if(!prefersReduced){...}`.

---

## Template 8 (Minimalist/Clean) — 1 BUG

| # | Check | Status |
|---|-------|--------|
| 3 | Lenis double-raf | Lines 930-935 use `requestAnimationFrame` loop. Lines 942-943 use `gsap.ticker.add`. **BOTH present.** |
| 4 | opacity:0 + reduced-motion | Lines 72-80 have wildcard `*` reduced-motion override for transitions/animations. Lines 504-506 set `.fade-up`, `.fade-in`, `.scale-in` to `opacity:1`. GSAP uses `fromTo` with `opacity:0`. Reduced-motion path (lines 1059-1064) explicitly sets `opacity:1` and `transform:none`. | CLEAN |
| 7 | registerPlugin order | Line 938. Lenis ScrollTrigger sync at 942 is AFTER registerPlugin. | CLEAN |
| 9-10 | Image paths | CLEAN — all valid |

**BUG 1 — Lenis double-raf (lines 930-935 + 942-943)**
- Line 930-934: `requestAnimationFrame` loop calls `lenis.raf(time)`.
- Line 943: `gsap.ticker.add(time => lenis.raf(time * 1000))` ALSO calls `lenis.raf()`.
- **Fix:** Remove the `requestAnimationFrame` loop (lines 930-934). Keep only `gsap.ticker.add`.

---

## Template 9 (Neon/Cyberpunk) — 1 BUG

| # | Check | Status |
|---|-------|--------|
| 3 | Lenis double-raf | Lines 1506-1510 use `requestAnimationFrame`. Lines 1513-1514 use `gsap.ticker.add`. **BOTH present.** |
| 4 | opacity:0 + reduced-motion | Lines 1059-1066 have wildcard override. GSAP uses `gsap.from` (not `fromTo`), so initial CSS state is `opacity:1` and GSAP animates FROM `opacity:0`. Reduced-motion block at 1059 prevents animations. | CLEAN |
| 7 | registerPlugin order | Line 1519, but `ScrollTrigger.update` referenced at 1513. Same CDN-global issue as T7, but less critical since ScrollTrigger object exists. | Minor |
| 9-10 | Image paths | CLEAN — all valid |

**BUG 1 — Lenis double-raf (lines 1506-1510 + 1513-1514)**
- Same pattern: both `requestAnimationFrame` loop AND `gsap.ticker.add` drive Lenis.
- **Fix:** Remove lines 1506-1510 (the `requestAnimationFrame` loop). Keep `gsap.ticker.add` at line 1514.

---

## Template 10 (Rustic/Warm) — CLEAN

| # | Check | Status |
|---|-------|--------|
| 3 | Lenis double-raf | Lines 1562-1564 use `requestAnimationFrame` loop only. No `gsap.ticker.add`. | CLEAN |
| 4 | opacity:0 + reduced-motion | Lines 100-111 have full reduced-motion override covering `.fade-up`, `.service-card`, `.review-card`, `.process-step`, `.gallery-item`. CSS sets them to `opacity:1` at lines 218, 552-553, 777, 832-833, 923-924. GSAP uses `gsap.to` to animate TO final state from CSS initial. | CLEAN |
| 7 | registerPlugin order | Line 1568 before any ScrollTrigger usage. | CLEAN |
| 9-10 | Image paths | CLEAN — all valid |
| 1-2, 5-6, 8 | N/A checks | Not applicable |

**NOTE:** T10 does NOT sync Lenis with ScrollTrigger (no `lenis.on('scroll', ScrollTrigger.update)`). This means ScrollTrigger may not fire correctly with smooth scroll. Same issue as T6.

**Recommended fix for T10:** Add after line 1564:
```js
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add(time => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);
```
And remove the `requestAnimationFrame` loop.

---

## Summary

| Template | Status | Bugs |
|----------|--------|------|
| **T6** | 1 bug | Missing Lenis-ScrollTrigger sync |
| **T7** | 3 bugs | Lenis double-raf, registerPlugin order, no reduced-motion for Lenis |
| **T8** | 1 bug | Lenis double-raf |
| **T9** | 1 bug | Lenis double-raf |
| **T10** | 1 bug | Missing Lenis-ScrollTrigger sync |

**All image paths valid.** No SplitType conflicts, no pinned slides, no `.visible` observer pattern, no z-index issues found in any template.
