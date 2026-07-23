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
token_budget: 2010
output:
  type: "code"
  path_hint: "./"
chain:
  consumes_from: ["system-architect", "database-designer", "devops-engineer"]
  feeds_into: ["devops-engineer", "database-reliability-engineer", "backend-developer"]
---
# Migration Architect

A veteran's playbook for planning and executing every type of production migration — database schema changes, platform swaps, language rewrites, framework upgrades, and cloud transitions — with zero downtime, military-grade rollback capability, and stakeholder trust.

This is not a theory document. Every section contains specific code, commands, scripts, and decision trees you can use tomorrow.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->

What are you trying to do?
├── Database migration (expand-contract, blue-green, parallel run) → Start at "Database Schema Migration" under Sub-Skills
├── Cloud migration (6 R's) → Go to "Cloud Migration" under Sub-Skills
├── Framework or language migration → Jump to "Framework & Library Migration" under Sub-Skills
├── Design a rollback strategy → Go to "Rollback Strategy" section in Core Workflow
├── Stakeholder communication during migration → Jump to "Stakeholder Management" under references/
├── Migration testing → Go to "Migration Testing" under Sub-Skills
├── Need architecture assessment first → Route to `system-architect`
├── Need schema design or index strategy → Route to `database-designer`
├── Need deployment orchestration → Route to `devops-engineer`
├── Need database reliability (replication, failover) → Route to `database-reliability-engineer`
└── Don't know where to start? → Start at "Database Schema Migration"

**Do not read the entire skill.** Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never migrate without a verified rollback plan tested in production-like conditions.** If you can't roll back, you can't go forward.
- **Every migration step must have a success criterion.** "Migration complete" is not measurable. "All reads serving from new table, no errors in 5 minutes" is.
- **Stakeholder communication must happen before, during, and after.** Silence during a migration breeds panic.
- **The "strangler fig" pattern beats big-bang rewrites.** Replace incrementally — never rewrite everything at once.
- **Always run parallel verification before cutover.** Old and new systems should produce identical results before switching.
- **Admit what you don't know.** If data integrity guarantees or legacy system behavior are unclear, pause and investigate.


## The Expert's Mindset

Masters of migration architect don't just build — they build **the right thing, at the right time, with the right trade-offs**. They think in systems, not tasks.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Shiny object syndrome** — chasing new tools without evaluating fit | Before adopting any new tool, write the "why this over the incumbent" justification |
| **Over-engineering** — building for hypothetical scale | Default to simplest solution; add complexity only when the current solution actually breaks |
| **Not-invented-here** — preferring to build rather than compose | Always evaluate 2 existing solutions before building custom |
| **Sunk cost fallacy** — sticking with a technology because you already invested in it | Re-evaluate tech choices every quarter; migration cost vs. staying cost |

### What Masters Know That Others Don't
- The **failure modes** of every component in their stack — not just the happy path
- When **not** to use their favorite tool (every tool has a misuse zone)
- That **data/model quality decays over time** — monitoring is not optional, it's foundational

### When to Break Your Own Rules
- **Move fast on reversible decisions.** Data format? Hard to change. Dashboard layout? Easy. Know the difference.
- **Skip the abstraction until the third use case.** Two is coincidence, three is a pattern.
## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single component/module | Implement a well-defined piece following established patterns |
| **L2** | Feature or service | Design and build a complete feature; make tech choices within team conventions |
| **L3** | System or product area | Define architecture for a product area; set team tech standards; mentor L1-L2 |
| **L4** | Multiple systems / platform | Define org-wide architecture patterns; make build-vs-buy decisions; influence industry practice |
| **L5** | Industry / ecosystem | Create new architectural patterns adopted across the industry; redefine what's possible |

**Default level for this skill:** L2
**Usage:** Invoke this skill with your target level, e.g., "as an L3 migration architect, design..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

- You need to execute a database schema migration in production without downtime using expand-contract or online schema change tools
- You are planning a cloud migration (on-prem to cloud or between clouds) and need to apply the 6 R's framework
- You need to migrate a framework or library (e.g., jQuery→React, REST→GraphQL, Express→Fastify) gradually with feature flags
- You are porting a service from one language to another (Python→Go, Ruby→Elixir, JS→TS) using the strangler fig pattern
- You need to design a rollback plan for every phase of a migration with kill switches and reverse data sync
- You are running a parallel verification — comparing old system output against new system output — before cutting over
- You need to backfill or transform 100K+ rows of data with checkpointing, batching, and consistency verification
- You are migrating a large codebase and need a phased plan with stakeholder communication, risk assessment, and testing gates


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | system-architect | Current system architecture, target architecture, migration feasibility assessment |
| **This** | migration-architect | Migration strategy, phased rollout plan, rollback procedures, verification scripts |
| **After** | devops-engineer | CI/CD pipeline updates, infrastructure provisioning, deployment automation for the migration |

Common chains:
- **Chain**: system-architect → migration-architect → devops-engineer — Architect defines what to build; migration architect plans how to get there; DevOps builds the pipeline.
- **Chain**: database-designer → migration-architect → database-reliability-engineer — Schema design flows into migration plan; DBRE ensures reliability during and after the migration.

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
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): Discovery & Assessment
**Input:** Existing system (codebase, infra, DB, dependencies)  
**Steps:** 1) Inventory all services, databases, and dependencies 2) Score each component by complexity (1-5) 3) Map dependency graph 4) Identify highest-risk components 5) Build migration wave plan  
**Output:** Scored inventory + dependency map + migration wave sequencing plan

