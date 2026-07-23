---
name: backend-developer
description: 'Multi-language backend development with Python/FastAPI, Node.js/Express,
  Go, REST APIs, JWT/OAuth authentication, database integration, caching strategies,
  async task processing, push notification delivery (APNs/FCM), real-time streaming
  (WebSocket/SSE), structured logging, and testing. Trigger: backend, FastAPI,
  Express, Go, JWT, OAuth, caching, async tasks, push notifications, WebSocket, API development.'
author: Sandeep Kumar Penchala
type: development
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- backend-developer
token_budget: 2835
output:
  type: code
  path_hint: ./
chain:
  consumes_from:
  - algorithmic-trader
  - api-designer
  - code-reviewer
  - database-designer
  - documentation-engineer
  - engineering-manager
  - hipaa-technical-implementation
  - idea-to-spec
  - migration-architect
  - monorepo-manager
  - performance-engineer
  - platform-engineer
  - privacy-engineer
  - security-engineer
  - security-reviewer
  - staff-engineer
  - system-architect
  - tdd-guide
  feeds_into:
  - algorithmic-trader
  - api-designer
  - api-test-suite-builder
  - ci-cd-builder
  - clinical-informatics-specialist
  - code-reviewer
  - customer-support-engineer
  - data-engineer
  - database-designer
  - devops-engineer
  - devrel-advocate
  - docker-kubernetes
  - embedded-engineer
  - frontend-developer
  - fullstack-developer
  - hipaa-technical-implementation
  - llm-engineer
  - market-data-engineer
  - mobile-developer
  - monorepo-manager
  - observability-engineer
  - performance-engineer
  - privacy-engineer
  - qa-engineer
  - sales-engineer
  - security-reviewer
  - staff-engineer
  - tdd-guide
  - technical-writer
------
# Backend Developer

Build production-grade backend services with polyglot expertise across Python (FastAPI), Node.js (Express/Fastify), and Go. This is the internal playbook for FAANG-level backend engineering — every section contains concrete, actionable implementation patterns, not generic advice. Covers the full lifecycle: language selection with tradeoff matrices, API design with framework-specific patterns, authentication and authorization (JWT, OAuth 2.0, RBAC), database integration with ORMs and raw SQL, multi-level caching architecture, asynchronous task processing with idempotency guarantees, structured logging with OpenTelemetry tracing, resilience patterns (circuit breakers, retries, graceful degradation), and comprehensive testing.

