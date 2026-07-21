---
name: migration-architect
description: Database migration strategies (expand-contract, blue-green, parallel run), cloud migration (6 R's), framework/language migration patterns, rollback strategy, stakeholder management, migration testing.
author: Sandeep Kumar Penchala
type: specialized
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - migration-architect
token_budget: 3134
output:
  type: "code"
  path_hint: "./"
---
# Migration Architect

A veteran's playbook for planning and executing every type of production migration — database schema changes, platform swaps, language rewrites, framework upgrades, and cloud transitions — with zero downtime, military-grade rollback capability, and stakeholder trust.

This is not a theory document. Every section contains specific code, commands, scripts, and decision trees you can use tomorrow.

## When to Use

- You need to execute a database schema migration in production without downtime using expand-contract or online schema change tools
- You are planning a cloud migration (on-prem to cloud or between clouds) and need to apply the 6 R's framework
- You need to migrate a framework or library (e.g., jQuery→React, REST→GraphQL, Express→Fastify) gradually with feature flags
- You are porting a service from one language to another (Python→Go, Ruby→Elixir, JS→TS) using the strangler fig pattern
- You need to design a rollback plan for every phase of a migration with kill switches and reverse data sync
- You are running a parallel verification — comparing old system output against new system output — before cutting over
- You need to backfill or transform 100K+ rows of data with checkpointing, batching, and consistency verification
- You are migrating a large codebase and need a phased plan with stakeholder communication, risk assessment, and testing gates

## Sub-Skills
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
## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### 1. Migration Strategy Selection
```
                     ┌────────────────────────┐
                     │ START: What's the      │
                     │ primary constraint?    │
                     └───────────┬────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
    ┌─────▼──────┐       ┌───────▼───────┐       ┌──────▼──────┐
    │ Deadline   │       │ Zero downtime │       │ Budget      │
    │ in <3      │       │ required,     │       │ <$50K,      │
    │ months?    │       │ user-facing?  │       │ small team? │
    └─────┬──────┘       └───────┬───────┘       └──────┬──────┘
          │YES                   │YES                    │YES
    ┌─────▼──────┐       ┌───────▼───────┐       ┌──────▼──────────┐
    │ Lift-and-  │       │ Strangler Fig │       │ Lift-and-Shift  │
    │ Shift      │       │ or Parallel   │       │ then optimize   │
    │ (Rehost).  │       │ Run. Migrate  │       │ incrementally.  │
    │ Optimize   │       │ piece by      │       │ Accept higher   │
    │ later.     │       │ piece.        │       │ infra cost       │
    └────────────┘       └───────────────┘       │ initially.      │
                                                 └─────────────────┘
          │NO (none of the above are critical constraints)
    ┌─────▼──────────────────┐
    │ Refactor-and-Migrate   │
    │ — best long-term ROI.  │
    │ Redesign for target    │
    │ platform. Higher risk, │
    │ highest payoff.        │
    └────────────────────────┘
```
**Lift-and-Shift:** When deadline <3 months or budget <$50K. Accept suboptimal architecture; optimize after migration.  
**Strangler Fig:** When zero downtime is required. Replace pieces incrementally behind a proxy/router.  
**Refactor-and-Migrate:** When long-term ROI matters more than speed. Highest payoff, highest risk.

### 2. Database Migration Approach
```
                   ┌──────────────────────────┐
                   │ START: Can you tolerate  │
                   │ write downtime?          │
                   └───────────┬──────────────┘
                               │
                    ┌──────────▼──────────┐
                    │ YES → Big-bang:     │
                    │ dump, transform,    │
                    │ load, verify,       │
                    │ cut-over. Fastest.  │
                    └─────────────────────┘
                    ┌──────────▼──────────┐
                    │ NO → How much data? │
                    └────┬───────────┬────┘
                         │           │
                    ┌────▼────┐ ┌───▼──────────┐
                    │ <100GB  │ │ >100GB or    │
                    └────┬────┘ │ high write   │
                         │      │ throughput   │
                    ┌────▼────┐ └───┬──────────┘
                    │ Dual-   │ ┌───▼──────────────┐
                    │ write + │ │ CDC (Debezium/   │
                    │ backfill│ │ Kafka Connect) + │
                    │         │ │ dual-write with  │
                    └─────────┘ │ eventual cutover │
                                └──────────────────┘
```
**Big-bang:** Writes paused → dump → transform → load → verify → cut over. For <100GB with a maintenance window.  
**Dual-write:** Write to both old and new, backfill history, verify consistency, cut reads, then cut writes.  
**CDC:** For >100GB or high-throughput — Debezium/Kafka pipelines, no application changes needed for reads.

### 3. Framework/Library Migration Decision
```
               ┌───────────────────────────┐
               │ START: How many dependent │
               │ packages and LOC?         │
               └───────────┬───────────────┘
                           │
                ┌──────────▼──────────┐
                │ <10K LOC, <50 deps? │
                └────┬───────────┬────┘
                     │YES        │NO
                ┌────▼────┐ ┌───▼──────────────┐
                │ Big-bang│ │ Are public APIs  │
                │ rewrite │ │ stable?          │
                │ in 1-2  │ └──┬───────────┬───┘
                │ sprints │    │YES        │NO
                └─────────┘ ┌──▼──────┐ ┌──▼──────────┐
                            │ Strangler│ │ Feature flag │
                            │ with     │ │ + adapter    │
                            │ adapter  │ │ per module   │
                            │ pattern  │ │              │
                            └──────────┘ └──────────────┘
```
**<10K LOC → big-bang rewrite.** One sprint, full replacement.  
**Stable APIs → Strangler with adapters.** Migrate module-by-module behind same interface.  
**Unstable APIs → Feature flags per module.** Gradual, safe, allows A/B testing each component.

### 4. Cloud Migration Strategy (6 R's)
```
                 ┌──────────────────────────┐
                 │ START: What's the app    │
                 │ architecture?            │
                 └───────────┬──────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
  ┌─────▼──────┐     ┌───────▼───────┐    ┌───────▼──────┐
  │ Monolith   │     │ Containerized │    │ Already      │
  │ on VM?     │     │ microservices?│    │ cloud-native?│
  └─────┬──────┘     └───────┬───────┘    └───────┬──────┘
        │                    │                    │
  ┌─────▼──────┐     ┌───────▼───────┐    ┌───────▼──────────┐
  │ Rehost     │     │ Replatform    │    │ Refactor or      │
  │ (lift-and- │     │ (ECS/GKE      │    │ Retain. Already  │
  │ shift) or  │     │ instead of    │    │ optimized. Mig-  │
  │ Retire if  │     │ self-managed  │    │ rate only if     │
  │ deprecated │     │ K8s)          │    │ multi-cloud      │
  └────────────┘     └───────────────┘    │ needed.          │
                                          └──────────────────┘
```
**Rehost:** VM to cloud VM. Fastest, cheapest migration. Optimize later.  
**Replatform:** Containerize + use managed services (RDS instead of self-managed Postgres). Better TCO.  
**Refactor:** Rewrite for cloud-native. Highest effort, highest long-term ROI.  
**Retain/Retire:** Keep on-prem if already optimized. Retire if app is deprecated.

### 5. When to Roll Back
```
                   ┌──────────────────────────┐
                   │ START: Is the migration  │
                   │ in production?           │
                   └───────────┬──────────────┘
                               │
                ┌──────────────▼──────────────┐
                │ Data corruption detected?   │
                └────┬───────────────────┬────┘
                     │YES                │NO
                ┌────▼────────┐  ┌───────▼──────────────┐
                │ ROLL BACK   │  │ P95 latency >3x      │
                │ IMMEDIATELY.│  │ baseline OR error    │
                │ Don't wait. │  │ rate >1%?            │
                │ Every minute│  └──┬──────────────┬────┘
                │ = more lost │     │YES           │NO
                │ data.       │┌────▼────────┐ ┌───▼──────────┐
                └─────────────┘│ ROLL BACK   │ │ Continue     │
                               │ after       │ │ bake +       │
                               │ confirming  │ │ monitor.     │
                               │ it's not a  │ │ Extend bake  │
                               │ transient   │ │ to 2x normal │
                               │ spike       │ │ duration.    │
                               └─────────────┘ └──────────────┘
```
**Data corruption → immediate rollback. No waiting. No investigation during incident.**  
**P95 >3x baseline or error rate >1% → roll back after confirming non-transient.**  
**Everything else → extend bake period. Never roll back on the first small anomaly.**

## Migration Patterns

Detailed migration patterns, assessment frameworks, and database migration deep dives are in **[references/migration-patterns.md](references/migration-patterns.md)**:

| Section | What's Covered |
|---------|---------------|
| **Assessment & Scoping** | Inventory gathering, complexity scoring (1-5 scale), dependency mapping, build-vs-buy decision framework |
| **Migration Patterns** | Lift-and-Shift, Refactor-and-Migrate, Strangler Fig, Parallel Run, Blue-Green Cutover — with decision matrix |
| **Database Migration** | Expand-Contract pattern with full code, schema evolution rules, batch/streaming/dual-write data migration, CDC (Debezium), migration frameworks comparison, online schema change tools (gh-ost, pt-online-schema-change), consistency verification |

**Quick Reference:**
- **Fastest path:** Lift-and-Shift → optimize incrementally post-migration
- **Zero-downtime DB:** Expand-Contract (add new column → dual-write → backfill → remove old)
- **Data sync verification:** Row counts + checksums + business-level reconciliation queries

## Migration Workflows

Detailed workflow steps for framework, language, cloud, and stakeholder management are in **[references/migration-workflows.md](references/migration-workflows.md)**:

| Section | What's Covered |
|---------|---------------|
| **Framework/Library Migration** | Dependency analysis, adapter pattern with code examples, gradual replacement via feature flags, real-world examples (Express→Fastify, React class→hooks, AngularJS→React) |
| **Language Migration** | When it makes sense, interop patterns (FFI/gRPC/sidecar), Strangler at module boundary, real-world approaches (Python→Go, Ruby→Elixir, Java→Kotlin) |
| **Cloud Migration** | The 6 R's framework, Well-Architected assessment, wave sequencing, AWS-specific tools (MGN, DMS, DRS), TCO calculation with comparison |
| **Testing During Migration** | Parallel run verification with diffing system, canary comparison, data integrity reconciliation, performance regression testing |
| **Rollback Strategy** | Per-phase rollback plans, feature flags for quick disable, data sync reversal, bake periods, decision triggers |
| **Stakeholder Management** | Timeline communication templates, business continuity assurance, success metrics (KPIs), communication cadence |

**Quick Reference:**
- **Framework migration <10K LOC:** Big-bang rewrite. >10K: Strangler with adapter.
- **Language migration:** Only if team hiring for target language is easier than hiring for current
- **Bake period minimums:** DB migration 24h → API migration 48h → Full stack 72h
- **Rollback trigger #1:** Data corruption anywhere = immediate rollback

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Discovery & Assessment
**Input:** Existing system (codebase, infra, DB, dependencies)  
**Steps:** 1) Inventory all services, databases, and dependencies 2) Score each component by complexity (1-5) 3) Map dependency graph 4) Identify highest-risk components 5) Build migration wave plan  
**Output:** Scored inventory + dependency map + migration wave sequencing plan

