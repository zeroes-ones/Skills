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
