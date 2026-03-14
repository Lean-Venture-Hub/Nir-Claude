# Med-Spa Templates 6-10 Audit Report

**Date:** 2026-03-14
**Scope:** Scroll/animation bugs + image issues across 10 checks

**Available images:** `hero.jpg`, `botox.jpg`, `facial.jpg`, `laser.jpg`, `body-contouring.jpg`, `microneedling.jpg`, `iv-therapy.jpg`, `skin-tightening.jpg`, `team.jpg`, `treatment-room.jpg`

---

## Template 6 — 3 BUGS

| # | Check | Line(s) | Bug | Fix |
|---|-------|---------|-----|-----|
| 1 | opacity:0 + reduced-motion | 243-263 | `.hero-eyebrow`, `.hero-subtitle`, `.hero-cta-row`, `.hero-scroll-indicator` have NO `opacity:0` in CSS but are animated with `gsap.to(opacity:1)` at L1112-1118. They need initial `opacity:0` **and** a reduced-motion override. Currently the reduced-motion block (L71-85) covers `.fade-up`, `.fade-in`, `.stagger-item`, `.hero-title .word` but **misses** these 4 hero elements. | Add `opacity:0` to `.hero-eyebrow`, `.hero-subtitle`, `.hero-cta-row`, `.hero-scroll-indicator` in CSS. Add them to the `@media(prefers-reduced-motion:reduce)` block with `opacity:1!important`. |
| 2 | SplitType conflict | 254-255 | `.hero-title .word-wrap` and `.hero-title .word` are manual `<span>` wrappers in HTML (L653-658). No SplitType loaded in this template. | **CLEAN** — no conflict (SplitType not used). However, the `.word` spans start with `transform:translateY(110%)` (L255) with no opacity — this is correct since the transform alone hides them. |
| 3 | Image paths | all | All `src="../../images/template-images/..."` paths reference files that exist. | **CLEAN** |

**Net: 1 real bug (missing opacity:0 initial state + reduced-motion override for 4 hero elements)**

---

## Template 7 — 2 BUGS

| # | Check | Line(s) | Bug | Fix |
|---|-------|---------|-----|-----|
| 1 | **Lenis double-raf** | 1447-1456 | Both `requestAnimationFrame(raf)` loop (L1447-1451) **AND** `gsap.ticker.add(...)` (L1455) call `lenis.raf()`. Double-driving Lenis causes janky/doubled scroll. | Remove the `requestAnimationFrame` loop (L1447-1451). Keep only `gsap.ticker.add`. |
| 2 | opacity:0 + reduced-motion | 946-947 | `.reveal` has `transform:translateY(40px)` but **no** `opacity:0` in CSS. The JS animates `opacity:1, y:0` with `gsap.to()` (L1551-1552), so initial opacity is implicitly 1 and the `gsap.to(opacity:1)` is a no-op — elements are visible before animation. The `.service-card` and `.gallery-item` classes also get `gsap.to(opacity:1, y:0)` but have no CSS `opacity:0`. | Add `opacity:0` to `.reveal`, `.service-card`, `.gallery-item` in CSS. The reduced-motion block (L959-969) already covers `.reveal` with `opacity:1; transform:none` — add `.service-card, .gallery-item` there too. |

**Image paths:** All CLEAN — reference existing files.
**registerPlugin order:** CLEAN — L1460, after Lenis but before ScrollTrigger usage at L1454 (ScrollTrigger.update is a reference, not a create, so this is acceptable).
**No pinned slides, no SplitType, no .visible pattern.**

---

## Template 8 — 2 BUGS

| # | Check | Line(s) | Bug | Fix |
|---|-------|---------|-----|-----|
| 1 | opacity:0 + reduced-motion | 555 | `.service-card-desc` has `opacity:0` in CSS (hover-reveal pattern). This is intentional for hover interaction, NOT a scroll animation — so it should NOT be overridden for reduced-motion. | **CLEAN** (hover pattern, acceptable). |
| 2 | opacity:0 + reduced-motion | 1150 | `.reveal-up` has `transform:translateY(40px)` but **no** `opacity:0` in CSS. JS does `gsap.from(el, {opacity:0, y:40})` (L1666) — `gsap.from` sets opacity to 0 at start then animates to current (1). This technically works but causes a flash: element is visible at opacity:1, then GSAP snaps it to 0 and animates up. | Add `opacity:0` to `.reveal-up` in CSS (L1150). Already covered in reduced-motion override at L1164. |
| 3 | `.service-card` + `.process-step` + `.testimonial-card` animation | 1674-1725 | These use `gsap.from(opacity:0)` but have **no** CSS `opacity:0`. Same flash-of-content risk. | Add `opacity:0` to `.service-card`, `.testimonial-card`, `.process-step` in CSS and add reduced-motion overrides. |

