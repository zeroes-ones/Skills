---
name: ui-ux-designer
description: 'Build design systems, define component specs, manage design tokens, prepare developer handoff, create responsive layouts, specify interaction patterns, and guide prototyping efforts. Use for
  design-to-code workflows, design system governance, and pixel-perfect implementation guidance. Triggers: design system, component spec, design tokens, developer handoff, responsive design, interaction
  pattern, prototype this.'
author: Sandeep Kumar Penchala
type: design
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- ui-ux-designer
chain:
  consumes_from:
  - brand-guidelines
  - product-manager
  - ux-researcher
  feeds_into:
  - accessibility-auditor
  - frontend-developer
  - idea-to-spec
  - medical-illustrator
  - mobile-developer
  - ux-writer
token_budget: 2280
output:
  type: code
  path_hint: ./
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
├── Need usability testing or user research? → `ux-researcher`
├── Need brand identity or visual design tokens? → `brand-guidelines`
├── Need accessibility audit or WCAG compliance? → `accessibility-auditor`
├── Need feature specs or PRD writing? → `product-manager`
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

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `ux-researcher` | User personas, journey maps, usability findings with severity ratings, design recommendations traced to observed behavior | Before starting any design; before usability testing |
| `brand-guidelines` | Design tokens (color, typography, spacing, motion), component theming guidance, dark mode palette, icon family, voice and tone | During visual design phase; before design token definition |
| `product-manager` | Prioritized user stories with RICE scores, acceptance criteria, success metrics, design constraints, accessibility requirements | During feature kickoff; before scope and trade-off decisions |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `frontend-developer` | Component specs with all 7 states (default, hover, focus, active, disabled, loading, error), design tokens, interaction patterns, responsive breakpoints, ARIA annotations | Devs guess measurements and states — implementation drifts from design, QA churn |
| `accessibility-auditor` | Component designs with contrast ratios, heading hierarchy, focus order, touch targets, motion specs | Accessibility issues caught in code instead of design — expensive rework |
| `ux-writer` | UI wireframes with copy placement, character limits, content hierarchy, error/empty state contexts | Copy doesn't fit UI — last-minute content changes break layouts |
| `idea-to-spec` | Screen inventory with defined states, interaction patterns, design constraints, accessibility requirements | Specs lack visual definition — engineering builds placeholder UI |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Design system breaking change (token rename, component API change) | `frontend-developer`, all consuming teams | Migration plan, deprecation timeline, migration guide |
| New component pattern that doesn't exist in design system | `frontend-developer`, `system-architect` | Feasibility check, technical constraints, performance implications |
| Accessibility regression in design (new color combination, interaction pattern) | `accessibility-auditor` | Fix before handoff — cheaper than fixing in code |
| Design handoff ready for engineering review | `frontend-developer`, `product-manager` | Schedule walkthrough, answer questions, clarify specs |
| User research reveals design needs major rework | `product-manager`, `ux-researcher` | Reprioritization, scope negotiation, timeline impact |
| Brand update requires design system token refresh | `brand-guidelines`, `frontend-developer` | Token mapping exercise, visual regression test suite update |
| Motion/animation spec exceeds performance budget | `frontend-developer` | Simplify animation, use GPU-accelerated properties, prefers-reduced-motion alternative |

### Escalation Path

