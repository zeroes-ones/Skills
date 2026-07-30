# Handoff State Schema — Standardized Format

## Complete State Bundle

```json
{
  "handoff_id": "uuid",
  "from_skill": "brainstorming",
  "to_skill": "idea-to-spec",
  "created_at": "ISO8601",
  "transferred_state": {
    "decisions": [
      {
        "id": "decision-1",
        "description": "Use PostgreSQL for primary database",
        "rationale": "Team expertise, ACID requirements, JSON support",
        "alternatives_considered": ["MySQL", "MongoDB"],
        "decided_by": "brainstorming",
        "decided_at": "ISO8601"
      }
    ],
    "constraints": [
      {
        "type": "technical",
        "description": "Must deploy on AWS (existing infra)",
        "severity": "hard"
      },
      {
        "type": "budget",
        "description": "Infra budget max $5K/month",
        "severity": "hard"
      },
      {
        "type": "timeline",
        "description": "MVP in 6 weeks",
        "severity": "soft"
      }
    ],
    "open_questions": [
      {
        "id": "q-1",
        "question": "Should we use GraphQL or REST for the API?",
        "context": "Frontend team prefers GraphQL; backend team has REST experience",
        "blocking": false,
        "assigned_to": "system-architect"
      }
    ],
    "ruled_out": [
      {
        "approach": "NoSQL-only architecture",
        "reason": "Requires ACID transactions for payment processing",
        "ruled_out_by": "brainstorming",
        "ruled_out_at": "ISO8601"
      },
      {
        "approach": "Serverless architecture",
        "reason": "Unpredictable costs at scale; cold starts unacceptable for real-time features",
        "ruled_out_by": "brainstorming"
      }
    ],
    "artifacts": [
      {
        "type": "document",
        "path": "docs/architecture-decisions.md",
        "description": "Architecture decision record from brainstorming session"
      },
      {
        "type": "diagram",
        "path": "docs/system-context.png",
        "description": "System context diagram — external integrations"
      }
    ],
    "assumptions": [
      "User base will grow from 1K to 50K in first year",
      "Peak traffic 10K requests/minute",
      "Payment volume $500K/month by month 6"
    ],
    "calibration": {
      "methodology_version": "brainstorming-v2.1",
      "parameters": {"depth": "L3", "participants": "CEO, CTO, Product"}
    }
  },
  "excluded_state": [
    "internal_scratchpad",
    "exploration_dead_ends",
    "preliminary_sketches"
  ],
  "resume_point": "Phase 2: Specification Writing — start with decision-1 and constraints",
  "validation_hash": "sha256_of_transferred_state",
  "validation_method": "SHA-256 of JSON-sorted transferred_state block"
}

```

## Validation Protocol

Receiving skill MUST:
1. Compute SHA-256 of `transferred_state` block
2. Compare with `validation_hash`
3. If mismatch: REJECT handoff. Request re-transmission.
4. If match: ACCEPT. Resume from `resume_point`.

## Minimum Viable Handoff

For simple pipelines, a minimal handoff is acceptable:

```json
{
  "handoff_id": "uuid",
  "from_skill": "A",
  "to_skill": "B",
  "transferred_state": {
    "decisions": ["What was decided"],
    "constraints": ["What limits exist"],
    "open_questions": ["What's unresolved"],
    "ruled_out": ["What was eliminated"]
  },
  "resume_point": "Phase N"
}

```
