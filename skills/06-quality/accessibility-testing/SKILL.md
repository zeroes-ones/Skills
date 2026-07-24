---
name: accessibility-testing
description: >
  Use when implementing automated accessibility testing in CI/CD pipelines, setting
  up WCAG 2.2 AA compliance gates, building accessibility monitoring dashboards, or
  integrating axe-core across test layers. Handles automated screen reader testing,
  visual regression for accessibility, accessibility linting, and test strategy
  across the testing pyramid. Do NOT use for manual accessibility audits, general QA
  strategy without a11y focus, or UI design system creation.
author: Sandeep Kumar Penchala
license: MIT
type: quality
status: stable
version: 1.1.0
updated: 2026-07-23
tags:
- accessibility
- a11y
- wcag
- axe-core
- ci-cd
- testing
- lighthouse
- pa11y
token_budget: 3500
chain:
  consumes_from:
  - accessibility-auditor
  - ci-cd-builder
  - qa-engineer
  - tdd-guide
  feeds_into:
  - accessibility-auditor
  - frontend-developer
  - mobile-developer
  - qa-engineer
---

# Accessibility Testing
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Build automated accessibility testing into every layer of the CI/CD pipeline — catch violations at lint time, component test time, e2e test time, and in production monitoring before users do.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("package.json", "\"axe-core\"\|\"jest-axe\"\|\"@axe-core/playwright\"\|\"cypress-axe\"\|\"pa11y\"")` OR `file_contains("*", "accessibility.*test\|a11y.*test\|axe\(\)\|pa11y")` | This is your skill. Jump to **Core Workflow** — Phase 2 (CI Integration). |
| A2 | `file_contains(".github/workflows/*", "axe\|pa11y\|lighthouse.*accessibility\|a11y")` OR `file_contains("lighthouserc", "\"accessibility\"")` | Jump to **Best Practices** — CI Gates. |
| A3 | `file_contains("package.json", "\"eslint-plugin-jsx-a11y\"")` AND `file_contains("*", "aria-\|role=\|tabIndex\|alt=\|htmlFor")` | Jump to **Best Practices** — Linting. |
| A4 | `file_contains("*", "VoiceOver\|TalkBack\|NVDA\|screen.*reader\|assistive.*tech")` | Jump to **Decision Trees** — Screen Reader Automation. |
| A5 | `file_contains("*", "WCAG\|Section.*508\|EN.*301.*549\|ADA\|accessibility.*standard\|compliance")` | Jump to **Error Decoder** — Compliance Gap section. |
| A6 | `file_contains("*", "prefers-reduced-motion\|prefers-color-scheme\|prefers-contrast\|forced-colors")` | Jump to **Core Workflow** — Phase 1 (User Preference Testing). |
| A7 | `file_contains("*", "keyboard\|focus.*trap\|tab.*order\|skip.*link\|focus.*visible")` | Jump to **Production Checklist** — AT13 (Keyboard Navigation). |
| A8 | `file_contains("*", "aria-live\|role=\"alert\"\|role=\"status\"\|dynamic.*content")` AND `file_contains("*", "SPA\|router\|navigation\|page.*change")` | Jump to **Error Decoder** — Dynamic Content Announcements. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What do you need?
├── Add a11y testing to existing CI/CD → Jump to "Core Workflow > Phase 2"
├── Set up axe-core in unit/component tests → Go to "Core Workflow > Phase 1"
├── Add Lighthouse CI accessibility budgets → Jump to "Best Practices > CI Gates"
├── Automate screen reader testing → Go to "Decision Trees > Screen Reader Automation"
├── Catch a11y regressions on every PR → Jump to "Core Workflow > Phase 3"
├── Add a11y linting to IDE and pre-commit → Go to "Best Practices > Linting"
├── Build an accessibility monitoring dashboard → Jump to "Core Workflow > Phase 4"
├── Need manual accessibility audit → Invoke accessibility-auditor skill instead
├── Need QA test strategy including a11y → Invoke qa-engineer skill instead
├── Need CI/CD pipeline integration → Invoke ci-cd-builder skill instead
├── Need frontend a11y implementation → Invoke frontend-developer skill instead
├── Need mobile a11y testing → Invoke mobile-developer skill instead
└── Mobile accessibility testing → Go to "Decision Trees > Mobile A11y"
```

## Ground Rules — Read Before Anything Else

