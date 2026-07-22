---
name: accessibility-testing
description: >-
  Automated accessibility testing in CI/CD pipelines — axe-core integration (unit tests, e2e, component tests), pa11y and Lighthouse CI for page-level audits, HTML CodeSniffer for continuous scanning, automated screen reader testing patterns, visual regression testing for accessibility (color contrast diffs, focus ring visibility), accessibility linting (eslint-plugin-jsx-a11y, stylelint-a11y, Android Lint accessibility checks, SwiftLint a11y rules), CI/CD quality gates with WCAG 2.2 AA compliance thresholds, accessibility monitoring and regression detection, test strategy across the testing pyramid (static → unit → integration → e2e), and accessibility score dashboards. Use when implementing automated a11y testing, setting up CI/CD accessibility gates, or building an accessibility monitoring system.
author: Sandeep Kumar Penchala
type: quality
status: stable
version: "1.0.0"
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
  type: "code"
  path_hint: "./"
chain:
  consumes_from:
    - accessibility-auditor
    - qa-engineer
    - ci-cd-builder
  feeds_into:
    - accessibility-auditor
    - frontend-developer
    - mobile-developer
    - qa-engineer
---
# Accessibility Testing

Build automated accessibility testing into every layer of the CI/CD pipeline — catch violations at lint time, component test time, e2e test time, and in production monitoring before users do.

## Route the Request
```
What do you need?
├── Add a11y testing to existing CI/CD → Jump to "Core Workflow > Phase 2"
├── Set up axe-core in unit/component tests → Go to "Core Workflow > Phase 1"
├── Add Lighthouse CI accessibility budgets → Jump to "Best Practices > CI Gates"
├── Automate screen reader testing → Go to "Decision Trees > Screen Reader Automation"
├── Catch a11y regressions on every PR → Jump to "Core Workflow > Phase 3"
├── Add a11y linting to IDE and pre-commit → Go to "Best Practices > Linting"
├── Build an accessibility monitoring dashboard → Jump to "Core Workflow > Phase 4"
└── Mobile accessibility testing → Go to "Decision Trees > Mobile A11y"
```

## Ground Rules

- **Accessibility bugs are production bugs with legal exposure.** A broken checkout flow costs revenue. A broken checkout flow that only affects screen reader users costs revenue AND exposes the company to ADA lawsuits. The severity classification must reflect this: accessibility P2 = functional P1.
- **Automated testing catches ~30-40% of accessibility issues.** The remaining 60-70% require manual testing (keyboard navigation, screen reader workflow, cognitive walkthrough). Automated testing is necessary but not sufficient. Never claim "100% a11y coverage" from automation alone.
- **Every passed accessibility check is a snapshot in time, not a guarantee.** A component that passes axe-core in isolation may fail when composed into a page with other components (focus order conflicts, heading hierarchy collisions, aria-owns cross-boundary issues). Always test at the integration level, not just the unit level.
- **Lighthouse accessibility score of 100 does NOT mean fully accessible.** Lighthouse tests ~30 automated checks. It cannot detect focus management bugs during SPA navigation, dynamic content announcements with aria-live, or keyboard trap scenarios. A 100 score is a green light for the easy stuff — manual testing covers the rest.
- **Accessibility monitoring must be continuous, not point-in-time.** The homepage passed WCAG 2.2 AA in last month's audit. Since then: the marketing team added a carousel (no pause button), the engineering team migrated to a new modal library (no focus trap), and the design team updated the color palette (new gray-on-white contrast ratio: 2.8:1, minimum: 4.5:1). Continuous monitoring catches these within 24 hours, not at the next annual audit.

## When to Use

- You need to integrate automated accessibility testing into existing CI/CD pipelines
- You are setting up axe-core, pa11y, or Lighthouse CI for the first time
- You want to add accessibility linting to the developer workflow (IDE + pre-commit)
- You need to configure accessibility quality gates that block PRs with violations
- You are building an accessibility monitoring system to catch regressions in production
- You need to automate screen reader testing for critical user flows
- You want to add accessibility visual regression testing to catch contrast and layout issues

## Decision Trees

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

