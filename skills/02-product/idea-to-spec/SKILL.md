---
name: idea-to-spec
description: >
  Use when transforming raw product ideas into structured engineering specifications,
  converting napkin sketches into actionable work items, or formalizing feature
  requests into PRDs. Handles PRD generation, data model design, API contract
  definition, screen inventory, domain modeling, and prioritized work item creation.
  Do NOT use for architecture decisions, code implementation, or UI/UX design
  execution.
license: MIT
tags:
- product
- prd
- specification
- requirements
- domain-model
- api-contract
author: Sandeep Kumar Penchala
type: product
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 2190
chain:
  consumes_from:
  - product-manager
  - system-architect
  - ui-ux-designer
  - ux-researcher
  feeds_into:
  - api-designer
  - backend-developer
  - database-designer
  - frontend-developer
  - qa-engineer
  - tdd-guide
---
# Idea to Spec
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Systematically decompose a raw product idea into a complete, implementation-ready specification package — PRD, domain model, API surface, screen inventory, and prioritized work items — so that an engineering team can estimate and build without ambiguity.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.md", "PRD\|spec\|scope.brief\|product.requirement")` AND `file_contains("*.md", "user.story\|acceptance.criteria\|GIVEN.*WHEN.*THEN")` | This is your skill. Jump to **Core Workflow** — Phase 2 (Specification Writing). |
| A2 | `file_exists("openapi.yaml\|openapi.json")` OR `file_contains("*.md", "endpoint\|REST\|GraphQL\|gRPC\|API.contract")` | Jump to **Core Workflow** — Phase 3 (API Design & Contract Generation). |
| A3 | `file_contains("*.md", "screen\|UI\|component\|interaction\|wireframe\|mockup")` AND `file_contains("*.md", "state\|loading\|empty\|error\|edge")` | Jump to **Core Workflow** — Phase 4 (Screen Inventory & Interaction Definitions). |
| A4 | `file_contains("*.md", "data.model\|entity\|schema\|relationship\|ERD")` AND `file_contains("*.md", "access.pattern\|query\|index")` | Invoke **database-designer** instead. This requires schema design expertise. |
| A5 | `file_contains("*.md", "prioritize\|RICE\|backlog\|feature.ranking")` | Invoke **product-manager** instead. This is backlog prioritization work. |
| A6 | `file_contains("*.md", "persona\|user.research\|journey.map\|usability.test")` | Invoke **ux-researcher** instead. This is user research territory. |
| A7 | `file_contains("*.md", "design.system\|component.spec\|design.token\|UI.component")` | Invoke **ui-ux-designer** instead. This is design system work. |
| A8 | `file_contains("*.md", "architecture\|microservice\|monolith\|C4\|system.design")` | Invoke **system-architect** instead. This is architecture design territory. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── New product ideation (greenfield, napkin sketch) → Start at "Core Workflow > Phase 1"
├── Feature specification or PRD writing → Jump to "Core Workflow > Phase 2"
├── API design and contract generation → Go to "Core Workflow > Phase 3"
├── Screen inventory and interaction definitions → Jump to "Core Workflow > Phase 4"
├── User story mapping and work breakdown → Go to "Core Workflow > Phase 5"
├── Stakeholder asks for a formal spec before sprint planning → Jump to "Decision Trees > Spec Depth Decision"
├── Need feature prioritization or backlog grooming? → `product-manager`
├── Need user research or persona validation? → `ux-researcher`
├── Need system architecture design or service boundaries? → `system-architect`
├── Need UI components or design handoff? → `ui-ux-designer`
└── Don't know where to start? → Start at Phase 1 (Discovery & Scoping)
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

### Routing Scenarios: Multi-Signal Decision Criteria

When a request mixes signals — e.g., "write a spec for a dashboard that shows real-time analytics and suggest the architecture" — use these decision criteria to route to the right specialist instead of trying to handle everything yourself.

