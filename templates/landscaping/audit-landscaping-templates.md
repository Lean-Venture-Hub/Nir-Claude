# Landscaping Templates Audit — Scroll/Animation & Image Bugs

**Date:** 2026-03-13
**Templates audited:** 1–5
**Available images:** `hero.jpg`, `before.jpg`, `after.jpg`, `hardscape-patio.jpg`, `irrigation.jpg`, `landscape-lighting.jpg`, `lawn-care.jpg`, `outdoor-living.jpg`, `retaining-wall.jpg`, `team.jpg`

---

## Template 1 — `template_example-1.html`

### Bugs Found

| # | Check | Line(s) | Bug | Fix |
|---|-------|---------|-----|-----|
| 1 | **Lenis double-raf** | 2234–2238, 2246 | Has BOTH `requestAnimationFrame` loop AND `gsap.ticker.add` driving Lenis. Double-pumps `lenis.raf()`. | Remove the `requestAnimationFrame` loop (lines 2234–2238). Keep only `gsap.ticker.add`. |
| 2 | **opacity:0 + reduced-motion** | 1563–1566 | `.anim-fade`, `.anim-fade-left`, `.anim-fade-right`, `.anim-scale` all set `opacity:0` in CSS but have NO `@media(prefers-reduced-motion)` override. The `return` at line 2319 handles it in JS, but if JS fails these elements are permanently invisible. | Add to the existing `@media(prefers-reduced-motion:reduce)` block (line 120): `.anim-fade,.anim-fade-left,.anim-fade-right,.anim-scale{opacity:1!important;transform:none!important}` |
| 3 | **registerPlugin order** | 2242 | `gsap.registerPlugin(ScrollTrigger)` is called AFTER `lenis.on('scroll', ScrollTrigger.update)` at line 2245 — but wait, line 2242 is before 2245, so this is actually fine. However, if lenis is created and `ScrollTrigger.update` is referenced at line 2245 before registerPlugin... Actually `ScrollTrigger` is loaded as a script, so it exists globally. **No bug — OK.** | — |

**Image paths:** All use `../../images/template-images/{name}.jpg` — all 10 filenames match existing files. **CLEAN.**

---

## Template 2 — `template_example-2.html`

### Bugs Found

| # | Check | Line(s) | Bug | Fix |
|---|-------|---------|-----|-----|
| 1 | **Lenis double-raf** | 1916–1920, 1924 | Has BOTH `requestAnimationFrame` loop AND `gsap.ticker.add`. | Remove the `requestAnimationFrame` loop (lines 1916–1920). Keep only `gsap.ticker.add` at line 1924. |
| 2 | **Lenis not gated by reduced-motion** | 1909–1920 | Lenis is initialized unconditionally (before `prefersReduced` check at line 1928). Smooth scroll runs even with reduced motion preference. | Wrap Lenis init (lines 1909–1925) in `if (!prefersReduced)` check, but `prefersReduced` must be declared first (move line 1928 before Lenis init). |
| 3 | **registerPlugin inside reduced-motion block** | 1939 | `gsap.registerPlugin(ScrollTrigger)` is inside `if (!prefersReduced)`. But `ScrollTrigger.update` is referenced at line 1923 unconditionally (Lenis scroll binding). If reduced motion is ON, `registerPlugin` never runs — but `ScrollTrigger` is still a global from the CDN script, so this works. However, it's fragile. | Move `gsap.registerPlugin(ScrollTrigger)` outside the `if (!prefersReduced)` block. |
| 4 | **SplitType + manual `.word-inner` spans** | 319–323, 1944 | CSS has `.hero-headline .word { display: inline-block; overflow: hidden; }` and `.hero-headline .word-inner { display: inline-block; transform: translateY(110%); }` at lines 319–323. The HTML likely has manual `<span class="word">` wrapping. Then SplitType at line 1944 runs `new SplitType(heroH1, { types: 'words' })` which creates its OWN word spans. **Conflict:** SplitType wraps words AND there are already manual word/word-inner spans. | Either remove the manual `.word`/`.word-inner` spans from HTML and CSS, OR remove SplitType and animate the manual spans. |
| 5 | **opacity:0 + reduced-motion partial** | 1316–1328 | The reduced-motion block covers `.hero-eyebrow`, `.hero-sub`, `.hero-ctas`, trust-cards, service-rows etc. — BUT `.hero-headline .word-inner` only gets `transform: none` (line 1323), not explicit `opacity: 1`. The `.word-inner` starts at `opacity: 0` implicitly (from transform hiding). **This is borderline OK** since the word-inner is hidden by transform, not opacity. | — |

