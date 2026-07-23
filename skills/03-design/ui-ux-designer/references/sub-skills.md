# Sub-Skills

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
