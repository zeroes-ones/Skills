# Inner Source Model for Polyrepo Ecosystems

Governance framework for enabling cross-team contributions across independent repositories. Inner source applies open source collaboration principles within an organization.

## Foundation Requirements

Every repo accepting inner source contributions must have:

- **CODEOWNERS:** At least 2 maintainers from the owning team. Auto-assigned for all PR reviews.
- **CONTRIBUTING.md:** Dev environment setup, how to run tests, PR process, code style guide.
- **Issue Templates:** Feature request vs. bug report. Triage SLA (e.g., response within 48h).
- **CI on Forked PRs:** CI must run safely on external PRs. Secrets must not be exposed.

## Contribution Workflow

1. Contributor forks repo, creates feature branch, submits PR.
2. CI runs automatically (lint, test, build). Security: no secrets to forked PRs.
3. CODEOWNERS auto-assigned as reviewers.
4. Review SLA: <48h for initial review, <1 week to merge or reject.
5. Rejection must include specific, actionable feedback — not "we do not want this."

## Governance

- Maintainer team has final decision authority on merges.
- Trusted contributors (3+ accepted PRs) get direct push to feature branches.
- Quarterly health report: cross-team PR count, review time, contributor retention.
- Recognition: top cross-team contributors highlighted in company all-hands.

## When Inner Source Does NOT Work

- Repo has <1 release per quarter (too dormant).
- Repo is safety-critical with strict change control (medical, aviation, compliance).
- Owning team lacks bandwidth for <48h reviews (frustrates contributors).

## Anti-Patterns

- Announcing "contribute anywhere!" without maintainer capacity -> backlog of unreviewed PRs.
- No CODEOWNERS -> PRs rot with no assigned reviewer.
- Rejecting without feedback -> contributors never return.
