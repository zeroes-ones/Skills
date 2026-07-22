# Release Management Playbook

> **Author:** Sandeep Kumar Penchala

Production release management patterns covering release types, calendar planning, branch strategy, checklists, rollback procedures, release notes automation, and DORA metrics. These practices operationalize the release-manager skill's end-to-end release lifecycle.

## Release Types

| Type | Version Change | Trigger | Lead Time | Risk Level | Rollback Strategy |
|------|---------------|---------|-----------|------------|-------------------|
| Major | `2.0.0` | Breaking API changes, architecture overhaul | Weeks/months | High | Feature flag + gradual rollout |
| Minor | `1.3.0` | New features, non-breaking additions | Days/weeks | Medium | Canary → full rollback |
| Patch | `1.2.1` | Bug fixes, security updates | Hours/days | Low | Quick rollback or hotfix-forward |
| Hotfix | `1.2.1-hotfix1` | Production incident, critical bug | Minutes/hours | Emergency (bypass some gates) | Fastest possible rollback |

### Release Type Decision Flow

```
Change contains breaking API changes? → Major
Change adds new feature?               → Minor
Change fixes a bug?                    → Patch
Production is down?                    → Hotfix (emergency process)
```

## Release Calendar

```
Quarterly release train (example):
  Q3 2026:
    v2.3.0  → Week 1: Feature freeze
               Week 2: RC1 → integration testing
               Week 3: RC2 → final fixes
               Week 4: GA release

  Patch window: Every Tuesday/Thursday, 10am-2pm
  Hotfix: Any time (emergency process)

LTS Schedule:
  v1.x LTS → Supported until Q4 2026 (security patches only)
  v2.x LTS → Supported until Q4 2027
```

## Release Branch Strategy

| Strategy | Description | Branch Pattern | Best For |
|----------|-------------|---------------|----------|
| Git Flow | `main`, `develop`, `release/*`, `hotfix/*` | Feature → develop → release → main | Scheduled releases, versioned products |
| Trunk-Based | All commits to `main`; release from tags | `main` + release tags | Continuous delivery, SaaS |
| Release Branches | Branch per release; cherry-pick fixes | `release/v2.3` from `main` | Mobile apps, on-prem software |

### Decision Matrix

```
SaaS / web app, deploy multiple times daily?       → Trunk-based
Mobile app with app store review?                   → Release branches
Enterprise software with versioned releases?         → Git Flow
Need both rapid deploys AND scheduled releases?     → Trunk-based + release branches
```

### Trunk-Based with Release Branches (Hybrid)

```bash
# Daily deploys from main
git checkout main && git pull
git tag v2.3.0-rc1   # Pre-release tag
# CI deploys tag to staging

# For the official release
git checkout -b release/v2.3.0 v2.3.0-rc1
# Cherry-pick any last-minute fixes
git tag v2.3.0
git push origin v2.3.0
# CI builds and promotes to production
```

## Release Checklist

```markdown
## Release v2.3.0 Checklist

### Code Freeze (T-3 days)
- [ ] All feature PRs merged to target branch
- [ ] No more feature additions — bug fixes only
- [ ] Dependency audit completed (`npm audit`, `trivy scan`)
- [ ] All tests passing on target branch (unit, integration, e2e)
- [ ] Performance benchmark run — no regression > 5%

### Pre-Deploy (T-1 day)
- [ ] Release notes drafted (auto-generated + manual review)
- [ ] Database migrations reviewed — backward-compatible?
- [ ] Rollback plan documented and tested
- [ ] Monitoring dashboards verified — all metrics reporting
- [ ] On-call schedule confirmed for release window
- [ ] Stakeholders notified (Slack/email: release time, impact, rollback contact)
- [ ] Feature flags configured (if gradual rollout)

### Deploy (T-0)
- [ ] Canary deploy to 5% traffic — monitor for 10 min
- [ ] Error rate < baseline; latency P95 < baseline + 20%
- [ ] Canary success → deploy to 100%
- [ ] Smoke tests pass (critical user journeys)
- [ ] Database migrations completed successfully

### Post-Deploy (T+1 hour)
- [ ] Monitor for 1 hour post-deploy (error rate, latency, saturation)
- [ ] Customer-facing features verified in production
- [ ] Release tag pushed to repository
- [ ] Release notes published (GitHub Releases + changelog)
- [ ] Post-deploy retrospective scheduled (if issues occurred)

### Post-Deploy (T+1 day)
- [ ] 24-hour metrics review — any delayed issues?
- [ ] Cache warmed; no cold-start performance problems
- [ ] Clean up feature flags for fully-rolled-out features
```

## Rollback Procedures

### Automated Rollback Triggers

