# Scale Depth: Solo → Small → Medium → Enterprise

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


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | product-strategist | Market opportunity, business case, strategic context |
| **This** | idea-to-spec | Structured PRD, API contracts, screen inventory, work items |
| **After** | product-manager | Prioritized backlog, roadmap placement, stakeholder alignment |

Common chains:
- **New product**: product-strategist → idea-to-spec → product-manager — from business case to prioritized roadmap
- **Feature work**: ux-researcher → idea-to-spec → backend-developer — from user evidence to implementable API contracts

### Service Interaction Designs

**idea-to-spec → api-designer: API contract generation from PRD**
When the spec defines user stories that require cross-service communication, the spec MUST include an endpoint inventory with request/response schemas. The `api-designer` skill consumes the spec's screen inventory and entity model to produce OpenAPI contracts. Every acceptance criterion that mentions "when the user clicks X" maps to at least one API endpoint. Missing endpoints in the spec = broken frontend-backend contracts.

**idea-to-spec → database-designer: entity modeling from spec**
The spec's domain model (entities, relationships, cardinalities, access patterns) feeds directly into schema design. For every entity in the spec, the `database-designer` needs: read vs write ratio, query patterns, data volume projections, and consistency requirements. Specs that omit access patterns force database designers to guess — and guessing produces schemas that don't match query reality.

**idea-to-spec → frontend-developer: component API alignment**
The screen inventory in the spec maps 1:1 to frontend components. Every screen must specify its data dependencies (which API endpoints, which entities) and its states (loading, empty, error, edge). Frontend developers should never discover missing states mid-sprint — the spec is the contract.
