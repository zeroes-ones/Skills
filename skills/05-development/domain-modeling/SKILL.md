---
name: domain-modeling
description: >
  Use when building or refining a project's shared vocabulary (ubiquitous language); when onboarding new team members who need to understand domain concepts; when code uses inconsistent terminology for the same concept; when domain rules are scattered across code without centralized documentation; or when making architectural decisions that need domain context. Handles ubiquitous language building through term challenging, edge-case scenario stress testing, CONTEXT.md maintenance as shared domain glossary, Architecture Decision Record (ADR) creation with three-part trigger test, code-vs-domain-rules cross-referencing, vague term detection and disambiguation, domain boundary mapping, and bounded context identification. Do NOT use for code implementation (route to appropriate developer skill), database schema design (route to database-designer), API contract design (route to api-designer), or system architecture diagrams (route to system-architect).
license: MIT
author: Sandeep Kumar Penchala
type: development
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - domain-modeling
  - ubiquitous-language
  - ddd
  - bounded-context
  - glossary
  - adr
  - domain-driven-design
  - context-mapping
token_budget: 4000
chain:
  consumes_from:
    - system-architect
    - product-manager
  feeds_into:
    - backend-developer
    - frontend-developer
    - api-designer
    - database-designer
    - qa-engineer
  alternatives: []
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
---

# Domain Modeling
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Active domain modeling discipline — not just a glossary but a living practice of challenging vague terms, stress-testing with edge-case scenarios, maintaining CONTEXT.md inline, and cross-referencing code against stated domain rules. ADRs are created only when a decision is hard-to-reverse, surprising-without-context, AND the result of a real tradeoff.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable. The agent MUST follow every rule on every invocation.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---|---|---|
| R1 | REFUSE to accept vague terms without challenging them | Any term used in a request or codebase that lacks a precise, testable definition in CONTEXT.md | Halt and ask: "What exactly does '{term}' mean here? Give me a definition I could encode as a validation rule." |
| R2 | DETECT when the same term means different things in different contexts | A term appears in multiple bounded contexts or modules with divergent behavior or constraints | Flag the term, document both meanings in CONTEXT.md with context qualifiers, and propose disambiguation (rename or namespace) |
| R3 | REFUSE to create ADRs without passing the three-part trigger test | User or workflow requests an ADR | Run the trigger test: (1) hard-to-reverse? (2) surprising-without-context? (3) result-of-real-tradeoff? If any answer is NO, explain why an ADR is not warranted and suggest a lightweight alternative |
| R4 | DETECT code that contradicts documented domain rules | Code scan reveals logic that violates a constraint, invariant, or state transition documented in CONTEXT.md | Flag the contradiction with file path, line number, the documented rule, and the violating code. Escalate to the owning team via the appropriate channel |
| R5 | REFUSE to let CONTEXT.md go stale | CONTEXT.md's `Last updated` date is older than 30 days OR code references in CONTEXT.md point to files that no longer exist | Trigger a CONTEXT.md refresh: re-scan the codebase, update stale references, archive deprecated terms, and log the refresh in the term drift log |
| R6 | DETECT implicit bounded contexts that lack explicit boundaries | Two teams or modules operate on the same concept with different rules, but no bounded context boundary is documented | Propose a boundary, name both contexts, define their ubiquitous languages separately, and add an Anti-Corruption Layer (ACL) if integration is needed |
| R7 | REFUSE to let domain rules live only in code | A business rule (invariant, constraint, state machine) exists in code but has no corresponding entry in CONTEXT.md | Extract the rule from code, write it in plain language in CONTEXT.md, and link back to the code location. The rule must be understandable by a domain expert who cannot read code |

## The Expert's Mindset

Domain modeling masters think differently. They don't just document — they interrogate. Every term is a hypothesis until tested against edge cases. Every boundary is a bet about where complexity lives. Every ADR is a signal that the team faced a genuine fork in the road.

### Cognitive Biases to Guard Against

