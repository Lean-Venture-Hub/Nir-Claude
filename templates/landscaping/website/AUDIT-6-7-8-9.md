# Landscaping Templates 6-9: Scroll/Animation & Image Audit

**Available images:** `hero.jpg`, `before.jpg`, `after.jpg`, `hardscape-patio.jpg`, `irrigation.jpg`, `landscape-lighting.jpg`, `lawn-care.jpg`, `outdoor-living.jpg`, `retaining-wall.jpg`, `team.jpg`

---

## Template 6 — BUGS FOUND

| # | Check | Line(s) | Bug | Fix |
|---|-------|---------|-----|-----|
| 3 | Lenis double-raf | 1693-1701 | Both `requestAnimationFrame(raf)` loop (L1693-1697) AND `gsap.ticker.add` (L1700) drive Lenis — double-update per frame | Remove the `requestAnimationFrame` loop; keep only `gsap.ticker.add` |
| 4 | opacity:0 + reduced-motion | 72-77 | `@media(prefers-reduced-motion:reduce)` at L71 does NOT override `clip-path` initial states like `.hero { clip-path: circle(0%) }` (L212), `.trust-bar { clip-path: polygon(0 0,0 0,0 100%,0 100%) }` (L386), `.services` (L427), `.before-after` (L521), `.portfolio` (L640), `.about` (L711), `.process` (L872) — these all start invisible. The `*` wildcard only handles animation/transition duration, but clip-path is not an animation — it's a static value. | Add to reduced-motion media query: `.hero, .trust-bar, .services, .before-after, .portfolio, .about, .process { clip-path: none !important; }` and `.review-card { clip-path: polygon(0 0,100% 0,100% 100%,0 100%) !important; }` |
| 5 | CSS .visible pattern | 829 | `.review-card` starts with `clip-path: polygon(50% 50%,...)` (L829) which is invisible, JS adds `.revealed` class (L1906). The reduced-motion block at L1979 adds `.revealed` to `.reveal-section` elements but review cards DO get `.revealed` at L1980 — OK. However, `.process` also starts invisible at L872 and its `.revealed` class IS set at L1979. **Actually OK — both paths covered.** | N/A |
| 7 | registerPlugin order | 1699-1704 | `gsap.ticker.add` uses `ScrollTrigger.update` at L1699 BEFORE `gsap.registerPlugin(ScrollTrigger)` at L1704. ScrollTrigger is loaded as a script tag so it's available globally, but `registerPlugin` should come first for safety. | Move `gsap.registerPlugin(ScrollTrigger)` to immediately after the IIFE opens (L1680), before any ScrollTrigger usage |
| 9 | Image paths | All | All `src="../../images/template-images/..."` paths reference: `hero.jpg`, `before.jpg`, `after.jpg`, `outdoor-living.jpg`, `hardscape-patio.jpg`, `lawn-care.jpg`, `retaining-wall.jpg`, `landscape-lighting.jpg`, `team.jpg` — **all exist** | CLEAN |

**Summary:** 2 real bugs (double-raf, registerPlugin order), 1 reduced-motion coverage issue (clip-path initial states not overridden).

---

## Template 7 — BUGS FOUND

| # | Check | Line(s) | Bug | Fix |
|---|-------|---------|-----|-----|
| 3 | Lenis double-raf | 1060-1063 | Same pattern: `requestAnimationFrame(raf)` loop at L1060 AND `gsap.ticker.add` at L1063. Lenis gets `.raf()` called twice per frame. | Remove the RAF loop; keep only `gsap.ticker.add` |
| 4 | opacity:0 + reduced-motion | 112-114 | `.reveal`, `.reveal-left`, `.reveal-right` all set `opacity:0` in CSS. The reduced-motion block at L592-596 correctly overrides these with `opacity:1; transform:none`. **OK.** | CLEAN |
| 7 | registerPlugin order | 1062-1068 | `lenis.on('scroll', ScrollTrigger.update)` at L1062 uses ScrollTrigger BEFORE `gsap.registerPlugin(ScrollTrigger)` at L1068. Again, works because script tag loads it globally, but technically wrong order. | Move `gsap.registerPlugin(ScrollTrigger)` before the Lenis setup block |
| 4b | opacity:0 reduced-motion | 209 | `.hero-scroll-line` has `animation: scrollPulse 2s infinite` (L208-209). Reduced-motion at L593 handles `animation-duration:0.01ms!important` which covers this. **OK.** | CLEAN |

