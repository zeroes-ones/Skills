# Technical Program Management — Q4 2026 Plan

## Top-Level Initiatives

| Initiative | Lead | Target | Success Metric |
|------------|------|--------|----------------|
| Plugin SDK v1.0 | Sarah Chen (Platform) | Oct 31, 2026 | 3 external plugins published, API stability commitment |
| Enterprise SSO | Marcus Wei (Auth) | Nov 15, 2026 | SAML/OIDC support, Okta + Azure AD integration tests passing |
| Multi-Region Deployment | Diego Rivera (Infra) | Dec 15, 2026 | eu-west-1 serving production traffic, cross-region latency < 200ms |

## Dependency Map

```
Plugin SDK v1.0
  ├── Blocks: Marketplace launch (external plugins require stable SDK)
  ├── Requires: Nothing (self-contained)
  └── Risk: Plugin adoption uncertainty — if no external developers build plugins by Nov 30, pivot to internal-only SDK

Enterprise SSO
  ├── Blocks: 4 enterprise deals (Acme Corp $95K, Globex $72K, Stark Industries $60K, Wayne Enterprises $85K)
  ├── Requires: Auth0 Organizations feature (GA July 2026 — available)
  └── Risk: Auth0 dependency for SAML federation — acceptable, migration cost estimated at 3 weeks if needed

Multi-Region Deployment
  ├── Blocks: EU expansion (3 prospects in Germany require EU data residency)
  ├── Requires: Plugin SDK v1.0 (plugins must be region-aware)
  └── Risk: Data replication complexity for Aurora Global Database — PostgreSQL limitations on conflict resolution
```

## Risk Register (7 Risks)

| Risk | Probability | Impact | Score | Mitigation |
|------|------------|--------|-------|------------|
| Plugin SDK adoption below target (3 external plugins) | Medium (40%) | High | HIGH | Run plugin hackathon in October ($5K prizes), personally onboard 5 target developers |
| Auth0 outage during enterprise SSO rollout | Low (10%) | High | MEDIUM | Auth0 SLA is 99.9% — acceptable. Maintain local auth fallback (email/password) for all customers |
| Multi-region data replication latency exceeds 200ms | Medium (35%) | High | HIGH | Use Aurora Global Database with 1-second replication SLA. Accept eventual consistency for non-critical data. Pre-production load test in September |
| Key engineer departure during Q4 | Low (15%) | High | MEDIUM | Bus factor ≥ 2 for all critical paths. Documentation up-to-date (ADR + runbooks). Retention bonuses in place |
| Enterprise customer demands on-premise deployment | Medium (30%) | Medium | MEDIUM | No on-premise roadmap. Offer AWS PrivateLink as a compromise. Escalate to CEO if deal > $100K |
| SOC 2 audit delays | Low (20%) | Medium | LOW | Audit scheduled November. Evidence collection automated via Vanta. Pre-audit readiness review in October |
| Scope creep from customer requests | High (60%) | Medium | HIGH | Strict "no new features during initiative" policy. Customer requests triaged to a "Post-Q4" Linear project. CEO approval required for exceptions |

## Executive Dashboard

Weekly OKR tracking in a Notion dashboard shared with the leadership team and board observers. Each initiative has: current status (on-track/at-risk/blocked), burndown chart (story points vs. time), blocker list (with owner and expected resolution date), and a confidence score (1–5, updated weekly by the initiative lead). Current overall confidence: 3.8/5 (Plugin SDK: 4, SSO: 5, Multi-Region: 3 due to replication complexity risk).

## Cadence

- **Weekly**: 30-minute initiative sync (leads only) — status update, blocker escalation, resource rebalancing
- **Bi-weekly**: 45-minute exec review — initiative leads present to CEO + CTO, decisions documented in Notion
- **Monthly**: 1-hour steering committee — CEO, CTO, VP Product, VP Engineering, external advisor (former VP Eng at HashiCorp). Strategic decisions: roadmap trade-offs, build-vs-buy, hiring priorities