| Bias | How It Corrupts Domain Modeling | Countermeasure |
|---|---|---|
| **Curse of Knowledge** | Assuming terms are "obvious" because you've lived with the domain for years | Explain every term to someone outside the team; if they squint, the term needs work |
| **False Consensus** | Believing the team agrees on definitions when they actually don't | Run a "define X in 30 seconds" exercise — compare answers across the team |
| **Anchoring** | Locking onto the first definition of a term and dismissing later refinements | Maintain a term drift log; treat definitions as evolving, not fixed |
| **Overgeneralization** | Using one term to cover multiple distinct concepts to avoid "over-engineering" | If a term needs "usually" or "typically" in its definition, it's too broad |
| **Sunk Cost** | Refusing to rename a core concept because "we've always called it that" | Price the cost of confusion over the next 12 months vs. the cost of the rename |

## Operating at Different Levels

Domain modeling operates at four levels of granularity. Ascend when the current level can't resolve the problem.

| Level | Scope | Artifacts | When to Use |
|---|---|---|---|
| **L1 — Term Definition** | A single domain term and its precise meaning | CONTEXT.md term entry, validation rules | Clarifying "what is a Customer?" during a code review |
| **L2 — Aggregate Design** | A cluster of entities treated as a single unit with an aggregate root | Aggregate diagram, invariant list, transactional boundary | Designing the Order aggregate: Order, LineItem, Payment, Shipment |
| **L3 — Bounded Context** | A boundary within which a specific domain model applies | Context map, ubiquitous language glossary per context | Separating "Billing Account" from "Identity Account" |
| **L4 — Enterprise Context Map** | The full map of bounded contexts and their integration patterns | Context map diagram, integration contracts, ACL specs | Planning how Ordering, Billing, Shipping, and Inventory contexts interact |

**Escalation rule**: If L1 term disputes can't be resolved without discussing aggregates, move to L2. If L2 aggregate conflicts stem from different assumptions about what "the system" means, move to L3.

## When to Use

- Onboarding new team members who need a mental model of the domain
- Refactoring when code uses inconsistent terminology for the same concept
- Sprint planning when acceptance criteria hinge on domain rule interpretation
- Architecture discussions where domain boundaries are unclear
- Code review when you spot a domain rule enforced differently in two places
- Pre-migration planning (monolith decomposition, service extraction)
- Auditing an existing codebase for undocumented business rules
- Preparing for a domain event storming session

### Do NOT Use

- **Code implementation** — route to [backend-developer], [frontend-developer], or [fullstack-developer]
- **Database schema design** — route to [database-designer]
- **API contract design** — route to [api-designer]
- **System architecture diagrams** — route to [system-architect]
- **Product roadmap decisions** — route to [product-manager] or [product-strategist]
- **UI/UX wireframes** — route to [ui-ux-designer]

## Route the Request

### Auto-Route by Artifacts

When the request context includes these files, auto-activate domain-modeling:

| Artifact Detected | Action |
|---|---|
| `CONTEXT.md` exists in repo root | Load it as the current domain glossary; challenge any stale entries |
| `**/*.glossary.md` or `**/glossary/` directory | Load all glossary files; check for cross-context term conflicts |
| `**/adr/` or `**/doc/adr/` directory | Load the ADR index; check each ADR against the three-part trigger test |
| `**/domain/` directory in code | Scan for aggregates, entities, value objects; cross-reference with CONTEXT.md |
| `**/bounded-contexts.md` or context map diagrams | Validate boundaries against current code organization |

### Intent Route

```
User request
  │
  ├─ "What does X mean?" / "Define X" / "Glossary" / "Ubiquitous language"
  │    └─ TRIGGER: L1 Term Definition — challenge, define, record
  │
  ├─ "ADR" / "Architecture Decision" / "Decision record"
  │    └─ TRIGGER: Run three-part test → create ADR or refuse
  │
  ├─ "Boundary" / "Bounded context" / "Context map" / "Where does X belong?"
  │    └─ TRIGGER: L3 Boundary analysis — identify, name, document
  │
  ├─ "Edge case" / "What happens when" / "Scenario"
  │    └─ TRIGGER: Phase 3 edge-case stress testing
  │
  ├─ "Cross-reference" / "Code vs docs" / "Is this rule enforced?"
  │    └─ TRIGGER: Phase 5 code cross-reference audit
  │
  ├─ "Onboarding" / "New team member" / "Explain the domain"
  │    └─ TRIGGER: Load CONTEXT.md → generate domain narrative
  │
  └─ "Term drift" / "Inconsistent" / "Two meanings"
       └─ TRIGGER: R2 term disambiguation protocol
```

