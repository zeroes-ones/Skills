---
name: analytics-engineer
description: >
  Use when building dbt data models, designing metric layers, enabling self-service BI (Looker/Metabase/Lightdash),
  running A/B tests, optimizing SQL performance, designing event tracking, or building data quality frameworks.
  Handles dbt project architecture, semantic layer design, experimentation methodology, SQL tuning, data storytelling,
  and BI governance. Do NOT use for raw ETL/ELT pipeline construction, statistical modeling, ML engineering,
  or infrastructure provisioning.
license: MIT
tags:
- analytics
- dbt
- bi
- metrics
- sql
- experimentation
- data-modeling
- looker
author: Sandeep Kumar Penchala
type: data
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 4000
chain:
  consumes_from:
  - business-intelligence-engineer
  - data-engineer
  - data-scientist
  feeds_into:
  - business-intelligence-engineer
  - data-scientist
  - demand-generation
  - growth-engineer
  - product-manager
  - revops-manager
  - seo-specialist
---
# Analytics Engineer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Bridge raw data and actionable business insight. This skill covers dbt project design and patterns
(model layers, incremental models, snapshots, macros, tests), metric definition (semantic models,
metric types, time dimensions), BI architecture (semantic layer vs direct query, caching, row-level
security), data modeling for analytics (wide tables vs star schema, pre-aggregation, denormalization),
experimentation (A/B test design, sample size, statistical significance, SRM), SQL optimization
(CTEs vs subqueries, window functions, query plans, materialization), and data visualization
principles (chart selection, dashboard design, data storytelling).
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional work and amateur guessing:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify domain currency.** Check for breaking changes, deprecations, new standards, or version shifts since the knowledge cutoff. | [STALE_RISK] Outdated advice breaks real systems. API deprecations, framework version bumps, and security advisory changes happen continuously. Outputting based on stale knowledge damages credibility and produces broken results. | Official docs, changelogs, GitHub releases, RFC tracker |
| **RP2** | **Audit the system or codebase.** Read relevant files. Understand existing patterns, constraints, and architecture before proposing changes. | [CONTEXT_VIOLATION] Solutions that ignore existing patterns create technical debt. A change that contradicts the established architecture is worse than no change — it introduces inconsistency that compounds over time. | Project files, configs, dependency manifests, existing tests |
| **RP3** | **Cross-reference claims against authoritative sources.** Every factual assertion needs a verifiable source. Mark each: [VERIFIED], [COMPUTED], or [ESTIMATED]. | [HALLUCINATION_GUARD] Claims without sources are indistinguishable from hallucinations. The #1 cause of incorrect output is treating assumptions as facts. Source tagging prevents this. | Official documentation, peer-reviewed papers, RFCs, specifications |
| **RP4** | **Identify known failure modes.** Before recommending, list what commonly breaks. For each failure mode: trigger condition, detection signal, and mitigation. | [FAILURE_BLINDNESS] Every domain has known failure patterns. Output that doesn't address them is dangerously incomplete. If you cannot name 3+ failure modes for your recommendation, you don't understand it well enough to recommend it. | Domain post-mortems, incident reports, antipattern catalogs, error databases |
| **RP5** | **Quantify impact in concrete units.** Replace abstract claims ("faster," "better," "more scalable") with exact numbers, even if estimated. | [VAGUENESS_PENALTY] "Faster" is unverifiable. "Reduces p95 latency from 340ms to 120ms (±15ms)" is verifiable. Abstract adjectives hide ignorance behind confidence. Concrete numbers expose gaps. | Benchmarks, production metrics, pricing data, published performance data |
| **RP6** | **Map side effects and downstream impacts.** What else breaks? Which dependencies are affected? Which downstream consumers need updating? | [CASCADE_BLINDNESS] Changes to one component ripple outward. A fix in module A can break module B that depends on A's old behavior. Map the blast radius before acting. | Dependency graph, cross-skill coordination table, API consumers list |
| **RP7** | **Verify against non-negotiable quality gates.** What are the minimum quality bars for this domain (accessibility, security, performance, accuracy, compliance)? | [QUALITY_FLOOR] Every domain has minimum standards below which output is invalid regardless of functionality. Missing WCAG AA = broken. Leaking credentials = broken. Silent data loss = broken. | Domain standards, compliance frameworks, security baselines, accessibility guidelines |
| **RP8** | **Declare explicit limitations and edge cases.** What does this NOT handle? What are the known boundaries? What scenarios are explicitly out of scope? | [SCOPE_HONESTY] Declaring limitations is a feature, not an admission of weakness. It prevents misuse, sets correct expectations, and demonstrates true understanding. Every solution has boundaries — naming them is professional. | This SKILL.md, domain literature, edge case databases |

**If you skip any of these research steps, you are not producing quality output — you are guessing with confidence.** Guessing wastes time, breaks systems, and destroys trust. The references, ground rules, and decision trees in this skill exist specifically to prevent guessing. Use them.

> **Compliance:** Research must be executed before any substantial output. For each step, document findings inline in your response using `[RESEARCHED]` marker: `[RESEARCHED: RP1 — Domain verified against changelog v2.4. No breaking changes since cutoff.]`. Partial research = partial quality. Zero research = zero credibility.



### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

