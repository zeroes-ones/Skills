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
  consumes_from:
    - data-engineer
    - database-reliability-engineer
    - backend-developer
  feeds_into:
    - algorithmic-trader
    - quantitative-analyst
    - data-scientist
  alternatives:
    - data-engineer
---

# Market Data Engineer

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Ingest, normalize, store, and serve financial market data at production scale. This skill covers options flow ingestion from Unusual Whales REST/WebSocket, CBOE LiveVol, Polygon.io Options API, and Bloomberg Terminal/API; real-time streaming via Kafka/Redpanda with stream processing; tick data storage in TimescaleDB (hot) and ClickHouse (analytics); corporate actions normalization (splits, dividends, mergers, ticker changes); dividend/split-adjusted options chains; historical data warehousing in Parquet on S3; data quality rules for stale quotes, arbitrage violations, and volume/OI discrepancies; and market-hours-aware scheduling. Every decision here is backed by war stories from production options pipelines — including the $50K dividend-adjustment loss and the survivorship-bias backtest disaster.

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
<!-- QUICK: 30s — follow the ASCII tree to your scenario -->

### Data Source Selection: Options Flow
```
                    +----------------------------------+
                    | START: Which options flow source? |
                    +----------------+-----------------+
                                     |
              +----------------------+----------------------+
              |                      |                      |
    +---------v--------+  +----------v---------+  +---------v-----------+
    | Need real-time    |  | Need historical    |  | Need exchange-level  |
    | unusual activity  |  | options chain      |  | OPRA depth + Greeks  |
    | alerts + dark pool|  | data for backtests?|  | for HFT/MM models?   |
    +----+--------------+  +----+---------------+  +----+----------------+
         | YES                   | YES                  | YES
    +----v----+            +-----v-------+       +------v-------+
    |Unusual  |            | Polygon.io  |       |CBOE LiveVol  |
    |Whales   |            | Options API |       |or Bloomberg  |
    |REST+WS  |            |REST, 15min  |       |Terminal API  |
    |$99-599/m|            |delayed free |       |$500-2000/m  |
    +---------+            |$29-199/m   |       +--------------+
                           +------------+
```
**When to choose Unusual Whales:** Real-time flow detection, dark pool prints, sweep detection, unusual-activity alerts. Free tier: 250 requests/month. Pro: $99/mo for REST + WebSocket premium flow. Enterprise: custom pricing for raw firehose.
**When to choose Polygon.io:** Historical options chains for backtesting, Greeks data, snapshots. Free tier: 5 req/min, 15-min delayed. Paid tiers from $29/mo (Stocks Starter) to $199/mo (Stocks Advanced with full options chain + Greeks).
**When to choose CBOE LiveVol/Bloomberg:** Market-making models, HFT signal generation, full OPRA depth-of-book. CBOE LiveVol ~$500/mo for professional. Bloomberg Terminal ~$2,000/mo with blpapi access.
**When to use multiple vendors:** Most production systems combine Unusual Whales (flow alerts) + Polygon.io (historical chains) + CBOE/Bloomberg (OPRA depth). Cross-reference volume/OI across sources for data quality validation.

### Storage Backend Selection: Tick Data
```
                    +----------------------------------+
                    | START: Where to store tick data?  |
                    +----------------+-----------------+
                                     |
              +----------------------+----------------------+
              |                      |                      |
    +---------v--------+  +----------v---------+  +---------v-----------+
    | Write-heavy:      |  | Read-heavy:         |  | Long-term archive:  |
    | 100K+ ticks/sec   |  | 1K+ analytical      |  | >30 days retention  |
    | sub-ms ingestion? |  | queries/day on      |  | cost is primary     |
    |                   |  | billions of rows?   |  | concern?            |
    +----+--------------+  +----+---------------+  +----+----------------+
         | YES                   | YES                  | YES
    +----v----+            +-----v-------+       +------v-------+
    |TimescaleDB|          | ClickHouse  |       |Parquet on S3 |
    |PostgreSQL |          |Columnar,    |       |Partitioned   |
    |hypertable |          |vectorized   |       |by ticker/date|
    |chunks=1day|          |queries,     |       |ZSTD compress |
    |continuous |          |materialized |       |Apache Arrow  |
    |aggregates |          |views        |       |format        |
    +-----------+          +-------------+       +--------------+
```
**When to choose TimescaleDB:** Hot storage (0-30 days). Chunk interval = 1 day per ticker. Continuous aggregates precompute 1-min, 5-min, 1-hour OHLCV. Automatic compression after 7 days (90%+ space savings). Use `time_bucket()` for aggregations. Max recommended hypertable size: 10 TB per node.
**When to choose ClickHouse:** Analytics layer. Store 30-365 days of tick data. `MergeTree` engine with `ORDER BY (ticker, timestamp)`. Materialized views for pre-aggregated options analytics (Greeks distributions, IV surfaces, volume profiles). Query 1B rows in < 1 second with vectorized execution.
**When to choose Parquet/S3:** Cold archive (30 days to 7 years). Partition: `s3://market-data/options/year=YYYY/month=MM/day=DD/ticker=SYM/`. ZSTD compression level 9 (30-40% smaller than Snappy). Queryable via AWS Athena, DuckDB, or Spark without deserializing entire dataset. S3 Intelligent-Tiering for automatic cost optimization.

### Real-Time Pipeline Architecture
```
+-------------------+     +------------------+     +------------------+     +------------------+
| Unusual Whales    |     | Kafka/Redpanda   |     | Stream Processor |     | TimescaleDB Hot  |
| WebSocket Feed    +---->+ Topic:           +---->+ (Faust/Bytewax   +---->+ hypertable       |
| (flow, sweeps,    |     | options.flow.raw |     |  Flink/KSQL)     |     | + alerting       |
|  dark pool)       |     | partitions=10    |     | enrich, dedupe,  |     |                  |
+-------------------+     +------------------+     | normalize        |     +--------+---------+
                                                   +--------+---------+              |
                                                            |               +--------v---------+
                                                   +--------v---------+     | ClickHouse       |
                                                   | Dead Letter Queue|     | analytics layer  |
                                                   | options.flow.dlq +---->| mat. views,      |
                                                   | manual review    |     | IV surfaces       |
                                                   +------------------+     +------------------+
```
**Pipeline topology decisions:**
- Partitions = number of tickers × 2 for consumer parallelism. For 500 actively traded tickers, use 10 partitions (not 1000 — partition overhead dominates).
- Retention: 7 days on raw topic (debug window), 90 days on enriched topic (backfill window). Compacted topic for corporate actions (retain latest per ticker).
- Exactly-once semantics: enable `enable.idempotence=true` on producers + `isolation.level=read_committed` on consumers.
- Alert thresholds: consumer lag > 50K messages OR > 5 minutes during market hours (9:30-16:00 ET).

### Data Quality Decision Tree
```
                    +----------------------------------+
                    | START: Data quality check failed  |
                    +----------------+-----------------+
                                     |
              +----------------------+----------------------+
              |                      |                      |
    +---------v--------+  +----------v---------+  +---------v-----------+
    | Stale quotes      |  | Arbitrage violation|  | Volume/OI anomaly   |
    | bid/ask > 5 min   |  | put-call parity    |  | >10x change day/day |
    | old during market |  | error > 5% spot   |  | or zero volume       |
    | hours?            |  |                    |  |                      |
    +----+--------------+  +----+---------------+  +----+----------------+
         | YES                   | YES                  | YES
    +----v------------+    +----v-------------+   +----v----------------+
    |Check data feed  |    |Check corporate   |   |Check pipeline lag  |
    |status: vendor   |    |actions: split/   |   |or source downtime |
    |API down or      |    |dividend not      |   |Check if market     |
    |rate-limited?    |    |applied to chain? |   |holiday/half-day?   |
    +-----------------+    +------------------+   +---------------------+
```

## Core Workflow
<!-- QUICK: 30s — scan phase titles to understand the process -->

<!-- DEEP: 10+min -->
### Phase 1 (~20 min): Data Source Integration & Schema Design
<!-- STANDARD: 3min -->
1. **Source Catalog** — Inventory every market data source with endpoint patterns:
   - **Unusual Whales REST**: `GET /api/flow/options?ticker=AAPL&date=2024-01-15` → premium, size, condition, exchange, price, spot. Auth: API key in `Authorization` header.
   - **Unusual Whales WebSocket**: `wss://api.unusualwhales.com/ws/flow` — real-time dark pool prints, sweeps, block trades. Auth via connection message.
   - **Polygon.io Options Contracts**: `GET /v3/reference/options/contracts?underlying_ticker=AAPL&expiration_date=2024-01-19` → full chain with strikes, types, contract IDs.
   - **Polygon.io Options Aggregates**: `GET /v2/aggs/ticker/O:AAPL240119C00150000/range/1/day/2024-01-01/2024-01-19` → OHLCV bars for single contract.
   - **CBOE LiveVol**: REST API for OPRA depth, Greeks surfaces, IV index data. Requires CBOE data agreement.
   - **Bloomberg Terminal**: `BDH()` / `BDP()` functions via blpapi Python library — real-time + historical with field codes (e.g., `OPT_CHAIN`, `OPT_GREEKS`).