## Core Workflow

### Phase 1: Term Harvesting — Scan the Codebase

**Goal**: Build an initial glossary of every domain-significant term in the codebase.

```
for each source in [code, docs, tickets, conversations]:
    extract nouns that appear in:
        - class/interface/type names
        - method/function names that represent business operations
        - database table/column names (filter out purely technical columns)
        - API endpoint resource names
        - enum values and constants
    for each noun:
        record in initial glossary with provisional definition from usage
```

**Heuristics for domain term detection**:
- Appears in a class name AND a database table (high confidence)
- Appears in multiple files across different modules (medium confidence)
- Appears only in comments or variable names (low confidence — may be informal)

**Output**: A table in CONTEXT.md with columns: Term, Provisional Definition, Source(s), Confidence.

### Phase 2: Term Challenging — Interrogate Every Definition

**Goal**: Refine provisional definitions into precise, testable domain definitions.

```
for each term in glossary:
    challenge round 1: "What does {term} mean here?"
        → Can I write a validation rule?  If NO → term is too vague
        → Does the definition exclude anything?  If NO → boundary is missing
        → Would a domain expert agree?  If NO → incorrect terminology

    challenge round 2: "What is {term} NOT?"
        → Define the negative space explicitly
        → Example: "Customer means a paying account holder, NOT a trial user, NOT a deleted account, NOT a prospect in the CRM"

    challenge round 3: "Does {term} mean the same thing everywhere?"
        → Scan for the term in other modules, APIs, or team documentation
        → If meaning diverges → flag for R2 disambiguation
```

**Output**: Precise definitions in CONTEXT.md, with negative-space clarifications and cross-context notes.

### Phase 3: Edge-Case Stress Testing — Break the Definitions

**Goal**: Invent adversarial scenarios to expose gaps in domain definitions.

```
for each term in glossary:
    generate edge cases using the SCANT framework:
        S — State: What if the entity is in an unexpected state?
        C — Concurrency: What if two actors modify it simultaneously?
        A — Absence: What if a required dependency is missing or deleted?
        N — Negation: What if the opposite of the happy path happens?
        T — Time: What if things happen out of expected order?

    for each edge case:
        determine expected behavior under current definitions
        if expected behavior is undefined or contradictory:
            → gap found — update domain rules
            → add to edge case table in CONTEXT.md
```

**Example edge cases per term**:
- **Order**: "A customer deletes their account while an order is in fulfillment"
- **Subscription**: "Payment succeeds but the provisioning webhook returns a 500"
- **Inventory**: "A warehouse reports stock that doesn't match the system's count"
- **User**: "A user logs in via SSO but the identity provider sends a different email than the one on file"

### Phase 4: CONTEXT.md Maintenance — Keep the Glossary Alive

**Goal**: Ensure CONTEXT.md is the single source of truth for domain knowledge.

```
on every session:
    load CONTEXT.md from repo root (or create if absent)
    check Last updated date:
        if > 30 days → flag for refresh (R5)
    check code references:
        for each Rule ID with a Code Location:
            verify file still exists and line range is valid
            flag broken references

on every term definition or rule change:
    update the relevant section of CONTEXT.md
    log term changes in the Term Drift Log
    update Last updated timestamp

on every edge case discovery:
    add to Edge Cases table with status "open"
    link to the domain rule it challenges
```

**CONTEXT.md sections to maintain**:
1. Bounded Contexts table
2. Core Terms glossary
3. Edge Cases table
4. Domain Rules table (cross-referenced to code)
5. Term Drift Log

### Phase 5: Code Cross-Reference — Verify Code Matches Domain Rules

**Goal**: Detect and flag contradictions between documented domain rules and implemented code.

