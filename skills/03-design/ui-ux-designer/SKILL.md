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
| R1 | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| R2 | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
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

**(QUICK)**

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

**(STANDARD)**

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


## Error Recovery

**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Best Practices

1. **Design system governance — adoption is a product metric, not a hope.** Track: component reuse rate (what % of UI is built from design system components vs. one-off implementations), design-to-code drift score (how many pixels/values differ between Figma specs and production), developer satisfaction (quarterly survey with NPS methodology), and time-to-ship for new components (from request to production). Set adoption targets: 80%+ component reuse within 6 months of system launch. Governance without metrics is theater — you'll think adoption is high until you audit production and discover teams rebuilt every component from scratch. Publish adoption dashboards publicly within the organization; transparency drives accountability.
2. **Component specification — all 8 states must be defined before handoff. Every component ships with: default (resting state), hover (desktop pointer entry), focus (keyboard focus ring, WCAG-visible), active/pressed (mouse down/tap), disabled (grayed out, non-interactive, with explanatory tooltip), loading/skeleton (placeholder during async operations), empty (zero data state with guidance), and error (validation failure, network error, with recovery action). A component spec that only shows the default happy path forces every developer to invent the other 7 states independently — producing 5 different loading spinners, 4 different error messages, and 3 different empty states for the same component type. Defining all 8 states in Figma takes 30 minutes per component; developers guessing takes 3 hours and produces permanently inconsistent UI.
3. **Design tokens as code packages — tokens that live only in Figma are design opinions, not design systems.** Export tokens as versioned npm/SPM/CocoaPods packages consumed by code. Semantic naming throughout: `color-surface-primary` not `color-gray-100`. Token changes follow semver: MAJOR for breaking renames, MINOR for new tokens, PATCH for value adjustments within the same semantic meaning. Every token change triggers: automated visual regression testing (Percy/Chromatic), a migration guide with before/after examples, and a deprecation timeline (old token aliased to new for one release cycle, then removed). Tokens are the API contract between design and engineering — treat them with the same rigor as any public API.
4. **Responsive design beyond breakpoints — design for every viewport width, not 3-4 magic numbers.** Breakpoints are where the layout changes because content breaks, not because a device category (mobile/tablet/desktop) exists. Test continuously: resize the browser from 320px to 2560px pixel-by-pixel. Find every width where text overflows, columns collide, or CTAs disappear below the fold. Design the in-between states — 35%+ of desktop users have browser widths between 1024px and 1440px. At 1100px, a layout that snaps to 1024px wastes 78px of usable space; a layout that snaps to 1440px overflows and hides content. Content-driven breakpoints, not device-driven, produce layouts that work everywhere.
5. **Interaction pattern documentation — static screens are half the design; motion and behavior are the other half.** Every interactive element needs specification for: trigger (click, hover, swipe, long-press, scroll position), animation (duration in ms, easing curve by name from token set, property being animated), response (what changes — opacity, position, scale, color), and edge behavior (what happens if the user triggers it twice rapidly? what if they're mid-animation when the data updates?). Document interaction patterns alongside static specs with video embeds (Loom, Figma prototype recording) — not as a separate "motion design" document that developers never find. Animation without specification is decoration; specification without animation is ambiguity.
6. **Developer handoff — a Figma link is not handoff; it's an invitation to guess.** Complete handoff includes for every frame: spacing tokens (not raw px values — the token name so devs use the variable), color tokens (semantic names referencing the token system), typography tokens (type scale level, not font-size in px), responsive behavior (what happens at 320/768/1024/1440), interaction states (all 8 per component), ARIA annotations (role, label, description, focus order), and character limits (min/max string lengths for every text field). Schedule a recorded walkthrough with the developer. If the developer opens the Figma file and needs to inspect a single element to find a value, the handoff is incomplete. The cost of annotating a hover state is 30 seconds; the cost of a developer guessing wrong is a 3-hour rebuild.
7. **Accessibility-first design — accessibility reviewed at wireframe stage, not as pre-launch remediation.** Start every design review with: (a) focus order — can every interactive element be reached via Tab in a logical sequence? (b) heading hierarchy — does the page structure make sense when read as an outline by a screen reader? (c) color contrast — do all text-on-background combinations pass 4.5:1 minimum? (d) touch targets — are all interactive elements ≥44×44px per WCAG 2.5.5? (e) content structure — do form labels, error messages, and help text have proper ARIA associations? Integrating accessibility at wireframe stage prevents the post-design accessibility pass that reveals the color palette, navigation, and forms all need redesign from scratch. An accessible design system is not an override layer — it's the default.
8. **Dark mode design system — not a color flip; it's a redesign of spatial relationships.** Dark mode changes how elevation, depth, and hierarchy communicate: shadows (which create depth on light backgrounds by casting dark shadows downward) don't work on dark backgrounds (dark shadow on dark surface = invisible). Elevation in dark mode is communicated through light — higher surfaces are lighter, lower surfaces are darker. Define a separate elevation palette keyed to ambient light: surface at elevation-0 = darkest, elevation increases = lighter surface. Validate all text-on-dark-background contrast at 4.5:1 minimum. Design dark mode tokens in parallel with light mode — retrofitting dark mode doubles design cost because every surface relationship must be reconsidered. Dark mode is a first-class design constraint, not an afterthought to be "inverted" at launch.
9. **Prototyping fidelity matched to research goal — the fidelity of your prototype determines what you can learn.** Low-fidelity (paper, wireframes, Balsamiq): test layout, information architecture, workflow — "can users find what they need and complete the task?" Mid-fidelity (Figma click-through with grayscale): test interaction patterns, navigation, form flow — "does the interaction model match user mental models?" High-fidelity (pixel-perfect with motion, data, edge cases): test visual design, micro-interactions, brand perception — "does the experience feel polished and trustworthy?" The most common prototyping mistake: using high-fidelity for layout testing. Users focus on color and typography feedback ("I don't like the blue") instead of structural issues ("I can't find the checkout button"). Match fidelity to the question you're trying to answer.
10. **Usability testing integration — 5 users, 1 hour each, before every major feature ships.** Jakob Nielsen's research shows 5 users catch 85% of usability problems; 15 users catch nearly all. Run moderated tests (facilitator observes user attempting core tasks, asks follow-up questions) for new features and major redesigns. Run unmoderated tests (Maze, UserTesting, UserZoom) for iterative validation between moderated rounds. Document findings with: observed behavior (not interpretation), severity rating (critical blocks task / major causes significant delay / minor annoyance), video timestamp, and recommended fix. Track whether findings result in design changes — if usability testing never changes the design, you're either not testing the right things or not listening to the results.

## Error Decoder

| Error Message / Situation | Root Cause | Fix | Lesson |
|--------------------------|------------|-----|--------|
| Component diverges between design and code — button padding is 12px in Figma, 16px in production; color is `primary-500` in tokens but `#0066FF` hardcoded in CSS | Design tokens not consumed as code packages. Figma uses one set of values; developers use a different set from memory, old specs, or inspecting screenshots. No visual regression testing to catch divergence | Export design tokens as versioned npm package consumed by code. Implement CI visual regression tests (Percy, Chromatic) that compare production screenshots against Figma-approved baselines. Block merge on visual diffs >1% pixel change. Run a design-to-code audit: sample 20 components, measure pixel differences between Figma specs and production DOM | Divergence is silent — it accumulates pixel by pixel until the product looks like a knockoff of its own design. The fix is not better documentation; it's automation that makes divergence visible and impossible to ship. Design tokens as code packages + visual regression testing = the design system's immune system |
| Design system has 0% developer adoption — 200+ beautifully crafted Figma components, zero code implementations | System designed in isolation: Figma components don't map to code patterns, tokens aren't available in developers' environment, documentation is design-only with no code examples, and no frontend engineer was on the design system team | Embed a frontend engineer in the design system team (50/50 split with product engineering). Ship tokens as code packages first (npm/SPM/CocoaPods). Write component documentation with Figma embed + code sandbox (CodePen/StackBlitz) side by side. Run developer onboarding sessions — treat adoption like a product launch with training, support, and success metrics | A design system with zero developer adoption is a Figma file — not a system. Design systems fail when they're built FOR developers instead of WITH developers. The designer-to-developer ratio on the design system team should never exceed 2:1; 1:1 is ideal for the first 6 months |
| Responsive layout breaks between breakpoints — at 1100px, content overflows because the layout snapped to 1024px mobile layout with 78px of wasted whitespace on the right | Breakpoints designed at device-class widths (768 mobile, 1024 tablet, 1440 desktop) without testing the continuous range between them. Content constraints (minimum column width, maximum text line length) not defined | Redefine breakpoints at content-breakage points: set a breakpoint when a column drops below minimum readable width (not at a device width). Test continuously by resizing from 320px to 2560px — find every width where text overflows, columns collide, or CTAs disappear. Define min-width/max-width constraints per component, not just viewport breakpoints. Use CSS clamp() for fluid typography between breakpoints | The browser viewport is a continuous spectrum, not 3-4 discrete sizes. 35%+ of desktop users browse at widths between common breakpoints. Content-driven responsive design (break when content breaks, not when device class changes) produces layouts that work at every width. Test by resizing continuously, not by clicking breakpoint presets |
| Dark mode implementation color-flips only — text inverted to white, background to black, but shadows are invisible, elevation hierarchy is lost, and brand colors vibrate against dark backgrounds | Dark mode treated as a CSS filter or simple color inversion rather than a redesign of spatial relationships. The team assumed "just invert the colors" would work | Design dark mode from scratch: (a) elevation system keyed to light — higher surfaces are lighter, not darker, (b) brand palette adjusted for dark backgrounds — the same blue that passes contrast on white may vibrate or fail on dark gray, (c) shadows replaced with light borders or subtle glow for elevation, (d) all text-on-dark contrast validated at 4.5:1 minimum. Create a separate dark mode token set (`color-surface-dark-elevation-1` through `elevation-5`) | Dark mode is an entirely separate visual language, not a CSS toggle. Shadows — the primary depth cue in light mode — are physically impossible in dark mode (you cannot cast a dark shadow on a dark surface). Elevation must be communicated through relative lightness. A color-flipped dark mode looks broken; a properly designed dark mode looks intentional |
| Usability test produces false confidence — 5 users, 0 failures, but 3 weeks post-launch, support tickets flood in about the same flow | Test participants were: (a) too similar (all power users, all same demographic, all tech-savvy), (b) given leading tasks that telegraphed the answer ("find the settings button" vs. "you want to change your notification preferences — go ahead"), or (c) tested in a quiet lab environment rather than their real context (commuting, multitasking, distracted) | Recruit diverse participants: mix of new and experienced users, different demographics, different tech comfort levels, including users with accessibility needs. Write tasks that describe the goal, not the path: "You want to cancel your subscription" not "Navigate to Account → Billing → Cancel." Test in realistic contexts: mobile during commute, desktop while multitasking, with notifications and interruptions. Run unmoderated tests (Maze, UserTesting) to supplement moderated sessions with larger, more diverse samples | Five users who all look like your design team will find zero problems because they share your mental model. The goal of usability testing is not to validate your design — it's to find the problems you're blind to. Diverse participants + goal-based tasks + realistic context = findings that predict real-world behavior |
| Handoff missing 7 interaction states — developer receives pixel-perfect screens for default state only; has to invent hover, focus, active, disabled, loading, empty, and error states independently | Design handoff treated as "final screens" delivery rather than "complete component specification." The design process focused on the ideal path; edge cases and interaction states were deferred to "we'll figure it out in development" | Before marking any screen ready for handoff, verify all 8 states exist for every interactive component: default, hover, focus, active/pressed, disabled, loading/skeleton, empty, error. Document each state with: visual spec (what changes), behavior spec (what triggers it), and copy spec (what text appears — error messages, empty state guidance, loading labels). If a state isn't designed, the developer invents it — and across 5 developers on 3 platforms, you get 15 different implementations | The happy path is 12.5% of the design. The other 87.5% — all the states users actually encounter when things aren't perfect — is where products earn or lose trust. A beautifully designed default state with a jarring, inconsistent error state tells users the polish is a facade. Handoff is not complete until every state is specified |

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


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
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

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "Users will figure it out — the interface is intuitive." | What's intuitive to the designer who spent 40 hours building it is opaque to a first-time user with 3 seconds of attention. Navigation that "makes sense" to you generates support tickets at **$15-$50 per ticket**, and 40% of confused users simply leave and never return. Cost: **$50K-$300K** in churned revenue from abandoned flows. |
| "Looks fine on my screen — 27" retina display, perfect." | 35% of users are on screens between your breakpoints. At 1100px, the layout snaps to 1024px (wasted space) or 1440px (overflow/hidden content). Design for the IN-BETWEEN states. Cost: **$15K-$50K** per project in responsive layout bugs found by users. |
| "We'll do accessibility later — let's get the design shipped first." | The post-design accessibility pass reveals that the color palette fails contrast minimums, navigation doesn't work with keyboard, and error messages are invisible to screen readers. Every fix requires redesigning screens from scratch. Cost: **$30K-$150K** in emergency redesign cycles + missed release dates + ADA legal exposure. |
| "The design system can wait — just ship this one screen custom." | "One screen" becomes 12 screens. Each with its own spacing, typography, and interaction patterns. Six months later, unifying them costs 3x what building the design system would have cost upfront. Cost: **$100K-$500K/year** in duplicated component work across teams. |
| "No need for usability testing — we know our users." | You ship, and discover that CTAs are below the fold, forms ask for unnecessary info, and the primary flow takes 4 steps instead of 2. Fixing post-launch costs 10x more than fixing in design. Five users in a moderated test would have caught all of it. Cost: **$50K-$300K** in post-launch redesign and lost conversions. |

## Anti-Patterns

- **Design system without developer adoption.** A beautifully crafted Figma design system with 200+ components that developers ignore because tokens aren't in code, component APIs don't match code patterns, or documentation is design-only. Teams rebuild the same components independently, diverging in behavior and appearance. Every duplicate component is engineering time burned. **Total cost: $100,000-$500,000 per year in duplicated component work across teams.** Fix: Embed a frontend engineer in the design system team; ship design tokens as code packages (npm/SPM/CocoaPods); treat developer adoption as a product metric with onboarding and support.
- **Skipping usability testing.** Designing in Figma and shipping to production without watching a single real user attempt core tasks. Navigation that makes sense to designers but not users, CTAs placed below the fold, forms that ask for unnecessary information — all discovered post-launch when the cost to fix is 10x higher than in design. **Total cost: $50,000-$300,000 in post-launch redesign and lost conversions during the broken period.** Fix: Run 5-user moderated usability tests on every major feature before development starts; unmoderated testing with Maze/UserTesting for iterative validation.
- **Design tokens as style dictionaries without inheritance** — `color-primary: #0066FF` defined once per platform (iOS, Android, Web) with the same value. When you change the primary color, 3 files need updating and one WILL be missed. Define tokens ONCE with platform transforms, not once per platform.
- **Figma components nested 5 levels deep** with variant overrides — the outer component has `variant: primary`, the inner button has `variant: secondary`, and the user changes the button to `variant: destructive`. The resulting component is a Frankenstein that exists in 0 designs. Override control must cascade or be locked.
- **Responsive breakpoints** at 768px, 1024px, 1440px — design for the breakpoints, but 35% of your users have screen widths between 1024px and 1440px. At 1100px, your layout snaps to 1024px (wasted space) or 1440px (overflow/hidden content). Design the IN-BETWEEN states, not just the breakpoints.
- **"Design handoff"** as a Figma link thrown over the wall — the developer opens it, sees 47 screens with no interaction states (loading, empty, error, success, focus, hover, active, disabled). They implement the happy path and guess on the other 7 states. Handoff must cover ALL states, not just the ideal screen.
- **Dark mode as color-flipping** — you invert the background and text, but shadows don't work in dark mode (dark shadow on dark background = invisible). Elevation must be communicated through LIGHT (higher surfaces are lighter). Dark mode needs its own elevation system keyed to ambient light, not shadow.
- **Accessibility treated as a post-design workstream.** Teams design the complete product, then schedule "an accessibility pass" weeks before launch. The pass reveals that the color palette fails contrast minimums, the primary navigation doesn't work with a keyboard, and form error messages are invisible to screen readers. Every fix requires redesigning screens from scratch, not just adding ARIA attributes — and the launch date has already been committed. **Total cost: $30,000-$150,000 in emergency redesign cycles, missed release dates, and ADA legal exposure from shipping fundamentally inaccessible experiences.** Fix: Integrate accessibility checks into every design review starting at the wireframe stage; annotate designs with focus order, heading hierarchy, and ARIA landmarks before developer handoff; use accessible color palettes as the design system default, not an override layer.
- **Designing screens for ideal data only.** Every Figma screen shows perfect states — profile pictures fully loaded, names fitting within cards, zero error states. Developers encounter 50-character German names that overflow containers, empty states with no guidance, and loading spinners with no skeleton layout defined. They invent their own solutions, creating UI inconsistency and broken edge-case layouts across the product. **Total cost: $15,000-$50,000 per project in developer guesswork, UI rework cycles, and permanently inconsistent edge-case handling.** Fix: Design every component for empty, loading, error, extreme-length, and edge-case states; include these states in the design system component specification; pair designers with developers during implementation sprints to catch missing states before they ship.
- **No interaction design specification in handoff.** Handoff includes static pixel-perfect screens but zero documentation on animation duration, easing curves, transition triggers, or gesture behavior. Each platform (iOS, Android, web) implements its own interpretation — swipe gestures behave differently, modals animate at different speeds, hover states diverge. The product feels unpolished and fragmented across platforms despite identical visual design. **Total cost: $20,000-$60,000 per year in platform inconsistency fixes and diminished perceived product quality impacting retention.** Fix: Define interaction patterns as design tokens: easing-curve tokens (ease-out, ease-in-out, spring), duration tokens (75ms micro-interaction, 200ms standard, 400ms emphasis); specify gesture behavior per component (swipe threshold, long-press timing, pull-to-refresh distance); document motion alongside static specs with video or prototype embeds.

## Verification

- [ ] Design tokens: exported as JSON/CSS/SCSS and imported by all platforms without manual conversion
- [ ] Component states: every component has defined states for default, hover, focus, active, disabled, loading, empty, error
- [ ] Responsive: design tested at 320px, 768px, 1024px, 1440px — no breakpoint-gap layouts
- [ ] Dark mode: all screens tested in dark mode — elevation hierarchy is clear, contrast ratios pass
- [ ] Accessibility: color contrast ≥ 4.5:1 for text, ≥ 3:1 for large text/icons — verified with contrast checker
- [ ] Handoff: Figma/Zepkin link reviewed by developer — all spacing, colors, and typography match design tokens

## Verification Guardrails

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.## Production Checklist

**(STANDARD)**

- [ ] **[UX1]** Design tokens exported as versioned JSON package, validated against schema, and consumed by Figma (Tokens Studio) and code (Style Dictionary → CSS custom properties/Swift/Kotlin) with matching semantic names — no manual conversion required
- [ ] **[UX2]** Component states documented: all 8 states (default, hover, focus, active, disabled, loading/skeleton, empty, error) defined for every interactive component with visual spec, behavior spec, and copy spec
- [ ] **[UX3]** Responsive behavior tested at continuous widths 320px-2560px — not just at breakpoints; in-between state layouts verified; content extremes tested (shortest possible strings, longest possible strings, empty content)
- [ ] **[UX4]** Dark mode verified: elevation hierarchy uses relative lightness (not shadow), contrast ratios pass WCAG 2.2 AA on all surfaces, `prefers-color-scheme: dark` media query implemented, separate dark mode token set defined
- [ ] **[UX5]** Accessibility contrast validated: all text-on-background combinations ≥4.5:1 (normal text) and ≥3:1 (large text/icons); focus order diagrammed, heading hierarchy documented, ARIA landmarks and labels annotated in handoff
- [ ] **[UX6]** Interaction specifications complete: animation duration tokens, easing curve tokens, gesture thresholds (swipe distance, long-press timing, pull-to-refresh distance), and `prefers-reduced-motion` alternatives documented for every animated element
- [ ] **[UX7]** Developer handoff complete: every Figma frame annotated with spacing tokens, color tokens, typography tokens, responsive behavior, ARIA annotations, character limits (min/max), and interaction states; recorded walkthrough scheduled with assigned developer
- [ ] **[UX8]** Prototype fidelity matched to research goal: low-fidelity for layout/workflow validation, mid-fidelity for interaction testing, high-fidelity for visual polish and micro-interaction evaluation — fidelity appropriate to the question being tested
- [ ] **[UX9]** Usability test results integrated: findings from last test traced to specific design changes with before/after screenshots; unresolved issues tracked with severity rating, assigned owner, and target resolution sprint
- [ ] **[UX10]** Design system adoption metrics tracked: component reuse rate (target ≥80%), design-to-code drift score (target <2% visual difference), developer satisfaction NPS (quarterly survey) — dashboard published and reviewed monthly
- [ ] **[UX11]** Figma file organization clean: pages structured by feature/epic (not by designer name), component library separated from screen designs, deprecated components archived with migration notes, file cover image and description set for searchability
- [ ] **[UX12]** Developer feedback loop active: monthly design system office hours scheduled, component request triage process defined (SLA by severity: critical 48h, standard 1 sprint, nice-to-have backlog), design QA checklist embedded in pull request template

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

