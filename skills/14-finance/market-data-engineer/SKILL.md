---
name: market-data-engineer
description: >
  Use when building market data ingestion pipelines, normalizing corporate actions, storing tick
  data, or streaming real-time financial data. Handles options flow ingestion (Unusual Whales,
  CBOE LiveVol, Polygon.io, Bloomberg), real-time streaming (Kafka/Redpanda), tick data storage
  (TimescaleDB, ClickHouse, Parquet), corporate actions normalization (splits, dividends, mergers),
  and dividend/split-adjusted options chains. Do NOT use for quantitative analysis, trading strategy
  development, or general ETL pipeline work.
license: MIT
tags:
  - market-data-engineer
  - options-flow
  - tick-data
  - kafka
  - timescaledb
  - corporate-actions
  - real-time-streaming
  - polygon
author: Sandeep Kumar Penchala
type: finance
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 4000
chain:
  type: upstream
  consumes_from:
    - data-engineer
    - database-reliability-engineer
    - backend-developer
  feeds_into:
    - algorithmic-trader
    - quantitative-analyst
    - data-scientist
    - crypto-trader
    - forex-trader
    - futures-trader
    - fixed-income-analyst
    - commodities-analyst
    - intraday-options-trader
  alternatives:
    - data-engineer
---
# Market Data Engineer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Ingest, normalize, store, and serve financial market data at production scale. This skill covers options flow ingestion from Unusual Whales REST/WebSocket, CBOE LiveVol, Polygon.io Options API, and Bloomberg Terminal/API; real-time streaming via Kafka/Redpanda with stream processing; tick data storage in TimescaleDB (hot) and ClickHouse (analytics); corporate actions normalization (splits, dividends, mergers, ticker changes); dividend/split-adjusted options chains; historical data warehousing in Parquet on S3; data quality rules for stale quotes, arbitrage violations, and volume/OI discrepancies; and market-hours-aware scheduling. Every decision here is backed by war stories from production options pipelines — including the $50K dividend-adjustment loss and the survivorship-bias backtest disaster.
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

