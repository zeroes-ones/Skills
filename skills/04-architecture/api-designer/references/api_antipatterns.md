# API Anti-Patterns

## 1. Tunneling Everything Through POST
❌ Using POST for queries, updates, and deletes — treating it as a universal method.
✅ Use proper HTTP methods: GET for reads, PUT/PATCH for updates, DELETE for deletes.

## 2. Chatty APIs
❌ Requiring N+1 requests to build a view (fetch user, then orders, then items).
✅ Use expansion/sparse fieldsets: `GET /users/{id}?expand=orders.items`

## 3. Stringly-Typed APIs
❌ All fields as strings: `"price": "19.99"`, `"count": "42"`, `"active": "true"`
✅ Use native JSON types: `"price": 19.99`, `"count": 42`, `"active": true`

## 4. Leaky Abstractions
❌ Exposing internal DB IDs, column names, or ORM relationships in API responses.
✅ Use opaque external IDs, map internal names to consumer-friendly names.

## 5. Inconsistent Error Formats
❌ 400 returns `{"error": "bad"}`, 404 returns `"not found"`, 500 returns HTML.
✅ Standardize error format across all endpoints.

## 6. Missing Idempotency Keys
❌ POST without idempotency — duplicate charges on retry.
✅ Accept `Idempotency-Key` header for POST/PATCH, return cached result on replay.

## 7. Mega-Endpoints
❌ One endpoint that does everything: `POST /api/v1/process` with massive payload.
✅ Resource-oriented endpoints with clear boundaries.

## 8. Ignoring HTTP Semantics
❌ Returning 200 with error body, 500 for validation failures.
✅ Use correct status codes — they're part of the contract.

## 9. No Rate Limiting Feedback
❌ Just returning 429 with no headers — client has no idea when to retry.
✅ Include `Retry-After` and rate limit headers.

## 10. Hard Deletes Only
❌ DELETE permanently removes data with no recovery.
✅ Soft-delete with `deletedAt` timestamp, keep for configurable retention period.

## 11. No Request IDs
❌ Error debugging impossible — no way to correlate client request with server logs.
✅ Generate or accept `X-Request-ID` header.

## 12. Blocking Long Operations
❌ POST starts a 30-second operation, client times out.
✅ Return `202 Accepted` with a status endpoint for polling or webhook for completion.