**Summary:** 2 bugs (double-raf, registerPlugin order). Image paths all valid.

---

## Template 8 — BUGS FOUND

| # | Check | Line(s) | Bug | Fix |
|---|-------|---------|-----|-----|
| 3 | Lenis double-raf | 1069-1074 | Same double-raf pattern: `requestAnimationFrame(raf)` at L1070-1071 AND `gsap.ticker.add` at L1073. | Remove the RAF loop; keep only `gsap.ticker.add` |
| 4 | opacity:0 + reduced-motion | 178 | `.fade-up` starts `opacity:0` (L178). Reduced-motion at L79 overrides `.fade-up` to `opacity:1!important; transform:none!important`. **OK.** | CLEAN |
| 5 | CSS .visible pattern | 178-179 | `.fade-up` starts `opacity:0`, observer adds `.is-visible` (L1128). CSS rule `.fade-up.is-visible{opacity:1;transform:translateY(0)}` exists at L179. And reduced-motion at L79 forces `opacity:1`. **OK.** | CLEAN |
| 7 | registerPlugin order | 1072-1103 | `lenis.on('scroll', ScrollTrigger.update)` at L1072 BEFORE `gsap.registerPlugin(ScrollTrigger)` at L1103. | Move `gsap.registerPlugin(ScrollTrigger)` to right after Lenis instantiation, before any ScrollTrigger reference |
| 3b | Lenis double-raf detail | 1069-1074 | Lenis is created WITHOUT reduced-motion guard — if user prefers reduced motion, Lenis still runs smooth scroll. Other templates guard this. | Wrap Lenis creation in `if(!prefersReduced){}` block |

**Summary:** 2 bugs (double-raf, registerPlugin order), 1 accessibility issue (Lenis runs even with prefers-reduced-motion). Image paths all valid.

---

## Template 9 — BUGS FOUND

| # | Check | Line(s) | Bug | Fix |
|---|-------|---------|-----|-----|
| 2 | SplitType conflicts | 324-330, 1457-1462 | HTML has manual `<span class="word">` elements at L329 inside `.hero__title`, AND SplitType runs on `#heroTitle` with `types: 'lines, words'` at L1458. SplitType will create its own word spans inside the existing `.word` spans, causing nested redundant wrapping. | Remove the manual `<span class="word">` wrappers in HTML — let SplitType handle word splitting entirely |
| 3 | Lenis double-raf | 1405-1414 | Same pattern: `requestAnimationFrame(raf)` loop at L1405-1408 AND `gsap.ticker.add` at L1413. | Remove the RAF loop; keep only `gsap.ticker.add` |
| 4 | opacity:0 + reduced-motion | 315-367 | `.hero__label` (L315, `opacity:0`), `.hero__subtitle` (L340, `opacity:0`), `.hero__cta` (L353, `opacity:0`), `.hero__trust` (L366, `opacity:0`), `.trust__item` (L386, `opacity:0`), `.service-card` (L431, `opacity:0; transform:translateY(30px)`), `.slider` (L476, `opacity:0`), `.portfolio__item` (L582, `opacity:0`), `.about__image` (L640, `opacity:0`), `.about__content` (L650, `opacity:0`), `.review-card` (L703, `opacity:0`), `.process__step` (L774, `opacity:0`), `.cta__form-card` (L835, `opacity:0`). Reduced-motion block at L1037-1058 overrides ALL of these with `opacity:1!important; transform:none!important`. **CLEAN.** | CLEAN |
| 7 | registerPlugin order | 1412-1418 | `lenis.on('scroll', ScrollTrigger.update)` at L1412 BEFORE `gsap.registerPlugin(ScrollTrigger)` at L1418. | Move `gsap.registerPlugin(ScrollTrigger)` to right after `'use strict'`, before any Lenis/ScrollTrigger usage |

**Summary:** 3 bugs (SplitType conflict, double-raf, registerPlugin order). Image paths all valid.

---

## Cross-Template Summary

| Template | Double-RAF | RegisterPlugin Order | SplitType Conflict | Reduced-Motion Gaps | Image Issues |
|----------|-----------|---------------------|-------------------|---------------------|-------------|
| **6** | BUG | BUG | clean | BUG (clip-path) | clean |
| **7** | BUG | BUG | clean | clean | clean |
| **8** | BUG | BUG | clean | clean (+ Lenis a11y) | clean |
| **9** | BUG | BUG | BUG | clean | clean |

**Total: 11 bugs across 4 templates. 0 image issues.**
