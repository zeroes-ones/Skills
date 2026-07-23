# Scale Depth: Solo → Small → Medium → Enterprise

<!-- STANDARD: 3min -->

### Solo
Developer tests manually with VoiceOver/TalkBack, basic axe-core scan. Focus: catching obvious issues before shipping. Skip: formal audit documentation, user testing with assistive tech.

### Small Team
Dedicated QA runs accessibility checks, automated axe-core in CI, basic screen reader testing. Focus: WCAG 2.1 AA compliance. Coordination: with designers on color contrast and touch targets, with developers on semantic HTML for screen readers.

### Medium Team
Accessibility testing team, dedicated assistive tech lab, user testing with PWD. Focus: WCAG 2.2 AA, platform-specific guidelines. Coordination: with legal on compliance documentation, with product on accessibility roadmaps.

### Enterprise
Full accessibility program, VPATs per product, WCAG AAA targets, continuous monitoring. Focus: regulatory compliance (ADA, Section 508, EN 301 549). Coordination: with legal on lawsuit defense, with marketing on inclusive brand positioning.

### Transition Triggers
| From → To | Trigger |
|-----------|---------|
| Solo → Small | First accessibility complaint; enterprise customer requires VPAT |
| Small → Medium | Operating in regulated market (EU, healthcare); >100K users |
| Medium → Enterprise | Legal requirement (Section 508, ADA lawsuit risk); IPO or government contract |
