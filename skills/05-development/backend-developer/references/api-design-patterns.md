# API Design Patterns

> **Author:** Sandeep Kumar Penchala

Production-grade REST API design patterns covering resource modeling, versioning, idempotency, rate limiting, authentication, long-running operations, and bulk endpoints. These patterns align with the backend-developer skill's contract-first API design philosophy.

## REST Design Fundamentals

### Resource Naming Conventions

```
# Resources as plural nouns — never verbs
GET    /orders              # List orders
POST   /orders              # Create order
GET    /orders/{id}         # Retrieve order
PUT    /orders/{id}         # Replace order (full update)
PATCH  /orders/{id}         # Partial update
DELETE /orders/{id}         # Delete order

# Sub-resources — max 2 levels deep
GET    /orders/{id}/items          # Items belong to an order
GET    /orders/{id}/items/{itemId} # Specific item

# Action endpoints (only when no resource fits)
POST   /orders/{id}/cancel        # Cancel is an action, not a resource
POST   /orders/{id}/fulfill       # Same pattern for other actions
```

### Nesting Rules

```
✅ ALLOWED:  /users/{id}/orders         (orders always belong to a user)
✅ ALLOWED:  /orders/{id}/items         (items always belong to an order)
❌ AVOID:    /users/{id}/orders/{id}/items/{id}/discounts  (too deep)
```

### Pagination

| Strategy | Pros | Cons | When to Use |
|----------|------|------|-------------|
| Cursor-based (`?cursor=abc&limit=50`) | Stable across mutations, efficient DB queries | Harder for "jump to page N" UI | Large/real-time datasets, feeds |
| Offset-based (`?offset=100&limit=50`) | Easy "page N" UX | Inconsistent when rows inserted/deleted | Small datasets, admin UIs |
| Keyset pagination (`?after_id=42&limit=50`) | Fastest for indexed columns | Requires sortable unique column | Time-series, append-only data |

```json
// Cursor-based response envelope
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTIzfQ==",
    "has_more": true,
    "total_estimate": 12500
  }
}
```

### Filtering, Sorting, Search

```
GET /orders?status=shipped&created_after=2026-01-01          # Equality + range
GET /orders?status=shipped,processing                        # Multi-value (comma)
GET /orders?sort=-created_at,+total                          # Sort: -desc, +asc
GET /orders?q=customer:john+product:widget                   # Field-scoped search
GET /orders?fields=id,total,status                           # Sparse fieldsets
```

### Error Format (RFC 7807 — Problem Details)

```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Failed",
  "status": 422,
  "detail": "The request body contains invalid fields.",
  "instance": "/orders",
  "request_id": "req_abc123",
  "errors": [
    { "field": "email", "message": "Must be a valid email address", "code": "INVALID_FORMAT" },
    { "field": "items[2].quantity", "message": "Must be at least 1", "code": "MIN_VALUE" }
  ]
}
```

## API Versioning

| Strategy | Example | Pros | Cons |
|----------|---------|------|------|
| URL path | `/v1/orders` | Simplest, visible in logs | URL pollution, cache fragmentation |
| Header | `X-API-Version: 2026-01` | Clean URLs, flexible | Hidden, harder to test in browser |
| Accept header | `Accept: application/vnd.api+json;version=1` | RESTful, content negotiation | Very complex, poor DX |

### Deprecation Policy

```http
# Sunset header — tell clients when this version goes away
HTTP/1.1 200 OK
Sunset: Sat, 01 Mar 2026 00:00:00 GMT
Deprecation: true
Link: </v2/orders>; rel="successor-version"
```

```
Timeline: Announce (3mo before) → Warn in response headers (1mo) → Remove
```

## Idempotency Patterns

Idempotency ensures retrying a request doesn't produce duplicate side effects. Critical for payment, order creation, and any financial operation.

```python
# FastAPI idempotency middleware
from fastapi import FastAPI, Request, HTTPException
import redis, uuid, json

app = FastAPI()
store = redis.Redis(decode_responses=True)

@app.middleware("http")
async def idempotency_middleware(request: Request, call_next):
    if request.method in ("POST", "PUT", "PATCH", "DELETE"):
        idempotency_key = request.headers.get("Idempotency-Key")
        if not idempotency_key:
            raise HTTPException(400, detail="Idempotency-Key header required for mutating requests")

        # Check if we've seen this key before
        cached = store.get(f"idem:{idempotency_key}")
        if cached:
            return JSONResponse(content=json.loads(cached), status_code=200)

        response = await call_next(request)
        # Cache the successful response for 24 hours
        body = b"".join([chunk async for chunk in response.body_iterator])
        store.setex(f"idem:{idempotency_key}", 86400, json.dumps({
            "status": response.status_code,
            "body": json.loads(body)
        }))
        return JSONResponse(content=json.loads(body), status_code=response.status_code)
    return await call_next(request)
```

### Client Usage

```bash
KEY=$(uuidgen)
curl -X POST https://api.example.com/orders \
  -H "Idempotency-Key: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"items": [...]}'
# Retry with the SAME key — server returns cached result, no duplicate order
```

## Rate Limiting

### Algorithm Comparison

