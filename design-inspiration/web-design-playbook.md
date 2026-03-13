# Web Design Playbook — Consolidated Reference
**Last updated:** 2026-03-12 | **Based on:** 55+ Awwwards/Godly sites + 2026 trend research

## TL;DR
Modern award-winning websites share 5 traits: (1) typography-first hierarchy with oversized display fonts + clamp() sizing, (2) scroll-triggered animations via GSAP + Lenis + SplitType, (3) dark-first color with mesh gradients + grain, (4) full-viewport section design with bento grids, (5) micro-interactions on every interactive element. Always use CSS logical properties for RTL, JSON-LD for SEO, and `prefers-reduced-motion` for accessibility.

---

## §1 Typography

### Font Pairings

| Display (Headlines) | Body (Text) | Vibe |
|---------------------|-------------|------|
| Cabinet Grotesk | Inter | Modern SaaS |
| Clash Display | DM Sans | Bold creative |
| Playfair Display | Inter | Luxury / editorial |
| Instrument Serif | Geist | Refined tech |
| Neue Montreal | DM Sans | Clean agency |
| Syne | Geist Mono | Futuristic |
| Neue Montreal | Editorial New | Grotesque + serif elegance |
| Inter | Playfair Display | Digital workhorse + luxury |

**Rule:** ONE display + ONE body font max. Never pair two display fonts — one must anchor.

### Sizing (clamp for responsive)
```css
--h1-hero: clamp(40px, 8vw, 80px);
--h1:      clamp(32px, 5vw, 56px);
--h2:      clamp(24px, 3.5vw, 40px);
--h3:      clamp(20px, 3vw, 28px);
--body:    clamp(16px, 1.1vw, 18px);
--small:   clamp(12px, 0.9vw, 14px);
```

### Spacing

| Context | line-height | letter-spacing |
|---------|-------------|----------------|
| Hero display | 0.9–1.1 | -1px to -2px (tight) |
| Headings | 1.1–1.3 | -0.5px to 0 |
| Body text | 1.5–1.7 | 0 to 0.5px |
| ALL-CAPS labels | 1.4 | 0.1em–0.15em |
| Luxury display | 1.0 | 2–6px (expanded) |

**WCAG:** line-height >= 1.5x font-size; letter-spacing >= 0.12em for compliance.

### Hero Headline Styling
- **Weight:** 700–900 (Bold to Black)
- **Case:** Sentence case (default) or ALL-CAPS (luxury/impact)
- **Effects:** Solid color, gradient text (`background-clip: text`), stroke-only (`-webkit-text-stroke: 2px #fff`), `mix-blend-mode: difference`
- **Variable fonts:** Animate `font-variation-settings: 'wght'` on hover/scroll
- **Loading:** WOFF2 only + `font-display: swap` + `<link rel="preload">`

---

## §2 Color & Theme

### Dark Mode (Default for Premium)
```css
:root { color-scheme: light dark; }
--bg-primary:   #0a0a0a;  /* near-black — maximum premium */
--bg-secondary: #141414;  /* cards, elevated surfaces */
--bg-tertiary:  #1a1a1a;  /* hover states */
--text-primary: #f5f5f5;  /* NOT pure white */
--text-muted:   #999;
--accent:       #3B82F6;  /* swap per client */
```

**Light/dark toggle:** Use `data-theme="dark"` on `<html>` + `@media (prefers-color-scheme: dark)`.
**CSS function:** `color: light-dark(#333, #efefec);`

### Palette Archetypes

| Palette | When to Use |
|---------|-------------|
| Dark + electric blue (`#3B82F6`) | SaaS, tech (Linear, Vercel) |
| Dark + acid green (`#ADFF2F`) | Dev tools (Supabase) |
| Dark + purple gradient | Crypto, AI (Phantom) |
| Dark + warm coral (`#FF6B6B`) | Creative agency |
| Off-white + navy + gold | Luxury, finance |
| Warm pastels | Friendly SaaS (Amie) |
| Pure black + white only | Editorial/fashion |

### Gradients & Effects

**Mesh gradient:**
```css
background:
  radial-gradient(ellipse at 20% 50%, rgba(120,119,198,0.3), transparent 50%),
  radial-gradient(ellipse at 80% 20%, rgba(255,182,255,0.3), transparent 50%),
  radial-gradient(ellipse at 50% 80%, rgba(120,200,255,0.3), transparent 50%),
  var(--bg-primary);
```