**The RP1-RP8 cycle above is NOT a one-time gate.** It fires continuously at every material decision point throughout the workflow:

| Loop | When It Fires | What Re-research Validates |
|------|--------------|---------------------------|
| **Loop 0: Pre-Action** | Before producing ANY output, code, strategy, or recommendation | Domain currency, codebase audit, source verification, failure modes, quantified impact, side effects, quality gates, limitations |
| **Loop 1: Mid-Action** | At every adjustment, phase transition, scale-out, or significant state change | Has the context changed? Are the original assumptions still valid? Has new information invalidated the Loop 0 conclusions? |
| **Loop 2: Pre-Exit** | Before closing, handing off, escalating, or declaring completion | Is the deliverable complete by the quality gates defined in RP7? Are all limitations declared (RP8)? Have failure modes been addressed (RP4)? |
| **Loop 3: Post-Action** | After completion: compare expected vs. actual outcome | What was the efficiency ratio (actual / theoretical max)? What learnings emerged? What should be fed back into the pattern database for future decisions? |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:
```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. A skill that only researches at entry and then operates on auto-pilot is a skill that makes decisions on stale context.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

**Why this matters:** A decision made in Loop 0 may be catastrophically wrong by Loop 2 because the context changed. Markets move. Requirements shift. Dependencies update. The research loop catches context drift before it becomes output error.

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence.



## Route the Request
<!-- STANDARD: 3min -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("dbt_project.yml")` OR `file_contains("**/*.sql", "{{\\s*ref\\(")` | Domain: **dbt Data Modeling**. Jump to "Sub-Skills > dbt Data Modeling" and "Core Workflow > Phase 1." |
| A2 | `file_exists("**/semantic_models/**/*.yml")` OR `file_contains("**/*.yml", "metric:|semantic_model:")` | Domain: **Metric Layer Design**. Jump to "Sub-Skills > Metric Layer Design." |
| A3 | `file_contains("**/*.{py,sql,md,R}", "experiment|A/B.test|power.analysis|SRM|CUPED")` OR `file_exists("**/experiments/**")` | Domain: **A/B Test Design & Analysis**. Jump to "Sub-Skills > A/B Test Design & Analysis." |
| A4 | `file_contains("**/*.sql", "EXPLAIN|query.plan|partition.by|cluster.by|materialized")` OR `file_exists("**/performance/**")` | Domain: **SQL Performance Tuning**. Jump to "Sub-Skills > SQL Performance Tuning." |
| A5 | `file_contains("**/*.lkml", "explore:|view:|dimension:|measure:")` OR `file_exists("**/looker/**")` OR `file_exists("**/metabase/**")` | Domain: **Self-Service BI Enablement**. Jump to "Sub-Skills > Self-Service BI Enablement." |
| A6 | `file_contains("**/*.{yml,yaml,json}", "tracking.plan|event.schema|snowplow|segment|rudderstack")` OR `file_exists("**/tracking/**")` | Domain: **Event Tracking Design**. Jump to "Sub-Skills > Event Tracking Design." |
| A7 | `file_contains("**/*.{md,ipynb}", "dashboard|visualization|storytelling|executive.summary")` OR `file_exists("**/dashboards/**")` | Domain: **Data Storytelling**. Jump to "Sub-Skills > Data Storytelling." |
| A8 | `file_contains("**/*.yml", "dbt.test|great_expectations|elementary|monte.carlo|freshness")` OR `file_exists("**/tests/**")` OR `file_exists("**/quality/**")` | Domain: **Data Quality & Observability**. Jump to "Sub-Skills > Data Quality & Observability." |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Build or refactor a dbt model → Jump to "Sub-Skills > dbt Data Modeling"
├── Define company-wide KPIs / metric layer → Go to "Sub-Skills > Metric Layer Design"
├── Design or analyze an A/B test → Jump to "Sub-Skills > A/B Test Design & Analysis"
├── Optimize slow SQL queries → Jump to "Sub-Skills > SQL Performance Tuning"
├── Enable self-service BI for stakeholders → Go to "Sub-Skills > Self-Service BI Enablement"
├── Design event tracking / instrumentation → Jump to "Sub-Skills > Event Tracking Design"
├── Create data visualizations / dashboards → Go to "Sub-Skills > Data Storytelling"
├── Set up data quality monitoring → Jump to "Sub-Skills > Data Quality & Observability"
├── Need raw data pipelines first → Invoke `data-engineer` skill instead
├── Need statistical / ML modeling → Invoke `data-scientist` skill instead
├── Need growth experiments → Invoke `growth-engineer` skill instead
├── Need product metrics framework → Invoke `product-manager` skill instead
└── Not sure where to start? → Start at "Core Workflow > Phase 1 (Data Modeling Foundation)"
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|---|---|---|
| **R1** | **REFUSE to build a dashboard or metric without a documented decision question.** Every deliverable must answer: "What will you do differently if this number moves?" | Trigger: Before creating any BI artifact — check if the user stated a decision question. If `file_contains("**/*.{md,yml}", "decision|question|action.if")` returns no matches in project docs, trigger fires. | STOP. Respond: "I cannot build this dashboard/metric until we define the decision it informs. Please answer: 'What specific action will you take differently if this number moves?' Document the answer in a DECISIONS.md or project README before proceeding." |
| **R2** | **REFUSE to define a metric without an owner, SQL definition, and data lineage.** "Revenue" without these three elements is semantic drift waiting to happen. | Trigger: Before creating any metric definition — grep for `owner:` and `sql:` in the metric YAML. If either is missing from the proposed metric file, trigger fires. | STOP. Respond: "Every metric needs: (1) an owner/team, (2) the exact SQL definition, (3) lineage back to source tables. Please provide all three before I define this metric." |
| **R3** | **DETECT and BLOCK self-service BI without field descriptions.** A Looker explore or Metabase question without field documentation creates more confusion than it solves. | Trigger: grep `description:` across all dimension/measure definitions. If `<50%` of fields have non-empty descriptions, trigger fires. | STOP. Respond: "Self-service requires documentation. {N} of {M} fields lack descriptions. I will add descriptions for all fields before publishing. Confirm you want me to proceed with documenting all fields." |
| **R4** | **REFUSE to write deeply nested SQL (>3 levels of subquery) in dbt models.** Favor CTEs. Deep nesting is unreadable and unmaintainable during incidents. | Trigger: Before committing a dbt model — grep for `SELECT.*FROM.*\\(.*SELECT` nested beyond 2 levels. If 3+ levels of nested subqueries detected, trigger fires. | STOP. Respond: "This model contains {N} levels of nested subqueries. dbt models must use CTEs for readability. I will refactor to CTEs before committing. Proceed with refactor?" |
| **R5** | **STOP and admit uncertainty when data volume assumptions change the recommendation.** If you haven't seen the query plan or don't know the row count, say so — don't guess. | Trigger: Before recommending a materialization strategy or query pattern — check if row count / table size was provided. If `file_contains("**/*.{md,sql,yml}", "row.count|table.size|bytes|partition.size|rows")` returns no data, trigger fires. | STOP. Respond: "My recommendation depends on data volume. Without row counts or table sizes, I'm guessing. Please provide: approximate row count, daily growth rate, and query latency requirements. Until then, I'll flag all assumptions explicitly." |
| **R6** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R7** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

