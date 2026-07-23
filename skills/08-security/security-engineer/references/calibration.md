# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You run vulnerability scanners and forward the raw report to engineering with subject line "Please fix these" | You can review a threat model and identify the 3 controls that matter — and you can argue both sides of a risk acceptance decision to the CISO and the VP of Engineering, and both agree | You design a detection that catches a real attacker in the first 5 minutes of a breach — and it actually works in production against a skilled adversary, not just in a tabletop exercise |
| You implement security controls because "the checklist says so" without understanding the threat they're mitigating | You can walk into any engineering team's design review and ask the 3 questions that make them redesign their architecture to be inherently more secure | A zero-day drops for a critical dependency you use, and your team has a patch deployed to production within 4 hours — and this wasn't a drill |
| Your "security architecture review" consists of running a SAST scanner and checking the OWASP Top 10 | You've designed a detection pipeline where every alert that fires has a >90% true positive rate, and your SOC team's mean time to triage is under 5 minutes | The CISO presents your security architecture to the board as evidence that security is a competitive advantage, not a cost center |

**The Litmus Test:** A developer pushes code that introduces an SSRF vulnerability in a new payment integration. Does your security pipeline catch it BEFORE it reaches production? If the answer involves "someone would notice during code review," you don't have a security engineering program — you have hope. Masters catch it at the pre-commit hook, the CI pipeline, and the WAF, and all three are verified to work.
