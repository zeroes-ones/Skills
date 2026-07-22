---
author: Sandeep Kumar Penchala
type: reference
domain: product-development
version: "1.0"
last_updated: 2026-07-21
parent_skill: idea-to-spec
---

# Specification Templates

> **Author:** Sandeep Kumar Penchala

Ready-to-use templates for PRDs, technical specs, feature briefs, user story maps, and spec-to-ticket decomposition. Each template is copy-paste ready with field descriptions. Use alongside the Idea-to-Spec skill's ideation and scoping workflows.

---

## 1. PRD Template (Product Requirements Document)

```markdown
# PRD: [Feature/Product Name]

| Field | Value |
|-------|-------|
| **Status** | Draft / In Review / Approved / In Development |
| **Author** | [Name] |
| **Stakeholders** | [Eng lead, Design lead, PM, GTM] |
| **Target release** | [Date or version] |
| **Last updated** | [YYYY-MM-DD] |

## Problem Statement
[1–2 paragraphs. What user problem does this solve? Why now?
Include data: "X% of users drop off at step Y," "N support tickets/week about Z."
Quote real user feedback if available.]

## User Personas
| Persona | Need | Priority (P0–P3) |
|---------|------|-------------------|
| [Persona 1] | [What they need to accomplish] | P0 |
| [Persona 2] | [What they need to accomplish] | P1 |

## Success Metrics
| Metric | Current | Target | Measurement method |
|--------|---------|--------|--------------------|
| [North Star input metric] | X% | Y% | [Analytics event name] |
| [Adoption metric] | X | Y | [Dashboard/query] |
| [Quality metric] | X | Y | [Monitoring/alert] |

## Scope
### In Scope (MVP)
- [Feature/requirement 1] — [Why it's essential]
- [Feature/requirement 2]
- [Feature/requirement 3]

### Out of Scope (Explicit non-goals)
- [Thing we are NOT building] — [Why not, and when it might be added]

### Future Iterations (v1.1+)
- [Feature] — depends on [prerequisite/dependency]

## User Flow
```
[Entry point] → [Step 1] → [Step 2] → [Decision point]
                                        ├── [Path A] → [Outcome A]
                                        └── [Path B] → [Outcome B]
```

## Edge Cases & Error States
- [ ] What happens when the user has no data?
- [ ] What happens on first use (zero state)?
- [ ] What happens if the API fails?
- [ ] What happens at scale (10K, 100K, 1M records)?
- [ ] What happens on mobile / small screens?
- [ ] What about accessibility (screen reader, keyboard nav)?
- [ ] What about international users (RTL, translations)?

## Dependencies
| Dependency | Owner | Status | Blocking? |
|------------|-------|--------|-----------|
| [API / service / design] | [Team/person] | Ready / In progress / Not started | Yes / No |

## Timeline
| Milestone | Date | Owner |
|-----------|------|-------|
| Design complete | [Date] | [Designer] |
| Technical spec approved | [Date] | [Eng lead] |
| Development start | [Date] | [Team] |
| Internal dogfood | [Date] | [Team] |
| Beta release | [Date] | [PM] |
| GA release | [Date] | [PM] |

## Open Questions
- [ ] [Question 1] — Owner: [Name], due: [Date]
- [ ] [Question 2] — Owner: [Name], due: [Date]
```

---

## 2. Technical Spec Template

```markdown
# Tech Spec: [Feature/System Name]

| Field | Value |
|-------|-------|
| **Status** | Draft / Reviewed / Approved |
| **Author** | [Engineer name] |
| **Reviewers** | [Names] |
| **Links** | [PRD], [Design file], [Tracking issue] |

## Summary
[3–5 sentences: what are we building, why this approach, what are the key technical decisions?]

## Architecture Overview
```
┌──────────┐    ┌──────────┐    ┌──────────┐
│ Client   │───▶│ API      │───▶│ Service  │
│ (React)  │    │ Gateway  │    │ (Worker) │
└──────────┘    └──────────┘    └─────┬────┘
                                      │
                                ┌─────▼────┐
                                │ Database │
                                │ (Postgres)│
                                └──────────┘
```

## API Contract
### POST /api/v1/feature
```
Request:
{
  "field_a": "string (required, max 255 chars)",
  "field_b": "integer (optional, default 0)",
  "field_c": "enum[option1, option2] (required)"
}

Response 201:
{
  "id": "uuid",
  "created_at": "ISO8601",
  "status": "active"
}

