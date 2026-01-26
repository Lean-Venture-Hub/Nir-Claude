# GTM-UI App Documentation for UX Review

## 1. Screen Inventory

| Screen Name | Route | Purpose | Key Components |
|-------------|-------|---------|----------------|
| SignUpPage | `/auth/signup` | User registration | OAuth buttons, email form |
| Home | `/home` | Primary dashboard | ActionCards, DashboardSection |
| Competitors | `/competitors` | Track competitors (Onboarding Step 2) | CompetitorsList, AddDialog |
| Audience | `/audience` | Select ICP personas (Step 3) | PersonaCards, PersonaModal |
| Brand | `/brand` | Brand asset management | LogoGrid, ColorPicker |
| BrandSettings | `/brand-settings` | Brand configuration | FontSelector, AssetUpload |
| MarketAnalysis | `/market` | Market trends | Charts, TrendCards |
| ICP | `/icp` | Detailed ICP definition | PersonaDetails, EditForm |
| Insights | `/insights` | Multi-tab analysis dashboard | TabNav, 5 sections |
| GTMPlaybook | `/gtm-playbook` | GTM strategy playbook | StrategyCards |
| Strategy | `/strategy` | Strategic recommendations | RecommendationCards |
| AdCreator | `/concept-maker` | Primary ad studio | MasonryGrid, ActionBar |
| MediaEditor | `/media-editor` | Video/image generation | MediaCanvas, ToolPanel |
| TextEditor | `/text-editor` | Ad copy editing | TextArea, Suggestions |
| SmartAdLibrary | `/smart-ad-library` | Competitor ads with filters | SmartFilters, MasonryGrid |
| SmartAdLibrary | `/hooks` | Hook-based ad library | HooksGrid, FilterTags |
| InspirationBook | `/inspiration-book` | Curated inspiration | InspirationGrid |
| Favorites | `/favorites` | User's favorited ads | FavoritesGrid |
| Publish | `/publish` | Export campaign assets | MediaGrid, CopyTable |
| CampaignPlanner | `/campaign-planner` | Campaign organization | PlannerBoard |
| Settings | `/settings` | Account/team settings | TabNav, Forms |
| Plans | `/plans` | Pricing & subscription | PricingCards |
| OnboardingFlow | `/onboarding/*` | 4-step setup wizard | StepIndicator |
| NotFound | `*` | 404 error page | ErrorMessage |

## 2. User Flows

### Onboarding Flow
```
SignUp → Company (Step 1) → Competitors (Step 2, min 3)
→ Personas (Step 3, 2-4) → Analysis Runs → Insights (Step 4)
```

### Core Ad Creation
```
/concept-maker → ActionBar → Select Format → Enter Prompt
→ Generate → Ads in Grid → Hover Actions → Favorite
→ /favorites → /publish → Download
```

### Competitor Intelligence
```
/competitors → Add URLs → Analyze → /smart-ad-library
→ Filter → Click ad → Remix with brand
```

### Publishing
```
Create ads → Favorite best → /publish → Download all + CSV
```

## 3. Menu Structure

### Sidebar Navigation (SideNav)
Collapsible left sidebar with accordion-style grouped navigation.

```
┌─────────────────────────────────────┐
│  [Logo] ← Click to collapse/expand  │
├─────────────────────────────────────┤
│  🏠 Home                    /home   │
├─────────────────────────────────────┤
│  ⚙️ Setup                           │
│    ├─ Competitors      /competitors │
│    ├─ Audience Personas   /audience │
│    └─ Brand          /brand-settings│
├─────────────────────────────────────┤
│  📊 GTM Analysis                    │
│    ├─ Market Insights       /market │
│    ├─ Audience Deep Dive       /icp │
│    └─ GTM Playbook     /gtm-playbook│
├─────────────────────────────────────┤
│  📚 AI Ad Library                   │
│    ├─ Smart Library /smart-ad-library│
│    ├─ Hooks                  /hooks │
│    ├─ Inspiration Book              │
│    │            /inspiration-book   │
│    └─ Landing Pages  /landing-pages │
├─────────────────────────────────────┤
│  ✏️ Create                          │
│    ├─ Ads Studio     /concept-maker │
│    ├─ Favorites          /favorites │
│    └─ All Media          /all-media │
├─────────────────────────────────────┤
│  🚀 Publish                         │
│    └─ Campaign Assets      /publish │
├─────────────────────────────────────┤
│  [Generation Status Banner]         │
│  [Invite & Earn Chip]               │
│  [Credits Display]                  │
│  [User Profile → Settings, Plans]   │
└─────────────────────────────────────┘
```