## Anti-Hallucination
<!-- STANDARD: 3min -->
- **Admit uncertainty**: If you are unsure about any API, version, configuration, or domain-specific fact, state "I am not certain about X — consult [authoritative source]" rather than guessing.
- **Flag your knowledge cutoff**: State "My training data ends in [date]. Verify current documentation for any version-specific details or newly released features."
- **Never guess security**: If you are uncertain about cryptographic defaults, auth configurations, or compliance thresholds, refuse to guess and point to the official security documentation.
- **VERIFIED**: Mark all definitive claims with **[VERIFIED]** when confirmed by documentation. Mark uncertain claims with **[BEST-KNOWN]** and provide the citation path to verify.

##
## The Expert's Mindset
<!-- STANDARD: 3min -->

Masters of analytics engineer don't just build — they build **the right thing, at the right time, with the right trade-offs**. They think in systems, not tasks.

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
<!-- STANDARD: 3min -->

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single component/module | Implement a well-defined piece following established patterns |
| **L2** | Feature or service | Design and build a complete feature; make tech choices within team conventions |
| **L3** | System or product area | Define architecture for a product area; set team tech standards; mentor L1-L2 |
| **L4** | Multiple systems / platform | Define org-wide architecture patterns; make build-vs-buy decisions; influence industry practice |
| **L5** | Industry / ecosystem | Create new architectural patterns adopted across the industry; redefine what's possible |

**Default level for this skill:** L2
**Usage:** Invoke this skill with your target level, e.g., "as an L3 analytics engineer, design..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use
<!-- STANDARD: 3min -->

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Designing a dbt project: model layering (staging → intermediate → marts), incremental strategies, snapshot design
- Defining a company-wide metric layer: single source of truth for "DAU," "Revenue," "Churn Rate"
- Building self-service BI with Looker, Metabase, Lightdash, or Superset for non-technical stakeholders
- Designing and analyzing A/B tests with statistical rigor: power analysis, CUPED, SRM checks
- Optimizing slow SQL queries: CTE vs subquery tradeoffs, window functions, query plan reading
- Designing event tracking: naming conventions, property design, identity resolution
- Creating data visualizations that tell a story: chart selection, dashboard architecture, data storytelling
- Migrating from "Excel hell" or legacy BI to a modern analytics stack

## Decision Trees
<!-- STANDARD: 3min -->
**(QUICK)**

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### dbt Materialization Strategy

```
                     ┌──────────────────────────┐
                     │ START: Which dbt          │
                     │ materialization?          │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Need to store historical   │
                    │ versions of rows (SCD      │
                    │ Type 2)?                   │
                    └────┬──────────────────┬───┘
                         │ YES              │ NO
                    ┌────▼──────┐    ┌──────▼──────────┐
                    │ Snapshot  │    │ Table < 1M rows  │
                    │ (dbt      │    │ AND runtime <    │
                    │ snapshot) │    │ 5 min?           │
                    └───────────┘    └──┬──────────┬────┘
                                       │YES       │NO
                                  ┌────▼────┐ ┌───▼──────────┐
                                  │ View    │ │ Incremental:  │
                                  │ (always │ │ append-only?  │
                                  │ fresh)  │ └──┬───────┬────┘
                                  └──────────┘    │YES   │NO (mutating)
                                              ┌───▼──┐ ┌─▼─────────┐
                                              │Append│ │Merge/delete│
                                              │+ insert│ │+ insert    │
                                              │overwrite│ │overwrite   │
                                              └──────┘ └────────────┘
```