<!-- DEEP: 10+min -->
### Phase 2 (~30 min): Pattern Selection & Proof of Concept
**Input:** Assessment results and constraints (time, budget, downtime tolerance)  
**Steps:** 1) Apply migration strategy decision tree 2) Select pattern (Strangler/Parallel/Lift-and-Shift/etc.) 3) Build PoC on 1-2 low-risk components 4) Validate approach with real data and traffic 5) Document pattern with code templates  
**Output:** Validated migration pattern + PoC results + reusable templates

<!-- DEEP: 10+min -->
### Phase 3 (~20 min): Data Migration Execution
**Input:** Source database schema and target schema design  
**Steps:** 1) Apply Expand-Contract for zero-downtime schema changes 2) Set up dual-write or CDC pipeline 3) Run backfill with checkpointing (resumable) 4) Verify consistency (row counts + checksums + business queries) 5) Cut over reads, monitor, cut over writes  
**Output:** Migrated database with verified consistency, rollback path ready

<!-- DEEP: 10+min -->
### Phase 4 (~15 min): Application Migration
**Input:** Validated patterns, migrated data plane  
**Steps:** 1) Migrate by wave (low-risk first) 2) Route percentage of traffic via feature flags/canary 3) Compare old vs new responses (diffing system) 4) Increase traffic 10% → 25% → 50% → 100% with monitoring gates 5) Keep old system in read-only mode for bake period  
**Output:** Application running on target platform with rollback capability

<!-- DEEP: 10+min -->
### Phase 5 (~25 min): Verification & Decommission
**Input:** Fully migrated system in production  
**Steps:** 1) Complete bake period (24-72h depending on component) 2) Run final data integrity reconciliation 3) Verify all monitoring/alerting operational on new system 4) Decommission old system (after confirmed no rollback needed) 5) Conduct retrospective, document lessons learned  
**Output:** Old system decommissioned, migration complete, retrospective document
## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Migration architecture is inherently cross-functional — it spans databases, application code, infrastructure, and QA. A migration without coordination is a production incident waiting to happen.

### Decision Gates & Artifacts

- **Gate 1 — Architecture Assessed:** Migration requires system architecture assessment and dependency mapping from `system-architect`. Artifact: architecture dependency graph.
- **Gate 2 — Schema Designed:** Database migrations require schema design, index strategy, and DDL review from `database-designer`. Artifact: DDL-reviewed migration scripts with Up/Down.
- **Gate 3 — Deployment Orchestrated:** Zero-downtime deployment requires blue-green orchestration and backup verification from `devops-engineer`. Artifact: deployment runbook with rollback commands.
- **Gate 4 — Reliability Ensured:** Replication, failover, and backup integrity validated by `database-reliability-engineer` before cutover. Artifact: replication lag and failover test report.
- **Artifact:** Migration runbook with per-phase rollback plan, data integrity reconciliation report, migration retrospective document.

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

