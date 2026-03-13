---
name: template-creator
description: Create a beautiful, responsive single-file HTML website template for a specific business vertical. Uses vertical research, design playbook, animation patterns, and design trends to produce production-grade templates with placeholder content. Use when building a new template for a vertical (e.g., auto repair, landscaping, dentist) — not for filling templates with real data.
---

# Template Creator

Create stunning, production-grade single-file HTML templates for a specific business vertical. The output is a reusable template that the `create-website-from-template` skill later fills with real business data.

## Trigger

- "Create a template for [vertical]"
- "Build a new [vertical] website template"
- "Design a template for auto repair shops"
- "Make a dark/bold/minimal template for [vertical]"
- "Create template variant for [vertical]"

## Prerequisites
- `vertical-research` → `research/{vertical-name}.md` must exist
- `web-design-research` → `design-inspiration/sites.csv` must exist (run at least once)

## Inputs

| Input | Required | Default |
|-------|----------|---------|
| Vertical name | Yes | — |
| Template style/variant | No | Determined from vertical research |
| Language | No | Hebrew (RTL) |
| Dark or light | No | Determined from vertical research |

---

## Step 0: Load Context (CRITICAL — read before designing)

Read ALL of these files before writing any code:

| File | Why |
|------|-----|
| `research/{vertical}.md` | Vertical-specific: color palettes, hero patterns, sections, services, psychology, anti-patterns |
| `design-inspiration/web-design-playbook.md` | **Consolidated playbook**: typography, color, hero patterns, animation stack (GSAP/Lenis/ScrollTrigger), CSS techniques, section patterns, responsive/RTL, performance/SEO, 2026 trends, anti-patterns |

Also check existing templates for this vertical:
```
ls templates/{vertical}/website/
```
Determine the next template number (e.g., if template-22 exists, create template-23).

**If the vertical research file doesn't exist**, tell the user to run the `vertical-research` skill first.

---

## Step 1: Design Decisions

Before coding, make explicit decisions for each of these. Write them as a comment block at the top of the HTML file.

### From vertical research (`research/{vertical}.md`):
- **Color palette** — pick one from the vertical's palette table
- **Hero pattern** — pick from the vertical's hero patterns list
- **Section order** — follow the vertical's "Must-Have Sections" priority order
- **Trust signals** — what Tier 1 signals to include
- **Photography style** — what the vertical's photography rules specify
- **CTA copy** — pick from the vertical's CTA patterns
- **Tone** — follow the vertical's tone of voice guidelines

### From design playbook + trends:
- **Font pairing** — pick from playbook §1 or trends §1, must match the vertical's vibe
- **Animation tier** — decide which animations to include (see Layer 4 below)
- **Effects** — which effects from the effects library (glass, gradient text, grain, etc.)

### Template identity:
- **Variant name** — descriptive (e.g., "dark-professional", "warm-community", "bold-modern")
- **Mood** — 3 adjectives that define this template's personality

Document all decisions in a design brief comment at the top of the HTML:
```html
<!--
  TEMPLATE DESIGN BRIEF
  Vertical: Auto Repair
  Variant: dark-professional
  Mood: Trustworthy, Technical, Bold
  Palette: Charcoal #1a1a1a + Red accent #E53E3E + Off-white text #f5f5f5
  Fonts: Cabinet Grotesk (display) + Inter (body)
  Hero: Full-width photo with dark overlay + trust badges
  Animation: IO reveals + GSAP hero entrance + Lenis smooth scroll
  Sections: Nav → Hero → Trust Bar → Services → About → Reviews → CTA → Footer
-->
```

---

## Step 2: Build the Template

### Architecture: Single HTML File

```
template_example-{N}.html     — Hebrew (RTL) version
template_example-{N}-en.html  — English (LTR) version (if requested)
```

Everything inline — CSS in `<style>`, JS in `<script>`, images via relative paths to shared `images/` folder.

### Required Structure

Every template MUST include these structural elements:

