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

## The Expert's Mindset

UI/UX design is not about making things pretty — it's about **making things understandable**. Every screen is a conversation between the system and the human. The designer's job is to make that conversation clear, efficient, and respectful of the human's cognitive load.

### Mental Models

| Model | Description |
|---|---|
| **Design is how it works, not how it looks** | A beautiful interface that confuses users is bad design. An ugly interface that users navigate effortlessly is good design. Start with functionality; aesthetics amplify usability, not replace it. |
| **Every pixel is a conversation** | Every element on screen asks the user to parse, decide, or act. Add elements only when the value of including them exceeds the cognitive cost. Remove ruthlessly. |
| **Users don't read, they scan** | People don't consume interfaces linearly. They scan for the first thing that looks like it matches their goal. Design for scanning, not reading. |
| **Consistency reduces cognitive load** | When the same action looks and behaves the same way everywhere, users learn once. When it doesn't, they have to relearn every time. |

### Cognitive Biases That Distort Design

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Aesthetic-usability effect** | Assuming a visually pleasing design is more usable | Test with users before declaring victory. Ugly prototypes test better than you think. |
| **False consensus bias** | Designing for yourself: "I find this intuitive, so users will too" | Test with 5 people outside your team. If 1 is confused, 30% of users will be. |
| **Dunning-Kruger (novice designer)** | Overestimating ability to solve complex interaction problems without research | Before designing any flow: watch a user try to accomplish it in the current state. |
| **Peak-end rule** | Over-focusing on the final screen (the "end") and neglecting the messy middle of a flow | Audit the entire journey, not just the happy path. Where do users get stuck? |
| **Change blindness** | Users missing important UI changes because they're focused elsewhere | Never rely on a single visual change to communicate critical information. Use animation + color + position. |

### What Masters Know That Others Don't

- **The best designers spend more time removing than adding.** The first pass adds everything that might be needed. The second pass removes everything that isn't. The third pass removes one more thing.
- **A design that can't be built within constraints is not a design — it's art.** Know the technical constraints (browser support, performance budget, API latency) before opening Figma.
- **Design systems are for the 80%, not the 20%.** A design system that covers every edge case is too bloated to use. Cover the common cases; let teams extend for the uncommon.
- **Copy is design.** Button labels, error messages, empty states — these are interface elements that determine usability as much as layout. Design them, don't fill them with lorem ipsum.

### When to Break Your Own Rules

- **Skip the design system when prototyping.** The design system is for production. When exploring ideas, move fast with rough components. Lock into the system once the direction is validated.
- **Break consistency when the inconsistency improves clarity.** A red "Delete account" button that looks different from other buttons is worth the inconsistency. Use sparingly.

## Operating at Different Levels

Design skill scales from individual components to org-wide design systems to company-defining design philosophy.

| Level | UI/UX Designer Output Characteristics |
|---|---|
| **L1 — Apprentice** | Designs individual screens or components from a design system. Learns interaction patterns and visual hierarchy. |
| **L2 — Practitioner** | Owns a feature's design end-to-end. Produces component specs, handles all states, and delivers developer-ready handoff. |
| **L3 — Senior** | Owns a product surface's design. Establishes interaction patterns, contributes to the design system, and advocates for the user in product decisions. Trade-off rationale included. |
| **L4 — Staff/Principal** | Owns the design system and design quality across products. Defines design principles. "This is how we think about design at this company." |
| **L5 — Design Leadership** | Defines design philosophy that shapes the industry. "Here's a new way to think about interaction design." |

**Usage**: Say "as an L3 designer, create the component spec for..." Default: **L2** (feature-level design, independent execution).

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

