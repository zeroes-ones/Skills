# State Serialization Contracts

## JSON Schema Template for Inter-Agent State
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "AgentHandoffState",
  "type": "object",
  "required": ["session_id", "turn_number", "domain", "state"],
  "properties": {
    "session_id": {"type": "string", "format": "uuid"},
    "turn_number": {"type": "integer", "minimum": 0},
    "domain": {"type": "string", "enum": ["architecture", "backend", "frontend", "testing", "security", "devops"]},
    "state": {
      "type": "object",
      "required": ["context", "decisions", "artifacts"],
      "properties": {
        "context": {"type": "object", "description": "Immutable context from upstream"},
        "decisions": {"type": "array", "items": {"$ref": "#/definitions/Decision"}},
        "artifacts": {"type": "array", "items": {"$ref": "#/definitions/Artifact"}}
      }
    },
    "parent_agent": {"type": "string"},
    "lineage": {"type": "array", "items": {"type": "string"}}
  },
  "definitions": {
    "Decision": {
      "type": "object",
      "required": ["id", "description", "alternatives", "rationale"],
      "properties": {
        "id": {"type": "string"},
        "description": {"type": "string"},
        "alternatives": {"type": "array", "items": {"type": "string"}},
        "rationale": {"type": "string"},
        "constraints": {"type": "array", "items": {"type": "string"}}
      }
    },
    "Artifact": {
      "type": "object",
      "required": ["path", "type", "summary"],
      "properties": {
        "path": {"type": "string"},
        "type": {"type": "string", "enum": ["file", "directory", "config", "test", "doc"]},
        "summary": {"type": "string"},
        "hash": {"type": "string"}
      }
    }
  }
}
```

## Key Principles
1. **Immutable context:** Upstream decisions are READ-ONLY for downstream agents
2. **Lineage tracking:** Every agent appends itself to lineage array
3. **Decision audit trail:** All design decisions with rationale and alternatives considered
4. **Artifact hash:** Content-addressed artifacts prevent silent corruption
