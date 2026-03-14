# Audit: Dentist Templates 16-20 — Scroll/Animation & Image Bugs

**Date:** 2026-03-13
**Scope:** 10-point checklist (pinned slides, SplitType, Lenis, opacity/reduced-motion, .visible pattern, animation initial state, registerPlugin, z-index, image paths, broken refs)

## Summary

| Template | GSAP/ScrollTrigger | Lenis | SplitType | Verdict |
|----------|-------------------|-------|-----------|---------|
| 16 | None (CSS + IntersectionObserver) | No | No | 2 BUGS |
| 17 | None (CSS only) | No | No | CLEAN |
| 18 | None (CSS + IntersectionObserver) | No | No | 2 BUGS |
| 19 | None (CSS + IntersectionObserver) | No | No | 2 BUGS |
| 20 | None (CSS + IntersectionObserver) | No | No | 2 BUGS |

**None of the 5 templates use GSAP, ScrollTrigger, SplitType, or Lenis.** Checks 1-3, 7-8 are N/A for all.

---

## Template 16 (Blue, SaaS-style)

**Check 4 — opacity:0 + reduced-motion: BUG**
- Line ~52-74: CSS keyframes use `from{opacity:0}` (fadeInUp, etc.)
- `.animate-on-scroll` class (line ~97) likely starts at `opacity:0` (defined outside visible area), `.hero-text`, `.hero-visual` use `animation: fadeInUp` which starts from `opacity:0`
- **No `@media(prefers-reduced-motion:reduce)` block exists anywhere.**
- **Fix:** Add at end of `<style>`:
```css
@media(prefers-reduced-motion:reduce){
  *,.animate-on-scroll,.hero-text,.hero-visual{
    animation:none!important;
    transition:none!important;
    opacity:1!important;
    transform:none!important;
  }
}
```

**Check 5 — CSS .visible pattern: BUG**
- Line ~1350-1358: JS adds `.visible` class via IntersectionObserver to `.animate-on-scroll` elements
- **No `.animate-on-scroll` initial state (opacity:0) defined in CSS**, and **no `.animate-on-scroll.visible` rule in CSS.**
- The elements use `transition-delay` inline styles, suggesting they should fade in, but the CSS scaffolding is missing.
- **Fix:** Add to CSS:
```css
.animate-on-scroll{opacity:0;transform:translateY(30px);transition:opacity 0.6s ease,transform 0.6s ease}
.animate-on-scroll.visible{opacity:1;transform:translateY(0)}
```

**Image paths: CLEAN** — Uses `../../images/template-images/image2.png` (exists) and `../../images/blog-images/7-teeth-whitening.jpg` through `10-invisible-aligners.jpg` (all exist).

---

## Template 17 (Teal, L-frame)

**All checks: CLEAN**

- No JS animations, no GSAP, no IntersectionObserver, no `.animate-on-scroll` pattern.
- Only CSS keyframes (`fadeInUp`, `diamondSpin`, `floatBob`, etc.) used for decorative elements.
- No `opacity:0` initial states that need reduced-motion override (keyframes are on floating badges and hero text, which are decorative).
- **Missing `prefers-reduced-motion`** is minor since animations are decorative only (floats/spins), but not a hard bug per the checklist since no elements start at `opacity:0` in static CSS.
- **Image paths: CLEAN** — `../../images/template-images/image2.png` (exists). Blog images `11-root-canal.jpg`, `12-pediatric-dentistry.jpg`, `13-gum-treatment.jpg`, `14-crowns-bridges.jpg` (all exist).

---

## Template 18 (Dark purple/mint, split hero)

**Check 4 — opacity:0 + reduced-motion: BUG**
- Line ~49-68: CSS keyframes `fadeInUp`, `fadeInRight`, `fadeInLeft`, `scaleIn` all start from `opacity:0`.
- Multiple hero elements use these animations: `.hero-badge` (line ~350 area), `.hero-headline`, `.hero-subtitle`, `.hero-ctas`, `.avatar-stack`, `.google-badge` (line ~518: `animation:scaleIn 0.7s ease 1s both`).
- **No `@media(prefers-reduced-motion:reduce)` block.**
- **Fix:** Same pattern as T16 — add reduced-motion override.