These rules are non-negotiable constraints that detect accessibility testing mistakes before they are given. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE claims of full a11y compliance from automation-only results | Trigger: Report asserts "X% accessible", "fully accessible", or "WCAG compliant" AND data source is exclusively automated tools (axe-core, Lighthouse, pa11y) with no manual testing evidence | STOP. Respond: "Automated tools catch at most 30-40% of accessibility issues. The remaining 60-70% require manual testing — keyboard navigation, screen reader workflows, and cognitive walkthroughs. Automated results are the beginning, not the end. Provide manual test evidence before claiming compliance." |
| R2 | REFUSE severity downgrade of a11y bugs below equivalent functional impact | Trigger: Bug is tagged "accessibility"/"a11y" AND severity is P3/P4/minor AND same functional impact in visual pathway would be P1/P2 | STOP. Respond: "Accessibility bugs are production bugs with legal exposure under ADA, Section 508, and EN 301 549. A checkout flow broken for screen reader users costs revenue AND exposes the company to lawsuits. A11y severity must match functional severity: accessibility P2 = functional P1. Reclassify before proceeding." |
| R3 | REFUSE unit-level-only a11y testing without integration verification | Trigger: All a11y test files target individual components AND zero page-level or composed-component a11y tests exist in the test suite | STOP. Respond: "Components that pass axe-core in isolation may fail when composed — focus order conflicts, heading hierarchy collisions, and aria-owns cross-boundary issues only surface at integration level. Add at minimum one page-level a11y scan per critical user flow before proceeding." |
| R4 | REFUSE Lighthouse 100 score cited as proof of full accessibility | Trigger: Output contains "Lighthouse 100", "perfect Lighthouse score", or "Lighthouse accessibility score of 100" AND context implies full compliance/conformance | STOP. Respond: "Lighthouse runs ~30 automated checks. It cannot detect focus management bugs during SPA navigation, aria-live announcement failures, keyboard trap scenarios, or screen reader UX issues. A 100 score means the easy stuff passed — it does NOT mean the page is accessible. Manual keyboard and screen reader testing are still required." |
| R5 | REFUSE point-in-time audit as ongoing compliance proof | Trigger: Compliance claim references a date-stamped audit report older than the most recent production deployment | STOP. Respond: "Accessibility monitoring must be continuous, not point-in-time. Since the last audit, new components, dependency updates, and content changes may have introduced regressions. Configure CI/CD a11y gates that run on every PR before accepting a compliance claim." |
| R6 | REFUSE a11y test strategy without explicit keyboard navigation pass | Trigger: Test plan/test strategy document lacks explicit step for keyboard-only navigation testing (Tab, Enter, Escape, arrow keys through all interactive elements) | STOP. Respond: "Keyboard navigation is the foundation of accessible interaction. Users with motor disabilities, screen reader users, and power users all rely on keyboard-only operation. Every a11y test strategy must include: (1) Tab order verification, (2) focus visibility check, (3) no keyboard traps, (4) all interactive elements reachable and operable without a mouse." |
| R7 | REFUSE a11y test strategy without screen reader workflow pass | Trigger: Test plan/test strategy lacks explicit screen reader testing step with named assistive technology (NVDA, JAWS, VoiceOver, TalkBack) | STOP. Respond: "Screen reader testing is required for WCAG 2.2 AA compliance. Automated tools cannot verify that dynamic content is properly announced, that aria-live regions fire correctly, or that navigation landmarks are usable. Include at minimum one screen reader (VoiceOver on macOS, NVDA on Windows) workflow pass per critical user journey." |
| R8 | DETECT and WARN when accessibility is treated as a QA-only activity that happens at the end of the development cycle | Trigger: accessibility testing mentioned only in QA phase or as a pre-release gate without evidence of design-time and development-time a11y activities | WARN. Shift left: (1) Design: annotate UI specs with heading levels, landmark regions, focus order, and accessible names. (2) Dev: eslint-plugin-jsx-a11y at IDE-time, jest-axe at unit test time. (3) CI: axe-core at PR time. (4) QA: manual keyboard + screen reader testing. Each layer finds issues before the next, more expensive, layer is reached. |
| R9 | REFUSE to accept VPATs (Voluntary Product Accessibility Templates) from third-party vendors without independent verification | Trigger: relying on third-party VPAT as sole evidence of accessibility for an integrated component or service | STOP. Require: (1) Run axe-core against the vendor's product in your integration context, (2) Manual keyboard test of the vendor's UI within your product, (3) Screen reader test of one critical flow involving the vendor's component. Document findings. If the vendor's product creates accessibility barriers, your product is not accessible — regardless of what the VPAT says. |

## The Expert's Mindset

Master accessibility testers know that automated tools catch at most 30-40% of barriers. The rest require **human judgment, assistive technology fluency, and understanding how disabled people actually use the web.** A clean axe-core scan is the beginning, not the end.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Automation coverage illusion** — believing axe-core or Lighthouse covers the full WCAG spectrum | After every automated scan, list the success criteria it CANNOT test: 1.3.2 Meaningful Sequence, 2.4.3 Focus Order, 3.3.2 Labels or Instructions. Manual-test those explicitly. |
| **Visual-centric bias** — designing tests for what sighted users experience, ignoring screen reader, voice control, and switch device users | Every test plan must include at least one non-visual modality: screen reader (NVDA or VoiceOver), keyboard-only, or voice navigation |
| **WCAG-as-ceiling** — treating AA conformance as "done" rather than the minimum bar for usable access | After passing WCAG AA, test with actual disabled users. WCAG doesn't measure: "Can a screen reader user complete checkout in under 5 minutes?" or "Can a voice control user navigate without 47 tab stops?" |
| **Disability-sampling bias** — testing only for blindness and ignoring cognitive, motor, auditory, and seizure disabilities | Maintain a disability matrix: for each feature, document how it works for users with: low vision, blindness, deafness, motor impairment (no mouse), cognitive/learning disabilities, photosensitive epilepsy. A gap in any column is a gap in your test plan. |

### What Masters Know That Others Don't
- **That the most common accessibility failure is not a code bug — it's a design decision made 3 sprints ago that nobody questioned.** Carousels without pause buttons, custom dropdowns without ARIA, color-only error states. Catch these in design review, not QA.
- **How to reproduce the user's actual experience.** They can operate a screen reader at 3x speed, navigate solely by headings/landmarks, and feel the difference between a well-structured page and a div-soup disaster in under 30 seconds.
- **That accessibility fixes compound.** Fixing the component library's focus management fixes every page that uses those components. Find the highest-leverage fix, not the longest bug list.

