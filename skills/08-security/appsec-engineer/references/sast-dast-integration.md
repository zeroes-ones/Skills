# SAST and DAST Pipeline Integration

## Pipeline Architecture

```
Developer Machine (pre-commit)
  -> detect-secrets, git-secrets (block secrets before commit)
  -> Semgrep local (fast subset of rules, <30 seconds)
  -> npm audit / pip audit (dependency changes only, <10 seconds)

Pull Request (CI, <5 minutes required)
  -> Semgrep diff scan (changed lines only, block net-new HIGH/CRITICAL)
  -> truffleHog (full git history secret scan, block on any finding)
  -> Snyk/Dependabot (new dependency additions, block CRITICAL+KEV)
  -> Checkov/tfsec (IaC misconfigurations, block HIGH/CRITICAL)

Main Branch Nightly (CI, no time constraint)
  -> CodeQL full analysis (deep data flow, variant analysis)
  -> SCA full audit (all dependencies, reachability, license risk)
  -> Trivy/Grype (container images, OS + app dependencies)
  -> OWASP ZAP baseline (staging environment, authenticated)

Pre-Release (manual + automated)
  -> OWASP ZAP active scan (high-risk endpoints only)
  -> Burp Suite Enterprise (scheduled deep scan)
  -> Manual penetration test (if major release or new critical features)
```

## False Positive Triage Workflow

### Roles
- Triage Lead: Security engineer, rotates weekly, 25% time allocation
- Rule Owner: The engineer who tuned/configured each SAST rule

### Triage Process
1. New finding arrives in triage queue (Jira/GitHub Issues/ASOC platform)
2. Triage Lead reviews within 1 business day
3. Decision:
   - Accept: Create ticket, assign to team, set SLA based on severity
   - False Positive: Suppress with justification (screenshot, code context, why not exploitable)
   - Defer: Accept risk with owner + expiry date (reviewed quarterly)
4. Weekly dashboard: FP rate per rule, top 5 noisiest rules, trend over time
5. Rule hygiene: Disable rules >70% FP, tune rules 40-70% FP

### Metrics to Track
- Precision: True Positives / Total Findings (target: >60%)
- Time to Triage: Hours from finding creation to triaged (target: <24 hours)
- Backlog Size: Open findings by severity (target: flat or declining sprint-over-sprint)
- Developer Friction: "Security tool blocked my PR and it was a false positive" (survey, target: <10%)

## Ruleset Optimization Strategy

Phase 1 (deploy): Start with top 20 highest-signal rules. p/default in Semgrep is a good start.
Phase 2 (observe): Run for 2-4 weeks in report-only mode. Catalog FP rate per rule.
Phase 3 (tune): Suppress existing findings. Disable high-FP rules. Add custom rules for your codebase.
Phase 4 (block): Enable blocking for net-new HIGH/CRITICAL. Monitor developer feedback.
Phase 5 (expand): Add 5-10 rules per month based on true positive rate and developer acceptance.
Phase 6 (custom): Build custom Semgrep/CodeQL rules for your business logic vulnerability patterns.
