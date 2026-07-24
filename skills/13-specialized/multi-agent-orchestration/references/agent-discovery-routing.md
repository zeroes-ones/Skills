# Agent Discovery & Routing

## Discovery Methods

### 1. Chain-Based Discovery
Parse skill frontmatter `chain.consumes_from` to find agents that handle specific domains.
```yaml
chain:
  consumes_from: [system-architect, api-designer]
  feeds_into: [backend-developer, qa-engineer]
```

### 2. Tag-Based Search
Query skill `tags` field for matching specializations.
```yaml
tags: [backend, python, fastapi, database, caching]
```

### 3. Description-Based Matching
Semantic similarity between task description and skill description.

## Routing Rules
1. Exact specialization match → route directly
2. Partial match → route to closest + flag uncertainty
3. No match → decompose task further
4. Multiple matches → select by token_budget fit
5. No agent exists → escalate

## Routing Anti-Patterns
- Routing to wrong specialization (backend task → frontend agent)
- Ignoring token budget (routing 10K-token task to 3K-budget agent)
- Circular routing (A→B, B→A)
