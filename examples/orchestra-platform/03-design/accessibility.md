# Accessibility Audit — WCAG 2.2 AA

**Audit Date**: July 15, 2026  
**Auditor**: Orchestra Accessibility Team + external consultant (Deque Systems)  
**Overall Pass Rate**: 94% (281 of 299 success criteria passed)

## Findings Summary

| # | Category | Severity | Description | Status |
|---|----------|----------|-------------|--------|
| 1 | Focus Management | P0 | Modal dialogs do not trap focus — tab cycles to browser chrome | Open |
| 2 | Focus Management | P0 | Wizard step transitions do not move focus to step heading | Open |
| 3 | Focus Management | P1 | Catalog filter changes do not announce result count to screen readers | Fixed |
| 4 | Focus Management | P1 | Skip-to-content link missing on catalog and admin pages | Fixed |
| 5 | Color Contrast | P1 | Table row hover state (4.2:1) falls below 4.5:1 minimum on zebra stripes | Fixed |
| 6 | Color Contrast | P1 | Placeholder text in dark mode inputs (3.8:1) | Open |
| 7 | Color Contrast | P1 | Success toast background + white text (4.1:1) | Fixed |
| 8 | ARIA Labels | P1 | Plugin config toggle switches missing `aria-label` | Fixed |
| 9 | ARIA Labels | P2 | Template execution progress bar missing `aria-valuenow` | Open |
| 10 | Keyboard Nav | P1 | Catalog card expand/collapse not operable via Enter/Space | Fixed |
| 11 | Keyboard Nav | P1 | Template wizard "Add Environment Variable" button unreachable via Tab | Fixed |
| 12 | Keyboard Nav | P2 | Data table row checkboxes missing keyboard selection (Shift+click range) | Backlog |

## Remediation Priority

- **P0 (Sprint current)**: Focus management in modals and wizards — blocks keyboard-only and screen reader users from completing core workflows. Estimated effort: 3 story points each.
- **P1 (Next sprint)**: Color contrast violations and missing ARIA labels — affects users with low vision and screen reader users. Estimated effort: 8 story points total across 7 items.
- **P2 (Backlog)**: ARIA improvements and keyboard enhancements — quality-of-life improvements. Estimated effort: 5 story points.

## Screen Reader Testing

| Screen Reader | Browser | OS | Pass Rate | Notes |
|---------------|---------|-----|-----------|-------|
| VoiceOver | Safari 17 | macOS 14 | 96% | Modal focus trap failure is the primary issue |
| NVDA 2024.1 | Chrome 126 | Windows 11 | 93% | ARIA live region announcements inconsistent on template execution page |
| TalkBack 14.2 | Chrome 126 | Android 14 | 94% | Swipe gestures on wizard stepper need custom handling |

All interactive components receive automated axe-core audits in CI (GitHub Actions, runs on every PR). Manual screen reader testing performed at the start of each sprint and before every release. The accessibility statement is published at `orchestra.dev/accessibility` and includes a contact email for user-reported issues.