| # | Scenario | Signals Present | Decision Criteria | Route To |
|---|----------|----------------|-------------------|----------|
| S1 | **Spec + Architecture in one request** | PRD/scope language mixed with "microservices", "deployment", "service boundaries", or "scale to N users" | Architecture always gates spec for platform-level features. If the request involves >2 services OR a new service boundary, route architecture first, then come back for spec. | `system-architect` first; return here with architecture constraints for spec writing |
| S2 | **Spec + UI/UX design in one request** | Screen definitions mixed with "design system", "component library", "brand colors", "typography scale" | If the request contains visual design decisions (colors, spacing, typography), the spec should define interaction states and the designer should define visual treatment. Split the work: spec owns behavior, designer owns presentation. | `ui-ux-designer` for visual design; this skill for interaction spec and screen inventory |
| S3 | **Spec + User research in one request** | Feature definition mixed with "persona", "user interview", "pain point validation", "usability test" | If the problem statement references user evidence the requestor can't produce ("users are frustrated because..."), validate before speccing. A spec built on assumed user needs is a solution searching for a problem. | `ux-researcher` for validation sprint (2-5 days); return here with validated problem statement and persona evidence |
| S4 | **Backlog item that needs estimation, not a spec** | "How big is this?", "Can we ship this in Q3?", "T-shirt size this" with no spec detail needed | Estimation without a spec is guessing. But a full PRD for a simple backlog item is overkill. Route to lightweight scope brief only — problem statement + API contract + 3 acceptance criteria. Do not enter full specification workflow. | This skill at L1 (Initiative) depth — output a Scope Brief only, not a full PRD |
| S5 | **Spec for an API-only feature (no UI)** | Endpoint definitions, data shapes, authentication, rate limiting — no screens mentioned | No screen inventory needed. Skip Phase 4 entirely. Focus on: domain model, API contract (OpenAPI 3.1), error codes, idempotency, pagination. The API contract IS the spec deliverable. | This skill — Phase 2 + Phase 3 only; coordinate with `api-designer` for contract validation |
| S6 | **Stakeholder wants a spec but can't articulate the problem** | "We need a spec for X" but when asked "what problem does X solve?" the answer is vague or circular ("X solves the problem of not having X") | This is the most dangerous spec request. The stakeholder has already decided on the solution and wants you to backfill justification. Refuse to enter specification workflow. Redirect to problem discovery. | `product-manager` for problem framing and validation; return here only when a validated problem statement exists |
| S7 | **Spec for a feature that already exists in a different form** | "Build a notification system" but the product already has email notifications via a marketing tool, in-app toasts via the frontend framework, and push via a third-party SDK | Before speccing a net-new system, audit what already exists. Duplicate infrastructure costs compound: two notification systems = two sets of bugs, two monitoring dashboards, two onboarding paths for new engineers. | This skill — but Phase 1 must include an existing-system audit before any new design. If audit reveals 80% coverage, recommend extending existing system instead |
| S8 | **Spec for a compliance-mandated change (GDPR, SOC2, PCI)** | "We need to add data retention policies" or "Users must be able to delete their data" with legal/regulatory driver | Regulatory specs have immutable constraints — you can't negotiate with a law. Route to `compliance-officer` or `gdpr-privacy` to establish the legal requirements before entering specification workflow. What you spec must satisfy the regulation; there is no MVP for compliance. | `compliance-officer` or `gdpr-privacy` first for regulatory requirements document; return here to spec the technical implementation of those requirements |
| S9 | **Urgent spec needed for exec demo in 48 hours** | "The CEO is demoing this to the board on Friday — we need a spec and working prototype" | Demo-driven specs invert the normal workflow. You're not speccing for engineering — you're speccing for theater. Produce: (1) happy-path-only spec (flag as demo-only, not production), (2) hardcoded mock data paths, (3) explicit "what's fake" appendix listing every shortcut taken. The risk is that demo code becomes production code via "we'll clean it up later" (which never happens). | This skill — but output a Demo Spec (happy path only) AND a Production Spec appendix listing every gap. Both documents must exist; the Production Spec is the contract for what happens after the demo. |

### Quick-Route Decision Flow

