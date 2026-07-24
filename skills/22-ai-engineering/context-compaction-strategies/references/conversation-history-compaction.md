# Conversation History Compaction

## Compaction Levels

### Level 1: Light (Turns 5-15)
Keep full last 3 turns, summarize turns 1-remaining.
```
Turn 1-2: [Summary: User asked for architecture design. 
Agent proposed microservices with 3 services. 
Decision: Microservices accepted. Constraint: Must use AWS.]
Turn 3: Agent designed data model...
Turn 4: Agent created API spec...
Turn 5: [CURRENT — full context preserved]
```

### Level 2: Moderate (Turns 15-30)
Keep full last 5 turns, bullet-point summary of earlier.
```
History (Turns 1-10):
• Architecture: Microservices (3 services) on AWS ECS
• Data: PostgreSQL RDS, Redis ElastiCache
• API: REST with JWT auth, rate limiting at gateway
• Decisions: 5 ADRs recorded (see state ledger)
• Errors: 2 resolved (CORS config, DB connection pool)
```

### Level 3: Deep (Turns 30+)
Keep full last 5 turns, structured state only for earlier.
```json
{"phase": "implementation", "decisions": [1,2,3,4,5],
 "artifacts": ["src/auth.py", "src/api.py", "tests/"],
 "constraints": ["AWS-only", "JWT-auth", "PG-RDS"],
 "errors_resolved": 2, "errors_open": 0}
```
