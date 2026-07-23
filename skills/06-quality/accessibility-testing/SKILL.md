---
name: accessibility-testing
description: Automated accessibility testing in CI/CD pipelines — axe-core integration
  (unit tests, e2e, component tests), pa11y and Lighthouse CI for page-level audits,
  HTML CodeSniffer for continuous scanning, automated screen reader testing patterns,
  visual regression testing for accessibility (color contrast diffs, focus ring visibility),
  accessibility linting (eslint-plugin-jsx-a11y, stylelint-a11y, Android Lint accessibility
  checks, SwiftLint a11y rules), CI/CD quality gates with WCAG 2.2 AA compliance thresholds,
  accessibility monitoring and regression detection, test strategy across the testing
  pyramid (static → unit → integration → e2e), and accessibility score dashboards.
  Use when implementing automated a11y testing, setting up CI/CD accessibility gates,
  or building an accessibility monitoring system.
author: Sandeep Kumar Penchala
type: quality
status: stable
version: 1.0.0
updated: 2027-01-21
tags:
- accessibility
- a11y
- testing
- ci-cd
- wcag
- automation
token_budget: 3500
output:
  type: code
  path_hint: ./
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

Build automated accessibility testing into every layer of the CI/CD pipeline — catch violations at lint time, component test time, e2e test time, and in production monitoring before users do.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
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
<!-- STANDARD: 3min -->

- **Accessibility bugs are production bugs with legal exposure.** A broken checkout flow costs revenue. A broken checkout flow that only affects screen reader users costs revenue AND exposes the company to ADA lawsuits. The severity classification must reflect this: accessibility P2 = functional P1.
- **Automated testing catches ~30-40% of accessibility issues.** The remaining 60-70% require manual testing (keyboard navigation, screen reader workflow, cognitive walkthrough). Automated testing is necessary but not sufficient. Never claim "100% a11y coverage" from automation alone.
- **Every passed accessibility check is a snapshot in time, not a guarantee.** A component that passes axe-core in isolation may fail when composed into a page with other components (focus order conflicts, heading hierarchy collisions, aria-owns cross-boundary issues). Always test at the integration level, not just the unit level.
- **Lighthouse accessibility score of 100 does NOT mean fully accessible.** Lighthouse tests ~30 automated checks. It cannot detect focus management bugs during SPA navigation, dynamic content announcements with aria-live, or keyboard trap scenarios. A 100 score is a green light for the easy stuff — manual testing covers the rest.
- **Accessibility monitoring must be continuous, not point-in-time.** The homepage passed WCAG 2.2 AA in last month's audit. Since then: the marketing team added a carousel (no pause button), the engineering team migrated to a new modal library (no focus trap), and the design team updated the color palette (new gray-on-white contrast ratio: 2.8:1, minimum: 4.5:1). Continuous monitoring catches these within 24 hours, not at the next annual audit.

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

## Best Practices
<!-- DEEP: 10+min -->
1. **Test after every DOM mutation, not just on page load.** SPA navigation, modal opens, tab switches, and infinite scroll all change the DOM. axe-core must re-run after each of these events. A page that passes on load can fail after the user opens a menu.
2. **Never globally exclude rules.** If you must exclude a rule, do it per-component or per-page with a comment explaining why and a ticket tracking the fix. Global exclusions hide regressions.
3. **Accessibility snapshot testing is fragile but valuable.** Storing axe-core results as snapshots means any DOM change may update the snapshot — but it forces developers to consciously acknowledge accessibility changes. Use sparingly on stable components.
4. **Color contrast is the most common violation — automate it everywhere.** Axe-core catches most contrast issues, but gradient backgrounds, images with text, and CSS pseudo-elements may be missed. Supplement with visual regression testing focused on contrast ratios.
5. **Track the accessibility debt ratio.** `(open violations / total checks) × 100`. A ratio trending down means the team is fixing faster than creating. A ratio trending up means the opposite. Review monthly.
6. **Focus order testing requires real keyboard simulation.** `page.keyboard.press('Tab')` in Playwright is not the same as the browser's native Tab behavior. Use `page.locator('body').press('Tab')` and verify `document.activeElement` matches the expected next element.
7. **Prefer integration tests over unit tests for a11y.** A `<Button>` component may pass axe in isolation. But 5 `<Button>` components with conflicting aria-labels inside a `<nav>` may fail at the integration level. The most common a11y bugs are compositional, not isolated.
8. **Mobile accessibility is not "small desktop accessibility."** Touch target size (minimum 44x44 CSS pixels), screen reader swipe gestures, dynamic type/text resize support, and reduced motion preferences are unique to mobile. Test on real devices, not just responsive viewports.

## Anti-Patterns

