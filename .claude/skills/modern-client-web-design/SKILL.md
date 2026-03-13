---
name: modern-client-web-design
description: Build fine-crafted, production-grade single-file websites with premium animation, typography, responsive layout, and micro-interactions. Use when generating HTML websites, building templates, or when the user wants a polished modern site — not for research/inspiration gathering.
---

# Modern Client Web Design

Build premium single-file HTML websites with the craft level of Awwwards/Godly sites — focused on animation, typography, responsive layout, and micro-interactions.

## Trigger

- "Build a website for [client]"
- "Create a landing page"
- "Make this site feel more premium"
- "Add animations to this template"
- "Improve the design quality of this site"

## Prerequisites
- This skill is a reference loaded by `template-creator`. No prerequisites needed to read it, but `web-design-research` should have been run to populate the reference files in `design-inspiration/`.

## Reference Files (READ before building)

| File | What it contains |
|------|-----------------|
| `design-inspiration/web-design-playbook.md` | **Consolidated playbook**: typography, color, hero patterns, animation stack (GSAP/Lenis), CSS techniques, section patterns, responsive/RTL, performance/SEO, 2026 trends, anti-patterns |
| `design-inspiration/sites.csv` | 57+ analyzed sites with hero types, color palettes, animation techniques |
| `design-inspiration/screenshots/` | Desktop + mobile hero screenshots of 15 reference sites |

---

## Architecture: Single-File HTML

Every site is one `.html` file. No build tools, no frameworks, no external CSS files.

```
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Brand | Service | City</title>
  <style>/* ALL CSS */</style>
</head>
<body>
  <!-- ALL HTML -->
  <script>/* ALL JS — GSAP/Lenis via CDN only if needed */</script>
</body>
</html>
```

**CDN includes (only when animations require them):**
```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/ScrollTrigger.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1/dist/lenis.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/split-type@0.3/umd/index.min.js" defer></script>
```

---

## The 7 Craft Layers

Every site you build MUST address all 7 layers. This is what separates generic from premium.

### Layer 1: Typography

**Rules (from playbook §1):**
- Pick exactly 1 display + 1 body font (or use system-ui for performance)
- Hero headline: `clamp(40px, 8vw, 80px)`, weight 700-900, letter-spacing -1px to -2px
- Body: `clamp(16px, 1.1vw, 18px)`, line-height 1.5-1.7
- ALL-CAPS labels: letter-spacing 0.1em-0.15em
- Never pure white text on dark — use `#f5f5f5`

**Implementation pattern:**
```css
:root {
  --font-display: 'Cabinet Grotesk', system-ui, sans-serif;
  --font-body: 'Inter', system-ui, sans-serif;
  --h1-hero: clamp(40px, 8vw, 80px);
  --h2: clamp(24px, 3.5vw, 40px);
  --body: clamp(16px, 1.1vw, 18px);
}
h1 { font-family: var(--font-display); font-size: var(--h1-hero); line-height: 0.95; letter-spacing: -1.5px; }
```

### Layer 2: Color & Theme

**Rules (from playbook §3):**
- Dark default for premium: `--bg: #0a0a0a`, `--surface: #141414`, `--text: #f5f5f5`
- One accent color derived from brand
- Gradient accents via `radial-gradient` mesh (not flat backgrounds)
- Grain overlay at 0.03-0.05 opacity for texture

**Dark mode support:**
```css
:root { color-scheme: light dark; }
```
See `web-design-playbook.md` §5 (CSS Techniques) for full implementation.

### Layer 3: Hero Section

**The 6-element hierarchy (from playbook §2):**
1. Eyebrow label — small, uppercase, muted
2. H1 headline — 6-12 words, value prop
3. Subheadline — 1-2 sentences
4. CTA button(s) — primary + optional ghost
5. Social proof — rating, logo strip, or count
6. Hero visual — screenshot, video, gradient, or 3D

**Load animation (staggered reveal):**
```js
gsap.timeline({ delay: 0.2 })
  .from('.hero-label', { opacity: 0, y: 10, duration: 0.5 })
  .from('.hero-h1', { opacity: 0, y: 24, duration: 0.7, ease: 'power3.out' }, '-=0.2')
  .from('.hero-sub', { opacity: 0, y: 16, duration: 0.5 }, '-=0.4')
  .from('.hero-cta', { opacity: 0, y: 12, duration: 0.5 }, '-=0.3')
  .from('.hero-proof', { opacity: 0, duration: 0.5 }, '-=0.2');
```

### Layer 4: Scroll Animations

**Tiered approach (from web-design-playbook.md §4):**