```
Design system conflict (two teams need incompatible versions of same component)
  └── `ui-ux-designer` + `frontend-developer` + `system-architect`. Component variant design, API extension or new component.

Irreconcilable UX vs. technical constraint (design requires capability that architecture can't support)
  └── `ui-ux-designer` + `system-architect` + `product-manager`. Explore alternatives, adjust scope, or invest in architecture.

Minor design drift (spacing off by 2px, wrong shade in one state)
  └── `frontend-developer` fixes directly. `ui-ux-designer` informed via design review. No escalation needed.
```

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| Component spec only documents default state — no loading, empty, error, or edge-case states | Flag immediately: block handoff to engineering until all 7 states are defined (default, hover, focus, active, disabled, loading, error) plus empty and edge cases. Components without states are not production-ready — they're design explorations | The empty state reveals more UX complexity than the happy path. A component spec without states forces every engineer to invent their own error handling and loading indicators, producing 5 different implementations of the same pattern |
| No mobile breakpoints or responsive behavior specified for a consumer-facing design | Propose responsive design: define breakpoints at content-breakage points (not device classes), specify layout behavior at 320px, 768px, 1024px, and 1440px. Test by resizing continuously, not at preset breakpoints. Coordinate with `mobile-developer` for platform-specific patterns | Responsive design is not about supporting 4 breakpoints — it's about working at every viewport width. Designs that only work at desktop resolution ship broken experiences to 60%+ of users |
| No dark mode consideration in a design that will be used in low-light environments | Alert: dark mode is not a color swap — it's a redesign of every surface relationship. Design dark mode tokens in parallel with light mode. Validate contrast for all text-on-dark-background combinations. Coordinate with `frontend-developer` for CSS custom property toggling strategy | Retrofitting dark mode doubles design and engineering cost. If you design light mode first and dark mode later, you will design every screen twice. Dark mode is a first-class design constraint, not an afterthought |
| Design token handoff to `frontend-developer` — are tokens in the right format? | Verify: tokens exported as JSON with semantic naming (not `blue-500` but `color-primary`). Validate against a schema. Ensure Figma tokens and code tokens use the same names. Export via Style Dictionary to CSS custom properties. Provide migration guide for any renamed tokens | The gap between Figma tokens and code tokens is where design drift lives. A token named `blue-500` in Figma and `primary` in code means designers and developers speak different languages — and the miscommunication shows up in production |
| Platform-specific design needed — iOS vs Android patterns differ | Coordinate with `mobile-developer` to define: navigation placement (iOS tab bar bottom vs Android nav bar top), gesture conventions (iOS swipe-back vs Android back button), typography scale differences (SF Pro vs Roboto), and component equivalents (iOS UIPicker vs Android Spinner). Design per platform, not pixel-perfect identical | Users compare your app against every other app on their device, not against your iOS and Android screenshots side by side. Following platform conventions creates a native-feeling experience; ignoring them creates friction |
| Animation spec exceeds performance budget or lacks `prefers-reduced-motion` fallback | Flag: simplify animation to use GPU-accelerated properties (transform, opacity). Add `prefers-reduced-motion` media query with a static alternative. Test on a low-end device, not just the designer's M3 Max. Every animation must answer: "What does this movement communicate?" — if the answer is "it looks nice," remove it | Motion is the most dangerous design tool — it can cause dizziness, nausea, and seizures in users with vestibular disorders. Every animation without a reduced-motion fallback is an accessibility violation waiting to happen |
| Design-to-dev handoff: are all Figma frames annotated and ready for engineering? | Before sending to engineering, verify every frame has: spacing tokens, color tokens, typography tokens, responsive behavior, interaction states, ARIA annotations, and character limits. Schedule a recorded walkthrough with the developer. If the developer has to guess any measurement, state, or behavior, the handoff is incomplete | An unannotated Figma file is a Rorschach test — every developer sees something different. The cost of annotating a hover state is 30 seconds; the cost of rebuilding a component that doesn't match the design is 3 hours |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- Name design tokens semantically from day one — renaming is exponentially expensive later.
- Every component variant should be expressed as prop combinations, not separate Figma frames.
- Design for the 99th percentile of content length, not the ideal — stress-test with long strings and edge content.
- Always specify the focused and disabled states before the hover state — they affect accessibility the most.
- Use `prefers-reduced-motion` as a design constraint; animations that can't gracefully degrade shouldn't exist.
- Version the design system — tag releases and maintain a migration guide for breaking changes.
- Involve an engineer in component design reviews before finalizing specs — feasibility checks prevent redesigns.

## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|-----------------|---------------------|
| Designing components with ideal content — perfect 12-character titles, balanced images, no extremes | Stress-test every component with minimum content (1 character), maximum content (200+ characters), zero content (empty state), and error content (network failure, validation error). Real user data breaks beautiful mockups within the first week of production |
| Handing off a Figma file with no design tokens, no annotations, and no interaction states — "it's obvious" | Annotate every frame with: spacing tokens, color tokens, typography tokens, breakpoint behavior, and all interaction states (default, hover, focus, active, disabled, loading, error). If the developer has to guess any measurement, state, or behavior, the handoff is incomplete |
| Designing at 1440px only and calling it "responsive" because "the developer will figure out mobile" | Design mobile-first or design mobile in parallel. Define breakpoints at content-breakage points (not device classes). Test by resizing continuously. A desktop-only design handed to engineering produces a broken mobile experience that takes 2x longer to fix than to design correctly from the start |
| Building a design system in Figma with no engineering partnership — components look perfect but are impossible to implement | Co-design with engineering: designers own visual specs, engineers own implementation feasibility. Every new component is reviewed by an engineer before it enters the design system. A design system without engineering buy-in is a design portfolio, not a tool |
| Using hardcoded color values (`#1A73E8`) throughout designs instead of semantic tokens (`color-primary`) | Use semantic design tokens for every color, spacing, and typography value. `#1A73E8` means nothing; `color-primary` means "the primary brand color" and can be updated in one place. Hardcoded values are technical debt that accrues every time the palette changes |
| Designing dark mode as an afterthought — "we'll just invert the colors later" | Design dark mode tokens in parallel with light mode tokens. Dark mode is not an inversion — shadows become highlights, some colors need elevation adjustments, and the visual hierarchy shifts. Designing dark mode after the fact costs 2x the time of designing both palettes together |
| Ignoring platform conventions — designing iOS with Material components or forcing identical layouts on iOS and Android | Follow platform conventions: iOS uses bottom tab bars, swipe-back gestures, SF Pro typography; Android uses top navigation bars, back button, Roboto typography. Users don't compare cross-platform screenshots — they compare your app against every other app on their device |
| Specifying animations with "spring, 0.5s" and no easing curve, no reduced-motion fallback, no performance consideration | Define animation tokens: duration (instant/fast/base/slow in ms), easing (ease-out for enter, ease-in for exit), GPU-accelerated properties only (transform, opacity). Always provide `prefers-reduced-motion: reduce` alternative. Test on a low-end device, not just the designer's workstation |

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

## What Good Looks Like

> The developer opens the Figma file, inspects any component, and immediately knows the exact spacing tokens, color variables, interactive states, keyboard behavior, and ARIA attributes needed — no guessing, no Slack pings, no "design intent" debates. Design tokens are exported as JSON and consumed directly by the codebase, so a palette change in Figma propagates to production in a single pull request with zero manual value updates. Every component spec covers loading, empty, error, and edge-case states before a single line of code is written. The responsive layout works seamlessly from 320px to 4K, and animations follow the same easing curves with a reduced-motion fallback that actually gets tested on a real device. Developer handoff takes minutes, not days, and the first implementation review surfaces cosmetic tweaks, not structural rework.

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


### War Story 1 — The Handoff That Became a Blame Game
**Symptom:** A design team handed off a beautiful Figma file for a new onboarding flow. Engineering built it in 3 weeks. The result looked completely different from the design — wrong spacing, wrong colors, missing states. The designer blamed the engineer. The engineer blamed the handoff.
**Root cause:** The Figma file had no design tokens, no responsive specs, no edge-case states, and no developer notes. The designer assumed "it's obvious" and the engineer assumed "I'll figure it out." Neither was right.
**Fix:** Standardized developer handoff: every Figma frame must include spacing tokens, color tokens, typography tokens, and responsive behavior before it leaves the design phase. Added a mandatory handoff review where designer and engineer walk through the spec together.
**Lesson:** A handoff without specs is not a handoff — it's a game of telephone. If the engineer has to guess any measurement, state, or behavior, the handoff is incomplete.