**Grain overlay:**
```css
.grain::after {
  content: ''; position: fixed; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.05'/%3E%3C/svg%3E");
  pointer-events: none; z-index: 9999; opacity: 0.04;
}
```

**Glass card:**
```css
.glass-card {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(12px) saturate(1.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
}
```

**Gradient text:**
```css
.gradient-text {
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
```

---

## §3 Hero Patterns

### Content Hierarchy (always this order)
```
1. Eyebrow label     — small, uppercase, muted — "New in 2026" / "Trusted by 10,000+"
2. H1 Headline       — 6-12 words max, value prop — 56-80px desktop
3. Subheadline       — 1-2 sentences, "why care?" — 18-22px, muted color
4. CTA button(s)     — primary + optional ghost — 48px min height
5. Social proof      — "Join 50,000 teams" / logo strip / star rating
6. Hero visual       — product screenshot, video, 3D, or illustration
```

### Background Treatments (ranked)
1. **Animated mesh gradient** — lightweight, premium (Linear, Superhuman)
2. **Video loop** — muted, 5-10s, WebM preferred
3. **3D Spline/WebGL object** — product-focused
4. **Gradient + grain texture** — editorial luxury, zero perf cost
5. **Static image + overlay** — fast, reliable fallback

### Hero Load Animation
```javascript
gsap.timeline({ delay: 0.2 })
  .from('.hero-label',    { opacity: 0, y: 10, duration: 0.5 })
  .from('.hero-h1',       { opacity: 0, y: 24, duration: 0.7, ease: 'power3.out' }, '-=0.2')
  .from('.hero-sub',      { opacity: 0, y: 16, duration: 0.5 }, '-=0.4')
  .from('.hero-cta-wrap', { opacity: 0, y: 12, duration: 0.5 }, '-=0.3')
  .from('.hero-proof',    { opacity: 0, duration: 0.5 }, '-=0.2');
```

### CTA Buttons
```css
.btn-primary {
  padding: 14px 28px; font-weight: 600; background: var(--accent); color: #fff;
  border-radius: 8px; transition: transform 0.2s, box-shadow 0.2s;
}
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(59,130,246,0.4); }
.btn-ghost { padding: 14px 28px; background: transparent; border: 1.5px solid rgba(255,255,255,0.3); }
```

---

## §4 Animation Stack

### Libraries

| Library | Size | Purpose |
|---------|------|---------|
| Lenis | ~7KB | Smooth scroll (cinematic feel) |
| GSAP + ScrollTrigger | ~32KB | Scroll-triggered animations |
| SplitType | ~5KB | Text splitting for character animation |
| Framer Motion | ~45KB | React component animations |

### Lenis + GSAP Setup
```javascript
import Lenis from 'lenis';
import gsap from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

const lenis = new Lenis({
  duration: 1.2,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  smoothWheel: true,
});
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);
```
**Pitfall:** Without `lenis.on('scroll', ScrollTrigger.update)` — animations fire at wrong positions.

### Scroll Patterns
```javascript
// 1. Fade + slide up (most common)
gsap.from(".section", {
  scrollTrigger: { trigger: ".section", start: "top 80%" },
  opacity: 0, y: 40, duration: 0.8
});

// 2. Stagger cards
gsap.from(".card", {
  scrollTrigger: { trigger: ".grid", start: "top 75%" },
  opacity: 0, y: 30, stagger: 0.15, duration: 0.7
});

// 3. Parallax
gsap.to(".bg-layer", {
  scrollTrigger: { trigger: ".section", scrub: 1 },
  y: -100
});

// 4. Clip-path reveal
gsap.from(".reveal", {
  scrollTrigger: { trigger: ".reveal", start: "top 80%" },
  clipPath: "polygon(0% 100%, 100% 100%, 100% 100%, 0% 100%)",
  duration: 1
});
```

### SplitType Text Animations
```javascript
import SplitType from 'split-type';
// Always wait for fonts: document.fonts.ready.then(() => ...)

// 3D word reveal (hero headings)
const split = new SplitType('.reveal-type', { types: 'lines,words' });
gsap.from(split.words, {
  scrollTrigger: { trigger: el, start: 'top 85%' },
  yPercent: 120, rotationX: -40, opacity: 0,
  duration: 1.2, stagger: 0.04, ease: 'expo.out',
});

// Apple-style scrub opacity (body copy)
gsap.to(split.words, {
  scrollTrigger: { trigger: el, start: 'top 80%', end: 'bottom 40%', scrub: 0.5 },
  opacity: 1, stagger: 0.1
});
```

