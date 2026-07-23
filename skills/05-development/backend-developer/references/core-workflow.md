# Core Workflow — Full Implementation

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
