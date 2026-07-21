# Technical Program Manager Practices

> **Author:** Sandeep Kumar Penchala

A practitioner's guide to technical program management — bridging engineering execution with business outcomes. Companion to the [Technical Program Manager SKILL.md](../SKILL.md).

---

## 1. TPM vs PM vs Engineering Manager

```
                    ┌──────────────────────────────┐
                    │        TPM                    │
                    │  ┌──────────┐  ┌───────────┐ │
                    │  │  Project  │  │ Technical  │ │
                    │  │  Manager  │  │  Depth     │ │
                    │  └──────────┘  └───────────┘ │
                    │                              │
                    │  Cross-team orchestration    │
                    │  Multi-quarter programs      │
                    │  Technical risk management   │
                    └──────────────────────────────┘
       ┌──────────────────────┐    ┌────────────────────────┐
       │   Project Manager    │    │  Engineering Manager    │
       │  • Single team scope │    │  • People management    │
       │  • Sprint execution  │    │  • Career growth        │
       │  • Task tracking     │    │  • Performance reviews  │
       │  • Stakeholder comms │    │  • Hiring + retention   │
       │  • Risk register     │    │  • Technical strategy   │
       └──────────────────────┘    └────────────────────────┘
```

### When to Hire Each

| Role | Signals You Need One |
|---|---|
| **PM** | Teams struggling with sprint predictability; stakeholders unclear on status |
| **TPM** | 3+ teams on coordinated delivery; technical risks span systems; quarterly+ programs |
| **EM** | Team has 5+ ICs; career development needed; hiring pipeline needed |

---

## 2. Program Charter Template

```markdown
# Program Charter: [Program Name]
**TPM:** [Name] | **Date:** [Date] | **Version:** 1.0

## Vision
[Why this program exists; the future state it creates]

## Scope
### In Scope
- [System A refactor]
- [New API version launch]
- [Cross-team dependency: Team X → Team Y data pipeline]

### Explicitly Out of Scope
- [Related system that will be addressed in follow-up program]

## Stakeholders & Governance
| Role | Name | Decision Rights |
|---|---|---|
| Executive Sponsor | [Name] | Budget, strategic direction |
| Technical Sponsor | [Name] | Architecture decisions |
| Program Owner (TPM) | [Name] | Day-to-day execution, risk escalation |

## Key Milestones
| Milestone | Date | Exit Criteria |
|---|---|---|
| M0: Architecture alignment | [Date] | ADRs approved by all teams |
| M1: Integration test pass | [Date] | All cross-team APIs working |
| M2: Staged rollout 10% | [Date] | Error rate < 0.1%, P99 latency < baseline + 10% |
| M3: GA launch | [Date] | 100% traffic; monitoring stable for 7 days |

## Success Metrics
| Metric | Baseline | Target | Measurement |
|---|---|---|---|
| P99 latency | 250ms | < 200ms | Datadog |
| Error rate | 1.2% | < 0.5% | Sentry |
| Developer adoption | — | 80% within 30 days | Internal analytics |

## Risks
| Risk | Severity | Mitigation | Owner |
|---|---|---|---|
| [Risk] | High/Med/Low | [Plan] | [Name] |
```

---

## 3. Cross-Team Dependency Management

### Dependency Map
```
Team A (API Platform)
  ├─► Team B (Mobile) — depends on: /v2/users endpoint by M1
  ├─► Team C (Web)    — depends on: /v2/analytics endpoint by M2
  └─► Team D (Data)   — depends on: event schema finalized by M0
```

### Dependency Tracking Board

| ID | Depends On | Dependent Team | Deliverable | Needed By | Status | Risk |
|---|---|---|---|---|---|---|
| D01 | Team A: /v2/users | Team B: Mobile | API endpoint + docs | Sprint 3 | On track | 🟢 |
| D02 | Team A: /v2/analytics | Team C: Web | API endpoint + docs | Sprint 4 | At risk | 🟡 |
| D03 | Team A: Event schema | Team D: Data | Schema spec | Sprint 1 | Blocked | 🔴 |

### Escalation Triggers
- Dependency status is **Red** for > 3 days
- Dependency delivery date slips by > 1 sprint
- Blocking dependency has no assigned owner
- Two teams give conflicting commitments for same dependency

