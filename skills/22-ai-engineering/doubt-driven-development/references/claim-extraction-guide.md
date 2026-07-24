# Claim Extraction Guide

## What Is a Claim?

A claim is any assertion the code makes about its behavior, its data, its timing, its security
posture, or its correctness. Claims are not opinions about code quality — they are falsifiable
statements that can be tested. Every line of code that makes a decision IS a claim.

## Claim Taxonomy

| Claim Type | Example | Falsification Test |
|---|---|---|
| **Behavior** | "This function returns sorted results" | Send unsorted input; verify output order |
| **Invariant** | "This value is never null here" | Inject null via reflection, mock, or edge input |
| **Security** | "Only authenticated users reach this handler" | Send request without auth; check middleware chain |
| **Timing** | "This operation completes within 100ms" | Load test with 10x expected volume |
| **Data integrity** | "This migration is idempotent" | Run migration twice; verify no duplicate side effects |
| **Concurrency** | "This counter is thread-safe" | Run 100 concurrent increments; verify final count |
| **Error handling** | "All errors are logged before propagation" | Trigger each error path; grep logs for error evidence |
| **API contract** | "Returns 404 when resource not found" | Request non-existent resource; verify status code |

## Extraction Heuristics by Language

### Python
```python
# Claim: db.query() returns empty list, not None, when no rows match
results = db.query("SELECT * FROM users WHERE id = ?", user_id)
if results:  # CLAIM: results is falsy only when empty; None would also be falsy here
```

### TypeScript/JavaScript
```typescript
// Claim: req.user is always populated after this middleware
// Extraction: grep for route handlers that don't use this middleware
app.use(authMiddleware);         // CLAIM: applied globally
app.get('/public', handler);     // CLAIM: /public is exempt from auth
```

### Go
```go
// Claim: err is always nil when result is non-nil
result, err := service.Fetch(id)
if err != nil {                  // CLAIM: error and result are mutually exclusive
    return err
}
```

### Java
```java
// Claim: @Transactional ensures rollback on any RuntimeException
@Transactional                  // CLAIM: all exceptions inside propagate correctly
public void transfer(Account from, Account to, BigDecimal amount) {
```

## Common Claim Blind Spots

### 1. The Implicit Else
When code handles a condition without an explicit else, the DEFAULT behavior is a claim.
```
if (user.isAdmin()) { grantAccess(); }
// CLAIM: non-admin users get no access (not even read)
// CLAIM: null/undefined user is handled before reaching this code
```

### 2. The Assumed Atomicity
Multi-step operations without explicit transaction boundaries.
```
deductFrom(from, amount);  // Step 1
creditTo(to, amount);      // Step 2 — CLAIM: Step 1 always succeeds before Step 2
```

### 3. The Missing Timeout
Network calls, DB queries, or external service calls without explicit timeouts.
```
fetch('https://api.partner.com/data')
// CLAIM: the partner API always responds (no timeout → infinite wait possible)
```

### 4. The Serialization Assumption
Objects passed across process boundaries without explicit serialization contract.
```
cache.set(key, complexObject);
// CLAIM: complexObject is serializable (no circular refs, no functions, no Symbols)
```

### 5. The Environment Parity Claim
```
if (process.env.NODE_ENV === 'production') { enableRateLimiting(); }
// CLAIM: rate limiting is ONLY needed in production (staging can be DDoS'd)
// CLAIM: NODE_ENV is always set to exactly 'production' in prod
```

## Extraction Protocol

For each file in the diff:
1. Identify every branching point (if/else, switch, ternary, try/catch, guard clause)
2. At each branch, ask: "What does this code ASSUME about the state before this point?"
3. For every function call with > 0 arguments, ask: "What does this code ASSUME about the return value?"
4. For every async operation, ask: "What does this code ASSUME about ordering, timing, and failure?"
5. Label each claim: `CLAIM-NNN: [type] [one-sentence assertion] @ [file:line]`