### War Story 2 — The Design System That Didn't Survive Contact With Real Data
**Symptom:** A design system's card component was designed with a perfect headline (12 characters), perfect description (40 characters), and perfect image (3:2 aspect ratio). In production, users uploaded 200-character titles, empty descriptions, and portrait photos. Every card broke.
**Root cause:** Components were designed with ideal content, not real content. No stress-testing with min/max content lengths. No empty-state handling. No fallback for missing images.
**Fix:** Introduced a "content stress test" policy: every component must be designed and tested with minimum content, maximum content, and zero content before it's added to the design system. Character limits are documented in the component spec.
**Lesson:** Design with the real content your users will provide, not the ideal content in your mockups. If a component breaks with real-world input, it's not production-ready.

### War Story 3 — The Responsive Design That Only Worked on the Designer's Screen
**Symptom:** A designer created a responsive dashboard at standard breakpoints (1440px, 1024px, 768px, 375px). It looked great in Figma. In production, users on a 1280px laptop saw a half-empty screen. Users on a 390px phone had overlapping buttons. Users on an 820px iPad saw an unusable layout.
**Root cause:** Breakpoints were inspired by device classes, not by real content breakage points. The design wasn't tested with actual viewport resizing — only at the 4 specified breakpoints.
**Fix:** Switched to a content-first responsive approach: resize the browser continuously and fix breakpoints at the actual points where content breaks, not arbitrary device sizes. Added container queries for component-level responsiveness.
**Lesson:** Responsive design isn't about supporting 4 breakpoints — it's about working at every viewport width between 320px and 4K. Test by resizing, not by switching device presets.


## Error Decoder
<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Design doesn't match brand | Missing design token reference | Define all colors, spacing, typography as tokens before starting any screen. Style guide → component library. | A design without tokens is a collection of one-offs. Tokens are the contract between brand intent and visual execution — skip them and every pixel is negotiation. |
| Accessibility gap found in audit | Not tested during design phase | Test with axe-core during design, not after. Color contrast and heading hierarchy are non-negotiable from the start. | Accessibility cannot be added after the fact — it must be designed in. A contrast violation caught in Figma costs seconds; the same fix post-launch costs a sprint. |
| Dev implementation differs from design | No handoff spec beyond mockups | Annotate every element: breakpoints, hover/focus/active states, animation timing, empty states. Zeplin/Figma Dev Mode. | Every interaction state you don't specify will be invented by the developer. The cost of annotating a hover state is 30 seconds; the cost of rebuilding a component is 3 hours. |
| Dark mode breaks screens | Only tested in light mode | Design dark mode in parallel. Every screen must support both from day one. | Dark mode is not a color swap — it is a redesign of every surface relationship. If you design light mode first, you will design dark mode twice. |
| Component doesn't scale to content | Designed with one data example | Test components with minimum, maximum, and empty content. Real user data, not Lorem Ipsum. | Lorem Ipsum hides layout bugs. Test every component with its real content extremes — the shortest string, the longest string, and no string at all. |
| Platform inconsistency (iOS vs Android) | No platform-specific adaptation | iOS uses tab bar (bottom); Android uses navigation bar (top). Design per platform, not pixel-perfect identical. | Users don't compare screenshots across platforms — they compare your app against every other app on their device. Design for OS conventions, not for a flat-lay hero shot. |
| Motion causes dizziness | Uncontrolled animation | Respect `prefers-reduced-motion`. Use `motion-safe`/`motion-reduce` for all animations. | Motion is a powerful design tool that can harm users when overused. Every animation should answer: what does this movement communicate? If the answer is "it looks nice," consider removing it. |


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