### Sidebar Bottom Section
| Element | Purpose | States |
|---------|---------|--------|
| Generation Status | Shows active ad/video generations | hidden, generating (spinner), complete (green), failed (red) |
| Invite Chip | Invite & earn referrals | default, collapsed (icon only) |
| Credits Chip | Display remaining credits | default, low-credits warning |
| User Profile | User avatar + dropdown | collapsed (avatar), expanded (name + email) |

### User Profile Dropdown
- Settings → `/settings`
- Plans → `/plans`
- Logout

### Navigation Behavior
- **Accordion:** Only one section expanded at a time
- **Active State:** Current route highlighted with accent color
- **Collapsed Mode:** Icons only, tooltips on hover
- **Mobile:** Hidden sidebar, hamburger menu in TopBar

## 4. Component Library

| Component | Used On | States |
|-----------|---------|--------|
| AdCard | AdCreator, Libraries | default, hover, loading, favorited |
| ConceptsList | AdCreator | default, empty, loading |
| PersonaCard | Audience, ICP | default, selected, editing |
| MasonryGrid | AdCreator, Libraries | default, loading, empty |
| TabNav | Insights, Settings | default, active, disabled |
| FilterBar | Libraries | default, active-filters |
| Dialog/Modal | Global | open, loading-content |
| Toast | Global | success, error, loading |
| Spinner | Global | small, medium, large |
| Button | Global | default, hover, loading, disabled |
| ActionBar | AdCreator | collapsed, expanded, generating |
| LoadingScreen | Analysis flows | spinning, with-status |
| EmptyState | All lists | no-data, with-cta |
| FavoriteButton | AdCards | default, favorited |
| SmartFilterDropdown | Libraries | closed, open, active |

## 5. Screen Details

### Competitors (`/competitors`)
- **Purpose:** Manage competitor list (Onboarding Step 2)
- **Layout:** List view + add dialog
- **Elements:** URL input, Competitor cards, Edit/Delete, Analyze CTA
- **States:** Empty, Loading (analysis), Default
- **Empty:** "No competitors added yet" + Add button
- **Actions:** Add URL, Edit, Delete, Start analysis
- **Nav:** → Audience, SmartAdLibrary

### Audience (`/audience`)
- **Purpose:** Select ICP personas (Onboarding Step 3)
- **Layout:** Selected + Suggested sections
- **Elements:** PersonaCards, Follow buttons, PersonaModal
- **States:** Loading, Empty, Analysis-running, Default
- **Empty:** "Select 2-4 personas to continue"
- **Actions:** Follow/Unfollow, Edit persona
- **Nav:** → Insights, ICP

### AdCreator (`/concept-maker`)
- **Purpose:** Primary ad generation studio
- **Layout:** Masonry grid + Floating ActionBar
- **Elements:** ConceptsList, Grid, ActionBar, ViewOptions, Sort
- **States:** Empty, Loading, Generating, Onboarding-draft, Default
- **Empty:** "Create your first ad" + Generate button
- **Actions:** Generate, Edit, Favorite, Delete, Variations
- **Nav:** → Favorites, Publish, MediaEditor

### SmartAdLibrary (`/smart-ad-library`)
- **Purpose:** Browse competitor ads with smart filters
- **Layout:** Filter bar + Masonry grid
- **Elements:** Filters, AdCards, HookDetailDialog
- **States:** Loading, Empty (no matches), Default
- **Empty:** "No ads match filters" + Clear button
- **Actions:** Filter, View details, Remix, Favorite
- **Nav:** → AdCreator, Favorites

### Insights (`/insights`)
- **Purpose:** Multi-tab analysis dashboard
- **Layout:** Scroll-synced tabs + Sections
- **Elements:** 5 tabs (Overview, Executive, Competitor, Ads, Strategic)
- **States:** Loading, Error, Default
- **Error:** "Failed to load" + Retry button
- **Actions:** Navigate tabs, Scroll sections
- **Nav:** → Strategy, GTMPlaybook

### Favorites (`/favorites`)
- **Purpose:** View favorited ads
- **Layout:** Grid view
- **Elements:** FavoritesGrid, AdCards
- **States:** Loading, Empty, Default
- **Empty:** "No favorites yet. Star ads you love!"
- **Actions:** Remove, Go to Publish
- **Nav:** → Publish, AdCreator