### Route to Other Skills

| If the Request Is About | Route To |
|--------------------------|----------|
| Architecture assessment, service boundaries, dependency mapping | `system-architect` |
| Schema design, index strategy, DDL review, query migration | `database-designer` |
| Deployment orchestration, blue-green coordination, backup verification | `devops-engineer` |
| Database replication, failover testing, backup integrity | `database-reliability-engineer` |
| Data access layer changes, API versioning, dual-write implementation | `backend-developer` |

## Proactive Triggers
<!-- QUICK: 30s — when to proactively notify stakeholders -->

| Trigger | Notify | Why |
|---------|--------|-----|
| Migration backfill progress falls >20% behind schedule | Project Manager, Backend Developers | Cutover date at risk; throughput investigation or resource reallocation needed |
| Replication lag exceeds 2 seconds sustained for >5 minutes | DBA, DevOps, Backend Developers | Old system falling behind; throttling or pause required to protect rollback capability |
| Data reconciliation check fails (row count or checksum mismatch) | DBA, Backend Developers, QA | Data integrity at risk; halt migration until root cause identified and fixed |
| Dual-write error rate exceeds 0.1% for either target | Backend Developers, DBA | Silent data loss possible; write verification failing; investigate write path immediately |
| Production performance degradation >15% during backfill window | Performance Engineer, DevOps, Project Manager | User impact; throttle backfill or reschedule to lower-traffic window |
| Migration window timing conflicts with release freeze or holiday moratorium | Project Manager, Product Strategist | Reschedule migration; never run migrations during change freezes |
| Third-party dependency for migration fails (CDC connector, cloud service, API) | System Architect, DevOps, Project Manager | Migration blocked; contingency plan or workaround activation needed |

## Production Checklist

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

## What Good Looks Like

> When migration architecture is executed flawlessly, every migration has a phased plan with rollback checkpoints at each phase, data integrity is verified with row counts, checksums, and business-level reconciliation before cutover, feature flags gate every new code path so rollback takes seconds not hours, replication lag is monitored and never exceeds thresholds, the pre-mortem's top three failure modes have automated triggers, and the cutover window is measured in minutes — the business continues operating without detecting the migration happened.

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


**What good looks like:** Migration plan with phases, rollback steps at each phase, and success criteria. Data integrity verified with pre/post migration checks. Cutover window < 2 hours. Rollback tested and timed. Stakeholder communication plan distributed.

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
9. **Never migrate and refactor simultaneously:** Either lift-and-shift (same logic, new platform) OR refactor-and-migrate (new logic). Doing both at once makes <!-- DEEP: 10+min -->
debugging impossible.
10. **Conduct a pre-mortem before every migration:** "The migration failed. What went wrong?" Write down the top 3 causes. Those are your rollback triggers and monitoring priorities.

## Error Decoder
<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|------------|-----|--------|
| Database migration silently corrupted 50K customer records | Migration script applied UPDATE without WHERE clause; no pre-migration backup verified; no data integrity checks before cutover | Always verify backup is restorable before migration; add WHERE clause linting in CI; run pre/post migration reconciliation queries | A migration without a verified rollback isn't a migration — it's a gamble with customer data |
| Incremental migration planned for 3 months still running after 18 months | No checkpointing; migration couldn't resume from failures; each restart started from the beginning | Batch data migration with checkpointing (save progress every 1K rows); use CDC for ongoing sync; set a deadline with automated escalation | Incremental without checkpointing is a death march — design every migration for resumability |
| Big-bang migration rolled back at 3 AM after a 12-hour outage | Hidden dependency discovered mid-migration; shared database accessed by 3 unannounced services | Before any migration conduct a full dependency audit — count every API consumer, ETL job, and webhook; add 50% buffer to every time estimate | "It's just a schema change" — until a forgotten cron job breaks your rollback in the middle of the night |
| Dual-write to old and new databases but only old data persisted | Dual-write code silently swallowed errors to the new database; team assumed it worked because no alerts fired | Add write-verification after every dual-write operation; monitor error rates for both databases separately; run periodic consistency reconciliation | If you're not monitoring both sides of a dual-write you only have one database |
| Schema migration blocked reads for 30 minutes in production | Direct ALTER TABLE on a 50M-row table caused an extended table lock | Use online schema change tools: gh-ost for MySQL, pgroll for PostgreSQL; always run CREATE INDEX CONCURRENTLY instead of blocking CREATE INDEX | A blocking ALTER on a large table isn't a migration — it's a planned outage by another name |