2. **Core Schema — Options Flow Table (TimescaleDB hypertable)**:
```sql
CREATE TABLE options_flow (
    flow_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker          VARCHAR(10) NOT NULL,
    underlying      VARCHAR(10) NOT NULL,
    strike          DECIMAL(12,2) NOT NULL,
    expiry          DATE NOT NULL,
    option_type     CHAR(1) CHECK (option_type IN ('C', 'P')),
    trade_timestamp TIMESTAMPTZ NOT NULL,
    premium         DECIMAL(15,4) NOT NULL,       -- size × price paid
    size            INTEGER NOT NULL,              -- number of contracts
    trade_condition VARCHAR(20),                   -- e.g., 'SWEEP', 'BLOCK', 'SPLIT'
    exchange        VARCHAR(5),                    -- e.g., 'CBOE', 'PHLX', 'ISE'
    bid             DECIMAL(12,4),
    ask             DECIMAL(12,4),
    last_price      DECIMAL(12,4),
    volume          INTEGER,
    open_interest   INTEGER,
    implied_vol     DECIMAL(8,4),
    delta           DECIMAL(6,4),
    gamma           DECIMAL(8,6),
    theta           DECIMAL(8,4),
    vega            DECIMAL(8,4),
    rho             DECIMAL(8,4),
    -- Adjustment tracking columns
    adj_factor      DECIMAL(10,4) DEFAULT 1.0,
    raw_strike      DECIMAL(12,2),
    raw_premium     DECIMAL(15,4),
    corp_action_id  UUID REFERENCES corporate_actions(action_id),
    -- Metadata
    source          VARCHAR(20) NOT NULL,          -- 'unusual_whales', 'polygon', 'bloomberg'
    raw_json        JSONB,
    ingested_at     TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('options_flow', 'trade_timestamp',
    chunk_time_interval => INTERVAL '1 day');

CREATE INDEX idx_flow_ticker_ts ON options_flow (ticker, trade_timestamp DESC);
CREATE INDEX idx_flow_underlying_expiry ON options_flow (underlying, expiry);
CREATE INDEX idx_flow_source ON options_flow (source, trade_timestamp DESC);
```

3. **Corporate Actions Schema**:
```sql
CREATE TABLE corporate_actions (
    action_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker          VARCHAR(10) NOT NULL,
    action_type     VARCHAR(20) CHECK (action_type IN (
        'split', 'reverse_split', 'cash_dividend', 'stock_dividend',
        'merger', 'spin_off', 'ticker_change', 'delisting'
    )),
    ex_date         DATE NOT NULL,
    record_date     DATE,
    pay_date        DATE,
    split_ratio     DECIMAL(10,4),       -- e.g., 3.0 for 3:1 split, 0.5 for 1:2 reverse split
    dividend_amount DECIMAL(12,6),       -- per share, USD
    new_ticker      VARCHAR(10),         -- for ticker changes and mergers
    announcement_ts TIMESTAMPTZ NOT NULL,
    source          VARCHAR(20) NOT NULL, -- 'bloomberg', 'refinitiv', 'sec_edgar'
    raw_json        JSONB
);

CREATE INDEX idx_corp_actions_ticker_date ON corporate_actions (ticker, ex_date);
```

4. **Point-in-Time Ticker Master**:
```sql
CREATE TABLE ticker_master (
    ticker            VARCHAR(10) PRIMARY KEY,
    company_name      VARCHAR(200),
    first_trade_date  DATE NOT NULL,
    last_trade_date   DATE,                  -- NULL if still active
    delisting_reason  VARCHAR(50),
    successor_ticker  VARCHAR(10),
    exchange          VARCHAR(10),
    is_active         BOOLEAN DEFAULT TRUE,
    updated_at        TIMESTAMPTZ DEFAULT NOW()
);
```

**What good looks like:** All 4+ data sources cataloged with endpoint URLs and auth methods. Schema in Git with versioned migration files. Test data for `AAPL`, `SPY`, `TSLA`, and `NVDA` loads successfully. Ticker master populated with 5+ years of historical symbols including delisted tickers.

<!-- DEEP: 10+min -->
### Phase 2 (~30 min): Real-Time Streaming Pipeline
<!-- STANDARD: 3min -->
1. **Kafka/Redpanda Topic Design**:
```yaml
topics:
  options.flow.raw:
    partitions: 10
    replication_factor: 3
    retention_ms: 604800000         # 7 days
    cleanup_policy: delete
    compression_type: zstd
  options.flow.enriched:
    partitions: 10
    replication_factor: 3
    retention_ms: 7776000000        # 90 days
    cleanup_policy: delete
  options.flow.dlq:
    partitions: 3
    retention_ms: 2592000000        # 30 days
  options.corporate_actions:
    partitions: 3
    retention_ms: -1                # forever (log compacted)
    cleanup_policy: compact
```

2. **Stream Processor — Faust Application**:
```python
import faust
from datetime import datetime

app = faust.App('options-flow', broker='kafka://localhost:9092',
                store='rocksdb://')

flow_topic = app.topic('options.flow.raw', value_type=dict)
enriched_topic = app.topic('options.flow.enriched', value_type=dict)
dlq_topic = app.topic('options.flow.dlq', value_type=dict)
actions_table = app.Table('corp_actions', default=None,
                          partitions=3)

@app.agent(flow_topic)
async def enrich_and_validate(flows):
    async for flow in flows:
        try:
            # Validate required fields
            required = ['ticker', 'strike', 'expiry', 'trade_timestamp', 'premium', 'size']
            for field in required:
                if field not in flow:
                    raise ValueError(f"Missing required field: {field}")

            # Apply corporate action adjustments from compacted table
            ticker = flow['ticker']
            action = actions_table.get(ticker)
            if action and action.get('split_ratio'):
                ratio = float(action['split_ratio'])
                flow['adj_factor'] = flow.get('adj_factor', 1.0) * ratio
                flow['raw_strike'] = flow['strike']
                flow['strike'] = float(flow['strike']) / ratio
                flow['raw_premium'] = flow['premium']
                flow['premium'] = float(flow['premium']) / ratio
                flow['corp_action_id'] = action.get('action_id')

            flow['processed_at'] = datetime.utcnow().isoformat()
            await enriched_topic.send(value=flow)

        except Exception as e:
            flow['error'] = str(e)
            flow['failed_at'] = datetime.utcnow().isoformat()
            await dlq_topic.send(value=flow)
```

3. **Token-Bucket Rate Limiter**:
```python
import time
import asyncio

class MarketDataRateLimiter:
    LIMITS = {
        'polygon': {'free': 5, 'starter': 50, 'advanced': float('inf')},
        'unusual_whales': {'free': 250, 'pro': 5000, 'enterprise': float('inf')},
        'cboe_livevol': {'standard': 100, 'premium': 1000}
    }

    def __init__(self, vendor: str, tier: str, cost_budget_daily: float = None):
        self.rate = self.LIMITS[vendor][tier]           # req/min
        self.tokens = self.rate
        self.last_refill = time.monotonic()
        self.cost_counter = 0
        self.cost_budget = cost_budget_daily
        self.daily_cost = 0.0

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.rate, self.tokens + elapsed * (self.rate / 60.0))
        self.last_refill = now

    async def acquire(self, estimated_cost: float = 0.0):
        while self.tokens < 1:
            await asyncio.sleep(1.0 / max(self.rate, 1))
            self._refill()
        self.tokens -= 1
        self.cost_counter += 1
        self.daily_cost += estimated_cost
        if self.cost_budget and self.daily_cost > self.cost_budget:
            raise RuntimeError(
                f"Daily cost budget {self.cost_budget} exceeded: {self.daily_cost}"
            )
```

<!-- DEEP: 10+min -->
**War story — Infinite Retention Disaster:** A team configured `retention_ms: -1` on `options.flow.raw` intending to preserve all raw data indefinitely for audit purposes. After 6 months, the Kafka cluster reached 98% disk usage and the 3 AM pages began. Root cause analysis revealed: uncompressed JSON at 50K messages/sec × 500 bytes/msg = 25 MB/sec × 86,400 sec/day = 2.16 TB/day × 180 days = 389 TB. Fix applied: (1) switched raw topic to 7-day retention, (2) adopted Avro encoding with Confluent Schema Registry (90% size reduction), (3) created enriched topic with 90-day retention as the durable store. Lesson: Never use infinite retention on unbounded streams. Log-compacted topics (for reference data like corporate actions) are the sole exception.

**What good looks like:** WebSocket feed → Kafka → Faust stream processor → TimescaleDB pipeline processing 50K+ msgs/sec with < 500ms end-to-end latency. Backpressure handled gracefully (consumer pause, not crash). DLQ has < 0.01% of messages. Rate limiter never triggers cost budget alert during normal operation.

<!-- DEEP: 10+min -->
### Phase 3 (~25 min): Corporate Actions Normalization
<!-- STANDARD: 3min -->
1. **Stock Split Adjustment — Options Chain** (NVDA 10:1 split, ex-date 2024-06-10):
```sql
-- Pre-split: NVDA trading at $1200, 1500C strike exists
-- Post-split: NVDA trades at $120, strike adjusts to $150, contract multiplier becomes 1000 shares
-- The adjustment: divide all strikes by 10, multiply contract size by 10
-- IMPORTANT: adjustment applies to all data BEFORE ex-date
UPDATE options_flow
SET
    strike      = strike * (1.0 / 10.0),
    size        = size * 10,
    adj_factor  = adj_factor * 10.0,
    raw_strike  = COALESCE(raw_strike, strike),    -- preserve pre-adjustment value
    raw_premium = COALESCE(raw_premium, premium),
    premium     = premium * (1.0 / 10.0)
WHERE underlying = 'NVDA'
  AND trade_timestamp < '2024-06-10'::date
  AND adj_factor = 1.0;  -- only adjust unadjusted rows

-- Verify: no negative impact on post-split data
SELECT COUNT(*) FROM options_flow
WHERE underlying = 'NVDA'
  AND trade_timestamp >= '2024-06-10'
  AND adj_factor != 1.0;  -- should return 0
```

