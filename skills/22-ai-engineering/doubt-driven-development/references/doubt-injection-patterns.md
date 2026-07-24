# Doubt Injection Patterns

## Catalog of Adversarial Doubt Patterns

Each pattern is a structured way to challenge a claim. Use the template:
`"Claim [X] would be WRONG if [condition]. Test: [concrete check]."`

---

## Security Patterns

### P1: Missing Authentication Check
**Doubt:** "Claim that only authenticated users reach this handler would be WRONG if a
middleware ordering bug allows unauthenticated requests to bypass auth."
**Test:** `curl -H "Authorization: " https://api/target-endpoint` — expect 401, not 200.

### P2: Token Validation Gap
**Doubt:** "Claim that invalid tokens are rejected would be WRONG if the JWT library
throws instead of returning null, and there's no try/catch around verification."
**Test:** `grep -n "try\|catch" auth.js` — if 0 results near jwt.verify, claim fails.

### P3: Secret in Logs
**Doubt:** "Claim that secrets are never logged would be WRONG if an error path
serializes the full request object including Authorization header."
**Test:** Trigger each error handler; `grep -i "bearer\|authorization" logs/*` — expect 0.

### P4: Injection via Interpolation
**Doubt:** "Claim that user input is sanitized would be WRONG if the sanitizer runs
before URL-decoding, allowing encoded injection payloads."
**Test:** Send `%3Cscript%3E` — if decoded AFTER sanitization, injection succeeds.

---

## Concurrency Patterns

### P5: Read-Modify-Write Race
**Doubt:** "Claim that inventory count is accurate would be WRONG if two concurrent
requests read count=5, both decrement to 4, and write back — losing one decrement."
**Test:** Run 10 concurrent decrements from count=10; `SELECT count FROM inventory` — expect 0.

### P6: Check-Then-Act TOCTOU
**Doubt:** "Claim that resource availability check prevents over-allocation would be
WRONG if the check and allocation are not atomic."
**Test:** Two simultaneous requests for the last available slot; verify only one succeeds.

### P7: Distributed Lock Drift
**Doubt:** "Claim that distributed lock prevents concurrent execution would be WRONG if
clock skew between nodes causes lock TTL to expire early."
**Test:** Set system clock on Node A forward by lock TTL + 1s; verify Node B cannot acquire lock.

---

## Data Integrity Patterns

### P8: Null vs Empty Confusion
**Doubt:** "Claim that empty result means 'not found' would be WRONG if the ORM returns
null for missing rows and [] for empty result — and the code only checks truthiness."
**Test:** `grep -n "if.*results\|if.*rows"` — verify explicit null check, not just truthiness.

### P9: Truncation Without Warning
**Doubt:** "Claim that data fits in the column would be WRONG if the database silently
truncates VARCHAR(255) instead of throwing, and input can exceed 255 chars."
**Test:** Insert 300-char string; `SELECT LENGTH(col)` — verify it's 300, not 255.

### P10: Idempotency Assumption
**Doubt:** "Claim that retrying a failed operation is safe would be WRONG if the first
attempt partially succeeded (e.g., payment charged but order not created)."
**Test:** Simulate network error after payment but before order creation; retry — verify no double charge.

---

## Error Handling Patterns

### P11: Swallowed Exception
**Doubt:** "Claim that all errors are handled would be WRONG if a catch block logs and
returns a default value, masking a data corruption signal."
**Test:** `grep -n "catch.*{"` — for each, verify the error is either propagated or escalated.

### P12: Finally Block Side Effect
**Doubt:** "Claim that resources are always released would be WRONG if the finally block
itself throws, suppressing the original error and leaving resources open."
**Test:** `grep -n "finally"` — verify no throwable operations in finally blocks.

---

## Performance Patterns

### P13: N+1 Query Under Load
**Doubt:** "Claim that this endpoint responds within 200ms would be WRONG if the ORM
lazy-loads a relation inside a loop, causing N+1 queries at scale."
**Test:** Enable query logging; call endpoint with N=100 related entities; count queries.

### P14: Unbounded Collection
**Doubt:** "Claim that memory usage is bounded would be WRONG if a query without LIMIT
loads all rows into memory before pagination."
**Test:** `grep -n "\.findAll\|SELECT.*FROM.*WHERE"` — verify LIMIT/OFFSET or cursor-based pagination.

---

## Pattern Application Template

```
PATTERN: [P#] [Name]
APPLIED_TO: [CLAIM-ID]
DOUBT: "Claim [ID] would be WRONG if [specific condition from pattern]."
TEST: [concrete command or code that verifies the condition]
RESULT: [PASS (claim holds) | FAIL (claim broken) — with evidence]
SEVERITY: [CRITICAL|HIGH|MEDIUM|LOW]
```