### When to Break Your Own Rules
- **Ship a partially-accessible feature with a documented remediation plan.** "Not accessible at all" to "keyboard-navigable but screen reader needs work" is progress. Ship the improvement; don't block the release for perfection.
- **Accept a WCAG non-conformance when the accessible alternative is worse for disabled users.** A conforming color contrast that makes text unreadable for users with dyslexia is not accessible. User outcomes over checklists.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single test/review | Execute defined quality procedures; follow checklists |
| **L2** | Feature quality | Own quality for a feature area; write custom test strategies |
| **L3** | System quality | Design quality strategy for a system; define gates and thresholds; mentor |
| **L4** | Org quality | Define org-wide quality standards; make investment cases for quality tooling |
| **L5** | Industry quality | Create quality methodologies adopted across the industry |

**Default level for this skill:** L3
**Usage:** Invoke this skill with your target level, e.g., "as an L3 accessibility testing, review..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

<!-- STANDARD: 3min -->

- You need to integrate automated accessibility testing into existing CI/CD pipelines
- You are setting up axe-core, pa11y, or Lighthouse CI for the first time
- You want to add accessibility linting to the developer workflow (IDE + pre-commit)
- You need to configure accessibility quality gates that block PRs with violations
- You are building an accessibility monitoring system to catch regressions in production
- You need to automate screen reader testing for critical user flows
- You want to add accessibility visual regression testing to catch contrast and layout issues

## Decision Trees

<!-- STANDARD: 3min -->

### Screen Reader Automation

```
What do you need to test with a screen reader?
├── Static page content and heading structure → axe-core + DOM snapshot comparison (no real SR needed)
├── Dynamic content announcements (toasts, live regions) → jest-axe + aria-live assertion tests
├── Navigation flow (tab order, skip links, landmarks) → Playwright + @guidepup/playwright + toBeFocused assertions
│   └── Example: test that Tab key follows landmarks in correct order
├── Form interaction (error announcements, required field cues) → Playwright + VoiceOver/ChromeVox automation
│   └── Use aria-live regions instead of testing actual speech output
└── Full screen reader UX → Manual testing required (automation cannot validate comprehension or usability)
    └── Supplement with: structured manual test scripts that QA follows

```

### Mobile Accessibility Testing

```
Platform?
├── iOS → XCUITest + accessibility Inspector + VoiceOver swipe gestures
│   └── Key checks: accessibilityLabel, accessibilityTraits, Modal dismiss gesture
├── Android → Espresso + AccessibilityChecks.enable() + TalkBack actions
│   └── Key checks: contentDescription, focusable, TouchTargetSizeCheck
├── React Native → @react-native-community/eslint-config + RN accessibility props assertions
│   └── Key checks: accessible, accessibilityLabel, accessibilityRole, importantForAccessibility
└── Flutter → flutter_test + SemanticsHandle + a11y audit in integration_test
    └── Key checks: Semantics widget, excludeFromSemantics, MergeSemantics

```

### CI/CD Gate Configuration

```
What a11y gate severity should you enforce?
├── Startup / early product (< 10 engineers) → Lint-only gate (eslint-plugin-jsx-a11y)
│   ├── Block: zero errors on pre-commit. Warn: violations in CI (non-blocking).
│   ├── Start with recommended ruleset. Add rules incrementally — 2 per sprint.
│   └── Goal: catch 60% of violations at lint time within 3 months.
├── Growth-stage (10-50 engineers) → axe-core in CI + Lighthouse budget
│   ├── Block PR on: zero NEW critical (A) or serious (AA) violations vs stored baseline.
│   ├── Warn on: moderate violations. Create Jira ticket automatically.
│   ├── Lighthouse CI: minimum accessibility score 95. Score drops > 5 points = block.
│   └── Keyboard navigation check: automated tab-order verification via Playwright.
├── Enterprise (50+ engineers, compliance requirements) → Full gates + manual review
│   ├── All growth-stage gates + pa11y-ci on sitemap + screen reader workflow tests.
│   ├── Block release on: any critical (A) violation on a key user flow.
│   ├── Automated VPAT generation from CI audit trail.
│   ├── Quarterly external accessibility audit results fed back into gate thresholds.
│   └── Accessibility score dashboard with per-team accountability and trend lines.
└── What to NEVER block on:
    ├── Minor/needs-review violations — these generate noise, not safety.
    ├── Third-party component violations you can't fix (document with VPAT exception).
    └── Color contrast on disabled elements (WCAG exempts inactive UI components).
```

### Manual Testing Strategy