```html
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{Business Name} | {Primary Service} | {City}</title>
  <meta name="description" content="{SEO description with location + service}">

  <!-- Fonts — pick from design decisions -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">

  <!-- JSON-LD structured data -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "{appropriate schema type from vertical}",
    "name": "{Business Name}",
    "telephone": "{phone}",
    "address": { "@type": "PostalAddress", "addressLocality": "{city}" }
  }
  </script>

  <style>/* ALL CSS */</style>
</head>
<body>
  <!-- Sections per design decisions -->

  <!-- CDN scripts (only if GSAP/Lenis animations used) -->
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js" defer></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/ScrollTrigger.min.js" defer></script>
  <script src="https://cdn.jsdelivr.net/npm/lenis@1/dist/lenis.min.js" defer></script>

  <script>/* ALL JS */</script>
</body>
</html>
```

---

## Step 3: Apply the 7 Craft Layers

Reference the `modern-client-web-design` skill for full details. Here's the checklist:

### Layer 1: Typography
- [ ] Display + body font pairing from design decisions
- [ ] `clamp()` sizing for all headings and body
- [ ] Hero headline: tight letter-spacing (-1px to -2px), weight 700-900
- [ ] ALL-CAPS labels: `letter-spacing: 0.1em`
- [ ] RTL: use `Heebo` for Hebrew body text, display font can stay Latin