```
Incoming request — what's the dominant signal?
├── "Build a spec for..." (spec-first language, no architecture/design/research signals)
│   └── → This skill. Start at Phase 1 (Discovery & Scoping).
├── "How would you architect..." or "Design a system that..." (architecture-first language)
│   └── → `system-architect`. Return here after architecture decisions are documented.
├── "Design the UI for..." or "What should this look like?" (design-first language)
│   └── → `ui-ux-designer`. Return here for interaction spec if needed.
├── "Our users need..." or "Users are complaining about..." (research-first language, unvalidated)
│   └── → `ux-researcher`. Validate. Return here with evidence.
├── "Prioritize these features..." or "What should we build first?" (prioritization language)
│   └── → `product-manager`. Return here to spec the top-priority items.
└── "I have a napkin sketch / one-paragraph idea / pitch deck slide" (raw ideation)
    └── → This skill. Start at Phase 1 (Discovery & Scoping). Full greenfield workflow.
└── Uncertain / mixed signals (can't decide which path fits)
    └── → This skill at L1 depth. Produce a Scope Brief only — problem statement, target users, success metrics, in/out scope. The Scope Brief IS the routing document: once written, it will make obvious whether this needs architecture, research, design, or can proceed to full spec.
```

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---:|
| "The problem is obvious — let's just spec the solution and move" | Specs that start with solutions are solutions in search of problems. Without a validated problem statement (who has it, evidence it matters), you're spending engineering weeks building something nobody asked for — and you won't know until launch. |
| "We'll handle error states later — get the happy path shipped first" | The happy path is 20% of the spec. Loading, empty, error, and edge cases are the other 80%. "We'll handle errors later" translates to "we'll handle errors in production, at 3 AM, while customers are reporting them." Production is the most expensive place to discover error states. |
| ""Use Redis for caching" — the architect said so, put it in the spec" | The spec defines WHAT (caching with configurable TTL), not HOW (Redis vs Memcached). Implementation details in specs lock engineering out of the best decision at implementation time. When Redis bills spike, you'll wish engineering had freedom to choose. |
| ""User can reset password" — that's clear enough, the team will figure it out" | "Can" is the most expensive word in software specs. GIVEN/WHEN/THEN format is not pedantic ceremony — it's the difference between 2 hours of implementation and 2 days of back-and-forth during QA. Every ambiguous story costs $500+ in rework. |
| "We don't need Out of Scope — we're all aligned on what we're building" | "We're all aligned" lasts exactly until a stakeholder asks for "one more small thing" during sprint 4. Out of Scope is a pre-agreed contract. Without it, alignment is just the temporary absence of disagreement — not the permanent presence of agreement. |

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to write a spec without a validated problem statement.** Every spec must begin with: (1) the problem, (2) who has it, (3) evidence it's worth solving. Specs that start with solutions are solutions in search of problems. | Trigger: spec content begins with a solution description ("Add a button that...", "Build a feature that...") without a preceding "Problem:", "User Need:", or "Why:" section within the first 200 characters | STOP. Respond: "Before I write the spec, I need the problem: (1) What problem are you solving? (2) Who has this problem and how do you know? (3) What user evidence supports this (interviews, analytics, support tickets)? Without a validated problem, the spec is a solution looking for a problem." |
| **R2** | **REFUSE to define only the happy path.** Every screen, API endpoint, and user flow must define loading, empty, error, and edge-case states. The happy path is ~20% of the spec; the other 80% is everything that can go wrong. | Trigger: spec contains screen/flow definitions where loading, empty, and error states are not mentioned within 10 lines of the primary state definition | STOP. Insert state checklist before proceeding: "For each interaction: define the Loading state (what user sees while waiting), Empty state (what user sees with no data), Error state (what user sees on failure with recovery action), and Edge case (concurrency, permissions, data limits)." |
| **R3** | **REFUSE to include implementation details in the spec.** "Use Redis", "Build in React", "Deploy on Kubernetes" are engineering decisions, not spec requirements. The spec describes WHAT, not HOW. | Trigger: spec contains technology-specific implementation directives (`use [technology]`, `build in [framework]`, `deploy on [platform]`) within requirement descriptions | STOP. Rewrite as outcome: "Cache query results with configurable TTL" not "Use Redis with 300s TTL." Engineering owns implementation choices; the spec owns the behavioral contract. |
| **R4** | **DETECT and WARN when acceptance criteria are not testable.** "User can reset password" is not testable. GIVEN/WHEN/THEN format with measurable outcomes is the minimum standard. | Trigger: user story acceptance criteria uses verbs without measurable outcomes: "works", "can", "able to", "supports" without a GIVEN/WHEN/THEN structure | WARN. Rewrite each: "'User can reset password' → 'GIVEN a registered user on the login page, WHEN they click Forgot Password and enter their email, THEN a reset link is sent within 60 seconds AND the user sees a confirmation message.'" |
| **R5** | **DETECT and WARN when the "Out of Scope" section is missing.** Without explicit non-goals, every conversation during implementation becomes a scope negotiation under time pressure. | Trigger: spec does not contain an "Out of Scope", "Non-Goals", or "What We're NOT Building" section | WARN. Insert: "**Out of Scope (explicitly NOT in this spec):** [list items stakeholders have mentioned but are deferred]. This section is a pre-agreed contract — when scope tries to expand during build, point here." |
| **R6** | **DETECT and WARN about unmapped dependencies.** Every external dependency (other team, service, API, vendor) must have an owner name, team, committed date, and fallback plan. | Trigger: spec mentions an external dependency ("Needs [service]", "Depends on [team]", "Requires [API]") without specifying: owner, team, committed date, AND fallback within 3 lines | WARN. Append dependency table: "\| Dependency \| Owner \| Team \| Committed Date \| Fallback if Late \|" with a row for each unmapped dependency. |
| **R7** | **DETECT and WARN when the spec describes a solution that has no clear user need or problem statement.** "Build a dashboard with real-time analytics" is a solution. "Users can't answer operational questions without asking the data team and waiting 2 days" is a problem. A spec that starts with the solution skips the most important question: should we build this at all? Solutions without problems produce features nobody uses. | Trigger: spec has detailed solution but no identifiable user problem statement or the problem is described as "users want X feature" | WARN. Require: spec preamble in JTBD format: "When [situation], I want to [motivation], so I can [outcome]." If the desired outcome can't be tied to a business metric, the problem isn't well-understood enough to spec. |
| **R8** | **REFUSE to accept edge-case-free specs that only describe the happy path.** "User logs in, clicks transfer, enters amount, hits submit, done." The spec describes 1 path. Engineering discovers 47 paths: what if the bank is offline? What if the amount exceeds the daily limit? What if 2FA times out? What if the recipient account is invalid? Each undiscovered edge case becomes an engineering decision made under sprint pressure rather than a considered product decision. | Trigger: spec has no error states, edge cases, or failure modes section | STOP. Require: every spec has an "Error States & Edge Cases" section covering: loading state (spinner, skeleton, placeholder), empty state (no data yet), error state (API failure, validation error, timeout), edge cases (max length, special characters, concurrent edits), and accessibility states (focus, screen reader announcements). |
| **R9** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R10** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

Master idea to specs understand that strategy is not about predicting the future — it's about **being less wrong than the competition, faster**.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Survivorship bias** — studying only winners, ignoring the graveyard | Study 3 failures for every success; what killed them? |
| **Narrative fallacy** — creating clean stories for messy realities | Write the "strategy could be wrong because..." section first |
| **Confirmation bias** — seeking data that supports your thesis | Assign a team member to build the best case AGAINST your strategy |
| **Short-termism** — optimizing this quarter at the expense of next year | Every decision gets a "6-month" and "3-year" impact column |

### What Masters Know That Others Don't
- **The bottleneck is always one thing.** Find it. Fix it. Then find the next one.
- **Strategy = what you say NO to.** If your strategy doesn't exclude anything, it's not a strategy.
- **Timing beats brilliance.** The best strategy at the wrong time loses to a mediocre strategy at the right time.

### When to Break Your Own Rules
- **Bet the company when the asymmetry is right.** If downside = $1M and upside = $1B, the math doesn't care about your process.
- **Ignore the data when you're creating a new category.** By definition, there's no data for something that doesn't exist yet.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Initiative | Execute a defined strategic initiative with clear metrics |
| **L2** | Product line / function | Define strategy for a product line; own outcomes |
| **L3** | Business unit | Set multi-year strategy for a business unit; allocate resources across competing priorities |
| **L4** | Company | Define company-wide strategy; make existential trade-off decisions |
| **L5** | Industry | Shape industry dynamics; create new market categories |

