---
author: Sandeep Kumar Penchala
type: reference
domain: design-systems
version: "1.0"
last_updated: 2026-07-21
parent_skill: ui-ux-designer
---

# Design Systems Guide

> **Author:** Sandeep Kumar Penchala

A comprehensive guide to building, maintaining, and scaling design systems. Covers design tokens, component hierarchy, accessibility standards, responsive breakpoints, design-to-code handoff, versioning, and maturity assessment. Use alongside the UI/UX Designer skill's component design and prototyping workflows.

---

## 1. Design Token Structure

Design tokens are the atomic values that define a design system's visual language. Store them in a platform-agnostic format and transform for each target.

### Core token categories

```json
{
  "color": {
    "primary": {
      "50":  "#EFF6FF",
      "100": "#DBEAFE",
      "200": "#BFDBFE",
      "300": "#93C5FD",
      "400": "#60A5FA",
      "500": "#3B82F6",
      "600": "#2563EB",
      "700": "#1D4ED8",
      "800": "#1E40AF",
      "900": "#1E3A8A"
    },
    "neutral": {
      "0":   "#FFFFFF",
      "50":  "#F9FAFB",
      "100": "#F3F4F6",
      "200": "#E5E7EB",
      "300": "#D1D5DB",
      "400": "#9CA3AF",
      "500": "#6B7280",
      "600": "#4B5563",
      "700": "#374151",
      "800": "#1F2937",
      "900": "#111827"
    },
    "semantic": {
      "success":  "#10B981",
      "warning":  "#F59E0B",
      "error":    "#EF4444",
      "info":     "#3B82F6"
    }
  },
  "typography": {
    "fontFamily": {
      "sans":  "'Inter', -apple-system, sans-serif",
      "mono":  "'JetBrains Mono', 'Fira Code', monospace"
    },
    "fontSize": {
      "xs":    "0.75rem",
      "sm":    "0.875rem",
      "base":  "1rem",
      "lg":    "1.125rem",
      "xl":    "1.25rem",
      "2xl":   "1.5rem",
      "3xl":   "1.875rem",
      "4xl":   "2.25rem"
    },
    "fontWeight": {
      "normal":  "400",
      "medium":  "500",
      "semibold":"600",
      "bold":    "700"
    },
    "lineHeight": {
      "tight":   "1.25",
      "normal":  "1.5",
      "relaxed": "1.75"
    }
  },
  "spacing": {
    "0":    "0",
    "px":   "1px",
    "0_5": "0.125rem",
    "1":    "0.25rem",
    "2":    "0.5rem",
    "3":    "0.75rem",
    "4":    "1rem",
    "5":    "1.25rem",
    "6":    "1.5rem",
    "8":    "2rem",
    "10":   "2.5rem",
    "12":   "3rem",
    "16":   "4rem",
    "20":   "5rem",
    "24":   "6rem"
  },
  "borderRadius": {
    "none":  "0",
    "sm":    "0.125rem",
    "base":  "0.25rem",
    "md":    "0.375rem",
    "lg":    "0.5rem",
    "xl":    "0.75rem",
    "full":  "9999px"
  },
  "shadow": {
    "sm":   "0 1px 2px 0 rgb(0 0 0 / 0.05)",
    "base": "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
    "md":   "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
    "lg":   "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)"
  },
  "motion": {
    "duration": {
      "instant": "0ms",
      "fast":    "150ms",
      "normal":  "300ms",
      "slow":    "500ms"
    },
    "easing": {
      "default":   "cubic-bezier(0.4, 0, 0.2, 1)",
      "in":         "cubic-bezier(0.4, 0, 1, 1)",
      "out":        "cubic-bezier(0, 0, 0.2, 1)",
      "bounce":     "cubic-bezier(0.68, -0.55, 0.265, 1.55)"
    }
  }
}
```

### CSS custom properties output (generated from tokens)
```css
:root {
  /* Color */
  --color-primary-500: #3B82F6;
  --color-neutral-100: #F3F4F6;
  --color-semantic-error: #EF4444;

  /* Typography */
  --font-sans: 'Inter', -apple-system, sans-serif;
  --text-base: 1rem;
  --leading-normal: 1.5;

  /* Spacing */
  --space-4: 1rem;
  --space-8: 2rem;

  /* Radius */
  --radius-md: 0.375rem;

  /* Motion */
  --duration-normal: 300ms;
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Token naming convention
```
--[category]-[name]-[variant?]-[state?]

Examples:
  --color-primary-500
  --color-primary-500-hover
  --space-4
  --text-lg
  --text-lg-bold