2. **Cash Dividend Adjustment — Forward Price**:
```sql
-- Apple pays $0.25/share dividend, ex-date 2024-02-09
-- The forward price used in options pricing shifts down by PV of dividend
-- This affects delta calculations and ITM probability estimates
UPDATE options_chain_snapshots
SET
    forward_price     = spot_price - 0.25 * EXP(-0.05 * (15.0/365.0)),
    dividend_adjusted = TRUE,
    dividend_amount   = 0.25,
    dividend_ex_date  = '2024-02-09'::date
WHERE underlying = 'AAPL'
  AND snapshot_date >= '2024-02-09'
  AND NOT dividend_adjusted;
```

3. **Ticker Change / Merger Handler** (FB → META, effective 2022-06-09):
```python
def handle_ticker_change(old_ticker: str, new_ticker: str,
                         effective_date: str):
    conn.execute("""
        UPDATE options_flow
        SET ticker = %(new)s, underlying = %(new)s
        WHERE underlying = %(old)s
          AND trade_timestamp >= %(eff)s
    """, {'new': new_ticker, 'old': old_ticker, 'eff': effective_date})

    conn.execute("""
        UPDATE ticker_master
        SET is_active = FALSE, last_trade_date = %(eff)s,
            successor_ticker = %(new)s
        WHERE ticker = %(old)s
    """, {'old': old_ticker, 'new': new_ticker, 'eff': effective_date})

    conn.execute("""
        INSERT INTO ticker_master (ticker, first_trade_date,
            predecessor_ticker)
        SELECT %(new)s, %(eff)s, %(old)s
        WHERE NOT EXISTS (SELECT 1 FROM ticker_master
                          WHERE ticker = %(new)s)
    """, {'old': old_ticker, 'new': new_ticker, 'eff': effective_date})

    conn.execute("""
        INSERT INTO corporate_actions (ticker, action_type, ex_date,
            new_ticker, announcement_ts, source)
        VALUES (%(old)s, 'ticker_change', %(eff)s,
                %(new)s, NOW(), 'manual_review')
    """, {'old': old_ticker, 'new': new_ticker, 'eff': effective_date})
```

4. **Corporate Actions Calendar — Automated Processing**:
```python
from datetime import date, timedelta

def process_daily_corporate_actions(as_of: date):
    """Run daily: fetch actions with ex_date = today, apply to all history."""
    actions = fetch_actions_as_of(as_of)

    for action in actions:
        if action['action_type'] == 'split':
            apply_split_adjustment(
                ticker=action['ticker'],
                ex_date=action['ex_date'],
                ratio=action['split_ratio']
            )
        elif action['action_type'] == 'cash_dividend':
            apply_dividend_adjustment(
                ticker=action['ticker'],
                ex_date=action['ex_date'],
                amount=action['dividend_amount']
            )
        elif action['action_type'] in ('ticker_change', 'merger'):
            handle_ticker_change(
                old_ticker=action['ticker'],
                new_ticker=action['new_ticker'],
                effective_date=action['ex_date']
            )

        log_action_processed(action['action_id'])

    # Verify: no unapplied corporate actions older than 1 business day
    unapplied = get_unapplied_actions_before(as_of - timedelta(days=1))
    if unapplied:
        alert_pager(f"{len(unapplied)} unapplied corporate actions: {unapplied}")
```

<!-- DEEP: 10+min -->
**War story — The $50K Dividend Adjustment:** A quant fund ran a backtest showing extraordinary returns from selling deep-ITM puts on a high-dividend utility stock. They deployed $500K in capital. On day one, they lost $50K. Root cause: the options data pipeline ingested raw prices without adjusting for a $2.50/share special dividend. Post-dividend, the stock dropped $2.50, making the deep-ITM puts substantially more expensive to close than the backtest predicted. The pipeline had stored the *pre-dividend* stock price alongside the *post-dividend* option price, creating an artificial arbitrage. Fix: implemented mandatory dividend adjustment as a non-bypassable step in the ETL, with automated reconciliation checks comparing adjusted prices to exchange-reported settlement prices.

**What good looks like:** All corporate actions applied within 1 hour of announcement. Historical data queryable correctly at any point in time — querying AAPL options on 2019-06-15 returns split-adjusted strikes that match what actually traded that day. Daily reconciliation shows zero unadjusted positions. Backtests no longer produce phantom arbitrage opportunities.

<!-- DEEP: 10+min -->
### Phase 4 (~20 min): Historical Data Warehousing
<!-- STANDARD: 3min -->
1. **Daily Parquet Export — TimescaleDB → S3**:
```python
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import date, timedelta

def export_day_to_parquet(export_date: date):
    """Export one day of options flow to partitioned Parquet on S3."""
    query = f"""
    SELECT ticker, underlying, strike, expiry, option_type,
           trade_timestamp, premium, size, trade_condition, exchange,
           bid, ask, last_price, volume, open_interest,
           implied_vol, delta, gamma, theta, vega, rho,
           adj_factor, source
    FROM options_flow
    WHERE trade_timestamp::date = '{export_date.isoformat()}'
    """

    df = pd.read_sql(query, engine)

    # Partition columns for Hive-style partitioning
    df['year'] = export_date.year
    df['month'] = f"{export_date.month:02d}"
    df['day'] = f"{export_date.day:02d}"

    table = pa.Table.from_pandas(df)
    pq.write_to_dataset(
        table,
        root_path='s3://market-data/options/',
        partition_cols=['year', 'month', 'day', 'ticker'],
        compression='zstd',
        compression_level=9,
        existing_data_behavior='overwrite_or_ignore',
        basename_template='part-{i}.parquet'
    )

    # Integrity check: row count matches source
    source_count = df.shape[0]
    parquet_count = pq.ParquetDataset(
        f's3://market-data/options/year={export_date.year}/'
        f'month={export_date.month:02d}/day={export_date.day:02d}/'
    ).read().num_rows
    assert source_count == parquet_count,         f"Row count mismatch: source={source_count}, parquet={parquet_count}"

    # Sanity check: date range is correct
    assert df['trade_timestamp'].min().date() == export_date,         f"Date mismatch in export: expected {export_date}"
```

2. **ClickHouse Analytics Materialized Views**:
```sql
-- IV Surface: hourly snapshots of implied volatility by strike/expiry
CREATE MATERIALIZED VIEW options_iv_surface
ENGINE = AggregatingMergeTree()
PARTITION BY toYYYYMM(snapshot_hour)
ORDER BY (underlying, expiry, strike, snapshot_hour)
AS SELECT
    underlying,
    expiry,
    strike,
    toStartOfHour(trade_timestamp) AS snapshot_hour,
    avgState(implied_vol)          AS avg_iv,
    minState(implied_vol)          AS min_iv,
    maxState(implied_vol)          AS max_iv,
    quantileState(0.10)(implied_vol) AS iv_p10,
    quantileState(0.50)(implied_vol) AS iv_p50,
    quantileState(0.90)(implied_vol) AS iv_p90,
    quantileState(0.99)(implied_vol) AS iv_p99,
    sumState(premium)              AS total_premium,
    sumState(volume)               AS total_volume,
    sumState(open_interest)        AS total_oi,
    countState()                   AS trade_count
FROM options_flow
GROUP BY underlying, expiry, strike, snapshot_hour;

-- Volume Profile: aggregate flow by ticker and trade condition
CREATE MATERIALIZED VIEW options_volume_profile
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(trade_hour)
ORDER BY (ticker, trade_hour, option_type, trade_condition)
AS SELECT
    ticker,
    toStartOfHour(trade_timestamp) AS trade_hour,
    option_type,
    trade_condition,
    sum(premium)  AS total_premium,
    sum(volume)   AS total_volume,
    sum(size)     AS total_contracts,
    count()       AS trade_count
FROM options_flow
GROUP BY ticker, trade_hour, option_type, trade_condition;
```

3. **Retention Lifecycle Policy**:
```yaml
retention_policy:
  hot_storage:
    backend: TimescaleDB
    duration: 30_days
    data: full tick-level with compression after day 7
  warm_storage:
    backend: ClickHouse
    duration: 365_days
    data: tick-level + materialized views (hourly aggregates)
  cold_storage:
    backend: S3 (Parquet, ZSTD-9)
    duration: 7_years
    data: tick-level, partitioned by date/ticker
  permanent:
    backend: S3 (Parquet)
    data: daily OHLCV aggregates per option chain
  delete:
    backend: N/A
    trigger: after 7 years
    data: tick-level Parquet files
```

<!-- DEEP: 10+min -->
**War story — The Date Parsing Bug:** A quant researcher reported backtest results that "looked too good." Investigation revealed the Parquet archive only contained data from 2019 onward — the pipeline had silently skipped 2015-2018. Root cause: a date-parsing bug in the export script where `YYYYMMDD` format dates with `DD <= 12` were parsed as `YYYY-DD-MM` by Python's `datetime.strptime` with an ambiguous format string. Every date like `2018-03-05` (March 5) was interpreted as May 3, and dates with `DD > 12` threw exceptions that were silently caught. Fix: (1) switched to ISO 8601 format exclusively (`YYYY-MM-DD`), (2) added `assert df['trade_timestamp'].min().year == int(year)` after every export batch, (3) implemented row-count integrity checks comparing exported Parquet row counts to TimescaleDB source counts, (4) added end-to-end monitoring that alerts if any day in the last 7 years has zero rows.