### Market Data Domain Extension — Execute These ADDITIONAL Research Steps

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP-F1** | **Validate data quality: check for missing ticks, duplicate bars, timestamp gaps, and price outliers.** A single bad tick (price = $0.01 for one millisecond) can corrupt an entire backtest. | [GARBAGE_IN_GARBAGE_OUT] Data quality issues are the silent killers of production trading systems. A strategy that "works" on dirty data works on fiction. Every data quality issue that reaches production is a future P&L loss waiting to happen. | Data quality dashboard, tick-level audit logs, outlier detection reports |
| **RP-F2** | **Handle corporate actions: splits, dividends, mergers, spin-offs, symbol changes.** A 2:1 stock split that isn't adjusted makes the stock look like it dropped 50% overnight — triggering every stop-loss and generating false signals. | [CORPORATE_ACTION_BOMB] Unadjusted corporate actions are the #1 source of backtest-contamination. A single unadjusted split can make a losing strategy look profitable or vice versa. | Corporate action calendar, adjustment factor database, exchange bulletins |
| **RP-F3** | **Assess survivorship bias.** Are backtest symbols still listed today? Stocks that went bankrupt, were delisted, or acquired are absent from current symbol lists — making historical returns look BETTER than reality. | [SURVIVORSHIP_BIAS] Using only currently-listed symbols adds 1-2% annually to backtest returns. A strategy that shows +12% on survivorship-biased data may be +10% (or worse) in reality. | Delisted securities database, historical index constituents, CRSP/Compustat |
| **RP-F4** | **Verify tick precision and timestamp granularity.** Options data at minute resolution hides 90%+ of actual trades. Sub-second timestamps matter for: fill probability estimation, slippage modeling, and signal latency measurement. | [RESOLUTION_BLINDNESS] A strategy that works on 1-minute bars may fail on tick data. The difference between the high of the minute and the actual trade price = hidden slippage. | Tick data archives, exchange timestamp specifications, fill reports |
| **RP-F5** | **Calculate data pipeline latency and reliability.** Measure: ingestion-to-availability latency (target: <100ms for real-time), uptime (target: 99.9%+), and data loss rate (target: <0.01%). Pipeline failure during market hours = blind trading. | [PIPELINE_BLINDNESS] A trading system without data is a car without headlights at night. Every minute of pipeline downtime during market hours is a minute of unmonitored risk. | Pipeline monitoring dashboard, latency histograms, incident reports |

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.py", "Polygon\|alpaca\|iexcloud\|polygon\|CBOE\|LiveVol\|UnusualWhales")` OR `file_contains("*.py", "kafka\|KafkaProducer\|KafkaConsumer\|redpanda")` OR `file_exists("schema/options_flow.avsc\|pipelines/ingest.py")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("*.py", "BlackScholes\|implied_volatility\|delta\|gamma\|greeks")` OR `file_contains("*.py", "scipy.stats.norm\|monte_carlo.*price")` | Invoke **quantitative-analyst** instead. This is pricing and Greeks analysis. |
| A3 | `file_contains("*.py", "backtrader\|zipline\|vectorbt\|alpaca.*trade\|Strategy.*next")` OR `file_contains("*.py", "order.*execution\|stop_loss\|take_profit")` | Invoke **algorithmic-trader** instead. This is strategy execution. |
| A4 | `file_contains("*.sql", "CREATE TABLE.*backtest\|SELECT.*sharpe\|regression")` AND `file_contains("*.py", "pandas\|numpy\|statsmodels\|sklearn")` | Invoke **data-scientist** instead. This is statistical analysis. |
| A5 | `file_contains("docker-compose.yml\|Dockerfile", "postgres\|timescale\|clickhouse")` AND `file_contains("*.sql", "CREATE INDEX\|VACUUM\|pg_stat")` | Invoke **database-reliability-engineer** instead. This is database operations. |
| A6 | `file_contains("*.py\|*.yml", "FastAPI\|flask\|@app\.(get\|post)")` AND `file_contains("*.py", "pipeline\|ingest\|etl")` | Jump to **Core Workflow** — Phase 1 (Ingestion API). |
| A7 | `file_contains("*.py", "pandas_market_calendars\|exchange_calendars\|trading_calendar")` OR `file_contains("*.py", "corporate.action\|split_adjust\|dividend_adjust")` | Jump to **Core Workflow** — Phase 3 (Corporate Actions). |
| A8 | `file_contains("docker-compose.yml", "kafka\|zookeeper\|redpanda\|schema-registry")` AND `file_contains("*.avsc\|*.proto", "record\|message")` | Jump to **Core Workflow** — Phase 2 (Streaming Pipeline). |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Ingest options flow data (dark pool, sweeps, block trades) → Jump to "Core Workflow" — Phase 1
├── Set up real-time streaming pipeline (Kafka/Redpanda + Avro) → Jump to "Core Workflow" — Phase 2
├── Store tick/options data (TimescaleDB or ClickHouse) → Jump to "Decision Trees" — Storage Backend Selection
├── Normalize corporate actions (splits, dividends, mergers) → Jump to "Core Workflow" — Phase 3
├── Adjust historical options chains for splits/dividends → Jump to "Core Workflow" — Phase 4
├── Build data warehouse on S3/Parquet for quant research → Jump to "Core Workflow" — Phase 5
├── Debug data quality: stale quotes, arbitrage violations, OI discrepancies → Jump to "Error Decoder"
└── Not sure? → Describe your market data problem and I'll route you