### Micro-Interactions
- **Magnetic buttons:** Element follows cursor within proximity (`mousemove` + transform)
- **Underline reveal:** `background-size: 0% 2px` to `100% 2px` on hover
- **Custom cursor:** Inner dot (instant) + outer ring (lag: 0.5s) — skip for local business sites
- **CTA hover:** `translateY(-2px)` + `box-shadow` glow

### Performance Rules

| Rule | Detail |
|------|--------|
| Safe to animate | `transform`, `opacity` only — GPU composited |
| Never animate | `width`, `height`, `top`, `left`, `margin`, `padding` |
| `will-change` | Only on persistent animated elements, never `*` |
| SplitType | Always inside `document.fonts.ready.then(...)` |
| Resize | Check `window.innerWidth` changed, kill + reinit ScrollTriggers |

### Accessibility (REQUIRED)
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  .cursor-follower { display: none !important; }
}
```
```javascript
// Gate non-essential JS animations
if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  initMagneticButtons();
}
```

---

## §5 CSS Techniques

### Container Queries — use instead of media queries for components
```css
.card-wrapper { container-type: inline-size; }
@container (min-width: 400px) { .card { flex-direction: row; } }
```

### :has() — parent/conditional styling without JS
```css
.pricing-card:has(.badge-popular) { border: 2px solid var(--accent); transform: scale(1.05); }
.form-field:has(input:invalid) label { color: red; }
```

### Native CSS Nesting — no Sass needed
```css
.nav { background: #111;
  a { color: white; &:hover { color: var(--accent); } }
}
```

### Scroll-Driven Animations (no JS)
```css
.card {
  animation: slide-fade-in linear both;
  animation-timeline: view();
  animation-range: entry 0% cover 30%;
}
@supports not (animation-timeline: view()) {
  .card { opacity: 1; transform: none; }
}
```

### Anchor Positioning (2026)
```css
.trigger { anchor-name: --btn; }
.tooltip { position: absolute; position-anchor: --btn; position-area: top;
           position-try-fallbacks: flip-block; }
