# State Ledger Design

## Purpose
A structured, append-only record of all decisions, constraints, assumptions, risks, and artifacts produced during a multi-agent workflow.

## Schema
```json
{
  "ledger_version": "1.0",
  "session_id": "uuid",
  "created_at": "ISO8601",
  "entries": [
    {
      "id": "entry-uuid",
      "type": "decision|constraint|assumption|risk|artifact",
      "timestamp": "ISO8601",
      "agent": "agent-name",
      "content": {
        "summary": "one-line description",
        "detail": "full context",
        "rationale": "why this was chosen",
        "alternatives": ["considered options"],
        "constraints": ["imposed constraints"]
      },
      "status": "active|superseded|invalidated",
      "superseded_by": "entry-id|null",
      "recovery_path": "how to retrieve full context"
    }
  ]
}
```

## Entry Types

### Decision
Record every architecture, design, and technology choice.
- What was decided, alternatives considered, rationale, constraints.

### Constraint
Record limits discovered during development.
- Source (requirement, test result, dependency), scope, enforcement level.

### Assumption
Record unvalidated beliefs that decisions depend on.
- What was assumed, validation status, risk if wrong.

### Risk
Record identified risks with mitigation.
- Description, probability, impact, mitigation, owner.

### Artifact
Record created files, APIs, schemas.
- Path, type, purpose, content hash, dependencies.