```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to store options data without recording the adjustment basis.** Raw prices without `adjustment_factor`, `adjustment_date`, and `corporate_action_id` are wrong if consumed as-is after a split. Always store `raw_price`, `adj_factor`, `adj_price` as three columns. | Trigger: generated schema or INSERT statement includes `strike` or `premium` column without a corresponding `adj_factor` column in the same table DDL within 5 lines | STOP. Insert: `strike_raw DECIMAL(12,4) NOT NULL, strike_adj DECIMAL(12,4), adj_factor DECIMAL(10,6) DEFAULT 1.0, corp_action_id UUID REFERENCES corporate_actions(id)`. Never overwrite raw prices with adjusted values. |
| **R2** | **REFUSE to hardcode `time.sleep()` for API rate limiting.** A 5-minute `sleep` on a 30-minute pre-market ingestion window loses 17% of data. Use token-bucket rate limiters with deadline-aware scheduling. | Trigger: generated code contains `time.sleep(` or `asyncio.sleep(` inside a loop that makes API calls without a `deadline` or `timeout` context | STOP. Replace with: `limiter = TokenBucket(rate=5, burst=10); async with limiter.acquire(): response = await api.fetch()`. Add deadline: `if time_remaining < (batch_size / rate): alert_and_skip_remaining()` |
| **R3** | **REFUSE to skip corporate actions normalization.** Unadjusted splits produce phantom alpha. A 3:1 split that is not applied shows "cheap" deep-ITM calls that don't exist post-split. | Trigger: generated pipeline processes `options_flow` or `options_chain` data AND `grep -rn "corporate.action\|split_adjust\|dividend_adjust" --include="*.py"` returns 0 in the same module | STOP. Add corporate action processing BEFORE any downstream analytics: `corp_actions = fetch_corp_actions(since=last_run); adjusted = apply_adjustments(raw_data, corp_actions); assert adjusted is not None`. Freeze downstream if `corp_actions.last_run < today 6 AM ET`. |
| **R4** | **REFUSE to filter by `WHERE ticker IN (SELECT DISTINCT ticker FROM current_universe)`.** This is survivorship bias manifested as SQL — it excludes delisted, bankrupt, and acquired tickers, inflating backtest returns by 2-4% annually. | Trigger: generated SQL contains `WHERE ticker IN (SELECT` or `WHERE symbol IN (SELECT` that references a current-universe table without a `trade_date` or `as_of_date` bound | STOP. Replace with point-in-time query: `WHERE ticker IN (SELECT ticker FROM ticker_master WHERE first_trade_date <= '{as_of_date}' AND (last_trade_date IS NULL OR last_trade_date >= '{as_of_date}'))`. Always query historically. |
| **R5** | **STOP and ASK when a schema migration is proposed without a reconciliation plan.** Migrations that change column types, precision, or names can silently corrupt data — strikes off by 1000×, premiums in wrong currency. | Trigger: generated SQL contains `ALTER TABLE ... ALTER COLUMN ... TYPE` or `ALTER TABLE ... RENAME COLUMN` without a subsequent `-- Reconciliation:` comment or `SELECT COUNT(*), AVG(column)` validation query | STOP. Respond: "Schema migrations require a reconciliation plan. Before I apply this: (1) what's the current row count? (2) what are the 1st, 50th, and 99th percentile values of the affected columns? (3) after migration, how will you verify these haven't changed beyond expected drift?" |
| **R6** | **DETECT and WARN about JSON serialization on Kafka/Redpanda topics above 1K msg/s.** At 50K msg/s, JSON costs 10× the storage and bandwidth of Avro. A single day becomes a $2,400/month bill vs $240 with Avro. | Trigger: generated Kafka producer code uses `json.dumps()` or `json.loads()` without `avro` or `protobuf` serializer in the same module. OR `docker-compose.yml` has a `KAFKA_TOPIC` without `value.serializer=io.confluent.kafka.serializers.KafkaAvroSerializer` | WARN: Insert comment: `# WARNING: JSON on Kafka at scale costs 10× more than Avro. Switch to Confluent Avro serializer with Schema Registry before production.` Add skeleton: `from confluent_kafka.schema_registry.avro import AvroSerializer` |
| **R7** | **DETECT and WARN about Parquet partitions keyed by `ticker/year/month/day`.** Query engines prune left-to-right. With ticker first, querying "AAPL on 2024-06-14" still scans every month under AAPL. Date-first partitioning eliminates 99.7% of data in a single pass. | Trigger: generated code or config contains `partition_by=['ticker', 'year'` or `PARTITIONED BY (ticker, year` — ticker before date in partition order | WARN: Replace with `partition_by=['year', 'month', 'day', 'ticker']`. Add comment: `# Date-first partitioning: a single-day single-ticker query hits exactly one partition. Always put highest-cardinality filter last.` |
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

Masters of market data engineer don't just build — they build **the right thing, at the right time, with the right trade-offs**. They think in systems, not tasks.

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
**Usage:** Invoke this skill with your target level, e.g., "as an L3 market data engineer, design..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

<!-- QUICK: 30s — scan the bullet list to decide if this skill fits -->
- Building a real-time options flow ingestion pipeline from Unusual Whales, Polygon.io, CBOE LiveVol, or Bloomberg
- Designing a market data lake with tick-level storage: TimescaleDB for hot (0-30 days), Parquet/S3 for cold archive (7 years), ClickHouse for analytics
- Normalizing corporate actions — stock splits, cash/stock dividends, mergers, ticker symbol changes, spin-offs — for historical data integrity
- Adjusting historical options chains: recalculating strikes, contract multipliers, and deliverable shares post-corporate-action
- Streaming order flow with Kafka/Redpanda for unusual options activity (UOA) detection pipelines
- Building data quality monitors: stale quote detection (bid/ask > 5 min old), arbitrage violation checks (put-call parity, box spreads), volume/OI reconciliation across sources
- Managing API cost and rate limits across multiple market data vendors with tiered pricing (Polygon free vs paid, Unusual Whales tiers)
- Warehousing historical options data in partitioned Parquet for quantitative research and strategy backtesting at scale
- Setting up market-hours-aware cron schedules, backfill windows, and holiday calendars for financial data pipelines

## Decision Trees

<!-- STANDARD: 3min -->
Full detail → references/market-data-computations.md

### DT1: Data Source Selection → Full detail in references
```
Equity data needed? → Polygon (primary), Yahoo Finance (fallback). Real-time → Polygon websocket.
Options data needed? → CBOE LiveVol (primary), Polygon options (fallback). Greeks → compute from chain.
Futures data? → CME DataMine (primary), Barchart (fallback). Continuous contracts → back-adjust.
Crypto? → CoinGecko (free, delayed), Binance API (real-time). Check rate limits.
```

### DT2: Anomaly Handling → Full detail in references
```
Price gap >50%? → Check for split (adjust), error (flag), real event (quarantine, verify against exchange).
Volume = 0 during market hours? → Flag stale. Switch to alternate provider.
OHLC logic violated? → H<L, etc. → CORRUPT. Discard bar, fill from alternate source.
NaN values? → DISCARD row. Log as DATA_LOSS. Backfill from nearest valid.
```
## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| Algorithm executes with stale market data producing incorrect signals | $10K-$1M in trading losses per incident | Implement data freshness heartbeat checks; halt trading on stale data; use redundant data feeds with failover under 100ms |
| Backtest overfits to historical data — 'looks great in backtest, fails in production' | $50K-$500K in strategy deployment losses | Use walk-forward validation; out-of-sample test on unseen periods; incorporate transaction costs and slippage in backtest; paper trade for 30+ days before live |
| Position sizing error due to unhandled edge case (corporate action, split, dividend) | $5K-$100K in unintended exposure | Automate corporate action handling; add position size sanity limits as circuit breakers; reconcile positions against prime broker daily |
| Personal finance plan excludes emergency fund leading to forced asset liquidation | $5K-$50K in opportunity cost and tax penalties | Build 3-6 month emergency fund before investing; keep in high-yield savings; treat as non-negotiable first step in any financial plan |
| Home purchase decision based on pre-approval max without accounting for hidden costs | $20K-$100K in financial strain over first year | Model total cost of ownership including taxes, insurance, maintenance (1-2% of home value/year), HOA, and utilities; stay under 28% DTI for housing |

| Gotcha | Cost | Fix |
|--------|------|-----|
| Algorithm executes with stale market data producing incorrect signals | $10K-$1M in trading losses per incident | Implement data freshness heartbeat checks; halt trading on stale data; use redundant data feeds with failover under 100ms |
| Backtest overfits to historical data — 'looks great in backtest, fails in production' | $50K-$500K in strategy deployment losses | Use walk-forward validation; out-of-sample test on unseen periods; incorporate transaction costs and slippage in backtest; paper trade for 30+ days before live |
| Position sizing error due to unhandled edge case (corporate action, split, dividend) | $5K-$100K in unintended exposure | Automate corporate action handling; add position size sanity limits as circuit breakers; reconcile positions against prime broker daily |
| Personal finance plan excludes emergency fund leading to forced asset liquidation | $5K-$50K in opportunity cost and tax penalties | Build 3-6 month emergency fund before investing; keep in high-yield savings; treat as non-negotiable first step in any financial plan |
| Home purchase decision based on pre-approval max without accounting for hidden costs | $20K-$100K in financial strain over first year | Model total cost of ownership including taxes, insurance, maintenance (1-2% of home value/year), HOA, and utilities; stay under 28% DTI for housing |

## Verification

- [ ] Timestamps: all timestamps stored in UTC with timezone offset column — no timezone-naive data
- [ ] Corporate actions: historical prices are split-adjusted from current date perspective
- [ ] Data quality: missing bars, zero-volume periods, and stale prices flagged in monitoring
- [ ] Cross-vendor: adjusted prices from all vendors reconciled within 0.1% tolerance
- [ ] Feed resilience: gap detection tested — simulated disconnect during volatile market triggers safety pause

## Verification Guardrails

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## Anti-Hallucination
<!-- STANDARD: 3min -->

- Admit uncertainty. If you cannot determine the correct approach, ask — do not guess.
- Flag your knowledge cutoff. If this project uses tools or patterns you have not seen, state your assumptions.
- Never guess security. If work touches auth, payments, or PII, route to security-reviewer.
- [VERIFIED] — Confirmed against official documentation or published standards
- [COMMON-PRACTICE] — Widely used in the industry
- [INFERRED] — Reasonable extrapolation from general principles
- [UNKNOWN] — Requires verification against specific context

## References

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
