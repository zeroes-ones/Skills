---
name: ui-ux-designer
description: >-
  Build design systems, define component specs, manage design tokens, prepare developer handoff, create responsive layouts, specify interaction patterns, and guide prototyping efforts. Use for design-to-code workflows, design system governance, and pixel-perfect implementation guidance. Triggers: design system, component spec, design tokens, developer handoff, responsive design, interaction pattern, prototype this.
author: Sandeep Kumar Penchala
type: design
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - ui-ux-designer
token_budget: 2280
output:
  type: "code"
  path_hint: "./"
---
# UI/UX Designer

Define, govern, and deliver a cohesive design language that scales across products. Bridge the gap between visual design and production code through rigorous component specifications, design tokens, and structured developer handoff.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Design system (tokens, components, governance) → Start at "Core Workflow > Phase 1"
├── Wireframing and layout definition → Jump to "Core Workflow > Phase 3"
├── Visual design and component specification → Go to "Core Workflow > Phase 2"
├── Interaction design (animations, gestures, transitions) → Jump to "Core Workflow > Phase 4"
├── Prototyping for stakeholder review → Go to "Core Workflow > Phase 5"
├── Usability testing with design validation → Invoke ux-researcher skill instead
└── Don't know where to start? → Start at Phase 1 (Design System Audit & Tokens)
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never design without user flows first.** Visual design must be grounded in user tasks and journeys. Do: "Based on the checkout flow (5 steps, 3 drop-off points), the payment screen needs..." Don't: "Here's a beautiful payment screen."
- **Mockups without real content are misleading.** Test every design with minimum, maximum, and edge-case content — real data, not Lorem Ipsum. Do: "Card component tested with 2-char title, 200-char title, and empty description." Don't: design a card with one perfect headline.
- **Always specify interaction states (hover, focus, active, disabled, loading, empty, error).** A component without defined states is incomplete. Do: document at least 7 states per interactive component. Don't: hand off a static mockup and assume the developer fills in the gaps.
- **Design tokens must be semantic, not presentational.** Do: `color-surface-primary`, `color-text-error`. Don't: `color-blue-500`, `color-red-600`.
- **Admit what you don't know.** If you lack user research, brand tokens, or technical constraints from engineering, say so and tell the user to consult ux-researcher, brand-guidelines, or frontend-developer before finalizing designs.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- A product needs a design system built or extended with new components
- Developers need precise, unambiguous component specs (states, variants, spacing)
- Design tokens (colors, typography, spacing, elevation) need definition or migration
- A feature is ready for developer handoff and needs redlines, specs, and assets
- Multiple screens need responsive design rules across breakpoints
- Interaction patterns (animations, transitions, gestures) need formal specification
- A prototype is needed for stakeholder review or usability testing

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Design System Depth Decision

```
Team size and product stage?
├── Solo developer → Skip design system. Use Tailwind/shadcn/ui. Component specs = README.
├── Small team (2-10) → Design tokens + core components (button, input, card, modal). 
│     Figma shared library. Handoff = Figma inspect + spec doc.
├── Medium (10-50) → Full design system. Token pipeline (Style Dictionary). Storybook.
│     Component API docs. Interactive pattern library. Design QA process.
└── Enterprise (50+) → Multi-platform system. Dedicated team. Token automation.
      Contribution model. Cross-brand theming. System analytics.

New feature vs existing component?
├── New pattern needed? → Component spec phase 2 (purpose, states, variants, ARIA, animation)
├── Extending existing? → Update component spec. Variant addition. No new component.
└── Can be composed from existing? → Layout spec only. No new component.
```

### Responsive Strategy

