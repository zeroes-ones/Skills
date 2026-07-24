# Decision Gate Ledger — Recording & Reconciling Decisions

## Purpose

Every irreversible or architecturally significant choice made by an agent MUST be recorded
in the decision gate ledger. This prevents downstream agents from unknowingly reversing
decisions or re-litigating settled questions.

## Ledger Entry Schema

```json
{
  "gate": "unique-kebab-case-id",
  "choice": "the selected option",
  "rationale": "why this option was chosen",
  "rejected_alternatives": ["alt1", "alt2"],
  "confidence": "high|medium|low",
  "reversible": true|false,
  "depends_on": ["gate-id-1"],
  "timestamp": "ISO8601",
  "agent": "skill-name",
  "cost_of_reversal": "low|<1day|<1week|>1week|prohibitive"
}
```

## Gate Lifecycle

```
PROPOSED → DEBATED → DECIDED → COMMITTED → SUPERSEDED
                       ↓
                    REVERSED
```

## Reconciliation Rules

When Agent B receives state from Agent A and finds contradictory decisions:

1. **Same gate, different choice, irreversible** → Agent B MUST ABORT and escalate.
   Do NOT silently override.
2. **Same gate, different choice, reversible** → Agent B may override but MUST
   document rationale and record original decision as SUPERSEDED.
3. **New gate depends on reversed gate** → All dependent gates become DRAFT and
   must be re-evaluated in order.
4. **Confidence mismatch** → If Agent A recorded `confidence: low` and Agent B
   has higher confidence, Agent B may upgrade with evidence.

## Example Ledger (Architecture Pipeline)

| Gate | Choice | Confidence | Reversible | Cost of Reversal |
|------|--------|------------|------------|------------------|
| architecture-pattern | event-driven-microservices | high | no | >1week |
| message-broker | Kafka | high | no | <1week |
| api-gateway | Kong | medium | yes | <1day |
| database-engine | PostgreSQL 15+ | high | no | >1week |
| caching-layer | Redis Cluster | medium | yes | <1day |
| auth-provider | Auth0 | low | yes | <1week |

## Anti-Patterns

- **Decision omission:** Making a choice without a ledger entry → downstream agents
  operate on incorrect assumptions
- **Silent override:** Changing a prior decision without marking it SUPERSEDED →
  audit trail breaks
- **Premature commitment:** Recording decisions as `irreversible: true` before
  sufficient validation → blocks future flexibility
- **Vague rationale:** Recording `rationale: "best option"` → useless for future
  agents trying to understand context
