# UI/UX Design

## Wireframe Descriptions

**Catalog Page**: Two-panel layout — left sidebar with faceted search (service type, owner team, health status, last deployed) and a results grid on the right. Each service card shows name, health indicator (green/amber/red dot), version, and a 3-line description. Clicking a card expands an inline detail panel with tabs for metadata, dependencies, and recent deployments.

**Template Wizard**: Five-step linear flow with a stepper component at the top. Step 1 selects a base template (Go API, React SPA, Cron Job, Data Pipeline, Custom Plugin). Step 2 configures parameters (service name, port, environment variables). Step 3 sets resource limits (CPU, memory, replicas). Step 4 reviews generated scaffold (read-only file tree preview). Step 5 deploys with a progress bar and link to the live service.

**Admin Dashboard**: Three-row grid. Top row: key metrics (total services, active templates, plugin count, on-call status). Middle row: recent activity timeline (deployments, failures, config changes). Bottom row: resource utilization charts (CPU, memory, cost across teams).

## Design System Tokens

| Token | Value | Usage |
|-------|-------|-------|
| Spacing | 4, 8, 12, 16, 24, 32, 48, 64px | 4px base grid |
| Border Radius | 4px (inputs), 8px (cards), 12px (modals) | Consistent rounding |
| Shadows | sm: 0 1px 2px rgba(0,0,0,0.05), md: 0 4px 6px rgba(0,0,0,0.07), lg: 0 10px 25px rgba(0,0,0,0.1) | Elevation hierarchy |
| Typography | Inter (UI), JetBrains Mono (code) | Google Fonts |
| Colors | Primary: #6C5CE7 (purple), Success: #00B894, Warning: #FDCB6E, Error: #E17055 | Semantic palette |

## Component Library

**Button**: 3 variants (primary, secondary, ghost), 3 sizes (sm, md, lg), states: default, hover, active, disabled, loading (spinner + disabled). Keyboard accessible with visible focus ring (2px offset, primary color).

**Card**: Compound component — Card, CardHeader, CardContent, CardFooter. Hover state elevates shadow from sm → md. Supports clickable variant (entire card is a link).

**Table**: Virtualized for 1000+ rows via @tanstack/react-virtual. Sortable columns, row selection with checkboxes, sticky header, responsive (horizontal scroll on mobile).

**Modal**: Portal-rendered, focus trapped, ESC to close, click-outside to dismiss. Animated entrance (fade + scale). Three size variants: sm (400px), md (600px), lg (900px).

**Wizard**: Composed from Stepper + Step + StepContent. Linear and non-linear modes. Validates each step before advancing. Persists state to sessionStorage to survive page refresh.

## Figma Prototype

Design file: `figma.com/file/abc123/Orchestra-Design-System`. Component library published as a shared library. Prototype links follow pattern: `figma.com/proto/abc123/Orchestra/{Page-Name}?node-id={id}&scaling=scale-down`.

## Interaction States

All interactive elements specify: default, hover (cursor: pointer, subtle background shift), focus (2px ring, high-contrast, keyboard-visible only via :focus-visible), active (pressed state, slight scale 0.98), disabled (reduced opacity 0.4, no pointer events), loading (inline spinner, cursor: wait). Error states show inline validation messages below inputs with red border and icon. Success states flash green briefly on save (300ms animation).