**Default level for this skill:** L2
**Usage:** Invoke this skill with your target level, e.g., "as an L3 idea to spec, develop..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- A stakeholder has a one-paragraph idea and needs a formal spec before sprint planning
- A feature request lacks technical detail (data shapes, API endpoints, error states)
- You need to evaluate feasibility and surface unknowns before committing to a roadmap
- A greenfield product needs its first structured artifact beyond a pitch deck
- An existing system needs a net-new module and someone must bootstrap the design doc

## Decision Trees

**(QUICK)**

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
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

**What good looks like:** The output opens correctly in the target tool. All validations pass. No placeholder content remains.

```

### Stakeholder Alignment Strategy

```
Which stakeholders need to sign off and how?
├── Solo founder / single decision-maker → Async review in document comments
│     Share the scope brief. 24-hour review window. Resolve comments in 1:1. Move fast.
├── Small team (2-5 engineers, 1 PM) → Spec review meeting (30 min)
│     Pre-read sent 24 hours before. Meeting time: 80% discussion, 20% presentation.
│     Outcome: approved / approved with changes / needs major rework with clear reasons.
├── Cross-functional (engineering + design + product + data) → RFC process (3-5 days)
│     Spec published as RFC document. Comment period: 3 business days minimum.
│     Resolution meeting to address unresolved threads. RACI per decision area.
│     If unresolved after meeting → escalate to engineering-manager + product-manager.
└── Enterprise (multiple teams, compliance, security, legal) → Formal review board (1-2 weeks)
      Architecture Review Board for system-level impact. Security review for auth/data concerns.
      Legal review for terms, privacy, compliance. Each gate must pass before next phase begins.
      Risk: review board becomes bottleneck — designate a single DRI to drive spec through gates.
```

### Breaking Down Work

```
How do you decompose a spec into implementable increments?
├── User story mapping (high-uncertainty features, new product) → Breadth-first
│   ├── Map the user journey horizontally: steps from start to goal
│   ├── Stack vertical slices by priority: what's the minimum usable version?
│   ├── Slice 1 (walking skeleton): user can complete the journey with minimal UI and no edge cases
│   ├── Slice 2 (meat): add primary features, error handling, 80% of user value
│   ├── Slice 3 (polish): edge cases, animations, accessibility, performance optimization
│   └── Each slice ships independently and provides user value — no "integration" milestone
├── CRUD decomposition (data-heavy features, dashboards) → Entity-first
│   ├── Identify entities: what data objects does the user interact with?
│   ├── For each entity: Read (list + detail view) → Create → Update → Delete
│   ├── Ship Read first (immediate value — users can see their data)
│   ├── Ship Create/Update second (users can modify)
│   ├── Ship Delete last (lowest urgency, highest risk)
│   └── Each entity ships as a self-contained increment
└── Workflow decomposition (multi-step processes, onboarding, checkout) → Step-sequential
    ├── Break the workflow into sequential steps
    ├── Ship Step 1 independently (even if steps 2-3 are manual/email for now)
    ├── Ship remaining steps one at a time, each completing more of the workflow
    └── Never: wait until all steps are done for a single "launch" — that's waterfall