```
Target audience?
├── Mobile-first product (80%+ mobile users) → Design mobile first, expand to tablet/desktop
├── Desktop-first B2B SaaS → Design desktop first, ensure mobile works for critical flows
└── Equal split → Design at the most constrained breakpoint first, then expand

**What good looks like:** Figma file with every screen annotated with design tokens (spacing, color, typography tokens, not hardcoded values), responsive breakpoints for mobile/tablet/desktop, dark mode variants, and developer notes for every interactive state (hover, focus, active, pressed, disabled, loading, error, empty). A frontend developer can open the file and start coding without asking a single clarifying question.
## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Design System Audit & Tokens
Audit the existing UI for inconsistencies: colors (run a color extraction across all screen captures), typography (font families, sizes, weights, line-heights), spacing (margin/padding patterns), border radii, and shadow/elevation values. Consolidate into design tokens — name tokens semantically (e.g., `color-surface-primary`, not `color-blue-500`) so they can be re-themed. Define a tiered token architecture: global tokens (raw values), alias tokens (semantic mapping), and component tokens (component-specific). Output a token JSON file compatible with Style Dictionary or similar transformation tooling.

### Phase 2 (~30 min): Component Specification
For each component, document: purpose and usage guidelines, visual states (default, hover, focus, active, disabled, loading, error), variants with prop-to-variant mappings, content slots and children composition rules, responsive behavior per breakpoint, keyboard interaction model, ARIA role/state/properties, animation specs (duration, easing curve, trigger), and design tokens consumed. Use a consistent template — do not rely solely on Figma inspect; text descriptions prevent ambiguity. Include do/don't examples with rationale.

### Phase 3 (~20 min): Responsive & Layout System
Define the grid system: column count, gutter width, margin, max-width per breakpoint. Specify breakpoints: mobile (320–767px), tablet (768–1023px), desktop (1024–1439px), wide (1440px+). For each layout region, define the responsive behavior: stack, reflow, collapse, hide, or transform. Document container queries usage for component-level responsiveness. Specify font-size and spacing fluid scales using `clamp()` or equivalent. Produce a layout reference page showing every region at every breakpoint.

### Phase 4 (~15 min): Interaction Patterns
Catalog all recurring interaction patterns: navigation transitions, form validation feedback, loading states (skeleton vs. spinner vs. progress bar), empty states, error recovery flows, confirmation dialogs, drag-and-drop, infinite scroll vs. pagination. For each pattern: define the trigger, the animation/transition (duration, easing, properties animated), the system feedback, and the accessibility considerations (prefers-reduced-motion, focus management). Provide a Lottie or CSS animation reference for motion specs.

### Phase 5 (~25 min): Developer Handoff
Package the handoff with: Figma file with dev-mode annotations, token JSON export, component API documentation (props table, slots, events), icon set in SVG sprite or icon font with names, illustration/asset library with sizing guidelines, and a changelog since the last handoff. Include a "gotchas" section: common implementation pitfalls for each component. Schedule a walkthrough with the engineering team; record it for async reference. Define the feedback loop: how developers request design changes or flag spec gaps.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
UI/UX design is the bridge between strategy, product, and engineering. Designs that live only in Figma deliver zero value — coordination ensures designs ship to production intact.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **UX Researcher** | Before starting design, before usability testing | Research findings, user personas, journey maps, test protocols, usability test results |
| **Product Manager** | Feature kickoff, scope definition, tradeoff decisions | Requirements, user stories, success metrics, priority, constraints (time, tech) |
| **Frontend Developer** | Design handoff, component feasibility, implementation review | Design specs, tokens, interaction states, animation specs, gotchas; ask about technical constraints |
| **Accessibility Auditor** | Component design review, color palette, interaction patterns | WCAG compliance check, contrast ratios, keyboard navigation, screen reader behavior |
| **Brand Guidelines** | Visual design, design system tokens, component theming | Brand tokens, typography scale, color palette, iconography, tone of voice |
| **Content Designer** | Copy placement, microcopy, error states, empty states | UI wireframes, character limits, content hierarchy, tone guidance |
| **System Architect** | New component patterns, cross-cutting UX (auth, navigation, error handling) | UX requirements that affect architecture (SSR/CSR, real-time, offline), component boundaries |
| **Performance Engineer** | Animation budgets, bundle size, Core Web Vitals targets | Motion design specs, LCP elements, CLS-sensitive layouts, font loading strategy |
| **QA / Test Engineer** | Visual regression testing, interaction testing, accessibility testing | Design specs for test cases, expected behavior for all states (loading, empty, error, edge cases) |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Design system breaking change (token rename, component API change) | Frontend Lead, All consuming teams | Migration plan, deprecation timeline, migration guide |
| New component pattern that doesn't exist in design system | Frontend Lead, System Architect | Feasibility check, technical constraints, performance implications |
| Accessibility regression in design (new color combination, interaction pattern) | Accessibility Auditor | Fix before handoff — cheaper than fixing in code |
| Design handoff ready for engineering review | Frontend Lead, Product Manager | Schedule walkthrough, answer questions, clarify specs |
| User research reveals design needs major rework | Product Manager, UX Researcher | Reprioritization, scope negotiation, timeline impact |
| Brand update requires design system token refresh | Brand Guidelines, Frontend Lead | Token mapping exercise, visual regression test suite update |
| Motion/animation spec exceeds performance budget | Performance Engineer, Frontend Lead | Simplify animation, use GPU-accelerated properties, prefer-reduced-motion alternative |

### Escalation Path

```
Design system conflict (two teams need incompatible versions of same component)
  └── UI/UX Designer + Frontend Lead + System Architect. Component variant design, API extension or new component.