```

---

## 2. Component Hierarchy (Atomic Design)

```
┌──────────────────────────────────────────────────────────────┐
│  PAGES         │  Dashboard, Settings, User Profile           │
│                │  (Composes templates + real content)         │
├──────────────────────────────────────────────────────────────┤
│  TEMPLATES     │  Two-column layout, Sidebar layout, Modal    │
│                │  (Page-level layout without real content)    │
├──────────────────────────────────────────────────────────────┤
│  ORGANISMS     │  Header, Form group, Data table, Card grid   │
│                │  (Complex UI sections — molecules + atoms)   │
├──────────────────────────────────────────────────────────────┤
│  MOLECULES     │  Search bar, Menu item, Form field + label   │
│                │  (Combinations of atoms forming a unit)      │
├──────────────────────────────────────────────────────────────┤
│  ATOMS         │  Button, Input, Label, Icon, Avatar, Badge  │
│                │  (Single HTML elements — can't break down)    │
└──────────────────────────────────────────────────────────────┘
```

### Component API pattern
```typescript
// Button — Atom
<Button
  variant="primary" | "secondary" | "ghost" | "destructive"
  size="sm" | "md" | "lg"
  disabled={boolean}
  loading={boolean}
  iconLeft={<Icon />}
  iconRight={<Icon />}
  onClick={() => void}
>
  {children}
</Button>

// DataTable — Organism
<DataTable
  columns={ColumnDef[]}
  data={T[]}
  sortable={boolean}
  filterable={boolean}
  pagination={{ pageSize: 20 }}
  onRowClick={(row) => void}
  emptyState={<EmptyState />}
/>
```

---

## 3. Accessibility in Design Systems

### Color contrast requirements
```
| Element                       | AA (Minimum)       | AAA (Enhanced)     |
|-------------------------------|--------------------|--------------------|
| Normal text (< 18px)          | 4.5:1              | 7:1                |
| Large text (≥ 18px bold)      | 3:1                | 4.5:1              |
| UI components / icons          | 3:1                | 3:1                |
| Disabled text                  | No requirement     | No requirement     |
| Text over image/gradient       | 4.5:1              | 7:1                |
```

### Touch target minimums (WCAG 2.5.5)
- **Minimum:** 24×24 CSS pixels (AA)
- **Recommended:** 44×44 CSS pixels (Apple HIG, Material Design)
- **Exception:** Inline links in text blocks
- **Spacing:** Minimum 8px between adjacent touch targets

### Focus indicators
```css
/* Visible focus ring — never use outline: none without replacement */
:focus-visible {
  outline: 2px solid var(--color-primary-500);
  outline-offset: 2px;
}

/* Skip-to-content link */
.skip-link {
  position: absolute;
  top: -100%;
  left: 0;
  padding: var(--space-4);
  background: var(--color-primary-500);
  color: white;
  z-index: 1000;
}
.skip-link:focus {
  top: 0;
}
```

### Screen reader considerations
```
| Element       | Required                            | Example                                     |
|---------------|-------------------------------------|---------------------------------------------|
| Icon button   | aria-label                          | <button aria-label="Close dialog">          |
| Image         | alt (decorative: alt="")            | <img alt="Bar chart showing Q3 growth">     |
| Form input    | label (associated via for/id)       | <label for="email">Email</label>            |
| Error message | aria-describedby linking to input   | <input aria-describedby="email-error">      |
| Loading       | aria-busy="true", aria-live="polite"| <div aria-busy="true" aria-live="polite">   |
| Alert/toast   | role="alert"                        | <div role="alert">Saved!</div>              |
| Modal         | role="dialog", aria-modal="true"    | <div role="dialog" aria-modal="true">       |
```

### Accessibility testing checklist per component
- [ ] Keyboard navigable (Tab, Enter, Escape, Arrow keys where relevant)
- [ ] Screen reader announces correctly (test with VoiceOver/NVDA)
- [ ] Color is not the only differentiator (icons, text labels as backup)
- [ ] Works at 200% zoom without horizontal scroll
- [ ] Focus order is logical (matching visual order)
- [ ] Animations respect `prefers-reduced-motion`

---

## 4. Responsive Breakpoints

```css
/* Mobile-first breakpoint system */
/* Base styles are mobile (< 768px) — no media query needed */

/* Tablet */
@media (min-width: 768px) { /* 768px–1023px */ }

/* Desktop */
@media (min-width: 1024px) { /* 1024px–1439px */ }

/* Wide */
@media (min-width: 1440px) { /* 1440px+ */ }
```

### Breakpoint usage guide
```
| Breakpoint | Primary device      | Layout pattern                  | Typography |
|------------|---------------------|--------------------------------|------------|
| < 768px    | Phone (portrait)    | Single column, stacked         | base       |
| 768–1023   | Tablet (portrait)   | 2-column grid, side nav hidden | lg         |
| 1024–1439  | Laptop/Desktop      | Multi-column, sidebar visible  | xl         |
| ≥ 1440     | Large monitor       | Max-width container, wider gaps| 2xl        |
```

### Container query pattern (modern alternative)
```css
/* Instead of viewport-based breakpoints, size based on parent */
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
}
```

---

## 5. Design-to-Code Handoff

### Figma → Code workflow
```
1. DESIGN        2. TOKEN          3. COMPONENT       4. REVIEW
   ┌──────┐        ┌──────┐          ┌──────┐           ┌──────┐
   │Figma │───────▶│Tokens│─────────▶│ Code │──────────▶│Visual│
   │Design│        │ JSON │          │(React│           │Diff  │
   │      │        │      │          │ etc) │           │Review│
   └──────┘        └──────┘          └──────┘           └──────┘
