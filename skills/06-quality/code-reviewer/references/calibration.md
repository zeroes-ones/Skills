# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| Your review comments are 80% style and formatting — you notice indentation errors faster than race conditions | Your reviews follow a consistent priority order (Security → Correctness → Performance → Error Handling → Testing → Style) and you can name the most dangerous line in any PR under 400 lines | You can predict which PRs will cause a production incident within 6 months — and your prediction accuracy is >50% when tracked over a year |
| You rubber-stamp PRs from senior developers because "they know what they're doing" | You find meaningful issues in PRs from developers at ALL levels — your review quality doesn't depend on the author's seniority | Engineering managers cite your reviews in promotion packets because your feedback demonstrably improved the quality of 10+ engineers |
| You leave "can we do this better?" feedback without suggesting HOW | Every review comment includes: what's wrong, why it matters, and a concrete fix — the author never has to ask "what should I do instead?" | You've designed a review process adopted by 3+ teams that reduced cycle time by 30% while reducing escaped defects by 40% — and you have the DORA metrics to prove it |

**The Litmus Test:** Can you review a 500-line PR in under 15 minutes and identify the 3 most dangerous lines — the ones most likely to cause a security breach, data loss, or outage? If you need more than 20 minutes or you find more style issues than substance, you're practicing reading, not reviewing.
