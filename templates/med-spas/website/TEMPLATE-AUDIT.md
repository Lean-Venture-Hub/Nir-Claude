# Med-Spa Templates Scroll/Animation & Image Audit

**Date:** 2026-03-14
**Templates audited:** 1-5
**Available images:** hero.jpg, botox.jpg, facial.jpg, laser.jpg, body-contouring.jpg, microneedling.jpg, iv-therapy.jpg, skin-tightening.jpg, team.jpg, treatment-room.jpg

---

## Template 1 — `template_example-1.html`

### BUG: Lenis double-raf (Check #3)
**Line 1485-1492** — Both `requestAnimationFrame(raf)` loop AND `gsap.ticker.add` drive `lenis.raf()`. Pick one.
```
FIX: Remove lines 1485-1489 (the requestAnimationFrame loop). Keep only gsap.ticker.add (line 1492).
```

### BUG: Missing CSS initial opacity:0 for animated elements (Check #4/#6)
**Lines 1503-1506, 1509** — Hero elements are animated `to` opacity:1 with `gsap.set` for y:30, but there is NO CSS `opacity:0` initial state on `.hero-eyebrow`, `.hero h1`, `.hero-sub`, `.hero-btns`. This means GSAP `.to()` starts from current CSS opacity (1), so the opacity animation does nothing. Same for `.trust-item` (line 465 has `transform:translateY(20px)` but no `opacity:0`), `.service-card`, `.about-content`, `.gallery-item`, `.testimonial-card`, `.process-step`.
```
FIX: Add to CSS:
.hero-eyebrow, .hero h1, .hero-sub, .hero-btns,
.trust-item, .service-card, .about-content,
.gallery-item, .testimonial-card, .process-step { opacity: 0; }

AND add to @media(prefers-reduced-motion:reduce):
.hero-eyebrow, .hero h1, .hero-sub, .hero-btns,
.trust-item, .service-card, .about-content,
.gallery-item, .testimonial-card, .process-step { opacity: 1 !important; transform: none !important; }
```

### BUG: registerPlugin order (Check #7)
**Line 1491** — `ScrollTrigger.update` is referenced at line 1491 inside Lenis setup, but `gsap.registerPlugin(ScrollTrigger)` doesn't happen until line 1497. ScrollTrigger is loaded via CDN so the global exists, but registering after usage is fragile.
```
FIX: Move gsap.registerPlugin(ScrollTrigger) to line 1478 (before any ScrollTrigger usage).
```

### Images: CLEAN
All `src` paths use `../../images/template-images/` + valid filenames (hero.jpg, botox.jpg, laser.jpg, facial.jpg, body-contouring.jpg, microneedling.jpg, iv-therapy.jpg, skin-tightening.jpg, team.jpg, treatment-room.jpg). All exist.

---

## Template 2 — `template_example-2.html`

### BUG: Lenis double-raf (Check #3)
**Lines 1047-1050** — Both `requestAnimationFrame(raf)` loop AND `gsap.ticker.add` drive `lenis.raf()`.
```
FIX: Remove lines 1047-1048 (the raf loop). Keep only gsap.ticker.add (line 1050).
```

### BUG: registerPlugin order (Check #7)
**Lines 1049-1055** — `ScrollTrigger.update` used at line 1049, but `gsap.registerPlugin(ScrollTrigger)` at line 1055.
```
FIX: Move gsap.registerPlugin(ScrollTrigger) before Lenis setup (before line 1045).
```

### CLEAN on other checks:
- Uses `gsap.from()` throughout, which sets initial state automatically — no CSS opacity:0 needed.
- No pinned slides, no SplitType, no `.visible` pattern.
- Reduced motion CSS at line 50-52 covers universal animation/transition override.
- All image paths valid.

---

## Template 3 — `template_example-3.html`

### BUG: Lenis double-raf (Check #3)
**Lines 1053-1064** — Both `requestAnimationFrame(raf)` loop (lines 1053-1057) AND `gsap.ticker.add` (line 1064) drive `lenis.raf()`.
```
FIX: Remove lines 1053-1057 (the raf loop). Keep only gsap.ticker.add (line 1064).
```

### BUG: Lenis runs without reduced-motion check
**Lines 1048-1065** — Lenis is initialized unconditionally. The `prefersReduced` check is at line 1068, AFTER Lenis is already running. Lenis should be gated.
```
FIX: Wrap Lenis init (lines 1048-1065) in: if(!prefersReduced){ ... }
```

### BUG: CSS `.reveal` / `.reveal-scale` have no `opacity:0` (Check #4/#6)
**Line 558-559** — `.reveal{transform:translateY(30px)}` and `.reveal-scale{transform:scale(.94)}` but NO `opacity:0`. The GSAP `fromTo` at lines 1083-1109 starts from `opacity:0`, but since CSS doesn't set it, there's a visible flash of un-transformed content before GSAP initializes.
```
FIX: Change line 558-559 to:
.reveal{opacity:0;transform:translateY(30px)}
.reveal-scale{opacity:0;transform:scale(.94)}

AND add inside @media(prefers-reduced-motion:reduce) (line 115-118):
.reveal,.reveal-scale{opacity:1!important;transform:none!important}
```