```
How should you prioritize manual accessibility testing effort?
├── Top 5 user flows (checkout, signup, search, settings, help) → Screen reader end-to-end walkthrough
│   ├── Test with: NVDA + Firefox (Windows), VoiceOver + Safari (macOS/iOS), TalkBack + Chrome (Android)
│   ├── Before testing: clear cookies, log out, start fresh. Don't skip any step.
│   ├── Document: "Can a screen reader user complete this flow independently in under 2x the time of a sighted user?"
│   ├── Record: screen + audio. Review with developers. Nothing communicates a11y issues like experiencing them.
│   └── Cadence: every release, rotate through 2 of the top 5 flows. Every flow tested at least quarterly.
├── Component library (buttons, modals, forms, tables, dropdowns, tabs) → Keyboard + axe-core on isolated components
│   ├── Every component: axe-core audit + keyboard interaction test (Tab, Enter, Escape, Arrow keys, Space)
│   ├── Modals specifically: focus trapped inside modal, focus returns to trigger on close, Escape closes
│   ├── Dynamic content: aria-live announcements tested with screen reader
│   └── Cadence: every new component must pass before being added to the library. Existing components re-tested on breaking changes.
├── Content & media (images, videos, documents, data visualizations) → Content audit
│   ├── Images: alt text audit — is every informative image described? Are decorative images marked as such?
│   ├── Videos: captions accuracy (not auto-generated), audio description track for key visual information
│   ├── Data viz: can the insight be understood from alt text alone? Pattern/texture difference in addition to color.
│   └── Cadence: quarterly content audit on top 20 most-visited pages
└── Accessibility statement & feedback loop → User-reported issues
    ├── Maintain a public accessibility statement with a feedback mechanism (email or form)
    ├── Triage user-reported issues within 48 hours. P1 (blocked from using): 24-hour fix target.
    ├── Track: issues reported per quarter (should decrease as automated testing improves)
    └── Test: the accessibility contact method itself — can a screen reader user actually submit feedback?
```

<!-- DEEP: 10+min -->

## Core Workflow

### Phase 1: Static + Unit-Level Testing (~1 hour setup)
Install and configure linting rules at the earliest detection layer. ESLint: `eslint-plugin-jsx-a11y` with recommended rules (alt-text, anchor-has-content, no-autofocus, tabindex-no-positive). Stylelint: `stylelint-a11y` for color and spacing rules. Run in IDE (real-time feedback) + pre-commit hook (lint-staged) + CI (fails build on violation). Configure axe-core in unit tests: `jest-axe` for React, `vitest-axe` for Vue, `jasmine-axe` for Angular. Test every component in isolation: buttons, inputs, modals, dropdowns, carousels. Store results as JUnit XML for CI dashboard ingestion.

### Phase 2: Integration + E2E Testing (~2 hours setup)
Add axe-core to Playwright or Cypress e2e tests. For Playwright: `@axe-core/playwright` — inject axe into each page, run after every navigation or state change. Configure `axe.run()` with WCAG 2.2 AA tag and specific rule exclusions (document with justification). Add pa11y for page-level audits outside e2e flows: `pa11y-ci` with a sitemap URL list, run on staging deploy. Configure Lighthouse CI: set accessibility score budget to 95 minimum. Store historical data to detect score regressions over time.

### Phase 3: CI/CD Quality Gates (~1 hour setup)
Define violation thresholds per severity level. Critical (WCAG 2.2 A violations): zero tolerance — block PR + notify author. Serious (WCAG 2.2 AA): zero new violations — existing baseline allowed, new violations block PR. Moderate (best practice): warn only — create Jira ticket, don't block. Minor (needs review): informational — no action required. Store baselines per-route in the repository so that intentional improvements update the baseline, not regressions. The gate script: count violations by severity → compare against baseline → apply threshold → return pass/fail.

### Phase 4: Production Monitoring (~1 hour setup)
Configure periodic (daily) accessibility scans of key production pages using pa11y-ci scheduled job or a hosted service (Deque Axe Monitor, Siteimprove, Tenon). Monitor: accessibility score trend, new violation count, and pages with score drops. Alert on: score dropping > 5 points in 24 hours, any new critical/serious violation on a key page, and pages missing from scan coverage. Dashboard: score per route over time, violation breakdown by WCAG criteria, time-to-fix (how long from detection to resolution).

## Cross-Skill Coordination

<!-- STANDARD: 3min -->

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `accessibility-auditor` | WCAG criteria interpretation, manual audit findings, accessibility acceptance criteria, violation priority | Before configuring automated rules; ensures testing tool detects the right patterns |
| `qa-engineer` | Test framework config, Playwright/Cypress integration, test baselines, regression suite structure | Before integrating a11y tests into the test pyramid |
| `ci-cd-builder` | Pipeline config, quality gate scripts, dashboard integration, blocking vs warning thresholds | Before wiring accessibility checks into CI/CD |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `frontend-developer` | ESLint config (jsx-a11y), jest-axe setup, component test patterns, violation baselines per route | Developers ship inaccessible components — expensive retrofit, potential legal exposure |
| `qa-engineer` | Accessibility test suite integration, pa11y-ci config, Lighthouse CI budget, violation regression baselines | QA can't include accessibility in regression testing — gaps in coverage |
| `accessibility-auditor` | Automated violation reports, violation trend data, CI gate pass/fail history | Auditor can only do one-time manual audits — no continuous monitoring |
| `mobile-developer` | Espresso AccessibilityChecks config, XCUITest a11y integration, mobile accessibility CI setup | Mobile ships with accessibility regressions — Play Store/App Store may reject |

### Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| Accessibility score drops >5 points in 24 hours | Accessibility Auditor, Frontend Developer | Investigate regression; may block release |
| New critical (A) or serious (AA) violation found in CI | PR author, Accessibility Auditor | Fix before merge; zero-tolerance for new critical/AA |
| Rule exclusion requested for a component | Accessibility Auditor | Justification review; may require VPAT update |
| Production monitoring detects accessibility degradation | Accessibility Auditor, Frontend Developer | Immediate investigation; legal/compliance risk |