### Phase 2 (~30 min): Pattern Selection & Proof of Concept
**Input:** Assessment results and constraints (time, budget, downtime tolerance)  
**Steps:** 1) Apply migration strategy decision tree 2) Select pattern (Strangler/Parallel/Lift-and-Shift/etc.) 3) Build PoC on 1-2 low-risk components 4) Validate approach with real data and traffic 5) Document pattern with code templates  
**Output:** Validated migration pattern + PoC results + reusable templates

### Phase 3 (~20 min): Data Migration Execution
**Input:** Source database schema and target schema design  
**Steps:** 1) Apply Expand-Contract for zero-downtime schema changes 2) Set up dual-write or CDC pipeline 3) Run backfill with checkpointing (resumable) 4) Verify consistency (row counts + checksums + business queries) 5) Cut over reads, monitor, cut over writes  
**Output:** Migrated database with verified consistency, rollback path ready

### Phase 4 (~15 min): Application Migration
**Input:** Validated patterns, migrated data plane  
**Steps:** 1) Migrate by wave (low-risk first) 2) Route percentage of traffic via feature flags/canary 3) Compare old vs new responses (diffing system) 4) Increase traffic 10% → 25% → 50% → 100% with monitoring gates 5) Keep old system in read-only mode for bake period  
**Output:** Application running on target platform with rollback capability