**What good looks like:** Daily Parquet exports complete within 2 hours of market close (by 18:00 ET). ClickHouse materialized views refresh within 5 minutes of new data arrival. Any date range 2010-2025 queryable in < 3 seconds via Athena/DuckDB. Row counts match source with zero discrepancies. Seven years of tick data occupies < 50 TB on S3 with ZSTD-9 compression.

<!-- DEEP: 10+min -->
### Phase 5 (~15 min): Data Quality Monitoring & Alerting
<!-- STANDARD: 3min -->
1. **Stale Quote Detection**:
```sql
-- Alert if any active ticker has quotes older than 5 minutes during market hours
SELECT ticker, COUNT(*) AS stale_count, MAX(snapshot_timestamp) AS last_seen
FROM options_chain_snapshots
WHERE snapshot_timestamp < NOW() - INTERVAL '5 minutes'
  AND EXTRACT(HOUR FROM NOW() AT TIME ZONE 'America/New_York') BETWEEN 9 AND 16
  AND EXTRACT(DOW FROM NOW() AT TIME ZONE 'America/New_York') BETWEEN 1 AND 5
GROUP BY ticker
HAVING COUNT(*) > 100
ORDER BY last_seen ASC;
```

2. **Put-Call Parity Arbitrage Detection**:
```sql
-- PCP violation: |C_bid - P_ask - S + K*e^(-rT)| > 0.05*S indicates data error
WITH parity_check AS (
    SELECT
        underlying, expiry, strike, option_type,
        snapshot_timestamp,
        ABS(call_bid - put_ask - underlying_price +
            strike * EXP(-0.05 * (expiry - CURRENT_DATE) / 365.0))
        AS parity_error
    FROM options_snapshots
    WHERE underlying_price > 0 AND call_bid IS NOT NULL AND put_ask IS NOT NULL
)
SELECT underlying, expiry, strike, parity_error,
       underlying_price * 0.05 AS threshold
FROM parity_check
WHERE parity_error > underlying_price * 0.05
ORDER BY parity_error DESC
LIMIT 100;
```

3. **Volume/OI Sanity Checks**:
```sql
-- Spike detection: daily volume > 10x previous day for same ticker
WITH daily_vol AS (
    SELECT ticker, trade_timestamp::date AS trade_date,
           SUM(volume) AS total_vol,
           SUM(premium) AS total_premium
    FROM options_flow
    WHERE trade_timestamp > NOW() - INTERVAL '7 days'
    GROUP BY ticker, trade_timestamp::date
)
SELECT ticker, trade_date, total_vol,
       LAG(total_vol) OVER (PARTITION BY ticker ORDER BY trade_date) AS prev_vol,
       ROUND(total_vol::numeric / NULLIF(LAG(total_vol) OVER (
           PARTITION BY ticker ORDER BY trade_date), 0), 2) AS ratio
FROM daily_vol
WHERE total_vol > 10 * LAG(total_vol) OVER (
    PARTITION BY ticker ORDER BY trade_date)
   OR total_vol = 0;  -- complete gap indicates pipeline failure
```

4. **Cross-Source Reconciliation**:
```sql
-- Compare total option volume between Unusual Whales and Polygon.io for top tickers
SELECT ticker, trade_timestamp::date,
       SUM(CASE WHEN source = 'unusual_whales' THEN volume ELSE 0 END) AS uw_volume,
       SUM(CASE WHEN source = 'polygon' THEN volume ELSE 0 END) AS poly_volume,
       ABS(SUM(CASE WHEN source = 'unusual_whales' THEN volume ELSE 0 END) -
           SUM(CASE WHEN source = 'polygon' THEN volume ELSE 0 END)) AS volume_diff
FROM options_flow
WHERE trade_timestamp::date = CURRENT_DATE - INTERVAL '1 day'
GROUP BY ticker, trade_timestamp::date
HAVING ABS(SUM(CASE WHEN source = 'unusual_whales' THEN volume ELSE 0 END) -
           SUM(CASE WHEN source = 'polygon' THEN volume ELSE 0 END)) >
       0.15 * GREATEST(SUM(CASE WHEN source = 'unusual_whales' THEN volume ELSE 0 END),
                        SUM(CASE WHEN source = 'polygon' THEN volume ELSE 0 END))
ORDER BY volume_diff DESC;
-- Alert if any ticker shows >15% volume discrepancy between sources
```

**What good looks like:** Quality dashboard shows all-green across stale detection, arbitrage checks, volume sanity, and cross-source reconciliation. Alerts fire within 2 minutes of anomaly detection. All violations investigated and root-caused within 15 minutes. Weekly quality reports show < 0.01% data error rate.

## Best Practices
<!-- STANDARD: 3min — rules extracted from production market data pipelines -->
- **Store raw and adjusted prices side by side.** Raw price, adjustment factor, adjusted price as three columns. You need the raw for audit trails and the adjusted for analysis. Never lose the raw — you cannot un-adjust data.
- **Chunk TimescaleDB hypertables by 1-day intervals.** One chunk per day per ticker balances compression efficiency (90%+ savings after day 7) with query performance. Monthly chunks cause inefficient full-chunk scans for single-day queries. Verify with `SELECT * FROM timescaledb_information.chunks WHERE hypertable_name = 'options_flow';`
- **Use Avro or Protobuf on Kafka, never JSON.** JSON at 50K msg/sec × 500 bytes = 25 MB/sec. Avro with schema registry = 2.5 MB/sec. Over 30 days, that is $2,400 vs $240 in Kafka storage costs. Use Confluent Schema Registry for schema evolution compatibility checks.
- **Partition Parquet by `year/month/day/ticker` — in that order.** Query pruning eliminates 99.7% of data for single-ticker single-day queries. S3 LIST operations scale with partition count — keep partition fanout under 10K paths per query. Never put ticker before date in the hierarchy.
- **Rate-limit with deadline awareness.** If ingestion must finish by 9:25 AM ET and it is 9:20 AM: skip non-essential tickers, parallelize across API keys, or fail loudly with a specific alert. Silent partial data is worse than no data — it corrupts downstream analytics without anyone knowing.
- **Run corporate actions processing BEFORE any analytics pipeline.** The analytics dbt models, the quant strategy backtest, and the risk system all depend on adjusted data. Freeze downstream pipelines until adjustments apply if corporate actions processing is delayed.
- **Maintain a point-in-time ticker master with delisting history.** Store `ticker`, `first_trade_date`, `last_trade_date`, `delisting_reason`, `successor_ticker`. Query historically: filter by `WHERE trade_date BETWEEN first_trade_date AND COALESCE(last_trade_date, '2099-12-31')`. Without this, every backtest has survivorship bias.
- **Pre-compute continuous aggregates filtered to market hours.** TimescaleDB continuous aggregates should filter to `EXTRACT(HOUR FROM ts AT TIME ZONE 'America/New_York') BETWEEN 9 AND 16` so dashboards do not show flat lines during closed hours.
- **Never silently drop bad data — use a quarantine table.** Rows that fail validation go to `options_flow_quarantine` with `validation_error` and `ingested_at`. Someone reviews quarantine daily. Silently dropped bad data = silently wrong analytics.
- **Test with AAPL, SPY, TSLA, and NVDA.** AAPL (highly liquid, multiple splits), SPY (ETF, no splits but quarterly dividends), TSLA (high IV, volatile, unusual activity magnet), NVDA (2024 10:1 split). If your pipeline handles these four correctly, it handles 95% of tickers.
<!-- DEEP: 10+min -->
- **Use ZSTD compression level 9 for Parquet archives.** ZSTD-9 achieves 30-40% smaller files than Snappy for financial time-series data. For 7 years of tick data at 50 TB raw, that is the difference between $2,000/month and $3,200/month on S3 Intelligent-Tiering. Decompression speed penalty is negligible (< 5%) for Athena queries that scan pre-pruned partitions.
- **Schedule all jobs in Eastern Time with holiday awareness.** Use `pandas_market_calendars` or `exchange_calendars` library. Never hardcode `0 9 * * 1-5` in cron — that runs on Good Friday, July 3 half-days, and misses post-holiday catch-up windows. Instead: `trading_calendar.is_trading_day(date)` before every pipeline run.

