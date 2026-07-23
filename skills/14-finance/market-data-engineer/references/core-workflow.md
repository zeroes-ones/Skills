# Core Workflow — Full Implementation

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
