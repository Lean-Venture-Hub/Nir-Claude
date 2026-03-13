# Templates Index

Master index of all templates across verticals.

## Dentists (22 templates)

| # | Variant | Style | Folder |
|---|---------|-------|--------|
| 2-22 | Various | Professional, warm, modern, bold | `dentists/website/template-{N}/` |

**Gallery:** `gallery.html` → Dentists tab

## Proposals (10 templates)

| # | Name | Style |
|---|------|-------|
| 1 | Clarity | Clean, minimal |
| 2 | Prestige | Dark, premium |
| 3 | Warmth | Soft, approachable |
| 4 | Atelier | Elegant, editorial |
| 5 | Rosewater | Pink accent, feminine |
| 6 | Ivory | Light, classic |
| 7 | Electric | Bold, neon accents |
| 8 | Aurora | Gradient, colorful |
| 9 | Collage | Photo-forward, magazine |
| 10 | Prism | Geometric, modern |

**Location:** `proposals/`

## Auto Repair (0 templates — pending)

Planned variants: dark-professional, warm-community

## Adding a New Template

1. Run `vertical-research` for the vertical (if not done)
2. Run `template-creator` → outputs to `templates/{vertical}/website/template-{N}/`
3. Update this INDEX.md
4. Update `gallery.html` verticals config

## Conventions

- Placeholder tokens: see `PLACEHOLDER_CONTRACT.md`
- Naming: lowercase, kebab-case, plural (`dentists`, `auto-repair`)
- Each template folder contains: `template_example-{N}.html`, optional `-en.html`, optional `template-manifest.json`
