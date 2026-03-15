# PRD: Scalefox Mini CRM

**TL;DR:** Turn the directory page into a lightweight sales CRM — single HTML file, no backend, localStorage for all state. Core value: know exactly who to contact next and what happened last time.

## 1. Problem Statement

You're doing outreach to 100+ local businesses across verticals. Right now you have a directory with status dropdowns but no way to:
- See when you last contacted someone or what was said
- Know who's overdue for a follow-up
- Track which leads are hottest (high reviews + responded)
- See pipeline value at a glance

Without this, leads fall through cracks and outreach becomes random instead of systematic.

## 2. Goals

| Goal | Metric |
|------|--------|
| Never forget a follow-up | 0 leads stuck in "Reached Out" for >7 days without action |
| Prioritize effectively | Top 10 "contact next" list always visible |
| Log every interaction in <10 sec | Activity log per lead with one-click templates |
| See pipeline health at a glance | Dashboard with counts per stage + conversion rates |

## 3. Non-Goals (v1)

- **No email sending from CRM** — use Gmail, just log that you sent it
- **No multi-user / auth** — solo operator, localStorage is fine
- **No backend / API** — everything client-side, export/import JSON for backup
- **No calendar integration** — just show "days since last contact"
- **No automated sequences** — manual outreach, CRM just tracks it

## 4. User Stories (Priority Order)

1. **As the operator, I want to see a prioritized "Contact Next" queue** so I don't waste time deciding who to call
2. **As the operator, I want to log a quick note after each interaction** so I remember context next time
3. **As the operator, I want to see days since last contact on each card** so overdue follow-ups are obvious
4. **As the operator, I want a pipeline summary bar** so I know how my funnel looks at a glance
5. **As the operator, I want to export/import all CRM data as JSON** so I never lose my work
6. **As the operator, I want to schedule a follow-up date** so the card surfaces at the right time
7. **As the operator, I want to filter by "needs follow-up today"** so my daily workflow is clear

## 5. Requirements

### P0 — Must Ship

#### 5.1 Activity Log per Lead
- Click a lead → slide-out panel or inline expand shows interaction history
- Quick-add: dropdown for type (Email / Call / SMS / Note) + text field + timestamp
- Each entry: `{type, text, date, auto-generated}` stored in localStorage keyed by slug
- Show last activity date and type on the card itself
- **Acceptance:** Can add a note, close panel, reopen — note persists

#### 5.2 "Days Since Last Contact" Badge
- Each card shows colored badge: green (0-3 days), yellow (4-7), red (8+), gray (never)
- Calculated from most recent activity log entry
- **Acceptance:** Adding a note updates the badge immediately

#### 5.3 Pipeline Dashboard Bar
- Horizontal bar at top showing: `Cold (45) → Reached Out (20) → Responded (8) → Meeting (3) → Closed (1)`
- Click a stage to filter to that stage
- Shows conversion % between stages
- **Acceptance:** Changing a lead's status updates the bar in real-time

#### 5.4 "Contact Next" Smart Queue
- Sortable priority view combining: status weight + days since contact + review count
- Formula: `priority = statusWeight * 10 + daysSinceContact * 2 + reviewCount / 100`
- Status weights: Responded=5, Reached1=4, Reached2=3, Cold=2, Meeting=1
- Top 10 shown in a pinned section above the grid
- **Acceptance:** Lead that responded 3 days ago ranks above cold lead contacted yesterday

#### 5.5 Data Export/Import
- "Export" button → downloads all localStorage CRM data as `scalefox-crm-backup-{date}.json`
- "Import" button → file picker, merges/overwrites localStorage
- Auto-export reminder if no backup in 7+ days (subtle banner)
- **Acceptance:** Export on browser A, import on browser B — all statuses, notes, follow-ups restored

### P1 — Should Ship

#### 5.6 Follow-Up Date Scheduling
- Date picker per lead: "Follow up on [date]"
- Filter: "Due today" / "Overdue" / "Upcoming (next 3 days)"
- Visual indicator on card when follow-up is today or overdue
- Stored in localStorage alongside status

#### 5.7 Quick Action Templates
- Pre-filled note templates: "Sent intro email", "Left voicemail", "Sent proposal link", "Followed up — no response"
- One click to log common actions instead of typing
- Configurable (add/edit templates in a settings panel)

#### 5.8 Lead Scoring Visual
- Show a small score badge (1-100) on each card based on: review count, rating, has email, has social, response history
- Color-coded: hot (red/orange), warm (yellow), cool (blue)

### P2 — Future

- **Email template compose** — draft emails within CRM with variable substitution ({name}, {city})
- **Bulk actions** — select multiple leads, change status or log note
- **Vertical-specific pipeline views** — separate funnels per vertical
- **Revenue tracking** — deal value per lead, total pipeline value
- **Chrome extension** — log interactions from Gmail/LinkedIn without switching tabs

## 6. Technical Approach

**Architecture:** Single HTML file, all state in localStorage.

```
localStorage keys:
  scalefox_crm_statuses    → {slug: status}           (existing)
  scalefox_crm_activities  → {slug: [{type,text,date}]}  (new)
  scalefox_crm_followups   → {slug: "YYYY-MM-DD"}       (new)
  scalefox_crm_settings    → {templates: [...]}          (new)
```

**UI Layout Changes:**
```
┌─────────────────────────────────────────┐
│  Header: Scalefox CRM                   │
├─────────────────────────────────────────┤
│  Pipeline Bar: Cold(45) → Reached(20)...│
├─────────────────────────────────────────┤
│  Contact Next (top 10 priority leads)   │
├─────────────────────────────────────────┤
│  Search + Filters (existing + new)      │
├─────────────────────────────────────────┤
│  Grid of cards (enhanced)               │
│  ┌──────────┐ ┌──────────┐             │
│  │ Name  [5d]│ │ Name  [2d]│             │
│  │ Status ▾  │ │ Status ▾  │             │
│  │ ph / email│ │ ph / email│             │
│  │ [+Note]   │ │ [+Note]   │             │
│  └──────────┘ └──────────┘             │
└─────────────────────────────────────────┘
```

## 7. Implementation Order

| Phase | What | Effort |
|-------|------|--------|
| 1 | Pipeline bar + days-since badge | ~1 session |
| 2 | Activity log (add/view notes per lead) | ~1 session |
| 3 | Contact Next smart queue | ~0.5 session |
| 4 | Export/Import | ~0.5 session |
| 5 | Follow-up scheduling + quick templates | ~1 session |

## 8. Open Questions

- **Data size risk:** localStorage caps at ~5-10MB. At 100 leads × 50 notes each ≈ 500KB — safe. At 1000+ leads may need IndexedDB migration. → Non-blocking, monitor.
- **Multi-device sync:** localStorage is browser-local. Export/import covers this for now. If needed later, could add a simple JSON endpoint on the server. → P2.
