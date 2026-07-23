# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| Your security reviews find SQL injection and XSS but you've never found an authorization bypass, a business logic flaw, or a race condition | You find vulnerabilities at the seams between components — the interaction between the auth system and the rate limiter, between the ORM and the raw SQL escape, between the CSP and the third-party script loader | You've found a vulnerability that would have caused a data breach affecting >10,000 users — and the fix was deployed to production before anyone exploited it |
| You run `npm audit` and believe "zero CVEs = secure" — you don't know what a transitive dependency is | You trace every dependency to its origin: direct vs. transitive vs. vendored — and your scan pipeline covers all three categories | You've designed a vulnerability management program where mean time to patch Critical CVEs dropped from 30 days to 48 hours — with automated canary deployments and rollback verification |
| You check for secrets in code but not in Terraform state, CI logs, or Docker image layers | You've built a multi-layer secret detection pipeline: pre-commit hooks, CI scanning (gitleaks, truffleHog), and regular scans of all state files and build artifacts | An external penetration test finds zero Critical or High findings in a system you reviewed — and the pentest report says "the security posture exceeds industry standards" |

**The Litmus Test:** Given a codebase you've never seen, can you find a vulnerability that a SAST tool (Semgrep, CodeQL, Snyk Code) would miss — in under 30 minutes? If you've never compared your manual findings against what a SAST tool caught on the same codebase, you don't actually know how much value you add beyond automation.