- **axe-only testing**: Believing a clean axe-core scan means the application is accessible. Automated tools catch ~30% of WCAG violations. Keyboard traps, focus management, cognitive barriers, and screen reader usability are invisible to automation. Always supplement with manual keyboard + screen reader walkthroughs.
- **Accessibility as a final step**: Running accessibility checks only before release instead of integrating them into the development workflow. Retrofitting accessibility is 10x more expensive than building it in. Shift-left: lint rules in IDE, axe in component tests, pa11y in CI on every PR.
- **ARIA misapplication**: Adding `aria-*` attributes without understanding their semantics — `aria-label` overriding visible text, missing required `aria-*` parent/child relationships, or using ARIA to "fix" inaccessible native elements. First rule of ARIA: don't use ARIA if native HTML works.
- **Color-only indicators**: Using color as the sole differentiator for state (red/green for error/success, blue links indistinguishable from body text). Users with color vision deficiency cannot perceive these distinctions. Always pair color with an icon, text label, or pattern.
- **Skip-link theater**: Adding a "Skip to main content" link that exists in the DOM but is non-functional (wrong target, hidden from focus order, or positioned off-screen without `:focus` styles). Test skip links with keyboard navigation — they must actually work.
- **Responsive ≠ accessible**: Assuming that a responsive layout is automatically accessible. Zooming to 200% can break layouts, fixed-position elements can overlap, and touch targets can shrink below 44x44px on smaller viewports. Test at 200% zoom and on real mobile devices.
- **Placeholder-as-label**: Using `placeholder` attributes as the only label for form inputs. Placeholders disappear on focus, have low contrast, and are not consistently announced by screen readers. Every input must have a persistent `<label>` or `aria-label`.
- **Animation without preference check**: Adding animations, parallax, or auto-playing video without respecting `prefers-reduced-motion: reduce`. Vestibular disorders make motion-triggered effects physically harmful. Wrap all animations in a media query check.

<!-- DEEP: 10+min -->
## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| WCAG audit passed with zero violations — manual audit found 47 critical failures | Automated testing only catches ~30% of WCAG issues. Manual-only violations (keyboard traps, focus management, cognitive barriers) are invisible to automation. | Never equate "axe passes" with "accessible." Run automated checks as a floor, not a ceiling. Every release must include manual keyboard navigation + screen reader walkthrough of top 5 user flows. | Automated accessibility testing is necessary but insufficient. Budget for manual audits proportional to the risk — a 100 Lighthouse score does not mean your app is usable by assistive technology. |
| Screen reader automation tests passed — user reported app completely unusable with VoiceOver | Automation tested with ChromeVox on desktop, but 82% of screen reader users on iOS use VoiceOver. Swipe gestures, rotor navigation, and dynamic content announcements differ radically between platforms. | Test with the actual screen reader your users use. For iOS: VoiceOver + XCUITest. For Android: TalkBack + Espresso. Desktop automation (JAWS/NVDA) does not substitute for mobile screen reader testing. | Platform matters. Screen reader behavior is not portable across OS/browser combinations. Test on the platform your users are on — automation on the wrong platform creates false confidence. |
| Color contrast ratio check passed (4.61:1) — user with low vision reported text unreadable | Automated check measured static text contrast. The problematic text was on a gradient background where the effective contrast ratio dropped to 2.3:1 in the middle of the gradient. | Always test contrast on the rendered background, not the CSS variable. For gradient/overlay backgrounds, test at 3+ sampling points. Use visual regression diffing to catch rendering-dependent contrast issues. | Color contrast is a rendering concern, not a code concern. Static CSS analysis misses runtime composition — gradient overlays, background images, and alpha blending all change effective contrast. |
| "No violations found" — component renders nothing in the test | Axe can't find violations on an empty DOM. The component test imported the component but didn't render it into the DOM tree. | Assert that the component renders expected interactive elements before running axe. Minimum: verify at least one button/input/link exists in the rendered output before running accessibility checks. | A test that passes because it tests nothing is worse than no test. Always verify the test subject rendered before checking accessibility. |
| CI gate blocks every PR with 47 "new" violations | Baseline was set to zero, so every pre-existing violation appears as a "new" violation. Every PR has 47 blockers — team starts flagging them as "won't fix." | Import existing violations as the baseline. Only changes (new or fixed) are flagged against the baseline. Reduce baseline by 10% each quarter to show continuous improvement. | If every PR fails, nobody takes the gate seriously. Set a realistic baseline and measure trend, not absolute count. |
| Screen reader announced "button" instead of meaningful label | Interactive element used a generic `<button>` with no `aria-label` or visible text — screen reader announced "button" with no context about what the button does | Every interactive element must have an accessible name. For icon-only buttons, use `aria-label`. For links, meaningful text between `<a>` tags. Test with actual screen reader, not just code review. | A SaaS app's "Save" button had no text content — just an SVG icon. VoiceOver announced "button" and users had to guess its purpose. Post-launch audit found 34 instances of unlabeled interactive elements across the app. |
| Focus trap made form unusable for keyboard-only users | Custom date picker modal trapped focus in an infinite loop — Tab never exited the modal, keyboard users were stuck and couldn't submit the form | Implement accessible focus management: trap focus within modals, close on Escape, return focus to trigger element on close. Test with keyboard-only navigation (no mouse) before shipping. | A government services portal's multi-step form trapped a blind user in the "date of birth" modal. They couldn't complete the application and had to call support. The lawsuit threat resulted in a $50K accessibility retrofit. |
| Touch target too small for users with motor impairments — 32px instead of 44px minimum | Button was sized to `24px` with `8px` padding — effective tap target was 32px, below Apple's 44px HIG minimum and WCAG 2.5.8 (44x44) | All interactive touch targets must be at least 44x44px. Use `min-width`/`min-height` on interactive elements. For responsive layouts, never let interactive elements shrink below minimum. | A meditation app's "Play" button was 32x32px on iPhone SE. Users with essential tremor couldn't reliably tap it. App Store reviews repeatedly mentioned the issue for 6 months before the 44px fix was shipped. |
| Dynamic content announcements were completely silent for screen reader users | Content updated via AJAX without ARIA live regions — screen reader users never knew new content appeared | Use `aria-live="polite"` for dynamic updates (chat messages, notifications, search results). Use `role="alert"` for time-sensitive updates. Test live regions with actual screen reader. | A stock trading app's price updates were invisible to screen reader users. A blind investor sold shares at the wrong price because the app never announced the real-time price change. The trading error cost $8K and was reported to the SEC. |
| Drag-and-drop interface completely inaccessible to keyboard users | Reorderable list used HTML5 drag-and-drop which is fundamentally inaccessible — no keyboard support, no screen reader announcements, no focus management | Implement accessible reordering: use up/down/increase buttons instead of drag-and-drop, or implement keyboard-based drag with `aria-grabbed` and `aria-dropeffect`. Never rely on HTML5 drag-and-drop as the only interaction. | A project management tool launched a Kanban board where tasks could only be reordered by dragging. A user with repetitive strain injury couldn't use drag-and-drop at all. The feature was reported as a barrier under the ADA. |

