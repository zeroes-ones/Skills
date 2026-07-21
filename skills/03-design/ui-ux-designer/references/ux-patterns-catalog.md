---
author: Sandeep Kumar Penchala
type: reference
domain: ux-patterns
version: "1.0"
last_updated: 2026-07-21
parent_skill: ui-ux-designer
---

# UX Patterns Catalog

> **Author:** Sandeep Kumar Penchala

A practical catalog of proven UX patterns for navigation, forms, feedback states, data display, and onboarding. Each pattern includes when to use it, examples, and anti-patterns. Use alongside the UI/UX Designer skill's interaction design and user flow guidance.

---

## 1. Navigation Patterns

### Pattern selection guide

| Pattern | Best for | Avoid when | Examples |
|---------|----------|------------|----------|
| **Top navigation** | 3–7 top-level sections; wide screens | 8+ sections (overflows); mobile-primary | GitHub, Stripe, Linear |
| **Sidebar** | 5+ sections; deep hierarchy; admin tools | Simple sites (overkill); small screens | Notion, Figma, AWS Console |
| **Bottom tab bar** | 3–5 primary destinations; mobile-only | Desktop (awkward); 6+ tabs | Instagram, Spotify, Twitter |
| **Hamburger menu** | Secondary/tertiary nav on mobile | Primary navigation (discoverability drops 50%+) | Most news sites |
| **Breadcrumbs** | Deep hierarchy (3+ levels); e-commerce | Flat sites; as primary nav | Amazon, documentation sites |
| **Mega menu** | Many categories (e-commerce, docs) | Few items (overkill) | Shopify, Apple |

### Navigation decision flowchart
```
Is this mobile-first?
├── YES → Is there 3–5 primary destinations?
│         ├── YES → Bottom tab bar
│         └── NO  → Top nav + hamburger for secondary
└── NO  → How many top-level sections?
          ├── 1–7   → Top navigation
          ├── 8–15  → Sidebar (collapsible)
          └── 15+   → Sidebar + search + breadcrumbs
```

### Anti-patterns to avoid
- ❌ Hamburger menu as the ONLY navigation on mobile for an app (use bottom tabs)
- ❌ Deeply nested dropdowns (3+ levels) — users lose context
- ❌ Navigation that changes position between pages
- ❌ Mystery meat navigation — icons without labels (add labels for clarity)

---

## 2. Form Patterns

### Layout: Single-column vs Multi-column
```
| Single-column wins when:          | Multi-column can work when:       |
|-----------------------------------|-----------------------------------|
| ✅ Complex forms (5+ fields)      | ✅ Short forms (2–3 related fields)|
| ✅ Mobile-friendly by default      | ✅ Fields are logically grouped     |
| ✅ Clear visual hierarchy          | ⚠️ Must collapse to single on mobile|
| ✅ Faster completion (Nielsen)     | ⚠️ Risk of incorrect tab order      |
```

### Inline validation pattern
```
Field states:

DEFAULT ──────────────────────────────────────────────
┌──────────────────────────────────────────────────┐
│  Email address                                   │
└──────────────────────────────────────────────────┘

FOCUS ──────────────────────────────────────────────
┌──────────────────────────────────────────────────┐
│  user@example.co│ ← cursor                       │
└──────────────────────────────────────────────────┘

VALID (on blur) ────────────────────────────────────
┌──────────────────────────────────────────────────┐
│  user@example.com                         ✓      │
└──────────────────────────────────────────────────┘

ERROR (on blur) ────────────────────────────────────
┌──────────────────────────────────────────────────┐
│  user@                                          │
└──────────────────────────────────────────────────┘
Please enter a valid email address
```

