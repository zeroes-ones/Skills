---
name: idea-to-spec
description: Transform raw product ideas into structured PRDs, data models, API contracts, screen definitions, and work items. Use when converting napkin sketches, feature requests, or brainstorming notes into actionable engineering specs. Triggers: "spec this out", "write a PRD from this idea", "formalize this feature", "idea to spec".
author: Sandeep Kumar Penchala
---

# Idea to Spec

Systematically decompose a raw product idea into a complete, implementation-ready specification package — PRD, domain model, API surface, screen inventory, and prioritized work items — so that an engineering team can estimate and build without ambiguity.

## When to Use
- A stakeholder has a one-paragraph idea and needs a formal spec before sprint planning
- A feature request lacks technical detail (data shapes, API endpoints, error states)
- You need to evaluate feasibility and surface unknowns before committing to a roadmap
- A greenfield product needs its first structured artifact beyond a pitch deck
- An existing system needs a net-new module and someone must bootstrap the design doc

## Decision Trees

### Spec Depth Decision

```
Feature complexity?
├── Simple CRUD (1 screen, 1 entity) → Lightweight spec (Scope Brief + API contract)
│     Time: 2-4 hours. No formal PRD. User stories in issue tracker.
├── Moderate feature (3-5 screens, multi-entity) → Full spec (PRD + API + Screen Inventory)
│     Time: 1-3 days. Include state machines for key entities. Async RFC review.
└── Platform-level (cross-team, 10+ screens) → Heavy spec (PRD + Domain Model + API + Screen + Architecture)
      Time: 1-2 weeks. Architecture review board sign-off required.

Greenfield product? → Start with Scope Brief. Spec only the first slice.
Adding to existing system? → Focus on API contract and screen inventory. Domain model reference only.
```

### Specification Tooling

```
Solo/Small team? → Notion/Google Docs with OpenAPI snippets. Keep it simple.
Medium team? → Notion + dedicated OpenAPI tool (Stoplight/SwaggerHub). RFC in doc comments.
Enterprise? → Spec management platform (Notion/Confluence + Jira integration). Automated validation.
```

## Core Workflow

### Phase 1: Discovery & Scoping
Extract the core problem, target persona, and success criteria from the raw input. Use the Five Whys to drill past solution proposals to root needs. Document explicit non-goals — what the feature deliberately excludes. Identify assumptions and unknowns that need validation before writing code. Output a one-page **Scope Brief** that captures: Problem Statement, Target Users, Success Metrics (leading and lagging), Scope Boundaries (in/out), and Open Questions with owners.

### Phase 2: Domain Modeling
Identify entities, their attributes, relationships, and cardinalities. Favor composition over deep inheritance. Define state machines for entities with lifecycle transitions. Annotate each entity with: required vs. optional fields, validation rules, uniqueness constraints, and indexing strategy. Produce an **Entity Relationship Diagram** (textual or visual) and a **Data Dictionary** with one row per field. For each relationship, specify ownership direction and cascade behavior.

### Phase 3: API Design
For every operation identified in the scope brief, define: HTTP method, URL path, request body schema (JSON/Protobuf), query parameters, response body schema, and error codes for every failure mode. Group endpoints by resource. Define pagination, sorting, and filtering conventions uniformly. Specify authentication and authorization per endpoint. Document idempotency guarantees. Output an **OpenAPI 3.1 spec** snippet or equivalent **API Contract** document.

### Phase 4: Screen & Interaction Inventory
List every screen, modal, drawer, or stateful view the feature requires. For each screen: name the route, list data dependencies (which API calls fire on mount), define loading, empty, error, and edge-case states, and enumerate all user actions with their system responses. Produce a **Screen Inventory** table and wireframe descriptions. Include accessibility requirements per screen (heading hierarchy, focus management, ARIA landmarks).

