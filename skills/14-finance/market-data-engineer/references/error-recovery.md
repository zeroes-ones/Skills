# Market Data Engineer — Error Recovery

## Symptom → Root Cause → Fix

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Backtest results differ from live after data pipeline update | Corporate action adjustment changed. Split factor applied twice or not at all. Dividend adjustment methodology changed. | Version all data transformations. Hash raw data before and after each pipeline stage. Compare adjusted prices against known reference (e.g., Yahoo Finance adjusted close). | **Data pipeline changes silently corrupt backtests.** Every transformation is a potential source of divergence. Check your adjusted prices against a public reference weekly. |
| Tick data storage costs exploding | Storing raw tick data without aggregation. No retention policy. Redundant fields. | Tiered storage: raw ticks → 1min bars → daily OHLCV. Retention: raw 30 days, 1min 2 years, daily forever. Columnar compression (Parquet with zstd). | **Tick data is a cost center until you use it.** Store what you need, aggregate what you don't, delete what you won't. |
| Real-time stream falls behind during volatility spikes | Kafka consumer lag. Processing can't keep up with message rate. | Backpressure handling: drop non-critical messages under load. Priority queue: order book updates > trades > quotes. Auto-scale consumers during VIX > 30. | **Market data volume spikes 10x during the moments you need it most.** Design for peak, not average. If your pipeline can't handle March 2020 volumes, it's not production-ready. |
| Corporate action missed, causing wrong position/P&L | Data vendor delay. Symbol change not propagated. Spin-off not reflected. | Multi-source verification: primary vendor + free source (Yahoo/IEX). Alert on symbol-day mismatch between sources. Reconciliation job runs before market open. | **One missed corporate action = wrong position sizes, wrong P&L, wrong decisions.** Automate reconciliation. Humans miss things that scripts don't. |
| Options chain data has stale or missing strikes | Vendor API rate limit. Options with zero volume not included. Expired chains not cleaned. | Cache chain snapshots with timestamp. Validate: every expiration date has contiguous strikes ±20% from ATM. Alert on missing strikes within 2% of underlying price. | **Missing strikes near the money = broken options analytics.** Greeks, P&L, and risk all depend on complete chains. |

## Provenance
[VERIFIED] Market data pipeline failure modes from production experience
[COMPUTED] Storage cost estimates based on typical data volumes
[AS OF 2026-01]