```yaml
# ArgoCD automated rollback
apiVersion: argoproj.io/v1alpha1
kind: Rollout
spec:
  strategy:
    canary:
      steps:
        - setWeight: 5
        - pause: { duration: 10m }
        - setWeight: 20
        - pause: { duration: 20m }
        - setWeight: 100
      analysis:
        templates:
          - templateName: error-rate-check
        args:
          - name: service-name
            value: order-service
      # Auto-rollback if analysis fails
```

### Manual Rollback Steps

```bash
# 1. Assess severity — is rollback necessary?
kubectl logs -l app=order-service --tail=100 --since=5m | grep ERROR

# 2. Notify stakeholders
# Template: "Rolling back order-service v2.3.0 → v2.2.1 due to elevated 5xx errors.
#  ETA: 3 minutes. Impact: orders-api unavailable during rollback."

# 3. Execute rollback (ArgoCD)
argocd app rollback order-service --to v2.2.1

# Or kubectl
kubectl rollout undo deployment/order-service -n prod

# 4. Verify rollback
kubectl rollout status deployment/order-service -n prod
curl -s https://orders-api.example.com/health | jq .

# 5. Communicate completion
# Template: "Rollback complete. order-service is now on v2.2.1. Error rate back to baseline.
#  Incident #INC-4242 open for root cause analysis."

# 6. Database rollback (if migration was part of release)
# Apply down migration: migrate down 1
```

### Communication Templates

```markdown
# Release Start Notification
:rocket: **Deploying v2.3.0 to production**
- Start: 2026-07-21 14:00 UTC
- ETA: 30 min
- Changes: 3 features, 12 bug fixes ([changelog](link))
- Rollback contact: @release-captain
- Monitor: [dashboard link]

# Rollback Notification
:warning: **ROLLING BACK v2.3.0 → v2.2.1**
- Reason: 5xx error rate at 8% (baseline: 0.1%)
- Impact: orders-api
- ETA: 3 min
- Incident: [INC-4242](link)

# Release Complete Notification
:white_check_mark: **v2.3.0 deployed successfully**
- Duration: 22 min
- Metrics nominal: error rate 0.09%, P95 187ms
- [Release notes](link)
```

## Release Notes Automation

### Conventional Commits → Changelog

```bash
# commit messages follow conventional commits:
# feat(orders): add bulk discount calculation
# fix(payments): resolve duplicate charge on retry
# BREAKING CHANGE: orders API now requires authentication header

# Generate changelog automatically
npx standard-version
npx semantic-release
```

### GitHub Release Integration

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags: ['v*']
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true    # Auto-generates from PRs
          body: |
            ## What's Changed
            ${{ steps.changelog.outputs.changes }}
            ## Docker Images
            `myapp:${{ github.ref_name }}`
            ## Migration Guide
            See [UPGRADING.md](UPGRADING.md)
```

## Release Metrics (DORA)

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| Deployment Frequency | On-demand (multiple/day) | Once/day - once/week | Once/week - once/month | Once/month - once/6 months |
| Lead Time for Changes | < 1 hour | 1 day - 1 week | 1 week - 1 month | 1-6 months |
| Mean Time to Restore (MTTR) | < 1 hour | < 1 day | < 1 week | < 1 month |
| Change Failure Rate | 0-5% | 5-10% | 10-15% | 15-30% |

### Tracking Dashboard

```sql
-- DORA metrics from deployment events
SELECT
  DATE_TRUNC('week', deployed_at) AS week,
  COUNT(*) AS deployments,
  AVG(EXTRACT(EPOCH FROM deployed_at - committed_at) / 3600) AS avg_lead_time_hours,
  AVG(EXTRACT(EPOCH FROM restored_at - failed_at) / 60) AS avg_mttr_minutes,
  COUNT(*) FILTER (WHERE failed) * 100.0 / COUNT(*) AS change_failure_rate_pct
FROM deployments
WHERE deployed_at > NOW() - INTERVAL '90 days'
GROUP BY 1 ORDER BY 1;
```

### Release Burndown

Track remaining work vs release date. If scope exceeds capacity, cut features — never slip the date.

```
Release Burndown (ideal line: 100% → 0% over 10 days):
Day 1:  ████████████░░░░░░░░░  100% (28 issues)
Day 3:  ██████████░░░░░░░░░░░  85%  (24 issues)
Day 5:  ████████░░░░░░░░░░░░░  60%  (17 issues) — BEHIND! Cut 3 low-priority items
Day 8:  ████░░░░░░░░░░░░░░░░░  30%  (8 issues)
Day 10: ░░░░░░░░░░░░░░░░░░░░░  0%   (RELEASE)
```

This release playbook implements the release-manager skill's full lifecycle — from release type selection through DORA metrics — ensuring every release is planned, executed, and measured with production-grade rigor.
