# How Service Discovery Works — Finding Services in a Dynamic World

> Original explainer for interview prep and learning. [research-source: title-only]

## The problem

In a dynamic system, service instances come and go: autoscaling adds nodes, deploys replace instances, failures remove them. Hard-coded addresses break instantly. Service discovery answers: **"which healthy instances of service B can service A call right now?"**

## Two halves of discovery

1. **Registration** — an instance announces "I exist at ip:port, healthy, with these tags" when it starts, and deregisters/heartbeats to stay listed.
2. **Resolution** — a caller finds the current list of instances (and typically gets a healthy subset).

## Three main styles (know the trade-offs)

| Style | How it works | Pros | Cons |
|---|---|---|---|
| **DNS-based** | Service name → A records via internal DNS; client or LB resolves | Ubiquitous, simple, no agent | Stale during churn (TTL), no health awareness by default, slow failover |
| **Registry-based (client-side)** | Services register with a registry (Consul, etcd, Zookeeper, Eureka); client queries registry, then calls instance directly | Health-aware, fast updates, rich metadata | Client complexity; every client needs registry logic + caching |
| **Server-side (via LB / service mesh)** | Caller hits a stable virtual IP / sidecar (Envoy) that resolves and load-balances | Client stays dumb; mesh adds retries/tls/observability | Extra hop; mesh control plane to operate |

**Service mesh** (Istio/Linkerd) is the modern server-side answer: a sidecar proxy per pod does discovery + balancing + retries + mTLS, so app code doesn't care where services live.

## Registration mechanisms (how liveness is known)

- **Self-registration + heartbeat:** instance registers and sends heartbeats (e.g., every 10s); registry evicts after N misses. Simple but instance must not lie when unhealthy (needs a health endpoint distinct from process-alive).
- **Health checking by the registry/LB:** the registry actively probes a health endpoint and marks unhealthy instances out of rotation — more robust, more load.
- **Kubernetes model:** the platform (kubelet) owns registration — pods get stable DNS (`svc.namespace.svc`), endpoints are maintained from readiness probes. App-level discovery often isn't needed at all inside a cluster.

## Why this is an interview favorite

Discovery forces you to think about **failure and dynamism**, not static topology:

- **Stale entries** — a dead instance still listed → connection failures/retries. Mitigate with health checks, fast eviction, and client-side retry to another instance.
- **Thundering herd on registry change** — all clients refetch at once after a big deploy. Mitigate with client-side caching + watch (push) instead of polling.
- **Consistency of the registry** — the registry itself must be highly available and consistent (etcd/Zookeeper = CP; some registries AP). Registry outage shouldn't kill traffic: clients keep using cached lists.
- **Where DNS fits vs where it doesn't** — good for coarse, slowly-changing topology; a registry/mesh for churn + health.

## Interview answer skeleton

"Service discovery has registration and resolution. I'd use the platform's native mechanism where possible — in Kubernetes that's stable service DNS backed by readiness-probed endpoints, often with a service mesh sidecar for health-aware balancing. Outside a platform, a registry like Consul with heartbeats plus client-side caching and watch updates. The key is that discovery must degrade gracefully: clients should keep working from a cached list even if the registry is briefly unavailable."

## Anti-patterns

- ❌ Hard-coded instance IPs "temporarily" — they go stale the moment autoscaling exists.
- ❌ DNS-only discovery with long TTLs for a churning fleet.
- ❌ No client-side caching of registry data → registry outage = total outage.
- ❌ Treating "process is alive" as "instance is healthy" — probe a real health endpoint.
- ❌ Building your own registry when the platform (k8s) or a mesh already provides one.

## Deliberate-practice drills

1. **Style drill:** for a 10-instance autoscaling API, compare DNS vs registry vs mesh discovery; pick and justify.
2. **Failure drill:** the Consul cluster is down for 5 minutes — trace what breaks and what still works with cached clients.
3. **Health drill:** design the registration + health-check cadence so a hanging-but-alive instance is removed within 30 seconds.
4. **k8s drill:** explain how a Deployment's pods become resolvable + how readiness gates remove a bad pod from the Service.
5. **Interview drill:** "your new service can't find the one it calls after a deploy — where do you look?" — answer with discovery staleness, health probe, namespace/DNS.

## References
- See also: dns-deep-dive.md, https-in-practice.md (this repo)
- `networking-engineer` SKILL.md — service mesh, L7 routing
- `cloud-architect` / `devops-engineer` SKILL.md — k8s networking, Consul/mesh ops