### Dependency SLA
- Critical dependency: 24-hour response to blocking questions
- Non-critical dependency: 3 business days
- Escalation path: TPM → Technical Sponsor → Executive Sponsor

---

## 4. Technical Design Review Process

### RFC Template
```markdown
# RFC: [Title]
**Author:** [Name] | **Date:** [Date] | **Status:** Draft / Review / Approved / Rejected

## Problem Statement
[What problem are we solving? Why now?]

## Proposed Solution
[High-level architecture; include diagrams]

## Alternatives Considered
| Alternative | Pros | Cons | Why Rejected |
|---|---|---|---|
| [Alt 1] | [Pros] | [Cons] | [Reason] |

## Detailed Design
[API contracts, data models, sequence diagrams, migration plan]

## Risks & Mitigations
| Risk | Severity | Mitigation |
|---|---|---|
| [Risk] | H/M/L | [Plan] |

## Rollout Plan
1. [Feature flag: 1% → 10% → 50% → 100%]
2. [Monitoring: dashboard link, alert thresholds]
3. [Rollback: how to revert within 5 minutes]

## Open Questions
- [ ] [Question] — Owner: [Name]
```

### Review Stages
1. **Author draft** → Share with immediate team (async, 2–3 days)
2. **Technical review** → Architecture review board; focus on feasibility
3. **Cross-team review** → Dependent teams verify API contracts
4. **Security review** → Security team sign-off (required for auth, PII, payments)
5. **Decision** → Sponsor approves/rejects; publish ADR in repo

### Decision Log
| ID | Date | Decision | Rationale | Alternatives Rejected | Decided By |
|---|---|---|---|---|---|
| ADR-001 | 2024-03-15 | Use PostgreSQL for audit log | ACID compliance; existing team expertise | MongoDB (no transactions), DynamoDB (cost) | Tech Sponsor |

---

## 5. Program Status Reporting

### Weekly Snapshot Template
```markdown
# [Program Name] — Week of [Date]
**RAG Status:** 🟢 Green | **TPM:** [Name]

## Executive Summary
[2–3 sentences on overall health and key development]

## Milestones
| Milestone | Target Date | Forecast | RAG | Notes |
|---|---|---|---|---|
| M0: Architecture | Mar 1 | Mar 1 | 🟢 | Complete |
| M1: Integration | Mar 15 | Mar 18 | 🟡 | 3-day delay due to dependency D02 |
| M2: Staged rollout | Apr 1 | Apr 1 | 🟢 | On track |
| M3: GA | Apr 15 | Apr 15 | 🟢 | On track |

## Top Risks
1. [Risk 1] — RAG: 🟡 — Owner: [Name] — Next action: [Action]
2. [Risk 2] — RAG: 🟢 — Mitigation in progress

## Key Decisions Needed This Week
- [ ] [Decision 1] — Decision maker: [Name]
- [ ] [Decision 2] — Decision maker: [Name]

## Blockers
- [Blocker 1] — Owner: [Name] — Escalated to: [Name]
```

### Stakeholder-Specific Views
| Stakeholder | Focus | Format |
|---|---|---|
| **Executive Sponsor** | RAG, budget, timeline, top risks | 1-pager, monthly |
| **Engineering Leads** | Technical risks, dependencies, decisions needed | Detailed, weekly |
| **Product Owner** | Feature readiness, UX feedback, customer impact | Mid-level, bi-weekly |
| **Extended Team** | Wins, upcoming changes, how it affects them | Newsletter, monthly |

---

## 6. Risk Management for Technical Programs

### Technical Risk Register

| ID | Risk | Category | Detection | Pre-Mitigation Score | Mitigation | Post-Mitigation Score | Owner |
|---|---|---|---|---|---|---|---|
| TR01 | P99 latency > 500ms at scale | Performance | Load test at 10× traffic | H (16) | Query optimization; caching layer; connection pooling | M (8) | Infra Lead |
| TR02 | Data migration corrupts records | Data Integrity | Canary migration validates checksums | H (20) | Shadow write; verify before cutover; rollback script tested | L (4) | DBA |
| TR03 | Auth service outage blocks all traffic | Availability | Circuit breaker pattern; degraded mode | C (25) | Multi-region failover; cached auth tokens with 1hr TTL | M (6) | SRE |
| TR04 | Third-party SDK breaks on update | Integration | Pin versions; integration tests in CI | M (9) | Automated dependency update PRs with test gates | L (3) | Dev Lead |