| Algorithm | Memory | Accuracy | Burst Handling | Best For |
|-----------|--------|----------|---------------|----------|
| Token Bucket | O(1) per client | Good | Allows bursts | API rate limiting |
| Sliding Window Log | O(N) per client | Perfect | Precise | Strict enforcement |
| Sliding Window Counter | O(1) per client | ~1% error | Good | Production default |
| Leaky Bucket | O(1) per client | Good | Smooths traffic | Upstream protection |
| Fixed Window | O(1) per client | Poor at boundaries | Prone to spikes | Simple use cases |

### Redis Sliding Window Implementation

```python
import time, redis

r = redis.Redis()

def is_rate_limited(client_id: str, limit: int, window_secs: int) -> bool:
    """Sliding window rate limiter with Redis sorted sets."""
    now = time.time()
    window_start = now - window_secs
    key = f"ratelimit:{client_id}"

    pipe = r.pipeline()
    pipe.zremrangebyscore(key, 0, window_start)  # Remove old entries
    pipe.zcard(key)                                 # Count current
    pipe.zadd(key, {str(now): now})                 # Add current request
    pipe.expire(key, window_secs)                   # Auto-expire
    _, count, _, _ = pipe.execute()

    return count > limit
```

### Response Headers

```http
RateLimit-Limit: 100
RateLimit-Remaining: 73
RateLimit-Reset: 1690000000
Retry-After: 15
```

## Authentication Patterns

### JWT Access + Refresh Token Rotation

```
Access Token:  Short-lived (15 min), sent in Authorization header
Refresh Token: Long-lived (7 days), httpOnly cookie, single use with rotation
```

```python
# Token rotation on refresh
def refresh_tokens(refresh_token: str):
    payload = verify_refresh_token(refresh_token)
    # Invalidate the used refresh token (prevent replay)
    invalidate_refresh_token(refresh_token)
    # Issue new pair
    new_access = create_access_token(payload["sub"])
    new_refresh = create_refresh_token(payload["sub"])
    return {"access_token": new_access, "refresh_token": new_refresh}
```

### OAuth2 Flow Selection

```
SPA / Mobile App → Authorization Code + PKCE (no client secret)
Server-to-Server → Client Credentials
Third-party Integration → Authorization Code (with refresh)
Machine-to-Machine → Client Credentials + mTLS
```

## Long-Running Operations

```python
# POST /reports — returns 202 Accepted immediately
@app.post("/reports")
async def create_report(request: ReportRequest):
    job_id = str(uuid.uuid4())
    await task_queue.enqueue("generate_report", job_id, request.dict())
    return JSONResponse(
        status_code=202,
        content={"job_id": job_id, "status": "pending"},
        headers={"Location": f"/jobs/{job_id}"}
    )

# GET /jobs/{id} — poll for completion
@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    job = await job_store.get(job_id)
    return {
        "job_id": job_id,
        "status": job.status,         # pending | processing | completed | failed
        "progress": job.progress,      # 0-100
        "result_url": f"/reports/{job.result_id}" if job.status == "completed" else None,
        "estimated_completion": job.eta
    }
```

### Webhook Notification Alternative

```python
# Register a webhook so clients don't need to poll
@app.post("/webhooks")
async def register_webhook(body: WebhookRegistration):
    await webhook_store.register(body.callback_url, body.events)
    # When job completes, POST to callback_url with job result
```

## Bulk Operations

```python
# POST /orders/bulk — create multiple orders atomically or partially
@app.post("/orders/bulk")
async def bulk_create_orders(requests: list[OrderRequest]):
    results = []
    for i, req in enumerate(requests):
        try:
            order = await order_service.create(req)
            results.append({"index": i, "status": "created", "id": order.id})
        except ValidationError as e:
            results.append({"index": i, "status": "failed", "errors": e.details()})
    # Return 200 with per-item status (not 201 — not all succeeded)
    return {
        "total": len(requests),
        "succeeded": sum(1 for r in results if r["status"] == "created"),
        "failed": sum(1 for r in results if r["status"] == "failed"),
        "results": results,
    }
```

### Consistency Guarantees

| Guarantee | Implementation | Tradeoff |
|-----------|---------------|----------|
| All-or-nothing | Wrap in DB transaction | May fail entirely; large batches timeout |
| Best-effort (partial) | Process individually, report results | Some succeed, some fail — client handles |
| Idempotent chunks | Split into N chunks, each idempotent | Client retries failed chunks |

## Cross-Cutting Concerns Cheat Sheet

```python
# FastAPI middleware stack order (outside-in)
# 1. Request ID injection (generates or extracts X-Request-ID)
# 2. Structured logging (binds request_id to every log line)
# 3. Rate limiting (check before spending server resources)
# 4. Authentication (extract and validate JWT/API key)
# 5. Authorization (RBAC/ABAC check)
# 6. Input validation (Pydantic/Zod models at boundary)
# 7. Business logic (your service layer)
# 8. Response serialization (ORM → DTO → JSON)
# 9. Error formatting (catch-all → RFC 7807)
```

These API design patterns implement the backend-developer skill's Phase 1 (API Design) principles: contract-first development, consistent error responses, proper pagination, and idempotency for all mutations.
