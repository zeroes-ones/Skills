# Monolith Decomposition Patterns

Decomposing a monolith into multiple repositories is one of the highest-risk architectural transformations. Follow these patterns to minimize blast radius.

## Decomposition Strategies

### 1. Strangler Fig Pattern (Recommended)
Incrementally extract capabilities behind a routing layer. The monolith shrinks as services grow.

```
Phase 1: Route /auth/* → new auth service
Phase 2: Route /billing/* → new billing service
Phase 3: Route /users/* → new user service
Phase 4: Monolith handles only legacy routes → archive
```

### 2. Vertical Slice (Domain-Driven)
Extract by bounded context. Each slice includes its own data, API, and UI.

```
Monolith:
  com.example.monolith.user.*
  com.example.monolith.billing.*
  com.example.monolith.reporting.*

After:
  user-service/     → com.example.user.* + user_db
  billing-service/  → com.example.billing.* + billing_db
  reporting-service/ → com.example.reporting.* + reporting_db (read-only from others)
```

### 3. Data-First Extraction
Extract the data layer first, then the service logic.

```
Step 1: Create new DB schema in target service
Step 2: Dual-write: monolith writes to both old and new DB
Step 3: Backfill historical data
Step 4: Switch reads to new service
Step 5: Remove old DB tables from monolith
```

## Pre-Decomposition Checklist

Before extracting any service, answer these questions:

- [ ] **Data ownership**: Who owns the data after extraction? No shared databases.
- [ ] **API contract**: Is the service boundary defined in Protobuf/OpenAPI?
- [ ] **Authentication**: How does the new service authenticate with others?
- [ ] **Observability**: Are metrics, logs, and traces standardized across services?
- [ ] **CI/CD**: Does the new repo have a pipeline before extraction?
- [ ] **Rollback**: Can you revert the extraction without data loss?
- [ ] **Feature flags**: Can you toggle between monolith and new service at runtime?

## Common Pitfalls

### Distributed Monolith
Symptom: Services share a database. Changing one service's schema breaks another's queries.
Fix: Each service owns its database. Use API calls (not direct DB access) for cross-service data.

### Premature Extraction
Symptom: Extracted service has 2 endpoints and 0 independent value.
Fix: Wait until a bounded context has clear boundaries and > 5 distinct operations.

### Sync Dependencies
Symptom: Service A calls Service B synchronously for every request, creating a chain: A→B→C→D.
Fix: Use async messaging (Kafka, NATS, SQS) for non-critical data flows. Only sync for read-your-writes guarantees.

## Success Metrics

Track these during decomposition:
- **Extraction velocity**: Services extracted per quarter
- **Incident rate**: Incidents attributed to extraction work
- **Latency p99**: Did extracting a service degrade end-to-end latency?
- **Team autonomy**: Can the owning team deploy independently?
- **Monolith shrinkage**: LOC/endpoints remaining in monolith