### Risk Review Cadence
- **Weekly:** Top 5 risks reviewed in program sync
- **Monthly:** Full risk register reviewed with technical sponsor
- **Per milestone:** Risk register scrubbed; stale risks closed; new risks added

---

## 7. Large-Scale Planning

### Annual Roadmap Framework
```
Q1: FOUNDATION                    Q2: EXECUTION
├─ Architecture decisions         ├─ Build MVP
├─ Prototypes & spikes            ├─ Internal dogfooding
├─ Vendor selection               ├─ Integration testing
└─ Hiring key roles               └─ Beta program launch

Q3: SCALE                         Q4: OPTIMIZE
├─ Staged rollout (1% → 100%)     ├─ Performance tuning
├─ Monitoring & alerting          ├─ Cost optimization
├─ Documentation & training       ├─ Retrospective
└─ GA launch                      └─ Next-year planning
```

### Quarterly Planning Cycle
```
Week 1–2:   Review OKRs; gather proposals from teams
Week 3:     T-shirt sizing; capacity planning
Week 4:     Prioritization (RICE: Reach × Impact × Confidence / Effort)
Week 5:     Draft quarterly plan
Week 6:     Cross-team dependency negotiation
Week 7:     Executive review and sign-off
Week 8:     Kickoff; publish plan
```

### Sprint-to-Sprint Execution
- **Week 1:** Sprint planning + unblock dependencies
- **Week 2:** Execution; mid-sprint check-in
- **End of sprint:** Demo + retro; update program dashboard

---

## 8. System Design Review Framework

### Architecture Review Board (ARB) Checklist
- [ ] Does the design align with company architecture principles?
- [ ] Are there known anti-patterns (distributed monolith, tight coupling)?
- [ ] Are API contracts defined and versioned?
- [ ] Is the data model documented? Migration plan included?
- [ ] Are failure modes identified and handled (circuit breakers, retries, timeouts)?
- [ ] Are observability hooks designed in (metrics, logs, traces)?
- [ ] Is the cost model estimated (compute, storage, bandwidth)?
- [ ] Is the security review complete (auth, encryption, PII handling)?

### Specialized Reviews
| Review Type | When Required | Reviewer |
|---|---|---|
| **Scalability** | System handles > 1K QPS or > 100K users | Infra/SRE |
| **Security** | Auth, payments, PII, admin functions | Security team |
| **Cost** | Estimated monthly burn > $10K | FinOps |
| **Compliance** | HIPAA, PCI, SOC 2 scope | Compliance officer |

---

## 9. Program Retrospective

### Agenda (90 minutes)
```
0–10 min:   Set the stage — review program charter, goals, metrics
10–35 min:  What went well — silent writing → group share
35–60 min:  What didn't go well — silent writing → group share
60–75 min:  Root cause analysis — 5 Whys for top 3 issues
75–85 min:  Action items — SMART, assigned, timeboxed
85–90 min:  Close — appreciate contributors; commit to actions
```

### Root Cause Categories
- **Process:** Missing gates, unclear ownership, insufficient review
- **Technical:** Architecture limitations, tooling gaps, tech debt
- **People:** Skill gaps, communication breakdown, turnover
- **External:** Vendor issues, regulatory changes, market shifts

### Action Item Template
```yaml
actions:
  - id: AI-01
    finding: "Three teams independently built duplicate auth middleware"
    root_cause: "No discoverable internal package registry or shared library culture"
    action: "Create internal npm/PyPI registry; publish auth middleware as shared package"
    owner: platform-team-lead
    deadline: 2024-05-01
    success_criteria: "All new services use shared auth package; 50% existing services migrated"
```

---

*Effective TPMs are force multipliers — they remove obstacles so engineering teams can do their best work. The frameworks here provide structure; your judgment provides direction.*
