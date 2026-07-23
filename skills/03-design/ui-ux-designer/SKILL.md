---
name: ui-ux-designer
description: >
  Use when building design systems, defining component specifications, managing design
  tokens, preparing developer handoff, creating responsive layouts, or specifying
  interaction patterns. Handles design-to-code workflows, design system governance,
  pixel-perfect implementation guidance, responsive design, prototyping, and component
  API design. Do NOT use for frontend implementation, accessibility auditing, or brand
  strategy definition.
license: MIT
tags:
- design
- design-system
- components
- design-tokens
- responsive
- prototyping
- handoff
author: Sandeep Kumar Penchala
type: design
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 2280
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
---

# UI/UX Designer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Define, govern, and deliver a cohesive design language that scales across products. Bridge the gap between visual design and production code through rigorous component specifications, design tokens, and structured developer handoff.

## Route the Request

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("design-tokens.json", "color")` AND `file_contains("design-tokens.json", "spacing")` | Design tokens exist. Jump to **Production Checklist**. |
| A2 | `file_exists("*.figma")` AND `file_contains("*.figma", "@Component")` | Figma component file detected. Jump to **Core Workflow → Phase 2**. |
| A3 | `file_exists("storybook/")` OR `file_contains("package.json", "@storybook")` | Storybook detected. Jump to **Core Workflow → Phase 5 (Developer Handoff)**. |
| A4 | `file_contains("*.css", "@media")` AND NOT `file_contains("*.css", "@container")` | Media queries exist but no container queries. Jump to **Core Workflow → Phase 3 (Responsive Layout)**. |
| A5 | `file_contains("*.css", "--color-")` AND NOT `file_exists("design-tokens.json")` | CSS custom properties exist without token source. Jump to **Core Workflow → Phase 1 (Design Tokens)**. |
| A6 | `file_contains("*.css", "@keyframes")` OR `file_contains("*.css", "transition")` | Animations exist. Jump to **Core Workflow → Phase 4 (Interaction Patterns)**. |
| A7 | `file_contains("*.css", "aria-")` OR `file_contains("*.css", "role=")` | ARIA attributes in use. Jump to **references/accessibility-design.md**. |
| A8 | `file_exists("CHANGELOG.md")` AND `file_contains("CHANGELOG.md", "design.system")` | Design system changelog exists. Jump to **references/design-system-governance.md**. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:
```
What are you trying to do?
├── Build a design system (tokens, components, governance) → Start at "Core Workflow > Phase 1"
├── Create wireframes and layout definitions → Jump to "Core Workflow > Phase 3"
├── Specify visual design and component behavior → Go to "Core Workflow > Phase 2"
├── Design interaction patterns (animations, gestures, transitions) → Jump to "Core Workflow > Phase 4"
├── Prepare developer handoff package → Go to "Core Workflow > Phase 5"
├── Need usability testing or user research? → `ux-researcher`
├── Need brand identity or visual design tokens? → `brand-guidelines`
├── Need accessibility audit or WCAG compliance? → `accessibility-auditor`
└── Not sure? → Describe the problem in plain language and I'll route you