## Anti-Patterns
<!-- STANDARD: 3min — patterns that predictably fail -->

| Anti-Pattern | Why It Fails | Correct Approach |
|---|---|---|
| Dropping old column in the same deploy that adds replacement | Rollback impossible — if new column has bugs, you can't go back to old; zero-downtime lost | Expand-Contract: add new column → dual-write → backfill → switch reads → remove old (separate deploys) |
| Running migration script without WHERE clause | One typo corrupts entire table; no way to resume from failure point; rollback requires full restore | Always include WHERE clause with batching condition; run on sample first; never UPDATE or DELETE without explicit filter |
| Assuming "it's just a schema change" without dependency audit | Hidden consumers break silently: cron jobs, reporting queries, ETL pipelines, unregistered services | Run full dependency audit before every migration: count all API consumers, direct DB readers, ETL jobs, and webhooks |
| Manual migration execution in production terminal | No audit trail; fat-finger risk; can't resume if SSH drops; no one else knows what was run | All migrations run through CI/CD pipeline; idempotent scripts; logged output with timestamps; no human-in-terminal execution |
| Delaying rollback test until migration day | Rollback script has syntax errors; untested rollback takes 10x estimated time; outage extends | Test rollback in staging for every migration phase; CI pipeline validates apply-up → test → rollback → test cycle |
| Using big-bang approach because "expand-contract takes too long" | 12-hour outage when hidden dependency breaks; no incremental verification; all-or-nothing gamble | Expand-contract costs calendar time but zero downtime; big-bang saves calendar time but guarantees downtime window |
| No feature flag gating new code paths | If migration fails, you must redeploy old code; deploy takes minutes, feature flag takes seconds | Feature-flag every new migration path; rollback = disable flag (seconds) not redeploy (minutes) |
| Decommissioning old system the day after cutover | Latent bugs surface after 48 hours; data edge cases discovered by users; no fallback available | Minimum bake: 24h simple, 48h API, 72h full-stack, 7-30 days financial; keep old system in read-only mode during bake |

