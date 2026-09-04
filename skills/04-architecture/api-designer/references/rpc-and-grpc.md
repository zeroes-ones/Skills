# How RPC Actually Works — Remote Calls Demystified

> Original explainer for interview prep and learning. [research-source: title-only]

## What RPC is

Remote Procedure Call lets a program call a function that runs on another machine as if it were local: `client.charge(order)` compiles into a network round trip. The promise is transparency; the reality is that the network is not transparent — which is exactly what RPC frameworks must help you manage.

## The anatomy of an RPC call (what actually happens)

1. **Stub (client)** — you call a generated local function; the stub serializes arguments.
2. **Serialization** — encode the call into bytes (protobuf, Thrift, JSON, msgpack…). This is the "contract" — both sides must agree on the schema.
3. **Transport** — send over the network (TCP, HTTP/2, QUIC). gRPC uses HTTP/2; classic RPC used custom TCP protocols.
4. **Server stub** — deserializes, dispatches to the actual implementation.
5. **Execution + response** — the server runs the function, serializes the result (or an error), and returns it.
6. **Client un-marshals** — your local call returns (or throws a remote exception).

Every step can fail in ways a local call can't: timeout, partial write, duplicate delivery, server crash mid-call, version mismatch between client and server stubs.

## Interface Definition Language (IDL) — the contract

gRPC/Thrift/Connect use an IDL (`proto3`, `.thrift`). The IDL generates stubs on both sides, so client and server **cannot silently disagree** on types — a compile-time contract. This is RPC's superpower vs ad-hoc JSON: schema evolution is governed by explicit rules (in proto3: additive field changes are backward compatible; removing/renumbering fields is breaking).

## RPC vs REST (pick the honest answer)

| Aspect | REST | RPC (gRPC) |
|---|---|---|
| Mental model | Resources + verbs (HTTP semantics) | Function calls / service methods |
| Contract | OpenAPI (often looser) | IDL, strongly typed, codegen |
| Transport | HTTP/1.1+ | HTTP/2 (multiplexed, binary) |
| Streaming | SSE/WebSocket bolted on | Native (client/server/bidi streams) |
| Performance | Higher overhead per call | Binary, low latency, connection reuse |
| Ecosystem | Browsers, caches, every language | Internal services, polyglot servers |
| Best fit | Public/web APIs | Service-to-service, real-time, high-throughput |

The sensible default: **REST/gRPC outside is often REST for external clients + gRPC for internal services** — you get typed, fast, streaming internal calls and browser-friendly external APIs.

## The hard parts interviewers care about

- **Failure semantics:** a network error is ambiguous — did the server execute or not? This is why RPC needs **idempotency** (see idempotency.md) and **timeouts/deadlines** propagated across the call graph.
- **Deadlines & cancellation:** gRPC propagates deadlines so a slow upstream doesn't hang the whole chain; cancellation should release resources end to end.
- **Retries:** retry only idempotent methods; add jitter; cap retries (retry storms).
- **Versioning/evolution:** follow IDL compatibility rules; never renumber fields; run old+new briefly during rollout.
- **Load & connection management:** HTTP/2 multiplexes many calls over one connection; watch connection churn, use keepalive, and balance per-subchannel.
- **Observability:** every RPC should carry a trace/correlation ID; measure per-method latency, error rate, and p99.

## Interview answer skeleton

"RPC makes a remote function call look local: a generated stub serializes the call, sends it over a transport like HTTP/2, and the server's stub dispatches it. The contract lives in an IDL so both sides are type-safe. The hard part is that the network isn't transparent — so I add deadlines, retries only on idempotent methods, schema-evolution rules, and per-method tracing. Internally I'd use gRPC for typed, streaming, low-latency calls and keep REST for external clients."

## Anti-patterns

- ❌ Treating RPC like a local call — no timeouts, no failure handling ("it's just a function").
- ❌ Retrying non-idempotent methods on timeout (double side effects).
- ❌ Breaking proto compatibility by renumbering/removing fields.
- ❌ Deep synchronous call chains (A→B→C→D) with no deadlines — one slow leaf stalls everything.
- ❌ No per-method metrics — you can't tell which service is slow.

## Deliberate-practice drills

1. **Anatomy drill:** trace one gRPC call end-to-end and name each failure point where a local call has no equivalent.
2. **IDL drill:** write a proto change that is backward compatible and one that is breaking; justify.
3. **Deadline drill:** A calls B calls C with 500ms client deadline — allocate deadlines per hop and handle cancellation.
4. **Comparison drill:** gRPC vs REST for a real-time collaborative editor's internal and external surfaces.
5. **Failure drill:** "server executed but the client timed out" — design the retry + idempotency that makes it safe.

## References
- See also: idempotency.md, api-design-best-practices.md (this repo)
- `api-designer` SKILL.md — gRPC design, error modeling
- `networking-engineer` SKILL.md — HTTP/2, transport
- `backend-developer` SKILL.md — service implementation patterns
