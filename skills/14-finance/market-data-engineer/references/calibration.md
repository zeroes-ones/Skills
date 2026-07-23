# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You ingest data and assume it's correct — no validation, no cross-source reconciliation | Your pipeline runs automated reconciliation against 2+ independent sources and halts downstream consumers when discrepancies exceed thresholds | You've designed a data platform where quants and traders never ask "is this data right?" because your pipeline has caught every error before they could see it — and you can prove it with 18 months of zero-surprise metrics |
| You run `ALTER TABLE` in production without knowing whether it rewrites the entire table or takes an exclusive lock | You test every schema migration on a production-sized anonymized copy, measure lock acquisition time, and validate data integrity with pre/post checksums | You've migrated a 50TB time-series database between storage backends (PostgreSQL → ClickHouse) with zero data loss and under 30 minutes of read downtime |
| You model pipeline costs on average daily volume and are surprised by the invoice every month | You model costs on 99th-percentile volume with per-vendor rate limiters and budget alerts — and you haven't had a surprise overage in 12 months | You've negotiated a multi-vendor data contract that saved 40% vs list pricing because you knew your exact peak throughput, redundancy requirements, and latency SLA per feed |

**The Litmus Test:** Take a random trading day from 3 years ago (not a day you've tested before). Ingest the raw data from two different vendors. Adjust for corporate actions. Produce a Parquet dataset. Now have a quant run their standard analysis pipeline on your data and the same analysis on Bloomberg terminal data. If any derived number differs by more than 0.1%, you have a pipeline bug. If you can't do this in under 4 hours for a single ticker, your pipeline isn't production-grade.
