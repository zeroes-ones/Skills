# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You run an automated scan, see "0 violations," and tell your team "we're accessible" | You've personally completed a full WCAG 2.2 AA manual audit — keyboard, screen reader, zoom, and contrast — on a production application with 50+ screens and produced a prioritized remediation backlog with severity ratings and SC references | A blind user completes a complex task (purchase, application, data entry) on a product you audited — with zero external assistance, in under twice the time of a sighted user — and your audit report is cited as evidence in the company's published VPAT |
| You add `role="button"` to a `<div>` with an `onclick` handler and consider it "accessible now" | You can identify 15+ distinct accessibility violations in 5 minutes of keyboard-only navigation on any random SaaS product, naming each by WCAG SC number | You train 20 engineers over 6 months and their PRs ship with 80% fewer accessibility regressions — and you can trace the improvement to specific practices, lint rules, and testing habits you taught them |
| You've never navigated a website with your monitor turned off | You file accessibility bugs that include: WCAG SC reference, affected user population, exact AT reproduction steps, severity rating (critical/major/minor), and a screen recording | A federal agency or Fortune 500 company accepts your accessibility conformance report without requesting additional evidence — your testing methodology is trusted at the regulatory level without supplementary validation |

**The Litmus Test:** Can you complete an online purchase using only a screen reader (monitor off) on a site you've never visited, in under 5 minutes? If you can't, you don't yet understand the user experience you're auditing.
