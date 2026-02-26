# Segment-Template Mapping

**TL;DR:** Each of our 9 clinic segments gets a primary HTML template (+ alternates) matched to their psychology. Premium templates for best leads (4b/4a), professional for digital clinics (1/2), urgent for reputation issues (3x), and calm for minimal-presence clinics (4). Outreach channel also varies: WhatsApp+mock site for no-website clinics, email+PDF for digital ones, physical letters for reputation-sensitive segments.

---

## Mapping Table

| Segment | Clinics | Profile | Primary Template | Alternates | Outreach Channel |
|---------|---------|---------|-----------------|------------|-----------------|
| **4b** | 24 | Invisible Good, High Reviews (4.0+, no site, 10+ reviews) | `template-4-atelier` (luxury/gold) | `template-5-rosewater`, `template-6-ivory` | WhatsApp + mock landing page |
| **4a** | 37 | Invisible Good, Some Reviews (4.0+, no site, 3-10 reviews) | `template-5-rosewater` (editorial/elegant) | `template-4-atelier`, `template-10-prism` | WhatsApp + mock landing page |
| **1** | 118 | Leaky Funnel (good rating, has site, 20+ reviews) | `template-1-clarity` (clean/professional) | `template-2-prestige`, `template-10-prism` | Email + PDF report |
| **2** | 85 | Warm Digital, No Proof (good rating, has site, <20 reviews) | `template-3-warmth` (approachable/friendly) | `template-5-rosewater`, `template-6-ivory` | Email + PDF report |
| **3b** | 71 | Reputation Rescue High (<4.0, 10+ reviews) | `template-7-electric` (urgent/bold) | `template-8-aurora`, `template-9-collage` | Physical letter + WhatsApp follow-up |
| **4** | 61 | Invisible Good, Minimal (4.0+, no site, <3 reviews) | `template-6-ivory` (zen/calm) | `template-3-warmth`, `template-4-atelier` | WhatsApp + mock landing page |
| **3a** | 16 | Reputation Rescue Some (<4.0, 3-10 reviews) | `template-2-prestige` (dark/professional) | `template-7-electric` | Physical letter + WhatsApp follow-up |
| **3** | 24 | Reputation Rescue (<4.0, <3 reviews) | `template-1-clarity` (simple/clean) | -- | Physical letter + WhatsApp follow-up |
| **5** | 3 | Digitally Absent (no data) | -- | -- | In-person walk-in only |

## Template Usage Summary

| Template | Primary For | Alternate For | Total Exposure |
|----------|------------|---------------|----------------|
| `template-1-clarity` | Seg 1 (118), Seg 3 (24) | -- | 142 clinics |
| `template-2-prestige` | Seg 3a (16) | Seg 1 | 134 clinics |
| `template-3-warmth` | Seg 2 (85) | Seg 4 | 146 clinics |
| `template-4-atelier` | Seg 4b (24) | Seg 4a, Seg 4 | 122 clinics |
| `template-5-rosewater` | Seg 4a (37) | Seg 4b, Seg 2 | 146 clinics |
| `template-6-ivory` | Seg 4 (61) | Seg 4b, Seg 2 | 170 clinics |
| `template-7-electric` | Seg 3b (71) | Seg 3a | 87 clinics |
| `template-8-aurora` | -- | Seg 3b | 71 clinics |
| `template-9-collage` | -- | Seg 3b | 71 clinics |
| `template-10-prism` | -- | Seg 4a, Seg 1 | 155 clinics |

## Design Rationale (Quick Reference)

- **Best leads (4b/4a/4):** Premium aesthetics signal "we invest in quality" -- mirrors their own high standards
- **Digital clinics (1/2):** Clean professional or warm trust-building -- they already know digital, don't need flash
- **Reputation issues (3b/3a/3):** Urgency-driven or attention-grabbing -- matches the crisis they may not realize they have
- **No-website clinics get mock landing pages** as the proposal itself -- shows value instantly
- **Reputation segments get physical letters** -- sensitive topic needs gravitas, not a random WhatsApp

## Channel Logic

| Channel | Segments | Why |
|---------|----------|-----|
| WhatsApp + mock site | 4b, 4a, 4 | No website = show them what they're missing. WhatsApp is their primary digital channel. |
| Email + PDF report | 1, 2 | Already digital. Email is expected. PDF report adds professionalism. |
| Physical letter + WhatsApp | 3b, 3a, 3 | Reputation is sensitive. Physical letter = authority. WhatsApp follow-up = personal touch. |
| In-person walk-in | 5 | No data to personalize. Need manual verification first. |