**When to choose Snapshot:** Historical tracking needed (SCD Type 2), audit trail required, or regulatory timestamp tracking.
**When to choose View:** Small reference tables (<1M rows), always want live data, zero storage cost, acceptable latency.
**When to choose Incremental:** >1M rows or runtime >5 min — append-only for event data, merge for mutable entities.

### Metric Layer: dbt vs BI Tool vs Semantic Layer

```
                     ┌──────────────────────────┐
                     │ START: Where should this   │
                     │ metric be defined?         │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Used across multiple BI    │
                    │ tools or teams?            │
                    └────┬──────────────────┬───┘
                         │ YES              │ NO
                    ┌────▼──────┐    ┌──────▼──────────┐
                    │ Semantic  │    │ Metric requires   │
                    │ Layer     │    │ multi-table joins │
                    │ (dbt SL, │    │ or complex        │
                    │ Cube)     │    │ aggregations?     │
                    └───────────┘    └──┬──────────┬────┘
                                       │YES       │NO
                                  ┌────▼────┐ ┌───▼──────────┐
                                  │ dbt mart│ │ BI tool       │
                                  │ (SQL)   │ │ calculation   │
                                  │ single  │ │ (LookML, DAX) │
                                  │ source  │ │ simple formula │
                                  └─────────┘ └──────────────┘
```

**When to choose Semantic Layer:** Multi-tool consumption (Looker + Metabase + embedded), need centralized governance, access control per metric.
**When to choose dbt mart:** Complex logic requiring SQL, need version control and testing, single source of truth in warehouse.
**When to choose BI tool:** Single-tool consumption only, simple arithmetic (ratio, sum), rapid prototyping by analysts.

### A/B Test Design

```
                     ┌──────────────────────────┐
                     │ START: Designing an       │
                     │ experiment                │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Expected effect size       │
                    │ < 5% relative lift?        │
                    └────┬──────────────────┬───┘
                         │ YES              │ NO (large)
                    ┌────▼──────┐    ┌──────▼──────────┐
                    │ Large     │    │ Can randomize     │
                    │ sample    │    │ at user level?    │
                    │ needed    │    └──┬──────────┬────┘
                    │ (power    │       │YES       │NO
                    │ analysis) │  ┌────▼────┐ ┌───▼──────────┐
                    └──┬────────┘  │Standard │ │Switchback/    │
                       │           │user-level│ │geo-level      │
                  ┌────▼───────┐  │A/B test │ │experiment     │
                  │ Use CUPED  │  └──┬───────┘ │(market test)  │
                  │ variance   │     │         └───────────────┘
                  │ reduction  │     │
                  └──┬─────────┘     │
                     │          ┌────▼──────────┐
                     ▼          │ Secondary:     │
              ┌──────────┐     │ Multiple MHT   │
              │ Calculate │     │ correction if   │
              │sequential │     │ multiple metrics│
              │ testing if│     │ or segments     │
              │continuous │     └────────────────┘
              │monitoring │
              └───────────┘
```

**When to use CUPED:** Small effects (<5%), want to reduce variance using pre-experiment covariates, increase statistical power without bigger sample.
**When to use Market/Switchback:** Cannot randomize at user level (network effects, supply-side constraints), use time-based or geo-based randomization.
**When to use sequential testing:** Continuous monitoring needed for safety, want early stopping for clear winners/losers — control false-positive rate.

### SQL Performance Tuning

```
                     ┌──────────────────────────────┐
                     │ START: Query too slow (>30s)?  │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Check EXPLAIN: full table      │
                    │ scan on large fact table?      │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────┐    ┌──────────▼──────────┐
                    │ Missing/  │    │ JOIN causing many-to- │
                    │ wrong     │    │ many explosion?       │
                    │ index/part│    └──┬──────────────┬────┘
                    │ key       │       │YES          │NO
                    │ → add     │  ┌────▼────┐ ┌──────▼─────────┐
                    │ cluster   │  │Fix grain│ │ CTE materialized │
                    │ key       │  │(pre-     │ │multiple times?   │
                    └───────────┘  │aggregate)│ └──┬──────────┬───┘
                                   └──────────┘    │YES      │NO
                                               ┌───▼──┐ ┌───▼───────┐
                                               │Use   │ │Window fn  │
                                               │temp  │ │optimization│
                                               │table │ │or partition│
                                               │or mat│ │pruning    │
                                               │CTE   │ └───────────┘
                                               └──────┘
```

**When to add partitioning/clustering:** Full scans on tables >10GB — partition by date, cluster by frequent filter columns.
**When to pre-aggregate:** Many-to-many JOIN causing row explosion — aggregate to target grain before joining, not after.
**When to use materialized CTE:** Same CTE referenced 3+ times — materialize to temp table to avoid redundant computation.

### Dashboard Design: Exploratory vs. Operational vs. Strategic

