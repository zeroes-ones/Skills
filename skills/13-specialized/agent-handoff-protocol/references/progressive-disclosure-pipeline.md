# Progressive Disclosure Pipeline — Tier 1/2/3 Loading Strategy

## Problem

Loading the entire context from all prior agents into every downstream agent
is expensive (tokens), slow (latency), and error-prone (noise). Progressive
disclosure solves this by loading context in tiers.

## Tier Definitions

### Tier 1: Critical (Always Loaded — ~2,000 tokens)

What every agent MUST see regardless of role:

```json
{
  "pipeline_id": "uuid",
  "current_stage": 3,
  "total_stages": 5,
  "active_topology": "supervisor",
  "immutable_constraints": ["GDPR compliance", "PostgreSQL 15+"],
  "escalation_path": "system-architect",
  "rollback_point": "stage-2"
}
```

**Contents:** Pipeline identity, non-negotiable constraints, escalation path, rollback point.

### Tier 2: Relevant (Loaded on Demand — ~5,000 tokens)

What the agent loads based on its role in the pipeline:

- **Backend developer:** API contracts, data models, tech constraints, ADRs
- **DevOps engineer:** Runtime deps, env vars, resource requirements, health checks
- **Security engineer:** Auth flows, data classification, dependency SBOM, network surface
- **QA engineer:** Test strategy, coverage targets, acceptance criteria, test data specs

**Loading trigger:** Agent requests `load_tier(2, filters=[...])` after Tier 1 review.

### Tier 3: Noise (Never Auto-Loaded — ~15,000+ tokens)

What exists in the full context but is irrelevant to current stage:

- Rejected architectural alternatives from 3 stages ago
- Business strategy details no longer actionable
- Internal agent reasoning transcripts
- Debug logs from prior agents
- Draft artifacts that were superseded

**Access:** Explicit request only: `load_tier(3, artifact_id="...")`

## Loading Protocol

```
Agent starts
    │
    ▼
┌─────────────┐
│ Load Tier 1 │  ← Automatic, mandatory, fast
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Tier 1 sufficient?│── Yes ──→ Proceed with work
└──────┬───────────┘
       │ No
       ▼
┌──────────────────────────┐
│ Request Tier 2 (filtered)│  ← Role-based filter
└──────┬───────────────────┘
       │
       ▼
┌──────────────────┐
│ Tier 2 sufficient?│── Yes ──→ Proceed with work
└──────┬───────────┘
       │ No
       ▼
┌──────────────────────────┐
│ Request specific Tier 3  │  ← Explicit artifact ID
│ artifact                 │
└──────────────────────────┘
```

## Tier Assignments Per Skill

| Skill | Tier 1 | Tier 2 Includes | Tier 3 (never auto) |
|-------|--------|-----------------|---------------------|
| system-architect | Pipeline ID, constraints | ADRs, NFRs, integration map | Business strategy, CEO notes |
| backend-developer | Constraints, ADRs | API specs, data models | Architecture debates, cost models |
| devops-engineer | Constraints, ADRs | Runtime deps, env schema | Source code, unit tests |
| security-engineer | Constraints, ADRs | Auth flows, SBOM, network surface | UI code, caching config |
