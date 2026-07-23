# Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Accessibility = use semantic HTML and check contrast. Run Lighthouse once before launch. No formal WCAG audit. No screen reader testing. Fix the obvious stuff.
- **What to skip**: Full WCAG audit. Screen reader testing. Keyboard-only testing. VPAT/ACR. Accessibility statement. Automated a11y in CI.
- **Coordination**: You test your own work. No coordination needed.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Lighthouse in CI (≥90 score gate). Manual keyboard testing on critical flows. Screen reader spot-check (VoiceOver + NVDA). Semantic HTML audit. Basic accessibility statement. Color contrast checked in design tool.
- **What to skip**: Full WCAG 2.2 AA audit. Professional accessibility audit. VPAT. Automated a11y beyond Lighthouse + axe-core. Accessibility specialist hire.
- **Coordination**: Designer checks contrast. Developer runs Lighthouse in PR. QA does keyboard pass on release. Monthly a11y check-in (15 min).

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: WCAG 2.2 AA conformance target with compliance roadmap. axe-core in CI with quality gates. Manual keyboard + screen reader testing per release. Accessibility champion on each team. VPAT/ACR for enterprise sales. Accessibility statement published. Design system with baked-in accessibility.
- **What to skip**: Full-time accessibility specialist (champions model works). WCAG AAA (target AA). Professional audit every release (annual is enough).
- **Coordination**: Accessibility champions bi-weekly sync. Quarterly accessibility review with PM leadership. VPAT updated per major release.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Dedicated accessibility team (1-3 specialists). Full WCAG 2.2 AA conformance across all products. Professional accessibility audit annually. Accessibility embedded in design system components. VPAT/ACR maintained for all products. Accessibility in procurement review. Legal review of accessibility risk. User testing with people with disabilities.
- **What's full production**: Accessibility program office. Continuous monitoring (axe-core + manual). Training program for all engineers and designers. Accessibility in definition of done. Procurement accessibility requirements.
- **Coordination**: Monthly accessibility program review. Quarterly executive accessibility report. Annual professional audit. Accessibility team weekly with product teams.

### Transition Triggers
- **Solo → Small**: First accessibility complaint or enterprise customer asking about VPAT.
- **Small → Medium**: Enterprise deals require WCAG conformance. Legal risk from accessibility lawsuits. >10K users.
- **Medium → Enterprise**: Multiple products requiring accessibility governance. Regulatory mandate (Section 508, EN 301 549). >100K users.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | ui-ux-designer | Component specs, interaction patterns, design tokens |
| **This** | accessibility-auditor | WCAG audit report, remediation priorities, VPAT/ACR |
| **After** | frontend-developer | Accessible implementation with ARIA, keyboard nav, semantic HTML |

Common chains:
- **Design to compliance**: ui-ux-designer → accessibility-auditor → frontend-developer — from visual design to accessible code
- **Risk assessment**: qa-engineer → accessibility-auditor → legal-advisor — from bug reports to legal risk evaluation



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
