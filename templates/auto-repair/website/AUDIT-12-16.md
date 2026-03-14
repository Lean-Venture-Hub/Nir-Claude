# Auto-Repair Templates 12-16 Scroll/Animation & Image Audit

**Available images:** `exterior.jpg`, `hero.jpg`, `service-brakes.jpg`, `service-diagnostics.jpg`, `service-engine.jpg`, `service-oil.jpg`, `service-tires.jpg`, `team.jpg`

---

## Template 12 — 2 bugs

| # | Check | Line | Bug | Fix |
|---|-------|------|-----|-----|
| 2 | SplitType conflict | L144,347-349 | CSS `.hero-headline .word{display:inline-block}` manually styles `.word` elements, and SplitType also creates `.word` elements on same `#heroHeadline` (L712). Not a fatal conflict since CSS just sets `display:inline-block` which SplitType words already have, but the manual CSS rule is redundant and fragile. | **LOW**: Remove L144 `.hero-headline .word{display:inline-block}` — SplitType handles it |
| 4 | opacity:0 + reduced-motion | L112-116 | `.gsap-fade`, `.gsap-fade-left`, `.gsap-fade-right`, `.gsap-scale` all start `opacity:0`. The reduced-motion `@media` block (L58-65) only sets `animation-duration`/`transition-duration` to 0 — it does NOT reset `opacity:0` on `.gsap-*` classes. JS handles it (L694), but if JS fails, elements are invisible. | Add to `@media(prefers-reduced-motion:reduce)`: `.gsap-fade,.gsap-fade-left,.gsap-fade-right,.gsap-scale{opacity:1!important;transform:none!important}` |
| 9 | Image paths | — | All paths `../../images/template-images/X.jpg` — filenames: `hero.jpg`, `service-engine.jpg`, `service-oil.jpg`, `service-brakes.jpg`, `service-diagnostics.jpg`, `service-tires.jpg`, `team.jpg`. All exist. **OK** |

**Checks 1,3,5,6,7,8,10: CLEAN** — No pinned slides, no Lenis, no observer `.visible` pattern, `registerPlugin` before usage (L706), no z-index issues, no broken image refs.

---

## Template 13 — 2 bugs

| # | Check | Line | Bug | Fix |
|---|-------|------|-----|-----|
| 4 | opacity:0 + reduced-motion | L106-108 | `.gsap-fade{opacity:0}`, `.gsap-scale{opacity:0}`, `.gsap-char{opacity:0}` — reduced-motion block (L67-74) only resets `animation`/`transition` durations, NOT the opacity. JS handles it (L1070-1073), but CSS-only fallback is missing. | Add to `@media(prefers-reduced-motion:reduce)`: `.gsap-fade,.gsap-scale,.gsap-char{opacity:1!important;transform:none!important}` |
| 7 | registerPlugin order | L1081 | `gsap.registerPlugin(ScrollTrigger)` is inside `initGSAP()` which waits for script load. Scripts are `defer`, so GSAP/ScrollTrigger load before DOMContentLoaded. But `initGSAP` uses `setTimeout` polling — safe enough. | **CLEAN** (defensive but works) |
| 9 | Image paths | — | All paths use `../../images/template-images/` — filenames: `hero.jpg`, `service-oil.jpg`, `service-engine.jpg`, `service-brakes.jpg`, `service-tires.jpg`, `service-diagnostics.jpg`, `team.jpg`. All exist. **OK** |

**Checks 1,2,3,5,6,8,10: CLEAN** — No pinned slides, no SplitType on manually-spanned elements, no Lenis, no `.visible` pattern, no z-index issues.

---

## Template 14 — 4 bugs

| # | Check | Line | Bug | Fix |
|---|-------|------|-----|-----|
| 1 | Pinned slides must fade out | L770-782 (stats), L860-871 (reviews) | Stats slides use `s.classList.remove('active')` + `gsap.to(opacity:0)` — **OK**. Review slides do the same — **OK**. | **CLEAN** |
| 2 | SplitType conflict | L138-139 | CSS: `.hero-headline .word{display:inline-block;overflow:hidden}` and `.hero-headline .char{display:inline-block;opacity:0;transform:translateY(100%)}` — these manually set styles on `.word` and `.char`. SplitType (L721) creates these elements. The manual `.char{opacity:0;transform:translateY(100%)}` duplicates what GSAP `fromTo` sets (L722-724). If SplitType fails to load, orphan CSS leaves text invisible. | Remove L139 `.hero-headline .char{display:inline-block;opacity:0;transform:translateY(100%)}` — let GSAP `fromTo` handle initial state. Keep `.word` rule for `overflow:hidden`. |
| 4 | opacity:0 + reduced-motion | L136,140-141,147,165 | `hero-eyebrow{opacity:0}`, `.hero-sub{opacity:0}`, `.hero-actions{opacity:0}`, `.hero-trust{opacity:0}`, `.stats-conclusion{opacity:0}`, `.reviews-count{opacity:0}`. Reduced-motion block (L63-73) doesn't reset these. It resets `[data-speed]` and `.pin-spacer` but NOT opacity:0 elements. | Add to `@media(prefers-reduced-motion:reduce)`: `.hero-eyebrow,.hero-sub,.hero-actions,.hero-trust,.hero-headline .char,.stat-slide,.stats-conclusion,.reviews-count{opacity:1!important;transform:none!important}` |
| 8 | z-index on overlapping slides | L794 | `statsConclusion` gets `zIndex:5` via `gsap.set` — **OK**. `reviewsCount` gets `zIndex:5` via `gsap.set` (L881) — **OK**. | **CLEAN** |
| 10 | Broken image ref | L590 | `../../images/template-images/exterior.jpg` — this file **EXISTS** in the images dir. **OK** |