### Progressive disclosure
```
Show the most important fields first.
Reveal advanced options on demand.

Example: Event creation form

┌─────────────────────────────────────────┐
│  Event name *                           │
│  ┌───────────────────────────────────┐   │
│  └───────────────────────────────────┘   │
│                                          │
│  Date & time *                           │
│  ┌──────────┐ ┌──────────┐               │
│  │  07/21   │ │  2:00 PM │               │
│  └──────────┘ └──────────┘               │
│                                          │
│  ▶ Advanced options (capacity, location) │
└─────────────────────────────────────────┘

On click "Advanced options":

┌─────────────────────────────────────────┐
│  Event name *                           │
│  ...                                     │
│  ▼ Advanced options                      │
│                                          │
│  Capacity                                │
│  ┌───────────────────────────────────┐   │
│  └───────────────────────────────────┘   │
│  Location                                │
│  ┌───────────────────────────────────┐   │
│  └───────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

---

## 3. Feedback Patterns

### Loading states — when to use each

| Pattern | Best for | Avoid when |
|---------|----------|------------|
| **Skeleton screen** | Page/section load (200ms–3s); content-heavy | Instant loads (< 100ms); very long waits |
| **Spinner** | Button actions; short operations (< 2s) | Page loads (use skeleton instead) |
| **Progress bar** | Deterministic: uploads, processing, multi-step | Indeterminate — use spinner |
| **Optimistic UI** | High-confidence actions (like, bookmark, delete) | Destructive actions without undo; payment |

```
Skeleton screen anatomy:
┌──────────────────────────────────────────────┐
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓        ▓▓▓▓▓▓▓▓▓  │  ← shimmer animation
│                                              │
│ ┌──────────────────┐ ┌──────────────────┐    │
│ │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │ │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │    │
│ │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │ │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │    │
│ │ ▓▓▓▓▓▓▓▓▓        │ │ ▓▓▓▓▓▓▓▓▓        │    │
│ └──────────────────┘ └──────────────────┘    │
└──────────────────────────────────────────────┘
```

### State matrix for every component
```
Every interactive element must handle:

| State       | Definition                          | Example                          |
|-------------|-------------------------------------|----------------------------------|
| Resting     | Default, ready for interaction      | Gray button                      |
| Hover       | Mouse cursor over element           | Slightly darker button           |
| Focus       | Keyboard focused (Tab)               | Blue outline ring                |
| Active      | Being pressed/clicked                | Darker + scale 0.98              |
| Loading     | Action in progress                   | Spinner + disabled               |
| Disabled    | Not available in current context      | Grayed out, cursor: not-allowed  |
| Error       | Something went wrong                 | Red border + message             |
| Success     | Action completed                     | Green checkmark + brief toast    |
| Empty       | No data to display                   | Illustration + CTA               |
```

### Error state patterns
```
INLINE ERROR (best for forms):
┌──────────────────────────────────────┐
│  Email *                             │
│  ┌──────────────────────────────┐    │
│  │ user@                        │ ⚠️ │
│  └──────────────────────────────┘    │
│  ⚠️ Please enter a valid email      │
└──────────────────────────────────────┘

PAGE-LEVEL ERROR:
┌──────────────────────────────────────────────┐
│              ┌────┐                           │
│              │ ⚠️ │                           │
│              └────┘                           │
│        Something went wrong                   │
│   We couldn't load your dashboard.            │
│          [Try again]  [Contact support]        │
└──────────────────────────────────────────────┘

TOAST NOTIFICATION (for background operations):
┌──────────────────────────┐
│ ✓ Report exported        │
│   Download (2.3 MB)      │  ← auto-dismiss after 5s
└──────────────────────────┘
```

---

## 4. Data Display Patterns

### Tables
```
┌─────────────────────────────────────────────────────────────┐
│  Users                                          [Search...] │
├──────────┬──────────────────┬──────────┬───────────────────┤
│  Name ▲  │  Email           │  Role    │  Status           │
├──────────┼──────────────────┼──────────┼───────────────────┤
│  Alice   │ alice@acme.com  │  Admin   │  ● Active          │
│  Bob     │ bob@acme.com    │  Member  │  ● Active          │
│  Carol   │ carol@acme.com  │  Viewer  │  ○ Invited         │
├──────────┴──────────────────┴──────────┴───────────────────┤
│  1–3 of 42 rows          [◀ Previous] [Next ▶]             │
└─────────────────────────────────────────────────────────────┘

Table features:
  ▲ = sortable column (click to toggle asc/desc)
  [Search...] = filterable by text
  Pagination = for > 20 rows
  Sticky header = for long tables (scrollable body)
  Row actions = on hover or rightmost column (⋮ menu)