### Publish (`/publish`)
- **Purpose:** Export campaign assets
- **Layout:** Media grid + Copy table
- **Elements:** DownloadAll, CSV export, Copy buttons
- **States:** Loading, Empty, Default
- **Empty:** "No favorited ads to publish"
- **Actions:** Download all, Export CSV, Copy text
- **Nav:** → Favorites

### Settings (`/settings`)
- **Purpose:** Account & preferences
- **Layout:** Tab nav + Form content
- **Elements:** Tabs (Account/Team/Prompts/Invite), Forms
- **States:** Loading, Saving, Default
- **Actions:** Update profile, Change password, Customize prompts
- **Nav:** → Plans

## 6. Data Flow

### Data by Screen
| Screen | Fetched | Inputs | Saved |
|--------|---------|--------|-------|
| Competitors | competitors | URL input | URLs, analysis |
| Audience | personas | Edit form | selections |
| AdCreator | concepts, ads | Prompt, images | ads, favorites |
| SmartAdLibrary | competitor_ads | Filters | favorites |
| Insights | analysis_results | None | None |
| Favorites | user_favorites | None | unfavorites |
| Publish | favorited_ads | None | None |
| Settings | user, prompts | Profile form | updates |

### WebSocket Events
| Event | Updates |
|-------|---------|
| `competitor_analysis` | Insights, SmartAdLibrary |
| `persona_suggestions` | Audience |
| `video_generation` | AdCreator media |
| `step_completion` | LoadingScreen |

### Local Storage
| Key | Purpose |
|-----|---------|
| `accessToken` | Auth token |
| `user` | User object |
| `sessionIds` | WebSocket tracking |

## Edge Cases & Empty States

| Screen | Empty Condition | Message | CTA |
|--------|-----------------|---------|-----|
| AdCreator | No concepts | "Create your first ad" | Generate |
| Favorites | No favorites | "Star ads you love" | Go to AdCreator |
| Publish | No favorites | "Favorite ads first" | Go to Favorites |
| Competitors | No competitors | "Add competitors" | Add button |
| Audience | No selection | "Select 2-4 personas" | Suggested list |
| SmartAdLibrary | No matches | "No ads match" | Clear filters |

## Error States

| Error | Trigger | Response |
|-------|---------|----------|
| 401 | Token expired | Auto-refresh + retry |
| 402 | No credits | Global credit modal |
| Network | API unreachable | Toast + retry |
| Validation | Invalid input | Inline error |
| Analysis | Backend error | Error screen + retry |

## Credit System Edge Cases
- **Insufficient:** 402 → Modal (OnboardingOutOfCreditModal / OnARollModal)
- **Reservation Timeout:** 5-min auto-cleanup
- **Spam Prevention:** Max 5 ops in 2 seconds

---

## 7. Additional UX Details

### Mobile Behavior

**Responsive Breakpoints:**
- `sm:` ~640px | `md:` ~768px | `lg:` ~1024px | `xl:` ~1280px

**Mobile-Specific Patterns:**
| Component | Desktop | Mobile |
|-----------|---------|--------|
| SideNav | Collapsible sidebar | Hidden, hamburger in TopBar |
| ActionBar | Full controls visible | Condensed, "More" dropdown |
| Settings tabs | Horizontal tabs | Dropdown select |
| Generation status | In sidebar | In TopBar |
| Smart Context toggle | Inline chip | Inside "More" menu |
| Video controls | All visible | Duration only, rest in "More" |

**Hook:** `useIsMobile()` - returns true below 768px

---

### ActionBar Details (`AdCreationActionBar`)

**Position:** Fixed bottom, respects sidebar width

**States:**
| State | Visual |
|-------|--------|
| Default | Dark glass bg, muted border |
| Focused | Purple border + ring glow |
| Drag over | Purple border, scale 1.02, lighter bg |
| Flashing | Purple highlight (600ms animation) |
| Triggering | Scale 0.98 press effect |

**Controls (Image Mode):**
- `[+]` Upload images button
- Prompt textarea (auto-resize)
- Smart Context toggle + popover (Brand DNA, Company, Market)
- Format dropdown: 1:1, 9:16, 16:9, 4:5
- More menu: Temperature slider, Language, Use Logo, Edit Ad, Model
- **Create X Ad(s)** button