**Actual bugs: 2** (SplitType `.char` conflict, opacity:0 reduced-motion gap)

---

## Template 15 — 3 bugs

| # | Check | Line | Bug | Fix |
|---|-------|------|-----|-----|
| 4 | opacity:0 + reduced-motion | L83-84 | `.gsap-fade{opacity:0;transform:translateY(40px)}`, `.gsap-scale{opacity:0;transform:scale(0.9)}`. Reduced-motion block (L63-72) only addresses `.parallax-layer` and `.floating-shape` — does NOT reset `.gsap-fade` or `.gsap-scale` opacity. JS handles it for `.gsap-fade` (L1121-1124) but only in the forEach loop which may miss some. | Add to `@media(prefers-reduced-motion:reduce)`: `.gsap-fade,.gsap-scale{opacity:1!important;transform:none!important}` |
| 9 | Image paths | L729,739 | `service-transmission.jpg` and `service-ac.jpg` — these files do **NOT EXIST** in the images directory. Available files are: `exterior.jpg`, `hero.jpg`, `service-brakes.jpg`, `service-diagnostics.jpg`, `service-engine.jpg`, `service-oil.jpg`, `service-tires.jpg`, `team.jpg`. | Replace `service-transmission.jpg` with `service-diagnostics.jpg` (or another existing image). Replace `service-ac.jpg` with `service-engine.jpg` (or another existing image). |
| 10 | Broken image refs | L729,739 | Same as above — `service-transmission.jpg` and `service-ac.jpg` will show broken images. | See fix above |

**Checks 1,2,3,5,6,7,8: CLEAN** — No pinned slides, SplitType removes `gsap-fade` class before splitting (L1108, good practice), Lenis uses `gsap.ticker.add` only (no double-raf), `registerPlugin` at L1030 before usage, no `.visible` pattern.

---

## Template 16 — 4 bugs

| # | Check | Line | Bug | Fix |
|---|-------|------|-----|-----|
| 2 | SplitType conflict | L202,880-881 | CSS: `.hero h1 .word{display:inline-block;opacity:0}`. SplitType (L880) creates `.word` elements, then L881 manually adds `.word` class (`split.words.forEach(w=>w.classList.add('word'))`). This is redundant (SplitType already creates elements with the right class) and the CSS `opacity:0` on `.word` means words start invisible. GSAP animates to `opacity:1` (L883-888). If GSAP or SplitType fails, headline is invisible. | Remove the manual class add at L881 (SplitType already assigns the class). The CSS `.word{opacity:0}` is the intended initial state — but add reduced-motion override (see below). |
| 4 | opacity:0 + reduced-motion | L183,202,203,204,302-305 | `.hero-trust{opacity:0}`, `.hero h1 .word{opacity:0}`, `.hero-subtitle{opacity:0}`, `.hero-cta-row{opacity:0}`, `.review-card{opacity:0;transform:translateY(-60px) rotate(-3deg)}`, `.feature-card{opacity:0;transform:scale(0)}`, `.blog-card{opacity:0;transform:translateY(40px)}`, `.service-card{clip-path:polygon(0 0, 0 0, 0 100%, 0 100%)}`, `.services-inner{clip-path:polygon(0 0, 0 0, 0 100%, 0 100%)}`. Reduced-motion block (L62-75) covers `.review-card,.feature-card,.blog-card,.service-card` **OK**, and hero elements **OK**. But `.services-inner{clip-path}` (L222) is NOT covered. | Add to existing reduced-motion block: `.services-inner{clip-path:none!important}` |
| 6 | Animation initial state | L331-333 | `.feature-card{opacity:0;transform:scale(0)}` — `scale(0)` is extremely aggressive. If GSAP fails, features section is completely invisible AND takes no space visually (scale 0). | Change to `transform:scale(0.9)` for a safer initial state |
| 9 | Image paths | L544,546,555,556 | `service-transmission.jpg` and `service-ac.jpg` — these files do **NOT EXIST**. Same issue as template 15. | Replace `service-transmission.jpg` with `service-diagnostics.jpg`. Replace `service-ac.jpg` with `service-engine.jpg`. |

**Checks 1,3,5,7,8: CLEAN** — No pinned slides (clip-path reveals, not pin), Lenis uses `gsap.ticker.add` only, no `.visible` observer pattern, `registerPlugin` at L825 before usage.

---

## Summary

| Template | Status | Bug Count | Critical |
|----------|--------|-----------|----------|
| 12 | 2 bugs | 2 | 1 (reduced-motion opacity) |
| 13 | 1 bug | 1 | 1 (reduced-motion opacity) |
| 14 | 2 bugs | 2 | 1 (reduced-motion opacity), 1 (SplitType .char) |
| 15 | 2 bugs | 2 | **1 BROKEN IMAGES** (service-transmission.jpg, service-ac.jpg), 1 (reduced-motion) |
| 16 | 3 bugs | 3 | **1 BROKEN IMAGES** (service-transmission.jpg, service-ac.jpg), 1 (reduced-motion), 1 (scale(0) too aggressive) |

**Most urgent:** Templates 15 and 16 reference `service-transmission.jpg` and `service-ac.jpg` which do not exist and will show broken images.

**Universal issue:** All 5 templates lack `@media(prefers-reduced-motion)` CSS overrides for `opacity:0` initial states on GSAP-animated elements.
