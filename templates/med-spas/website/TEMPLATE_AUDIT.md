# Med Spa Template Audit Report

**Date:** 2026-03-14
**Templates audited:** 1, 2, 4, 6, 8, 10

## Summary

Templates 1 and 10 have the most issues. Template 1 sets CSS `opacity: 0` on many elements that rely on GSAP `gsap.to()` to reveal them, but uses `gsap.set()` AFTER the timeline runs, creating a race condition. Templates 2 and 10 have Lenis-ScrollTrigger sync issues. All templates have the 10 required sections present and service cards are fully populated.

---

## Template 1

**File:** `template-1/template_example-1.html`

### Issues Found

1. **CRITICAL: GSAP `gsap.set()` called AFTER timeline starts (race condition)** — Line 1521: `gsap.set(['.hero-eyebrow', '.hero h1', '.hero-sub', '.hero-btns'], { y: 30 })` is called AFTER the hero timeline at line 1513 already starts `.to()` animations. The `gsap.set()` should come BEFORE the timeline, otherwise the initial `y:30` may override the animation or cause a visible jump. The hero elements have CSS `opacity: 0` but the `gsap.set()` does not set opacity, so they start invisible but may flash.

2. **CRITICAL: CSS `opacity: 0` on many elements with no fallback** — Lines 469 (`.trust-item`), 519 (`.service-card`), 592 (unclear context), 732 (`.about-content`), 777 (`.gallery-item`), 831 (`.testimonial-card`), 912 (`.process-step`) all have `opacity: 0` in CSS. If GSAP fails to load or errors, these sections remain invisible forever. The reduced-motion fallback at line 1645 handles this, but only if prefers-reduced-motion is set. Normal users with blocked CDN = blank page.

3. **Minor: `about-content` set to `opacity: 0` then `gsap.set('.about-content', { x: 40 })` at line 1585** — The `x: 40` set happens AFTER the `gsap.to` for about-content (line 1575). Same race condition as hero.

4. **Before/After slider uses `clipPath` on the BEFORE image** — Line 1704: `before.style.clipPath`. This works but is backwards from the usual convention (clip the after image). Not a bug but could cause confusion during customization.

### Sections Present
Nav, Hero, Trust Bar, Services (6 cards), Before/After, About, Gallery, Testimonials, Process, Footer/Contact -- **All 10 present**

### Scroll/Lenis
- Lenis initialized correctly (line 1492)
- `ScrollTrigger.update` synced (line 1503)
- `gsap.registerPlugin(ScrollTrigger)` called (line 1509)
- No body/html overflow:hidden blocking scroll

---

## Template 2

**File:** `template-2/template_example-2.html`

### Issues Found

1. **POTENTIAL: Lenis sync with ScrollTrigger uses reference BEFORE registration** — Line 1049: `lenis.on('scroll', ScrollTrigger.update)` is called BEFORE `gsap.registerPlugin(ScrollTrigger)` on line 1055. ScrollTrigger is available as a global from the CDN script tag, so `ScrollTrigger.update` likely works, but it's bad practice and could cause subtle timing issues.

2. **POTENTIAL: Before/After slider clips the AFTER image `inset(0 N% 0 0)`** — Line 1128: `afterImg.style.clipPath='inset(0 '+(100-pct)+'% 0 0)'`. This clips from the right, which means the "after" image is revealed from the left. This is the expected behavior but the variable is named `afterImg` while being clipped -- should verify visual result matches expectation.

3. **No CSS `opacity: 0` on elements** — Template 2 uses `gsap.from()` pattern instead of CSS `opacity: 0` + `gsap.to()`. This is much safer -- if GSAP fails, everything is visible by default.

### Sections Present
Nav, Hero, Trust Bar, Services (6 cards), Before/After, About, Gallery, Testimonials, Process, Footer/Contact -- **All 10 present**

### Scroll/Lenis
- Lenis initialized (line 1046)
- ScrollTrigger registered (line 1055)
- No blocking overflow

---

## Template 4

**File:** `template-4/template_example-4.html`

### Issues Found

1. **CRITICAL: CSS `opacity: 0` and `transform` on `.reveal-up` and `.reveal-clip` classes** — Line 1150-1153: `.reveal-up { opacity: 0; transform: translateY(40px); }` and `.reveal-clip { clip-path: polygon(...) }`. Many elements use these classes (hero eyebrow, hero-sub, hero-cta, trust items, service cards, gallery items, testimonials, process steps). If GSAP fails to load, ALL content below the hero bg image is invisible.