```

## Core Workflow

**(STANDARD)**

<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Discovery & Scoping
Extract the core problem, target persona, and success criteria from the raw input. Use the Five Whys to drill past solution proposals to root needs. Document explicit non-goals — what the feature deliberately excludes. Identify assumptions and unknowns that need validation before writing code. Output a one-page **Scope Brief** that captures: Problem Statement, Target Users, Success Metrics (leading and lagging), Scope Boundaries (in/out), and Open Questions with owners.

### Phase 2 (~30 min): Domain Modeling
Identify entities, their attributes, relationships, and cardinalities. Favor composition over deep inheritance. Define state machines for entities with lifecycle transitions. Annotate each entity with: required vs. optional fields, validation rules, uniqueness constraints, and indexing strategy. Produce an **Entity Relationship Diagram** (textual or visual) and a **Data Dictionary** with one row per field. For each relationship, specify ownership direction and cascade behavior.

### Phase 3 (~20 min): API Design
For every operation identified in the scope brief, define: HTTP method, URL path, request body schema (JSON/Protobuf), query parameters, response body schema, and error codes for every failure mode. Group endpoints by resource. Define pagination, sorting, and filtering conventions uniformly. Specify authentication and authorization per endpoint. Document idempotency guarantees. Output an **OpenAPI 3.1 spec** snippet or equivalent **API Contract** document.

### Phase 4 (~15 min): Screen & Interaction Inventory
List every screen, modal, drawer, or stateful view the feature requires. For each screen: name the route, list data dependencies (which API calls fire on mount), define loading, empty, error, and edge-case states, and enumerate all user actions with their system responses. Produce a **Screen Inventory** table and wireframe descriptions. Include accessibility requirements per screen (heading hierarchy, focus management, ARIA landmarks).

### Phase 5 (~25 min): Work Item Breakdown
Slice the spec into vertically deliverable user stories. Each story must be independently shippable and demonstrable. Write stories in the `As a [role], I want [action], so that [value]` format with concrete acceptance criteria. Sequence stories by dependency and value-to-effort ratio. Tag each story with a t-shirt size estimate for early capacity planning. Output a **Story Map** ordered by priority.

## Best Practices

1. **Start with a Scope Brief, not a PRD.** Before writing a full PRD, produce a one-page Scope Brief: Problem Statement, Target Users, Success Metrics, Scope Boundaries, and Open Questions. If stakeholders cannot align on the Scope Brief, they will never align on the PRD. The Scope Brief is the cheapest artifact that can prevent a bad spec.

2. **Match spec depth to complexity.** Simple CRUD (1 screen, 1 entity) → 3-5 pages. Integration-heavy feature (3-5 screens, multi-entity) → 8-12 pages + API contract. Platform capability (10+ screens, cross-team) → 15+ pages + architecture review. Over-spec wastes design time; under-spec guarantees rework. Both directions cost money.

3. **Define non-functional requirements before implementation.** When performance targets, security requirements, and scalability ceilings are absent from the spec, engineering optimizes for functional correctness only. Retrofitting caching, auth rewrites, or database sharding post-implementation costs 5-10x more. Every spec must include: p95 latency target, throughput expectations, auth model, data classification, and growth rate over 12 months.

4. **The API contract is the spec's single source of truth.** When frontend and backend interpret "the user endpoint returns profile data" differently, you discover the mismatch during integration testing — after both teams have "finished." Always include an OpenAPI/GraphQL schema in the spec and validate it with a mock server before any code is written.

5. **Every spec must define success criteria that can be verified before code freeze.** "Users will love the new workflow" cannot be verified until launch. Success criteria must include pre-launch proxies: "In usability testing, 8/10 users complete the workflow in <3 minutes without assistance." Verifiable before code freeze = spec is testable.

6. **Specs describe WHAT; engineering decides HOW.** When the PM writes "use PostgreSQL with composite indexes," two things happen: engineers lose ownership, and the implementation might be wrong but nobody questions it because "it's in the spec." The boundary: if an engineer is making a UX decision, the spec is undertooled. If the PM is making a database decision, the spec is overreaching.

7. **Include data provenance for every metric and data element.** "Build a dashboard with these 15 metrics" — but 7 of the 15 require data from a system that doesn't have an API. Every spec must trace: "Metric X comes from system Y via endpoint Z, field `field_name`." Data provenance gaps discovered during implementation are the #1 cause of scope creep.

8. **Structure for SKIM → DIVE.** A 40-page prose spec is not consumed. Structure: 1-page executive summary (decisions), entity-relationship diagram (structure), OpenAPI spec (contract). Details in appendices. Engineers should be able to start estimating from page 1 and coding from page 5.

9. **Define the MVP boundary explicitly.** Document what's IN scope and what's deliberately OUT of scope with equal clarity. "Out of scope" is not a failure — it's a decision. Without explicit non-goals, every stakeholder review adds scope. The spec that says "yes" to everything is the spec that ships nothing.

10. **Post-mortem every spec 3 months after implementation.** Compare what was spec'd vs what shipped. Track: spec accuracy score (0-100%), number of "discovered during implementation" changes, and engineering rework cost from missed edge cases. Your spec accuracy score IS your skill level.

## Error Decoder

| Error Message / Situation | Root Cause | Fix | Lesson |
|--------------------------|------------|-----|--------|
| Engineering discovers 15 missing requirements mid-build | Under-spec: "build a dashboard" with no data provenance, no error states, no edge cases. Engineers fill gaps with guesses. | Minimum viable spec: data model, API contract, error-state handling, data provenance for every metric. Write the spec as if YOU had to build it. | The spec you don't write is the spec engineering guesses. Guesses cost 2-3x more in rework than writing the spec upfront. |
| Feature ships on time but cannot answer "did it work?" | No success criteria in the spec. PM defined WHAT to build but not HOW to know if it succeeded. | Every spec includes: primary metric + target, counter metrics, instrumentation plan, evaluation timeline. "We'll measure after launch" means you won't measure at all. | A spec without success criteria is an open-ended commitment with no off-ramp. |
| Spec is 40 pages of prose — engineering reads 3 pages and starts coding | Spec structured for reading, not for skimming. Engineers need API contract and data model; prose summary is background. | Structure for SKIM → DIVE: 1-page executive summary (decisions), entity-relationship diagram (structure), OpenAPI spec (contract). Details in appendices. | A spec that isn't consumed isn't a spec. It's a document that made the PM feel productive. |
| "Build a dashboard with these 15 metrics" — 7 have no data source | PM specified WHAT to display without verifying WHERE the data comes from. Engineering discovers the gap during implementation and the feature doubles in scope. | Every data element in the spec must trace to a source system, endpoint, and field. If the data doesn't exist, the spec is a wishlist, not a plan. | Data provenance gaps are the #1 cause of scope creep in specs. Trace every metric to its source before the spec is approved. |
| Spec says "use PostgreSQL with composite indexes" — PM overreaching into implementation | PM wrote implementation instructions instead of requirements. Engineers implement the wrong architecture because "it's in the spec." | Specs describe WHAT (user needs, requirements, success criteria). Engineering writes HOW (architecture, technology choices). The boundary is non-negotiable. | When PMs write code, two things happen: engineers lose ownership, and the architecture is suboptimal. |
| Scope Brief aligned, PRD approved, but stakeholder sends "one quick addition" per day during implementation | No change control process. Every "quick addition" adds 1-3 days of engineering + QA. Five unplanned additions per sprint = unbudgeted scope creep. | Gate every addition: "We can add this — what existing item should we deprioritize to make room?" Trade-offs must be explicit and visible. | Scope creep without trade-offs is just a wishlist with deadlines. |

## Error Recovery

**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Cross-Skill Coordination

<!-- QUICK: 30s -- table of who to talk to when -->
Converting an idea into a spec is inherently collaborative — it synthesizes product intent, design thinking, and engineering reality. A spec written in isolation produces three things: rework, frustration, and missed deadlines.

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `product-manager` | Prioritized backlog, RICE scores, user stories, success metrics, stakeholder constraints | During feature kickoff; before scope trade-off decisions |
| `ux-researcher` | User personas, journey maps, research findings, mental models, task flows, pain point evidence | Before writing acceptance criteria; when user flow ambiguity exists |
| `system-architect` | Architecture constraints, service boundaries, API conventions, data flow direction, performance budgets | When designing new services or cross-service features; before API contract design |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `api-designer` | Endpoint inventory, request/response schemas, error codes, idempotency requirements, pagination needs | API contracts are inconsistent — integration bugs and rework |
| `frontend-developer` | Screen inventory with loading/empty/error/edge states, interaction specs, accessibility requirements | Devs discover edge cases mid-sprint — missed deadlines |
| `backend-developer` | Domain model, data dictionary, business rules, validation logic, performance requirements | Business logic gaps found during implementation — sprints slip |
| `database-designer` | Entity relationship diagram, access patterns, data volume projections, consistency requirements | Schema must be reworked after implementation — data migrations cascade |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Scope change after spec approved | `product-manager`, `engineering-manager`, `qa-engineer` | Sprint replanning, capacity reallocation, timeline impact |
| API contract change during spec | `api-designer`, `frontend-developer`, `backend-developer`, `qa-engineer` | Contract versioning, mock updates, test case changes |
| New dependency discovered (external service, data pipeline) | `system-architect`, `backend-developer`, `product-manager` | Integration complexity, timeline risk, architectural review |
| Ambiguity in acceptance criteria flagged by QA | `product-manager`, `engineering-manager` | Clarification needed before implementation proceeds |
| Cross-team dependency identified late | `product-manager`, `system-architect` | Dependency sequencing, parallelization opportunities, blocker resolution |
| Performance requirement exceeds known system capacity | `system-architect`, `backend-developer` | Architecture review, caching strategy, load testing plan |

### Escalation Path

```
Spec blocked (unresolved ambiguity, missing stakeholder, scope conflict)
  └── `product-manager` + `engineering-manager`. Resolution within 24 hours or escalation to `cto-advisor`.

