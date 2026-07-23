# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You run axe-core and think "0 violations" means the site is accessible — you've never tested with a screen reader | You triage every axe violation: "This is a real issue (must fix)" vs. "This is a false positive (document why)" vs. "This needs manual review (schedule screen reader test)" | You've designed an accessibility testing strategy where automated tools catch >80% of WCAG violations before a human auditor touches the page — and you can prove it with audit data |
| You disable accessibility lint rules to ship faster and tell yourself "we'll fix it later" | Your baseline violation count trends DOWN every sprint — you close more violations than you accumulate | A VPAT you authored survived an ADA lawsuit because your automated CI audit trail produced timestamped evidence of every violation detection, fix, and verification |
| You think accessibility testing is "just running axe" — you've never done a keyboard-only walkthrough of your own product | You maintain per-route violation baselines, a separate manual test script for screen reader flows, and a keyboard navigation test suite — and all three run on every release | You've trained an entire engineering org on accessibility testing, and 12 months later, accessibility bugs reported by users dropped 70% |

**The Litmus Test:** Can you audit a production web application and correctly identify which WCAG SC violations CANNOT be detected by ANY automated tool (axe-core, Lighthouse, pa11y)? If you can't name at least 5 such categories (e.g., focus order meaningfulness, error suggestion clarity, link purpose in context), you're not L3 yet.
