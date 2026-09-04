# How WebSockets Work — Realtime Transport Explained

> Original explainer for interview prep and learning. [research-source: title-only]

## What it is

WebSockets is a full-duplex, message-based protocol over a single TCP connection, upgraded from an HTTP request via the `Upgrade: websocket` handshake. After the handshake both client and server can push messages at any time — no polling, no repeated HTTP round-trips. It's the standard answer for chat, live dashboards, notifications, collaborative editing, and games.

## The lifecycle (know it precisely)

1. **HTTP handshake** — client sends `GET` with `Upgrade: websocket`, `Connection: Upgrade`, `Sec-WebSocket-Key`. Server replies `101 Switching Protocols` with `Sec-WebSocket-Accept`. (HTTP/2 and later HTTP/3 have their own extended CONNECT/WebTransport paths.)
2. **Frames** — after upgrade, messages travel as frames (text/binary), each optionally fragmented.
3. **Heartbeat/ping-pong** — protocol-level pings keep the connection alive and detect dead peers through proxies.
4. **Close** — either side sends a close frame; TCP tears down.

## Why not just HTTP polling?

| Option | Cost | Use when |
|---|---|---|
| **Polling** | Request per update; latency = interval | Low-frequency, simple |
| **Long polling** | Holds a request until data; still one-directional, reconnect-heavy | Older fallback |
| **SSE (Server-Sent Events)** | One-way server→client over HTTP; auto-reconnect built in; text only | Notifications, feeds (server push only) |
| **WebSockets** | Full-duplex; single connection; binary+text | Chat, presence, live collab, games |

Interview line: "if the server only pushes to the client, SSE is simpler and HTTP-friendly; WebSockets earns its complexity when the client must also push (chat, presence) or you need binary/low-latency both ways."

## Server architecture — the scaling crux

A WebSocket server holds **long-lived connections**, which changes the scaling model vs stateless HTTP:

- **State lives in the connection** — you can't round-robin an established socket to another instance; the client must reconnect, or you need a **connection registry**.
- **Horizontal scaling:** a gateway/LB must be **sticky or L4** for WebSockets; then instances share state via a **pub/sub backbone** (Redis pub/sub, Kafka, or a message bus) so "user A's message" reaches whichever instance holds user B's socket.
- **Connection registry + pub/sub** is the canonical pattern: instance 1 receives A's message, publishes "to B", the bus fans out, instance 2 (holding B) pushes it. This is exactly why chat systems look like "WebSocket gateway + Redis/Kafka" in every design.
- **Limits:** file descriptors per node, memory per connection, and idle connections through proxies (timeouts) — heartbeat and reconnection are mandatory.

## Reconnection & reliability (what interviewers dig into)

- Expect disconnects (mobile, proxies, deploys). Design a **reconnect with backoff** and **resume** (session id / last-seen sequence) so the client doesn't lose the middle of a conversation.
- **Ordering + gap detection:** if messages carry a per-conversation sequence number, the client detects gaps on resume and requests missing messages.
- **Deploys:** draining — stop accepting, let in-flight finish, push "reconnecting" to clients. Rolling restarts must not drop everyone at once.
- **Backpressure:** a slow client shouldn't buffer unboundedly in memory; cap send buffers and disconnect/reconnect the laggard.

## Security notes (brief, cross-ref security skills)

- WSS (TLS) is non-negotiable outside localhost.
- **Origin checking** on the handshake prevents cross-site WebSocket hijacking.
- Auth at handshake (cookie/token), then authorize *messages* per event.
- Validate and rate-limit incoming messages; a WebSocket is not a free pipe for abuse.

## Interview answer skeleton

"WebSockets upgrades an HTTP request to a full-duplex connection over TCP. The scaling problem is that connections are stateful, so I keep a connection registry and share events through a pub/sub backbone — any instance can reach the one holding the target socket. Clients reconnect with backoff and resume from a sequence number, and I send pings to detect dead peers."

## Anti-patterns

- ❌ WebSockets for one-way server push — SSE is simpler and HTTP-native.
- ❌ Round-robin L7 load balancing over WebSocket instances without stickiness or a registry.
- ❌ No heartbeat → half-open connections leak resources and "ghost" users stay online.
- ❌ No reconnect/resume → every deploy or blip drops conversation state.
- ❌ Unbounded send buffers on slow clients → memory exhaustion.

## Deliberate-practice drills

1. **Handshake drill:** write out the exact upgrade request/response headers.
2. **Scaling drill:** 1M concurrent chat users across 50 instances — draw the gateway + registry + pub/sub flow for a direct message.
3. **Resume drill:** design the sequence-numbered resume protocol for a chat app after a mobile network blip.
4. **Comparison drill:** polling vs long-polling vs SSE vs WebSockets for a live crypto-price ticker — pick and justify.
5. **Failure drill:** a node dies mid-conversation; walk reconnect → registry lookup → resume with no lost messages.

## References
- See also: message-queues.md (this repo)
- `event-driven-architect` SKILL.md — realtime patterns, pub/sub
- `backend-developer` SKILL.md — realtime service implementation
- `secure-api-design` SKILL.md — auth at handshake/message level
