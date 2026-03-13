# Website Pipeline — Improvement Plan

**Created:** 2026-03-12 | **Status:** In Progress

## TL;DR
The pipeline works end-to-end for dentists but is blocked for any other vertical. Three critical fixes unlock multi-vertical support: generalize `create-website-from-template`, define a placeholder contract, and consolidate overlapping reference files. Then we can ship auto-repair as the first non-dentist vertical.

---

## Phase 1: Unblock Multi-Vertical (CRITICAL)

| # | Task | Skill/File | Status | Depends On |
|---|------|-----------|--------|------------|
| 1.1 | Generalize `create-website-from-template` — replace all `dentists/` hardcoding with `{vertical}` param, make output path dynamic, derive schema type from vertical research | `create-website-from-template` | ✅ DONE | — |
| 1.2 | Generalize `website-from-template-audit` — remove dentist assumptions | `website-from-template-audit` | ✅ DONE | — |
| 1.3 | Define placeholder contract — `templates/PLACEHOLDER_CONTRACT.md` with exact field names (`{{BUSINESS_NAME}}`, `{{PHONE}}`, etc.) used by both template-creator and create-website | New file | ✅ DONE | — |
| 1.4 | Update `template-creator` to use placeholder contract | `template-creator` | ✅ DONE | 1.3 |
| 1.5 | Update `create-website-from-template` to read contract for deterministic replacement | `create-website-from-template` | ✅ DONE | 1.3 |
| 1.6 | Add "Prerequisites" section to each skill listing required prior skills | All 7 skills | ✅ DONE | — |
| 1.7 | Standardize vertical naming: lowercase, kebab-case, plural (`dentists`, `auto-repair`) — document in CLAUDE.md | CLAUDE.md | ✅ DONE | — |

---

## Phase 2: Consolidate Reference Files (IMPORTANT)

| # | Task | File | Status | Depends On |
|---|------|------|--------|------------|
| 2.1 | Merge `animation-patterns-reference.md` + `modern-client-web-dev-research.md` + `design-trends-2026.md` INTO `web-design-playbook.md` — one reference instead of 4 overlapping files | `design-inspiration/` | ✅ DONE | — |
| 2.2 | Update `modern-client-web-design` skill to be thin pointer to consolidated playbook | `modern-client-web-design` | ✅ DONE | 2.1 |
| 2.3 | Update `template-creator` Step 0 to read 1 file instead of 4 | `template-creator` | ✅ DONE | 2.1 |
| 2.4 | Delete the 3 merged files | `design-inspiration/` | ✅ DONE | 2.1-2.3 |

---

## Phase 3: Feedback Loop & Quality (IMPORTANT)

| # | Task | File | Status | Depends On |
|---|------|------|--------|------------|
| 3.1 | Add `template-manifest.json` output to `template-creator` — lists all placeholders, images, sections, schema type | `template-creator` | ✅ DONE (Step 7) | 1.3 |
| 3.2 | Make `create-website-from-template` read manifest for deterministic replacement | `create-website-from-template` | ✅ DONE (references PLACEHOLDER_CONTRACT) | 3.1 |
| 3.3 | Add `templates/{vertical}/feedback.md` — audit findings feed back into templates | New convention | DEFERRED (created on first audit) | — |
| 3.4 | Add `templates/INDEX.md` — master index of all templates with descriptions | New file | ✅ DONE | — |

---

## Phase 4: First Non-Dentist Vertical — Auto Repair (HIGH)

| # | Task | Skill | Status | Depends On |
|---|------|-------|--------|------------|
| 4.1 | Run `vertical-research` for auto-repair | `vertical-research` | ✅ DONE | — |
| 4.2 | Create `templates/auto-repair/` folder structure | Manual | ✅ DONE | — |
| 4.3 | Run `template-creator` — 5 variants (dark-professional, warm-community, bold-modern, clean-trust, premium-gold) | `template-creator` | ✅ DONE | Phase 1, 4.1 |
| 4.4 | Update `gallery.html` with auto-repair templates | `gallery.html` | ✅ DONE | 4.3 |
| 4.5 | End-to-end test: create website for real auto-repair shop | `create-website-from-template` | TODO | 1.1, 4.3 |
| 4.6 | Audit generated site | `website-from-template-audit` | TODO | 4.5 |

---

## Phase 5: Polish (NICE-TO-HAVE)

| # | Task | Status |
|---|------|--------|
| 5.1 | Document screenshot batch workaround (max 3 sites/agent) in `web-design-research` | TODO |
| 5.2 | Add screenshot capture to `vertical-research` (top 5 sites) | TODO |
| 5.3 | Gallery auto-discovery from folder structure instead of hardcoded JS | TODO |

---

## Completed (2026-03-12)

- Created `modern-client-web-design` skill (7 craft layers)
- Created `template-creator` skill (full workflow)
- Created `animation-patterns-reference.md` and `modern-client-web-dev-research.md`
- Captured 15 site screenshots (desktop + mobile)
- Restructured templates: `Dentists/templates/` → `templates/{vertical}/`
- Fixed all path references (skills, Python scripts, galleries)
- Created unified cross-vertical `templates/gallery.html`
- Added pipeline documentation to CLAUDE.md

---

## Recommended Execution Order

```
1.3 (placeholder contract) ──→ 1.4 + 1.5 (update skills)
                            └→ 3.1 (manifest) → 3.2

1.1 + 1.2 (generalize skills) → 4.5 (e2e test)

1.6 + 1.7 (prerequisites + naming)

2.1 → 2.2 → 2.3 → 2.4 (consolidate files)

4.1 (research) → 4.3 (templates) → 4.4 (gallery) → 4.5 (test) → 4.6 (audit)
```