## Footguns
<!-- DEEP: 10+min — war stories from system migrations -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| "Strangler Fig" migration planned for 8 weeks has been running for 18 months — the old system is still processing 40% of traffic, the new system has been in "almost done" status for 14 months, and the team can't name the completion criteria | A healthtech company started a Strangler Fig migration from a monolith to microservices in January 2023. Planned duration: 8 weeks. By July 2024 (18 months later): 60% of endpoints migrated, remaining 40% were the "hard ones" (complex business logic, no tests, original authors had left). The team had been saying "2 more sprints" since sprint 8. Two senior engineers quit out of frustration. The migration consumed 6,000 engineering hours. | The Strangler Fig had no hard cutover date — the "strangle until complete" pattern became "strangle until we get bored." No completion criteria were defined: "when all endpoints are migrated" is not a criterion, it's a tautology. The remaining endpoints were the hardest ones, but estimates were based on the easy ones. | **Every migration needs an exit gate with a deadline.** Define: "Migration is complete when X% of traffic/endpoints are moved AND the remaining Y are explicitly deprioritized with a business case for staying." Set a hard cutover date: "On [date], the old system enters read-only mode. Remaining unmigrated endpoints will be rebuilt on the new system from scratch." The Strangler Fig without a deadline is a zombie migration — it consumes resources forever without ever completing. Duration of migration should be measured and tracked as a KPI. |
| Dual-wrote to old and new databases for 4 weeks during migration — data diverged within 48 hours because the new system's validation logic rejected 3% of writes that the old system accepted silently | A logistics company ran dual-write to old (PostgreSQL) and new (DynamoDB) databases during a 4-week migration in September 2024. Within 48 hours, data divergence was detected: the new system validated phone numbers and rejected non-E.164 format numbers (3% of records). The old system accepted them as-is. By day 3, 12,000 records existed in the old database but not the new one. When the team cut over to the new system, customers with "invalid" phone numbers couldn't receive delivery notifications. The migration was rolled back. Data reconciliation took 2 weeks. | Dual-write assumes both systems apply identical business logic. They didn't. No comparison checkpoint was automated — the team manually sampled 100 records daily, which wasn't enough to catch the 3% divergence rate. The inconsistency was discovered by customers, not monitoring. | **Dual-write requires automated reconciliation, not manual sampling.** Run a full-row-count comparison every hour: `SELECT count(*) FROM old_db.users` vs `SELECT count(*) FROM new_db.users`. If counts diverge by >0.1%, halt migration. Run a hash-based comparison on a 5% sample every hour: `SELECT md5(row_to_json(t.*)::text) FROM ...`. Any mismatch triggers investigation BEFORE cutover. Better yet: avoid dual-write if possible — prefer read-only shadowing first, then cut over writes atomically. |
| Migration tested on a production-sized staging database (50M rows, 4 hours) — in production with real traffic, row locks and replication lag extended runtime to 14 hours and locked critical tables for the last 3 hours | A fintech company tested their database migration on a 50M-row staging clone in August 2024. The test took 4 hours — within their 6-hour maintenance window. In production: real traffic caused row-level locks that the migration's `ALTER TABLE` waited on, replication lag on the read replica hit 45 minutes (vs. 2 minutes in staging), and an unplanned ANALYZE kicked off mid-migration. Total runtime: 14 hours. Critical tables were locked for the last 3 hours when the migration had to wait for a long-running reporting query. 6-hour maintenance window overrun by 8 hours. Customer impact: degraded service for 14 hours. | Staging testing didn't simulate concurrent traffic — the database was idle during the test migration. Production had 2,000 QPS of read traffic causing row locks, replication, and autovacuum interference. The maintenance window didn't account for "what if it takes 2x the estimate?" | **Test migration timing on a database with simulated production traffic.** Before migration: (1) run the exact migration steps on staging with `pgbench` or similar generating realistic QPS, (2) check `pg_stat_activity` for lock waits during migration, (3) check replication lag every 60 seconds — if it exceeds 5x baseline, the migration has a serialization bottleneck. Maintenance window = 3x the worst-case test time with traffic. Never schedule migrations in a window that can't accommodate a 3x overrun. |
| Decommissioned the old API 24 hours after cutover — a nightly batch job that ran at 2 AM against the old API had no equivalent on the new system and failed silently for 3 days before anyone noticed | A retail platform migrated their order management API in March 2024. Cutover: Friday 10 PM. Old API decommissioned: Saturday 10 PM (24-hour bake). Monday morning: warehouse team reported that weekend orders weren't being fulfilled. Investigation: a nightly batch job that ran at 2 AM Sunday against the old API (`GET /orders?since=...`) was hardcoded with the old API URL. The batch job had been written by a contractor 3 years earlier — no documentation, no monitoring, no team knew it existed. 3 days of orders (14,000 orders, $890K revenue) were delayed. | The 24-hour bake period was too short to discover all system dependencies. Nightly batch jobs and cron jobs often run on 24-hour cycles — a 24-hour bake guarantees missing at least one run. No dependency audit had identified this batch job because it wasn't in any service catalog. | **Minimum bake periods by criticality: 24h simple, 72h API, 7 days data pipeline, 30 days financial.** During bake: run the old system in read-only mode, capture all requests to it, and audit for unknown consumers. Alert on any request to the old API during bake — each one is an undocumented dependency. Before cutover: run a dependency audit that includes not just registered API consumers, but also batch jobs, cron expressions, ETL pipelines, and hardcoded URLs in config files. |
| Feature-flagged the new code path for 10% of traffic — flag evaluation happened on every request including the 90% going to the old path, adding 35ms latency per request, P99 API latency went from 180ms to 320ms, customers noticed | A SaaS company feature-flagged their new billing calculation engine in October 2024. The flag was evaluated on 100% of requests (not just the 10% going to the new path) because the flag check was in middleware before the routing decision. The flag evaluation required a Redis call (15ms) plus JSON parsing of a complex targeting rule (20ms). P99 latency increased by 78% across all traffic. Customer complaints about "slow checkout" started within 2 hours. The team initially blamed the new engine's performance — but the 90% of traffic on the old path was also slower because of the flag evaluation overhead. | Feature flag evaluation cost was not profiled before deployment. The flag was placed in the hot path (every request) instead of at the routing layer (only requests going to the new path). No latency regression testing included the flag evaluation overhead. | **Profile feature flag evaluation separately from the code path it gates.** Before deploying: (1) measure flag evaluation latency in isolation (P50, P95, P99), (2) if flag evaluation adds >1ms at P95, it needs to be at the routing layer, not the middleware layer, (3) always test latency with the flag ON and OFF at both 0% and 100% rollout — the 90/10 split is the most dangerous configuration because overhead affects everyone but only 10% get the new behavior. Flag evaluation should be a local, in-memory operation — if it requires a network call, you're doing it wrong. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can write a migration script but every migration you've run required at least one rollback — and you don't have a postmortem for any of them | You've led a migration that completed on schedule with <1 hour of user-visible impact, and you have the post-migration report with actual vs. planned downtime, data integrity validation, and lessons learned | An engineering director says "we need to migrate our payment processing system with zero downtime and zero data loss — 99.999% availability, $2M/hour cost of failure" — you deliver a plan, execute it, and the business never notices |
| You think migrations are technical problems solved by better scripts and bigger maintenance windows | You think migrations are coordination problems — your migration plans include dependency audits, stakeholder communication timelines, rollback decision trees, and bake period criteria, not just technical steps | You can look at a proposed migration plan and within 30 minutes identify the 3 highest-risk assumptions — and when those exact risks materialize, your contingencies are already in place |
| Your migration rollback plan is "restore from backup and hope" — it's never been tested | Your rollback plan is tested in staging for every migration phase, and your CI pipeline validates apply-up → verify → rollback → verify before any production run | You've designed a migration strategy that saved a company from a multi-day outage — the rollback took 90 seconds instead of 8 hours because you architected for reverseability from day one |

**The Litmus Test:** A company needs to migrate their core database (8TB, 500M rows, 10,000 QPS peak) from self-hosted PostgreSQL to managed PostgreSQL with <5 minutes of write downtime. Their last attempt (by a different team) caused a 14-hour outage. Can you design a migration strategy that the CTO will bet their job on? If your strategy involves a big-bang cutover with a maintenance window, you're L1. Masters design for reversibility at every step and have survived at least one migration that would have been catastrophic without their rollback plan.

## Deliberate Practice

```mermaid
graph LR
    A[Build] --> B[Measure<br/>failure modes] --> C[Study<br/>post-mortems] --> D[Re-build<br/>with constraints] --> A
```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Rebuild an existing system from scratch, then compare your design with the original | Monthly |
| **Competent** | Add a new constraint (10x data, zero downtime, etc.) to a familiar design and re-architect | Quarterly |
| **Expert** | Design the same system under 3 conflicting constraint sets; write a decision record for each | Quarterly |
| **Master** | Teach a junior to design a system; your role is to ask questions, not give answers | Monthly |

**The One Highest-Leverage Activity:** Every quarter, take a system you built 6+ months ago and redesign it from scratch with what you know now. Write down what changed and why.

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
