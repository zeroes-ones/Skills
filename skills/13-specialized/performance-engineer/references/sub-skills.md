# Sub-Skills

<!-- QUICK: 30s -- table of deeper dives by topic -->
When the agent identifies a specific performance bottleneck, drill into the relevant sub-skill. Each sub-skill has dedicated tools, profiling guides, and optimization playbooks in `references/`.

| Sub-Skill | What It Covers | Key Tool / Command |
|-----------|---------------|--------------------|
| **CPU & Memory Profiling** | Flame graphs, heap analysis, GC tuning, memory leak detection, allocation profiling — language-specific guides in `references/profiling-guide.md` | `py-spy record -o flame.svg -- python app.py` |
| **Database Query Optimization** | `EXPLAIN ANALYZE` deep dive, index strategy (covering, composite, partial), query rewriting (N+1 elimination, JOIN optimization), connection pooling (PgBouncer) | `psql -c "EXPLAIN (ANALYZE, BUFFERS) SELECT ..."` |
| **Load Testing** | k6 scenario design (ramp-up, soak, spike, stress), infrastructure sizing from results, statistical analysis of latency distributions, coordinated omission avoidance | `k6 run --duration 5m --vus 100 load-test.js` |
| **Frontend Performance** | Core Web Vitals (LCP, INP, CLS), bundle analysis (webpack-bundle-analyzer), critical rendering path, code splitting, image/font optimization — full cookbook at `references/frontend-performance-cookbook.md` | `npx lighthouse https://example.com --output json` |
| **Caching Strategy** | Multi-layer caching (browser, CDN, application, database), invalidation patterns (TTL, write-through, event-driven), cache stampede protection, CDN cache key design | `curl -sI https://example.com \| grep cache` |
| **Performance Budgets** | Time/size/quantity budgets, Lighthouse CI enforcement, bundlesize, break-PR-on-regression setup, SLO-based alerting | `npx lighthouse-ci --assert-pairs '{"lcp": "<2500"}'` |

> **Token-saving rule:** If P95 is high and APM shows 65% DB time, load only "Database Query Optimization" and "Caching Strategy." Don't load frontend or profiling sub-skills. The profiling guide alone is 450 lines — only load it when the bottleneck is confirmed CPU/memory-bound.