```
for each domain rule in CONTEXT.md with a Code Location:
    read the referenced code
    verify:
        → The rule is actually enforced (not commented out, not dead code)
        → The enforcement logic matches the documented rule precisely
        → No other code path bypasses this enforcement

for each code file in the domain layer:
    scan for business logic (validation, state transitions, calculations)
    for each piece of business logic found:
        → check if it has a corresponding entry in CONTEXT.md
        → if not: flag as "undocumented domain rule" (R7 violation)

report findings:
    ✅ Rule X enforced at path:line — matches documentation
    ⚠️ Rule Y documented but enforcement missing or incomplete
    ❌ Rule Z enforced in code but absent from CONTEXT.md
```

## Decision Trees

### Term Ambiguity Detection

```
Term T encountered in request or codebase
  │
  ├─ Is T defined in CONTEXT.md?
  │    ├─ YES → Does the definition include negative space?
  │    │         ├─ YES → Is the definition testable as a validation rule?
  │    │         │         ├─ YES → TERM IS WELL-DEFINED — proceed
  │    │         │         └─ NO  → Refine definition until testable
  │    │         └─ NO  → "What is T NOT?" → add negative space → retest
  │    └─ NO  → Provisional definition from usage → add to CONTEXT.md → challenge
  │
  └─ Does T appear in multiple bounded contexts?
       ├─ YES → Same meaning in all contexts?
       │         ├─ YES → Document as cross-context term
       │         └─ NO  → R2: Disambiguate — namespace or rename
       └─ NO  → Single-context term — no disambiguation needed
```

### ADR Trigger Decision

```
ADR requested for decision D
  │
  ├─ TEST 1: Is D hard-to-reverse?
  │    └─ Would undoing D require: major refactoring? data migration? retraining? contract breaking?
  │         ├─ YES → continue to test 2
  │         └─ NO  → REFUSE: "This decision is easily reversible. Use a team wiki page or comment instead."
  │
  ├─ TEST 2: Would D be surprising without context?
  │    └─ Would a new team member ask "why did they do it this way?"
  │         ├─ YES → continue to test 3
  │         └─ NO  → REFUSE: "This decision follows natural defaults. No ADR needed."
  │
  └─ TEST 3: Was D the result of a real tradeoff?
       └─ Were there genuine alternatives with different pros/cons?
            ├─ YES → CREATE ADR with: Title, Status, Context, Decision, Alternatives, Consequences
            └─ NO  → REFUSE: "Only one reasonable approach existed. No tradeoff to document."
```

### Bounded Context Boundary Placement

```
Proposed boundary between concepts A and B
  │
  ├─ Do A and B use different ubiquitous languages?
  │    └─ i.e., do domain experts use different terms for A vs B?
  │         ├─ YES → BOUNDARY IS VALID — proceed to integration design
  │         └─ NO  → Check next signal
  │
  ├─ Are A and B owned by different teams with different roadmaps?
  │    ├─ YES → BOUNDARY IS VALID — organizational boundary implies domain boundary
  │    └─ NO  → Check next signal
  │
  ├─ Do A and B have different lifecycles (create/update/delete schedules)?
  │    ├─ YES → BOUNDARY IS VALID — lifecycle independence is a strong signal
  │    └─ NO  → Check next signal
  │
  ├─ Would a single transaction span A and B?
  │    ├─ YES → BOUNDARY IS SUSPECT — reconsider; shared kernel may be appropriate
  │    └─ NO  → BOUNDARY IS VALID — distinct transactional boundaries
  │
  └─ No signals triggered → Likely NOT a bounded context boundary
       → Consider: shared kernel, or same context with sub-modules
```

### Edge-Case Generation Strategy

```
Given domain term T with definition D
  │
  ├─ STATE: What unexpected states can T be in?
  │    ├─ Invalid state transitions (e.g., Order goes from SHIPPED back to PENDING)
  │    ├─ Intermediate states that are "impossible" per the model
  │    └─ Legacy data in states not covered by current code
  │
  ├─ CONCURRENCY: What if two actors operate on T simultaneously?
  │    ├─ Two admins approve the same refund
  │    ├─ User updates profile while billing runs
  │    └─ Inventory allocation and order cancellation race
  │
  ├─ ABSENCE: What if a dependency of T is missing?
  │    ├─ Parent entity deleted while child entity is processing
  │    ├─ Required external service returns 404
  │    └─ Referenced data migrated away mid-operation
  │
  ├─ NEGATION: What is the opposite of the happy path?
  │    ├─ Payment fails AFTER order confirmation
  │    ├─ Subscription cancels DURING renewal
  │    └─ User revokes OAuth grant mid-session
  │
  └─ TIME: What if operations happen out of order?
       ├─ Shipment arrives before payment clears
       ├─ Notification sent before transaction commits
       └─ Scheduled job runs during a deployment
```