Architecture conflict (spec requires pattern that violates architecture principles)
  └── `system-architect` + `cto-advisor`. Decision documented as ADR. Spec updated or exception granted.

Cross-team dependency deadlock (two teams block each other)
  └── `product-manager` + engineering leads of both teams. `cto-advisor` breaks ties if unresolved in 48 hours.
```

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| Idea description is too vague ("make it better," "improve UX") with no concrete user problem | Ask clarifying questions: "What user behavior change do you want to see?" and "What does success look like numerically?" Refuse to write spec until problem is defined in one sentence | Vague ideas produce vague specs. A spec built on an undefined problem will be rejected by engineering, QA, and users — the cost of clarifying upfront is 10 minutes; the cost of rewriting a spec is 2 weeks |
| No non-functional requirements mentioned (performance, security, accessibility, compliance) | Proactively ask: "What's the P95 latency budget? Are there regulatory constraints? Does this need to work offline?" Add NFRs section before declaring spec complete | NFRs discovered mid-implementation cause the worst kind of rework — architecture-level changes. Every missing NFR in the spec is a potential sprint derailment |
| No mobile or responsive consideration in a consumer-facing feature spec | Flag "mobile-first" design requirement. Ask: "What happens at 320px? What gestures are expected? Is offline mode needed?" Add responsive behavior to screen inventory | 60%+ of consumer traffic is mobile. Designing desktop-first and retrofitting mobile produces clunky experiences and missed launch dates — handle viewport strategy in the spec, not in the bug tracker |
| No API contract mentioned when cross-service communication is required | Propose OpenAPI spec generation as part of the spec deliverable. Coordinate with `api-designer` to define endpoints, request/response schemas, error codes, and idempotency requirements | API contract ambiguity is the #1 cause of integration bugs. A spec without an API contract is a wish, not a plan — frontend and backend teams will build against different assumptions |
| Acceptance criteria use "works," "functional," or "complete" as completion signal | Replace all vague criteria with GIVEN/WHEN/THEN format. Reject any story that can't be validated by QA without asking clarifying questions | "Works" means 10 different things to 10 different engineers. Measurable acceptance criteria are the contract between product intent and engineering delivery — without them, QA is guessing |
| Spec mentions a dependency on another team's service/API without a named contact or date | Map all external dependencies with owner name, team, expected availability date, and fallback plan. Flag to `product-manager` if any dependency has no committed date | An unmapped dependency is a delayed launch. Every external team needs a named contact and a timeline — otherwise the spec is planning around assumptions, not commitments |
| Feature spec doesn't reference any user research or data that justifies the feature | Ask: "What user evidence supports this feature? Is there a pain point severity rating, support ticket count, or churn signal?" If none exists, flag to `ux-researcher` for validation sprint before full spec | Features built without evidence become shelfware. A 2-day validation sprint costs far less than a 2-month build of something nobody needs |
| No entity relationship model when feature touches database schema | Coordinate with `database-designer` to produce ERD, data dictionary, access patterns, and cardinality rules. Add to spec appendix | Schema decisions made by individual engineers without coordination create data inconsistencies that take quarters to untangle. Spec-level data modeling prevents migration cascades |


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

### How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "idea-to-spec",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }
   ```
3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.

### State Log Schema

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |

### Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## What Good Looks Like

### BEFORE (Novice) → AFTER (World-Class)

