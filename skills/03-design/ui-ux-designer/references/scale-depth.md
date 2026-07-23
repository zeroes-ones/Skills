# Scale Depth: Solo → Small → Medium → Enterprise

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