### Phase 5 (~25 min): Verification & Decommission
**Input:** Fully migrated system in production  
**Steps:** 1) Complete bake period (24-72h depending on component) 2) Run final data integrity reconciliation 3) Verify all monitoring/alerting operational on new system 4) Decommission old system (after confirmed no rollback needed) 5) Conduct retrospective, document lessons learned  
**Output:** Old system decommissioned, migration complete, retrospective document
## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Migration architecture is inherently cross-functional — it spans databases, application code, infrastructure, and QA. A migration without coordination is a production incident waiting to happen.

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Backend Developers** | Schema changes, data access layer changes, API versioning | Migration sequence, dual-write requirements, backward compatibility rules |
| **DBA / Database Team** | Schema migration, index changes, query performance | DDL review, lock duration estimates, replication lag impact, rollback plan |
| **DevOps / Infrastructure** | Deployment orchestration, environment management, backup/restore | Migration deployment order, blue-green coordination, backup verification |
| **System Architect** | Architecture changes, service boundaries, data ownership | Data ownership shifts, service decomposition impact, eventual consistency model |
| **QA Engineer** | Migration testing, data integrity verification, regression testing | Test environments, data comparison scripts, rollback test scenarios |
| **Security Reviewer** | Data migration security, sensitive data handling, encryption | Data at rest/in transit during migration, access control for migration tools |
| **Project Manager** | Migration timeline, stakeholder communication, resource coordination | Migration milestones, risk register, rollback decision authority |
| **Performance Engineer** | Migration impact on production performance, load during backfill | Backfill throttling, read/write load analysis, connection pool impact |
| **CTO Advisor** | Build vs buy migration tooling, architecture decisions | Tooling investment, migration strategy approval, risk acceptance |
| **Product Strategist** | User-facing migration impact, downtime communication, feature flags | User impact assessment, maintenance window communication, feature flag coordination |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Migration script ready for production execution | Project Manager, DevOps, Backend Developers, DBA | Execution window scheduling; all stakeholders on standby |
| Data integrity check fails (row count mismatch, checksum mismatch) | DBA, Backend Developers, QA | Stop migration; root cause analysis; potentially pause backfill |
| Migration causes production latency increase >20% | Performance Engineer, DevOps, Project Manager | Throttle or pause; production impact unacceptable |
| Rollback plan activated for any reason | Project Manager, All Coordinated Teams | Incident declared; all teams execute rollback checklist |
| Schema change requires application downtime (cannot be done online) | Product Strategist, Project Manager, DevOps | Schedule maintenance window; user communication required |
| Backfill estimated completion shifts by >50% | Project Manager, Backend Developers | Replan cutover date; stakeholder expectation reset |
| Cross-team dependency for migration not met (e.g., API not ready, service not deployed) | Project Manager, Affected Team Lead | Blocking dependency; escalation for prioritization |
| Migration complete — verification passing, dual-write retired | All Coordinated Teams, Product Strategist, CTO Advisor | Migration closure; celebration; post-migration monitoring period begins |

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| Data corruption detected post-migration (>10 rows or any customer-impacting) | **CTO Advisor** + VP Engineering + Incident Commander | Production incident; may require restore from backup |
| Migration blocked by external vendor/API limitation indefinitely | **CTO Advisor** + Product Strategist + Project Manager | Strategy pivot; may require architectural workaround or vendor change |
| Rollback fails during attempted execution | **CTO Advisor** + DevOps Lead + DBA | Critical incident; restore from backup may be only option |
| Migration cost/time exceeds original estimate by >100% | **CTO Advisor** + Project Manager + Stakeholders | Re-baseline; build vs buy vs maintain re-evaluation |
| Compliance/regulatory issue discovered in migrated data | **Legal Advisor** + Security Reviewer + Regulatory Specialist | Regulatory exposure; may require data remediation or disclosure |