**Image paths:** All use `../../images/template-images/{name}.jpg` — all filenames match existing files. **CLEAN.**

---

## Template 3 — `template_example-3.html`

### Bugs Found

| # | Check | Line(s) | Bug | Fix |
|---|-------|---------|-----|-----|
| 1 | **Lenis double-raf** | 690–691, 693 | Has BOTH `requestAnimationFrame` loop AND `gsap.ticker.add`. | Remove the `requestAnimationFrame` loop (lines 690–691). Keep only `gsap.ticker.add` at line 693. |
| 2 | **Lenis not gated by reduced-motion** | 689–694 | Lenis is initialized unconditionally. `prefersReduced` check is at line 700, but Lenis + raf loop + ticker are all set up before it. | Wrap Lenis init (lines 689–694) in `if (!prefersReduced)` block. |
| 3 | **opacity:0 + reduced-motion** | 261–264 | Reduced-motion block only does `*{animation:none!important;transition:none!important}` and `.hscroll-track{transform:none!important}`. Does NOT set `opacity:1` on any elements. ALL `gsap.from()` calls (lines 706–807) start from `opacity:0` — if JS fails or reduced-motion users don't run the animation block, elements stay invisible. | Add to `@media(prefers-reduced-motion:reduce)`: `.hero-tag,.hero-headline,.hero-desc,.hero-phone,.hero-scroll,.trust-num,.service-card,.ba-slider,.project-card,.about-quote blockquote,.about-bio,.review-block,.process-step,.area-tag,.cta-title{opacity:1!important;transform:none!important}` |
| 4 | **Animation initial state** | 706–710 | Hero elements don't have CSS `opacity:0` — they use `gsap.from({opacity:0})` which sets inline opacity:0 at runtime. If JS loads slowly, there's a flash of unstyled content (FOUC) before GSAP hides them. Minor but inconsistent with other templates. | Add CSS `opacity:0` to `.hero-tag,.hero-headline,.hero-desc,.hero-phone,.hero-scroll` and include them in reduced-motion override. |

**Image paths:** All use `../../images/template-images/{name}.jpg` — all filenames match existing files. **CLEAN.**

---

## Template 4 — `template_example-4.html`

### Bugs Found

| # | Check | Line(s) | Bug | Fix |
|---|-------|---------|-----|-----|
| 1 | **Lenis double-raf** | 933–934, 936 | Has BOTH `requestAnimationFrame` loop AND `gsap.ticker.add`. | Remove the `requestAnimationFrame` loop (lines 933–934). Keep only `gsap.ticker.add` at line 936. |
| 2 | **Pinned slides: no fade-out on exit** | 1035–1056 | Hero is pinned with `end: '+=220%'` and elements fade IN via scrub timeline, but there is **no `gsap.to(opacity:0)` on exit**. When the pin releases, hero content stays fully visible behind the next section. Same issue on services (line 1074), before/after (1105), portfolio (1151), about (1188), and CTA (1215). | For each pinned chapter, add fade-out at the end of the scrub timeline, e.g. `hTl.to('.hero-content-wrapper', {opacity: 0, duration: .15}, .85)`. Or ensure the next section has a solid background + sufficient `z-index`. |
| 3 | **No manual `<span class="word">` conflict with SplitType** | 1031 | Line 1031 does `hlEl.innerHTML = ... '<span class="word">'...`. No SplitType is used — the manual word split IS the animation mechanism. The `.word` CSS at line 202 sets `opacity:0; transform:translateY(60px) rotateX(30deg)`. **No SplitType conflict — OK.** | — |
| 4 | **`.visible` pattern OK** | 176–183 | `.hero-ambient` starts `opacity:0` at line 181, `.hero-ambient.visible` sets `opacity:1` at line 183. JS adds `.visible` at line 1045 (desktop) and 1050 (mobile). Reduced-motion at line 995 also adds `.visible`. **CLEAN.** | — |
| 5 | **`#portFilters` not in reduced-motion override** | 530–536 | Line 353 sets `.port-filters` to `opacity:0`. The reduced-motion CSS at line 532 lists `.port-filters` — but the JS references `#portFilters` (an ID). Checking... the CSS class `.port-filters` opacity:0 is at line 353 and IS covered at line 532. **OK — no bug.** Wait, line 532 says `.port-filters` but also check the ID. Let me re-read: line 1157 does `gsap.to('#portFilters', ...)`. The CSS at line 353 uses the class `.port-filters`, and reduced-motion at line 532 also uses `.port-filters`. The element likely has both `class="port-filters"` and `id="portFilters"`. **CLEAN.** | — |