**Lenis:** CLEAN — only `gsap.ticker.add`, no double-raf.
**registerPlugin:** CLEAN — L1598, before first usage.
**Image paths:** All CLEAN.
**No pinned slides, no SplitType, no .visible pattern.**

---

## Template 9 — 3 BUGS

| # | Check | Line(s) | Bug | Fix |
|---|-------|---------|-----|-----|
| 1 | **Lenis double-raf** | 1629-1640 | Both `requestAnimationFrame(raf)` loop (L1629-1633) **AND** `gsap.ticker.add(...)` (L1637-1638) call `lenis.raf()`. | Remove the `requestAnimationFrame` loop (L1629-1633). Keep only `gsap.ticker.add`. |
| 2 | opacity:0 + reduced-motion | 145-147 | `.reveal` has `transform:translateY(30px)` but **no** `opacity:0` in CSS. JS animates `opacity:1, y:0` (L1721-1722). Elements start visible then jump. | Add `opacity:0` to `.reveal` in CSS (L145). Already has reduced-motion override at L1230-1233. |
| 3 | Hero initial states | 362-406 | `.hero__eyebrow`, `.hero__subtitle`, `.hero__cta` are animated to `opacity:1, y:0` via `gsap.to()` (L1697-1700) but have **no** `opacity:0` in CSS. The reduced-motion block (L1239-1244) correctly covers them with `opacity:1!important` — but the initial CSS `opacity:0` is missing, so without JS they'd be visible (no animation effect). | Add `opacity:0; transform:translateY(20px)` to `.hero__eyebrow`, `.hero__subtitle`, `.hero__cta` in CSS. |

**Image paths:** All CLEAN — all reference existing files.
**registerPlugin:** CLEAN — L1646, before usage.
**No pinned slides, no SplitType, no .visible pattern.**

---

## Template 10 — 1 BUG

| # | Check | Line(s) | Bug | Fix |
|---|-------|---------|-----|-----|
| 1 | opacity:0 + reduced-motion | 705-708 | `.reveal`, `.reveal-left`, `.reveal-right`, `.reveal-scale` have transforms but **no** `opacity:0` in CSS. JS animates `opacity:1` (L1286-1322). | Add `opacity:0` to all four classes. The JS reduced-motion fallback (L1253-1258) already handles it by setting `style.opacity='1'`, but CSS initial state is still missing. |

**Lenis:** CLEAN — only `gsap.ticker.add`, no double-raf.
**registerPlugin:** CLEAN — L1198, before first usage.
**Image paths:** All CLEAN.
**Reduced-motion:** Has both CSS `@media` block (L67-74) and JS fallback (L1253-1258). The CSS block is generic (kills all animation/transition) but doesn't explicitly reset the reveal classes — the JS fallback handles it.
**No pinned slides, no SplitType, no .visible pattern, no pinned gallery.**

---

## Summary

| Template | Status | Critical Bugs |
|----------|--------|---------------|
| **6** | 1 bug | Missing `opacity:0` initial + reduced-motion for hero elements |
| **7** | 2 bugs | **Double-raf** + missing `opacity:0` on reveal/card classes |
| **8** | 2 bugs | Missing `opacity:0` on `.reveal-up`, `.service-card`, `.testimonial-card`, `.process-step` |
| **9** | 3 bugs | **Double-raf** + missing `opacity:0` on `.reveal` + hero elements |
| **10** | 1 bug | Missing `opacity:0` on `.reveal*` classes |

**Common pattern across all 5:** Missing CSS `opacity:0` initial state for elements animated by GSAP. This causes a flash-of-visible-content before GSAP kicks in.

**Double-raf (templates 7 & 9):** Both `requestAnimationFrame` loop and `gsap.ticker.add` drive `lenis.raf()`. Remove the rAF loop.

**No issues found for:** Pinned slides fade-out, SplitType conflicts, .visible pattern, registerPlugin order, z-index on overlays, image paths, broken image refs.