## Anti-Patterns
<!-- DEEP: 5min -- each anti-pattern includes machine-detectable patterns -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| Storing only adjusted prices because "raw data takes too much space" | Store `raw_price`, `adj_factor`, `adj_price` as three columns. Compress raw with ZSTD-9 — storage cost difference is <15%. Adjustment factors change retroactively — without raw, you cannot re-adjust. | `grep -rn "CREATE TABLE.*options\|strike\|premium" schema/ --include="*.sql" \| grep -v "raw\|adj_factor\|corp_action"` → finds schemas without raw/adj columns | `scripts/check-schema-columns.sh` — fails if `options_flow` table is missing `raw_strike`, `raw_premium`, or `adj_factor` columns |
| Using JSON serialization on Kafka/Redpanda at > 1K msg/s because "it's easier to debug" | Use Avro or Protobuf with Confluent Schema Registry. Enforce schema compatibility checks (BACKWARD, FORWARD, FULL). JSON costs 10× the storage and network bandwidth at scale. | `grep -rn "json.dumps\|json.loads\|value_serializer.*json" src/streaming/ --include="*.py"` → finds JSON serializers in Kafka producers | `scripts/check-kafka-serializer.sh` — fails if any Kafka producer uses `json.dumps` without an Avro fallback. Schema registry: enforce `json.enable=false` |
| Running corporate actions processing AFTER downstream analytics pipelines | Corporate actions must complete BEFORE any downstream pipeline runs. Add dependency gate: if `corp_actions.last_run < today 6 AM ET`, freeze all downstream. Unadjusted prices silently corrupt every model. | `grep -rn "corp_action\|corporate_action" docker-compose* airflow/ --include="*.yml" --include="*.py" \| grep -v "upstream\|depends\|wait_for"` → finds corp actions without upstream dependency | Airflow: set `depends_on_past=False` but add `ExternalTaskSensor` on corp_actions DAG. CI: fail if any downstream DAG lacks `wait_for_corp_actions` sensor |
| Partitioning Parquet by `ticker/year/month/day` instead of date-first | Partition as `year/month/day/ticker`. Query engines prune left-to-right. Date-first: a single-day single-ticker query hits ONE partition. Ticker-first: scans every month under that ticker. | `grep -rn "partition.*ticker.*year\|partition_cols.*ticker" src/ --include="*.py"` → finds ticker-first partition order | `scripts/check-parquet-partition-order.sh` — fails if partition_cols has `ticker` before `year` |
| Silently dropping rows that fail validation to "keep the pipeline running" | Route failed rows to a quarantine table with `validation_error`, `raw_payload`, `ingested_at`. Review quarantine daily. Alert if quarantine rate > 1% of daily ingested volume. | `grep -rn "except.*:\s*$" src/pipeline/ -A 3 \| grep -c "pass\|continue"` → finds silent error swallowing in pipeline code | `pytest tests/test_quarantine.py` — inject invalid rows, assert they appear in quarantine table, not silently dropped |
| Hardcoding market hours as `9:30-16:00 ET` in pipeline configs and cron jobs | Use `pandas_market_calendars` or `exchange_calendars` for ALL schedule decisions. Check `calendar.is_trading_day(date)` before every pipeline run. Never hardcode times. | `grep -rn "9:30\|16:00\|14:00\|13:00" config/ crontab* airflow/ --include="*.yml" --include="*.py" \| grep -v "calendar\|is_trading_day"` → finds hardcoded times | `scripts/check-hardcoded-times.sh` — fails if any schedule config contains literal time strings without `calendar.` or `is_trading_day` |
| Deploying schema migrations without data reconciliation — strikes off by 1000× | Every migration must include: (a) pre-migration row count and value distribution snapshot, (b) migration with idempotency guard, (c) post-migration reconciliation query comparing percentiles. Reject if reconciliation fails. | `grep -rn "ALTER TABLE\|ALTER COLUMN" migrations/ --include="*.sql" -A 20 \| grep -v "checksum\|COUNT(\|AVG(\|PERCENTILE"` → finds migrations without reconciliation queries | `pytest tests/test_migration_reconciliation.py` — runs each migration, verifies pre/post checksums match for all numeric columns |
| Assuming vendor API "unlimited" tier is actually unlimited — $50K overage charge | Review vendor rate cards quarterly. Configure per-vendor rate limiters with daily cost budgets. Model costs using 99th-percentile daily volume (earnings season), not average. Set cost alerts at 50%/75%/90% of monthly budget. | `grep -rn "unlimited\|rate.limit.*None\|no.rate.limit" config/ --include="*.yml" --include="*.py"` → finds vendor configs without explicit rate caps | `scripts/check-vendor-limits.sh` — fails if any vendor config lacks `rate_limit_per_second`, `daily_cost_budget`, or `monthly_cost_budget` |

## Error Decoder
<!-- DEEP: 5min -- each entry includes a console-string matcher for automatic recovery loops -->

| 🖥️ Console Match (grep pattern) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|---|---|---|---|---|
| `ConnectionError\|ConnectionRefusedError\|Errno 61\|Connection reset by peer` + `grep -rn "feed\|websocket\|stream" src/ -A 10 \| grep -v "reconnect\|backoff\|on_error"` | Feed handler crashed at 9:31 AM on the first day of live trading — missed the entire market open | Feed handler had no reconnection logic. Single point of failure with no redundant data source. The `on_error` callback just logged and exited. | Implement automatic reconnection with exponential backoff (1s, 2s, 4s, 8s, 16s, max 10 retries). Maintain at least 2 independent data sources for each feed. Run disconnect-reconnect drills before go-live. | 1. Find all feed handlers: `grep -rn "websocket\|feed\|stream" src/ --include="*.py"` 2. Add reconnection wrapper: `@retry(stop=stop_after_attempt(10), wait=wait_exponential(multiplier=1, max=16))` 3. Add second data source: `fallback_feed = PolygonStream()` 4. Drill: `docker-compose stop feed-primary` → verify `feed-fallback` takes over within 5s |
| `psycopg2.errors.NumericValueOutOfRange\|OverflowError\|decimal.Overflow` + `grep -rn "strike\|premium\|price" migrations/ -A 5 \| grep "DECIMAL("` | Tick data corruption after schema migration — all historical strikes off by a factor of 1000 | Schema migration changed `strike_price` from `DECIMAL(10,2)` to `DECIMAL(12,4)`. Migration script multiplied values instead of casting — `WHERE strike_price < 100` re-ran on already-multiplied values. | Every schema migration must include: (a) pre-migration data snapshot/checksum, (b) migration script with idempotency guard (migration_version flag), (c) post-migration reconciliation query comparing row counts and value distributions at 1st, 50th, 99th percentiles. | 1. Add migration version: `ALTER TABLE options_flow ADD COLUMN migration_version INT DEFAULT 0` 2. Pre-migration checksum: `SELECT COUNT(*), AVG(strike_price), PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY strike_price) FROM options_flow` 3. Migration guard: `WHERE migration_version < {target_version}` 4. Post-migration reconciliation: compare pre/post checksums 5. Reject migration if any column differs beyond 0.01% |
| `requests.exceptions.HTTPError: 429 Client Error: Too Many Requests` + `grep -rn "requests\.\|httpx\.\|urllib" src/ -A 5 \| grep -v "rate.limit\|sleep\|backoff\|TokenBucket"` | Daily tick volume 3× higher than vendor contract allowed — $50K overage charge in first month | Assumed vendor's "unlimited" tier was actually unlimited. Burst traffic during earnings season exceeded the 100M quotes/day soft cap at $0.001/quote overage rate. | Review vendor rate cards quarterly (not marketing pages). Implement per-vendor rate limiters with daily cost budgets. Set cost alerts at 50%, 75%, and 90% of monthly budget. Model costs using 99th-percentile daily volume, not average. | 1. Pull actual rate card: `curl -s "https://api.polygon.io/vX/usage" -H "Authorization: Bearer $KEY" \| jq .rate_limits` 2. Configure hard limit at 80% of tier cap: `rate_limiter = TokenBucket(rate=daily_tier_cap * 0.8 / 86400)` 3. Cost alerts: `if daily_cost > budget * 0.5: send_alert()` 4. Model worst case: `worst_case_monthly = peak_daily_quotes * 21 * overage_rate; assert worst_case_monthly < monthly_budget` |
| `KeyError: 'close'\|TypeError: 'NoneType'\|ValueError: cannot convert float NaN` + `grep -rn "stale\|freshness\|timestamp\|age" src/ -A 3 \| grep -v "check\|validate\|assert"` | Stale quote detection not running — pipeline fed 4-hour-old quotes to quant models for 3 hours before anyone noticed | No data freshness gate. Market data feed silently dropped during pre-market but pipeline continued processing last-cached prices. Timestamp column existed but no automation checked it. | Implement data freshness checks on every pipeline stage. Reject data older than 60s during market hours. Add heartbeat monitoring with automated pipeline halt if feed is stale > 120s. | 1. Freshness gate: `if (datetime.now() - quote.timestamp).seconds > 60: raise StaleDataError()` 2. Heartbeat monitoring: `SELECT MAX(ingested_at) FROM options_flow; if now() - max > 120s: send_pagerduty()` 3. Automated halt: `if stale_count > 100: freeze_downstream_pipelines()` 4. Test: inject stale data → verify rejection and alert |
| `pyarrow.lib.ArrowInvalid\|parquet\|IOError\|No such file` + `grep -rn "write_to_parquet\|to_parquet\|write_parquet" src/ \| grep -v "verify\|checksum\|validate\|row.count"` | Parquet export partially written — half the day's data missing, quant model trained on 50% of actual volume | Pipeline crashed mid-export (OOM, disk full, network blip). The partial Parquet file was written without verification. Downstream consumers read the partial file as complete — no row count check. | Write to a temp file first, verify row count matches source, then atomically rename. Add daily export integrity check: row count match, date range is exactly one day, no nulls in required columns. | 1. Atomic write: `df.to_parquet(f'{output_path}.tmp'); assert len(df) == expected_rows; os.rename(f'{output_path}.tmp', output_path)` 2. Integrity check: `exported = pq.read_table(output_path); assert len(exported) == source_row_count; assert exported.column('date').unique().to_pylist() == [expected_date]` 3. Cron: `python3 scripts/verify_parquet_exports.py --date $(date -d 'yesterday' +%Y-%m-%d)` → fail if any check fails |
| `ImportError: No module named 'avro'\|ModuleNotFoundError: No module named 'confluent_kafka.schema_registry'` + `grep -rn "json.dumps\|json.loads" src/streaming/` finds JSON in Kafka producer | Kafka topic consumed 900GB/day of JSON instead of 90GB with Avro — $8,700/month bill vs $870 | Producer was configured with `value_serializer=lambda v: json.dumps(v).encode('utf-8')` — JSON at 50K msg/s with 500-byte payloads. Schema Registry was deployed but never enforced at the producer level. | Enforce Avro or Protobuf at the producer via Schema Registry. Set `value.serializer=AvroSerializer(schema_registry_client, schema_str)`. Reject JSON payloads at the producer — configure `json.enable=false` in broker config. | 1. Find JSON producers: `grep -rn "json.dumps\|json.loads" src/streaming/ --include="*.py"` 2. Replace with Avro: `from confluent_kafka.schema_registry.avro import AvroSerializer` 3. Schema Registry check: `curl -s http://schema-registry:8081/subjects/options-flow-value/versions/latest` 4. Enforcement: set broker config `json.validator.enable=true` to reject JSON on wire |
## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->
<!-- Run: `bash scripts/checklist-mktdata.sh` for automated pass/fail on all items. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | All market data vendor API keys stored in secrets manager, never in config files or env vars | `grep -rn "API_KEY\|api_key\|token.*=" config/ --include="*.yml" --include="*.py" --include="*.env" \| grep -v "os.environ\|secret\|vault"` → must return 0 results | CI lint: `detect-secrets scan --all-files` in pre-commit hook |
| **[S2]** | Rate limiters configured per vendor with daily cost budgets and hard caps at 80% of tier limit | `python3 -c "from pipeline.rate_limiter import check_limits; assert check_limits()['all_configured'], f'Missing: {check_limits()[\"missing\"]}'"` → exit 0 | Template: copy `templates/rate_limiter.py` into `pipeline/rate_limiter.py` |
| **[S3]** | Market-hours calendar integrated via `pandas_market_calendars` or `exchange_calendars` — no hardcoded 9:30-16:00 | `grep -rn "9:30\|16:00\|market.*open\|market.*close" src/ --include="*.py" \| grep -v "calendar\|trading_calendar\|is_trading_day"` → must return 0 | Replace all hardcoded times with `calendar.open_time` and `calendar.close_time` |
| **[S4]** | Data source redundancy: at least 2 independent sources for volume/OI with automated cross-source reconciliation | `python3 -c "from pipeline.reconciliation import check_redundancy; assert len(check_redundancy()['sources']) >= 2, 'Need >=2 data sources'"` → exit 0 | `python3 scripts/add_fallback_source.py --primary=Polygon --fallback=CBOE` |
| **[S5]** | Options flow schema includes `adj_factor`, `raw_strike`, `raw_premium`, `corp_action_id` columns | `psql $DATABASE_URL -c "SELECT column_name FROM information_schema.columns WHERE table_name='options_flow' AND column_name IN ('adj_factor','raw_strike','raw_premium','corp_action_id')" \| wc -l` → must return 4 | Migration: `ALTER TABLE options_flow ADD COLUMN IF NOT EXISTS raw_strike DECIMAL(12,4), ADD COLUMN IF NOT EXISTS adj_factor DECIMAL(10,6) DEFAULT 1.0` |
| **[S6]** | TimescaleDB hypertable created with 1-day chunk interval; compression enabled for chunks > 7 days | `psql $DATABASE_URL -c "SELECT * FROM timescaledb_information.hypertables WHERE hypertable_name='options_flow'" \| grep options_flow` → must return 1 row | `SELECT create_hypertable('options_flow', 'ingested_at', chunk_time_interval => INTERVAL '1 day'); ALTER TABLE options_flow SET (timescaledb.compress, timescaledb.compress_segmentby = 'ticker'); SELECT add_compression_policy('options_flow', INTERVAL '7 days');` |
| **[S7]** | Parquet export partitioned as `year/month/day/ticker` with ZSTD compression level 9 | `aws s3 ls s3://market-data/options/ --recursive \| head -1` → path must match `year=YYYY/month=MM/day=DD/ticker=SYM/` | `df.to_parquet(s3_path, partition_cols=['year','month','day','ticker'], compression='zstd', compression_level=9)` |
| **[S8]** | Ticker master populated with all symbols since 2015, including delisted/bankrupt/acquired tickers | `psql $DATABASE_URL -c "SELECT COUNT(DISTINCT ticker), MIN(first_trade_date), MAX(COALESCE(last_trade_date, CURRENT_DATE)) FROM ticker_master"` → must show >= 10,000 tickers, min date <= 2015-01-01 | Script: `python3 scripts/backfill_ticker_master.py --source=CRSP --start-date=2015-01-01` |
| **[S9]** | Avro or Protobuf serialization enforced via Schema Registry — JSON rejected at producer level | `curl -s http://schema-registry:8081/subjects/options-flow-value/versions/latest \| jq .schema` → must return valid Avro schema | Broker config: `json.validator.enable=true`. Producer config: `value.serializer=AvroSerializer(schema_registry_client, schema_str)` |
| **[S10]** | Dead letter queue monitored: DLQ consumer count > 0 triggers daily alert; DLQ replay mechanism tested end-to-end | `kafka-consumer-groups --bootstrap-server localhost:9092 --group dlq-monitor --describe \| grep options-flow-dlq \| awk '{print $5}'` → LAG must be < 1000 | `pytest tests/test_dlq_replay.py` — inserts test messages to DLQ, replays, verifies end-to-end |
| **[S11]** | Corporate actions processing runs BEFORE any downstream analytics — freeze downstream if actions are unapplied | `python3 -c "from pipeline.corp_actions import check_status; assert check_status().applied_today, 'Corp actions not applied today'"` → exit 0 | Cron: `python3 scripts/apply_corp_actions.py --date $(date +%Y-%m-%d)`. Downstream gate: `if not corp_actions_applied: sys.exit('FREEZE: corp actions not applied')` |
| **[S12]** | Stale quote detection running every 2 min during market hours; alert if >100 quotes >5 min old | `python3 -c "from pipeline.quality import check_staleness; s = check_staleness(); assert s.stale_count < 100, f'{s.stale_count} stale quotes'"` → exit 0 | Cron (market hours): `*/2 9-16 * * 1-5 python3 scripts/check_stale_quotes.py --max-age 300 --max-count 100` |