```

### Figma inspect panel — what to check
```
| Property        | Figma field       | Maps to CSS/token              |
|-----------------|-------------------|--------------------------------|
| Width/Height    | W / H             | width / height                 |
| Padding         | Padding           | padding: top right bottom left |
| Gap             | Gap               | gap (flexbox/grid)             |
| Border radius   | Corner radius     | border-radius                  |
| Font            | Text properties   | font-family, font-size, etc.   |
| Color           | Fill / Stroke     | color / background-color       |
| Shadow          | Effects           | box-shadow                     |
| Opacity         | Layer opacity     | opacity                        |
| Auto layout     | Auto layout       | display: flex; flex-direction  |
```

### Component mapping spreadsheet
```
| Figma Component         | Code Component       | Status        | Props mismatch |
|-------------------------|----------------------|---------------|----------------|
| Button / Primary / M    | <Button variant="primary" size="md"> | ✅ Synced | — |
| Input / Default         | <Input />            | ⚠️ Outdated   | Missing: error state |
| Modal / Default         | <Modal>              | ❌ Not built  | — |
```

---

## 6. Versioning Design Systems

### Semantic versioning for design
```
MAJOR.MINOR.PATCH  —  e.g., v2.1.3

MAJOR: Breaking changes — component removed, prop renamed, token renamed
       → Requires migration guide and migration codemod

MINOR: New features — new component, new variant, new token
       → Backward compatible; announce in changelog

PATCH: Fixes — visual bug, accessibility fix, token value correction
       → Auto-applied; no consumer action needed
```

### Breaking change policy
1. Announce breaking changes 2 releases before removal (deprecation → removal)
2. Deprecated components get console warnings in dev mode
3. Provide a migration guide with before/after code examples
4. Ship a codemod (jscodeshift) for mechanical transformations
5. Support the old API for one full MINOR cycle after deprecation

```
Timeline:
v2.0.0: Component deprecated (warning in console, docs updated)
v2.1.0: Component still works, warning persists
v3.0.0: Component removed (MAJOR bump)
```

---

## 7. Design System Maturity Model

```
LEVEL 0: NO SYSTEM
├── No shared components or styles
├── Each team builds from scratch
└── Symptom: 15 different button implementations

LEVEL 1: STYLE GUIDE
├── PDF/Figma style guide exists
├── Brand colors, typography documented
├── No code implementation
└── Symptom: Guide says "use blue" but every page has a different blue

LEVEL 2: COMPONENT LIBRARY
├── Shared component library (npm package)
├── 2–3 people maintain part-time
├── Basic documentation (Storybook)
└── Symptom: Library exists but teams fork it when blocked

LEVEL 3: DESIGN SYSTEM
├── Design tokens as source of truth
├── Dedicated design system team (2+ people)
├── Figma ↔ Code sync workflow
├── Contribution model for other teams
└── Adoption: 60–80% of product

LEVEL 4: PLATFORM
├── Multiple products share one system
├── Automated visual regression testing
├── Accessibility baked into every component
├── Design system metrics tracked: adoption %, contribution velocity
└── The system is a product itself — roadmap, OKRs, dedicated PM

LEVEL 5: ECOSYSTEM
├── External partners build on your system
├── White-label theming
├── Community contributions accepted
├── System used beyond your company
└── Examples: Shopify Polaris, IBM Carbon, Google Material
```

---

See also: UI/UX Designer skill for component design patterns, prototyping, and visual design principles.