**Controls (Video Mode):**
- Start/End frame upload zones (drag-drop enabled)
- Duration: 4s, 6s, 8s (locked to 8s with both frames)
- Resolution: 720p, 1080p
- Model: veo3.1 fast, veo 3.1Pro
- Format: 9:16, 16:9 only

**Image/Video Toggle:** Dropdown at end of action row

---

### Onboarding Step Screens

| Step | Route | Screen | User Task |
|------|-------|--------|-----------|
| 1 | `/onboarding/company` | CompanyInfoPage | Enter company name, website, description |
| 2 | `/onboarding/competitors` | CompetitorInfoPage | Add 3+ competitor URLs |
| 3 | `/onboarding/icp` | ICPPage | Select 2-4 personas from suggestions |
| 4 | `/onboarding/brand` | BrandPage | Upload logo, pick colors (optional) |
| 5 | `/onboarding/loader` | LoaderPage | Wait for analysis (game/video gallery) |
| 6 | `/onboarding/effective` | EffectivePage | View effective themes results |
| 7 | → `/concept-maker` | AdCreator | View draft ads (step 10) |

**LoaderPage Variants:**
- **Desktop:** FoxGame (interactive game during wait)
- **Mobile:** VideoGalleryLoader (scrolling video gallery)

---

### Loading Patterns

| Pattern | Used Where | Visual |
|---------|------------|--------|
| Full-screen spinner | Insights, Analysis flows | `LoadingScreen` with status message |
| Skeleton cards | Ad grids (not currently used) | `Skeleton` component available |
| Inline spinner | Buttons, small areas | `Spinner` component (sizes 1-3) |
| Progress indicator | Ad generation | Spinner in ActionBar button |
| Optimistic update | Favorites toggle | Instant UI, API in background |

**Note:** Skeleton component exists (`ui/skeleton.tsx`) but app primarily uses spinner-based loading.

---

### Toast Behavior

**Library:** Sonner (via `sonner` package)

**Usage Pattern:**
```
toast.success('Message')
toast.error('Message')
toast.success('Message', { duration: 2000 })
```

**Behavior:**
- **Position:** Bottom-right (default Sonner)
- **Duration:** Default ~4s, custom via `duration` prop
- **Stacking:** Auto-stacks multiple toasts
- **Styling:** Theme-aware (dark mode), subtle shadow

**Common Toast Contexts:**
| Action | Toast Type | Example |
|--------|------------|---------|
| Add competitor | success | "Competitor added successfully!" |
| Toggle favorite | success | "Added to favorites" / "Removed from favorites" |
| API failure | error | "Failed to add competitor. Please try again." |
| Credit issue | error | "Insufficient credits" (with description) |
| Board created | success | `Board "${name}" created` |

---

### Micro-interactions

**Hover Effects:**
| Element | Effect |
|---------|--------|
| AdCard | Border color change to purple, shadow glow |
| Buttons | `hover:bg-*` color shift, `hover:scale-[1.02]` |
| Filter chips | Border/text color brighten |
| Nav items | Background highlight, text brighten |
| Favorite button | Color fill (yellow/rose) |

**Transitions:**
- **Duration:** `transition-all duration-200` (standard)
- **Cards:** `duration-300` for smoother feel
- **ActionBar:** `duration-[240ms]` custom timing

**Animations:**
| Animation | Usage |
|-----------|-------|
| `animate-in fade-in` | Image previews appearing |
| `animate-in slide-in-from-bottom-2` | ActionBar content |
| `animate-in zoom-in` | New images added |
| `animate-pulse` | Button during generation |
| `scale-[0.98]` | Button press feedback |
| Flash effect | 600ms purple highlight on drag start |

**Drag & Drop:**
- ActionBar highlights on drag over
- Target zones (start/end frame) show purple border
- Smart fill: drops to first empty slot

---

## 8. Screenshots Needed

| Screen | Priority | Notes |
|--------|----------|-------|
| AdCreator (empty) | High | First-time user experience |
| AdCreator (generating) | High | Loading state with ActionBar |
| ActionBar (expanded) | High | All controls visible |
| ActionBar (video mode) | High | Frame upload zones |
| SmartAdLibrary (filters active) | Medium | Filter chips selected |
| Onboarding loader (desktop) | Medium | FoxGame view |
| Onboarding loader (mobile) | Medium | VideoGalleryLoader |
| Mobile ActionBar | Medium | Condensed view |
| Credit modal | Medium | Insufficient credits state |
| Toast examples | Low | Success/error variants |