## Footguns
<!-- DEEP: 10+min — war stories from market data infrastructure -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| Options chain showed 10,000 open interest at a strike that didn't exist — the corporate action adjustment was applied to the raw OI but the strike column wasn't adjusted | A quant desk at a $500M fund ran a covered call screen in May 2024. The screener flagged ticker VMW as having 12,000 OI at the $95 strike with 95th-percentile IV. The desk sold 2,000 contracts. The actual adjusted strike was $142.50 (post-Broadcom acquisition adjustment), making the calls deep ITM. The desk was assigned at $95 — a $9.5M gap between expected and realized outcome. The data pipeline split-adjusted the OI number but not the strike price field. | Two separate ETL jobs handled strikes and OI. The strikes job ran on a Monday holiday schedule but the OI job ran on the regular schedule. On the Tuesday after Memorial Day 2024, OI was adjusted but strikes still reflected pre-acquisition values for 36 hours until the next scheduled run. | **Atomic corporate action batches.** All adjustments for a single corporate action — strikes, OI, volume, Greeks — must be applied in a single transaction that either fully succeeds or fully rolls back. Never run independent jobs on related columns. Add a reconciliation query that runs hourly: `SELECT DISTINCT corp_action_id FROM options_flow WHERE adj_strike IS NOT NULL AND adj_oi IS NULL` — if it returns rows, halt all downstream pipelines. |
| Tick data pipeline cost $87,000/month instead of the modeled $28,000 because the vendor's "unlimited" tier capped at 100M quotes/day and the burst pricing kicked in during FOMC days | A market data team at a crypto quant shop migrated from Alpaca to Polygon.io's $2,499/month "unlimited" tier in January 2025. They modeled 30M quotes/day based on average January volume. On FOMC days ( Jan 29, Mar 19), SPX options volume spiked to 280M quotes. Polygon's overage rate was $0.001/quote beyond 100M. The team got a $59,000 overage invoice for March 2025 alone. | The team modeled costs on average daily volume, not peak. They never read the fine print of Polygon's rate card, which defines "unlimited" as 100M API calls/month for stocks and options combined. | **Model costs on your 99th-percentile day, not your 50th.** Pull the vendor's actual rate card (not the marketing page) and compute: `peak_daily_quotes × trading_days × overage_rate = worst_case_monthly`. If that number exceeds your budget, implement a hard rate limiter at 80% of the tier cap. Set cost alerts at 50%, 75%, and 90% of monthly budget. Negotiate a custom enterprise agreement if you're within 2× of a tier cap. |
| A schema migration changed `strike_price` from `DECIMAL(10,2)` to `DECIMAL(12,4)` — all historical strikes under $10 became 100× larger because the migration multiplied instead of casting | In November 2023, a data engineering team at a retail brokerage widened the strike precision on their options flow database. The migration script was: `UPDATE options_flow SET strike_price = strike_price * 100 WHERE strike_price < 100`. The intent was to convert dollar notation to cent notation. But 3.4M rows with strikes under $10 (SPY puts, penny stocks) got multiplied again on a re-run because the `WHERE` clause checked the raw value, not a migration-flag column. SPY $4 puts became $400 puts. The error was detected 4 days later when a trader noticed a $0.05 put being flagged as "deep ITM." | The migration had no idempotency guard. There was no pre-migration data hash, no post-migration validation against a known-good sample. The `WHERE` clause was state-dependent — it relied on the column's current value rather than a migration version flag. | **Never write state-dependent migration conditions.** Add a `migration_version` column or use a separate migration tracking table. Every migration must: (1) compute a checksum of the affected rows before running, (2) apply the change in a transaction, (3) compute the checksum after, (4) validate the delta matches expectations. Test migrations on an anonymized production-sized snapshot — 10K rows in staging won't surface precision bugs. |
| The Parquet data lake showed 900GB of data for a single trading day — someone ingested raw FIX messages instead of normalized trades | A market data team configured a Redpanda → S3 Parquet pipeline for options trades. The producer was supposed to publish only normalized JSON trade records. A developer accidentally pointed the same pipeline at the raw FIX message topic during testing — and forgot to switch it back. For 6 months, the "options trades" Parquet dataset contained raw FIX 4.4 messages (every heartbeat, sequence reset, and session-level message). The data lake ballooned to 340TB. Athena queries timed out because every query scanned gigabytes of FIX administrative messages. | The pipeline had no schema validation at the Parquet writer level. It accepted any JSON payload and wrote it into the "trades" prefix. There was no byte-size anomaly alert on the daily export — 900GB vs the expected 4GB should have triggered an alert on day 1. | **Enforce schema at the producer, consumer, and storage layers.** Avro/Protobuf schema registry at the producer. JSON Schema validation at the consumer (before writing to Parquet). Daily Parquet partition size monitoring: if any partition exceeds 3 standard deviations of the 30-day rolling average, halt the pipeline and investigate. The schema registry is your contract — if a message doesn't match, dead-letter it, never silently write it. |
| A corporate action adjusted 100% of the options chain — but the underlying stock price in the same database wasn't adjusted, so every Greek computation was wrong for 3 days | When Google executed its 20:1 stock split in July 2022 (via Alphabet's GOOGL), a market data pipeline correctly adjusted all GOOGL option strikes and contract multipliers. But the equity price feed — a separate ETL job from IEX Cloud — continued reporting the pre-split price of ~$2,200 for 3 days because the IEX feed had a 48-hour adjustment lag. The quant desk's Black-Scholes engine used the adjusted strikes with the unadjusted spot price, producing delta estimates that were off by 300-500%. | The equity price feed and options feed came from different vendors with different adjustment schedules. There was no cross-feed reconciliation that verified "does the spot price × contract multiplier ≈ the ATM strike range?" | **Reconcile cross-feed consistency daily.** After every corporate action: compute the ATM strike from the options chain. Multiply by the contract multiplier. Verify it's within 1% of the spot price from the equity feed. If not, freeze all options analytics until the feeds are consistent. Use a single vendor or synchronize adjustment schedules contractually. A split-adjusted option with an unadjusted stock price is financial poison — every derived value is wrong. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You ingest data and assume it's correct — no validation, no cross-source reconciliation | Your pipeline runs automated reconciliation against 2+ independent sources and halts downstream consumers when discrepancies exceed thresholds | You've designed a data platform where quants and traders never ask "is this data right?" because your pipeline has caught every error before they could see it — and you can prove it with 18 months of zero-surprise metrics |
| You run `ALTER TABLE` in production without knowing whether it rewrites the entire table or takes an exclusive lock | You test every schema migration on a production-sized anonymized copy, measure lock acquisition time, and validate data integrity with pre/post checksums | You've migrated a 50TB time-series database between storage backends (PostgreSQL → ClickHouse) with zero data loss and under 30 minutes of read downtime |
| You model pipeline costs on average daily volume and are surprised by the invoice every month | You model costs on 99th-percentile volume with per-vendor rate limiters and budget alerts — and you haven't had a surprise overage in 12 months | You've negotiated a multi-vendor data contract that saved 40% vs list pricing because you knew your exact peak throughput, redundancy requirements, and latency SLA per feed |