### Phase 5: Work Item Breakdown
Slice the spec into vertically deliverable user stories. Each story must be independently shippable and demonstrable. Write stories in the `As a [role], I want [action], so that [value]` format with concrete acceptance criteria. Sequence stories by dependency and value-to-effort ratio. Tag each story with a t-shirt size estimate for early capacity planning. Output a **Story Map** ordered by priority.

## Cross-Skill Coordination

Converting an idea into a spec is inherently collaborative — it synthesizes product intent, design thinking, and engineering reality. A spec written in isolation produces three things: rework, frustration, and missed deadlines.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Product Manager / Product Strategist** | Feature kickoff, scope trade-offs, priority conflicts | PRD, success metrics, user segments, MVP scope, stakeholder constraints |
| **UX Researcher** | User flow ambiguity, persona questions, edge case discovery | Research findings, user behavior data, usability test results, accessibility requirements |
| **System Architect** | New service, cross-service feature, data model changes | Architecture constraints, service boundaries, API contracts, data flow direction |
| **API Designer** | New endpoints, endpoint changes, API contract design | Request/response schemas, error codes, idempotency requirements, pagination needs |
| **Frontend Developer** | Screen design, component requirements, state management | Screen states (loading/empty/error/edge), interaction patterns, accessibility specs |
| **Backend Developer** | Data model, business logic, integration points | Domain rules, validation rules, error handling strategy, performance requirements |
| **QA Engineer** | Acceptance criteria refinement, test planning | Test scenarios, edge cases, expected vs actual behavior, regression risk areas |
| **Security Reviewer** | Auth flows, data handling, payment features, PII exposure | Data classification, threat surfaces, auth requirements, compliance constraints |
| **Database Designer** | New entities, schema changes, query patterns | Access patterns, data volume projections, consistency requirements |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Scope change after spec approved | Product Manager, Engineering Lead, QA | Sprint replanning, capacity reallocation, timeline impact |
| API contract change during spec | API Designer, Frontend Dev, Backend Dev, QA | Contract versioning, mock updates, test case changes |
| New dependency discovered (external service, data pipeline) | System Architect, Backend Dev, Product Manager | Integration complexity, timeline risk, architectural review |
| Ambiguity in acceptance criteria flagged by QA | Product Manager, Engineering Lead | Clarification needed before implementation proceeds |
| Cross-team dependency identified late | Product Manager, System Architect, impacted teams | Dependency sequencing, parallelization opportunities, blocker resolution |
| Performance requirement exceeds known system capacity | System Architect, Backend Dev, Performance Engineer | Architecture review, caching strategy, load testing plan |

### Escalation Path

```
Spec blocked (unresolved ambiguity, missing stakeholder, scope conflict)
  └── Product Manager + Engineering Lead. Resolution within 24 hours or escalation to CTO.

Architecture conflict (spec requires pattern that violates architecture principles)
  └── System Architect + CTO Advisor. Decision documented as ADR. Spec updated or exception granted.

Cross-team dependency deadlock (two teams block each other)
  └── Product Manager + Engineering Leads of both teams. CTO breaks ties if unresolved in 48 hours.
```