### Escalation Path

```
Blocked by inaccessible third-party component? → Accessibility Auditor → Legal Advisor (VPAT review)
ADA/Section 508 complaint received? → Legal Advisor → Compliance Officer → CTO
Accessibility score < 70 on critical user flow? → Product Manager → CTO Advisor

```

## Proactive Triggers

| Trigger | Action | Rationale |
|---|---|---|
| New UI component added | Run axe-core on component in isolation and within the page layout; verify ARIA labels, roles, and focus management | New components are the most common source of accessibility regressions — catch violations at the component level before they propagate |
| Color scheme, theme, or design token change | Run automated contrast ratio checks on all affected component states (default, hover, focus, disabled, error) | A palette change that passes WCAG AA for one state can fail for another — check the full state matrix |
| New form or form step added | Verify all inputs have persistent labels, error messages are linked via `aria-describedby`, required fields are marked, and keyboard tab order is logical | Forms are the #1 interaction point between users and services — inaccessible forms block core business functions |
| Navigation structure change (menu, tabs, routing) | Test keyboard navigation: verify focus order matches visual order, skip links work, focus is not trapped, and active element is always visible | Navigation is the skeleton of accessibility — if users can't navigate, they can't use anything else |
| Third-party component or library introduced | Audit the component's accessibility documentation and VPAT; run axe against the component in your actual usage context | Third-party components often have incomplete ARIA implementations — test in your real DOM, not the library's demo page |
| CI pipeline for frontend configured | Wire axe-core into component tests and E2E tests; set Lighthouse CI accessibility budget (minimum score 95); enforce zero new critical/serious violations baseline | CI gates prevent regressions from reaching production — the most effective time to catch a violation is before it merges |
| Production accessibility score drops >5 points in 24 hours | Trigger investigation; check recent deploys for DOM structure changes, new components, or third-party script additions | Production monitoring catches regressions that slip through CI — page composition at runtime differs from test environments |

**Service Interaction Designs:**

| Interaction | Design Detail |
|---|---|
| A11y ↔ Frontend | eslint-plugin-jsx-a11y enforces semantic HTML at the IDE level. Component library enforces accessible patterns (required `aria-label` on icon buttons, `alt` text on images). Design system tokens include accessible color pairings with pre-verified contrast ratios. |
| A11y ↔ CI/CD | axe-core integrated into Playwright/Cypress E2E tests — runs after every navigation and DOM mutation. pa11y-ci scans sitemap-based URL list on staging deploy. Lighthouse CI enforces minimum 95 accessibility score with budget. Zero new critical (A) or serious (AA) violations against stored baseline blocks merge. |
| A11y ↔ Mobile | Espresso AccessibilityChecks (Android) and XCUITest accessibility checks (iOS) enabled in mobile CI. Touch target size enforcement (44x44dp minimum). Dynamic type/text resize testing on real devices. Reduced motion preference testing. |
| A11y ↔ QA | Accessibility test suite integrated into the regression suite. Violation baseline tracked per-route. Accessibility debt ratio tracked monthly. QA owns the manual screen reader + keyboard navigation walkthrough for top 5 user flows. |
| A11y ↔ Design | Design tokens include contrast-verified color pairings. Component specs include accessibility requirements (focus order, ARIA roles, keyboard interactions). Design review includes accessibility checklist before handoff. |
| A11y ↔ Legal/Compliance | VPAT (Voluntary Product Accessibility Template) updated per release. WCAG conformance level (A/AA/AAA) documented per feature. ADA/Section 508 compliance evidence collected from CI audit trail. Legal notified of any pattern of accessibility regressions. |

## What Good Looks Like

### BEFORE (Novice) → AFTER (World-Class)

**Testing Coverage:**
- **BEFORE:** Runs axe-core once before release. Score is 92. Declares product "accessible." Ships. ADA demand letter arrives 6 months later citing: focus order violations, missing aria-live announcements, keyboard traps in modals — none of which axe-core detects. Legal fees: $15K-$50K. Emergency remediation: $30K-$100K.
- **AFTER:** Four-layer defense: (1) eslint-plugin-jsx-a11y at IDE + pre-commit (catches ~30%), (2) jest-axe on every component (catches ~30%), (3) axe-core in Playwright e2e on every page after every navigation (catches ~20%), (4) production monitoring with pa11y-ci daily scans and score trend alerts (catches regressions). Manual keyboard + screen reader walkthrough on top 5 flows per release. Automated gates block merging, not just warn. Zero new critical/serious violations policy. External accessibility audit annually.

**Violation Response:**
- **BEFORE:** Accessibility bug filed as P4 ("nice to have"). Sits in backlog for 18 months. Same functional impact in visual pathway would have been P2 and fixed within days. Legal exposure compounds.
- **AFTER:** Accessibility severity matches functional severity. A checkout flow broken for screen reader users = P1 (revenue + legal risk). A heading hierarchy issue on a marketing page = P3. Severity classification enforced by CI: P1/P2 violations block release regardless of whether they're "accessibility" or "functional" — they're both.

