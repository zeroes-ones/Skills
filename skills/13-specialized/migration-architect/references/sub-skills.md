# Sub-Skills

<!-- QUICK: 30s -- table of deeper dives by topic -->
When the agent encounters a specific migration type, drill into the relevant sub-skill rather than reading the full 1600+ line SKILL.md. Each sub-skill has dedicated patterns, scripts, and rollback plans.

| Sub-Skill | What It Covers | When to Load |
|-----------|---------------|--------------|
| **Database Schema Migration** | Expand-contract phases, online schema change tools (gh-ost, pgroll), `CREATE INDEX CONCURRENTLY`, backward-compatible schema evolution rules | Changing table structure in production |
| **Data Migration** | Batch processing with checkpointing, CDC (Debezium/Kafka), dual-write consistency verification, streaming data pipelines | Backfilling or transforming >100K rows |
| **Cloud Migration** | 6 R's framework (Rehost/Replatform/Repurchase/Refactor/Retire/Retain), wave planning, TCO analysis, AWS DMS/Application Migration Service | Moving infrastructure between providers or on-prem → cloud |
| **Framework & Library Migration** | Dependency graph analysis, adapter/wrapper pattern, gradual replacement with feature flags, real-world migration recipes (jQuery→React, REST→GraphQL, Express→Fastify) | Upgrading or swapping a major dependency |
| **Language Migration** | Strangler fig at module boundary, interop patterns (sidecar, gRPC, shared queue), when it makes business sense vs rewrite | Porting Python→Go, Ruby→Elixir, JS→TS, Java→Kotlin |
| **Rollback Engineering** | Per-phase rollback plans, feature flag kill switches, reverse data sync (new→old), bake period design, automated rollback triggers | Any migration where rollback risk is non-trivial |
| **Migration Testing** | Parallel run verification (old vs new output diff), canary deployment with metric comparison, data integrity reconciliation, load test before/after comparison | Validating correctness before cutting over |

> **Token-saving rule:** A migration of a 5GB Postgres database doesn't need the cloud migration or language migration sub-skills. Load only what's relevant. Each section is self-contained with its own scripts, patterns, and checklists.

---
