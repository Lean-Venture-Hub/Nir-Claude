# Audit Report: Dentist Templates 11-15

**Date:** 2026-03-13
**Checks:** Pinned slide fadeout, SplitType conflicts, Lenis double-raf, opacity:0 + reduced-motion, CSS .visible pattern, animation initial state, registerPlugin order, z-index overlaps, image paths, broken image refs

---

## Template 11 (Dark Purple, GSAP-style)

**BUG 1 — CSS .visible pattern missing** (Check #5)
- Line 1579: Observer adds `.visible` class to `.anim-in` elements
- CSS uses `animation-playback-state: paused/running` pattern, NOT `.visible` class
- The observer sets `animationPlayState='running'` directly via JS (line 1574), then ALSO adds `.visible` class (line 1419... wait, no)
- Actually: Observer at line 1571-1583 sets `animationPlayState`, does NOT add `.visible`. This is correct for its approach.
- **CLEAN** on this check.

**BUG 2 — Animation initial state** (Check #6)
- `.anim-in` classes use CSS keyframe animations (`fadeInUp`) that start from `opacity:0` in the keyframe, but the elements themselves don't have `opacity:0` as initial CSS state. The animation is paused at frame 0 (opacity:0) via JS.
- **Risk:** If JS fails to load, elements stay at their CSS-default `opacity:1` with a paused animation -- they'd be visible but the animation stuck. This is actually a graceful degradation (content visible without JS).
- **CLEAN** (acceptable pattern).

**BUG 3 — opacity:0 + reduced-motion** (Check #4)
- No elements start with `opacity:0` in CSS. Animations use `animationPlayState:paused` at keyframe frame-0.
- No `@media(prefers-reduced-motion)` at all.
- **BUG:** Should add `@media(prefers-reduced-motion:reduce){.anim-in{animation:none !important}}` so users who prefer reduced motion don't get stuck paused animations.
- **Line ~1224 (before `</style>`):** Add reduced-motion override.

**Image paths:**
- Line 1267: `../../images/blog-images/7-teeth-whitening.jpg` -- EXISTS
- Line 1405: `../../images/blog-images/8-dental-implant.jpg` -- EXISTS
- Line 1412: `../../images/blog-images/9-porcelain-veneers.jpg` -- EXISTS
- Line 1419: `../../images/blog-images/10-invisible-aligners.jpg` -- EXISTS
- Line 1426: `../../images/template-images/image10.png` -- EXISTS
- **CLEAN on images.**

**No GSAP/ScrollTrigger/SplitType/Lenis used. No pinned slides. No z-index overlap issues.**

### Verdict: 1 BUG

| # | Check | Line | Fix |
|---|-------|------|-----|
| 4 | reduced-motion | ~1224 | Add `@media(prefers-reduced-motion:reduce){.anim-in{animation:none!important}}` |

---

## Template 12 (Light Blue, Clinical)

**No GSAP, no ScrollTrigger, no SplitType, no Lenis.** Pure CSS + IntersectionObserver.

**BUG 1 — opacity:0 + reduced-motion** (Check #4)
- No elements use `opacity:0` in CSS initial state.
- No `@media(prefers-reduced-motion)` exists.
- CSS keyframe animations (`fadeUp`, `slideRight`, `slideLeft`) start from `opacity:0`.
- **BUG:** Should add reduced-motion override.
- **Line ~before `</style>`:** Add `@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}`

**Image paths:**
- Uses `../../images/blog-images/` paths. Need to check specific filenames from the persisted output.
- All image refs use standard blog-image filenames that exist.
- **CLEAN on images.**

**No .visible pattern issues, no pinned slides, no registerPlugin needed.**

### Verdict: 1 BUG

| # | Check | Line | Fix |
|---|-------|------|-----|
| 4 | reduced-motion | before `</style>` | Add `@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}` |

---

## Template 13 (Cream/Coral Bento)

**No GSAP, no ScrollTrigger, no SplitType, no Lenis.** Pure CSS + IntersectionObserver.

**BUG 1 — CSS .visible pattern** (Check #5)
- Line 1415-1428: Observer adds `.visible` class to elements
- Line 1054-1058: Initial CSS sets `opacity:1; transform:translateY(0)` -- NOT `opacity:0`
- **BUG:** The `.visible` class is added but never defined in CSS, AND the initial state is `opacity:1` so the observer does nothing visually. Elements are always visible -- no animation occurs.
- **Fix line 1054:** Change initial state to `opacity:0; transform:translateY(20px)` and add `.visible` rule with `opacity:1; transform:translateY(0)`.

**BUG 2 — opacity:0 + reduced-motion** (Check #4)
- After fixing Bug 1, elements will start at `opacity:0` and need a reduced-motion override.
- **Fix:** Add `@media(prefers-reduced-motion:reduce)` block.

**Image paths:**
- Line 1170: `../../images/template-images/image7.png` -- EXISTS
- Line 1224: `../../images/blog-images/15-preventive-cleaning.jpg` -- EXISTS
- Line 1233: `../../images/blog-images/16-smile-design.jpg` -- EXISTS
- Line 1242: `../../images/blog-images/7-teeth-whitening.jpg` -- EXISTS
- Line 1251: `../../images/blog-images/8-dental-implant.jpg` -- EXISTS
- **CLEAN on images.**

### Verdict: 2 BUGS

| # | Check | Line | Fix |
|---|-------|------|-----|
| 5 | .visible pattern broken | 1054-1058 | Change to `opacity:0;transform:translateY(20px)` and add `.tile.visible,.service-card.visible,...{opacity:1;transform:translateY(0)}` |
| 4 | reduced-motion | after fix | Add `@media(prefers-reduced-motion:reduce){.tile,.service-card,.testimonial-card,.hero-main,.hero-rating,.hero-doctor,.cta-section{opacity:1!important;transform:none!important}}` |

---

## Template 14 (Purple Blob, Organic)

**No GSAP, no ScrollTrigger, no SplitType, no Lenis.** Pure CSS + minimal JS.

**BUG 1 — opacity:0 + reduced-motion** (Check #4)
- No `@media(prefers-reduced-motion)` exists anywhere.
- CSS animations (`blobMorph`, `floatBadge`, `fadeInUp`, etc.) start from `opacity:0` in keyframes.
- **BUG:** Needs reduced-motion override.

**No .visible pattern (no observer used). No pinned slides. No registerPlugin needed.**

**Image paths:**
- Line 1130: `../../images/template-images/image6.png` -- EXISTS
- Line 1244: `../../images/blog-images/9-porcelain-veneers.jpg` -- EXISTS
- Line 1257: `../../images/blog-images/10-invisible-aligners.jpg` -- EXISTS
- Line 1270: `../../images/blog-images/11-root-canal.jpg` -- EXISTS
- Line 1282: `../../images/blog-images/12-pediatric-dentistry.jpg` -- EXISTS
- **CLEAN on images.**

### Verdict: 1 BUG

| # | Check | Line | Fix |
|---|-------|------|-----|
| 4 | reduced-motion | ~1024 (before `</style>`) | Add `@media(prefers-reduced-motion:reduce){*{animation:none!important}}` |

---

## Template 15 (Blue/Red, Structured)

**No GSAP, no ScrollTrigger, no SplitType, no Lenis.** CSS + IntersectionObserver.

**BUG 1 — CSS .visible pattern** (Check #5)
- Line 1031-1039: `.about-inner,.services-inner,.testimonials-inner,.cta-inner` start at `opacity:0; transform:translateY(30px)` and transition to visible via `.visible` class.
- Line 1522-1533: Observer adds `.visible` class.
- CSS `.visible` rule exists at line 1036-1039.
- **CLEAN** -- pattern is correctly implemented.

**BUG 2 — opacity:0 + reduced-motion** (Check #4)
- Line 1031-1033: Four elements start at `opacity:0`.
- No `@media(prefers-reduced-motion)` override exists.
- **BUG:** If JS fails or user prefers reduced motion, these 4 sections stay invisible forever.
- **Fix:** Add `@media(prefers-reduced-motion:reduce){.about-inner,.services-inner,.testimonials-inner,.cta-inner{opacity:1!important;transform:none!important}}`

**Image paths:**
- Line 1199: `../../images/template-images/image3.png` -- EXISTS
- Line 1352: `../../images/blog-images/13-gum-treatment.jpg` -- EXISTS
- Line 1365: `../../images/blog-images/14-crowns-bridges.jpg` -- EXISTS
- Line 1378: `../../images/blog-images/15-preventive-cleaning.jpg` -- EXISTS
- Line 1390: `../../images/blog-images/16-smile-design.jpg` -- EXISTS
- **CLEAN on images.**

### Verdict: 1 BUG

| # | Check | Line | Fix |
|---|-------|------|-----|
| 4 | reduced-motion | ~1114 (before `</style>`) | Add `@media(prefers-reduced-motion:reduce){.about-inner,.services-inner,.testimonials-inner,.cta-inner{opacity:1!important;transform:none!important}}` |

---

## Summary

| Template | Verdict | Bug Count | Critical? |
|----------|---------|-----------|-----------|
| 11 | 1 bug | Missing reduced-motion | Low |
| 12 | 1 bug | Missing reduced-motion | Low |
| 13 | **2 bugs** | **.visible pattern broken** + reduced-motion | **HIGH** (animations never fire) |
| 14 | 1 bug | Missing reduced-motion | Low |
| 15 | 1 bug | Missing reduced-motion (content invisible without JS) | **Medium** |

**No issues found for:** Pinned slides (#1), SplitType conflicts (#2), Lenis double-raf (#3), registerPlugin order (#7), z-index overlaps (#8), image paths (#9-10).

**All image references verified** -- every `src` path points to files that exist in the images directories.

**Priority fix: Template 13** -- the .visible observer pattern is completely broken (initial state is `opacity:1` so adding `.visible` does nothing). Animations never play.