## 10. Production Checklist

- [ ] **Inventory complete:** all databases, services, cron jobs, consumers, and dependencies documented with row counts, throughput estimates, and coupling scores
- [ ] **Migration pattern selected** with documented rationale and scored using the decision matrix (expand-contract, strangler, parallel run, blue-green, rehost, refactor)
- [ ] **Complexity scored** using the 1–5 scoring system; high-score migrations have staged rollout plans
- [ ] **Hidden dependencies found:** shared databases, hardcoded endpoints, shared sequences; mitigation plan documented
- [ ] **Dependency graph built** (upstream + downstream) and shared with all affected teams; each consumer has been individually contacted and confirmed awareness
- [ ] **Build vs buy decision** made and documented; managed services (DMS, MGN, gh-ost, pgroll) evaluated where appropriate
- [ ] **Schema changes are backward-compatible** at every intermediate phase; no breaking changes without expand-contract
- [ ] **Migration framework selected** (Flyway, Alembic, Prisma, golang-migrate, atlas, goose) with versioned, checksummed, reviewable migrations
- [ ] **Up and Down scripts** exist for every schema change; Down scripts tested in staging
- [ ] **CI pipeline validates:** migrations apply cleanly on a fresh database, no drift from production schema, Down scripts tested, data-loss operations require explicit confirmation
- [ ] **Data migration scripts** use batch processing with checkpoint-based resumability, idempotency guarantees, and configurable throttling (sleep between batches)
- [ ] **CDC replication tested** (if using Debezium/Kafka for streaming): binlog replication slot created, consumer lag monitored, JSON deserialization verified
- [ ] **Dual-write consistency verification** script written and tested; periodic sampling compares old vs new row-by-row
- [ ] **Reconciliation queries** written: row count comparison, full-table checksum, per-row sampling with hashed comparison, orphan detection
- [ ] **Performance tested** on a production-scale snapshot: duration, database load, replication lag impact, query plan comparison, lock contention analysis
- [ ] **Load test executed** on both old and new systems; P50/P95/P99 latencies compared; error rates confirmed below threshold
- [ ] **Rollback plan documented per phase** with exact commands/scripts, estimated duration, data risk, and verification steps
- [ ] **Rollback tested in staging** — full up-and-down cycle verified for every phase
- [ ] **Feature flags implemented** for dual-write/dual-read toggling with instant rollback capability (≤ 30 seconds per flag flip)
- [ ] **Rollback decision triggers defined** with numeric thresholds (error rate > 0.5%, P99 latency > 1s, replication lag > 60s)
- [ ] **Reverse sync script written** (for rolling back data from new → old during dual-write phase)
- [ ] **Pre-migration backup completed** and verified as restorable (tested on a separate environment)
- [ ] **Monitoring dashboards configured:** replication lag, lock contention, error rates, migration progress, latency percentiles (P50/P95/P99), connection count
- [ ] **Alarms configured:** replication lag > threshold, error rate spike, migration checkpoint stall > 10 min
- [ ] **Bake period defined** (minimum 24 hours for simple schema changes, 7 days for platform migrations, 30 days for financial systems)
- [ ] **Communication plan executed:** stakeholders, support team, on-call informed of migration window and phases
- [ ] **Go/no-go decision process defined** — who decides, based on what metrics, at what checkpoints
- [ ] **Post-migration cleanup** planned: old schema removal, feature flag removal, dual-write code removal, old system decommission
- [ ] **Postmortem scheduled** and template prepared: what went well, what went wrong, what to improve