Error 422:
{
  "error": "validation_error",
  "details": [{ "field": "field_a", "message": "required" }]
}
```

## Data Model
```sql
CREATE TABLE feature_entity (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES users(id),
    status      TEXT NOT NULL DEFAULT 'active',
    field_a     TEXT NOT NULL,
    field_b     INTEGER DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_feature_user_status ON feature_entity(user_id, status);
```

## Migration Plan
1. **Schema migration:** Add tables/columns — fully backward compatible
2. **Code deploy:** New code behind feature flag `feature_name_v1`
3. **Data backfill:** [Script/process to populate new fields for existing records]
4. **Rollout:** Gradual % ramp: 1% → 10% → 50% → 100%
5. **Cleanup:** Remove feature flag + old code path after 2 weeks at 100%

## Rollback Plan
- [ ] Can we roll back the deploy? [Yes / No — explain constraints]
- [ ] Can we roll back schema changes? [Yes / No — migration is reversible?]
- [ ] What happens to data created in the new format if we roll back?

## Security Considerations
- [ ] Authentication required? [Yes — which roles?]
- [ ] Authorization checks? [Owner only / Admin / Team-based]
- [ ] Rate limiting? [Endpoint / tier]
- [ ] Input validation and sanitization?
- [ ] Audit logging for sensitive operations?

## Monitoring & Alerts
| Metric | Alert threshold | Dashboard |
|--------|----------------|-----------|
| API latency p95 | > 500ms | [Link] |
| Error rate | > 1% | [Link] |
| Feature adoption | Monitor only | [Link] |

## Testing Strategy
- [ ] Unit tests: [What's covered]
- [ ] Integration tests: [API contract, database queries]
- [ ] E2E tests: [Critical user flow]
- [ ] Load tests: [Expected throughput — requests/sec]
```

---

## 3. Feature Brief Template (Lightweight)

For small features or experiments that don't need a full PRD.

```markdown
# Feature Brief: [Name]

**Problem:** [One sentence — what user pain are we solving?]
**Hypothesis:** We believe [doing X] will result in [metric Y moving Z%].
**Success metric:** [One metric with target]
**Scope:**
  - Must have: [2–3 items]
  - Nice to have: [1–2 items]
  - Won't have: [1–2 items]
**User flow:** [3–5 bullet steps or one sketch link]
**Edge cases:** [2–3 most critical]
**Dependencies:** [API, design, other teams]
**Timeline:** [Start] → [Ship/Experiment]: ~[N] days
**Decision:** Go / No-go / Needs discussion
```

---

## 4. User Story Mapping Template

```
┌─────────────────────────────────────────────────────────────┐
│ BACKBONE (Core narrative left-to-right)                     │
├──────────┬──────────┬──────────┬──────────┬────────────────┤
│ Onboard  │ Create   │ Invite   │ Manage   │ Review &      │
│ & sign   │ first    │ team     │ projects │ report        │
│ up       │ project  │ members  │          │               │
├──────────┴──────────┴──────────┴──────────┴────────────────┤
│                                                             │
│ WALKING SKELETON (Minimum viable — all backbone steps)       │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐│
│ │Email    │ │Title+   │ │Invite   │ │Task     │ │Export   ││
│ │signup   │ │descrip- │ │by email │ │create/  │ │CSV      ││
│ │         │ │tion     │ │         │ │complete │ │         ││
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘│
│                                                             │
│ SLICE 1 (Next release)                                       │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐│
│ │Google   │ │Templa-  │ │Invite   │ │Due      │ │PDF      ││
│ │SSO      │ │tes      │ │by link  │ │dates    │ │report   ││
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘│
│                                                             │
│ SLICE 2                                                        │
│ ┌─────────────────────────────┐ ┌─────────────────────────┐│
│ │SAML SSO, Team defaults,     │ │ Subtasks, dependencies, ││
│ │bulk invite via CSV          │ │ rich dashboards         ││
│ └─────────────────────────────┘ └─────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### How to use
1. **Define the backbone:** 5–7 user tasks in chronological order — this is the narrative
2. **Walking skeleton:** Minimum card per backbone step that delivers end-to-end value
3. **Slice 1:** Next most valuable cards. Each slice should be independently releasable.
4. **Continue slicing** until all ideas are placed

---

## 5. Spec Review Checklist

Before a spec is approved, verify:

- [ ] **Problem clarity:** Does the spec state the problem before the solution?
- [ ] **User value:** Is it clear who benefits and how?
- [ ] **Success metrics:** Are they measurable, with baseline and target?
- [ ] **Non-goals:** Are they explicit? Is scope contained?
- [ ] **Edge cases:** Error states, empty states, loading states, permissions — addressed?
- [ ] **Dependencies identified:** Are all upstream/downstream teams aware?
- [ ] **API contract defined:** Endpoints, request/response shapes, error codes?
- [ ] **Data model:** New tables/columns, migration path, backward compatibility?
- [ ] **Security review:** AuthN, AuthZ, rate limiting, input validation?
- [ ] **Accessibility:** Keyboard nav, screen reader, color contrast considered?
- [ ] **Internationalization:** RTL support, locale-aware formatting?
- [ ] **Feature flag plan:** Ramp percentage, kill switch?
- [ ] **Monitoring & alerts:** What dashboards, what thresholds?
- [ ] **Rollback plan:** Can we undo this safely?
- [ ] **Stakeholder sign-off:** Eng, Design, PM, Security, and any dependent teams?

---

## 6. Spec-to-Ticket Breakdown

How to decompose a PRD + Tech Spec into sprint-ready tickets:

### Ticket template
```markdown
## [Component] — [Action]

**Spec reference:** [Link to PRD section]

**Acceptance criteria:**
- [ ] [Given/When/Then or checklist format]
- [ ] Includes unit tests
- [ ] Includes integration test (if API change)
- [ ] Feature-flagged behind [FLAG_NAME]

**Design:** [Figma link] (if UI)
**Technical notes:** [Link to tech spec section, API contract]
**Estimate:** [Story points or hours]
**Depends on:** [Ticket ID or "None"]
```

### Decomposition pattern by layer
1. **Database ticket** — schema migration + backfill script (if needed)
2. **API ticket** — endpoint, validation, authorization, tests
3. **Worker/async ticket** — background job, queue consumer (if applicable)
4. **Frontend ticket(s)** — one per major UI area (page, modal, component group)
5. **Integration ticket** — wire frontend to API, error handling, loading states
6. **Analytics ticket** — instrument events, create dashboard
7. **Documentation ticket** — update help center, changelog, API docs

### Sizing heuristic
- 1-day ticket = ~2 AC items
- 3-day ticket = ~5 AC items
- 5+ day ticket → break it down further; it's a mini-epic

---

See also: Idea-to-Spec skill for ideation frameworks, user research synthesis, and prototyping guidance.
