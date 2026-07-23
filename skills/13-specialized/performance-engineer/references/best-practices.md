# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
1. **Profile before you optimize:** Never guess the bottleneck. APM > flame graph > EXPLAIN ANALYZE before any code change. Guessing wastes time and often makes things worse.
2. **Fix one bottleneck at a time:** If you change indexes, add caching, and tune GC simultaneously, you can't tell what worked. One change → measure → decide next step.
3. **Vertical scale first:** Try a bigger instance before building a distributed system. A $50/month instance upgrade beats $5K/month of engineering time on horizontal scaling.
4. **Cache the hot data, not everything:** A Redis cluster with 5% hit rate adds latency without benefit. Find the 3 queries responsible for 80% of DB load — cache only those.
5. **SLOs without burn-rate alerts are wishes:** "P95 < 500ms" means nothing if no one wakes up when it's violated. Set 2% error budget burn over 1 hour as your first alert.
6. **Load test in CI, not just before launch:** A load test the night before Black Friday that finds a 10x slowdown leaves no time to fix. Run 60s benchmarks on every PR.
7. **Performance budgets prevent regressions:** Without a CI gate that fails on bundle size or P95 increase, optimizations slowly erode. Set numeric budgets and enforce them.
8. **Monitor the right percentile:** Average latency hides the bad experiences. P95 is the minimum. P99 shows your worst users. Track both — P50 alone is deceptive.
9. **Database queries are the #1 bottleneck:** Before profiling CPU or tuning GC, run EXPLAIN ANALYZE on the top 5 queries by total_time. Missing indexes fix 60% of perf issues.
10. **Don't optimize what's not slow:** If all endpoints are P95 <200ms and LCP <2s, stop optimizing. Set baselines, monitor, and ship features instead.
