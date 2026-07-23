# When NOT to Use This Skill (Overkill)

- **Pre-launch with 0 users**: You can dump, modify, and restore your database in minutes. Zero-downtime migration patterns are solving a problem you don't have.
- **Database is <1GB and migrations take <5 seconds**: `ALTER TABLE` during a maintenance window is fine. Don't build an online schema change pipeline.
- **Solo developer**: Expand-contract requires dual-write code paths, feature flags, and multi-phase deploys. That's operational overhead for a team of 1. Simple migrations work.
- **Read-only or append-only database**: If you never alter existing tables (only create new ones and append data), migration patterns for schema changes aren't needed.
- **Prototype/throwaway project**: Don't version migrations for a project you'll delete in 2 weeks. Raw SQL is fine.
