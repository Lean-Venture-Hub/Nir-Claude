# HVAC Templates 1-5 Audit Report

**Date:** 2026-03-14
**Available images:** ac-install.jpg, commercial.jpg, ductwork.jpg, emergency.jpg, furnace-repair.jpg, heat-pump.jpg, hero.jpg, maintenance.jpg, team.jpg, thermostat.jpg

---

## Template 1 — CLEAN

All 10 checks pass.

- No pinned slides, no SplitType, no `.visible` pattern
- Lenis: `gsap.ticker.add` only (line 812) -- correct, no double-raf
- Reduced motion: blanket `*` override (line 77)
- `gsap.registerPlugin(ScrollTrigger)` at line 808, before first usage line 827
- **Images: ALL VALID** -- all `src` paths match existing files

---

## Template 2 — 1 BUG

### BUG: Unclosed CSS `.hero-lines` rule (line 126-131)
**Severity:** HIGH -- breaks all CSS after this point

```css
.hero-lines{position:absolute;inset:0;z-index:1;pointer-events:none;opacity:.06;
  background:repeating-linear-gradient(
    -45deg,
    transparent,transparent 40px,
    var(--electric) 40px,var(--electric) 41px
  )}           /* <-- missing closing brace */
.hero-content{...  /* this rule absorbs into hero-lines */
```

Line 131: the `)}` closes the `background` value and the `repeating-linear-gradient()` parenthesis, but the selector block `{` from line 126 is never closed with `}`.

**Fix line 131:** Change `)}` to `);}`  (add semicolon before the closing brace, or just add a `}` on a new line after)

Everything else passes:
- Lenis: `gsap.ticker.add` only (line 793), no double-raf
- `gsap.registerPlugin` at line 787, before usage
- Reduced motion: blanket `*` override (line 311)
- **Images: ALL VALID**

---

## Template 3 — 1 BUG

### BUG: registerPlugin AFTER ScrollTrigger.update reference (line 1228 vs 1234)
**Severity:** LOW-MEDIUM -- works because CDN `<script>` makes `ScrollTrigger` global, but violates best practice

```js
lenis.on('scroll', ScrollTrigger.update);   // line 1228 -- uses ScrollTrigger
...
gsap.registerPlugin(ScrollTrigger);          // line 1234 -- registers after
```

**Fix:** Move `gsap.registerPlugin(ScrollTrigger);` to before the Lenis block (~line 1224).

Everything else passes:
- No pinned slides, no SplitType, no `.visible` pattern
- Lenis: `gsap.ticker.add` only (line 1229), no double-raf
- Reduced motion: blanket `*` override (line 71)
- Template uses `{{PLACEHOLDER}}` tokens (correct for template pipeline)
- **Images: ALL VALID**

---

## Template 4 — 2 BUGS

### BUG 1: Lenis double-raf (lines 991-994)
**Severity:** HIGH -- Lenis processes frames twice, causing jitter/doubled scroll speed

```js
function raf(time){lenis.raf(time);requestAnimationFrame(raf)}  // line 991
requestAnimationFrame(raf);                                      // line 992
lenis.on('scroll',ScrollTrigger.update);                         // line 993
gsap.ticker.add(time => lenis.raf(time * 1000));                 // line 994
```

**Fix:** Delete lines 991-992. Keep only:
```js
lenis.on('scroll',ScrollTrigger.update);
gsap.ticker.add(time => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);
```

### BUG 2: registerPlugin AFTER ScrollTrigger.update reference (line 993 vs 998)
**Severity:** LOW-MEDIUM -- same pattern as Template 3

```js
lenis.on('scroll',ScrollTrigger.update);   // line 993
...
gsap.registerPlugin(ScrollTrigger);         // line 998
```

**Fix:** Move `gsap.registerPlugin(ScrollTrigger);` to line 990 (before Lenis block).

Everything else passes:
- Manual `<span class="word">` in hero (line 553-555) -- no SplitType loaded, so these are intentional animation targets, not a conflict
- Reduced motion: explicit element overrides (lines 73-84) covering `.reveal,.service-card,.testimonial-card,.gallery-item,.process-step,.trust-item,.about-img-wrap` and hero elements -- thorough
- **Images: ALL VALID**

---

## Template 5 — CLEAN

All 10 checks pass.

- No pinned slides, no SplitType, no `.visible` pattern
- Lenis: `gsap.ticker.add` only (line 681), no double-raf
- `gsap.registerPlugin(ScrollTrigger)` at line 679, before first usage (line 680)
- Reduced motion: blanket `*` override (line 282-284) + explicit hero/counter fallbacks (lines 813-821)
- **Images: ALL VALID**

---

## Summary

| Template | Status | Bugs | Severity |
|----------|--------|------|----------|
| 1 | CLEAN | 0 | -- |
| 2 | **1 BUG** | Unclosed CSS `.hero-lines` (line 131) | HIGH |
| 3 | **1 BUG** | registerPlugin order (line 1228 vs 1234) | LOW-MED |
| 4 | **2 BUGS** | Double-raf (lines 991-992); registerPlugin order (line 993 vs 998) | HIGH + LOW-MED |
| 5 | CLEAN | 0 | -- |

**Image paths:** All 5 templates reference only files that exist in `template-images/`. Zero broken image refs across all templates.