```
                     ┌──────────────────────────────┐
                     │ START: Dashboard type?         │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Need to monitor live systems   │
                    │ with alerts (p99 latency,     │
                    │ error rates)?                  │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────┐    ┌──────────▼──────────┐
                    │Operational│    │ For executive/board  │
                    │Dashboard  │    │ review (monthly/     │
                    │Auto-refresh│    │ quarterly)?          │
                    │<5 min data│    └──┬──────────────┬────┘
                    │Alerts on  │       │YES          │NO
                    │thresholds │  ┌────▼────┐ ┌──────▼─────────┐
                    └───────────┘  │Strategic│ │Exploratory     │
                                   │Dashboard│ │Dashboard       │
                                   │High-level│ │Interactive    │
                                   │KPIs,    │ │filters,       │
                                   │trends   │ │drill-down,    │
                                   │MoM/YoY  │ │ad-hoc analysis│
                                   └─────────┘ └───────────────┘
```

**When to build Operational:** Real-time monitoring, alerting, on-call response — use streaming data, auto-refresh, threshold alerts.
**When to build Strategic:** Executive review, board reporting — high-level KPIs, trend lines, MoM/YoY comparisons, snapshot data.
**When to build Exploratory:** Self-service analysis — interactive filters, drill-down capabilities, flexible date ranges, multi-dimensional pivots.

## Core Workflow
<!-- STANDARD: 3min -->
**(STANDARD)**

<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): dbt Project Design & Patterns

1. **Project Structure** — The standard layered approach:

   ```
   models/
   ├── staging/        # stg_stripe__payments.sql — 1:1 with source, rename + cast
   │                   #   Config: materialized='view' (cheap, always fresh)
   ├── intermediate/   # int_order_payments.sql — business logic, multi-source joins
   │                   #   Config: materialized='table' or 'ephemeral' (CTE)
   └── marts/          # fct_orders.sql — business-facing, single source of truth
                       #   Config: materialized='table' or 'incremental'
   ```

**What good looks like:** dbt project with model documentation, tests, and lineage. BI dashboard loads in under 5 seconds. All metrics have definitions documented in a shared glossary. Data freshness meets SLA for every report. No hard-coded table references in SQL — all ref()'d.

2. **Materialization Decision Matrix**:

   | Strategy | When | Pros | Cons |
   |---|---|---|---|
   | **View** | Simple transforms, always-current data | Zero storage, always fresh | Recomputes on every query |
   | **Table** | Complex joins, dashboard source tables | Fast queries, snapshotable | Must be rebuilt/re-run |
   | **Incremental** | Large fact tables (>100M rows), append-mostly | Fast builds, low cost | Complex logic, late data handling |
   | **Ephemeral** | Reusable CTEs, not queried directly | No storage, composable | Re-computed per downstream model |
   | **Snapshot** | SCD Type 2 dimensions | Tracks history automatically | Storage grows over time |

3. **Incremental Model Pattern**:

   ```sql
   {{
       config(
           materialized='incremental',
           unique_key='event_id',
           partition_by={'field': 'event_date', 'data_type': 'date'},
           on_schema_change='sync_all_columns'
       )
   }}
   SELECT * FROM {{ source('events', 'product_events') }}
   {% if is_incremental() %}
   WHERE event_date >= (SELECT MAX(event_date) FROM {{ this }})
   {% endif %}

   ```

4. **Snapshot (SCD Type 2) Strategy**:

   ```sql
   {% snapshot customer_dimension %}
   {{ config(target_schema='marts', unique_key='customer_id', strategy='check', check_cols=['plan_type', 'region', 'status']) }}
   SELECT * FROM {{ ref('stg_customers') }}
   {% endsnapshot %}
   -- dbt automatically adds: dbt_valid_from, dbt_valid_to, dbt_scd_id
   ```

5. **dbt Tests — The Minimum Viable Suite**:

   ```yaml
   models:
     - name: fct_orders
       columns:
         - name: order_id
           tests: [unique, not_null]
         - name: customer_id
           tests: [not_null, {relationships: {to: ref('dim_customers'), field: 'customer_id'}}]
         - name: amount
           tests: [not_null, {dbt_utils.accepted_range: {min_value: 0.01}}]
         - name: status
           tests: [not_null, {accepted_values: {values: ['pending', 'completed', 'cancelled']}}]

   ```

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.

  Complete when: Architecture diagram finalized, technology choices documented with rationale, and design reviewed by peers.
Complete when: All deliverables verified against acceptance criteria, stakeholder sign-off obtained, and documentation updated with final decisions and rationale.
Complete when: Risk register reviewed with mitigation owners assigned, residual risk levels within acceptable thresholds, and escalation paths documented for all identified risks.
Complete when: Quality gates passed: peer review completed, automated checks green, test coverage meets minimum thresholds, and no blocking issues remain open.
Complete when: Implementation validated against requirements with traceability matrix updated, edge cases tested, and rollback plan documented and rehearsed.
Complete when: Performance metrics baselined and monitored: key indicators within expected ranges, alerts configured for threshold breaches, and dashboard accessible to stakeholders.
Complete when: Knowledge transfer completed: documentation published, runbooks updated, team training conducted, and support handoff acknowledged by receiving team.
Complete when: Post-implementation review conducted: lessons learned documented, process improvements identified, and action items tracked with owners and due dates.