**Spec Quality:**
- **BEFORE:** "Build a dashboard with these 15 metrics." Engineers start coding from a 3-bullet Slack message. Discover mid-sprint that 7 metrics come from a system without an API, 3 metrics have conflicting definitions, and nobody defined what "real-time" means. Two sprints of rework. $50K-$150K in engineering waste.
- **AFTER:** Spec includes: problem statement with user evidence, data provenance for every metric (source system + endpoint + field), API contract (OpenAPI 3.1, validated — mock server generates from it), screen inventory with loading/empty/error/edge states per screen, explicit out-of-scope list, and dependency map with owner names and committed dates. Engineering estimates within 20% of actual. Zero "discovered during implementation" architecture changes.

**Scope Discipline:**
- **BEFORE:** "Can we also add sorting? And export to CSV? And a dark mode?" Five unplanned additions per sprint. Each adds 1-3 engineering days. Release delayed by 3 weeks. Nobody knows why the sprint keeps "failing."
- **AFTER:** Every scope change gates through: "We can add this — what existing item should we deprioritize?" Out-of-scope section in the spec acts as a pre-agreed contract. When scope tries to expand, point at the spec. Trade-off decisions made at spec time, not during crunch time.

**Dependency Management:**
- **BEFORE:** "We need the billing team's new API." No named contact. No committed date. No fallback plan. Billing team deprioritizes the API. Your feature blocks for 6 weeks. Launch delayed.
- **AFTER:** Dependency table with: dependency name, owning team, named contact, committed date, fallback if late. Escalation path defined. Cross-team dependency deadlock resolved within 48 hours via product-manager + engineering leads.

> Every requirement traces back to a user interview, analytics event, or support ticket — there are no orphan features that "seemed like a good idea."

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.

## Deliberate Practice

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Take a feature currently in development at your company. Write the spec for it retroactively: problem statement, data model, API contract, screen inventory, work breakdown. Then compare with what the team actually built. Where did your spec diverge from reality? What did the team discover during implementation that you missed? | Monthly |
| **Competent** | Write the same feature spec at 3 depths: lightweight (scope brief + API contract, 2-4 hours), standard (PRD + API + screens, 1-3 days), heavy (full spec with architecture, 1-2 weeks). For each, identify which scenario justifies that depth. Present to a senior engineer for feedback on whether you matched depth to complexity correctly. | Quarterly |
| **Expert** | Take a spec you wrote 6+ months ago and post-mortem it against the shipped product. What was accurate? What was wrong? Which assumptions proved false? Which edge cases did you miss that caused the most rework? Write a 1-page "spec accuracy report" and identify the pattern in your blind spots. | Quarterly |
| **Master** | Design a spec template and process for a 200-person engineering org. Include: when to write a spec vs skip it, depth decision framework, review process (who reviews, how long, what gates), template structure, quality checklist, and integration with sprint planning. Pilot it with 2 teams, measure spec-to-reality accuracy, iterate. | Annually |

**The One Highest-Leverage Activity:** Post-mortem every spec 3 months after implementation. Compare what was spec'd vs what shipped. Track: spec accuracy score (0-100%), number of "discovered during implementation" architecture changes, and engineering rework cost from missed edge cases. Your spec accuracy score IS your skill level.

## Anti-Patterns