## Best Practices
- Always define the empty state and error state before the happy path — they reveal the most design complexity.
- Prefer denormalized read models for query-heavy screens; normalize only writes.
- Every API response must include a `requestId` field for production debugging.
- Write acceptance criteria as executable assertions: "Given X, when Y, then Z."
- Use the "Mom Test" on every story: would a real user pay or change behavior for this?
- Version the spec artifact — date-stamp every iteration so teams can trace decisions.
- Socialize the spec asynchronously (RFC-style) before any synchronous review meeting.
- Capture every decision with context: what alternatives were considered and why they were rejected.

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Spec = a few bullet points in a Notion doc. No formal PRD. User stories = you writing code yourself. "Acceptance criteria" = it works in production.
- **What to skip**: Full PRDs. RICE scoring. Formal story mapping. API contracts (you own both sides). Non-functional requirements docs.
- **Coordination**: You talk to yourself. Ship daily.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Lightweight spec template (problem, solution, success metrics, non-goals). User stories with GIVEN/WHEN/THEN. Simple story mapping for complex features. API contract documented collaboratively. Scope brief before major features.
- **What to skip**: Full RICE/CD3 (value vs effort matrix is enough). Formal RFC process. Spec versioning beyond date stamps. Entity state machines for simple CRUD.
- **Coordination**: Async spec review (comment in doc). Weekly refinement session (45 min). Quick sync with designer before UI work.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Full PRD template. RICE or CD3 scoring. Story maps for all features. API contracts as source of truth (OpenAPI). Entity state machines for complex domains. Spec versioned with changelog. RFC-style async review. Edge case catalog per feature area.
- **What to skip**: Formal spec review board (peer review is enough). Six Sigma requirements traceability. Full UML for everything (use for complex flows only).
- **Coordination**: RFC async review (3-day window). Bi-weekly spec review with engineering. Pre-refinement with tech lead before team refinement. Cross-team dependency mapping session monthly.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Formal spec lifecycle (proposal → review → approval → implementation → validation). Architecture review board sign-off for cross-cutting specs. Requirements traceability matrix. Compliance review for regulated features. Accessibility requirements embedded. Internationalization specs. Product ops manages spec template evolution.
- **What's full production**: Spec management platform (Notion/Confluence + Jira integration). Automated acceptance criteria validation. Cross-team impact analysis. Regulatory review workflow.
- **Coordination**: Weekly spec review board. Architecture review async + monthly sync. Cross-team spec alignment quarterly. Compliance review before implementation start.

### Transition Triggers
- **Solo → Small**: You can't hold the full spec in your head anymore. Another dev builds the wrong thing from your spec.
- **Small → Medium**: 3+ teams need coordinated specs. First enterprise customer demands traceability.
- **Medium → Enterprise**: Regulatory compliance requires spec sign-off. Multi-product spec dependencies. IPO audit trail needed.

## Sub-Skills

| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `prd-writing` | Feature definition, stakeholder alignment | Phase 2 — scope brief, success metrics, non-goals |
| `domain-modeling` | Entity design, data relationships, state machines | Phase 2 — ERD, data dictionary, cardinalities |
| `api-contract-design` | Endpoint definition, error schemas, pagination | Phase 3 — OpenAPI 3.1 spec, idempotency |
| `screen-inventory` | Screen enumeration, state mapping, interaction design | Phase 4 — loading/empty/error/edge states |
| `story-mapping` | Work breakdown, sequencing, dependency ordering | Phase 5 — user stories, acceptance criteria |
| `rfc-process` | Cross-team spec review, async approval | `product-manager` — stakeholder alignment |
| `accessibility-requirements` | WCAG integration into screen specs | `accessibility-auditor` — heading hierarchy, focus management |

## Production Checklist
- [ ] Scope brief approved by product owner and tech lead
- [ ] Non-goals explicitly documented and agreed upon
- [ ] Entity state machines cover all lifecycle transitions including rollback paths
- [ ] API contract includes error schemas for every 4xx and 5xx response
- [ ] Pagination, sorting, and filtering patterns are consistent with existing APIs
- [ ] Every screen has defined loading, empty, error, and permission-denied states
- [ ] Story map ordered by dependency and value-to-effort ratio
- [ ] Each user story has at least 3 acceptance criteria in Given/When/Then format
- [ ] Open questions have assigned owners and due dates
- [ ] Spec versioned and distributed for async review before any planning meeting

## References
- **product-manager** — for stakeholder alignment and RICE prioritization after spec generation
- **ui-ux-designer** — for design system integration of screen inventory
- **accessibility-auditor** — for WCAG compliance of screen definitions
- _Shape Up_ by Ryan Singer — for shaping bets before speccing
- _Domain-Driven Design_ by Eric Evans — for entity and aggregate design patterns
- OpenAPI 3.1 Specification — for API contract format reference