## Best Practices
<!-- STANDARD: 3min -->

1. **dbt models should be modular — one model, one concept.** A single model that joins 12 tables and produces 50 columns is a maintenance nightmare. Split into staging (1:1 with source, light cleaning), intermediate (business logic, joins), and marts (business-ready tables). Each model should have a clear, single purpose.

2. **Star schema is the default for analytics — denormalize only with purpose.** Fact tables with numeric measures, dimension tables with descriptive attributes. Wide tables (OBT) are acceptable for performance-critical dashboards with < 5 dimensions and no SCD Type 2 history. Kimball methodology over ad-hoc modeling every time.

3. **dbt tests are non-negotiable — uniqueness, not_null, referential integrity at minimum.** Custom data tests for business logic validation. Tests run as part of the pipeline, not as optional post-hoc checks. `dbt test --store-failures` preserves failure data for debugging. Schema tests catch bad data before it reaches dashboards.

4. **Materialization strategy is a performance and freshness contract.** Views for lightweight, always-fresh transformations. Tables for performance-critical models queried frequently. Incremental for large fact tables (> 1M rows/day). Ephemeral for reusable CTE logic. `materialized='incremental'` with `unique_key` and `merge_update_columns` for late-arriving updates.

5. **Documentation is code, not commentary.** Every model has a YAML description. Column descriptions explain what the field means in business terms, not just its data type. `dbt docs generate` and `dbt docs serve` should produce a browsable, trustworthy data catalog. Undocumented models are technical debt.

6. **SQL style guide enforced by automation.** Consistent formatting (lowercase keywords, trailing commas, meaningful aliases). sqlfluff or dbt pre-commit hooks enforce style in CI. Readable SQL is debuggable SQL. Nested subqueries beyond 2 levels are a refactoring signal.

7. **Metric definitions live in ONE place — the semantic layer, not individual dashboards.** dbt MetricFlow, LookML explores, or a metrics store ensures "revenue" means the same thing everywhere. Duplicate metric definitions are the #1 source of organizational data distrust. The semantic layer is the single source of truth for business logic.

8. **Data contracts between producers and consumers.** Schema, freshness SLA, and ownership for every dataset. Producers commit to not breaking the contract without notice. dbt model contracts with `constraints` enforce column types, nullability, and primary keys at build time.

9. **CTE chains beyond 5-7 signal refactoring.** dbt compiles CTE chains into single massive queries. Redshift/Postgres materialize every CTE. On large datasets, disk spillage starts around CTE #5. Use ephemeral materialization or split into multiple models.

10. **Freshness over perfection in operational dashboards.** A stale-but-perfectly-modeled dashboard is useless during an incident. Configure source freshness checks (`dbt source freshness`) with SLAs. Alert when data is late. Executives make decisions on stale data if they don't know it's stale.

## Error Recovery
<!-- STANDARD: 3min -->
**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Tool/command not found | Tool binary is not installed or not in the system PATH | First: Check installation with `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`). If that fails: Check `$PATH` and verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable. Last resort: Use a functionally equivalent alternative tool (e.g., `grep -r` instead of `rg`, `git` directly or GitHub API via `curl` instead of `gh`). | If PATH does not find it, either it is not installed or the shell cannot see it — never assume installation status from a "not found" error alone. |
| Permission denied | Incorrect file ownership, missing execute bits, expired credentials, or resource locked by another process | First: Check ownership with `ls -la [path]`. Fix with `chmod` or `sudo` as appropriate. For API errors (401/403), verify credentials have not expired with `echo $TOKEN` or check `~/.netrc`. If that fails: Refresh credentials by re-authenticating. For file permissions, check if locked by another process with `lsof [path]`. Last resort: Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS). | A 403 is far more likely to be stale credentials than a missing file permission — always check auth expiry first. |
| Command hangs or times out | Resource exhaustion (CPU/memory/disk), unresponsive network, or operation scope too large for default timeouts | First: Kill the process with `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an`. If that fails: Add verbose/debug flags (`--verbose`, `--debug`, `-v`). Check logs with `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency. Last resort: Split work into smaller batches with a retry loop and exponential backoff (1s, 2s, 4s, 8s). If network-related, add `--retry 3`. | Kill first, diagnose second — a hung process wastes resources you need for debugging. |
| Unexpected output or error message | Assumption mismatch: command output format changed, or the tool is being used in an unexpected context | First: Read the error message completely — the solution is in the last 3 lines. Search the exact error in the repo: `grep -r "[error text]"`. If that fails: Check GitHub issues for the tool (`gh issue list --repo owner/repo --search "[error keyword]"`) or Stack Overflow. Last resort: Simplify the approach. Break a complex one-liner into sequential commands; use a more basic tool with more steps. | The last 3 lines of an error message contain 80% of the diagnostic value — read those before searching the web. |
| Data integrity concern (wrong output, silent failure) | Pipeline bug, silent truncation, or unvalidated transformation corrupting data between source and output | First: Verify with a manual check — compare output against a known-correct baseline. Run validation: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"`. If that fails: Run the operation on a smaller subset first. Compare checksums with `shasum` or `md5`. Check for silent truncation with `wc -l` before and after. Last resort: Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay. | A silent data corruption that propagates for 3 hours is irrecoverable; a halted pipeline with an alert is fixed in 15 minutes. Always abort on integrity doubt. |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `data-engineer` | Raw data schemas, freshness SLAs, data dictionary, PII classification, partitioning strategy | Before building dbt models or defining metric sources |
| `data-scientist` | Metric calculation logic, experiment metric implementation, analysis dataset requirements | Before designing metric layers or experiment tracking tables |
| `business-intelligence-engineer` | BI tool configuration, dashboard requirements, self-service access patterns | Before building semantic layers or certified datasets |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `data-scientist` | Curated analysis datasets, experiment metric implementation, statistical function integration in dbt | Data scientists work with raw unmodeled data — analysis velocity plummets |
| `product-manager` | Metric taxonomy, event tracking specification, A/B test metric framework, dashboard requirements | Product decisions made without reliable metrics — strategy guesswork |
| `growth-engineer` | A/B test metric definitions, statistical analysis queries, activation funnel instrumentation, cohort definitions | Growth experiments have no measurement framework — can't validate impact |
| `revops-manager` | Revenue definitions, CAC/LTV calculations, ARR/MRR reporting, customer segmentation queries | Revenue operations fly blind — forecasting and planning impossible |