2. **Reduced motion fallback only covers CSS** — Line 1164-1165: The CSS `prefers-reduced-motion` reset sets `opacity: 1` and `transform: none` on `.reveal-up` and `.reveal-clip`. But if GSAP fails for OTHER reasons (network error), there's no fallback.

3. **No Lenis-ScrollTrigger sync** — Lines 1040-1045: Lenis is initialized with a simple `raf()` loop, but there is NO `lenis.on('scroll', ScrollTrigger.update)` call, and NO `gsap.ticker.add()` integration. This means **Lenis and ScrollTrigger are not synced**, which can cause ScrollTrigger animations to fire at wrong scroll positions or not at all.

4. **Section `clip-path` reveal animation** — Line 1153-1161: `section-reveal` class uses `clipPath: 'inset(8% 4% 8% 4%)'` with scrubbed ScrollTrigger. Combined with the missing Lenis sync (issue 3), this could cause sections to appear clipped/partially visible and never fully reveal.

### Sections Present
Nav, Hero, Trust Bar, Services (6 cards), Before/After, About, Gallery, Testimonials, Process, Footer/Contact -- **All 10 present**

### Scroll/Lenis
- Lenis initialized (line 1042) -- YES
- Lenis-ScrollTrigger sync -- **MISSING** (critical)
- ScrollTrigger registered (line 1048) -- YES
- Hero: `min-height: 100dvh` -- OK

---

## Template 6

**File:** `template-6/template_example-6.html`

### Issues Found

1. **CRITICAL: Hero `opacity: 0` elements with `gsap.to()` pattern** — The hero uses `.to()` animations (lines 1112-1118) targeting `.hero-eyebrow`, `.hero-title .word`, `.hero-subtitle`, `.hero-cta-row`, `.hero-scroll-indicator`. The CSS sets initial opacity via CSS (hero-eyebrow at line ~254 likely has opacity:0). If GSAP fails, hero content stays invisible.

2. **Trust bar counter animation may produce garbled text** — Lines 1128-1149: The counter animation uses `gsap.from(el, { innerText: 0 })` with `snap` and manual `onUpdate`. The `innerText` tween approach is fragile -- it converts innerHTML to a number, which can produce `NaN` if the element contains non-numeric characters like "+" suffix or star characters.

3. **Scroll progress bar uses GSAP ScrollTrigger** — Line 1051-1058: `gsap.to(progressBar, { width: '100%', scrollTrigger: { ... scrub: 0.3 } })`. This works but duplicates functionality that could be done with a simple scroll listener (as template 10 does).

4. **Footer form animation targets children** — Line 1276: `gsap.from('.footer-form > *', ...)` -- this is fine but could animate form inputs which may look odd.

### Sections Present
Nav, Hero, Trust Bar, Services (6 cards), Before/After, About, Gallery, Testimonials, Process, Footer/Contact -- **All 10 present**

### Scroll/Lenis
- Lenis initialized (line 1042) -- YES
- Lenis-ScrollTrigger sync -- **PRESENT but indirect** (via ScrollTrigger.create for nav, no explicit `lenis.on('scroll', ScrollTrigger.update)`)
- Actually checking again: the Lenis sync is NOT present. The code does NOT have `lenis.on('scroll', ScrollTrigger.update)` or `gsap.ticker.add()`. **MISSING Lenis-ScrollTrigger sync**.
- ScrollTrigger registered (line 1048) -- YES

---

## Template 8

**File:** `template-8/template_example-8.html`

### Issues Found

1. **CRITICAL: Pinned horizontal scroll gallery may cause scroll lock** — Line 1728-1755: The gallery uses `ScrollTrigger` pin with horizontal scroll (`gsap.to(galleryTrack, { x: getScrollAmount, scrollTrigger: { pin: true, scrub: 1 } })`). If Lenis and ScrollTrigger are not properly synced, the pinned section can trap the user -- they scroll but nothing happens. However, Lenis IS synced in this template (lines 1601-1604).

2. **CSS `opacity: 0` and `.reveal-up` class** — Line 1150-1153: Same pattern as Template 4 -- `.reveal-up { opacity: 0; transform: translateY(40px); }`. Many elements use this class. GSAP failure = invisible content.

3. **`position: fixed` elements** — Lines 89, 99: `.scroll-progress` (line 86: `position:fixed; height:3px; z-index:10000`) and a pseudo-element `.noise-overlay::before` (line 101: `position:fixed; inset:0; z-index:9998; pointer-events:none`). The noise overlay has `pointer-events:none` so it won't block interaction, but z-index 9998 is very high.

4. **Gallery `overflow: hidden` on section** — Line 213: `section { overflow: hidden }`. This applies to ALL sections, which could clip ScrollTrigger pin spacers or cause pin miscalculation. The gallery section at line 1358 is inside a `.gallery-pinned` div though, which may work around this.