1. **Test after every DOM mutation, not just on page load.** SPA navigation, modal opens, tab switches, and infinite scroll all change the DOM. axe-core must re-run after each of these events. A page that passes on load can fail after the user opens a menu.
2. **Never globally exclude rules.** If you must exclude a rule, do it per-component or per-page with a comment explaining why and a ticket tracking the fix. Global exclusions hide regressions.
3. **Accessibility snapshot testing is fragile but valuable.** Storing axe-core results as snapshots means any DOM change may update the snapshot — but it forces developers to consciously acknowledge accessibility changes. Use sparingly on stable components.
4. **Color contrast is the most common violation — automate it everywhere.** Axe-core catches most contrast issues, but gradient backgrounds, images with text, and CSS pseudo-elements may be missed. Supplement with visual regression testing focused on contrast ratios.
5. **Track the accessibility debt ratio.** `(open violations / total checks) × 100`. A ratio trending down means the team is fixing faster than creating. A ratio trending up means the opposite. Review monthly.
6. **Focus order testing requires real keyboard simulation.** `page.keyboard.press('Tab')` in Playwright is not the same as the browser's native Tab behavior. Use `page.locator('body').press('Tab')` and verify `document.activeElement` matches the expected next element.
7. **Prefer integration tests over unit tests for a11y.** A `<Button>` component may pass axe in isolation. But 5 `<Button>` components with conflicting aria-labels inside a `<nav>` may fail at the integration level. The most common a11y bugs are compositional, not isolated.
8. **Mobile accessibility is not "small desktop accessibility."** Touch target size (minimum 44x44 CSS pixels), screen reader swipe gestures, dynamic type/text resize support, and reduced motion preferences are unique to mobile. Test on real devices, not just responsive viewports.

## Error Decoder

| Error | Root Cause | Fix |
|-------|-----------|-----|
| CI gate blocks every PR with 47 new violations — team starts skipping a11y checks | Baseline never established. Every violation is a "new" violation because the baseline is zero. | Import existing violations as the baseline. Only changes (new or fixed) are flagged. Reduce baseline by 10% each quarter. |
| Lighthouse score dropped from 97 to 82 with no code changes | Third-party script (chat widget, analytics, cookie banner) injects inaccessible DOM. | Audit third-party scripts on page load. If chat widget adds unlabeled iframe, exclude it from audit with comment and file bug with vendor. Monitor for vendor fixes. |
| Axe passes in dev but fails in CI — flaky test on color contrast | CI runs in a different viewport or font rendering causes different text layout. | Run CI at a fixed viewport (1280x720). Disable font smoothing differences. Or use a single consistent Docker image for CI a11y tests. |
| Screen reader automation says "pass" but manual tester finds critical issue | Automation checked aria-label exists; didn't check that it makes sense. `aria-label="button"` passes automation but fails usability. | Add semantic validation rules: aria-label must be unique within context, must not repeat the role name, must describe the action not the element type. |
| "No violations found" on component test — component is completely inaccessible | Component is empty or rendering nothing in the test. Axe can't find violations on an empty DOM. | Assert that the component renders expected interactive elements before running axe. Minimum: verify at least one button/input/link exists in the rendered output. |

## Production Checklist

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

| Skill | When to Coordinate | What to Share |
|-------|-------------------|--------------|
| **accessibility-auditor** | WCAG criteria interpretation, manual audit findings to automate | Violation patterns, audit reports, WCAG rule mapping |
| **qa-engineer** | Integration with test pyramid, test strategy, regression suites | Test framework config, Playwright/Cypress integration, test baselines |
| **ci-cd-builder** | CI/CD quality gate configuration, blocking vs warning thresholds | Pipeline config, gate scripts, dashboard integration |
| **frontend-developer** | Component-level a11y testing, lint rule configuration, snapshots | ESLint config, jest-axe setup, component test patterns |
| **mobile-developer** | Mobile a11y testing (Espresso, XCUITest, RN accessibility props) | Platform-specific test setup, device testing matrix |
| **ui-ux-designer** | Color contrast checks, focus ring visibility, design token compliance | Figma contrast plugin results, design system token file |
| **legal-advisor** | ADA/Section 508/EN 301 549 compliance monitoring evidence | Automated compliance reports, monitoring dashboards |

## What Good Looks Like

**What good looks like:** A developer opens a PR that changes a button component from a `<div>` with an onClick handler to a native `<button>`. The CI pipeline runs. ESLint passes (the `<div>` would have been caught by `jsx-a11y/no-static-element-interactions`). Unit tests pass (jest-axe confirms the button has an accessible name). E2e tests pass (axe-core finds no new violations on any page containing the button). The accessibility dashboard in CI shows a green check and a baseline diff of "+0 new, -1 fixed" because the old `<div>` violation is now resolved. The developer didn't think about accessibility at all — the pipeline caught everything. That's what good looks like.

## Scale Depth
<!-- QUICK: 30s -- how this skill changes as the company grows -->

| Stage | Scope | Focus | Key Difference |
|-------|-------|-------|----------------|
| **Solo** | axe-core in dev, manual Lighthouse audits | Catch the obvious, learn WCAG | Run axe in browser DevTools; fix what you find before shipping |
| **Startup** | CI/CD a11y gates on every PR, linting in IDE | Automate enforcement, block regressions | Lint + axe in CI; violation baseline established; score tracked |
| **Scale-up** | Cross-platform testing (web + iOS + Android), monitoring | Cover all platforms, continuous compliance | Daily production scans; mobile a11y automation; debt ratio tracked |
| **Enterprise** | Dedicated a11y team, real-user monitoring, legal compliance | Proactive accessibility, ADA/508 defense | Accessibility program with dedicated headcount; VPATs published; user testing with assistive tech |

## References

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