```

### Cards vs Lists vs Tables — when to use each
```
| Display | Best for | Example |
|---------|----------|---------|
| Table   | Comparing across many attributes; dense data | User management, order history |
| Cards   | Browsing/scanning visually rich items | Products, articles, team members |
| List    | Simple linear scanning; minimal metadata | Notifications, messages, activity feed |
| Grid    | Visual browsing with uniform item size | Photo gallery, template picker |
```

### Dashboard layout pattern
```
┌──────────────────────────────────────────────────────────────┐
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  KPI Card 1 │  │  KPI Card 2 │  │  KPI Card 3 │          │
│  │   $12,430   │  │   1,204     │  │   94.2%     │          │
│  │   ↑ 12%     │  │   ↓ 3%      │  │   → 0%      │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                              │
│  ┌───────────────────────────────────────┐ ┌──────────────┐ │
│  │                                       │ │              │ │
│  │          Chart (line/bar)             │ │  Top N List  │ │
│  │          Revenue over time            │ │  Top users   │ │
│  │                                       │ │  1. ...      │ │
│  │                                       │ │  2. ...      │ │
│  └───────────────────────────────────────┘ └──────────────┘ │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │           Full-width table (recent activity)            │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## 5. Onboarding Patterns

### Pattern selection by product complexity

| Pattern | Best for | Avoid when |
|---------|----------|------------|
| **Progressive onboarding** | Complex tools (Figma, Notion); show features as needed | Simple utilities (calculator — just use it) |
| **Task-based onboarding** | Goal-oriented products (Asana, Todoist) | Exploration-heavy products (Pinterest) |
| **Benefit-focused** | B2B SaaS; explain ROI before setup | Consumer apps with instant gratification |
| **Skip-able tutorial** | First-time user needs orientation | Critical setup flows (banking, health) |
| **Empty state-driven** | Content/creation products; guide first action | Pre-populated products (social feeds) |

### Onboarding sequence template
```
Step 1: VALUE PROP (1 screen, skippable)
  ┌──────────────────────────────────┐
  │        [Product illustration]    │
  │                                  │
  │   Organize anything, together    │
  │   All your team's work in one   │
  │   place. Free forever.          │
  │                                  │
  │        [Get started →]          │
  │                                  │
  │    Already have an account?     │
  │        [Sign in]                │
  └──────────────────────────────────┘

Step 2: QUICK SETUP (1–3 screens, NOT skippable)
  ┌──────────────────────────────────┐
  │  What's your team called?        │
  │  ┌────────────────────────────┐  │
  │  │ Acme Corp                  │  │
  │  └────────────────────────────┘  │
  │                                  │
  │  What best describes your role?  │
  │  ○ Engineering  ○ Design         │
  │  ○ Product      ○ Other          │
  │                                  │
  │           [Continue →]           │
  │  ┌─── 1/3 ──────────────────┐   │
  │  └──────────────────────────┘   │
  └──────────────────────────────────┘

Step 3: FIRST TASK (guided, with empty state CTA)
  ┌──────────────────────────────────┐
  │  ┌──────────────────────────┐    │
  │  │  📋                      │    │
  │  │  Create your first board │    │
  │  │  Boards organize projects│    │
  │  │                          │    │
  │  │  [+ Create board]        │    │
  │  └──────────────────────────┘    │
  │                                  │
  │  [Skip tour — I'll explore]      │
  └──────────────────────────────────┘

Step 4: GRADUAL FEATURE REVEAL (contextual tooltips)
  "Try inviting teammates — click Share in the top right."
  (Only show after user has created content)
```

### Onboarding metrics to track
```
| Metric                | Target        | Measurement method          |
|----------------------|---------------|----------------------------|
| Signup completion    | > 70%         | % of started signups completed |
| Time to first action  | < 2 minutes   | Signup → first core action |
| Day 1 retention       | > 50%         | % returning within 24 hrs  |
| Day 7 retention       | > 30%         | % active on day 7          |
| Onboarding NPS        | > 40          | Survey after day 3         |
```

---

See also: UI/UX Designer skill for interaction design, visual hierarchy, and prototyping workflows.
