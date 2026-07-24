# Agent Handoff State — JSON Schema Specification v1.0.0

## Root Object

```json
{
  "handoff_version": "1.0.0",
  "pipeline_id": "uuid",
  "origin_skill": "string",
  "target_skill": "string",
  "created_at": "ISO8601",
  "decisions": [],
  "artifacts": [],
  "constraints": [],
  "context_pruned": {},
  "open_questions": []
}
```

## Field Specifications

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `handoff_version` | semver string | Yes | Schema version for forward/backward compatibility |
| `pipeline_id` | UUIDv4 | Yes | Unique identifier linking all handoffs in one pipeline run |
| `origin_skill` | enum string | Yes | Skill name sending the handoff |
| `target_skill` | enum string | Yes | Skill name receiving the handoff |
| `created_at` | ISO8601 | Yes | UTC timestamp of handoff creation |
| `decisions` | array | No | Decision gate ledger entries |
| `artifacts` | array | No | Output files with paths and status |
| `constraints` | array | No | Non-negotiable guardrails for downstream agents |
| `context_pruned` | object | No | Pruning metadata when context was trimmed |
| `open_questions` | array | No | Unresolved items delegated to downstream agents |

## Decision Object

```json
{
  "gate": "string",
  "choice": "string",
  "rationale": "string",
  "rejected_alternatives": ["string"],
  "confidence": "high|medium|low",
  "reversible": true|false,
  "timestamp": "ISO8601"
}
```

## Artifact Object

```json
{
  "type": "adr|diagram|config|code|doc|test",
  "path": "relative/path",
  "status": "approved|draft|blocked|superseded",
  "checksum": "sha256"
}
```

## Constraint Object

```json
{
  "type": "technology|architecture|security|compliance|budget",
  "value": "string",
  "source": "string",
  "non_negotiable": true|false
}
```

## Validation Rules (MUST pass all)

1. `pipeline_id` is consistent across all handoffs in a pipeline
2. `origin_skill` ≠ `target_skill` (no self-handoffs)
3. Every constraint with `non_negotiable: true` must be carried forward
4. `handoff_version` major version mismatch aborts the pipeline
5. Open questions must have non-empty `assigned_to` and `deadline`