---
## Scale Depth
<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person) → Small (2-10) → Medium (10-50) → Enterprise (50+)

| Dimension | Solo | Small | Medium | Enterprise |
|-----------|------|-------|--------|------------|
| **Migration Scope** | 1 database, <10 tables, <1GB | 1 codebase, 1 DB, <50 tables | 5-20 services, multiple DBs | 50+ services, multi-region, multi-DB |
| **Tooling** | ORM auto-migrate, raw SQL | Framework-based (Flyway/Alembic/Prisma) | Online schema change (gh-ost/pgroll) + CDC | Blue-green DB deploys + automated drift detection |
| **Testing** | Manual apply, verify, roll back | CI: apply up → test → roll back → test | Prod-scale clone testing + perf regression | Automated migration testing with synthetic traffic |
| **Risk Management** | Maintenance window acceptable | Expand-Contract for zero-downtime | Feature flags + canary per migration phase | Multi-region gradual rollout + auto-rollback on anomaly |
| **Rollback** | Manual script per migration | Documented rollback per phase | Automated rollback tested in CI | Instant feature-flag disable + data sync reversal |
| **Coordination** | Developer owns migration end-to-end | 1 backend specialist reviews | Migration architect + DB team | Dedicated migration team with runbook and stakeholder comms |

### Transition Triggers

| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo → Small | Paying users who would notice >1s downtime | Add versioned migrations, Expand-Contract for schema changes, CI validation |
| Small → Medium | Database >50GB or >5 services | Online schema change tools, CDC for data migration, automated rollback testing |
| Medium → Enterprise | Multi-region, >50 services, regulatory compliance | Blue-green deployments, automated drift detection, migration runbook with stakeholder comms |

## Cost-Effective Decision Table

| Decision | Free/Cheap Option | Paid Upgrade | When to Upgrade |
|----------|------------------|--------------|-----------------|
| Migration framework | ORM built-in (ActiveRecord, Prisma, SQLAlchemy auto-migrate) | Flyway Teams ($3K/yr) or Liquibase Pro | Need dry-run validation, undo scripts, or enterprise DB support (Oracle, DB2) |
| Online schema changes | PostgreSQL: `CREATE INDEX CONCURRENTLY` (built-in). MySQL: `gh-ost` (free OSS) | — | Free OSS tools cover 95% of needs |
| Data migration (backfill) | Custom Python/Node script with batching + checkpointing (1-2 days to write) | Data pipeline tool (Airbyte, Fivetran) | Backfill spans 10+ tables with complex transformations or needs scheduling |
| Schema drift detection | `pg_dump --schema-only` diff or manual comparison | Skeema ($250/mo) or Atlas ($295/mo) | >50 tables or multiple environments that drift frequently |
| Migration testing | CI job: apply migration to prod clone, verify | Database Lab Engine (Postgres, OSS) or Snaplet | Need instant (<1s) database clones for fast CI feedback |
| Rollback planning | Manual: write down script per phase | Atlas (declarative schema, auto-generates rollback) | >20 migrations/month or team >5 people |

**Annual migration tool budget by phase:** MVP: $0 (ORM built-in). Growth: $0-1K (OSS tools). Scale: $0-10K (OSS tools + CI infra).

## When NOT to Use This Skill (Overkill)

- **Pre-launch with 0 users**: You can dump, modify, and restore your database in minutes. Zero-downtime migration patterns are solving a problem you don't have.
- **Database is <1GB and migrations take <5 seconds**: `ALTER TABLE` during a maintenance window is fine. Don't build an online schema change pipeline.
- **Solo developer**: Expand-contract requires dual-write code paths, feature flags, and multi-phase deploys. That's operational overhead for a team of 1. Simple migrations work.
- **Read-only or append-only database**: If you never alter existing tables (only create new ones and append data), migration patterns for schema changes aren't needed.
- **Prototype/throwaway project**: Don't version migrations for a project you'll delete in 2 weeks. Raw SQL is fine.

## Token-Efficient Workflow

```
# Step 1: Migration readiness check
python3 scripts/migration_check.py --db-url $DATABASE_URL --output json
# Returns: {"size_gb": 2.5, "table_count": 42, "largest_table_rows": 1500000,
#           "has_replicas": true, "replication_lag_ms": 50, "active_connections": 80}

# Step 2: Decision tree → choose migration pattern
# largest_table_rows > 1M → Online schema change (gh-ost/pgroll). Don't ALTER directly.
# size_gb > 50 → Test on prod-scale clone first. Expect migration to take hours.
# has_replicas + lag > 1000ms → Throttle migration to reduce lag. Monitor closely.

# Step 3: Validation with exit codes
# Verify migration applies cleanly
npm run migrate:up -- --dry-run  # Exit code 0 = clean apply

# Verify migration rolls back
npm run migrate:down -- --dry-run  # Exit code 0 = clean rollback

# Verify no schema drift
python3 scripts/check_schema_drift.py --source migrations/ --target $DATABASE_URL
# Exit code 0 = no drift, 1 = drift detected

# Step 4: During migration — monitor replication lag
python3 scripts/monitor_replication.py --threshold-ms 2000 --output json
# Exit code 0 = lag below threshold, 1 = threshold exceeded (pause migration)
```