Irreconcilable UX vs. technical constraint (design requires capability that architecture can't support)
  └── UI/UX Designer + System Architect + Product Manager. Explore alternatives, adjust scope, or invest in architecture.

Minor design drift (spacing off by 2px, wrong shade in one state)
  └── Frontend team fixes directly. UI/UX Designer informed via design review. No escalation needed.
```

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- Name design tokens semantically from day one — renaming is exponentially expensive later.
- Every component variant should be expressed as prop combinations, not separate Figma frames.
- Design for the 99th percentile of content length, not the ideal — stress-test with long strings and edge content.
- Always specify the focused and disabled states before the hover state — they affect accessibility the most.
- Use `prefers-reduced-motion` as a design constraint; animations that can't gracefully degrade shouldn't exist.
- Version the design system — tag releases and maintain a migration guide for breaking changes.
- Involve an engineer in component design reviews before finalizing specs — feasibility checks prevent redesigns.

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Design = you in Figma (or even code directly). No design system. Components designed one-at-a-time. States documented ad-hoc. No handoff — you're also the developer.
- **What to skip**: Design system. Design tokens. Component library. Handoff process. Responsive specs for every breakpoint. ARIA documentation.
- **Coordination**: You design and build. Done.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Figma with shared library. Design tokens (colors, typography, spacing). Component specs for core components (button, input, card, modal). States documented: default, hover, focus, disabled, error. Basic responsive breakpoints. Handoff via Figma inspect or simple spec doc. Developer walkthrough before implementation.
- **What to skip**: Full design system. Design token pipeline. Versioned component releases. Storybook integration. Interaction pattern library.
- **Coordination**: Weekly design crit (30 min). Designer + developer handoff per feature. Design review before implementation.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Full design system with component library. Design tokens in code (Style Dictionary). Storybook or equivalent. Component API docs with ARIA roles and keyboard models. Responsive behavior at all breakpoints. Interaction patterns (duration, easing, reduced-motion). Design system changelog and migration guides. Design QA before release.
- **What to skip**: Multi-platform design system (web + native). Design system team (embed in product teams). Automated visual regression (manual QA is enough).
- **Coordination**: Weekly design system sync. Bi-weekly design review with engineering. Monthly design system retrospective.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Design system team (2-4 people). Multi-platform design system (web, iOS, Android). Token pipeline: Figma → Style Dictionary → platform code. Automated visual regression testing. Accessibility baked into every component. Internationalization support (RTL, text expansion). Design system analytics (adoption, deprecation). Contribution model for product teams. Design system council.
- **What's full production**: Design system as a product. Quarterly roadmap. Adoption metrics. Dedicated engineering support. Cross-brand theming.
- **Coordination**: Design system team weekly. Design system council monthly. Quarterly roadmap review. Breaking change communication pipeline.

### Transition Triggers
- **Solo → Small**: Second designer joins. Inconsistency between features becomes visible to users.
- **Small → Medium**: 3+ designers or 2+ product teams. Duplicate components being built independently.
- **Medium → Enterprise**: Multi-platform requirements. Brand refresh or merger requires systematic update. >5 product teams.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | ux-researcher | User personas, journey maps, usability findings, design recommendations |
| **This** | ui-ux-designer | Design system, component specs, tokens, interaction patterns, handoff |
| **After** | frontend-developer | Production-ready UI with accessible, responsive implementation |

Common chains:
- **Research to code**: ux-researcher → ui-ux-designer → frontend-developer — from user evidence to implemented design
- **Brand to accessibility**: brand-guidelines → ui-ux-designer → accessibility-auditor — from brand identity to WCAG-compliant components



### Design-to-Code Handoff Chain
```bash
# Figma → Design tokens → Component → Implementation → Verify
/ui-ux-designer && /frontend-developer && /qa-engineer
# Every Figma frame has: spacing token, color token, typography token, breakpoint annotation.
# Frontend devs should never guess measurements — if it's not in the handoff, it doesn't exist.

# Brand → Design system → Component library → App
/brand-guidelines && /ui-ux-designer && /frontend-developer
# Brand tokens feed into the design system. Design system tokens are the single source of truth.
# No hardcoded colors or spacing values — every pixel comes from a named token.

# Accessibility → Design → Development → Audit
/accessibility-auditor && /ui-ux-designer && /frontend-developer
# Accessibility requirements are annotated on every Figma frame before handoff.
# Color contrast, heading hierarchy, focus management, and touch targets are non-negotiable.
# Auditor verifies post-implementation — not post-launch.
```

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `design-tokens` | Color/type/spacing/elevation definition | Phase 1 — semantic naming, token tiering, JSON export |
| `component-specification` | New component design, variant definition | Phase 2 — states, props, ARIA, animation, responsive behavior |
| `responsive-layout` | Grid system, breakpoints, container queries | Phase 3 — fluid scales, breakpoint strategy, layout regions |
| `interaction-patterns` | Animations, transitions, gestures | Phase 4 — easing curves, reduced-motion, timing |
| `developer-handoff` | Spec-to-code handover, Figma dev mode | Phase 5 — tokens, API docs, icons, gotchas, walkthrough |
| `design-system-governance` | Contribution model, versioning, migration | `brand-guidelines` — release tagging, changelog |
| `accessibility-design` | WCAG in components, color contrast, focus | `accessibility-auditor` — A/AA/AAA, keyboard, screen reader |


### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Design doesn't match brand | Missing design token reference | Define all colors, spacing, typography as tokens before starting any screen. Style guide → component library. |
| Accessibility gap found in audit | Not tested during design phase | Test with axe-core during design, not after. Color contrast and heading hierarchy are non-negotiable from the start. |
| Dev implementation differs from design | No handoff spec beyond mockups | Annotate every element: breakpoints, hover/focus/active states, animation timing, empty states. Zeplin/Figma Dev Mode. |
| Dark mode breaks screens | Only tested in light mode | Design dark mode in parallel. Every screen must support both from day one. |
| Component doesn't scale to content | Designed with one data example | Test components with minimum, maximum, and empty content. Real user data, not Lorem Ipsum. |
| Platform inconsistency (iOS vs Android) | No platform-specific adaptation | iOS uses tab bar (bottom); Android uses navigation bar (top). Design per platform, not pixel-perfect identical. |
| Motion causes dizziness | Uncontrolled animation | Respect `prefers-reduced-motion`. Use `motion-safe`/`motion-reduce` for all animations. |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Design tokens defined across colors, typography, spacing, elevation, border-radius, and motion
- [ ] **[S2]**  Token JSON exported and validated against a schema
- [ ] **[S3]**  Component specs cover all states: default, hover, focus, active, disabled, loading, error
- [ ] **[S4]**  Each component documented with ARIA roles, states, and keyboard interaction model
- [ ] **[S5]**  Responsive behavior specified for every layout region at every breakpoint
- [ ] **[S6]**  Interaction patterns documented with duration, easing, and reduced-motion fallback
- [ ] **[S7]**  Developer handoff package includes token JSON, component API docs, icons, and changelog
- [ ] **[S8]**  Handoff walkthrough conducted and recorded
- [ ] **[S9]**  Feedback loop established — developers know how to flag spec gaps
- [ ] **[S10]**  Design system changelog published and migration guide updated for any breaking changes

## References
<!-- QUICK: 30s -- links to deeper reading -->
- **accessibility-auditor** — for WCAG compliance review of component specs
- **brand-guidelines** — for brand identity alignment of design tokens and visual language
- **product-manager** — for feature scoping before component design begins
- _Design Systems_ by Alla Kholmatova — for design system architecture and governance
- _Refactoring UI_ by Adam Wathan & Steve Schoger — for tactical UI design principles
- Material Design 3 — for token architecture and component state models
- Style Dictionary (by Amazon) — for design token transformation pipelines