### Glossary Maintenance Cadence

```
CONTEXT.md maintenance trigger
  │
  ├─ PASSIVE: Last updated > 30 days ago?
  │    └─ YES → R5 STALE — full refresh required
  │
  ├─ EVENT-DRIVEN: Domain event occurred?
  │    ├─ New feature added → scan new code for domain terms → add to glossary
  │    ├─ Bug caused by domain rule misinterpretation → strengthen rule definition
  │    ├─ Team discussion revealed terminology confusion → update and disambiguate
  │    └─ Domain expert joined/left → review all definitions for accuracy
  │
  ├─ CODE-DRIVEN: Code change detected?
  │    ├─ New aggregate/entity/value object → extract domain terms → add to glossary
  │    ├─ Validation logic changed → update corresponding domain rule in CONTEXT.md
  │    ├─ State machine modified → update lifecycle documentation
  │    └─ File referenced in CONTEXT.md was deleted/moved → fix broken reference
  │
  └─ REVIEW-DRIVEN: Scheduled review?
       ├─ Sprint boundary → review all terms touched this sprint
       ├─ Pre-release → verify all domain rules have code enforcement
       └─ Quarterly audit → full glossary review with domain expert
```

## Cross-Skill Coordination

Domain modeling feeds domain clarity into every downstream skill while consuming strategic intent from upstream.

| Direction | Skill | What Domain Modeling Provides / Consumes |
|---|---|---|
| **Consumes** | [system-architect] | System decomposition decisions, integration patterns, architectural constraints |
| **Consumes** | [product-manager] | Business requirements, user stories, stakeholder terminology, feature priorities |
| **Feeds** | [backend-developer] | Precise domain definitions, aggregate boundaries, invariant rules, state machines |
| **Feeds** | [frontend-developer] | Ubiquitous language for UI labels, form validation rules, workflow definitions |
| **Feeds** | [api-designer] | Resource naming, bounded context boundaries for API scoping, domain constraints for request validation |
| **Feeds** | [database-designer] | Aggregate boundaries that guide transaction scoping, entity relationships, invariant enforcement points |
| **Feeds** | [qa-engineer] | Domain rules as test cases, edge-case scenarios for test planning, invariant validation checks |

### Coordination Protocol

When domain-modeling detects a conflict between a consumed artifact and domain reality:
1. Document the conflict in CONTEXT.md under a "Cross-Skill Conflicts" section
2. Propose resolution with rationale
3. Route back to the upstream skill for re-alignment
4. Do NOT silently accept upstream artifacts that contradict domain understanding

## Proactive Triggers

The agent watches for these signals and acts without being asked.

| Trigger | Detection Method | Automatic Response |
|---|---|---|
| New PR contains a domain-significant class/entity name not in CONTEXT.md | Scan PR diff for new class/interface/type names matching domain patterns | Comment on PR: "New domain term '{X}' detected. Add to CONTEXT.md?" with provisional definition |
| Two PRs use different terms for the same concept | Compare terminology across recent PRs in the same domain area | Flag the inconsistency, propose canonical term, request alignment |
| CONTEXT.md Last updated > 30 days | Check file metadata on repo load | Trigger R5 stale glossary refresh workflow |
| Bug report mentions "confusion" or "unclear" about business rules | Monitor issue tracker for keywords: confused, unclear, inconsistent, ambiguous | Proactively load CONTEXT.md, check if the relevant rule is defined clearly, propose clarification |
| New microservice or module created without bounded context documentation | Detect new top-level directories in monorepo or new services in deployment config | Ask: "Does this new service represent a new bounded context? Document the boundary." |
| Code comment contains "TODO: clarify business rule" | grep for `TODO.*(business rule\|domain rule\|clarify\|verify)` | Extract the TODO, create a task to define the rule in CONTEXT.md, link back to the code location |