### Layer 2: Color & Theme
- [ ] CSS custom properties for all colors in `:root`
- [ ] No pure white (#fff) text — use #f5f5f5
- [ ] No pure black (#000) bg — use #0a0a0a or warmer
- [ ] Accent color from vertical palette
- [ ] Gradient or texture treatment on hero background

### Layer 3: Hero Section
- [ ] All 6 elements: eyebrow → H1 → subtitle → CTA → social proof → visual
- [ ] CTA with `tel:` link for tap-to-call
- [ ] Hero visual matches vertical's photography rules
- [ ] `min-height: 100dvh` on hero
- [ ] Staggered load animation (GSAP timeline)

### Layer 4: Scroll Animations
- [ ] Every section has entrance animation (IO-based fade+slide)
- [ ] Hero heading: GSAP timeline reveal on load
- [ ] Cards/features: stagger reveal on scroll
- [ ] `prefers-reduced-motion` CSS guard included

### Layer 5: Micro-Interactions
- [ ] Button hover: translateY(-2px) + shadow glow
- [ ] Nav link underline reveal
- [ ] Card hover: subtle lift + shadow
- [ ] Smooth scroll via Lenis (disabled on touch)

### Layer 6: Responsive Layout
- [ ] Mobile-first CSS
- [ ] Breakpoints: 768px (tablet), 1024px (desktop)
- [ ] Tested at 375px width (all content visible, no overflow)
- [ ] 48px minimum tap targets
- [ ] Hamburger menu on mobile
- [ ] Sticky mobile CTA (tap-to-call bar)
- [ ] CSS logical properties for RTL (`margin-inline-start`, `text-align: start`)

### Layer 7: Performance & SEO
- [ ] JSON-LD structured data (schema type from vertical)
- [ ] Semantic HTML: `<header>`, `<main>`, `<section>`, `<footer>`, `<nav>`
- [ ] Single `<h1>` with primary keyword + location
- [ ] `<meta description>` with service + location
- [ ] Images: `width`/`height` attributes, `loading="lazy"` below fold
- [ ] `fetchpriority="high"` on hero image
- [ ] Font: `font-display: swap`

---

## Step 4: Placeholder Content

Templates use realistic placeholder content that makes the template look complete. This content gets replaced by `create-website-from-template`.

**CRITICAL: Use EXACTLY the placeholder tokens defined in `templates/PLACEHOLDER_CONTRACT.md`.** Every replaceable value must use the `{{TOKEN_NAME}}` format from the contract. Do not invent new tokens or use ad-hoc placeholder text.

### Placeholder conventions:
- **Business name**: Use a believable name for the vertical (e.g., "מוסך אלון" for auto repair, "דנטל פלוס" for dentist)
- **Phone**: `077-000-0000`
- **Address**: Real-sounding address in a major Israeli city
- **Services**: 6 services from the vertical's services taxonomy
- **Reviews**: 3 realistic review placeholders with Hebrew names and text
- **Doctor/owner name**: Believable Hebrew name with title (ד״ר, etc.)
- **Images**: Reference paths like `images/hero.jpg`, `images/service-1.jpg`, etc.

**CRITICAL: Every piece of placeholder content must be obviously replaceable** — the `create-website-from-template` skill searches and replaces these. Use consistent naming.

---

## Step 5: Image Strategy

### Required images (template references these paths):
```
images/
├── hero.jpg          — hero background (1920x1080)
├── about.jpg         — about section photo (800x600)
├── service-1.jpg     — service card images (600x400 each)
├── service-2.jpg
├── service-3.jpg
├── service-4.jpg
├── service-5.jpg
├── service-6.jpg
├── gallery-1.jpg     — optional gallery (800x600 each)
├── gallery-2.jpg
├── gallery-3.jpg
└── og-image.jpg      — social sharing (1200x630)
```

For the template preview, use high-quality stock images from Unsplash/Pexels that match the vertical. Include the source URLs in a comment block so they can be replaced later.

---

## Step 6: Variant Support

When creating multiple variants for the same vertical, each variant should differ in:

| Dimension | Example variants |
|-----------|-----------------|
| Color mode | Dark vs. light |
| Personality | Professional vs. friendly vs. bold |
| Hero style | Photo bg vs. split layout vs. gradient |
| Layout density | Spacious/editorial vs. compact/info-dense |
| Animation level | Minimal (IO only) vs. full (GSAP + Lenis) |

Name variants descriptively: `template-23` (dark-professional), `template-24` (warm-community).

Each variant gets its own folder under `templates/{vertical}/website/template-{N}/`.

---

## Step 7: Output & File Structure

### Create this structure:
```
templates/{vertical}/website/template-{N}/
├── template_example-{N}.html        — Hebrew RTL version
├── template_example-{N}-en.html     — English LTR version (if requested)
├── template-manifest.json            — placeholder token manifest (format defined in PLACEHOLDER_CONTRACT.md)
├── blog.html                         — blog listing page (optional)
└── blog/                             — blog article pages (optional)
```

### template-manifest.json
Generate this file alongside the HTML. It lists every `{{PLACEHOLDER}}` token used in the template, its location (CSS selector or line context), and expected data type. See `templates/PLACEHOLDER_CONTRACT.md` for the exact format.

Images go in the shared `templates/{vertical}/images/` folder (or reference existing images if available).

---

## Step 8: Self-Review

Before delivering, open the template in Playwright and verify:

### Desktop (1440x900):
- [ ] All sections render correctly
- [ ] Animations fire on scroll
- [ ] Hero looks complete with all 6 elements
- [ ] No horizontal overflow
- [ ] Colors match design brief

### Mobile (375x812):
- [ ] Hamburger menu works
- [ ] All content is readable
- [ ] CTA is accessible (sticky bar or prominent button)
- [ ] No text overflow or tiny tap targets
- [ ] Images don't break layout

### Take screenshots:
- Desktop hero → `template_example-{N}-desktop.png`
- Mobile hero → `template_example-{N}-mobile.png`

---

## Output Summary

Print to chat:
```
Template created for {Vertical} — variant: {variant-name}

📁 templates/{vertical}/website/template-{N}/
📄 template_example-{N}.html (Hebrew RTL)

Design: {3-word mood} | {palette description} | {font pairing}
Sections: {list of sections included}
Animations: {animation tier summary}

Screenshots saved for review.
```

---

## Error Handling

- **No vertical research file**: Stop. Tell user to run `vertical-research` skill first.
- **Existing template number conflict**: Auto-increment to next available number.
- **User wants a style not in vertical research**: Adapt — use the vertical's content/sections but apply the requested style from the design playbook.
- **Template too large (>200KB HTML)**: Optimize — inline SVGs may need to be external, reduce animation code.
- **Playwright not available for review**: Skip self-review step, note it in output.
