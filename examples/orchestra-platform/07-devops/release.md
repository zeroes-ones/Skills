# Orchestra Platform — v1.0 Release Runbook

**Last updated:** 2026-07-21 | **Owner:** Platform Engineering

## Release Train Schedule

| Milestone | Window | Duration |
|---|---|---|
| Feature freeze | Monday 9:00 AM UTC | — |
| Staging deploy (`main` → staging) | Monday 11:00 AM UTC | ~30 min |
| Smoke tests (automated + manual) | Monday 1:00–3:00 PM UTC | 2 hours |
| Go/no-go meeting | Monday 4:00 PM UTC | 30 min |
| Production deploy | Tuesday 10:00 AM UTC | ~60 min |
| Monitoring watch | Tuesday–Thursday | 48 hours |

## Go/No-Go Criteria

All criteria **must** pass for go-decision:

- [ ] All end-to-end tests green on staging (Cypress suite, 247 tests)
- [ ] Zero open P0/P1 bugs against v1.0 milestone
- [ ] Security review signed off by AppSec (required; see SECURITY.md)
- [ ] Rollback procedure tested and verified in staging (target: <5 minutes)
- [ ] Error budget remaining > 50% (current: 72% of monthly budget)

## Deployment Strategy — Canary

```
T+0     → 10% of traffic (2-hour soak)
T+2h    → Metrics gate (p95 latency, error rate, saturation)
T+2h    → 50% of traffic (2-hour soak)
T+4h    → Metrics gate
T+4h    → 100% of traffic
```

**Automated rollback triggers:** p95 latency > 250ms for 5 consecutive minutes, or error rate > 1% for any rolling window.

## Feature Flags (LaunchDarkly)

| Flag | State at Launch | Notes |
|---|---|---|
| `plugin-marketplace` | **OFF** | V2; requires plugin-registry service |
| `ai-recommendations` | **OFF** | Internal-only beta for 2 weeks |
| `enterprise-sso` | **OFF** | SAML integration pending Okta certification |

## Communication Plan

- **D-1:** Release notes published on docs.orchestra.dev and changelog
- **During deploy:** Status page banner updated (status.orchestra.dev)
- **On completion:** #eng-announce Slack message posted
- **D+1:** Email to all workspace admins with upgrade summary

## Rollback Procedure

```bash
helm rollback orchestra-v1.0 orchestra-v0.9 --namespace production
argocd app sync orchestra-production
```

Pre-deploy, DNS cache TTL is temporarily lowered to 60 seconds. Staging rollback time:
**4 minutes 23 seconds** (verified July 20, 2026).

## Post-Release

- 48-hour monitoring watch with on-call escalation path
- Daily check-in standup for 3 consecutive days (Tues–Thurs 3:00 PM)
- Retrospective scheduled for **Friday 4:00 PM** — calendar invite sent
