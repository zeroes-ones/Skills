# Input Validation Hardening — Reference

## Allowlist vs Denylist

| Approach | Security | Maintenance | Example |
|----------|----------|-------------|---------|
| Allowlist (whitelist) | ✅ Strong — reject everything except known good | Higher — must enumerate all valid inputs | `if field in ['asc', 'desc']` |
| Denylist (blacklist) | ❌ Weak — attackers constantly find bypasses | Lower — add new bad patterns reactively | `if field not in [';', '--', '/*']` |
| Hybrid | ⚠️ Partial — allowlist for structure + denylist for content | Medium | JSON Schema (structure) + HTML sanitizer (content) |

**Cardinal rule: Allowlist for structure validation. NEVER denylist for security-critical validation.**

## JSON Schema Allowlist Example

```json
{
  "type": "object",
  "required": ["name", "email"],
  "additionalProperties": false,
  "properties": {
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100,
      "pattern": "^[a-zA-Z0-9\\s'-]+$"
    },
    "email": {
      "type": "string",
      "format": "email",
      "maxLength": 254
    },
    "role": {
      "type": "string",
      "enum": ["user", "editor", "admin"]
    },
    "age": {
      "type": "integer",
      "minimum": 0,
      "maximum": 150
    }
  }
}
```

Key protections in this schema:
- `additionalProperties: false` — rejects unknown fields (mass assignment protection)
- `enum` for controlled vocabulary fields — cannot inject arbitrary roles
- `pattern` with character allowlist — prevents control characters, null bytes
- `format: "email"` — validates email structure
- Numeric `minimum`/`maximum` — prevents integer overflow/underflow attacks

## Mass Assignment Protection

### Vulnerable Pattern (NEVER DO THIS):
```javascript
// Attacker sends: {"name": "Alice", "role": "admin", "is_verified": true}
app.put('/users/:id', (req, res) => {
  await db.users.update(req.params.id, req.body);  // 😱 Mass assignment!
});
```

### Secure Pattern (ALWAYS DO THIS):
```javascript
// Only allowed fields are extracted
app.put('/users/:id', (req, res) => {
  const { name, email, bio } = req.body;  // Destructure ONLY allowed fields
  const validated = validateSchema(userUpdateSchema, { name, email, bio });
  await db.users.update(req.params.id, validated);
});
```

## GraphQL Depth & Cost Limiting

### Depth Limiting
Maximum query depth of 5-7 prevents exponential data loading:
```graphql
# Depth 1: query { user { ... } }            — OK
# Depth 3: query { user { posts { title } } } — OK
# Depth 7: query { user { posts { comments { user { posts { comments { text } } } } } } } — REJECTED
```

### Cost Analysis Formula
```
Query Cost = Σ (field_weight × estimated_items × nesting_multiplier)
```
Where:
- `scalar field` weight = 1
- `object field` weight = 2
- `connection/list` weight = 5 + (first/last × 1)
- `nesting_multiplier` = 1.5 ^ depth

### Protobuf Validator Chains (gRPC)
```protobuf
message CreateUserRequest {
  string name = 1 [(buf.validate.field).string = {
    min_len: 1,
    max_len: 100,
    pattern: "^[a-zA-Z0-9\\s'-]+$"
  }];
  string email = 2 [(buf.validate.field).string.email = true];
  int32 age = 3 [(buf.validate.field).int32 = {gte: 0, lte: 150}];
}
```