**Principle:** `migration_check.py` analyzes database metadata, outputs JSON. Agent applies decision tree to select pattern. Validation uses exit codes (dry-run, drift check). Monitoring script checks replication lag programmatically during execution.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
1. **Expand-Contract for every schema change:** Add → dual-write → backfill → switch reads → remove old. Never drop a column in the same deploy that adds its replacement.
2. **Test rollbacks before you need them:** Every migration must pass CI: apply up → run tests → roll back → run tests. If rollback can't be tested, it doesn't exist.
3. **Start with low-risk components first:** Migrate your least critical, least coupled service first. Learn from it. Don't start with the payment system.
4. **Batch data migration with checkpointing:** Process 1K-10K rows per batch with a sleep interval. Save checkpoint after each batch. A failed 100M-row migration must resume, not restart.
5. **Feature flags for every migration path:** Every new code path gets a flag. If something breaks, you disable the flag — not roll back a deploy. Flags toggle in seconds; deploys take minutes.
6. **Bake period scales with blast radius:** DB-only change → 24h bake. API migration → 48h. Full-stack → 72h minimum. Never decommission old system before bake completes.
7. **Monitor replication lag during migration:** Lag >2s → throttle or pause migration. The old system is your rollback — don't let it fall behind.
8. **Consistency verification is non-negotiable:** Row counts match. Checksums match. Business-level reconciliation queries pass. All three must pass before cutover.
9. **Never migrate and refactor simultaneously:** Either lift-and-shift (same logic, new platform) OR refactor-and-migrate (new logic). Doing both at once makes debugging impossible.
10. **Conduct a pre-mortem before every migration:** "The migration failed. What went wrong?" Write down the top 3 causes. Those are your rollback triggers and monitoring priorities.

## References
<!-- QUICK: 30s -- links to deeper reading -->
### Patterns & Theory
- [Parallel Change / Expand-Contract (Martin Fowler)](https://martinfowler.com/bliki/ParallelChange.html)
- [Blue-Green Deployment (Martin Fowler)](https://martinfowler.com/bliki/BlueGreenDeployment.html)
- [Strangler Fig Pattern (Martin Fowler)](https://martinfowler.com/bliki/StranglerFigApplication.html)
- [The 6 R's of Cloud Migration (Gartner/AWS)](https://aws.amazon.com/blogs/enterprise-strategy/6-strategies-for-migrating-applications-to-the-cloud/)

### Database Migration Tools
- [gh-ost — GitHub's Online Schema Migration for MySQL](https://github.com/github/gh-ost)
- [pt-online-schema-change — Percona Toolkit](https://docs.percona.com/percona-toolkit/pt-online-schema-change.html)
- [pgroll — Zero-Downtime Schema Changes for PostgreSQL](https://github.com/xataio/pgroll)
- [pg_repack — Online Table Rebuild for PostgreSQL](https://github.com/reorg/pg_repack)
- [Flyway — Database Migrations](https://flywaydb.org/)
- [Liquibase — Database Schema Change Management](https://www.liquibase.com/)
- [Alembic — Database Migration Tool for SQLAlchemy](https://alembic.sqlalchemy.org/)
- [Prisma Migrate — Declarative Database Migrations](https://www.prisma.io/docs/orm/prisma-migrate)
- [golang-migrate — Database Migrations in Go](https://github.com/golang-migrate/migrate)
- [atlas — Declarative Schema Management](https://atlasgo.io/)
- [goose — Database Migrations in Go](https://github.com/pressly/goose)

### Cloud Migration
- [AWS Application Migration Service (MGN)](https://aws.amazon.com/application-migration-service/)
- [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS VM Import/Export](https://aws.amazon.com/ec2/vm-import/)
- [Google Cloud Migration Services](https://cloud.google.com/migration)
- [Azure Migrate](https://azure.microsoft.com/en-us/products/azure-migrate/)

### Data Streaming & CDC
- [Debezium — Change Data Capture Platform](https://debezium.io/)
- [Apache Kafka — Event Streaming Platform](https://kafka.apache.org/)
- [Kafka Connect — Scalable Streaming Integrations](https://kafka.apache.org/documentation/#connect)

### Feature Flags & Rollback
- [LaunchDarkly — Feature Management](https://launchdarkly.com/)
- [Feature Flags (Martin Fowler)](https://martinfowler.com/articles/feature-toggles.html)

### Testing & Verification
- [Locust — Load Testing Framework](https://locust.io/)
- [k6 — Modern Load Testing](https://k6.io/)
- [Apache JMeter — Performance Testing](https://jmeter.apache.org/)