### CLEAN on other checks:
- Uses `gsap.fromTo()` for most animations (safe).
- `gsap.registerPlugin(ScrollTrigger)` at line 1060 — before any ScrollTrigger usage in animation code (hero animation at 1073 uses it correctly).
- No pinned slides, no SplitType, no `.visible` pattern.
- All image paths valid.

---

## Template 4 — `template_example-4.html`

### CLEAN
- **Lenis (Check #3):** Uses ONLY `gsap.ticker.add` (line 1883), no `requestAnimationFrame` loop. Correct.
- **registerPlugin (Check #7):** `gsap.registerPlugin(ScrollTrigger)` at line 1888, after Lenis uses `ScrollTrigger.update` at 1882. Same fragile order, but since it's `gsap.from()` throughout, the global is loaded from CDN and works.
- **Reduced motion (Check #4):** Reduced motion CSS at lines 1439-1451. Lenis gated behind `!prefersReducedMotion` (line 1874).
- **Uses `gsap.from()`** throughout — sets initial state automatically, no CSS `opacity:0` needed.
- **No pinned slides, SplitType, `.visible` pattern.**
- **All image paths valid.**

### MINOR: registerPlugin order
**Line 1882 vs 1888** — Same pattern as templates 1-2. `ScrollTrigger.update` referenced before `registerPlugin`. Works due to CDN global but not best practice.
```
FIX: Move gsap.registerPlugin(ScrollTrigger) before line 1882.
```

---

## Template 5 — `template_example-5.html`

### BUG: Missing CSS `opacity:0` on GSAP-animated elements (Check #4/#6)
**Lines 109-112** — `.gs-fade`, `.gs-scale`, `.gs-left`, `.gs-right` set `transform` but NO `opacity:0`. The JS uses `gsap.to()` to animate `opacity:1` (lines 997-1021), which means elements start at CSS opacity:1 — the fade-in does nothing.
```
FIX: Change lines 109-112 to:
.gs-fade{opacity:0;transform:translateY(28px)}
.gs-scale{opacity:0;transform:scale(0.95)}
.gs-left{opacity:0;transform:translateX(-40px)}
.gs-right{opacity:0;transform:translateX(40px)}

Already handled by reduced-motion at lines 949-953 (sets opacity:1, transform:none) — GOOD.
```

### BUG: Lenis double-raf (Check #3)
**Lines 944-945** — Uses `requestAnimationFrame(raf)` loop but no `gsap.ticker.add`. This is actually fine (single driver). However, Lenis is not synced with ScrollTrigger — missing `lenis.on('scroll', ScrollTrigger.update)` and no GSAP ticker sync.
```
FIX: Add after line 945:
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add(time => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);
And remove lines 944-945 (the raf loop).
```

### BUG: Lenis not gated behind reduced-motion
**Line 943** — Lenis initializes unconditionally. The `prefersReduced` check at line 948 returns early, but Lenis is already running.
```
FIX: Wrap Lenis init in: if(!prefersReduced){ ... } before line 943.
```

### BUG: Hero content `.gs-fade` initial state invisible without JS
**Line 596** — `.hero-content.gs-fade` has `.gs-fade` class. If JS fails, hero content stays invisible (once opacity:0 fix above is applied). The JS at line 983 animates it, but this is the hero — critical content.
```
FIX: Add a <noscript><style>.gs-fade,.gs-scale,.gs-left,.gs-right{opacity:1!important;transform:none!important}</style></noscript> in the <head>.
```

### CLEAN on other checks:
- All image paths valid.
- No pinned slides, SplitType, `.visible` pattern.
- `gsap.registerPlugin(ScrollTrigger)` at line 956 — correctly before all ScrollTrigger usage.

---

## Summary Table

| # | Check | T1 | T2 | T3 | T4 | T5 |
|---|-------|----|----|----|----|-----|
| 1 | Pinned slides fade-out | N/A | N/A | N/A | N/A | N/A |
| 2 | SplitType conflicts | N/A | N/A | N/A | N/A | N/A |
| 3 | Lenis double-raf | **BUG** | **BUG** | **BUG** | CLEAN | **BUG** |
| 4 | opacity:0 + reduced-motion | **BUG** | CLEAN | **BUG** | CLEAN | **BUG** |
| 5 | CSS .visible pattern | N/A | N/A | N/A | N/A | N/A |
| 6 | Animation initial state | **BUG** | CLEAN | **BUG** | CLEAN | **BUG** |
| 7 | registerPlugin order | **BUG** | **BUG** | CLEAN | minor | CLEAN |
| 8 | z-index overlapping slides | N/A | N/A | N/A | N/A | N/A |
| 9 | Image paths | CLEAN | CLEAN | CLEAN | CLEAN | CLEAN |
| 10 | Broken image refs | CLEAN | CLEAN | CLEAN | CLEAN | CLEAN |
| - | Lenis reduced-motion gate | OK | OK | **BUG** | OK | **BUG** |