**Developer Experience:**
- **BEFORE:** Developer discovers accessibility violation 3 days before release. Fix requires component redesign. Sprint derailed. "Accessibility always blocks our releases" becomes team sentiment. Accessibility becomes the villain.
- **AFTER:** Developer sees a11y violation in their IDE as they type (eslint-plugin-jsx-a11y real-time feedback). Fix takes 2 minutes while the code is fresh. CI confirms fix. Developer never thinks about "accessibility" — the tooling catches everything. Accessibility becomes invisible infrastructure, not a bottleneck.

**What good looks like:** A developer opens a PR that changes a button component from a `<div>` with an onClick handler to a native `<button>`. The CI pipeline runs. ESLint passes (the `<div>` would have been caught by `jsx-a11y/no-static-element-interactions`). Unit tests pass (jest-axe confirms the button has an accessible name). E2e tests pass (axe-core finds no new violations on any page containing the button). The accessibility dashboard in CI shows a green check and a baseline diff of "+0 new, -1 fixed" because the old `<div>` violation is now resolved. The developer didn't think about accessibility at all — the pipeline caught everything. That's what good looks like.

**Accessibility Culture & Governance:**
- **BEFORE:** Accessibility is "owned" by one champion engineer who reviews every PR for a11y issues. When they go on vacation, a11y regressions ship. When they leave the company, a11y knowledge walks out the door. Designers hand off specs without accessibility annotations. The VP of Engineering mentions accessibility in all-hands once per year after a lawsuit scare. No accessibility statement exists on the corporate website. When a user reports a barrier, the feedback goes to an unmonitored inbox. A11y is a person, not a process — and when that person isn't there, a11y doesn't happen. The board has never seen an accessibility metric. Procurement signs contracts with third-party vendors without requiring a VPAT or conducting an a11y review. The legal team finds out about accessibility only when a demand letter arrives.
- **AFTER:** Accessibility is a shared responsibility enforced by infrastructure, not individuals. Design system components have built-in a11y — developers get accessible behavior by default without knowing ARIA. Design specs include heading levels, landmark regions, focus order, and accessible names as standard annotations (same as color hex codes or font sizes). ESLint + CI gates catch violations regardless of who reviews the PR. Accessibility score is a KPI on the engineering dashboard alongside uptime, latency, and error rate. Quarterly a11y training is part of onboarding and ongoing development — every engineer completes at least one keyboard-only and one screen reader task flow per quarter. The company publishes a public accessibility statement with a monitored feedback mechanism and triages user-reported issues within 48 hours (P1 blockers within 24 hours). The board reviews an accessibility scorecard quarterly: violation trends, user-reported issues, audit findings, and VPAT coverage for third-party integrations. Procurement requires a VPAT + independent verification before signing any vendor contract. Legal is proactively looped into accessibility governance — they review the accessibility statement, monitor regulatory changes (ADA Title II updates, European Accessibility Act), and receive CI audit trails as compliance evidence. When the original champion engineer leaves, nothing changes — the pipeline, the design system, the training program, the procurement process, and the board-level accountability ensure accessibility is continuous. The true test: a new hire can ship an accessible feature in their first week without ever talking to the a11y specialist, and a vendor can't get past procurement without proving their product is accessible.