```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These are hard-gate constraints. Violate any one and the output is invalid.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|--------------------|--------------------|
| G1 | Never hand off a component without all 7 interaction states documented — default, hover, focus, active, disabled, loading, error | `file_contains(output, "component.spec|handoff")` AND NOT `file_contains(output, "hover.*focus.*active.*disabled.*loading.*error")` | REFUSE. Append: "Component spec incomplete — missing interaction states. Document all 7: default, hover, focus, active, disabled, loading, error." |
| G2 | Never use hardcoded color or spacing values in design specs — everything must reference named semantic tokens | `file_contains(output, "#[0-9A-Fa-f]{6}")` OR `file_contains(output, "[0-9]+px")` AND NOT `file_contains(output, "token|semantic|var(--)")` | DETECT. Append: "Hardcoded values detected. Replace `#1A73E8` with `color-primary`, `16px` with `spacing-md` — all values must be semantic tokens." |
| G3 | Never design responsive layouts at fixed breakpoints only — define behavior at content-breakage points and validate with continuous resize testing | `file_contains(output, "breakpoint")` AND NOT `file_contains(output, "content-break|resize|continuous|320px|4K")` | STOP. Append: "Responsive strategy incomplete. Breakpoints must be content-driven and validated from 320px to 4K." |
| G4 | Never specify an animation without duration, easing curve, GPU-accelerated property list, and reduced-motion fallback | `file_contains(output, "animate|transition|spring")` AND NOT `file_contains(output, "duration.*ms|ease-out|ease-in|prefers-reduced-motion|transform|opacity")` | REFUSE. Append: "Animation spec incomplete. Every animation must specify: duration (ms), easing, GPU-only properties, and reduced-motion fallback." |
| G5 | Never ship a component spec that wasn't stress-tested with min/max/zero/error content at all supported breakpoints | `file_contains(output, "component")` AND NOT `file_contains(output, "minimum.content|maximum.content|empty.state|error.state|edge.case")` | STOP. Append: "Component not stress-tested. Test with: 1-char min, 200-char max, zero content, network error, validation error at every breakpoint." |
| G6 | Never provide a Figma handoff without an engineering walkthrough recorded and annotated with timing, token mappings, and platform-specific notes | `file_contains(output, "handoff")` AND `file_contains(output, "Figma")` AND NOT `file_contains(output, "walkthrough|recorded|token.map|platform")` | DETECT. Append: "Handoff incomplete. Every Figma handoff must include: token JSON export, recorded walkthrough, platform-specific notes, and a feedback channel for spec gaps." |

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

## What Good Looks Like

> Every component spec covers loading, empty, error, and edge-case states before a single line of code is written.

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.


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

## Gotchas

- **Design tokens as style dictionaries without inheritance** — `color-primary: #0066FF` defined once per platform (iOS, Android, Web) with the same value. When you change the primary color, 3 files need updating and one WILL be missed. Define tokens ONCE with platform transforms, not once per platform.
- **Figma components nested 5 levels deep** with variant overrides — the outer component has `variant: primary`, the inner button has `variant: secondary`, and the user changes the button to `variant: destructive`. The resulting component is a Frankenstein that exists in 0 designs. Override control must cascade or be locked.
- **Responsive breakpoints** at 768px, 1024px, 1440px — design for the breakpoints, but 35% of your users have screen widths between 1024px and 1440px. At 1100px, your layout snaps to 1024px (wasted space) or 1440px (overflow/hidden content). Design the IN-BETWEEN states, not just the breakpoints.
- **"Design handoff"** as a Figma link thrown over the wall — the developer opens it, sees 47 screens with no interaction states (loading, empty, error, success, focus, hover, active, disabled). They implement the happy path and guess on the other 7 states. Handoff must cover ALL states, not just the ideal screen.
- **Dark mode as color-flipping** — you invert the background and text, but shadows don't work in dark mode (dark shadow on dark background = invisible). Elevation must be communicated through LIGHT (higher surfaces are lighter). Dark mode needs its own elevation system keyed to ambient light, not shadow.

## Verification

- [ ] Design tokens: exported as JSON/CSS/SCSS and imported by all platforms without manual conversion
- [ ] Component states: every component has defined states for default, hover, focus, active, disabled, loading, empty, error
- [ ] Responsive: design tested at 320px, 768px, 1024px, 1440px — no breakpoint-gap layouts
- [ ] Dark mode: all screens tested in dark mode — elevation hierarchy is clear, contrast ratios pass
- [ ] Accessibility: color contrast ≥ 4.5:1 for text, ≥ 3:1 for large text/icons — verified with contrast checker
- [ ] Handoff: Figma/Zepkin link reviewed by developer — all spacing, colors, and typography match design tokens

## References

Detailed reference material loaded on demand:

- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)

