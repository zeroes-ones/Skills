# Preparation

This statement was prepared on [Date]. It was last reviewed on [Date].
```

---
### Phase 9 (~20 min): Legal Landscape

| Law/Standard | Jurisdiction | Applies To | Key Requirement |
|-------------|-------------|------------|-----------------|
| **ADA Title III** | USA | Places of public accommodation (websites, apps considered places) | "Reasonable accommodation" — courts have consistently interpreted this as WCAG 2.1 AA |
| **Section 508** | USA | Federal agencies and contractors | WCAG 2.0 AA (refreshed to 2.1 in 2028) + ICT requirements |
| **EN 301 549** | EU | Public sector bodies, increasingly private sector via EAA | WCAG 2.1 AA — harmonized European standard |
| **European Accessibility Act (EAA)** | EU | Products and services sold in EU (effective June 2025) | WCAG 2.1 AA for e-commerce, banking, transport, e-books, ATMs |
| **AODA** | Ontario, Canada | Public & private sector orgs with 50+ employees | WCAG 2.0 AA (moving to 2.1) |

**Risk assessment factors:**
- **High risk:** E-commerce, banking, healthcare, education, government. These sectors see the most lawsuits.
- **Medium risk:** B2B SaaS, media/publishing, real estate.
- **Lower risk:** Internal tools, developer tools, early-stage startups (though this is changing).

---
### Phase 10: Remediation Prioritization

Use severity-based triage — prioritize by user impact, not by WCAG level:

| Severity | Description | Example | Response |
|----------|-------------|---------|----------|
| **Blocker** | User literally **cannot** complete a core task | Checkout button not keyboard-accessible | Fix immediately — same sprint |
| **Critical** | User can complete task but with **extreme difficulty** or **no alternative** | CAPTCHA without audio alternative | Fix within 2 weeks |
| **Major** | User can complete task with **significant friction** | Missing form error association, requiring guessing which field errored | Fix within 1 month |
| **Minor** | **Annoying** but workaround exists | Heading level skipped, causing confusing navigation | Fix within 3 months |
| **Cosmetic** | Best practice, minimal user impact | Missing `lang` attribute on a single quoted phrase | Backlog — fix opportunistically |

**Blocker → Critical → Major → Minor → Cosmetic.** Fix in that order, regardless of WCAG level. A Level A issue that blocks users is more urgent than a Level AA issue that's cosmetic.