**The Litmus Test:** Take a random trading day from 3 years ago (not a day you've tested before). Ingest the raw data from two different vendors. Adjust for corporate actions. Produce a Parquet dataset. Now have a quant run their standard analysis pipeline on your data and the same analysis on Bloomberg terminal data. If any derived number differs by more than 0.1%, you have a pipeline bug. If you can't do this in under 4 hours for a single ticker, your pipeline isn't production-grade.

## Cross-skills Integration
<!-- QUICK: 30s — real skill chains, not boilerplate -->

Market data engineering feeds every quantitative and analytical downstream system. The data you produce — cleaned, adjusted, partitioned — is the foundation for alpha generation, risk management, and regulatory reporting.

### Predecessor → This Skill → Successor

```
data-engineer                  market-data-engineer            quantitative-analyst
(general ETL patterns)  ──►  (options flow, tick storage,  ──► (Greeks analysis,
                              corporate actions, Parquet        IV surface modeling,
                              warehousing)                      options pricing)

database-reliability-         market-data-engineer            data-scientist
engineer               ──►   (TimescaleDB hypertables,     ──► (UOA detection ML,
(TimescaleDB/ClickHouse       ClickHouse mat. views)             flow sentiment models,
operations, backup)                                              strategy backtesting)

                              market-data-engineer            backend-developer
                              (Parquet/S3 data lake,         (REST API serving
                              Athena-queryable archives) ──►  options data to
                                                              trading dashboard)
```

### Concrete Integration Commands

**Chain 1: Flow Ingestion → Adjustment → Quant Analysis**
```bash
# Phase 1: Market data engineer ingests and normalizes
python ingest_flow.py --date 2024-06-14 --tickers AAPL,SPY,TSLA
python apply_corporate_actions.py --as-of 2024-06-14
python export_to_parquet.py --date 2024-06-14

# Phase 2: Quantitative analyst consumes adjusted Parquet
# Reads from s3://market-data/options/year=2024/month=06/day=14/
python build_iv_surface.py --date 2024-06-14 --output signals/iv_skew.csv
```

**Chain 2: Streaming → TimescaleDB → UOA Detection**
```bash
# Market data engineer sets up streaming
docker compose up -d kafka timescaledb
python stream_processor.py --topics options.flow.raw,options.flow.enriched

# Data scientist runs unusual options activity model
# Queries TimescaleDB hot storage for last 24 hours of flow
python uoa_detector.py --lookback 24h --threshold 3.0 --output alerts/uoa_signals.json
```

**Chain 3: Corporate Actions → Database Reliability → Backtesting**
```bash
# Market data engineer processes corporate action
python process_daily_corporate_actions.py --as-of 2024-06-10

# Database reliability engineer verifies TimescaleDB health
python check_hypertable_health.py --table options_flow
python verify_compression.py --table options_flow --older-than 7d

# Quantitative analyst runs backtest on adjusted data
python run_backtest.py --strategy covered_call --start 2020-01-01 --end 2024-06-01
```

### Coordination Table

| Coordinate With | When | What to Share/Ask |
|---|---|---|
| **data-engineer** | Setting up general ETL infrastructure (Airflow/Dagster, dbt project) | Raw data schemas, ingestion frequency, partitioning strategy, data freshness SLAs |
| **database-reliability-engineer** | TimescaleDB hypertable sizing, ClickHouse cluster design, backup strategy | Ingestion rate (rows/sec), query patterns (time-range, ticker-filtered), retention requirements, compression ratios |
| **quantitative-analyst** | Options pricing model inputs, Greeks data requirements, IV surface needs | Adjusted options chains, corporate action history, dividend schedules, point-in-time data availability dates |
| **data-scientist** | UOA detection model training, flow sentiment features, anomaly detection | Enriched flow data (size, premium, condition), historical patterns, labeled unusual activity events |
| **backend-developer** | API for options data access, real-time streaming endpoint | Parquet file locations, Athena table schemas, query patterns (by ticker, date range, strike/expiry), expected latency |
| **devops-engineer** | Kafka cluster deployment, stream processor containerization, CI/CD for pipeline code | Resource requirements (CPU/memory for Faust workers, Kafka broker sizing), deployment frequency, rollback procedures |
| **security-engineer** | API key rotation, financial data access controls, PII in trade data | Vendor API key inventory, data classification (market data = confidential, trade data with client IDs = restricted), encryption requirements for data at rest |
| **finops-engineer** | API cost monitoring, S3 storage cost optimization, Kafka cluster cost allocation | Per-vendor daily spend, S3 storage by tier (hot/warm/cold), data transfer costs, cost per query metrics |
| **algorithmic-trader** | Live trading execution, order management, broker connectivity | Data freshness for trade signals — stale data means bad entries. **Decision gate:** Is pipeline latency < 500ms? → live trading OK. **Artifact:** data freshness SLA report per venue. |
| **backend-developer** | API gateway, query service, caching layer for data access | API design for data consumption patterns. **Decision gate:** Can query serve 100 concurrent requests at < 3s p99? → API is production-ready. **Artifact:** load test report + API schema docs. |

## Cross-Skill Coordination
<!-- QUICK: 30s — table of who to talk to when -->

Market data engineers sit at the intersection of infrastructure, quantitative research, and trading operations. They coordinate with data engineers for pipeline infrastructure, quantitative analysts for data requirements, database reliability engineers for storage operations, and security engineers for financial data compliance.

### Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| **Corporate action announced** (split, dividend, merger) | quantitative-analyst, data-scientist | Adjusted data will be available within 1 hour; downstream models must account for adjustment lag |
| **Market data vendor API outage** (Polygon 503, Unusual Whales WebSocket disconnect) | quantitative-analyst, devops-engineer | Real-time flow data gap; estimate recovery time; switch to backup vendor if available |
| **Data quality check failure** (stale quotes, volume spike, parity violation) | quantitative-analyst, data-scientist | Downstream analytics may be corrupted; hold model retraining until quality restored |
| **Kafka consumer lag > 5 min during market hours** | devops-engineer, database-reliability-engineer | Streaming pipeline degraded; TimescaleDB ingestion delayed; investigate broker health and consumer throughput |
| **Parquet export integrity failure** (row count mismatch) | quantitative-analyst, data-scientist | Historical archive may have gaps; do not use affected date range for backtesting until re-exported |
| **API cost budget exceeded** (daily spend > threshold) | finops-engineer, devops-engineer | Review rate limiter config; consider vendor tier upgrade or request frequency optimization |
| **New options data source onboarding** | quantitative-analyst, data-scientist, backend-developer | Schema design review, historical backfill plan, API endpoint documentation needed |
| **Data retention policy change** (e.g., extend cold storage from 7 to 10 years) | database-reliability-engineer, finops-engineer | S3 storage cost impact estimation, rehydration testing for older partitions |

### Escalation Path
```
Market data pipeline down (production)? → devops-engineer → site-reliability-engineer (if SEV2+)
Options data quality breach (widespread stale/corrupt data)? → quantitative-analyst → data-scientist
API cost overrun > 200% daily budget? → finops-engineer → cto-advisor
Corporate action missed for major index constituent? → quantitative-analyst → cto-advisor (legal/regulatory risk)
PII discovered in raw market data feed? → security-engineer → compliance-officer
```

## Proactive Triggers
<!-- QUICK: 30s -- when to proactively notify stakeholders -->

| Trigger | Notify | Why |
|---------|--------|-----|
| Data feed latency exceeds 60 seconds during market hours | quantitative-analyst + algorithmic-trader | Real-time UOA detection and trade signals are degraded; downstream consumers trading on stale data must halt until feed recovers |
| Kafka consumer lag exceeds 50K messages or 5 minutes during market hours | devops-engineer + database-reliability-engineer | Streaming pipeline bottleneck; TimescaleDB ingestion falling behind; risk of data loss if lag exceeds topic retention window |
| Vendor API cost exceeds 75% of daily budget before 11 AM ET | finops-engineer + devops-engineer | On track for daily budget overrun; consider rate-limit tightening or vendor tier upgrade before overage charges hit at month-end |
| Daily quarantine table exceeds 1% of ingested rows | quantitative-analyst + data-scientist | Data quality degradation — downstream analytics potentially corrupted; investigate root cause and quarantine pattern before next model training run |
| Corporate action announced for top-50 index constituent (split, dividend, merger) | quantitative-analyst + algorithmic-trader | Adjusted data will lag announcement by up to 1 hour; all models consuming unadjusted prices for this ticker are unreliable until processing completes |
| Cross-source reconciliation shows >15% volume discrepancy between vendors | quantitative-analyst + data-scientist | One data source is reporting incorrect volume; backtests and signals consuming the bad source are invalid; identify source of truth and quarantine the bad feed |
| Parquet export integrity check fails (row count mismatch or nulls in required columns) | quantitative-analyst + data-scientist | Historical archive has gaps; affected date range must be excluded from backtesting until re-export completes and passes integrity check |
| Primary vendor API returns 503 for 3+ consecutive requests | devops-engineer + quantitative-analyst | Vendor outage confirmed; initiate failover to backup data source; estimate data gap duration and notify all downstream consumers of recovery ETA |

## What Good Looks Like
<!-- QUICK: 30s — the concrete definition of success -->

A production-quality market data pipeline that passes all 25 production checklist items produces the following observable outcomes:

**Data Freshness:** Real-time flow data arrives in TimescaleDB within 500ms of WebSocket message. End-of-day options chain data exported to Parquet by 18:00 ET. Corporate actions applied within 1 hour of announcement.

**Data Correctness:** Options strikes match exchange-reported values within 0.01. Put-call parity holds within 1% of spot for 99.9% of observations. Cross-source volume reconciliation shows < 5% discrepancy per ticker. Zero stale quotes during market hours.

**Historical Integrity:** Querying any ticker on any date from 2010-2025 returns complete, split-adjusted, dividend-adjusted data. Delisted tickers are preserved with their full trading history. Survivorship bias is eliminated — backtests show realistic win/loss ratios matching live trading.

**Operational Reliability:** Pipeline uptime > 99.9% during market hours. Kafka consumer lag < 10K messages. DLQ messages < 0.01% of total throughput. API cost within 90% of daily budget. All alerts actionable within 15 minutes.

**Consumability:** Parquet archives queryable in < 3 seconds via Athena for any single-ticker single-day query. ClickHouse materialized views refresh within 5 minutes. Data dictionary documents every column with business meaning, type, and source. Downstream skills (quantitative-analyst, data-scientist) can consume data without market-data-domain expertise.

**What you should see when it works:**
```bash
# Verify pipeline health
$ curl https://monitoring.internal/api/v1/pipeline-health
{"status":"healthy","lag_ms":120,"rows_ingested_24h":43200000,"dlq_size":47,"cost_today":78.50}

# Query yesterday's AAPL options flow — returns in < 500ms
$ psql -c "SELECT COUNT(*), SUM(premium) FROM options_flow
           WHERE ticker='AAPL' AND trade_timestamp::date = CURRENT_DATE - 1;"
 count  |   sum
--------+----------
 184723 | 4521000.50
```

## Scale Depth
<!-- QUICK: 30s -- find your team size column -->

### Solo
- **What changes**: Single data source, batch ETL, CSV/Parquet files. Get usable data, learn the domain. Manual downloads and cron jobs; one asset class; local storage.
- **What to skip**: Real-time streaming (batch is fine). Multi-venue aggregation. Data quality SLAs. Tick-level storage. Regulatory compliance infrastructure.
- **Coordination**: Self-contained. Manual data checks. Weekly pipeline review.
- **Cost**: Free — Polygon.io free tier, CSV files, local PostgreSQL.

### Small Team
- **What changes**: Real-time streaming, multiple venues, automated pipeline. Reliable data flow, reduce latency. WebSocket feeds replace batch; data lands in DB within seconds.
- **What to skip**: Tick-level data for all tickers. Multi-asset coverage beyond core universe. Petabyte-scale data lake. Internal data marketplace.
- **Coordination**: Daily data quality checks. Weekly pipeline review with trading team. Coordinate with vendor for feed reliability.
- **Cost**: $1K-$5K/month (paid data feeds, Kafka cluster, cloud infrastructure).

### Medium Team
- **What changes**: Tick-level data, multi-asset coverage, data quality SLAs. Breadth and depth of coverage. Every tick captured; options flow + equities + futures; data quality monitoring.
- **What to skip**: FPGA-accelerated feed processing. Full regulatory reporting infrastructure. Internal data products for external sale.
- **Coordination**: Daily data quality meeting. Weekly pipeline performance review. Monthly vendor contract review. Cross-team data governance.
- **Cost**: $10K-$50K/month (multiple data feeds, Kafka+ClickHouse cluster, cloud compute, data team).

### Enterprise
- **What changes**: Petabyte-scale data lake, regulatory reporting, data marketplace. Institutional-grade infrastructure. SEC CAT/Reg NMS compliance; historical replay; internal data products sold to clients.
- **What's full production**: 24/7 data operations team. Dedicated data quality team. Regulatory compliance team. Internal data product P&L.
- **Coordination**: Daily ops handoff. Weekly data governance meeting. Monthly regulatory reporting review. Quarterly vendor audit.
- **Cost**: $100K-$500K+/month (colocation, direct exchange feeds, data team, compliance, storage).

### Transition Triggers

| From \u2192 To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo \u2192 Small | Reliable data needed for trading decisions, >5 data sources | Move from batch to streaming; add Kafka; formalize schema management |
| Small \u2192 Medium | Multi-asset coverage, tick-level requirements, AUM >$10M | Add ClickHouse for analytics; implement data quality SLAs; hire dedicated data engineer |
| Medium \u2192 Enterprise | Regulatory requirements (SEC CAT), internal data products, >$100M AUM | Implement full data governance; build data marketplace; hire compliance and data ops teams |

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
<!-- QUICK: 30s — links to deeper reading and reference documentation -->

### Skill References (create these in `references/` directory)
- **[Market Data Sources Guide](references/market-data-sources.md)** — Detailed API documentation for Unusual Whales (REST + WebSocket), Polygon.io Options API, CBOE LiveVol, and Bloomberg Terminal/blpapi. Includes authentication patterns, rate limits, response schemas, and cost comparison matrix.
- **[Options Data Schema Reference](references/options-schema-reference.md)** — Complete DDL for all tables (options_flow, corporate_actions, ticker_master, options_chain_snapshots), column descriptions with business meaning, indexing strategy rationale, and TimescaleDB hypertable configuration.
- **[Corporate Actions Processing Guide](references/corporate-actions-guide.md)** — Step-by-step procedures for handling stock splits, reverse splits, cash dividends, stock dividends, mergers, spin-offs, ticker changes, and delistings. Includes adjustment formulas, multi-leg corporate action handling, and reconciliation checks.
- **[Streaming Pipeline Operations](references/streaming-pipeline-ops.md)** — Kafka/Redpanda topic configuration, Faust stream processor deployment, DLQ management, consumer group monitoring, schema registry operations, and incident response playbooks.
- **[Data Quality Rulebook](references/data-quality-rulebook.md)** — Detailed specifications for stale quote detection, put-call parity checks, volume/OI anomaly detection, cross-source reconciliation, and quarantine table management.

### External References
- Unusual Whales API Docs: https://docs.unusualwhales.com
- Polygon.io Options API: https://polygon.io/docs/options
- CBOE LiveVol Data: https://www.cboe.com/delayed_quotes/livevol
- Bloomberg API (blpapi): https://www.bloomberg.com/professional/support/api-library
- TimescaleDB Documentation: https://docs.timescale.com
- ClickHouse Documentation: https://clickhouse.com/docs
- Apache Parquet: https://parquet.apache.org/docs
- pandas_market_calendars: https://pypi.org/project/pandas-market-calendars
- OCC Options Adjustment Notices: https://www.theocc.com/company-information/dividends-and-corporate-actions
- SEC EDGAR Corporate Filings: https://www.sec.gov/edgar