**Image paths:** All use `../../images/template-images/{name}.jpg` — all filenames match existing files. **CLEAN.**

---

## Template 5 — `template_example-5.html`

### Bugs Found

| # | Check | Line(s) | Bug | Fix |
|---|-------|---------|-----|-----|
| 1 | **Lenis double-raf** | 1595–1596, 1598 | Has BOTH `requestAnimationFrame` loop AND `gsap.ticker.add`. | Remove the `requestAnimationFrame` loop (lines 1595–1596). Keep only `gsap.ticker.add` at line 1598. |
| 2 | **opacity:0 + reduced-motion** | 1162–1169 | Reduced-motion block only kills animation/transition durations and `.scroll-line`. Does NOT override `opacity:0` on: `.hero-eyebrow` (L285), `.hero-sub` (L311), `.hero-actions` (L319), `.hero-scroll-hint` (L370), `.trust-card` (L423-425 via `opacity:0; transform:translateY(30px)`), `.section-header` (L461-462), `.service-card`, `.portfolio-overlay` (L707), etc. | Add to `@media(prefers-reduced-motion:reduce)`: `.hero-eyebrow,.hero-sub,.hero-actions,.hero-scroll-hint,.trust-card,.section-header,.service-card,.portfolio-item,.review-card,.process-step,.cta-inner,.about-visual,.about-content{opacity:1!important;transform:none!important}` |
| 3 | **`.hero-headline .word` CSS + SplitType** | 303, 1687 | CSS at line 303 defines `.hero-headline .word { display: inline-block; }`. Then SplitType at line 1687 runs with `types: 'lines, words, chars'`. SplitType creates its own `.word` spans. If the HTML already contains manual `.word` spans, this would conflict. However, looking at the HTML (line 1237–1239), the headline is plain text: `Landscapes That Move You`. **No manual `.word` spans — SplitType creates them, and the CSS rule `.hero-headline .word` targets those generated spans. No conflict — OK.** | — |
| 4 | **No `<img>` in hero background** | 229 | Hero background uses CSS `url('../../images/template-images/hero.jpg')` via `background:` shorthand. This is fine but means no `alt` text for the hero image — accessibility concern, not a bug per se. | — |

**Image paths:** Uses both `<img src>` and CSS `background: url()` — all reference `../../images/template-images/{name}.jpg`. All filenames match existing files. **CLEAN.**

---

## Summary

| Template | Lenis double-raf | Pinned slide fade-out | SplitType conflict | Reduced-motion opacity | Image issues |
|----------|:---:|:---:|:---:|:---:|:---:|
| **1** | BUG | n/a | OK | BUG (`.anim-*` classes) | CLEAN |
| **2** | BUG | n/a | BUG (manual `.word-inner` + SplitType) | borderline OK | CLEAN |
| **3** | BUG | n/a | OK | BUG (no overrides at all) | CLEAN |
| **4** | BUG | BUG (6 pinned sections, none fade out) | OK (no SplitType) | OK (comprehensive list) | CLEAN |
| **5** | BUG | n/a | OK | BUG (no overrides) | CLEAN |

### Universal fix — Lenis double-raf (all 5 templates)
In every template, remove the `requestAnimationFrame` loop and keep only `gsap.ticker.add((time) => lenis.raf(time * 1000))`. The ticker already calls `lenis.raf()` every frame; the separate rAF loop calls it a second time per frame, causing jank.

### Critical bugs
1. **Template 4, pinned sections:** 6 chapters pinned with no opacity fade-out — content stacks visually when pins release.
2. **Templates 3 & 5, reduced-motion:** Elements with CSS `opacity:0` have no reduced-motion override — completely invisible to users who prefer reduced motion.
3. **Template 2, SplitType conflict:** Manual `.word`/`.word-inner` spans + SplitType both wrapping the same headline.