- **Building without a spec costs 2-3x in rework.** When engineers start coding from a Slack message or a 3-bullet ticket, they guess at edge cases, data models, and error states. Each rework cycle costs 50-200% of the original build — a $50K feature becomes a $100K-$150K feature. A 2-day spec sprint costs ~$4K in PM + engineering time and prevents $50K-$500K in rework. **Total cost: $50K-$500K per underspecified feature.** Never greenlight engineering without at minimum: data model, API contract, and error-state handling defined.
- **Scope creep without change control bleeds $10K-$100K/month.** Every "quick addition" — "can we also add sorting?", "what about export to CSV?" — adds 1-3 days of engineering + QA per request. Five unplanned additions per sprint = 5-15 extra engineering days per sprint. At a $200K fully-loaded engineer, that's $4K-$12K per sprint in unbudgeted scope. **Total cost: $10K-$100K/month in delayed release and over-budget work.** Gate every addition through a change control: "We can add this — what existing item should we deprioritize to make room?"
- **Wrong spec depth wastes money in both directions.** An over-spec with 40 pages of UI mockups and interaction states costs $20K-$50K in design time for a feature that engineering will inevitably adapt during implementation. An under-spec with "build a dashboard" costs $50K-$200K when engineering discovers 15 missing requirements mid-build. **Total cost: $20K-$200K depending on which extreme you land on.** Match spec depth to complexity: simple CRUD (3-5 pages), integration-heavy feature (8-12 pages + API contract), platform capability (15+ pages + architecture review).
- **Missing API contract in the spec guarantees integration rework.** When frontend and backend teams interpret "the user endpoint returns profile data" differently, you discover the mismatch during integration testing — after both teams have "finished." Fixing contract mismatches costs $15K-$50K in rework for a medium-complexity feature. **Total cost: $15K-$50K per feature without a shared API contract.** Always include an OpenAPI/GraphQL schema in the spec and validate it with a mock server before any code is written — the contract is the spec's single source of truth.
- **Skipping non-functional requirements in the spec until implementation.** When performance targets, security requirements, and scalability ceilings are absent from the spec, engineering optimizes for functional correctness only. A feature that works on a developer's laptop crumbles under real load, fails a penetration test two weeks before launch, or can't scale past 100 concurrent users. Retrofitting caching layers, database sharding, or auth rewrites post-implementation costs 5-10x more than designing for them upfront. **Total cost: $30K-$150K per feature requiring architectural retrofit for missing NFRs.** Include explicit NFR sections in every spec: performance (p95 latency, throughput), security (auth model, data classification, threat assumptions), and scalability (concurrent users, data volume, growth rate over 12 months).
- **Writing the spec without defining what success looks like in production.** A spec describes what to build but not how to know if it worked. Engineering builds to spec. The feature launches. Three months later, PM can't answer: "Did it work?" No success metrics, no baseline, no instrumentation. This is how features accumulate that nobody can justify killing or keeping. **Total cost: $50K-$150K per feature built without success criteria (engineering + design + PM cost that produced zero learning).** Fix: Every spec includes a "Success Criteria" section with: (1) Primary metric + target (e.g., "Increase checkout completion from 62% to 68% within 30 days"), (2) Counter metrics that must not degrade (e.g., "Returns must not increase by > 2%"), (3) instrumentation plan (what events to log), (4) evaluation timeline (when do we look and decide ship/kill?).
- **Specifying implementation details ("use PostgreSQL with composite indexes") instead of requirements ("queries must return in < 50ms at P95").** When the PM writes implementation details, two things happen: (1) engineers lose ownership and motivation, (2) the implementation might be wrong but the engineer implements it anyway because "it's in the spec." Six months later: the composite index wasn't the right solution but nobody questioned it during development. **Total cost: $20K-$60K per project in suboptimal architecture + engineer disengagement and attrition risk.** Fix: Specs describe WHAT (user needs, functional requirements, non-functional requirements, success criteria). Engineering writes HOW (architecture, technology choices, implementation). The boundary is: if an engineer is making a UX decision, the spec is undertooled. If the PM is making a database decision, the spec is overreaching.
- **"Blueprint" that's 40 pages of prose** — the engineering team doesn't read it. They skim the data model diagram and the API contract, then start coding. A spec that isn't consumed isn't a spec. Structure for SKIM → DIVE: 1-page executive summary (decisions), entity-relationship diagram (structure), OpenAPI spec (contract). Details in appendices.
- **"Build a dashboard with these 15 metrics"** — the spec describes WHAT to display, not WHERE the data comes from. Engineering discovers that 7 of the 15 metrics require data from a system that doesn't have an API. Spec must include DATA PROVENANCE: "Metric X comes from the billing system via `GET /invoices`, field `total`."
- **Success criteria that can't be verified until launch** — "Users will love the new workflow" — you won't know until it ships. Success criteria must include pre-launch proxies: "In usability testing, 8/10 users complete the workflow in < 3 minutes without assistance." Verifiable before code freeze.

## Verification

- [ ] Executive summary: 1 page — decisions, not details (details in appendices)
- [ ] Data provenance: every data element traced to source system and endpoint
- [ ] API contract: OpenAPI/GraphQL schema validated (can generate a mock server from it)
- [ ] Data model: ER diagram with all entities, relationships, and key fields labeled
- [ ] Success criteria: pre-launch proxies defined — verifiable before code freeze
- [ ] Stakeholder sign-off: Engineering, Design, and Product have reviewed and approved

## Verification Guardrails

Before delivering work, the agent must verify:

- [ ] **Self-check against What Good Looks Like:** All deliverables meet the quality bar defined above
- [ ] **No broken references:** All file paths, URLs, and skill references resolve correctly
- [ ] **Continuity with State Log:** No prior decisions contradicted without documented rationale
- [ ] **Anti-hallucination check:** No fabricated APIs, version numbers, or capabilities asserted
- [ ] **Error Recovery paths exercised:** Failure modes documented and recovery steps tested
- [ ] **Cross-skill dependencies satisfied:** All upstream skill outputs consumed as documented

If any checkbox fails, revise before delivering. When all pass, add to the state log.

## Production Checklist

**(STANDARD)**

- [ ] **[ITS1]** Scope Brief written: Problem Statement, Target Users, Success Metrics, Scope Boundaries (in/out), Open Questions with owners
- [ ] **[ITS2]** Domain model complete: entities, attributes, relationships, cardinalities, state machines for lifecycle entities
- [ ] **[ITS3]** API contract defined: OpenAPI/GraphQL schema validated, mock server generates successfully, authentication and authorization per endpoint specified
- [ ] **[ITS4]** Data provenance documented: every data element traced to source system, endpoint, and field
- [ ] **[ITS5]** Non-functional requirements specified: p95 latency target, throughput, auth model, data classification, scalability ceiling with 12-month growth projection
- [ ] **[ITS6]** Screen inventory complete: every screen/state documented with data dependencies, loading/empty/error/edge-case states, accessibility requirements
- [ ] **[ITS7]** MVP boundary explicit: IN scope and OUT of scope documented with equal clarity; non-goals are decisions, not omissions
- [ ] **[ITS8]** Work items sliced vertically: each story independently shippable and demonstrable, sequenced by dependency and value-to-effort ratio
- [ ] **[ITS9]** Success criteria include pre-launch proxies: verifiable before code freeze (e.g., usability test benchmarks)
- [ ] **[ITS10]** Change control process defined: scope additions gated through explicit trade-off ("what do we deprioritize to make room?")
- [ ] **[ITS11]** Stakeholder sign-off: Engineering, Design, and Product have reviewed and approved the spec
- [ ] **[ITS12]** Spec accuracy tracked: post-mortem scheduled for 3 months post-launch; spec accuracy score and rework cost measured

## References

Detailed reference material loaded on demand:

- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)