## Route the Request
<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("package.json", "\"express\"")` OR `file_contains("requirements.txt", "fastapi\|flask\|django")` OR `file_exists("go.mod")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("*.sql", "CREATE TABLE\|ALTER TABLE")` OR `file_contains("prisma/schema.prisma", "model ")` | Invoke **database-designer** instead. You need schema design, not backend code. |
| A3 | `file_contains("docker-compose.yml\|Dockerfile", "nginx\|proxy\|load")` OR `file_exists("terraform/\|.github/workflows/deploy")` | Invoke **devops-engineer** instead. This is infrastructure work. |
| A4 | `file_exists("openapi.yaml\|openapi.json\|swagger.json")` AND `file_contains("*.yaml", "paths:\|/api/")` | Invoke **api-designer** instead. This is API contract work. |
| A5 | `file_exists("jest.config.*\|vitest.config.*\|cypress.config.*")` AND `file_contains("*.test.*", "describe\|it\(")` | Invoke **qa-engineer** instead. This is test strategy work. |
| A6 | `file_contains("package.json", "\"next\"\|\"react\"\|\"vue\"")` AND `file_contains("*.tsx\|*.jsx", "useState\|useEffect\|<template>")` | Invoke **frontend-developer** or **fullstack-developer** instead. |
| A7 | `file_contains("*", "JWT\|OAuth\|passport\|bcrypt\|@nestjs/passport")` | Jump to **Decision Trees** — Authentication Strategy. |
| A8 | `file_contains("*", "redis\|memcached\|cache\|CacheManager")` | Jump to **Decision Trees** — Caching Strategy. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Design a new REST API or GraphQL service → Jump to "Core Workflow" — Phase 1 (API Design)
├── Implement authentication (JWT, OAuth) or RBAC → Go to "Decision Trees" — then Phase 2
├── Optimize database queries or set up caching → Jump to "Decision Trees" — Caching Strategy
├── Handle errors, retries, and resilience patterns → Jump to "Best Practices" — idempotency & resilience
├── Set up a project from scratch → Jump to "Scale Depth" — pick your team size, follow the stack
├── Need system architecture decisions → Invoke system-architect skill instead
├── Need security review of backend → Invoke security-reviewer skill instead
└── Not sure? → Describe the problem in plain language and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else
<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to write code without the data model.** Do not produce a single line of endpoint code until you know the schema, relationships, and query patterns. | Trigger: user asks for API endpoint code AND `grep -rn "schema\|migration\|\.sql" --include="*.ts"` returns 0 results in the repo | STOP. Respond: "I need the data model first. Share your schema (Prisma, SQL, ORM models) or describe the entities and relationships. I won't write API code against an unknown database." |
| **R2** | **REFUSE to let exceptions propagate as raw 500s.** Every external call (database, API, queue, file system) MUST have explicit error handling with status codes, logging, and fallback behavior. | Trigger: generated code contains `fetch(` or `axios(` or `pool.query(` without `try/catch` or `.catch()` in the same function scope | STOP. Insert error boundary before proceeding. Add: `try { ... } catch (err) { logger.error({ err, requestId }, 'External call failed'); return res.status(502).json({ error: 'SERVICE_UNAVAILABLE', requestId }); }` |
| **R3** | **REFUSE to pass request bodies directly to database queries or external services.** Validate types, ranges, formats, sizes, and business rules at the boundary. | Trigger: generated code contains `db.query(req.body.` OR `db.insert(req.body)` OR `sql` with `${req.body` without prior Zod/Joi validation | STOP. Insert validation layer: `const schema = z.object({ ... }); const parsed = schema.safeParse(req.body); if (!parsed.success) return res.status(400).json(...)` |
| **R4** | **REFUSE to make breaking API changes without a deprecation window.** New major version OR migration path required. | Trigger: generated code removes a field from response type OR changes a route signature OR renames a query parameter | STOP. Add deprecation header (`Sunset`, `Deprecation`), keep old behavior for 1 version, document migration path. Breaking changes without deprecation are forbidden. |
| **R5** | **STOP and ASK when critical context is missing.** Do not assume database schema, expected QPS, deployment environment, or auth provider. | Trigger: generating code that references database queries, external services, auth, or deployment configs without explicit confirmation of those details in the conversation | STOP. Ask targeted questions: "What's your database? (Postgres/MySQL/Mongo). What's the expected QPS? What auth provider? (Auth0/Clerk/Proprietary). What's the deployment environment?" |
| **R6** | **DETECT and WARN about missing idempotency on write endpoints.** Every POST/PUT/PATCH/DELETE endpoint that changes state MUST have idempotency protection. | Trigger: generated code creates `router.post(` or `router.put(` or `router.delete(` handler without `Idempotency-Key` header check or `idempotency_key` field | WARN: Add comment `// TODO: Add idempotency key check before processing` and insert skeleton: `const idempotencyKey = req.headers['idempotency-key']; if (!idempotencyKey) return res.status(400).json({ error: 'MISSING_IDEMPOTENCY_KEY' });` |
| **R7** | **DETECT and WARN about external calls without timeouts.** Every HTTP call, database query, or gRPC request MUST have an explicit timeout < 10s. | Trigger: generated code contains `fetch(url)` or `axios(url)` or `grpc.Client()` without `timeout` parameter or `AbortSignal` | WARN: Add `timeout: 5000` or `AbortSignal.timeout(5000)`. External calls without timeouts become cascading failures under load. |

## The Expert's Mindset
<!-- DEEP: 10+min — how masters think, not just what they do -->

### The Mental Model Shift
Competent developers make things work. Masters make things **unbreakable under load.** The shift: stop thinking about code paths and start thinking about failure modes. For every endpoint, ask "what happens when 10,000 requests hit this simultaneously?" The database connection pool, the memory allocator, the garbage collector — these are your real constraints. Code you haven't load-tested is code you haven't finished.

### Cognitive Biases That Kill Backend Systems
| Bias | How It Manifests | Antidote |
|-------|------------------|----------|
| **Premature optimization** | Adding Redis before measuring if Postgres is the bottleneck | Profile first. Optimization without a flame graph is superstition. |
| **Resume-driven development** | Choosing Kafka for a 100 msg/day queue or Kubernetes for a single service | Every infrastructure choice must solve a measured problem. If you can't point to the bottleneck, you don't need the tool. |
| **Abstraction addiction** | Wrapping every database query in a repository pattern "in case we switch databases" | You won't switch databases. Build abstractions around behavior, not storage. One good abstraction beats five premature ones. |

### What Backend Masters Know That Others Don't
- **Connection pool math is deterministic.** `pool_size = (expected_qps × avg_query_ms) / 1000`. If this exceeds your database's max_connections, you have a scaling problem before you write a line of code.
- **Idempotency is not a feature — it's insurance.** Every payment, order, and write endpoint needs an idempotency key. Retries without idempotency = duplicates. Every retry mechanism without idempotency is a bug.
- **Backpressure propagates.** A slow database makes slow APIs makes slow clients makes angry users. Every layer in the stack needs a timeout shorter than the layer above it. The database timeout must be shorter than the API timeout must be shorter than the client timeout.
- **Every refactor must remove dead code — not just reorganize it.** When you touch a module to refactor, actively hunt for unused routes, dead code paths, commented-out blocks, deprecated wrappers, and legacy compatibility shims. A refactor's diff should be net-negative in lines. Dead code left behind is a tax on every future reader.

### When to Break Your Own Rules
- **Skip the abstraction for one-off scripts.** A 50-line migration script doesn't need repository pattern, dependency injection, or a service layer. It needs to run once and be correct.
- **Use raw SQL when the ORM creates N+1 queries.** ORMs optimize for developer convenience, not query efficiency. When you see 500 queries in your logs for a single endpoint, drop to raw SQL. The ORM is a tool, not a religion.

## Operating at Different Levels

The same backend task produces fundamentally different output depending on the practitioner's level. Invoke this skill with your target level (or the level you want to grow toward) to calibrate depth and scope.

| Level | Backend Output Characteristics |
|---|---|
| **L1 — Apprentice** | Step-by-step implementation with explanations. Safe defaults. "Here's the route handler, here's why we use this pattern." |
| **L2 — Practitioner** | Production-ready implementation with tests, error handling, and edge cases covered. Independent execution. |
| **L3 — Senior** | API design with trade-off analysis, data model design, architectural decisions. Decision rationale included. System-level thinking. |
| **L4 — Staff** | API design standards for the org, cross-service patterns, architectural RFCs. "This is how all our services should handle auth/caching/errors." |
| **L5 — Principal** | Novel patterns that change how the industry thinks about backend design. Framework-level contributions. "Here's a new approach to this class of problem." |

**Usage**: Say "as an L3 backend developer, design the API for..." or "give me an L2 implementation of this endpoint" to calibrate the response. If no level is specified, defaults to **L2** (production-ready, independent execution).

## When to Use

- You are building a new REST API or GraphQL service and need to choose the right language and framework
- You need to implement authentication (JWT, OAuth 2.0) and role-based access control (RBAC)
- You are designing a database schema, writing migrations, or optimizing queries for a relational database
- You need to add caching (in-memory, Redis, CDN) to improve API response times
- You are setting up async task processing with background jobs, message queues, and idempotency guarantees
- You need to implement structured logging, distributed tracing (OpenTelemetry), and health check endpoints
- You are preparing a service for production with rate limiting, graceful shutdown, and deployment checklists
- You need to add resilience patterns — circuit breakers, retries with backoff, graceful degradation

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Language & Framework Selection

```
Startup/Small team, rapid prototyping?
├── YES → Python/FastAPI or Node.js/Express
│         Fastest dev speed, largest hiring pool, most libraries
└── NO → Performance-critical? (latency < 10ms, high concurrency)
    ├── YES → Go or Rust
    │         Go: simpler, great concurrency, fast compile
    │         Rust: maximum performance, memory safety, steep learning
    └── NO → Team already skilled in one? → Use what they know

Data-heavy with complex business logic? → Python/FastAPI
Real-time, WebSocket-heavy? → Go or Node.js
Enterprise, Java ecosystem? → Kotlin/Spring Boot
```

### Caching Strategy Decision Tree

```
Data freshness requirement?
├── < 1 second → In-memory cache (application-level, no network)
├── 1-60 seconds → Redis/Memcached (shared, TTL-based)
├── 1-60 minutes → Redis + CDN for static, DB query cache
└── > 1 hour → CDN, precomputed materialized views

Read:write ratio > 100:1? → Aggressive caching, denormalized reads
Read:write ratio < 10:1? → Minimal caching, focus on write performance

**What good looks like:** `curl http://localhost:8000/health` returns `{"status":"ok"}` within 200ms. OpenAPI spec renders at `/docs`. All endpoints respond within p95 < 200ms.

```

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): API Design
1. **Contract-first**: Design OpenAPI 3.1 spec before writing code. Share with frontend/mobile teams.
2. **Endpoints**: Resources (nouns), not actions (verbs). `GET /orders/{id}` not `GET /getOrder`.
3. **Pagination**: Cursor-based for large datasets. `?cursor=xxx&limit=50`. Avoid offset pagination beyond page 10.
4. **Error responses**: Consistent format: `{ "error": { "code": "VALIDATION_ERROR", "message": "...", "details": [...] } }`. Include request ID for tracing.
5. **Versioning**: URL prefix (`/v1/`) or header-based. Avoid query param versioning. Have a deprecation policy.

### Phase 2 (~30 min): Implementation
<!-- DEEP: 10+min -->
1. **Project structure**: Feature-based, not layer-based. `src/orders/` contains routes, service, repository, models together.
2. **Validation**: Validate at boundary (API layer). Use Pydantic (Python), Zod (Node.js), or `go-playground/validator` (Go). Reject invalid data early.
3. **Error handling**: Never expose stack traces. Use error codes. Log full error with context server-side. Return sanitized error to client.
4. **Database access**: Repository pattern. Never expose ORM models directly to API layer. Use Data Transfer Objects (DTOs).
5. **Async tasks**: Offload non-critical work to background jobs. Ensure idempotency (idempotency keys, deduplication).

### Phase 3 (~20 min): Testing
1. **Unit tests**: Business logic, validation, transformations. Mock external dependencies.
2. **Integration tests**: Database, cache, message queue. Use test containers or in-memory alternatives.
3. **Contract tests**: Verify API responses match OpenAPI spec. Catch breaking changes before deploy.
4. **Load tests**: k6 or Locust. Test at 2× expected peak QPS. Find bottlenecks before users do.

### Phase 4 (~15 min): Deployment Readiness
1. **Health checks**: `/health` (liveness — is process alive), `/health/ready` (readiness — can serve traffic). Kubernetes uses both.
2. **Graceful shutdown**: Handle SIGTERM. Stop accepting new requests, drain in-flight requests, close DB connections.
3. **Migrations**: Run before deploy. Backward-compatible changes only. Rollback plan for every migration.
4. **Secrets**: Environment variables for config, secrets manager for credentials. Never in code or config files.

### Phase 5 (~20 min): Real-Time & Streaming

1. **Choose the right protocol**: WebSocket for bidirectional (chat, collaboration), SSE for server→client streaming (dashboards, logs), Polling for simple/legacy clients.

| Factor | WebSocket | SSE | Polling |
|--------|-----------|-----|---------|
| Direction | Bidirectional | Server→Client | Client→Server |
| Connection | Persistent | Persistent | Per-request |
| Reconnect | Manual | Auto (EventSource) | Built-in |
| Binary | Yes | No (text only) | Via HTTP |
| HTTP/2 Friendly | Requires upgrade | Native multiplexing | Native |
| Complexity | Medium | Low | Minimal |
| Backpressure | Manual | Stream-native | N/A |

2. **WebSocket server** — Node.js with `ws`:
```js
const { WebSocketServer } = require('ws');
const wss = new WebSocketServer({ port: 8080 });
const clients = new Map(); // userId → ws

wss.on('connection', (ws, req) => {
  const userId = authenticate(req);
  // Reject duplicate connections from same user
  if (clients.has(userId)) {
    ws.close(4001, 'Duplicate connection');
    return;
  }
  clients.set(userId, ws);
  ws.isAlive = true;

  ws.on('pong', () => { ws.isAlive = true; });
  ws.on('message', (data) => {
    const msg = JSON.parse(data);
    // Route to handler, broadcast, or publish to Redis
  });
  ws.on('close', () => clients.delete(userId));
});

// Heartbeat: terminate dead connections every 30s
const interval = setInterval(() => {
  wss.clients.forEach((ws) => {
    if (!ws.isAlive) return ws.terminate();
    ws.isAlive = false;
    ws.ping();
  });
}, 30000);
wss.on('close', () => clearInterval(interval));
```

3. **FastAPI WebSocket** — Python async:
```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active: dict[str, WebSocket] = {}

    async def connect(self, user_id: str, ws: WebSocket):
        await ws.accept()
        self.active[user_id] = ws

    def disconnect(self, user_id: str):
        self.active.pop(user_id, None)

    async def broadcast(self, message: dict):
        import json
        dead = []
        for uid, ws in self.active.items():
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(uid)
        for uid in dead:
            self.disconnect(uid)

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def ws_endpoint(ws: WebSocket, user_id: str):
    await manager.connect(user_id, ws)
    try:
        while True:
            data = await ws.receive_json()
            await manager.broadcast({"user": user_id, "msg": data})
    except WebSocketDisconnect:
        manager.disconnect(user_id)
```

4. **SSE endpoint** — FastAPI one-way streaming:
```python
from fastapi.responses import StreamingResponse
import asyncio, json

async def event_stream(request):
    while True:
        if await request.is_disconnected():
            break
        data = await get_latest_events()
        # SSE format: "data: <payload>\n\n"
        yield f"data: {json.dumps(data)}\n\n"
        await asyncio.sleep(1)

@app.get("/events/stream")
async def sse_endpoint(request: Request):
    return StreamingResponse(
        event_stream(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # disable nginx buffering
        }
    )
```

5. **Connection pool management** — hard limits prevent memory leaks:
```js
const MAX_CONNECTIONS = 10_000;
const IDLE_TIMEOUT_MS = 5 * 60 * 1000;

wss.on('connection', (ws) => {
  if (wss.clients.size >= MAX_CONNECTIONS) {
    ws.close(1013, 'Server at capacity');
    return;
  }
  ws._idleTimer = setTimeout(() => ws.close(1001, 'Idle timeout'), IDLE_TIMEOUT_MS);
  ws.on('message', () => {
    clearTimeout(ws._idleTimer);
    ws._idleTimer = setTimeout(() => ws.close(1001, 'Idle timeout'), IDLE_TIMEOUT_MS);
  });
});
```

6. **Broadcasting with Redis pub/sub** — scale beyond single process:
```js
const redis = require('redis');
const pub = redis.createClient();
const sub = redis.createClient();

sub.subscribe('room:general', (message) => {
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) client.send(message);
  });
});

// On message from any server instance:
ws.on('message', (data) => {
  pub.publish('room:general', data); // fan-out to all instances
});
```

7. **Reconnection-aware state**: Assign monotonically increasing sequence numbers to each event. Store the last N events (e.g., 1000) in a ring buffer. On reconnect, the client sends `{ lastSeq: 42 }` and the server replays events 43+. For longer disconnections, fall back to a REST endpoint for historical data. Use sticky sessions or a Redis sorted set in multi-instance deployments.

8. **WebSocket health check**: Expose an HTTP endpoint that verifies the WS server is accepting connections:
```python
@app.get("/health/ws")
async def ws_health():
    return {
        "ws_connections": len(manager.active),
        "max_connections": MAX_CONNECTIONS,
        "status": "ok"
    }
```

### Phase 6 (~25 min): Push Notification Delivery

Production push notification infrastructure is a bridge between your backend and Apple/Google push services. A broken push pipeline produces zero user-facing errors — just silently undelivered notifications. This phase implements the server-side delivery with proper error handling, token lifecycle management, and CI-testable verification.

**1. Push notification delivery architecture:**

```
┌──────────┐    ┌──────────────────┐    ┌─────────┐    ┌───────────┐
│ App Code  │──→│ Push Task Queue  │──→│ Provider │──→│ APNs/FCM  │──→ Device
│ notify()  │   │ (Celery/BullMQ)  │   │ Router   │   │           │
└──────────┘    └──────────────────┘    └─────────┘    └───────────┘
                                              │
                    ┌─────────────────────────┘
                    ▼
              ┌──────────┐    ┌──────────────┐
              │ Token DB │←──→│ In-App Store │
              └──────────┘    └──────────────┘
```

- **Push Task Queue**: Decouples user-facing requests from push delivery. A slow APNs response (up to 30s for invalid tokens) must not block your API.
- **Provider Router**: Routes to APNs or FCM based on `platform` field. Handles provider-specific authentication and payload construction.
- **Token DB**: Stores `(user_id, platform, token, is_active, last_updated)`. Tokens are ephemeral — stale token cleanup is critical.
- **In-App Store**: Creates notification record in your database BEFORE push dispatch. A push failure must never lose the notification — users can see it when they open the app.

**2. APNs provider — Python with HTTP/2 + JWT:**

```python
import time, jwt, httpx
from cryptography.hazmat.primitives import serialization

class APNsProvider:
    """Token-based (JWT) APNs provider. One p8 key covers all team apps.
    Certificate-based auth is deprecated — JWT tokens never expire (regenerate hourly)."""

    def __init__(self, key_path: str, key_id: str, team_id: str, topic: str, use_sandbox: bool = False):
        with open(key_path, "rb") as f:
            self._private_key = serialization.load_pem_private_key(f.read(), password=None)
        self._key_id = key_id
        self._team_id = team_id
        self._topic = topic  # Bundle ID, e.g. "com.lantern.app"
        self._base_url = (
            "https://api.sandbox.push.apple.com" if use_sandbox
            else "https://api.push.apple.com"
        )
        self._jwt: tuple[str, float] = ("", 0.0)

    def _generate_jwt(self) -> str:
        now = time.time()
        if not self._jwt[0] or now > self._jwt[1] - 300:
            token = jwt.encode(
                {"iss": self._team_id, "iat": int(now)},
                self._private_key,
                algorithm="ES256",
                headers={"kid": self._key_id},
            )
            self._jwt = (token, now + 3600)
        return self._jwt[0]

    async def send(self, device_token: str, title: str, body: str,
                   badge: int | None = None, sound: str = "default",
                   category: str | None = None, mutable_content: int = 0,
                   data: dict | None = None) -> dict:
        """Send push via APNs HTTP/2. Returns {status, reason, apns_id}."""
        payload = {
            "aps": {
                "alert": {"title": title, "body": body},
                "sound": sound,
                "badge": badge,
                "category": category,
                "mutable-content": mutable_content,
            }
        }
        if data:
            payload["data"] = data

        async with httpx.AsyncClient(http2=True, timeout=30.0) as client:
            response = await client.post(
                f"{self._base_url}/3/device/{device_token}",
                json=payload,
                headers={
                    "authorization": f"bearer {self._generate_jwt()}",
                    "apns-topic": self._topic,
                    "apns-push-type": "alert",
                    "apns-priority": "10" if badge else "5",
                    "apns-expiration": "0",
                },
            )
        result = {"status": response.status_code, "apns_id": response.headers.get("apns-id")}
        if response.status_code == 200:
            return result
        reason = response.json().get("reason", "unknown")
        result["reason"] = reason
        if reason in ("Unregistered", "BadDeviceToken"):
            result["action"] = "delete_token"
        return result
```

**3. FCM provider — Node.js with Firebase Admin SDK:**

```js
const admin = require('firebase-admin');

// Initialize once at startup — loads service account JSON
admin.initializeApp({
  credential: admin.credential.cert(require('./firebase-service-account.json')),
});

class FCMProvider {
  static async send(token, title, body, options = {}) {
    const message = {
      token,
      notification: { title, body },
      android: {
        priority: 'high',
        ttl: (options.ttl || 86400) * 1000,
        notification: {
          channelId: options.channelId || 'default',
          ...(options.collapseKey && { tag: options.collapseKey }),
        },
      },
      apns: {
        payload: {
          aps: { sound: 'default', badge: 1, 'mutable-content': 1 },
        },
      },
      data: options.data || {},
    };

    try {
      const response = await admin.messaging().send(message);
      return { sent: true, messageId: response };
    } catch (error) {
      const code = error.code || '';
      if (code === 'messaging/registration-token-not-registered') {
        return { sent: false, error: code, action: 'delete_token' };
      }
      if (code === 'messaging/invalid-argument') {
        return { sent: false, error: code, action: 'delete_token' };
      }
      if (code === 'messaging/server-unavailable') {
        return { sent: false, error: code, action: 'retry' };
      }
      return { sent: false, error: code, action: 'log_and_continue' };
    }
  }
}
```

**4. Token lifecycle API — Python/FastAPI:**

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/push", tags=["push"])

class TokenRegister(BaseModel):
    token: str = Field(..., min_length=32, max_length=512)
    platform: str = Field(..., pattern="^(ios|android)$")
    previous_token: str | None = Field(None, min_length=32, max_length=512)

@router.post("/register")
async def register_push_token(req: TokenRegister, user=Depends(get_current_user)):
    """Register push token. Called on every app launch."""
    async with db.transaction():
        await db.execute(
            "DELETE FROM push_tokens WHERE token = :token",
            {"token": req.token}
        )
        if req.previous_token:
            await db.execute(
                "UPDATE push_tokens SET is_active = FALSE, updated_at = NOW() "
                "WHERE token = :prev AND user_id = :uid",
                {"prev": req.previous_token, "uid": user.id}
            )
        await db.execute(
            """INSERT INTO push_tokens (user_id, platform, token, is_active, created_at, updated_at)
               VALUES (:uid, :platform, :token, TRUE, NOW(), NOW())
               ON CONFLICT (user_id, platform, token) DO UPDATE
               SET is_active = TRUE, updated_at = NOW()""",
            {"uid": user.id, "platform": req.platform, "token": req.token}
        )
    return {"status": "registered"}
```

**5. Delivery dispatch — Python with Celery task:**

```python
@celery_app.task(bind=True, max_retries=3, default_retry_delay=30, acks_late=True)
def send_push_notification(self, user_id: str, title: str, body: str,
                           data: dict | None = None):
    """Dispatch push to all active devices. In-app notification created FIRST."""
    # Create in-app notification before push (fast DB write)
    create_in_app_notification.delay(user_id, "custom", title, body, data)

    tokens = fetch_active_tokens(user_id)
    if not tokens:
        return {"sent": False, "reason": "no_tokens"}

    sent, failed, deleted = 0, 0, 0
    for token_row in tokens:
        result = None
        if token_row.platform == "ios":
            result = asyncio.run(apns.send(token_row.token, title, body, data=data))
        elif token_row.platform == "android":
            result = FCMProvider.send(token_row.token, title, body, {"data": data})

        if result.get("action") == "delete_token":
            deactivate_token(token_row.token)
            deleted += 1
        elif result.get("action") == "retry":
            failed += 1
        else:
            sent += 1

    return {"sent": sent, "failed": failed, "deleted_tokens": deleted}
```

**6. Delivery monitoring metrics:**

| Metric | Alert Threshold | Why |
|--------|----------------|-----|
| Push delivery rate (`sent / (sent + failed)`) per 5min | < 95% | APNs/FCM auth issue or mass invalidation |
| Token invalidation rate per hour | > 20% | App reinstall spike or token refresh bug |
| APNs 403 rate | > 1% | JWT expired or wrong key |
| Push latency P95 | > 5s | Slow provider or network issue |
| Stale token ratio (>30 days since update) | > 15% | Token cleanup job failing |

**7. CI/CD test endpoint — verify push pipeline:**

```python
@router.post("/test")
async def test_push(user=Depends(get_current_user)):
    """Send silent test notification. Run in CI on every deploy."""
    tokens = await fetch_active_tokens(user.id)
    if not tokens:
        raise HTTPException(400, "No push tokens registered")

    for token_row in tokens:
        if token_row.platform == "ios":
            result = await apns.send_silent(token_row.token, {
                "aps": {"content-available": 1, "category": "test"},
                "data": {"test_id": str(uuid.uuid4()), "timestamp": int(time.time())},
            })
        else:
            result = await fcm.send_data_only(token_row.token, {
                "test_id": str(uuid.uuid4()), "timestamp": int(time.time()),
            })

        if not result.get("sent"):
            raise HTTPException(502, {
                "error": "PUSH_PIPELINE_BROKEN",
                "platform": token_row.platform,
                "reason": result.get("error", "unknown"),
            })

    return {"status": "push_pipeline_healthy", "devices_tested": len(tokens)}
```

**8. Payload design principles:**
- Never put sensitive data in payload — APNs/FCM servers log these. Put only a reference ID in `data`, fetch content from API on notification tap.
- Platform-adaptive: iOS needs `apns-priority`, `apns-push-type`, `mutable-content`; Android needs `android.priority`, `channel_id`, `collapse_key`.
- Collapse keys: Use for state-replacement notifications (like count). Without one, 50 likes = 50 notification cards.
- TTL: Set `apns-expiration: "0"` for time-sensitive notifications. Set longer TTL (1 day) for evergreen content.
- Badge count: iOS uses absolute badge count — backend must track unread count per user.

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **Stack**: Python/FastAPI or Node.js/Express. Fastest path to working API.
- **Database**: SQLite for dev, managed Postgres (Render/Railway free tier) for prod.
- **Deploy**: Single server or PaaS (Railway, Render, Fly.io). Dockerfile + `git push`.
- **Skip**: Kubernetes, microservices, message queues, distributed tracing. All overkill.
- **Coordination**: None. You are the API designer, developer, and reviewer.

### Small Team (2-10 people, 100-10K users)
- **Add**: CI/CD pipeline (GitHub Actions), structured logging, basic monitoring (health checks + error alerts).
- **Database**: Managed Postgres with connection pooling (PgBouncer). Redis for caching and sessions.
- **API**: OpenAPI spec as contract between frontend and backend. API versioning policy.
- **Queue**: Redis or SQS for async tasks. Keep simple — one queue, one worker.
- **Skip**: Kubernetes (use PaaS or docker-compose), multi-service architecture, event sourcing.

### Medium Team (10-50 people, 10K-1M users)
- **Add**: Distributed tracing (OpenTelemetry), metrics dashboard (Grafana), SLO-based alerting.
- **Architecture**: Modular monolith or 2-3 services around clear bounded contexts.
- **Database**: Read replicas for read-heavy endpoints. Connection pooling per service.
- **Queue**: Dedicated message broker (RabbitMQ, SQS). Dead letter queues for failed jobs.
- **Testing**: Contract tests in CI. Load tests before major releases.

### Enterprise (50+ people, 1M+ users)
- **Architecture**: Microservices or service-oriented. Event-driven where appropriate.
- **Database**: Multi-region with sharding. Dedicated DBRE (Database Reliability Engineer).
- **Security**: API gateway with rate limiting, WAF, regular penetration testing.
- **Compliance**: SOC 2, GDPR, PCI DSS controls implemented. Audit logging everywhere.
- **Coordination**: Cross-team API governance. Shared infrastructure team.

### Transition Triggers
- Solo → Small: You're the bottleneck. Hire backend dev #2.
- Small → Medium: P95 latency > 200ms sustained. DB CPU > 60%. Team can't ship independently.
- Medium → Enterprise: 3+ teams need to coordinate per deploy. Compliance mandates separation of concerns.

## What Good Looks Like

> Every endpoint is contract-first, validated at the boundary, and fully documented. Authentication is airtight — JWTs validated, RBAC enforced, secrets never leaked. The database hums with connection pooling, indexed queries, and targeted caching that keeps p95 latency under 200ms. Async tasks are idempotent, retried with exponential backoff, and monitored via dead-letter queues. Structured logs carry correlation IDs from ingress to response, and health checks report green before users notice anything wrong. The service ships with confidence — migrations are backward-compatible, rollback plans are tested, and load tests pass at 2× peak QPS.

### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | api-designer | OpenAPI specs, error models, pagination conventions, auth patterns |
| **This** | backend-developer | Implementation: routes, validation, business logic, database access, caching, async tasks |
| **After** | code-reviewer | Reviews code quality, security vulnerabilities, error handling completeness |

Common chains:
- **API to production**: api-designer → backend-developer → code-reviewer — API contract drives implementation, code review ensures quality before merge
- **Schema to service**: database-designer → backend-developer → qa-engineer — Schema defines data model, backend builds the service layer, QA validates behavior

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `api-design` | New service, new endpoint | Phase 1 |
| `auth-implementation` | Login, permissions, API keys | Decision Trees |
| `database-integration` | Schema design, queries, migrations | `database-designer` skill |
| `caching-strategy` | Performance optimization, scaling reads | Decision Trees |
| `async-processing` | Background jobs, webhooks, notifications | Phase 2 |
| `testing-strategy` | Test pyramid, contract testing | Phase 3 |
| `performance-tuning` | Latency issues, throughput bottlenecks | `performance-engineer` skill |
| `containerization` | Docker, deployment | Phase 4 |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **API contract first**: Design the API before writing code. Share with consumers. Use OpenAPI.
- **Fail fast, fail loud**: Validate at boundaries. Invalid data should never reach business logic.
- **Idempotency for mutations**: Every POST/PUT/PATCH that affects state should be idempotent via idempotency keys.
- **Observability from day one**: Structured logging (JSON), request IDs on every log line, health checks.
- **Database per service** (if microservices): Never share databases across services. API is the contract.
- **Connection pooling**: Always pool database connections. Set statement timeout and idle-in-transaction timeout.
- **Migrate forward, rollback tested**: Every migration has a tested reversal. Expand-contract for zero-downtime schema changes.

## Anti-Patterns
<!-- DEEP: 5min -- each anti-pattern includes machine-detectable patterns -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| Using long polling for real-time features (chat, live dashboards) | Use WebSocket for bidirectional or SSE for server→client. Polling 10K clients every 1s = 10K req/s for no data. WebSocket/SSE push only when there is data. | `grep -rn "setInterval\|setTimeout" --include="*.ts" --include="*.js" \| grep -i "fetch\|axios\|http"`  → finds polling loops making HTTP calls | eslint `no-restricted-globals: ["error", {name: "setInterval", message: "Use WebSocket/SSE for real-time. Polling does not scale."}]` |
| Storing WebSocket connections in a global array without cleanup | Use a `Map` keyed by user ID. Remove on `close` event. Add heartbeat-based zombie detection every 30s. Monitor connection count in health checks. | `grep -rn "connections\.push\|clients\.push\|sockets\[\]" --include="*.ts" --include="*.js"`  → finds global arrays that grow unbounded | eslint `no-restricted-syntax: [{selector: "AssignmentExpression[left.property.name='push'][right.callee.object.name=/connections\|clients\|sockets/]", message: "Use Map with cleanup, not unbounded arrays."}]` |
| Returning raw stack traces in API error responses | Return sanitized errors: `{ "error": { "code": "DB_CONNECTION_FAILED", "message": "Service temporarily unavailable", "request_id": "abc-123" } }`. Log the full stack trace server-side with the same request ID. | `grep -rn "res\.send(err\|res\.json(error\|\.stack" --include="*.ts" --include="*.js"`  → finds raw error objects sent to clients | eslint `no-restricted-syntax: [{selector: "CallExpression[callee.property.name='json'][arguments.0.property.name='stack']", message: "Never expose stack traces to clients."}]` |
| Opening a DB transaction, making an external API call, then committing | Fetch external data first, then open the transaction. An open transaction holds locks and blocks other queries — a 5s external call inside a transaction can stall the entire connection pool. | `grep -rn "transaction\|beginTransaction" --include="*.ts" --include="*.js" -A 20 \| grep -E "fetch\|axios\|http\.\|request\("`  → finds HTTP calls within transaction blocks | eslint custom rule: `no-async-in-transaction` — detect `await fetch()` or `await axios()` between `transaction()` and `commit()` |
| Sharing a single database across multiple services | Each service owns its data. Services communicate via API, never by reading each other's tables. Shared databases create tight coupling and make every schema change a cross-team negotiation. | `grep -rn "DATABASE_URL\|DB_HOST" --include="*.env*" \| sort \| uniq -c \| awk '$1 > 1'`  → finds same database URL used in multiple services | Pre-commit hook: `scripts/check-db-isolation.sh` — fails if `DATABASE_URL` is identical across service directories |
| Hardcoding secrets, API keys, or connection strings in source code | Use environment variables for config (non-sensitive), a secrets manager (AWS Secrets Manager, HashiCorp Vault) for credentials. Scan code in CI for secret patterns before merge. | `grep -rn "api_key\|API_KEY\|secret\|password\|token\s*=\s*['\"][a-zA-Z0-9_-]{8,}" --include="*.ts" --include="*.js" --include="*.py"`  → finds hardcoded credential patterns | GitGuardian / `detect-secrets` in pre-commit hook. CI: `trufflehog filesystem . --json --fail` in pipeline |
| Skipping idempotency on payment/order endpoints — retries create duplicates | Add idempotency keys: client generates a UUID in `Idempotency-Key` header. Server stores key → response mapping. On retry with same key, return cached response. Use a DB unique constraint as the safety net. | `grep -rn "router\.(post\|put\|patch\|delete)" --include="*.ts" --include="*.js" -A 10 \| grep -v "idempotency\|Idempotency-Key\|idempotency_key"`  → finds write endpoints with no idempotency header check | Package: `express-idempotency-middleware` or `fastapi-idempotency`. CI lint: fail if `POST/PUT/PATCH/DELETE` route handler doesn't reference `idempotency` within 20 lines |

## Error Decoder
<!-- DEEP: 5min -- each entry includes a console-string matcher for automatic recovery loops -->

| 🖥️ Console Match (grep pattern) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|---|---|---|---|---|
| `Error: authMiddleware not applied\|401 Unauthorized on public endpoint` + `grep -rn "app.use.*Router\|router\." src/` shows routes registered before `app.use(authMiddleware)` | User A could see User B's private messages in production | Auth middleware was applied AFTER the route handler — `app.use('/api/messages', messagesRouter)` was placed before `app.use(authMiddleware)` in the Express setup | Reorder middleware: auth before routes. Add integration tests that test every endpoint (a) authenticated, (b) unauthenticated, (c) wrong-user scenarios. Implement auth middleware as a global filter unless explicitly excluded | 1. Grep route registration order: `grep -n "app.use\|router\." src/index.ts` 2. Verify auth middleware appears before any route middleware 3. Run: `curl -s http://localhost:${PORT}/api/messages \| jq .status` — must return 401, not 200 |
| `Error: invalid byte sequence\|ERROR: invalid input syntax\|Mojibake detected in column` + `grep -rn "req\.body\." src/` shows direct body access without validation | Silent data corruption: user profiles showed scrambled names for 2 months | Input validation accepted arbitrary Unicode and control characters. A REST endpoint stored user input directly without sanitization, corrupting the database | Add server-side validation with Pydantic/Zod: reject control characters, enforce character sets per field. Implement input sanitization at the boundary. Backfill and repair corrupted data with a migration | 1. Find all `req.body` accesses without prior validation: `grep -rn "req\.body\." src/ -B 5 \| grep -v "validate\|zod\|joi"` 2. Add Zod schema or Joi validation before each 3. Test: `curl -X POST -d '{"name":"test\x00\x1f"}'` → must return 400 |
| `Error: timeout\|ETIMEDOUT\|query took [0-9]{5,}ms` + `grep -rn "\.findAll\|\.query\|\.execute" src/ -A 3` shows ORM calls in loops | Dashboard page took 45 seconds to load — timed out and showed an error | API endpoint for dashboard fired 2,300 individual SQL queries (N+1): loaded users, then looped over each to load orders, then looped over each order to load line items | Use eager loading or batch queries. Add N+1 detection. Result: 3 queries, 120ms | 1. Enable query logging: `SQLALCHEMY_ECHO=True` or `log_queries=true` 2. Count queries per request: wrap handler with counter 3. Assert: `expect(queryCount).toBeLessThan(5)` in integration test 4. Add CI gate: `jest --testNamePattern="query-count"` |
| `Error: getaddrinfo\|ECONNREFUSED\|ETIMEDOUT\|socket hang up` + no `timeout` in request config | External API call blocked the request handler for 30 seconds, causing server-wide thread pool exhaustion | An endpoint called an external API with no timeout configured — when the external service was slow, the thread hung until the default OS timeout (30s on Linux) | Add explicit timeouts on ALL external calls: `httpx.Timeout(5.0)`, `axios({ timeout: 5000 })`. Implement circuit breaker for external dependencies. Use async I/O | 1. Grep for HTTP calls without timeout: `grep -rn "fetch(\|axios(\|request(" src/ -A 5 \| grep -v "timeout"` 2. Add `timeout: 5000` to every call 3. Install circuit breaker: `npm install opossum` 4. Test: `tc qdisc add dev eth0 root netem delay 10000ms` → system must degrade gracefully |
| `Error: DELETE.*archive\|ERROR: permission denied for table\|FATAL: terminating connection` + `grep -rn "\.destroy\|\.remove\|\.delete" src/` finds multiple delete paths | `DELETE /api/users` was a soft delete, but support team accidentally called `DELETE /api/users/archive` — 1,200 user records permanently lost | The API had two separate delete endpoints with confusing names — no idempotency, no confirmation for destructive operations | Consolidate to a single `DELETE` endpoint with a `hard` query parameter. Add confirmation prompts for destructive operations in admin UI. Lock down destructive operations behind a separate auth role | 1. Audit all delete paths: `grep -rn "\.destroy\|\.delete\|\.remove\|DROP\|TRUNCATE" src/` 2. Require `hard=true` query param for irreversible deletes 3. Guard with role check: `requireRole('admin')` 4. Log every destructive operation with user ID and timestamp |
| `FATAL ERROR: CALL_AND_RETRY_LAST Allocation failed - JavaScript heap out of memory` + `grep -rn "new WebSocket\|new ws\.\|ws\.on" src/ -c` shows connection count rising over time | 10K WebSocket connections, server OOM-killed at 2GB RSS within 90 minutes | No max connection limit was configured. Each ws connection held a buffer and file descriptor — unbounded growth consumed all available memory until the OOM killer terminated the process | Set `MAX_CONNECTIONS` (e.g., 10,000). Add idle timeout (5 min) that terminates inactive sockets. Monitor `process.memoryUsage()` and alert if RSS exceeds 80% of container limit | 1. Add: `server.maxConnections = 10000` 2. Add heartbeat: `ws.on('pong', () => ws.isAlive = true)` with 30s interval 3. Monitor: `setInterval(() => { if(process.memoryUsage().rss > 0.8*limit) server.close() }, 5000)` 4. Add `--max-old-space-size` to Node flags |
| `nginx 502 Bad Gateway` + `grep "proxy_read_timeout" nginx.conf` shows 60s or less | SSE endpoint caused nginx 502 after exactly 60 seconds — every client disconnected and reconnected on a loop | Proxy timeout defaulted to 60s. nginx `proxy_read_timeout` terminated the SSE stream because no data frame arrived within the timeout window. `EventSource` auto-reconnected, masking the issue | Send SSE keepalive comments every 15s: `: heartbeat\n\n`. Set `proxy_read_timeout 300s;`. Disable response buffering. Add `X-Accel-Buffering: no` response header | 1. Add heartbeat: `setInterval(() => res.write(': heartbeat\n\n'), 15000)` 2. nginx: `proxy_read_timeout 300s; proxy_buffering off;` 3. Test: `curl -N -H "Accept: text/event-stream" http://localhost/events` → must stay connected > 60s 4. Response header: `res.setHeader('X-Accel-Buffering', 'no')` |
| `Error: ECONNRESET\|socket hang up\|health check failed` + `grep -rn "forEach.*\.send\|for.*\.send\|\.clients.*forEach" src/` finds synchronous broadcast loops | Fan-out broadcast to 50K clients caused 30-second latency spikes — WebSocket event loop blocked and health checks started failing | Synchronous broadcast iterating all 50K connections in a single tick: `wss.clients.forEach(c => c.send(data))`. The Node.js event loop is single-threaded — a 500ms broadcast blocks all other request handlers | Shard connections across worker processes (1 per CPU core). Use Redis pub/sub: publish once per channel, each worker sends only to its subset. Batch broadcasts. For one-way flows, use SSE | 1. Refactor: `redis.publish('events', JSON.stringify(data))` instead of `forEach.send()` 2. Each worker subscribes: `redis.subscribe('events')` and sends to its shard only 3. Batch: collect events for 50ms, send once 4. Test: `autocannon -c 5000 -d 60` → health check must stay green |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->
<!-- Run: `bash scripts/checklist-backend.sh` for automated pass/fail on all items. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | API documented with OpenAPI 3.1 spec — shared with consumers, validated in CI | `npx @redocly/cli lint openapi.yaml --format=stylish` → must return 0 | CI: `redocly lint` in `.github/workflows/api-lint.yml` |
| **[S2]** | Authentication and authorization implemented — JWT validated, RBAC enforced, secrets managed | `grep -rn "auth\|jwt\|rbac\|passport" src/ --include="*.ts" --include="*.js"`  → must match > 0 files | — |
| **[S3]** | Input validation on all endpoints — server-side, not client-side only | `grep -rn "validate\|zod\|joi\|yup\|class-validator" src/ --include="*.ts" --include="*.js"`  → must find validation at every POST/PUT handler | ESLint: `no-restricted-imports` — forbid `req.body` direct access outside validation middleware |
| **[S4]** | Error responses consistent format with request IDs for tracing | `grep -rn "request_id\|requestId\|correlationId" src/ --include="*.ts" --include="*.js"`  → must match in error handler | Template: copy `templates/error-response.ts` into `src/middleware/error-handler.ts` |
| **[S5]** | Database migrations versioned and backward-compatible with rollback plan | `npx prisma migrate status` OR `npx knex migrate:list` → must show all applied, no pending | CI check: `prisma migrate deploy --preview-feature` in dry-run mode |
| **[S6]** | Health checks: liveness (`/health`) and readiness (`/health/ready`) endpoints | `curl -s http://localhost:${PORT}/health \| jq .status` → must return `"ok"` | Copy `templates/health-check.ts` into `src/routes/health.ts` |
| **[S7]** | Structured logging with correlation IDs propagated across services | `grep -rn "pino\|winston\|bunyan\|structuredClone\|JSON.stringify" src/ --include="*.ts" --include="*.js"`  → must match logger initialization | — |
| **[S8]** | Graceful shutdown handling SIGTERM with connection draining | `grep -rn "SIGTERM\|SIGINT\|graceful\|server.close" src/ --include="*.ts" --include="*.js"`  → must match signal handler | Copy `templates/graceful-shutdown.ts` into `src/server.ts` |
| **[S9]** | Rate limiting and throttling on public endpoints | `grep -rn "rate.limit\|rateLimit\|express-rate-limit\|throttle" src/ --include="*.ts" --include="*.js"`  → must match middleware setup | `npm install express-rate-limit` + copy `templates/rate-limit.ts` |
| **[S10]** | Integration tests on database, cache, and external service interactions | `npx jest --testPathPattern="integration\|\.integration\." --passWithNoTests` (or vitest equivalent) → must find and pass integration tests | CI: `jest --testPathPattern=integration` in pipeline |
| **[S11]** | Load tested at 2× expected peak QPS before production launch | `npx autocannon -c 100 -d 30 http://localhost:${PORT}/api/health` → P99 latency must be < 100ms at 2× peak QPS | `npm install --save-dev autocannon` + script: `scripts/load-test.sh` |
| **[S12]** | Monitoring: error rate, P95 latency, throughput, DB connection pool, queue depth | `grep -rn "prometheus\|datadog\|newrelic\|opentelemetry\|metrics" package.json`  → must find monitoring SDK | `npm install prom-client` + copy `templates/metrics.ts` |

## Footguns
<!-- DEEP: 10+min — war stories from production backend systems -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| Connection pool exhaustion cascading across services — 502s everywhere at 9:47 AM when a marketing email went out | Traffic spiked 10× from a campaign. Each request opened a DB connection, ran a query, and held the connection for 800ms while rendering a template. The pool (default: 10 connections in many ORMs) saturated instantly. All services sharing the pool returned 502. Recovery took 22 minutes while marketing pulled the email. | Default connection pool size in SQLAlchemy is 5, in HikariCP is 10, in node-postgres is 10. No one changed the defaults. Template rendering happened INSIDE the transaction, doubling connection hold time. | **Size your pool to peak, not average.** Formula: `pool_size = (peak_qps × p95_query_ms) / 1000 × 1.5`. For 500 QPS with 50ms queries: (500 × 50) / 1000 × 1.5 = 37.5 → set pool to 40. Move template rendering and I/O OUTSIDE the transaction. Set `pool_timeout` to fail fast (3s) instead of blocking indefinitely. |
| N+1 query went undetected for 9 months because "the dashboard loaded fine on my machine" with 12 records — production had 15,000 | GET /api/orders returned 100ms in dev. In production, with 15,000 orders and 3 nested relationships (customer, items, shipments), it issued 45,001 queries and timed out at 30s. The endpoint was never tested with realistic data volumes OR ORM query logging enabled. | ORMs like Django ORM, Rails ActiveRecord, and Hibernate silently issue lazy queries when you access relations in a loop or template. `order.customer.name` inside `{% for %}` = 1 query per iteration. | **Always enable query logging in development** (`SQLALCHEMY_ECHO=True`, `config.active_record.verbose_query_logs = true`). Use `select_related` / `prefetch_related` / `eagerloading`. Add a test that asserts query count: `assert len(captured_queries) <= 3` for any endpoint. Set a CI check that fails if any endpoint exceeds N queries. |
| Deployed a "backward-compatible" database migration that locked the `users` table for 37 minutes during business hours | The migration `ALTER TABLE users ADD COLUMN last_login_at TIMESTAMP DEFAULT NOW()` looked harmless. But PostgreSQL's `ADD COLUMN ... DEFAULT` on a table with 8M rows rewrites every row to fill the default value. The `users` table was locked for writes (including logins) for 37 minutes. | In PostgreSQL < 11, `ADD COLUMN ... DEFAULT` rewrites the entire table. In 11+, it's instant for non-volatile defaults. The team was on Postgres 10.6 — nobody checked the version before running the migration. | **Always check your migration's lock behavior.** Use `SELECT pg_stat_activity` to check for lock-waiting queries. Split into: (1) `ADD COLUMN last_login_at TIMESTAMP` (instant, nullable), (2) backfill in batches, (3) `ALTER COLUMN SET DEFAULT`. Test migrations on a production-sized anonymized database, not a dev database with 50 rows. |
| Retried a payment webhook without idempotency — charged the customer 7 times for $499 each | Payment provider sent a webhook, the handler processed it but returned 500 due to a downstream logging error. The provider retried 6 times at exponential intervals. Each retry processed the payment again because the handler didn't check for duplicate transaction IDs. Customer's bank flagged it as fraud and blocked the merchant account. | The webhook handler used `POST /api/payments` which creates a new payment every time — no idempotency check on `idempotency_key` or `provider_transaction_id`. The 500 was from a logging service timeout, not payment processing failure. | **Every payment/order/write endpoint needs an idempotency key.** Store `(idempotency_key, response)` in a database. On receipt: check if key exists → if yes, return stored response. If no, process and store. Set a TTL (24h). Add a unique constraint on `(provider_transaction_id)` at the database level. Test retry scenarios explicitly: fire the same webhook 3 times and verify exactly 1 payment. |
| Added Redis cache, 99.7% hit rate, served 50% stale data for 2 weeks because TTL was 24 hours — nobody noticed until a customer called support | To speed up a product catalog endpoint, the team added Redis caching with `EXPIRE 86400`. The inventory update service wrote to PostgreSQL but not Redis. Products showed "in stock" for 24 hours after selling out. Customers ordered products that didn't exist. | Cache invalidation was never wired up. The team assumed "data doesn't change that often" — but inventory changes every time someone buys. The 24h TTL was copied from a blog post about static content caching. | **Cache invalidation is the hard part, not caching.** Write-through: update cache on every write. Write-behind: invalidate cache on write so next read repopulates. Or use a shorter TTL that reflects actual data volatility (product inventory: 30s, not 24h). Add a "cache age" header to responses and monitor staleness as a metric. **The only thing worse than no cache is a cache that lies.** |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can build an endpoint but don't know what happens when 10,000 users hit it simultaneously | You load-test your endpoints before deployment and can name the bottleneck (DB query, serialization, connection pool) from the flame graph | You design a system architecture and 6 months later, it handles 10× the original traffic with no major rewrites |
| You use `try/catch` but don't differentiate between retryable errors (network timeout) and non-retryable errors (validation failure) | You implement circuit breakers, retry with exponential backoff + jitter, and graceful degradation for every external dependency | You can look at a production incident and identify whether the fix needs to be in the code, the infrastructure, or the architecture — and you're right |
| You copy-paste error handling patterns without understanding why one endpoint returns 400 vs 409 vs 422 | You have a consistent error response format with unique error codes that the frontend team can programmatically handle | You define org-wide error handling standards and the teams that adopt them see 40% fewer P1 incidents |

**The Litmus Test:** Can you write a production service from scratch — routing, middleware, error handling, connection pooling, health checks, graceful shutdown — using only the standard library and a database driver? If you need a framework to get started, you're not L3 yet.

## Deliberate Practice
<!-- DEEP: 10+min — how to improve, not just what to do -->

### The Backend Improvement Loop
1. **Profile under load** — Run `wrk` or `k6` at 2× expected peak QPS. Find the slowest endpoint.
2. **Flame graph the bottleneck** — Is it a missing index? N+1 query? Serialization overhead?
3. **Fix one thing** — Optimize the single biggest bottleneck. Re-profile. Did it move?
4. **Repeat monthly** — Systems degrade. Last month's profile is not this month's reality.

### Practice Routines
| Skill Level | Practice | Frequency | Expected Result |
|-------------|----------|-----------|-----------------|
| Novice → Competent | Build the same API in 3 different frameworks; compare ergonomics, performance, error handling | Monthly | Can articulate when to use FastAPI vs Express vs Go based on actual data |
| Competent → Expert | Design a system for 1000 QPS, then 10,000, then 100,000. Find the breaking point of your architecture | Quarterly | Can identify the bottleneck before writing code |
| Expert → Master | Contribute a performance fix to an open-source framework you use. Read 1000 lines of its source code | Quarterly | Understands why the framework works, not just how to use it |

### The One Thing
**Write a production service from scratch with zero frameworks every 6 months.** No FastAPI. No Express. Just the standard library and a database driver. You'll learn what your frameworks actually do, what abstractions are worth the cost, and where the real complexity lives. Framework fluency ≠ backend mastery.

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [12 Factor App](https://12factor.net/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)
- [OpenTelemetry](https://opentelemetry.io/docs/)
- [The Pragmatic Programmer](https://pragprog.com/titles/tpp20/) — Andy Hunt & Dave Thomas
- [Designing Data-Intensive Applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/) — Martin Kleppmann

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `api-designer` | OpenAPI 3.1 spec, auth scheme, rate limits, error codes, pagination conventions | Before implementing any endpoint; contract-first development |
| `database-designer` | ERD, schema DDL, indexing strategy, migration scripts, query performance baselines | Before implementing data access layer; schema changes |
| `system-architect` | Service boundaries, technology stack decisions, inter-service contracts, deployment topology | Before choosing framework/language or defining service boundaries |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `frontend-developer` | OpenAPI spec, type-safe SDK, error response formats, pagination conventions | Frontend builds against wrong API shapes — costly rework |
| `fullstack-developer` | API implementation, type definitions, validation schemas, middleware behavior | Fullstack features blocked on backend availability |
| `devops-engineer` | Resource requirements (CPU/memory), health check endpoints, migration steps, build commands | Infrastructure can't be provisioned or CI/CD can't be configured |
| `qa-engineer` | Test data requirements, API test scenarios, mock service endpoints, error response patterns | QA can't author integration tests without API implementation |
| `security-reviewer` | Auth implementation details, data classification, dependency inventory, API surface | Security review can't assess implementation without understanding the code |
| `mobile-developer` | API implementation with mobile-specific concerns (rate limiting, push notification payloads) | Mobile client development blocked on backend availability |

### Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| API breaking change (field removal, type change) | Frontend, Mobile, Fullstack | Coordinated migration to avoid production errors |
| Database migration with locking/downtime | DevOps, CI/CD Builder, QA | Deploy sequencing, test environment updates |
| New external service dependency | Security Engineer, DevOps | Security review, network egress rules, secrets setup |
| Auth flow change (token format, session behavior) | Security Engineer, Frontend, Mobile | Auth integration testing across all clients |
| Performance degradation discovered | Observability Engineer, DevOps | Metrics review, incident readiness |

### Escalation Path

```
Blocked by infrastructure? → DevOps Engineer → Cloud Architect
Auth/security concern? → Security Engineer → Compliance Officer
Data contract dispute? → System Architect → CTO Advisor
Cross-team dependency blocking? → System Architect → Project Manager
```

## Proactive Triggers

| Trigger | Response |
|---------|----------|
| "WebSocket connections dropping after every deploy" | Implement connection draining: on SIGTERM, stop accepting new WebSocket connections (`server.close()` in ws), send close frames (code 1001) to existing clients with a `Retry-After` header equivalent, and wait for in-flight messages to complete before process exit. Add a readiness probe that returns 503 while draining so the load balancer stops routing new traffic. |
| "SSE clients getting 502 after exactly 60 seconds" | Proxy timeout is killing the stream. Configure `proxy_read_timeout 300s;` in nginx or increase the ALB idle timeout to 120s+. Send SSE keepalive comments (`: heartbeat\n\n`) every 15–30 seconds to prevent idle connection drops. Disable response buffering with `proxy_buffering off;` and set the `X-Accel-Buffering: no` response header from the application. |
| "Memory leak in production — WebSocket connections growing unbounded over days" | Set `MAX_CONNECTIONS` cap at server startup. Add idle timeout (5 min) that terminates inactive connections after two missed heartbeats. Implement per-user connection deduplication — reject new connections from the same user if one already exists. Monitor `wss.clients.size` in health checks and alert on growth trends. |
| "Broadcast to 50K connections causes event loop lag and request timeouts" | Shard connections across multiple processes/instances (1 per CPU core). Use Redis pub/sub for cross-instance fan-out. Batch broadcasts: accumulate 50ms of events, send once instead of per-message. Consider SSE instead of WebSocket for one-way broadcasts — lower overhead per connection, no per-frame ACK overhead. |
| "Client reconnects after 30s disconnect and misses events — data loss" | Assign monotonically increasing sequence numbers to each broadcast event. Store the last N events (e.g., 1,000) in a ring buffer per connection/channel. On reconnect, client sends `{ lastSeq: 42 }` and server replays events 43+. For disconnects longer than the ring buffer, fall back to a REST endpoint for historical data. |
| "WebSocket upgrade fails with 426/400 behind a proxy or load balancer" | Ensure the proxy forwards WebSocket upgrade headers. In nginx: `proxy_set_header Upgrade $http_upgrade;` and `proxy_set_header Connection "upgrade";`. In AWS ALB: the listener protocol must be HTTP/HTTPS (not HTTP/2, which doesn't support protocol upgrade). Verify the backend route matches the WebSocket path exactly. |
| "Zombie connections — server thinks 5K clients are connected, only 2K are actually reachable" | Implement application-level ping/pong heartbeat (30s interval, 2 missed pongs = terminate). TCP keepalive defaults to 2+ hours — always do application-level heartbeats. On the client side, use `EventSource` auto-reconnect (SSE) or implement exponential backoff reconnection with jitter (WebSocket). |
| "Fan-out broadcast storm — one incoming event triggers cascading broadcasts that amplify" | Rate-limit broadcasts per room/channel (e.g., max 10/sec). Use a debounce pattern: if the same event type fires within 100ms, coalesce into one broadcast. Attach a `broadcastId` UUID to each message and deduplicate at the receiving end. Never broadcast raw upstream events without sanitizing/aggregating first. |

