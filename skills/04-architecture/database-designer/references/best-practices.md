# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Model for access patterns, not for "purity"**: Denormalize when read performance matters more than write simplicity.
- **UUIDs over auto-increment IDs** for distributed systems: UUIDv7 (time-ordered) for primary keys to avoid hot spots.
- **Soft deletes with caution**: `deleted_at` simplifies recovery but complicates every query (add `WHERE deleted_at IS NULL`). Consider archiving to separate tables instead.
- **Separate read and write models**: CQRS pattern for high-scale systems with disparate read/write patterns.
- **Connection management**: Set appropriate pool sizes (CPU cores * 2-4 for OLTP), statement timeouts, idle-in-transaction timeouts.
- **Regular maintenance**: `VACUUM ANALYZE`, index rebuilds, statistics updates, bloat monitoring.