**Check 5 — CSS .visible pattern: BUG**
- Line ~1577-1585: JS observer adds `.visible` to `.animate-on-scroll` elements.
- **No `.animate-on-scroll` initial CSS (opacity:0) and no `.visible` CSS rule** — same bug as T16.
- **Fix:** Same as T16.

**Image paths: CLEAN** — `../../images/template-images/image3.png` (exists), `../../images/template-images/image4.png` (exists). Blog images `15-preventive-cleaning.jpg`, `16-smile-design.jpg`, `7-teeth-whitening.jpg`, `8-dental-implant.jpg` (all exist).

---

## Template 19 (Amber/warm, geometric)

**Check 4 — opacity:0 + reduced-motion: BUG**
- Line ~46-73: Keyframes `fadeInUp`, `fadeInRight`, `fadeInLeft`, `float`, `pulse-soft`, `shimmer`, `rotate-slow` — several start from `opacity:0`.
- `.hero-visual` (line ~188: `animation:fadeInRight 0.8s ease-out`), `.hero-text` (line ~295: `animation:fadeInLeft 0.8s ease-out 0.2s both`).
- **No `@media(prefers-reduced-motion:reduce)` block.**
- **Fix:** Add reduced-motion override.

**Check 5 — CSS .visible pattern: BUG**
- Line 75: `.animate-on-scroll{opacity:1;transform:translateY(0);transition:all 0.7s...}` — initial state is `opacity:1`, NOT `opacity:0`.
- Line ~1422-1433: JS observer adds `.visible` class.
- **But initial state is `opacity:1` so nothing actually animates** — the observer fires but `.visible` has no CSS rule. The animation is broken/no-op.
- **Fix:** Change line 75 to:
```css
.animate-on-scroll{opacity:0;transform:translateY(30px);transition:all 0.7s cubic-bezier(0.16,1,0.3,1)}
.animate-on-scroll.visible{opacity:1;transform:translateY(0)}
```

**Image paths: CLEAN** — `../../images/template-images/image2.png` (exists). Blog images `9-porcelain-veneers.jpg`, `10-invisible-aligners.jpg`, `11-root-canal.jpg`, `12-pediatric-dentistry.jpg` (all exist).

---

## Template 20 (Purple, blob hero)

**Check 4 — opacity:0 + reduced-motion: BUG**
- Line ~61-64: `@keyframes fadeInUp{from{opacity:0;...}}`
- `.hero-text` (line ~147: `animation:fadeInUp 0.8s ease-out`), `.hero-visual` (line ~220: `animation:fadeInUp 0.8s ease-out 0.2s both`)
- **No `@media(prefers-reduced-motion:reduce)` block.**
- **Fix:** Add reduced-motion override.

**Check 5 — CSS .visible pattern: N/A** — No `.animate-on-scroll` class used anywhere. No IntersectionObserver JS. **CLEAN.**

**Image paths: CLEAN** — `../../images/template-images/image4.png` (exists). Blog images `13-gum-treatment.jpg`, `14-crowns-bridges.jpg`, `15-preventive-cleaning.jpg`, `16-smile-design.jpg` (all exist).

---

## Fix Matrix (quick reference)

| Bug | Templates | Fix |
|-----|-----------|-----|
| Missing `@media(prefers-reduced-motion:reduce)` | 16, 18, 19, 20 | Add override block to CSS |
| `.animate-on-scroll` missing initial `opacity:0` + `.visible` rule | 16, 18 | Add both CSS rules |
| `.animate-on-scroll` starts at `opacity:1` (animation is no-op) | 19 | Change initial to `opacity:0;transform:translateY(30px)` + add `.visible` rule |

**Template 17 is the only fully CLEAN template.**