```

### View Transitions API
```javascript
document.startViewTransition?.(() => updateDOM());
```
```css
.hero-img { view-transition-name: hero; }
::view-transition-old(hero) { animation: fade-out 0.25s ease-in; }
::view-transition-new(hero) { animation: scale-in 0.25s ease-out; }
```

### Native Popover (zero JS)
```html
<button popovertarget="menu">Open</button>
<div id="menu" popover><!-- content --></div>
```

### Native Dialog
```html
<dialog id="modal"><form method="dialog"><button type="submit">Close</button></form></dialog>
```

---

## §6 Section Patterns

### Recommended Page Structure
```
1. Nav          — sticky, frosted glass, logo + links + CTA
2. Hero         — full viewport (see §3)
3. Logo strip   — trust signal, marquee or static row
4. Features     — alternating split (text/visual) or icon grid (3-4 col)
5. Bento grid   — key capabilities, 1 featured large card
6. Testimonials — marquee carousel or 3-column cards
7. Pricing      — 3-tier (Starter / Pro highlighted / Enterprise)
8. FAQ          — native <details>/<summary> accordion
9. CTA section  — full-width centered, bold headline + single button
10. Footer      — logo + nav columns + social + newsletter
```

### Bento Grid
```css
.bento { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.bento-featured { grid-column: span 2; grid-row: span 2; }
```

### Testimonials Marquee
```css
.marquee-track { animation: marquee 30s linear infinite; }
@keyframes marquee { to { transform: translateX(-50%); } }
```

### Pricing — 3-Tier
- Middle card larger + colored bg + "Most Popular" badge
- Monthly/annual toggle with "Save 20%" on annual
- Each: price (48px+), feature checklist, CTA

### FAQ — Native Accordion
```html
<details><summary>Question</summary><p>Answer</p></details>
```
Add `@type: FAQPage` JSON-LD for SEO. 8-12 questions max.

### Footer
- Background: slightly different from body (`#161616` on `#111`)
- Minimal: curated links, not full nav repeat
- Optional newsletter CTA

---

## §7 Responsive & RTL

### Mobile Rules
- Hero height: `min-height: 100dvh` (not `vh` — accounts for browser chrome)
- CTA buttons: minimum 48px tap target
- Tap-to-call: always `tel:` link, sticky at bottom on mobile
- Lenis: `smoothTouch: false`
- Disable custom cursor on touch devices
- Collapse bento to single column
- Test at 375px width minimum

### RTL Support — CSS Logical Properties

| Physical (avoid) | Logical (use) |
|---|---|
| `margin-left/right` | `margin-inline-start/end` |
| `padding-top/bottom` | `padding-block-start/end` |
| `text-align: left` | `text-align: start` |

```html
<html lang="ar" dir="rtl">  <!-- layout flips automatically -->
```

---

## §8 Performance & SEO

### Core Web Vitals

| Metric | Target |
|--------|--------|
| LCP | < 1.5s (< 2.5s acceptable) |
| INP | < 200ms |
| CLS | < 0.1 |
| Total page weight | < 2MB (< 100KB for single-file) |

### Image Optimization
```html
<!-- Above fold (LCP critical) -->
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" alt="..." width="800" height="500" fetchpriority="high" decoding="sync">
</picture>

<!-- Below fold -->
<img src="feature.jpg" loading="lazy" decoding="async" width="600" height="400" alt="...">
```
- Always set `width` + `height` to prevent CLS
- AVIF ~50% smaller than WebP; WebP ~30% smaller than JPEG
- Never lazy-load the first visible image

### SEO — JSON-LD
```html
<script type="application/ld+json">
{ "@context": "https://schema.org", "@type": "LocalBusiness",
  "name": "...", "telephone": "...",
  "address": { "@type": "PostalAddress", "addressLocality": "City" } }
</script>
```
- Semantic HTML: `<header>`, `<main>`, `<section>`, `<footer>`, `<nav>`
- One `<h1>` per page with primary keyword + location
- Font loading: WOFF2 + `font-display: swap` + preload critical

---

## §9 2026 Trends

- **Mesh gradients** ascending — lightweight, premium feel replacing flat color
- **Variable font animation** — weight/axis transitions on hover/scroll
- **CSS `light-dark()` function** — native dual-theme with zero JS
- **Anchor Positioning** — tooltips/dropdowns without JS (Baseline early 2026)
- **View Transitions API** — native page transitions (Baseline 2025, 75% support)
- **Scroll-driven animations** — CSS `animation-timeline: view()` replacing IO for simple reveals
- **`@starting-style`** — entry animations for elements added to DOM
- **Brutalist typography** — uncompromising bold letterforms, Art Deco revival
- **Skeleton screens** preferred over spinners (~30% less perceived load time)
- **Glassmorphism refined** — still relevant but sparingly, on gradient/image backgrounds only

---

## §10 Anti-Patterns

- Stock photos of people shaking hands
- More than 2 fonts
- Hero without CTA above the fold
- "Welcome to our website" as headline
- Scroll-jacking entire page (2-3 snap sections max)
- Pure white `#fff` text on dark (use `#f5f5f5`)
- Pure black `#000` background (use `#0a0a0a` or `#111`)
- Animations without `prefers-reduced-motion` fallback
- Contact form as only conversion path (add click-to-call)
- Loading spinners instead of skeleton screens
- Generic icon sets (Flaticon) — use Lucide, Phosphor, or custom
- Animating `width`/`height`/`margin` — only `transform` + `opacity`
- `will-change` on `*` — kills mobile RAM
- jQuery, icon font libraries — use inline SVG
- Google Fonts CDN for single-file sites — use system-ui or embed base64

---

## Quick-Start Checklist

- [ ] Pick 1 display + 1 body font from pairing table
- [ ] Set up clamp() type scale
- [ ] Choose dark or light base palette
- [ ] Set up Lenis + GSAP + ScrollTrigger
- [ ] Build hero with 6-element hierarchy
- [ ] Add scroll-triggered fade-in to every section
- [ ] Add hover micro-interactions to buttons/links
- [ ] Use CSS logical properties for RTL support
- [ ] Build mobile-first, test at 375px
- [ ] Add `prefers-reduced-motion` media query
- [ ] Add JSON-LD structured data
- [ ] Check LCP < 1.5s, CLS < 0.1

---

*Consolidated from: web-design-playbook, animation-patterns-reference, modern-client-web-dev-research, design-trends-2026. Sources: 55+ Awwwards/Godly sites, MDN, Chrome Developers, GSAP docs, W3C WCAG 2.1.*
