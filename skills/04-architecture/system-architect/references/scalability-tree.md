# Scalability Decision Tree

```
DB CPU > 70% sustained?
├── YES → Add read replicas → Still high? → Shard by tenant.
└── NO → Don't shard.

P95 latency > 200ms?
├── YES → Profile → Add cache (Redis) → Optimize queries → Make async.
└── NO → You're fine.

CI > 15 minutes?
├── YES → Parallelize tests → Split into smaller jobs → Consider service extraction.
└── NO → Ship features.

>2 teams colliding in same codebase?
├── YES → Extract one bounded context at a time.
└── NO → Keep the monolith.

Service handles < 100 req/s? → It's a library, not a service. Merge back.
Cache hit rate < 50%? → Remove the cache. It's adding latency.
```
