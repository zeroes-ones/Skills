# Consistent Hashing — What It Is, Why Distributed Systems Need It

> Original explainer for interview prep and learning. [research-source: title-only]

## The problem it solves

You have N cache servers and a key→server mapping. The naive answer is `server = hash(key) % N`. It is simple and fast — but when N changes (a server dies, you add capacity), almost **every key remaps** to a different server. In a cache that means a near-total cache miss storm (thundering herd against the DB). Consistent hashing makes remapping *minimal*: when N changes, only ~1/N of keys move.

## How it works

1. Place servers on a ring of hash values (e.g., `hash(server_id)` → position on a 0..2³² circle).
2. For a key, compute `hash(key)` and walk **clockwise** to the first server — that server owns the key.
3. When a server is added/removed, only the keys between it and its clockwise neighbor remap.

### The hot-spot problem and virtual nodes
Real keys aren't uniform, and few real servers can make the ring balanced. Fix: each physical server registers **K virtual nodes** at random ring positions, so its share is spread across the ring. This improves balance and makes removal/addition smoother.

### Ordering guarantees
Consistent hashing gives *no* ordering or replication semantics by itself — it is a placement strategy. Replication is layered on top (e.g., store a key on the next R servers clockwise for R-way redundancy, which is how Dynamo-style systems get availability).

## Where it's used (name-drop these correctly)

- **Distributed caches:** Memcached clusters (libketama), so adding a node doesn't flush everything.
- **DynamoDB / Cassandra:** partition placement with virtual nodes; replication to the next N nodes.
- **CDNs:** edge server selection that survives node churn.
- **Load balancers:** consistent hashing by client/IP so sticky state survives topology changes.

## What interviewers probe

- **"Why not hash % N?"** — answer the remapping storm, then mention consistent hashing's minimal-movement property.
- **"What breaks?"** — balance (fix with virtual nodes), and that it doesn't handle *replication/ordering* (pair with a replication scheme).
- **"What about a hot key?"** — consistent hashing spreads keys, not popularity; a single viral key still hammers one server → add key-level caching, replication of hot keys, or shard-by-tenant.
- **"Is it a database? Does it persist?"** — no; it's placement. Pair with replication + durability.

## Interview answer skeleton (30 seconds)

"To map keys to servers we can't use modulo-N because any node change remaps nearly everything. Consistent hashing puts servers on a ring and assigns each key to the first server clockwise; adding or removing a node only moves its neighbor's slice. We add virtual nodes per server so load stays balanced. It's placement, not replication — we layer R-way replication and handle hot keys separately."

## Anti-patterns

- ❌ Presenting consistent hashing as a *consistency* mechanism (it's about *placement/balance* under churn).
- ❌ Ignoring balance: without virtual nodes, few servers → lopsided rings → hot servers.
- ❌ Treating it as a substitute for replication, durability, or hot-key handling.

## Deliberate-practice drills

1. **Hand-simulate:** draw an 8-slot ring, place 3 servers, hash 10 keys; remove one server and count how many keys move (expect ~1/3).
2. **Virtual-node drill:** simulate 3 servers × 50 vnodes vs 3 plain nodes; measure load variance on 1,000 keys.
3. **Design drill:** architect a distributed cache for 100M keys across 10 nodes that can lose 2 nodes without a DB storm.
4. **Comparison drill:** consistent hashing vs rendezvous hashing vs modulo — when is each better?
5. **Interview drill:** answer "we added a cache node and the DB melted — why?" with the remapping-storm explanation and the fix.

## References
- See also: distributed-systems-101.md, system-design-101.md (this repo)
- `system-architect` SKILL.md — capacity planning, sharding
- `database-designer` SKILL.md — partitioning/sharding references
