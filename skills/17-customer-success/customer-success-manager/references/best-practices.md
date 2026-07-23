# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Measure TTFV by segment and optimize the bottleneck step.** If enterprise TTFV is 45 days but 20 of those are "waiting for IT security review," move that step to pre-contract (provide security package during procurement, not after).
- **Calibrate health scores against actual churn quarterly.** If your model predicts 15% of accounts as "at risk" but only 5% churn, your thresholds are too aggressive. Adjust weights until predicted risk distribution matches actual churn distribution within 10%.
- **Health scores are lagging without relationship signals.** A customer can have perfect product usage and still churn because of M&A, budget cuts, or leadership change. Always include relationship health signals.
- **QBR slides must be 70% complete before the meeting.** Send the deck 48 hours in advance. The meeting is for discussion and alignment, not reading slides together.
- **Distinguish between "fixable churn" and "unavoidable churn."** Fixable: poor adoption, missing features, support issues. Unavoidable: company acquired, went bankrupt, changed business model. Track separately — they require different responses.
- **Every churned customer gets a structured exit interview within 30 days.** Template: (1) What problem were you solving? (2) When did you realize it wasn't working? (3) What did you switch to? (4) What would have changed your decision? Feed answers to product-manager within 1 week.
- **Onboarding is not complete until the customer achieves measurable value, not until your checklist is done.** Redefine "onboarded" as: "customer's stated success criterion met AND confirmed by customer in writing."
- **Digital-touch does not mean zero-touch.** Even automated CS programs need a human escalation path. Define triggers that auto-create a task for a pooled CSM: health score drops below 50, NPS below 0, support ticket >5 in a week.
- **NRR calculation must exclude new logo acquisition.** NRR = (starting ARR + expansion - contraction - churn) / starting ARR. If you include new logos in NRR, you're measuring sales performance, not CS performance.
- **Run a quarterly churn post-mortem with product-manager.** Review every churned account >$10K ACV. Classify churn reason. Identify patterns. Assign 1-3 product improvements per quarter based on findings.