## Proactive Triggers
<!-- STANDARD: 3min -->

| Trigger | Action | Why |
|---------|--------|-----|
| dbt source freshness check fails — source table > 24 hours stale | Notify data-engineer, downstream consumers; pause dependent dashboard updates; investigate upstream pipeline | A green dbt run with stale data is worse than a red one — creates false confidence that dashboards are current |
| Two teams report conflicting "Revenue" or "DAU" numbers to executives | Escalate to metric governance lead; lock definition in semantic layer; add glossary entry with canonical formula and caveats | Semantic drift is invisible until executives compare numbers — one definition, one owner, one source prevents re-litigation |
| A/B test result shared as "statistically significant (p=0.04)" before pre-registered duration ends | Halt result sharing; flag as premature; enforce sequential testing or alpha-spending protocol | Peeking inflates false positive rate 5-20x — a p-value that looks significant today is often noise tomorrow |
| Dashboard load time exceeds 5 seconds for executive-facing reports | Profile query plan; add materialized views or aggregate tables; move heavy computation to dbt; implement BI cache | Executive trust in data erodes with every second of loading — if the CEO can't get an answer in a board meeting, the dashboard is dead |
| Incremental model reconciliation shows > 2% discrepancy vs source system | Investigate late-arriving data; extend lookback window; schedule end-of-month full refresh; add row-count reconciliation check | Incremental models are fast but leaky — trust requires periodic full reconciliation against source of truth |
| BI tool usage analytics show dashboard with zero views for 90+ days | Archive candidate; notify original stakeholder; redirect to maintained equivalent; free warehouse credits | Unused dashboards consume compute, confuse users, and dilute metric trust — archive aggressively |
| New data source added to warehouse without dbt source definition or freshness check | Add dbt source YAML with freshness SLA before any model references it; notify data-engineer | Sources without freshness monitoring are blind spots — you won't know data is stale until users report wrong numbers |
| Metric layer change proposed that would change historical reporting (e.g., "active user" definition) | Require impact analysis on all downstream dashboards; version the metric; communicate change to all consumers before deploying | Changing a metric definition retroactively breaks every historical comparison — version and communicate before, not after |

## State Log
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## What Good Looks Like
<!-- STANDARD: 3min -->

> dbt models run on a schedule, tests catch anomalies before dashboards update, and stale models are deprecated before anyone builds a report on them.

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.

### Cross-skills Integration

```bash
# Data pipeline → Analytics models → Data science
/data-engineer && /analytics-engineer && /data-scientist
# Product requirements → Analytics design → Growth experiments
/product-manager && /analytics-engineer && /growth-engineer
# Data engineers deliver clean datasets. Analytics engineers model for consumption. Data scientists run experiments.
```

## Deliberate Practice
<!-- STANDARD: 3min -->

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

## Anti-Patterns
<!-- STANDARD: 3min -->

- **dbt `ref()` vs `source()`**: `ref()` builds a DAG dependency — dbt knows model B depends on model A and runs them in order. `source()` references raw data with NO dependency tracking. If you `source('raw', 'events')` but someone upstream changes the schema, dbt can't warn you. **Total cost: $5,000-$25,000 in data downtime, broken dashboards, and engineering time debugging silent schema breakages that cascade through downstream models.**
- **dbt incremental models** with `unique_key` but without `merge_update_columns` — only NEW rows are inserted. Updates to existing rows are silently ignored. You get duplicate key errors OR stale data depending on the `on_schema_change` config. **Total cost: $10,000-$50,000 in bad business decisions driven by stale data — execs making pricing, inventory, or hiring calls from reports that silently diverged from source truth.**
- **`dbt test` runs schema tests (unique, not_null) AND data tests (custom SQL assertions) but they run AFTER the data is already in the warehouse. A uniqueness test failure means you've already loaded bad data. Use `dbt test --store-failures` to preserve failure data. **Total cost: $15,000-$75,000 in corrupted warehouse tables that require full rebuilds, stakeholder trust erosion, and delayed reporting cycles.**
- **CTE (Common Table Expression) chains with 15+ CTEs** in a single model: dbt compiles these into a single massive query. Redshift/Postgres materialize every CTE as an in-memory temp table. On large datasets, you hit disk spillage at CTE #5. Use ephemeral materialization (`+materialized: ephemeral`) or split into multiple models. **Total cost: $5,000-$20,000 in compute overruns — disk-spilled queries run 10-50x slower, blowing past warehouse credit budgets and delaying downstream SLAs.**
- **`dbt run` with `--select`** only runs the selected models. Downstream models that depend on the updated model are NOT auto-selected. If you `dbt run --select stg_orders` but `fct_orders` depends on it, `fct_orders` still has old data and you won't know until someone queries it. **Total cost: $10,000-$40,000 in incorrect executive reports and operational decisions made from stale downstream models — discovered days or weeks later when someone notices the numbers don't reconcile.**

