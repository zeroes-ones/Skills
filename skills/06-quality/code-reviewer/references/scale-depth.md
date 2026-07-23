# Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Code review = self-review checklist before merging. Review dimensions: correctness + security (just check for obvious issues). No PR process. No automated checks.
- **What to skip**: Multi-reviewer PR process. Automated CI checks (lint, type-check, tests). Security specialist review. Review SLAs. Severity grading.
- **Coordination**: Self-review. Ship fast, fix forward.

### Small Team (2-10 people, 100-10K users)
- **What changes**: PR required for all merges. One reviewer (peer). Automated checks: lint, type-check, tests. Review dimensions: all 6 but lighter on architecture/performance. Severity grading used. Review SLA: <24 hours. Security-sensitive changes get extra scrutiny.
- **What to skip**: Multiple reviewers per PR. Formal review board. Review metrics tracking. Security specialist for every PR.
- **Coordination**: PR assigned via GitHub. Async review within 24 hours. Quick sync for complex changes.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Two reviewers for critical paths (auth, payments, data). Full 6-dimension review enforced. Automated checks: lint + type-check + tests + security scan + coverage. Severity-based merge gates (Critical/High block merge). Review metrics tracked (turnaround time, review depth). Security reviewer for sensitive changes.
- **What to skip**: Formal review board (peer review is enough). Mandatory architecture review for every PR. Review metrics as performance evaluation.
- **Coordination**: CODEOWNERS for domain expertise. Weekly code review quality sync. Monthly review metrics review.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Multiple reviewer tiers (peer → domain expert → security → architecture for critical changes). Automated review bots (linter, type-checker, security scanner, dependency checker). Formal review checklist per change type. Review board for cross-cutting changes. Compliance review gates (SOC 2, HIPAA, PCI DSS). Review metrics as quality KPIs. Reviewer training program.
- **What's full production**: Automated pre-review (AI-assisted review). Change-risk-based review depth. Reviewer workload balancing. Review quality auditing. Cross-team review coordination.
- **Coordination**: Weekly review quality audit. Monthly review board for cross-cutting changes. Quarterly reviewer calibration.

### Transition Triggers
- **Solo → Small**: Second developer joins. Need shared understanding of code changes.
- **Small → Medium**: 5+ developers. Critical production incidents traced to merged code. >10K users.
- **Medium → Enterprise**: Compliance requirements. Multiple teams with shared code ownership. >50 developers.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | backend-developer | Feature implementation with tests |
| **This** | code-reviewer | Six-dimension review with severity-graded findings |
| **After** | qa-engineer | Test coverage for flagged risk areas |

Common chains:
- **Chain**: backend-developer → code-reviewer → qa-engineer — Code is reviewed for quality/security, then QA targets findings with additional tests
- **Chain**: frontend-developer → code-reviewer → release-manager — UI changes reviewed for accessibility and performance, then queued for release