| Element | Technique | Weight |
|---------|-----------|--------|
| Hero heading | GSAP + SplitType word reveal | ~40KB CDN |
| Section headings | CSS `animation-timeline: view()` | 0KB |
| Cards/features | Intersection Observer + CSS transition | 0KB |
| Background layers | GSAP parallax with `scrub: 1` | included |

**Always include reduced motion guard:**
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Layer 5: Micro-Interactions

The details that make it feel alive:

- **Button hover:** `translateY(-2px)` + subtle box-shadow glow in accent color
- **Nav link underline:** `background-size: 0% 2px → 100% 2px` on hover
- **Card hover:** slight `translateY(-4px)` + shadow increase
- **CTA glow:** `box-shadow: 0 0 20px rgba(accent, 0.3)` on hover
- **Smooth scroll:** Lenis with `duration: 1.2` (skip on touch devices)

See `web-design-playbook.md` §4 for code.

### Layer 6: Responsive Layout

**Rules:**
- Mobile-first: `min-height: 100dvh` (not `vh`)
- Use CSS logical properties for RTL support (`margin-inline-start`, `text-align: start`)
- Container queries for component-level responsiveness
- CTA buttons: 48px minimum tap target
- Sticky tap-to-call on mobile
- Collapse grids to single column at 768px
- Test at 375px minimum

**Key breakpoints:**
```css
/* Mobile-first, then: */
@media (min-width: 768px)  { /* tablet */ }
@media (min-width: 1024px) { /* desktop */ }
@media (min-width: 1440px) { /* wide */ }
```

### Layer 7: Performance & SEO

**Targets:**
- Total page weight < 2MB (< 100KB without images)
- LCP < 1.5s
- CLS < 0.1
- System fonts preferred; if custom, use WOFF2 + `font-display: swap` + preload
- Images: AVIF > WebP > JPEG, `fetchpriority="high"` on hero, `loading="lazy"` below fold
- JSON-LD structured data (MedicalClinic, LocalBusiness, etc.)

See `web-design-playbook.md` §8 for full details.

---

## Section Build Order

Follow this order for every site (from playbook §5):

```
1.  Nav — sticky, frosted glass (backdrop-filter: blur(12px))
2.  Hero — full viewport, 6-element hierarchy
3.  Logo strip / trust bar — infinite marquee or static
4.  Features — alternating split layout (text ↔ visual)
5.  Bento grid — capabilities with 1 featured large card
6.  Testimonials — marquee or 3-column cards
7.  Pricing — 3-tier with highlighted middle (if applicable)
8.  FAQ — native <details>/<summary> accordion
9.  CTA — full-width, bold headline + single button
10. Footer — logo + nav columns + social + newsletter
```

Not every site needs all 10. Minimum viable: Nav + Hero + Features/Services + CTA + Footer.

---

## Effects Library (use sparingly)

| Effect | CSS |
|--------|-----|
| Glass card | `background: rgba(255,255,255,0.06); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1);` |
| Specular border | `box-shadow: 0 0 0 1px rgba(120,119,198,0.2), 0 0 40px rgba(120,119,198,0.06);` |
| Gradient text | `background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; color: transparent;` |
| Grain overlay | `::after` with SVG fractalNoise at `opacity: 0.04` |
| Marquee | `animation: marquee 30s linear infinite; @keyframes marquee { to { translateX(-50%) } }` |

---

## Anti-Patterns (from playbook §9)

NEVER do these:
- Stock photos of handshakes or pointing at screens
- More than 2 fonts
- Hero without CTA above the fold
- "Welcome to our website" headline
- Full-page scroll-jacking
- Pure white `#fff` text on dark (use `#f5f5f5`)
- Pure black `#000` background (use `#0a0a0a`)
- Animations without `prefers-reduced-motion`
- Contact form as only conversion path (add click-to-call)
- Generic icon sets — use Lucide, Phosphor, or inline SVG

---

## Quality Checklist

Before delivering any site, verify:

- [ ] Typography: display + body fonts set, clamp() sizing, tight hero letter-spacing
- [ ] Color: no pure white/black, accent color applied, gradient or texture on hero bg
- [ ] Hero: all 6 elements present, staggered load animation
- [ ] Scroll: every section has entrance animation (IO or CSS scroll-driven)
- [ ] Hover: all buttons/links have micro-interaction
- [ ] Mobile: tested at 375px, 48px tap targets, `100dvh`, sticky CTA
- [ ] RTL: logical properties used if Hebrew/Arabic
- [ ] Performance: images optimized, LCP image has `fetchpriority="high"`, system fonts or preloaded WOFF2
- [ ] SEO: JSON-LD, semantic HTML, meta description, single `<h1>`
- [ ] A11y: `prefers-reduced-motion` guard, sufficient color contrast, keyboard navigable
