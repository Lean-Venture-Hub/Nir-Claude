# HVAC Templates 6-10 Audit Report

**Available images:** ac-install.jpg, commercial.jpg, ductwork.jpg, emergency.jpg, furnace-repair.jpg, heat-pump.jpg, hero.jpg, maintenance.jpg, team.jpg, thermostat.jpg

---

## Template 6 — 3 BUGS

| # | Rule | Line(s) | Bug | Fix |
|---|------|---------|-----|-----|
| 1 | **opacity:0 + reduced-motion** | CSS L120-123 | `.gs-fade`, `.gs-fade-right`, `.gs-fade-left`, `.gs-scale` all lack `opacity:0` in their CSS initial state (only `transform` is set). GSAP `gsap.to()` animates TO `opacity:1` but the CSS never sets `opacity:0` — elements are visible before GSAP loads, causing a flash. | Add `opacity:0` to all four classes: `.gs-fade{opacity:0;transform:translateY(40px)}` etc. |
| 2 | **opacity:0 + reduced-motion** | CSS L74-81 | The `@media(prefers-reduced-motion:reduce)` rule kills animations/transitions but does NOT override the `opacity:0` that should be added (per bug #1). After fixing bug #1, elements will be invisible in reduced-motion. | Add `.gs-fade,.gs-fade-right,.gs-fade-left,.gs-scale{opacity:1!important;transform:none!important}` inside the `@media(prefers-reduced-motion:reduce)` block. |
| 3 | **Lenis double-raf** | JS L1052-1056 | Uses BOTH `requestAnimationFrame(raf)` loop AND `gsap.ticker.add(time=>lenis.raf(time*1000))`. Lenis gets `.raf()` called twice per frame. | Remove the `function raf(time){lenis.raf(time);requestAnimationFrame(raf)} requestAnimationFrame(raf);` loop. The `gsap.ticker.add` call alone is sufficient. |

**Image paths:** CLEAN — all 10 `src` paths resolve to existing files in `../../images/template-images/`.

---

## Template 7 — 2 BUGS

| # | Rule | Line(s) | Bug | Fix |
|---|------|---------|-----|-----|
| 1 | **CSS .visible pattern** | CSS L69-76 | `.reveal`, `.reveal-left`, `.reveal-right`, `.reveal-scale` all lack `opacity:0` in their initial CSS state. The CSS defines `.reveal.visible{opacity:1}` but the initial state only sets `transform`, not `opacity:0`. GSAP `fromTo` animates from `opacity:0` which works, but without CSS `opacity:0`, elements flash visible before JS executes. | Add `opacity:0` to `.reveal`, `.reveal-left`, `.reveal-right`, `.reveal-scale` initial CSS rules. |
| 2 | **CSS .visible pattern** | CSS L69-76 | The `.visible` CSS rules exist (`opacity:1;transform:...`) but are never used — GSAP handles all reveals. These dead CSS rules plus the `stagger-*` transition-delay classes (L82-87) are leftover from an observer-based pattern. Not a runtime bug, but misleading. | Remove `.visible` CSS rules and `stagger-*` delay classes OR remove the GSAP reveals and use an IntersectionObserver with `.visible` instead — pick one pattern. |

**Image paths:** CLEAN — all paths valid. Uses `background:url(...)` for hero (L170) and `<img src>` for all others. All resolve to existing files.

---

## Template 8 — 3 BUGS

| # | Rule | Line(s) | Bug | Fix |
|---|------|---------|-----|-----|
| 1 | **opacity:0 + reduced-motion** | CSS L141-144 | `.gs-fade{transform:translateY(36px)}`, `.gs-scale{transform:scale(0.94)}`, `.gs-fade-right`, `.gs-fade-left` all lack `opacity:0`. GSAP animates to `opacity:1` but initial CSS never hides them — elements flash visible before JS runs. | Add `opacity:0` to all four classes. |
| 2 | **Lenis double-raf** | JS L1023-1027 + L1034-1036 | Uses BOTH `function raf(time){lenis.raf(time);requestAnimationFrame(raf)} requestAnimationFrame(raf);` AND `gsap.ticker.add((time)=>{lenis.raf(time*1000)})`. Double `.raf()` calls per frame. | Remove the `requestAnimationFrame` loop. Keep only `gsap.ticker.add`. |
| 3 | **registerPlugin order** | JS L1030 vs L1033 | `gsap.registerPlugin(ScrollTrigger)` is called at L1030, but `lenis.on('scroll', ScrollTrigger.update)` is called at L1033. The `ScrollTrigger.update` reference at L1033 works because `ScrollTrigger` is loaded as a global, but `registerPlugin` should logically come before any ScrollTrigger usage. Currently it works — **low severity** but note that `lenis.on('scroll', ScrollTrigger.update)` at L1033 runs before `registerPlugin` at L1030 in code order is fine since the Lenis event fires asynchronously. | No code change strictly required, but moving `registerPlugin` before the Lenis setup is cleaner. |

**Image paths:** CLEAN — all valid.

---

## Template 9 — CLEAN (0 bugs)

All 10 checks pass:

- **No pinned slides** — no ScrollTrigger pin
- **No SplitType** — not used
- **Lenis:** Uses only `gsap.ticker.add` (L1047), no double-raf
- **opacity:0 + reduced-motion:** Has explicit reduced-motion override at L82-85 that sets `.reveal,.reveal-up,.reveal-left,.reveal-right,.reveal-scale{opacity:1!important;transform:none!important}` plus individual element overrides
- **CSS .visible pattern:** Uses `reveal-left`/`reveal-right` classes but GSAP handles all animation via `gsap.from()` (not CSS `.visible` toggle) — consistent single pattern
- **Animation initial state:** Uses `gsap.from()` which means GSAP sets initial state programmatically — no CSS `opacity:0` needed
- **registerPlugin order:** L1052 — correct, after Lenis setup but before ScrollTrigger usage
- **z-index:** No overlapping slides
- **Image paths:** All 10 images reference `../../images/template-images/{name}.jpg` — all exist
- **No broken image refs**

---

## Template 10 — 2 BUGS

| # | Rule | Line(s) | Bug | Fix |
|---|------|---------|-----|-----|
| 1 | **opacity:0 + reduced-motion** | CSS L120-122 | `.gsap-fade{transform:translateY(40px)}`, `.gsap-scale{transform:scale(0.9)}`, `.gsap-slide{transform:translateX(-40px)}` all lack `opacity:0`. GSAP `fromTo` at L949-973 explicitly sets `opacity:0` in the `from` values, which works — but between page load and GSAP executing, elements are visible at wrong transform, then snap to `opacity:0`, then animate in. This causes a layout flash. | Add `opacity:0` to `.gsap-fade`, `.gsap-scale`, `.gsap-slide` in CSS. The `@media(prefers-reduced-motion:reduce)` block at L78 already overrides these classes — it will work after adding `opacity:0`. |
| 2 | **Lenis + ScrollTrigger sync** | JS L915-917 | `lenis.on('scroll', ScrollTrigger.update)` at L915 references `ScrollTrigger.update` before `gsap.registerPlugin(ScrollTrigger)` at L921. This works because `ScrollTrigger` is a global from the CDN, but the reference to `.update` in the Lenis callback fires asynchronously so it's fine at runtime. **Low severity** — code order is misleading but not broken. | Move `gsap.registerPlugin(ScrollTrigger)` above the Lenis block for clarity. |

**Image paths:** CLEAN — all valid.

---

## Summary

| Template | Status | Bug Count | Critical |
|----------|--------|-----------|----------|
| 6 | **3 bugs** | 3 | opacity:0 missing, Lenis double-raf |
| 7 | **2 bugs** | 2 | opacity:0 missing, dead .visible CSS |
| 8 | **3 bugs** | 3 | opacity:0 missing, Lenis double-raf, registerPlugin order |
| 9 | **CLEAN** | 0 | -- |
| 10 | **2 bugs** | 2 | opacity:0 missing, registerPlugin order |

**Most common issue:** Missing `opacity:0` in CSS initial state for animated elements (templates 6, 7, 8, 10).
**Second most common:** Lenis double-raf (templates 6, 8).
**Image paths:** All 5 templates are CLEAN — no broken image references.