## Footguns
<!-- DEEP: 10+min — war stories from production design systems -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| Design tokens had `spacing-md: 17px` and `spacing-lg: 23px` — every component had 1-2px alignment offsets that accumulated to 14px misalignment in complex dashboard layouts | A design system team defined spacing tokens by "eyeballing" Figma auto-layout gaps: `xs: 5px, sm: 9px, md: 17px, lg: 23px, xl: 31px`. Engineers implemented them exactly. Within 3 months, every dashboard had subtle misalignments: a data table header with 4 columns accumulated 2px per cell = 8px offset from the row below; a form with label+input+helper accumulated 3px per row = 15px over 5 fields. Users didn't consciously see the misalignment but reported the UI feeling "janky" and "unpolished." A heuristic evaluation 6 months later found 140+ alignment defects across the product. | Spacing tokens were designed visually ("that looks about right") on a 2× retina display instead of mathematically. Retina displays can't distinguish 16px from 17px at 100% zoom — but the DOM can. Spacing systems must be based on a consistent baseline grid (4px or 8px) so all values are multiples and components align perfectly when stacked or placed side-by-side. | **Every spacing token must be a multiple of the baseline grid (4px or 8px).** Valid: 4, 8, 12, 16, 20, 24, 32, 48, 64, 96. Invalid: 5, 9, 17, 23, 31. Validate with a design token lint rule: `token % 4 !== 0 → error`. Test alignment: place any two components side-by-side — their total widths must land on the grid. Place N components stacked vertically — their total height must land on the grid. |
| Component spec defined 11 states but the loading state was undefined for the primary button — causing 3-second blank screens during payment submission and 8% of payments double-charged | A design system shipped a comprehensive Button component spec: 11 states per variant, 3 sizes, 5 color variants = 165 documented states. QA wrote automated visual regression tests for 163 of them. The missing 2: "Loading state — Primary Button (Large)" and "Loading state — Primary Button (Small)." When the payment flow called the API, the button transitioned to... nothing. The screen showed a blank space for 2-4 seconds while the payment processed. Users double-clicked, triple-clicked, refreshed. 8% of payments were double-charged because the idempotency key was tied to a client-generated nonce that reset on refresh. | The spec was treated as a design artifact (completeness = all states rendered in Figma), not an implementation contract (completeness = every state works in every production context). No one tested the component in a real flow with real API latency. The loading state specification lived in the "animation spec" document — a separate file that engineers never received in the handoff package. | **Every component spec must include loading, empty, and error states as first-class states, not afterthoughts.** Test each component in a real flow with 2-second simulated latency. The litmus test: can a user complete the core task (purchase, search, submit) without ever seeing a blank screen, a flashing layout, or a dead-end error? For interactive components, the contract is: "This component always renders something meaningful, even while waiting for data." |
| Developer handoff included a Figma file with 87 screens — but no interaction specs, so 6 frontend teams independently invented hover, focus, and press behaviors that diverged within 2 sprints | A design team handed off a complete redesign as a Figma file: 87 screens, all states rendered as separate frames. The handoff meeting lasted 45 minutes. Engineers asked: "What's the hover duration? What's the press animation? What's the focus ring style?" The designer said: "Just make it feel native." Within 2 sprints, Team A used 150ms ease-in hovers, Team B used 200ms linear, Team C used instant color swap. The product felt like 6 different products stitched together. A unified interaction pass 4 months later required touching 1,200+ CSS declarations across 6 codebases. | Figma is a visual design tool, not an interaction specification tool. Screens show what it looks like at a moment in time, not what it feels like over time. "Make it feel native" is not a specification — it's an abdication that delegates hundreds of micro-decisions to engineers who were not hired to make interaction design decisions. | **Every handoff must include an interaction spec with: duration, easing curve, animated property, and trigger condition.** Format: "Button hover: background-color transitions from `blue-500` to `blue-600` over 150ms using `ease-out`. Press: scale(0.97) over 100ms `ease-in`. Focus ring: 2px solid `blue-400`, offset 2px from border, appears instantly (0ms)." Export these as animation tokens in the design token JSON. Build a reference demo page engineers can interact with to feel the intended timing before implementing. |
| Design system v2 launched with 27 breaking changes — no migration guide, no codemod, no deprecation warnings. 6 product teams ran 6 different versions for 8 months | A design system team spent 4 months building v2: renamed 18 components (`Tile` → `Card`, `Callout` → `Alert`), changed 9 prop APIs, removed 4 deprecated components. They published v2.0.0 to npm and announced in Slack: "Design System v2 is live! 🎉 Please upgrade." No migration guide. No codemods. No deprecation warnings in v1. Six product teams looked at the breaking change list and stayed on v1. After 8 months, 2 teams were on v2, 3 on v1, and 1 had forked v1 with custom patches. The design team couldn't deprecate v1 because 60% of the product was stuck on it — they were now maintaining two systems. | Breaking changes without migration tooling are not upgrades — they're rewrites. The design system team optimized for their own velocity (clean v2 API) without accounting for consumer migration cost. Every renamed component = every import in every file across every consuming codebase must change manually. For a medium-sized app with 400+ component usages, that's days of grunt work. | **Every breaking change ships with an automated codemod.** Use jscodeshift or ts-morph to automate the migration. The rule: if a human has to manually change code to upgrade, the migration is broken. Deprecation timeline: v1 continues receiving critical fixes for 6 months after v2 launch. Announce breaking changes 3 months before release. Publish a migration guide with before/after examples for every changed API. |
| Responsive breakpoints defined at 768px (tablet) and 1024px (desktop) — but 43% of users were on 375-414px phones where the "mobile" layout didn't activate until 767px | A B2C marketplace defined responsive breakpoints from a 2018 framework: mobile < 768px, tablet 768-1023px, desktop ≥ 1024px. The "mobile" layout — single column, hamburger menu, stacked cards — only activated below 768px. But iPhone SE (375px), iPhone 14 (390px), iPhone 14 Pro Max (430px), and Galaxy S23 (384px) were all well below 768px but the product's "tablet" layout was served because of a CSS bug: `max-width: 767px` instead of `max-width: 767.98px`. Product images rendered at 28px wide. The "Add to Cart" button was 14px tall. Mobile conversion was 0.3% for 7 months before anyone cross-referenced analytics by actual device width against the breakpoint CSS. | The breakpoint system was device-class-based (phone/tablet/desktop) instead of content-based and validated against actual user telemetry. The framework assumed "mobile = under 768px" but never checked that the CSS implementation matched. A 1px off-by-one in a media query (767 vs 767.98) silently served the wrong layout to 43% of users. | **Set breakpoints based on actual user device distribution, not industry defaults.** Pull device-width analytics from 90 days of production data. Find natural clusters — typically 320-375px (small phones), 375-430px (modern phones), 768-834px (tablets), 1024-1440px (laptops). Design the mobile layout for the smallest device in your 95th percentile. Add visual regression tests that capture screenshots at every breakpoint boundary ±1px to catch off-by-one media query bugs. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You design screens in Figma but can't explain how the layout resolves at 320px, 768px, 1440px, and 2560px without opening the file | You ship a component spec and 6 months later, the production implementation still exactly matches — no design drift, no engineer improvisation, no "we changed it because the spec didn't cover this edge case" | Engineers invite you to their sprint planning because your specs prevent rework — the team estimates 30% fewer "design clarification" spikes since you started writing specs their way |
| You hand off a Figma file and say "let me know if you have questions" | You hand off a package containing design tokens JSON, interaction specs, responsive behavior tables, accessibility annotations, and a recorded walkthrough — engineers implement 90%+ on first pass without follow-up questions | You define the design system that 50+ engineers use daily and you can trace a 40% reduction in design-to-code time to specific, measurable improvements you made in the handoff pipeline |
| You design a component's default state beautifully but discover the loading, error, and empty states during QA — or worse, in production | Every component spec you ship includes: default, hover, focus, active, disabled, loading, empty, error, and overflow states — with accessibility annotations and interaction timing for each | A junior designer you mentored for 3 months ships their first independent component spec and you have zero substantive feedback — your standards are internalized and reproducible by others |