## What Good Looks Like

A well-modeled domain has clear boundaries, a shared language, and traceability from business rule to code.

```
┌─────────────────────────────────────────────────────────────────────┐
│                     ENTERPRISE CONTEXT MAP                           │
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐  │
│  │   Identity   │    │   Billing    │    │     Fulfillment      │  │
│  │   Context    │    │   Context    │    │       Context        │  │
│  │              │    │              │    │                      │  │
│  │  Account     │───▶│  Account     │    │  Order               │  │
│  │  Profile     │    │  Invoice     │◀───│  Shipment            │  │
│  │  Session     │    │  Payment     │    │  Inventory           │  │
│  │              │    │  Plan        │    │                      │  │
│  │  UB: "Account│    │              │    │  UB: "Order =        │  │
│  │  = identity  │    │  UB: "Account│    │  confirmed purchase  │  │
│  │  for login"  │    │  = paying    │    │  with line items"    │  │
│  └──────────────┘    │  entity"     │    └──────────────────────┘  │
│         │            └──────┬───────┘              │                │
│         │                   │                      │                │
│         ▼                   ▼                      ▼                │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    CONTEXT.md (Single Source of Truth)         │  │
│  │  • Core Terms: 47 defined, 0 ambiguous                        │  │
│  │  • Domain Rules: 23 documented, 23 code-verified              │  │
│  │  • Edge Cases: 31 catalogued, 12 resolved                     │  │
│  │  • Bounded Contexts: 3 explicit, 0 implicit                   │  │
│  │  • ADRs: 2 created (both passed 3-part test)                  │  │
│  │  • Last updated: 3 days ago                                   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  Key: UB = Ubiquitous Language   ───▶ = Integration via ACL/Events  │
└─────────────────────────────────────────────────────────────────────┘
```

**Signs of excellence**:
- A new team member can read CONTEXT.md and understand the domain without asking questions
- Every domain rule in CONTEXT.md has a corresponding test that would fail if the rule changed
- Code reviews catch terminology drift before it reaches main
- ADRs exist for the 2-3 truly contentious decisions; everything else is in lightweight documentation
- The term drift log shows active evolution, not neglect

## Deliberate Practice

Five exercises to sharpen domain modeling skills.

### Exercise 1: The 30-Second Definition
Pick any domain term from your current project. Define it in 30 seconds to a colleague who knows nothing about the project. If they can't explain it back correctly, your definition isn't precise enough. Repeat until they can.

### Exercise 2: The Edge-Case Gauntlet
Take the 5 most important domain rules in your project. For each, write 3 edge cases that would break a naive implementation. Then check if your current code handles them. Document the gaps.

### Exercise 3: The Terminology Audit
Pick a bounded context. List every term used in class names, API endpoints, and database tables. Circle any term that appears in more than one bounded context with a different meaning. Propose disambiguation.

### Exercise 4: The ADR Litmus Test
Review the last 10 "architecture decisions" your team made informally (Slack threads, PR comments, meeting notes). For each, run the three-part trigger test. How many would have warranted a formal ADR? Write those ADRs.

### Exercise 5: The Glossary Time Machine
Open your CONTEXT.md (or create one). For each term, ask: "Would this definition have been correct 6 months ago? Will it be correct 6 months from now?" Terms that fail the time test need the term drift log.

## Gotchas

These are the expensive mistakes — quantified in real costs.

### The Cost of Ambiguous Terminology Across Teams
**$50,000–$150,000/year** in wasted engineering time. When "Account" means different things to the Identity team and the Billing team, every cross-team integration requires a discovery meeting. Over a year with 8 cross-team features, that's ~200 hours of clarification meetings. At $250/hr fully loaded, that's $50,000 in direct cost — and the rework from misunderstandings doubles or triples it.

### The Cost of a Stale CONTEXT.md
**$30,000–$80,000 per onboarded developer**. A new hire spends their first 3-4 weeks building a mental model through trial-and-error, asking senior devs, and reading outdated docs. With a maintained CONTEXT.md, onboarding compresses to 1 week. At a $150,000 salary, each week saved is ~$3,000. Across 10 hires, that's $30,000 saved — and the senior devs get their time back.

