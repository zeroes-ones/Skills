# Token-Efficient Workflow

```
# Step 1: Quick bottleneck detection
python3 scripts/perf_scan.py --service checkout --output json
# Returns: {"p95_ms": 850, "db_time_pct": 65, "cache_hit_pct": 23, 
#           "gc_pause_ms": 15, "top_slow_query": "SELECT * FROM orders WHERE..."}

# Step 2: Decision tree → single action
# db_time_pct > 50% → Database is the bottleneck. Run EXPLAIN ANALYZE on top query.
# cache_hit_pct < 30% → Cache isn't helping. Re-evaluate TTLs or eviction policy.
# gc_pause_ms > 50 → GC tuning needed. Check heap size, allocation rate.

# Step 3: Quick fix verification
# After adding index, verify query performance
psql $DATABASE_URL -c "EXPLAIN ANALYZE SELECT * FROM orders WHERE status='pending'" \
  | grep "Execution Time"  # Compare before/after

# Run k6 load test for 60 seconds, check P95
k6 run --duration 60s --vus 50 load-test.js 2>&1 | \
  python3 -c "import sys,json; d=json.load(sys.stdin); 
  print(f'P95: {d[\"metrics\"][\"http_req_duration\"][\"p(95)\"]}ms')"

# Step 4: Post-fix verification
python3 scripts/perf_scan.py --service checkout --compare-before --output json
# Exit code 0 = improved, 1 = worsened (roll back)
```

**Principle:** `perf_scan.py` queries APM API or parses logs for structured metrics. Agent sees one bottleneck, applies one fix. k6 outputs JSON with P95 latency. Exit codes confirm improvement.
