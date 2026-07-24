# Downstream Sync

> Keeping repos aligned with their templates after initial creation.

## Sync Strategies

### Automated PR (10-100 repos)
* **Trigger:** Template update merged to main
* **Action:** Script clones each downstream repo, applies template diff, opens PR
* **SLAs:** Non-critical: 1 week. Security: 24 hours.
* **Auto-merge rules:** If PR only updates non-functional files (SECURITY.md, CODEOWNERS) and CI passes, auto-merge after 24 hours

### Drift Detection (100+ repos)
* **Trigger:** Scheduled (daily/weekly) CI check in each downstream repo
* **Action:** CI compares local configs against template baseline, alerts on drift
* **Dashboard:** Percentage of repos in sync, drift age, security-critical drift count

### Manual Sync (<10 repos)
* **Trigger:** Quarterly audit
* **Action:** Engineer manually compares each repo against template, creates PRs
* **Checklist:** CI config, linter rules, SECURITY.md, CODEOWNERS, .gitignore

## Security-Critical Sync Path

For template changes that affect security posture:
1. Security team approves the template change
2. Sync script opens PRs to ALL repos immediately
3. PRs auto-merge after 24 hours if no objection
4. Any repo that fails CI or rejects the PR is escalated to engineering leadership

## Sync Metrics

| Metric | Target | Measurement |
|--------|--------|------------|
| Sync completeness | >90% repos in sync | Drift dashboard |
| Sync latency (non-critical) | <7 days | Time from template merge to all PRs open |
| Sync latency (security) | <24 hours | Time from template merge to all PRs merged |
| Drift age | <30 days | Time since last sync per repo |
