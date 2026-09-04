# How DNS Works — From Domain to IP (and Back Again)

> Original explainer for interview prep and learning. [research-source: title-only]

## What DNS is

The Domain Name System translates human-readable names (`api.example.com`) into the records clients actually need (IP addresses, mail servers, etc.). It is a **distributed, hierarchical, cached** database — no single server holds the whole namespace, and caching is what makes it fast enough to use on every request.

## The lookup path (know it in order)

1. **Browser/resolver cache** — first check local cache (browser, OS, stub resolver).
2. **Recursive resolver** (ISP / 8.8.8.8 / corporate) — if not cached, it walks the hierarchy on your behalf:
   - **Root servers** → point to `.com` TLD servers.
   - **TLD servers** (`com`, `org`, …) → point to the authoritative nameservers for `example.com`.
   - **Authoritative nameservers** → return the actual answer (A/AAAA record) for `api.example.com`.
3. **Answer + TTL** — the resolver returns the record and caches it for the record's **TTL** (time-to-live); subsequent lookups hit cache.

Recursive resolution typically takes **tens of milliseconds** when uncached (a few round trips) and **<1ms** when cached.

## Record types to know cold

| Record | Purpose |
|---|---|
| **A / AAAA** | IPv4 / IPv6 address for a name |
| **CNAME** | Alias — `www` → canonical name (must not point to another CNAME chain root; no other records on a CNAME) |
| **MX** | Mail exchange server + priority |
| **TXT** | Arbitrary text — SPF, DKIM, domain verification |
| **NS** | Authoritative nameserver delegation |
| **SOA** | Zone metadata (serial, refresh) |
| **PTR** | Reverse: IP → name |

## How it scales and stays reliable

- **Hierarchy** — delegation means no single point of failure for the whole system.
- **Caching + TTL** — most lookups never touch the network; TTL is the dial between freshness and load.
- **Anycast** — root and TLD servers (and many resolvers) run from many locations under one IP; you reach the nearest.
- **Redundancy** — authoritative zones run on ≥2 nameservers; glue records keep delegation reachable.

## DNS in system design (the interview-relevant part)

- **TTL strategy:** short TTL (30–60s) when you need fast failover/changes (blue-green cutover, CDN mapping); long TTL (hours–days) to cut resolver load. Failover speed vs query volume is the trade-off.
- **DNS load balancing** — round-robin A records and geo-based answers are cheap L7 routing but have no health checking and slow failover (cached TTLs). Use it for coarse distribution; use a load balancer for real traffic.
- **CDN integration** — CDNs use DNS to route users to the nearest edge (via geo/anycast + low TTL on the CDN hostname).
- **Service discovery** (internal) — DNS is *one* discovery mechanism: `myservice.prod.svc` style names. But pure DNS lacks health awareness; internal discovery usually pairs DNS with a registry (see dns-and-service-discovery.md in this repo).
- **Failure modes:** DNS outage = total outage (you can't even find the load balancer). Design for it: redundant resolvers, cached/fallback IPs for critical hosts, monitoring of resolver health.
- **Security:** DNS spoofing/poisoning → **DNSSEC** (signed records) where trust matters; **DoH/DoT** to prevent on-path snooping of lookups. Subdomain takeover: dangling DNS records pointing at deprovisioned hosts are a real vulnerability.

## Interview answer skeleton

"DNS is a hierarchical, cached, distributed database. An uncached lookup walks resolver → root → TLD → authoritative nameserver, then the answer is cached per TTL. For design, I think in TTLs — short for fast failover, long for cache efficiency — and I use DNS for coarse geo/routing while real load balancing and service discovery sit behind it with health checks."

## Anti-patterns

- ❌ Forgetting TTL when planning failover — a 24h TTL on a host you need to cut over means a day of stale traffic.
- ❌ Using DNS round-robin as the primary load balancer for stateful or health-critical traffic.
- ❌ Dangling DNS records → subdomain takeover.
- ❌ Treating DNS as instantly consistent — propagation is bounded by TTL, not by "I changed the record."

## Deliberate-practice drills

1. **Path drill:** `dig +trace api.example.com` and narrate each hop.
2. **TTL drill:** design the TTLs for a blue-green cutover (pre-switch lower TTL, switch, then raise).
3. **Record drill:** given a zone, write A, CNAME, MX, TXT/SPF records correctly; spot the invalid CNAME setup.
4. **Discovery drill:** compare DNS-based service discovery vs registry-based (Consul/etcd) for a 200-service mesh — latency, health, failure.
5. **Failure drill:** the company resolver is down — what still works, what breaks, and what's your mitigation?

## References
- See also: dns-and-service-discovery.md, https-in-practice.md (this repo)
- `networking-engineer` SKILL.md — VPC/DNS/CDN design, zero trust
