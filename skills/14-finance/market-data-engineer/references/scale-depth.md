# Scale Depth

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
