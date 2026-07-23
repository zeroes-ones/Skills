# Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Brand = a logo + 2-3 colors + 1 font. No guidelines document. "Brand identity" lives in your head and the app itself.
- **What to skip**: Brand guidelines document. Design tokens. Brand architecture model. Motion guidelines. Icon sets. Brand governance process.
- **Coordination**: You design everything. Consistency is natural.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Simple brand guidelines (1-page PDF or Figma file). Logo variants (primary, icon-only). Color palette (4-6 colors). Typography (1-2 fonts with hierarchy). Basic do/don't examples. Assets shared via Google Drive or Figma.
- **What to skip**: Full brand architecture model. Design tokens. Motion guidelines beyond "keep it simple." Illustration system. Brand governance committee.
- **Coordination**: Designer owns brand. New assets reviewed by designer before use. Quarterly brand audit (30 min).

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Comprehensive brand guidelines portal. Full brand architecture model. Design tokens (colors, typography, spacing, elevation). Semantic color tokens (primary, semantic, neutral). Dark mode palette. Icon set with consistent style. Illustration direction. Motion tokens. Brand governance with review process. Asset distribution portal (Figma library + CDN).
- **What to skip**: Multi-brand architecture (unless acquired). Brand valuation study. Global brand compliance audits.
- **Coordination**: Brand designer reviews all public-facing assets. Monthly brand council. Quarterly brand refresh consideration.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Multi-brand architecture (Branded House / House of Brands). Design token pipeline (Figma → Style Dictionary → code). Global brand compliance. Brand valuation tracking. Brand guidelines for 10+ markets/languages. Co-branding and partnership guidelines. M&A brand integration playbook. Brand governance committee with cross-functional membership. Legal trademark management.
- **What's full production**: Brand center of excellence. Annual brand audit. Brand training for all marketers and designers. Brand compliance scoring. Automated design token distribution.
- **Coordination**: Monthly brand council. Quarterly brand compliance review. Annual brand strategy offsite. Legal review for trademark use.

### Transition Triggers
- **Solo → Small**: Second designer or external agency needs brand direction. Inconsistent brand in marketing materials.
- **Small → Medium**: Multiple products or sub-brands. Design system needs consistent tokens. >10 people creating branded content.
- **Medium → Enterprise**: International expansion with localization. M&A activity. >50 people creating branded content across markets.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | product-strategist | Market positioning, audience definition, competitive landscape |
| **This** | brand-guidelines | Brand architecture, identity system, tokens, governance |
| **After** | ui-ux-designer | Design system themed with brand tokens, component library |

Common chains:
- **New brand**: product-strategist → brand-guidelines → ui-ux-designer — from market strategy to branded product UI
- **Brand refresh**: ux-researcher → brand-guidelines → frontend-developer — from audience insights to implemented brand system



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