**The Litmus Test:** Can you take a raw PRD for a feature you've never seen, produce a complete component spec (all states, responsive layout, accessibility annotations, interaction timing, design tokens) in under 4 hours, and have an engineer implement it without asking a single clarification question?

## Deliberate Practice

Design skill is built through iteration with real users, not through polishing pixels in isolation. The designer who tests with 5 users weekly improves 10x faster than the designer who tests with 0.

### The Design Improvement Loop

```
DESIGN → TEST WITH USERS → OBSERVE CONFUSION → REFINE → repeat
```

The key: you are not your user. Every time you're surprised by what a user does, that's a gap in your mental model. Close that gap.

### Practice Routines by Skill Level

| Level | Practice | Frequency |
|---|---|---|
| **Novice** | Recreate 5 well-known UI patterns from scratch (search bar, data table, onboarding flow). Compare your version to the canonical implementation. Identify 3 differences and understand why each exists. | Weekly |
| **Competent** | Design the same component 3 different ways. Test each version with 3 users. Which performed best? Write down why you were surprised by at least one result. | Biweekly |
| **Expert** | Conduct a heuristic evaluation of a product you didn't design (Nielsen's 10 heuristics). Write up findings with severity ratings. Compare with a peer's independent evaluation. | Monthly |
| **Master** | Redesign a complex flow (checkout, onboarding, settings). Measure completion rate and time-on-task before and after. Write a case study: what improved, what didn't, and why. | Quarterly |

### The One Highest-Leverage Activity

**Watch a user use your design in silence.** Don't explain. Don't justify. Don't help. Just watch where they hesitate, where they click wrong, where they say "huh." One session of silent observation is worth 10 design critiques.

## References
<!-- QUICK: 30s -- links to deeper reading -->
- **accessibility-auditor** — for WCAG compliance review of component specs
- **brand-guidelines** — for brand identity alignment of design tokens and visual language
- **product-manager** — for feature scoping before component design begins
- _Design Systems_ by Alla Kholmatova — for design system architecture and governance
- _Refactoring UI_ by Adam Wathan & Steve Schoger — for tactical UI design principles
- Material Design 3 — for token architecture and component state models
- Style Dictionary (by Amazon) — for design token transformation pipelines