## Production Checklist
<!-- STANDARD: 3min -->
**(STANDARD)**

- [ ] **dbt project structure follows best practices:** Staging, intermediate, and marts layers with clear separation of concerns
- [ ] **Materialization strategy documented per model:** View/table/incremental/ephemeral chosen with documented rationale; incremental models have `unique_key` and merge strategy
- [ ] **Tests passing in CI:** `dbt test` runs on every PR; schema tests (unique, not_null) + custom data tests for business logic
- [ ] **Source freshness monitored:** `dbt source freshness` runs on schedule; alerts on SLA breach; freshness displayed on dashboards
- [ ] **Documentation generated and accessible:** `dbt docs generate` produces browsable catalog; column descriptions in business terms
- [ ] **SQL style consistent:** sqlfluff or pre-commit hooks enforce formatting; no unformatted SQL in production models
- [ ] **Metric definitions centralized:** All metrics defined in semantic layer (dbt MetricFlow/LookML); no duplicate metric definitions across BI tools
- [ ] **Data contracts enforced:** Model contracts with constraints on column types, nullability, and primary keys; breaking changes communicated to consumers
- [ ] **Incremental models verified idempotent:** Full refresh produces identical results to incremental run; late-arriving data handled correctly
- [ ] **Lineage graph complete:** `dbt docs` lineage shows all upstream/downstream dependencies; no orphaned models
- [ ] **Performance SLAs met:** All models build within configured time limits; long-running models identified with `dbt ls --resource-type model --output json`
- [ ] **dbt package dependencies pinned:** Version constraints in `packages.yml`; no floating versions

## Gotchas
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Pipeline silently produces stale data due to missing freshness checks | $5K-$25K in bad decisions per week | Implement source freshness monitoring with dbt `source freshness` checks and automated alerts on SLA breach |
| Incremental model divergence from source of truth beyond 2% | $10K-$50K in incorrect executive reports per quarter | Schedule weekly full-refresh reconciliation; add row-count audit checks comparing incremental vs full-refresh output |
| Notebook results unreproducible due to kernel state and cell execution order | $20K-$100K per incident | Restart kernel and 'Run All' before sharing; pin dependencies in requirements.txt; set random seeds with documentation |
| Data leakage through improper train/test split before preprocessing | $10K-$100K in production model failures | Split before any `.fit_transform()`; use `Pipeline` objects; audit features for temporal or target leakage before training |
| Dashboard loading >5s erodes executive trust | $15K-$50K in lost stakeholder confidence | Profile query plans; add materialized views; push heavy compute to dbt; implement BI query cache with freshness SLAs |

| Gotcha | Cost | Fix |
|--------|------|-----|
| Pipeline silently produces stale data due to missing freshness checks | $5K-$25K in bad decisions per week | Implement source freshness monitoring with dbt `source freshness` checks and automated alerts on SLA breach |
| Incremental model divergence from source of truth beyond 2% | $10K-$50K in incorrect executive reports per quarter | Schedule weekly full-refresh reconciliation; add row-count audit checks comparing incremental vs full-refresh output |
| Notebook results unreproducible due to kernel state and cell execution order | $20K-$100K per incident | Restart kernel and 'Run All' before sharing; pin dependencies in requirements.txt; set random seeds with documentation |
| Data leakage through improper train/test split before preprocessing | $10K-$100K in production model failures | Split before any `.fit_transform()`; use `Pipeline` objects; audit features for temporal or target leakage before training |
| Dashboard loading >5s erodes executive trust | $15K-$50K in lost stakeholder confidence | Profile query plans; add materialized views; push heavy compute to dbt; implement BI query cache with freshness SLAs |

## Verification
<!-- STANDARD: 3min -->

- [ ] Run `dbt deps` — all dependencies resolve, no missing packages
- [ ] Run `dbt run --select state:modified+` — only changed models and downstream dependencies are rebuilt
- [ ] Run `dbt test` — uniqueness, not-null, referential integrity, and custom data tests all pass
- [ ] Run `dbt docs generate && dbt docs serve` — documentation renders, lineage graph shows complete DAG
- [ ] Verify incremental models: `dbt run --full-refresh --select ${incremental_model}` in staging — output matches non-incremental equivalent row-for-row
- [ ] Check model performance: no model exceeds SLA (e.g., `< 5 minutes` for daily runs)

## Verification Guardrails
<!-- STANDARD: 3min -->

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## References
<!-- STANDARD: 3min -->

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)