## Production Checklist
<!-- STANDARD: 3min -->

- [ ] [AT1] eslint-plugin-jsx-a11y installed with recommended ruleset, running in IDE and pre-commit
- [ ] [AT2] jest-axe (or framework equivalent) integrated into component unit tests
- [ ] [AT3] @axe-core/playwright or cypress-axe integrated into e2e test suite, runs after every navigation
- [ ] [AT4] pa11y-ci configured with sitemap-based URL list, runs on staging deploy
- [ ] [AT5] Lighthouse CI accessibility budget set: minimum score 95
- [ ] [AT6] CI/CD quality gate: zero new critical (A) or serious (AA) violations compared to baseline
- [ ] [AT7] Violation baseline stored per-route in repository, updated with intentional improvements
- [ ] [AT8] Rule exclusions documented per-component with justification and fix tracking ticket
- [ ] [AT9] Production monitoring: daily accessibility scan of top 20 pages
- [ ] [AT10] Alert configured for accessibility score drop > 5 points in 24 hours
- [ ] [AT11] Mobile accessibility: Espresso AccessibilityChecks (Android) and XCUITest a11y checks (iOS) enabled
- [ ] [AT12] Accessibility debt ratio tracked monthly with trend analysis
- [ ] [AT13] Keyboard navigation test covers tab order, skip links, focus traps, and escape key behavior
- [ ] [AT14] Screen reader test scripts maintained for top 5 user flows (manual, not automated)

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

## Scale Depth: Solo → Small → Medium → Enterprise
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

## What Good Looks Like
<!-- STANDARD: 3min -->

**What good looks like:** A developer opens a PR that changes a button component from a `<div>` with an onClick handler to a native `<button>`. The CI pipeline runs. ESLint passes (the `<div>` would have been caught by `jsx-a11y/no-static-element-interactions`). Unit tests pass (jest-axe confirms the button has an accessible name). E2e tests pass (axe-core finds no new violations on any page containing the button). The accessibility dashboard in CI shows a green check and a baseline diff of "+0 new, -1 fixed" because the old `<div>` violation is now resolved. The developer didn't think about accessibility at all — the pipeline caught everything. That's what good looks like.

## References
<!-- STANDARD: 3min -->

- axe-core API Reference: https://github.com/dequelabs/axe-core/blob/develop/doc/API.md
- jest-axe Setup Guide: https://github.com/nickcolley/jest-axe
- @axe-core/playwright: https://www.npmjs.com/package/@axe-core/playwright
- pa11y-ci Configuration: https://github.com/pa11y/pa11y-ci
- Lighthouse CI: https://github.com/GoogleChrome/lighthouse-ci
- eslint-plugin-jsx-a11y: https://github.com/jsx-eslint/eslint-plugin-jsx-a11y
- WCAG 2.2 Quick Reference: https://www.w3.org/WAI/WCAG22/quickref/
- Deque Axe Monitor: https://www.deque.com/axe/monitor/
- Android Accessibility Testing (Espresso): https://developer.android.com/guide/topics/ui/accessibility/testing
- iOS Accessibility Testing (XCUITest): https://developer.apple.com/documentation/xctest/accessibility
