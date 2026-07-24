# Decision Capture

## Why Decisions Decay

A decision recorded without its rationale will be questioned and possibly reversed by the next agent. The cost of re-litigating a decision (research, discussion, re-implementation) is 3-10x the cost of documenting it during the original session.

## Decision Record Format

```markdown
DECIDED: [one-line summary]
Context: [what problem were we solving?]
Options:
  (a) [option A] — [pros/cons]
  (b) [option B] — [pros/cons]
  (c) [option C] — [pros/cons]
Chose: [option X]
Rationale: [why X over the alternatives, in 1-3 sentences]
Tradeoffs: [what we gave up by not choosing the alternatives]
Revisit trigger: [condition that would cause us to reconsider]
Date: [YYYY-MM-DD]
```

## Decision Classification

| Type | Example | Documentation Priority |
|------|---------|----------------------|
| **Architecture** | Monolith vs microservices | MANDATORY — record in ADR |
| **Technology choice** | Redis vs PostgreSQL for caching | MANDATORY — record in ledger |
| **Pattern choice** | Factory vs builder pattern | RECOMMENDED — record if non-obvious |
| **Naming** | Variable/function naming | OPTIONAL — unless controversial |
| **Workaround** | Deliberate tech debt | MANDATORY — record with revisit trigger |

## Anti-Rationalization Table

| Excuse | Reality |
|--------|---------|
| "The choice was obvious" | Obvious to you, not to the next agent |
| "The code explains itself" | Code shows the choice, not the rejected alternatives |
| "We can always change it later" | Changing later costs 10x without decision context |
| "It's documented in the PR comments" | PR comments are not part of the handoff and will be lost |

## Decision Smells

* Decision made in <5 minutes with no alternatives listed
* Decision based on "it's what we always use" without fit-for-purpose analysis
* Decision deferred with "we'll decide when we need to" — this IS the decision (to accept uncertainty)