**Governance Metrics Dashboard:**
- **Accessibility debt ratio:** (open a11y violations / total UI components) — tracked monthly, reviewed quarterly at the VP level. Target: < 5%. Above 10% triggers a remediation sprint.
- **Mean time to resolve (MTTR) by severity:** P1 a11y issues (blocks assistive technology users from core flows) resolved within 24 hours. P2 within one sprint. P3 within two sprints. Dashboard shows MTTR trend — increasing MTTR signals a process breakdown.
- **Automated coverage ratio:** percentage of WCAG 2.2 AA success criteria covered by automated checks in CI. Baseline: ~30% (axe-core's coverage). Target: 30% automated + 70% manual documented. A gap in either column is a gap in your defense.
- **VPAT accuracy score:** for every third-party component with a vendor VPAT, the percentage of VPAT claims verified by independent testing. A vendor scoring below 80% accuracy is flagged for replacement or contractual remediation.
- **User-reported issue trend:** accessibility issues reported by actual users per quarter. Should decrease as automated coverage increases and manual testing matures. An increase signals a regression blind spot — investigate immediately.
- **Training participation rate:** percentage of engineers who completed quarterly a11y training (keyboard-only + screen reader task flow). Target: 100%. Below 90% triggers a manager escalation.

**Testing Cadence by Layer:**

| Layer | Frequency | Tool | Threshold | Owner |
|-------|-----------|------|-----------|-------|
| IDE (lint) | Real-time as-you-type | eslint-plugin-jsx-a11y, stylelint-a11y | Zero errors (configured rules) | Individual developer |
| Pre-commit | Every commit | lint-staged + jsx-a11y | Block commit on new violations | Individual developer |
| Unit/Component | Every test run | jest-axe, vitest-axe, jasmine-axe | Zero critical (A) violations | CI pipeline |
| Integration/E2E | Every PR | @axe-core/playwright, cypress-axe | Zero new critical/serious vs baseline | CI pipeline |
| Page-level audit | Every staging deploy | pa11y-ci, Lighthouse CI | Score ≥ 95, drops > 5 = block | CI pipeline |
| Production scan | Daily | pa11y-ci scheduled job | Alert on new critical/serious | Monitoring system |
| Manual keyboard | Every release | Structured test script | All interactive elements reachable | QA engineer |
| Manual screen reader | Every release (rotate 2 of top 5 flows) | NVDA, VoiceOver, TalkBack | Flow completable independently | QA engineer |
| External audit | Annually | Third-party accessibility auditor | Remediation plan for all findings | VP Engineering |
| User testing with PwD | Quarterly | Fable, Access Works, or internal panel | Task completion rate ≥ sighted baseline | Product Manager |

## Deliberate Practice

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Install eslint-plugin-jsx-a11y on a real project with zero a11y tooling. Run it. Fix every violation. Time yourself. Repeat with a different project — can you fix them faster by recognizing patterns? | Monthly |
| **Competent** | Take a production web app and run axe-core against all pages. Then run a manual keyboard-only navigation of the same pages. Compare findings: what did axe miss? Build a checklist of manual-only checks based on what you found. | Biweekly |
| **Expert** | Design a CI/CD a11y pipeline for a 50-engineer org: lint rules, component test integration, e2e integration, Lighthouse CI budget, production monitoring, violation baseline management, and a per-team accessibility score dashboard. Implement it on a sample project and measure: false positive rate, time-to-detect, developer friction. | Quarterly |
| **Master** | Teach a frontend team with zero a11y experience to self-sufficiently maintain accessibility in 3 months. Design the curriculum: Week 1-2 (automated tooling), Week 3-6 (manual testing skills), Week 7-10 (screen reader proficiency), Week 11-12 (independent audit capability). Measure: can they pass an external accessibility audit without your involvement? | Annually |

**The One Highest-Leverage Activity:** Keep a "mistakes journal." Every time an accessibility issue reaches production, write down: what escaped detection, which layer should have caught it (lint/unit/e2e/monitoring), and what rule or check would prevent it next time. After 10 entries, you'll see patterns in your pipeline's blind spots.

## Gotchas

- **Automated-only a11y testing.** Running axe-core or Lighthouse in CI and declaring the product "accessible" because the automated score is 100. Automated tools catch only ~30-40% of WCAG issues: focus order, keyboard traps, meaningful alt text semantics, heading hierarchy correctness, and dynamic content announcements all require human judgment. The 60-70% of issues that slip through are exactly what plaintiffs' firms scan for when sending ADA demand letters — and automated passing provides no legal defense. **Total cost: $15,000-$50,000 in missed violations leading to ADA demand letters, legal fees, and emergency remediation.** Fix: Combine automated testing with manual keyboard audits, screen reader testing (VoiceOver/NVDA/JAWS), and periodic external accessibility audits; use axe-core as a safety net, not a certification.
- **Running a11y tests only before release.** Accessibility checks happen in the final QA gate, days before launch. Issues found then — a missing `aria-label` on a critical CTA, a keyboard trap in a checkout flow — require design review, code changes, retesting, and release delay. Fixing the same issue during development costs ~$200 in developer time; fixing it post-release costs $500-$2,000+ with hotfix overhead, and fixing it after an ADA complaint adds $5,000-$50,000 in legal exposure. **Total cost: $10,000-$75,000 per year in emergency fixes ($500-$2,000 each) vs. $2,000 in-shift fixes ($200 each for 10 issues).** Fix: Shift a11y testing left — run axe-core on every PR, require keyboard testing during development, block merge on a11y regressions; integrate pa11y or Lighthouse CI as a quality gate with enforced thresholds.
- **axe-core detects ~30-40% of WCAG issues** automatically. The remaining 60-70% require manual testing: focus order, keyboard traps, meaningful alt text, heading hierarchy semantics, and color contrast in dynamic states. Automated passing ≠ accessible.
- **`aria-label` overrides visible text** but screen readers vary in how they handle this. JAWS announces `aria-label`, NVDA announces both, VoiceOver announces `aria-label` only if the element is interactive. Don't rely on `aria-label` alone for critical information.
- **`role="button"` on a `<div>`** doesn't get keyboard handling for free. You must add `tabindex="0"`, `onKeyDown` for Enter/Space, and prevent default behavior. Native `<button>` does all this automatically — prefer it.
- **Color contrast ratio 4.5:1** is minimum for AA, but large text (18px+ bold or 24px+ regular) only needs 3:1. Many tools report false failures for large text that actually passes.
- **`display: none` and `aria-hidden="true"`** both hide from screen readers, but `display: none` also hides from keyboard focus while `aria-hidden` does not. An `aria-hidden` modal overlay is still keyboard-navigable — users can tab to invisible elements.
- **Never testing with actual assistive technology users.** Automated tests pass, manual keyboard checks by sighted developers pass, and screen reader testing by non-disabled QA engineers passes — but actual screen reader users encounter cascading usability failures. Navigation order is logical to someone who can see the layout but nonsensical when read linearly, live regions update too frequently and interrupt the user mid-task, and custom widgets implement WAI-ARIA patterns in ways that behave correctly in testing tools but confuse real AT users. **Total cost: $10,000-$40,000 in post-release remediation for issues only real AT users discover, plus legal exposure from technically-passing but practically-inaccessible UI that fails the "equivalent experience" standard in ADA litigation.** Fix: Include people with disabilities in usability testing at least once per major release cycle; contract with accessibility-focused testing services (Fable, Access Works) for structured AT-user feedback; maintain a standing panel of assistive technology users for quarterly feedback sessions; complement automated conformance testing with task-completion testing by real AT users.
- **Dynamic content updates without ARIA live region announcements.** A React SPA updates search results as the user types, a chat message arrives in the background, or a form validation error appears below a field — all via DOM mutation with no `aria-live` region markup. Screen reader users have no idea the page content changed. They submit a form, perceive no response, resubmit, get rate-limited, and abandon the task entirely. **Total cost: $5,000-$25,000 in permanently lost conversions from inaccessible dynamic UIs, plus a growing volume of support tickets from frustrated assistive technology users who cannot complete core product flows.** Fix: Wrap every dynamically updating content region in an appropriate `aria-live` container (`aria-live="polite"` for non-urgent updates, `aria-live="assertive"` for critical errors and alerts); use `aria-atomic` to control whether the full region or only changed content is announced; test every dynamic interaction with a running screen reader; add an accessibility lint rule that flags DOM mutations without corresponding live region markup.
- **Focus management abandoned after SPA route transitions.** In a traditional multi-page app, focus resets to the top of the document on navigation. In a SPA, when React Router or Next.js changes routes, the browser keeps focus on the link the user just clicked — now hidden behind the new page content. Screen reader users tab forward and land on a random element mid-page with zero context of where they are or what page loaded. They become disoriented and leave. **Total cost: $5,000-$20,000 in lost user engagement from screen reader users who find the SPA fundamentally disorienting, plus legal exposure from non-compliant client-side navigation that violates WCAG 2.4.3 Focus Order.** Fix: Move focus to a skip-link or the page `<h1>` on every route change; announce page transitions with a visually hidden live region (`<div aria-live="polite" className="sr-only">`); implement a focus management utility that runs after every navigation event; test every route transition with VoiceOver (macOS) or NVDA (Windows) to verify the experience.
- **Testing only keyboard navigation (Tab key) and ignoring screen reader workflows.** 60% of web accessibility issues are screen-reader-specific: missing ARIA labels, incorrect heading hierarchy, dynamic content without aria-live announcements, unlabeled form controls, and custom widgets that are invisible to assistive technology. A site that passes keyboard-only testing can still be completely unusable with a screen reader. **Total cost: $15K-$50K in legal demand letter settlement plus $30K-$100K in emergency remediation when a screen reader user files a complaint.** Fix: Every release cycle, complete one end-to-end screen reader task flow (e.g., "complete purchase using NVDA+Firefox" or "create account using VoiceOver+Safari"). Rotate through AT/browser combinations. This catches the issues automated testing and keyboard-only testing miss.
- **Buying an accessibility overlay solution (AccessiBe, AudioEye, etc.) and declaring the site "accessible."** Overlays inject JavaScript that attempts to fix accessibility issues at runtime. They cannot fix: semantic HTML structure, keyboard focus management, form labeling, or custom component accessibility — which together represent 70%+ of real accessibility barriers. They introduce performance overhead, conflict with actual assistive technology, and create a false sense of compliance. Over 500 accessibility professionals have signed the Overlay Fact Sheet stating these tools cannot make sites compliant. Yet companies continue buying them because the sales pitch ("one line of code," "$49/month") is compelling. **Total cost: $2K-$10K/year in overlay subscription + $15K-$50K+ in legal exposure because overlay-protected sites are still being sued (and losing).** Fix: Invest overlay budget into developer a11y training, automated testing infrastructure (axe-core, pa11y, Lighthouse CI), and manual testing. An overlay is a legal liability, not a solution.
- **Relying on accessibility audits as a one-time activity rather than continuous monitoring.** An accessibility audit produces a clean report on Tuesday. On Wednesday, a developer ships a modal without focus trapping. Thursday, marketing adds a new landing page with contrast issues. By next week, 15% of the audit findings have regressed. By next quarter, the site is back to pre-audit accessibility levels — but the VP of Engineering reports "we passed an accessibility audit" to the board. **Total cost: $25K-$50K per audit that becomes obsolete within weeks + ongoing legal exposure as regressions accumulate.** Fix: Audit identifies baseline. CI/CD pipeline prevents regression. Automated scans run on every PR and every production deploy. Dashboard tracks accessibility score over time with alerts for drops. Re-audit manually annually, but the automated pipeline maintains quality between audits.

## Verification

- [ ] Run `axe-core` in CI: zero violations at WCAG 2.2 AA level
- [ ] Run `pa11y` or `lighthouse --only-categories=accessibility` — score ≥ 95
- [ ] Keyboard audit: tab through every interactive element — no keyboard traps, logical focus order
- [ ] Screen reader audit: Navigate main flow with VoiceOver (macOS) or NVDA (Windows) — all content announced, all actions reachable
- [ ] Color contrast: verify all text/UI components pass 4.5:1 (text) and 3:1 (large text/icons) using `axe` or `contrast-ratio` tool
- [ ] Verify `eslint-plugin-jsx-a11y` passes with zero errors in CI
- [ ] Third-party components: axe-core scan in integration context; keyboard and screen reader test of one flow involving each vendor component
- [ ] Accessibility statement published and feedback mechanism tested with a screen reader
- [ ] CI quality gates configured: zero new critical/serious violations vs baseline blocks PR merge

## References

Detailed reference material loaded on demand:

- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Negative Constraints**: See [negative-constraints.md](references/negative-constraints.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)