### The Cost of Premature ADR Creation
**$5,000–$15,000 in decision debt**. Each unnecessary ADR clutters the decision register, making it harder to find the decisions that actually matter. When a new architect joins and has to read 40 ADRs to understand the project — but only 3 are genuinely important — that's a full week of wasted ramp-up. Worse: important ADRs get skimmed because "they all look the same."

### The Cost of Missing a Bounded Context Boundary
**$100,000–$500,000 in remediation**. Failing to separate "Identity Account" from "Billing Account" early on means every schema change to one breaks the other. When you finally split them (and you will), the migration involves: data separation, API versioning, client updates, and coordinated deployments across teams. This is 3-6 months of sustained effort.

### The Cost of Domain Rules Encoded Only in Code
**$20,000–$60,000 per regulatory audit failure**. When auditors ask "where is your policy for handling expired subscriptions?" and the answer is "it's in the code," you fail the audit. A documented domain rule in CONTEXT.md linked to its enforcing code passes. The fine for a single compliance gap in regulated industries (finance, healthcare) starts at $20,000.

### The Cost of Term Drift Over Sprints
**$10,000–$25,000 per quarter** in misdirected development. When sprint 6 uses "User Status" to mean "account active/inactive" but sprint 12's feature treats it as "online/offline presence," the second feature is built on a false assumption. The rework costs 2-3 sprints. Maintaining a term drift log catches this before code is written.

## Verification

Run these checks to confirm the domain model is healthy.

```bash
# Check CONTEXT.md freshness (should be < 30 days old)
find . -name "CONTEXT.md" -mtime +30 -exec echo "STALE: {}" \;

# Find domain terms used in class names but missing from CONTEXT.md
grep -rn "class [A-Z]" --include="*.ts" --include="*.java" --include="*.py" --include="*.go" . | \
  grep -v node_modules | grep -v vendor | \
  while read line; do echo "$line"; done

# Detect terms used in multiple modules with potentially different meanings
grep -rn "\bAccount\b\|\bOrder\b\|\bUser\b\|\bCustomer\b" --include="*.ts" . | \
  awk -F: '{print $3}' | sort | uniq -c | sort -rn | head -20

# Find domain rules in comments that aren't in CONTEXT.md
grep -rn "MUST\|MUST NOT\|SHALL\|SHALL NOT\|business rule\|domain rule\|invariant" \
  --include="*.ts" --include="*.java" --include="*.go" . | \
  grep -v node_modules | grep -v vendor

# Verify all ADRs pass the three-part test
for adr in adr/*.md doc/adr/*.md; do
  echo "=== $adr ==="
  grep -c "hard.to.reverse\|surprising\|tradeoff\|alternative" "$adr" 2>/dev/null || echo "  WARNING: no tradeoff signals found"
done

# Check for undocumented bounded contexts
grep -rn "bounded.context\|context.map\|ACL\|anti.corruption" --include="*.md" . | \
  grep -v node_modules

# Cross-reference: find CONTEXT.md rules without code enforcement
# (requires manual review of output)
grep "Rule ID" CONTEXT.md | while read rule; do
  rule_id=$(echo "$rule" | awk '{print $NF}')
  echo "Rule: $rule_id — verify code enforcement exists"
done
```

## References

1. [Ubiquitous Language](references/ubiquitous-language.md) — Core principles and maintenance of shared vocabulary
2. [Term Challenging](references/term-challenging.md) — Protocol for interrogating domain term precision
3. [Edge-Case Scenarios](references/edge-case-scenarios.md) — Adversarial scenario generation to stress-test definitions
4. [CONTEXT.md Template](references/context-md-template.md) — Living domain glossary structure and sections
5. [ADR Trigger Rules](references/adr-trigger-rules.md) — Three-part test for when to create an Architecture Decision Record
6. [Domain Boundaries](references/domain-boundaries.md) — Identifying where one domain ends and another begins
7. [Code Cross-Reference](references/code-cross-reference.md) — Verifying code implements documented domain rules
8. [Bounded Contexts](references/bounded-contexts.md) — Designing explicit boundaries for domain models