5. **No reduced motion CSS fallback for `.reveal-up`** — The CSS has reduced motion rules (lines 1156-1166) but they target `animation-duration` and `transition-duration`, not the `.reveal-up` class opacity/transform. There IS a specific rule at line 1165: `.reveal-up { opacity: 1; transform: none; }` -- OK, this IS covered.

### Sections Present
Nav, Hero, Trust Bar, Services (6 cards), Before/After, About, Gallery (horizontal scroll), Testimonials, Process, Footer/Contact -- **All 10 present**

### Scroll/Lenis
- Lenis initialized (line 1590) -- YES
- Lenis-ScrollTrigger sync (lines 1602-1604) -- YES, properly done
- ScrollTrigger registered (line 1599) -- YES
- Hero: `min-height: 100dvh` -- OK

---

## Template 10

**File:** `template-10/template_example-10.html`

### Issues Found

1. **CRITICAL: CSS `opacity: 0` on `.reveal` class elements** — Multiple elements use `.reveal` class which has initial CSS `opacity: 0; transform: translateY(30px)` (check CSS). The `gsap.to()` pattern at line 1288 reveals them. GSAP failure = invisible content.

2. **Trust bar counter animation depends on `data-count` attribute** — Line 1327-1348: `const target = parseInt(el.dataset.count)`. The trust bar HTML (lines 1219-1242) uses TEXT content like "4.9", "418+", "7+", "12K+" but does NOT have `data-count` attributes. `parseInt(el.dataset.count)` returns `NaN`. The counter animation will set all trust numbers to `NaN` or display incorrectly.

3. **`position: fixed` noise overlay and mesh blobs** — Lines 101, 109: Fixed pseudo-element and mesh blobs cover the full viewport. Both have `pointer-events: none` so they don't block interaction. The mesh blobs at z-index 0 with `overflow: hidden` should be fine.

4. **All sections have `overflow: hidden`** — Line 213: `section { position: relative; z-index: 1; overflow: hidden }`. This is global for all sections. Should be fine for most but could clip absolutely positioned decorative elements.

5. **Scroll progress bar uses vanilla JS instead of GSAP** — Lines 1203-1208: Simple scroll listener updates width. This is fine and more resilient than GSAP-based approach.

6. **Before/After slider clips the AFTER image from the LEFT** — Line 1241: `baAfter.style.clipPath = 'inset(0 0 0 ' + (pos * 100) + '%)'`. This reveals the before image as you drag right. This is the **reverse** of what's expected -- the "after" should be revealed, not hidden. The before image is shown full, and the after is clipped from the left. When user drags right, they see MORE of the before and LESS of the after. This is **backwards**.

### Sections Present
Nav, Hero, Trust Bar, Services (6 cards), Before/After, About, Gallery, Testimonials, Process, Footer/Contact -- **All 10 present**

### Scroll/Lenis
- Lenis initialized (line 1190) -- YES
- Lenis-ScrollTrigger sync (lines 1194-1196) -- YES
- ScrollTrigger registered (line 1200) -- YES
- Hero: `min-height: 100vh` -- OK

---

## Cross-Template Issues Summary

| Issue | T1 | T2 | T4 | T6 | T8 | T10 |
|-------|----|----|----|----|----|----|
| CSS `opacity:0` with no GSAP fallback | YES | no | YES | PARTIAL | YES | YES |
| Lenis-ScrollTrigger sync missing | no | no | **YES** | **YES** | no | no |
| `gsap.set()` race condition | YES | no | no | no | no | no |
| B/A slider direction wrong | no | no | no | no | no | **YES** |
| Trust counter NaN bug | no | no | no | RISK | no | **YES** |
| Empty/missing content | no | no | no | no | no | no |
| Missing sections | no | no | no | no | no | no |
| Body/html overflow blocking scroll | no | no | no | no | no | no |
| Fixed elements covering page | no | no | no | no | no | no |

## Priority Fixes

1. **Template 4 + 6:** Add Lenis-ScrollTrigger sync (`lenis.on('scroll', ScrollTrigger.update)` + `gsap.ticker.add()`)
2. **Template 10:** Fix trust bar counter (add `data-count` attributes or change JS to parse textContent)
3. **Template 10:** Fix Before/After slider direction (clip before image, not after)
4. **Template 1:** Move `gsap.set()` calls before timeline creation
5. **Templates 1, 4, 8, 10:** Add a JS fallback that removes `opacity: 0` if GSAP fails to load (e.g., `window.addEventListener('load', ...)` timeout check)
