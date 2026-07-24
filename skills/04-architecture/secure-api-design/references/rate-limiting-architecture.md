# Rate Limiting Architecture — Reference

## Algorithm Comparison

| Algorithm | Behavior | Best For | Limitation |
|-----------|----------|----------|------------|
| Token Bucket | Tokens refill at steady rate; bucket capacity allows bursts | APIs with bursty traffic patterns | Requires tuning burst size |
| Sliding Window Log | Track timestamp of each request; count in sliding window | Accurate rate enforcement | Higher memory usage (stores timestamps) |
| Sliding Window Counter | Approximate sliding window using weighted previous window | Balance of accuracy and memory | Slightly less accurate at window boundaries |
| Leaky Bucket | Requests queue; processed at fixed rate (FIFO) | Smoothing bursty traffic, queues | Introduces latency for queued requests |
| Fixed Window | Simple counter per time window; resets at window boundary | Simplest implementation | "Stampede" at window boundary (double rate) |

## Distributed Rate Limiting with Redis (Token Bucket)

```lua
-- Lua script for atomic rate limit check in Redis
-- KEYS[1]: rate limit key (e.g., "ratelimit:tier0:user123:minute")
-- ARGV[1]: max requests allowed
-- ARGV[2]: window size in seconds

local current = redis.call('GET', KEYS[1])
if current and tonumber(current) >= tonumber(ARGV[1]) then
    return 0  -- Rate limited
end
redis.call('INCR', KEYS[1])
if tonumber(current or 0) == 0 then
    redis.call('EXPIRE', KEYS[1], ARGV[2])
end
return 1  -- Allowed
```

### Rate Limit Key Composition
```
Format: ratelimit:{tier}:{identifier}:{window_size}
Examples:
  ratelimit:tier0:user_abc123:minute     — Auth endpoint, per-user, 1-minute window
  ratelimit:tier1:user_abc123:minute     — Sensitive endpoints, per-user
  ratelimit:tier2:ip_192.168.1.1:minute  — Standard endpoints, per-IP
```

## Endpoint Tier Definitions

| Tier | Endpoints | Limit (per user) | Limit (per IP) | Rationale |
|------|-----------|-----------------|----------------|-----------|
| 0 — Auth | /login, /token, /mfa, /password-reset | 3 req/min | 20 req/min | Highest-value target; credential stuffing, brute force, enumeration |
| 1 — Sensitive | /users/*, /admin/*, /billing/*, /api-keys | 60 req/min | — | Access to PII, admin functions, financial data |
| 2 — Standard | CRUD operations, search, filters | 300 req/min | — | Normal API usage |
| 3 — Public | GET /products, GET /catalog, health checks | — | 1000 req/min | Anonymous access, cacheable content |

## GraphQL Cost Analysis Formula

```
Cost = Σ for each field in query:
  field_base_cost × max(1, estimated_items) × (1.5 ^ depth)

Where:
  scalar field (String, Int, Boolean) = 1 point
  object field (nested type) = 2 points
  connection/list field = 5 points + (first/last argument × 1 point per item)
  estimated_items = first/last argument value, or default 100 if not specified
  depth = nesting level of the field (root = 0)

Example: query { user { posts(first: 50) { title, comments(first: 10) { text } } } }
  user: 2 × 1 × 1.5^0 = 2
  posts: 5 + 50 × 1.5^1 = 82.5
  title: 1 × 50 × 1.5^1 = 75
  comments: 5 + 10 × 1.5^2 = 27.5
  text: 1 × 10 × 50 × 1.5^2 = 1125  ← explosive growth!
  Total: ~1312 — likely over threshold
```

## gRPC Flow Control

```go
// Server-side gRPC configuration
var opts = []grpc.ServerOption{
    grpc.MaxConcurrentStreams(100),          // Max concurrent streams per connection
    grpc.MaxRecvMsgSize(4 * 1024 * 1024),    // 4MB max received message
    grpc.MaxSendMsgSize(4 * 1024 * 1024),    // 4MB max sent message
    grpc.KeepaliveParams(keepalive.ServerParameters{
        MaxConnectionIdle:     15 * time.Minute,
        MaxConnectionAge:      1 * time.Hour,
        MaxConnectionAgeGrace: 30 * time.Second,
        Time:                  5 * time.Minute,  // Ping if idle for 5 min
        Timeout:               20 * time.Second, // Wait 20s for ping ack
    }),
}
```

## Response Headers (RFC 6585)

When rate limiting, always include these headers:
```
X-RateLimit-Limit: 60         # Max requests in window
X-RateLimit-Remaining: 42     # Requests remaining
X-RateLimit-Reset: 1620000000 # Unix timestamp when window resets
Retry-After: 30               # Seconds to wait (only on 429)
```

HTTP Status: **429 Too Many Requests** (not 403, not 503)
