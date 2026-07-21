---
name: performance-engineer
description: Performance profiling (flame graphs, CPU/memory/I/O), load testing (k6/wrk/Artillery), frontend optimization (Core Web Vitals, bundle analysis), database optimization, caching strategies, performance budgets, SLOs.
author: Sandeep Kumar Penchala
---

# Performance Engineer

End-to-end performance engineering framework covering profiling, load testing, bottleneck diagnosis, and optimization across the full stack — frontend, backend, database, and infrastructure.

## Sub-Skills

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

## When to Use

- Diagnosing high P95/P99 latency in a production service with unclear root cause
- Running a systematic load test before a major event (product launch, Black Friday, seasonal peak)
- Profiling CPU, memory, or I/O bottlenecks that GC logs and APM dashboards can't explain
- Designing and validating a multi-layer caching strategy (browser, CDN, application, database)
- Analyzing and optimizing frontend bundle size, JavaScript parse time, or rendering performance
- Optimizing slow database queries — index tuning, query rewriting, connection pooling
- Conducting a CDN configuration audit: cache hit ratio, TTL strategy, edge function performance
- Building performance budgets into CI to prevent regressions

## Performance Measurement

### Establishing Baselines

Instrument every layer of the stack. Without baselines, you cannot tell if an optimization helped or hurt.

| Layer | What to Measure | Tools |
|-------|----------------|-------|
| Application | Latency (P50/P95/P99), throughput, error rate per endpoint | OpenTelemetry, APM (Datadog, New Relic, Honeycomb) |
| Infrastructure | CPU, memory, disk I/O, network I/O | Prometheus + Node Exporter, Grafana |
| Database | Query latency, connections, cache hit ratio, replication lag, deadlocks | pg_stat_statements, EXPLAIN ANALYZE, slow query log |
| Frontend | LCP, INP, CLS, TTFB, FCP, JS parse time | RUM (CrUX, Web Vitals JS), Lighthouse |

### Percentile Metrics Deep Dive

- **P50 (median)**: Tells you what the "typical" user experiences — but it's misleading because it hides the tail. A service can have a 50ms P50 and a 10s P99 and still look good.
- **P95**: 95% of users are faster than this. Best single number for "most users experience acceptable performance."
- **P99**: Catches the outliers — GC pauses, cold starts, network contention. Critical for SLOs: "99% of requests complete within 500ms."
- **Histogram vs Summary**: Histograms let you compute arbitrary percentiles client-side (Prometheus `histogram_quantile`). Summaries precompute percentiles server-side but cannot be aggregated across dimensions. Prefer histograms.

### Latency Distribution & Long-Tail Latency

Long-tail latency — the few requests that take 10x longer than the median — is the most damaging to user experience. Common causes:
- **Coordinated omission**: Load tools that pause between requests (ignoring queued latency) report artificially low latency. wrk2 and k6 solve this with open-loop or constant-throughput modes.
- **Head-of-line blocking**: One slow request blocks subsequent requests in a single-threaded model.
- **Garbage collection pauses**: Stop-the-world GC in Java/C#/Go causes all threads to pause briefly — visible only at P99+.
- **Cold starts**: Serverless functions, connection pool warm-up, JVM warm-up — first request after idle is disproportionately slow.

### RED vs USE Methodologies

- **RED** (Rate, Errors, Duration): Application-focused. For every service: What is the request rate? How many are failing? How long do successful ones take?
- **USE** (Utilization, Saturation, Errors): Infrastructure-focused. For every resource: What is the utilization? Is it saturated (queue depth > 0)? Are there errors?

Use both in tandem — RED tells you _what_ is slow, USE tells you _which resource_ is the bottleneck.

## Frontend Performance

### Critical Rendering Path

The browser's process for converting HTML/CSS/JS to pixels:

1. **HTML parsing** → DOM tree — byte-by-byte parsing, progressive
2. **CSS parsing** → CSSOM tree — render-blocking by default
3. **DOM + CSSOM** → Render Tree — only visible elements
4. **Layout (Reflow)** → Box model geometry — most expensive step
5. **Paint** → Pixels — fill pixels for visible elements
6. **Composite** → Layers — GPU-accelerated compositing

**Optimizations per step**:
- Minimize render-blocking CSS (inline critical CSS, defer non-critical)
- Defer non-critical JavaScript (use `defer` or `async`)
- Avoid layout thrashing (batch DOM reads before writes)
- Use `transform` and `opacity` for animations (compositor-only, no layout/paint)
- Reduce DOM depth (shallower tree = faster layout calculations)

### Resource Prioritization

- **`<link rel="preload">`**: Critical resources the browser should load ASAP. Use for fonts, hero images, above-the-fold critical CSS/JS. Example: `<link rel="preload" href="font.woff2" as="font" crossorigin>`
- **`<link rel="prefetch">**`: Resources needed on the _next_ page. Low priority, fetched after CPU is idle. Use for likely next-page bundles.
- **`<link rel="preconnect">`**: Warm up connections (DNS + TCP + TLS) to third-party origins. Use for analytics, CDN, API endpoints. Saves ~100-500ms per origin.
- **`<link rel="dns-prefetch">`**: DNS lookup only. Fallback for preconnect — lower overhead but only saves DNS time.

### Core Web Vitals

**LCP (Largest Contentful Paint)** — Perceived load speed. Target: < 2.5s.
- **Sub-parts**:
  1. TTFB (Time to First Byte) — server response time, CDN cache status
  2. Resource Load Delay — time before the LCP resource starts loading
  3. Resource Load Time — time to download the LCP resource
  4. Element Render Delay — time from resource load to visible render
- **Optimization**: Improve TTFB (server-side rendering, CDN caching, faster backend), preload LCP image, optimize image compression, reduce render-blocking resources.

**INP (Interaction to Next Paint)** — Responsiveness. Target: < 200ms. Replaces FID.
- Measures the longest interaction latency on the page (click, tap, keyboard).
- **Optimization**: Break up long tasks (>50ms), reduce JS execution time, optimize event callbacks, avoid complex selectors in event handlers.

**CLS (Cumulative Layout Shift)** — Visual stability. Target: < 0.1.
- Caused by: images/videos without dimensions, ads/embeds injected above content, web fonts causing FOIT/FOUT.
- **Fixes**: Always set `width` and `height` on images/videos, reserve space for ads/embeds, use `font-display: optional` or `swap`, avoid inserting content above existing content.

### Bundle Analysis

- **webpack-bundle-analyzer**: Interactive treemap of your bundle. Identifies: duplicated libraries, unexpectedly large dependencies, accidental inclusion of full packages instead of subsets.
- **source-map-explorer**: Maps bundle bytes back to source files. Good for TypeScript projects where compiled output size is surprising.
- **bundlephobia.com**: Quick check of a package's size before importing it. Shows minified + gzipped size, tree-shakeability, and dependency weight.
- **Import cost** (VS Code extension): Inline annotation of import size as you type.

### Code Splitting Strategies

1. **Route-based**: Split per page/route — each page gets its own chunk. Example: `const Dashboard = React.lazy(() => import('./Dashboard'))` in React, dynamic `import()` in Next.js pages.
2. **Component-level**: Split heavy below-the-fold components. Example: heavy charts, rich text editors, data tables — load only when scrolled into view or on user interaction.
3. **Conditional imports**: Load features only when needed. Example: `if (user.isAdmin) { const AdminPanel = await import('./AdminPanel') }`.
4. **Vendor splitting**: Separate third-party code (react, lodash, moment) into a stable `vendor.js` that rarely changes — better caching.

### JavaScript Execution Cost

- **Long tasks**: Any task > 50ms blocks the main thread and delays user interactions. Chrome DevTools Performance panel highlights them in red.
- **Total Blocking Time (TBT)**: Sum of all long task durations beyond 50ms between FCP and TTI. Lighthouse metric.
- **Web Workers**: Offload CPU-heavy computation — data processing, cryptography, image manipulation — to a background thread. The main thread stays responsive.
- **`requestIdleCallback`**: Schedule non-critical work for when the browser is idle. Used for analytics, logging, deferred rendering.
- **Debounce/Throttle**: Rate-limit scroll/resize/input event handlers to avoid excessive execution.

## API Performance

### Connection Pooling

- **Pool sizing formula**: `connections = (core_count × 2) + effective_spindle_count` (traditional) or for SSDs: `connections ≈ core_count × 2 ÷ (expected_active_queries_per_connection)`
- **Connection timeout configuration**: Set `connect_timeout` (fail fast if DB is down), `idle_in_transaction_session_timeout` (release stuck connections), `statement_timeout` (kill runaway queries).
- **Idle connection management**: Tune `idle_timeout` (close unused connections), `max_lifetime` (periodically rotate connections to avoid stale ones), use connection health checks (`SELECT 1`).

### Query Optimization

- **N+1 queries**: One request triggers 1 query for a list + N queries per item. Example: fetching 100 blog posts then querying author for each. Fix: eager loading (`JOIN ... IN`), DataLoader pattern (batch + cache).
- **DataLoader**: Batching + memoization per request. Combines N individual lookups into one batched query. Standard in GraphQL ecosystems.
- **Eager loading**: Use `SELECT * FROM posts JOIN authors ON posts.author_id = authors.id` instead of N+1 individual queries.

### Response Caching

- **ETag**: Content-based hash. Client sends `If-None-Match`, server responds `304 Not Modified` if unchanged. Great for API responses that change infrequently.
- **Last-Modified**: Timestamp-based. Client sends `If-Modified-Since`. Coarser than ETag but simpler.
- **Cache-Control**:
  - `public, max-age=60, s-maxage=300` — browser caches 60s, CDN caches 300s
  - `private` — do not cache in shared caches (CDN/proxies) — for user-specific data
  - `no-cache` — revalidate with origin on every use
  - `stale-while-revalidate=86400` — serve stale data for 24h while revalidating in background
- **CDN-edge caching**: For read-heavy APIs, cache at the CDN edge. Invalidate on write (surrogate-key based purge). Reduces origin load by 60-90%.

### Compression

- **gzip**: Universal support, ~70% reduction on text. Default baseline.
- **Brotli**: 15-20% better than gzip for text, supported by all modern browsers. Use at CDN or origin (dynamic Brotli is CPU-intensive; Brotli + static caching is best).
- **zstd**: Better ratios than Brotli, faster decompression. Growing browser support. Best for static assets served via CDN.
- **When to compress**: At CDN edge for static assets (compress once, cache forever). At application level for dynamic API responses (Brotli for JSON, negotiate with `Accept-Encoding`).
- **What NOT to compress**: Already-compressed formats (JPEG, PNG, WebP, AVIF, video, audio) — waste of CPU with no benefit.

### Pagination

- **Cursor-based**: `?cursor=eyJsYXN0X2lkIjogMTAwMH0=` (base64-encoded opaque token). Stable even if data is inserted/deleted. Required for real-time or high-churn data. Preferred for APIs.
- **Offset-based**: `?offset=20&limit=10`. Simple but unstable — inserting rows before the current page shifts offset. Acceptable for static/admin UIs with small datasets (<10K rows).
- **Keyset pagination**: `WHERE id > last_seen_id ORDER BY id LIMIT 10`. Faster than offset, no skip overhead. Works only with sortable, unique columns.

## Database Performance

### Query Plan Analysis (EXPLAIN ANALYZE)

Reading a query plan from innermost to outermost:

- **Node types**:
  - **Sequential Scan**: Reads all rows — BAD on large tables. Fix: add index or add `LIMIT`.
  - **Index Scan**: Reads via index. Good. Single index lookup.
  - **Bitmap Heap Scan** + **Bitmap Index Scan**: Reads via index then fetches heap pages. Used for low-selectivity queries (many matching rows).
  - **Index Only Scan**: All needed data in the index, no heap fetch. Best case — add covering indexes.
- **Join methods**:
  - **Nested Loop**: For each outer row, probe inner. Good for small result sets or when inner side has an index.
  - **Hash Join**: Build hash table on one side, probe with other. Best for large, unsorted data sets.
  - **Merge Join**: Sort both sides then merge. Good for pre-sorted data (index order).
- **Key metrics**: `rows` (estimated) vs `actual rows` — mismatch >10x means stale statistics. `cost` — relative, not absolute. `buffers` — how many 8KB pages read.

### Index Optimization

- **Covering indexes**: Include all columns needed by a query in the index. PostgreSQL: `CREATE INDEX idx ON posts (author_id) INCLUDE (title, created_at)`. Enables index-only scans.
- **Composite index column order**: Put high-cardinality / high-selectivity columns first. `(user_id, status)` — user_id filters most rows, then status differentiates. Wrong order: `(status, user_id)` — status has few values, not selective.
- **Partial indexes**: Index only a subset of rows. Example: `CREATE INDEX idx_active_users ON users (email) WHERE active = true`. Smaller, faster.
- **Expression indexes**: Index on a function result. Example: `CREATE INDEX idx_lower_email ON users (LOWER(email))`. Enables `WHERE LOWER(email) = '...'`.
- **Write overhead**: Each index adds ~10-30% write overhead. Don't index columns you never query. Monitor `pg_stat_user_indexes` for unused indexes.

### Connection Pooling (Database)

- **PgBouncer**: Lightweight, dedicated PostgreSQL connection pooler. Three modes:
  - **Session pooling**: Connection assigned to client for entire session. Lowest overhead but uses most connections.
  - **Transaction pooling** (recommended for web apps): Connection returned to pool after each transaction. Requires no session-level state (`SET`, prepared statements).
  - **Statement pooling**: Connection returned after each statement. Even stricter — no session state at all.
- **Pool sizing**: `max_connections = (num_cores × 2) ÷ (avg_query_time ÷ avg_query_interval)`. Start at 20-30 per pooler, benchmark up.
- **Watch**: `server_idle_timeout` (close idle connections), `query_timeout` (kill stuck queries), `max_db_connections` (don't overwhelm the database).

### Read Replica Routing

- **Pattern**: Write to primary, read from replicas. Route at the application layer or via middleware (PgBouncer with replica config, ProxySQL).
- **Replication lag**: Monitor `pg_stat_replication` (PostgreSQL) or `SHOW SLAVE STATUS` (MySQL). Acceptable lag depends on use case — real-time dashboard vs historical reporting.
- **Stale read handling**: If your application cannot tolerate stale data, read-write splits must be aware: send critical reads to primary, use replica for analytics and reporting.
- **Load balancing**: Distribute read queries across replicas with health-aware round-robin. Remove unhealthy replicas from rotation automatically.

### Vacuum & Analyze (PostgreSQL)

PostgreSQL's MVCC means dead tuples accumulate on UPDATE/DELETE. Autovacuum reclaims this space.

- **Monitoring**: Check `n_dead_tup` in `pg_stat_user_tables`. If dead tuples exceed 20% of live tuples, autovacuum is falling behind.
- **Tuning**: Increase `autovacuum_vacuum_scale_factor` (default 0.2 = vacuum after 20% changed). For large tables, set it lower or use fixed thresholds.
- **When to intervene**: Run `VACUUM ANALYZE` manually after bulk updates. `VACUUM FREEZE` before long-running transactions to avoid transaction ID wraparound.
- **Bloated indexes**: `REINDEX INDEX idx_name CONCURRENTLY` — rebuilds index without blocking writes.

## Memory

### Heap Analysis

- **Heap snapshots**: Record the complete state of the JavaScript/Java heap at a point in time.
- **Shallow size**: Memory consumed by the object itself (header + fields).
- **Retained size**: Shallow size + size of all objects this object keeps alive (via references). This is what you care about for leak detection.
- **Dominator tree**: Shows which objects retain the most memory. Roots (GC roots) → dominators (unique owner) → dominated objects. Finding the dominator of a large retained set tells you the _root cause_ of a leak or high retention.

### Memory Leak Detection

**Patterns**:
1. **Global variables**: Accidentally storing data on `window` or a global singleton that never clears.
2. **Detached DOM**: Removing DOM nodes from the tree but keeping JavaScript references to them (e.g., stored in a cache or closure). The DOM tree stays alive because JS holds the reference.
3. **Closures**: Closures that capture large scopes. `function outer() { const hugeData = ...; return function inner() { /* uses hugeData */ } }` — the closure retains all captured variables as long as `inner` is referenced.
4. **Timers / Intervals**: `setInterval(() => { store(el.innerHTML) }, 1000)` — `el` is never released. Always clear timers.
5. **Event listeners**: Attaching listeners without removing them. `element.addEventListener('scroll', handler)` — if `element` is removed, `handler` keeps the element alive.

**Tools**:
- **Chrome DevTools**: Memory tab → Heap Snapshot (comparison view), Allocation Instrumentation (timeline of allocations), Allocation Sampling (low-overhead snapshots).
- **Node.js**: `--inspect` + Chrome DevTools, or programmatic heap snapshots with `v8.getHeapSnapshot()`.
- **Eclipse MAT (Java)**: Leak Suspects report, dominator tree, OQL (Object Query Language) for custom queries.
- **VisualVM (Java)**: Live heap monitoring, heap dump analysis, GC visualization.

### Garbage Collection Tuning

**GC Log Analysis**: Enable GC logging to understand pause times, frequency, and phases.

- **Java**: `-Xlog:gc*:file=gc.log` (JDK 9+). Key metrics: young GC pauses, full GC pauses, concurrent cycle phases.
- **Go**: `GODEBUG=gctrace=1` — prints GC timing, STW duration, and memory stats.
- **Node.js (V8)**: `--trace-gc` — see GC events, `--expose-gc` for manual triggering.

**Choosing a GC** (Java):
- **G1GC**: Default since JDK 9. Balances throughput and pause time. Tune with `-XX:MaxGCPauseMillis=200`. Good for most applications.
- **ZGC**: Sub-millisecond pauses (<1ms), concurrent. Scales to multi-TB heaps. Best for latency-sensitive applications. Available since JDK 11 (production-ready in JDK 15+).
- **Shenandoah**: Similar to ZGC (low-pause, concurrent). Available since JDK 12. Better throughput than ZGC at the cost of slightly higher CPU.
- **Parallel GC**: High throughput but long pauses. Good for batch processing, not interactive services.

## Concurrency & Async Patterns

### Thread Pool Sizing

- **CPU-bound tasks**: Pool size = number of cores (or cores + 1 for cache miss tolerance). More threads = context switching overhead with no throughput gain.
- **I/O-bound tasks**: `pool_size = cores × (1 + wait_time / service_time)`. If service_time = 10ms and wait_time (blocking) = 90ms: `cores × (1 + 9) = 10 × cores`. This is the "Little's Law" equivalent for thread pools.
- **Mixed workloads**: Use separate pools for CPU and I/O tasks, or use async I/O to avoid blocking pool threads entirely.

### Async I/O Patterns

- **Event loop model (Node.js)**: Single thread + non-blocking I/O. The event loop never blocks — all blocking operations (file I/O, DNS, crypto) are offloaded to a thread pool (`libuv`). Never use `fs.readFileSync` or synchronous DB calls in the hot path.
- **Reactor pattern (Netty, Java NIO)**: Event demultiplexer (Selector) dispatches I/O events to handlers. Scales to thousands of connections with few threads.
- **Virtual threads (Java 21+)**: Lightweight threads managed by the JVM. Pause on blocking I/O without pinning OS threads. "One thread per request" becomes practical at scale. Eliminates the need for reactive programming in most cases.
- **Async/await**: Syntactic sugar over promises/futures. Non-blocking but cooperative — long CPU-bound sections still block the calling thread.

### Race Condition Detection

- **ThreadSanitizer (TSan)**: Detects data races in C/C++ and Go. Compile with `-fsanitize=thread` (C++) or run `go build -race` (Go). Flags any access to shared memory without synchronization.
- **Go race detector**: `go run -race`, `go test -race`. Instruments all memory accesses. Catches unsynchronized reads/writes to the same variable from different goroutines.
- **Identifying shared mutable state**: If two goroutines/threads both read and write the same variable without a mutex, channel, or atomic — that's a data race. Fix: use channels (Go), locks, or immutable data structures.

## Profiling Methodology

### CPU Profiling

- **Sampling profilers**: Periodically interrupts the program and records the call stack. The frequency determines granularity (default: 99-1000 Hz). Lower overhead than instrumentation.
- **Flame graph interpretation**:
  - **x-axis**: Proportion of samples (width = time spent on-cpu).
  - **y-axis**: Call stack depth (root at bottom, leaves at top).
  - **Plateaus**: Wide top-edge functions — these are your hot functions consuming the most CPU.
  - **Towers**: Deep call stacks — may indicate over-abstracted code paths.
  - **Search**: Interactive flame graphs let you search for function names and highlight their footprint across all stacks.
- **Sampling vs instrumentation**: Sampling (pprof, perf) shows _where_ time is spent. Instrumentation (gprof, Java HPROF) adds probes to every function — higher overhead but gives exact call counts.

### Memory Profiling

- **Allocation profiling** (`pprof --alloc_space`, `async-profiler alloc`): Shows what code allocates the most memory — this is different from what _retains_ the most. High allocation rate causes GC pressure.
- **Heap profiling** (`pprof --inuse_space`, heap snapshots): Shows what is currently in the heap. Good for finding leaks.
- **The distinction**: A function that allocates 1GB per second but releases it immediately (high allocation rate, low heap-in-use) is a GC pressure problem. A function that holds 1MB that never gets freed (low allocation rate, high heap-in-use) is a memory leak.

### I/O Profiling

- **strace**: Trace system calls. Look for: excessive `read`/`write` syscalls (many small I/O operations), slow `open`/`stat` (cold file system cache), `epoll_wait` delays.
- **iostat**: Per-disk metrics. Key columns: `%util` (time disk is busy — >80% is saturated), `await` (average I/O latency per request — >10ms indicates problem), `r/s` + `w/s` (IOPS).
- **iotop**: Per-process I/O usage. Find which process is generating disk I/O.
- **Signs of trouble**: High `iowait` in `top` or `mpstat`, combined with high disk `await` in `iostat` — processes are stuck waiting for disk.

## Load Testing

### k6 Scripts

Use `k6 run script.js` with the `--out json` flag for detailed results.

**Ramp-up (Baseline)**:
```javascript
import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  stages: [
    { duration: '5m', target: 100 },   // ramp up to 100 users
    { duration: '10m', target: 100 },  // hold
    { duration: '5m', target: 0 },     // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<2000'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/endpoint');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```

**Soak (Endurance)** — detect memory leaks, connection leaks:
```javascript
export const options = {
  stages: [
    { duration: '10m', target: 50 },   // ramp to moderate load
    { duration: '8h', target: 50 },    // hold for 8 hours
    { duration: '5m', target: 0 },     // ramp down
  ],
};
```

**Spike (Burst)** — test auto-scaling and queue buffering:
```javascript
export const options = {
  stages: [
    { duration: '1m', target: 10 },    // baseline
    { duration: '10s', target: 500 },  // sudden spike to 500
    { duration: '5m', target: 500 },   // hold spike
    { duration: '5m', target: 10 },    // recover
  ],
};
```

**Stress (Breaking point)** — find where the system breaks:
```javascript
export const options = {
  stages: [
    { duration: '5m', target: 200 },
    { duration: '5m', target: 400 },
    { duration: '5m', target: 600 },
    { duration: '5m', target: 800 },
    { duration: '5m', target: 1000 },
  ],
};
```

### wrk2 — Constant-Throughput Latency Testing

wrk2 maintains a fixed request rate (unlike wrk's open-loop), making it ideal for correct latency-at-load measurements:

```bash
# 10,000 requests/sec for 60 seconds, 4 threads, 100 connections
wrk2 -t4 -c100 -d60s -R10000 --latency https://api.example.com/endpoint
```

Key difference from k6: wrk2 is L7 HTTP only, no scripting. Best for micro-benchmarks of a single endpoint.

### Artillery — YAML-Based Scenario Testing

```yaml
config:
  target: 'https://api.example.com'
  phases:
    - duration: 60
      arrivalRate: 5
      rampTo: 50
      name: 'Warm up'
    - duration: 600
      arrivalRate: 50
      name: 'Sustained load'
  defaults:
    headers:
      Authorization: 'Bearer {{ token }}'

scenarios:
  - name: 'User browsing flow'
    flow:
      - get:
          url: '/api/products'
          capture:
            - json: '$.products[0].id'
              as: 'productId'
      - think: 3
      - get:
          url: '/api/products/{{ productId }}'
      - post:
          url: '/api/cart'
          json:
            productId: '{{ productId }}'
            quantity: 1
```

Artillery excels at multi-step user flows and WebSocket testing.

### Infrastructure Sizing from Load Test Results

- **Correlating load to resources**: If 200 VUs produce 500 req/s at 60% CPU, then 400 VUs (1000 req/s) will need ~2x the instances or ~83% CPU.
- **Cost prediction**: (peak_req_per_sec / capacity_per_instance) × instance_cost × replica_for_redundancy = monthly compute cost at scale.
- **Headroom**: Design for 60-70% utilization at peak. Above 80%, response times degrade exponentially (queueing theory).
- **Bottleneck identification**: Instrument every hop. If CPU is at 30% but latency is high — it's not CPU, it's the DB/network/lock contention.

### Statistical Analysis of Results

- **Interpreting percentiles**: Flat curve up to P95 then a "knee" means a specific bottleneck activates at that load (e.g., GC kicks in, connection pool exhausts).
- **Identifying bottlenecks from data**: High P50 + low P50 = fast median but rare events are terrible (GC/lock contention). Low P50 + high P95 = queueing delay or resource saturation at peak. Growing P50 over time in soak = memory leak.
- **Comparing before/after**: Run exactly the same test (same tool, same parameters, same environment), compare percentiles at the same request rate.

## Performance Budgets

### Time Budgets

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | < 2.5s | 2.5s - 4.0s | > 4.0s |
| TBT | < 200ms | 200ms - 600ms | > 600ms |
| FID / INP | < 100ms / < 200ms | 100-300ms / 200-500ms | > 300ms / > 500ms |
| CLS | < 0.1 | 0.1 - 0.25 | > 0.25 |

### Size Budgets

| Resource | Budget (compressed) |
|----------|---------------------|
| JavaScript (critical path) | < 200KB |
| CSS (critical path) | < 50KB |
| Hero images (LCP) | < 500KB |
| Total page weight | < 1.5MB |

### Quantity Budgets

| Metric | Budget |
|--------|--------|
| HTTP requests per page | < 25 |
| DOM nodes | < 1500 |
| Render-blocking resources | < 5 |
| Third-party origins | < 5 |

### CI Enforcement

- **Lighthouse CI**: Run Lighthouse in CI, assert scores against budgets. Fail the PR build if thresholds are exceeded.
- **bundlesize**: Configure per-chunk size limits. Fail if a chunk exceeds its budget.
- **Custom checks**: `webpack-stats-plugin` + GitHub Action that compares bundle sizes against a baseline and posts a comment on the PR.
- **Perf budget notification**: Comment on PRs with before/after comparison tables for bundle size, LCP, and TBT.

## Optimization Methodology

### The Loop

```
Measure → Profile → Identify Bottleneck → Optimize → Verify → Repeat
```

1. **Measure**: Establish a baseline — what is the current latency/throughput/size?
2. **Profile**: Drill into _why_ — what function, query, or resource is the bottleneck?
3. **Identify bottleneck**: Pinpoint the single constraint limiting performance.
4. **Optimize**: Apply the targeted fix (not speculative optimization).
5. **Verify**: Run the same measurement again — did it improve? By how much? Did anything else degrade?
6. **Repeat**: The bottleneck usually moves to the next constraint.

### Amdahl's Law

`speedup = 1 / ((1 - P) + (P / S))` where P = proportion that can be improved, S = speedup factor.

If you can only optimize 50% of the execution time, the maximum speedup is 2x — even if you make that 50% infinitely fast. This means: **measure the proportion first**. Optimizing 80% of execution is worth 5x; optimizing 5% is never worth the effort.

### Pareto Principle (80/20 Rule)

80% of performance issues come from 20% of the code. Focus on the hot paths — the 20% that serves 80% of requests. Don't inline utility functions that run once per user session while pagination queries are doing sequential scans.

### Common Anti-Patterns

- **Premature optimization** (Knuth): "The real problem is that programmers have spent far too much time worrying about efficiency in the wrong places and at the wrong times."
- **Optimizing without measuring**: You don't know what's slow until you measure. Intuition is frequently wrong.
- **Optimizing the wrong thing**: Making a function 10x faster that runs 0.1% of the time saves nothing. Always optimize what matters to users — not what looks satisfying.
- **Vendor lock without profiling**: Adding Redis because "it's fast" when the bottleneck is a missing index on `users.email`. Layer in complexity only when needed.
- **Confusing micro-optimization with architecture**: Switch statement vs if-else doesn't matter when you're doing a sequential scan over 10M rows.

## Cross-Skill Coordination

Performance is not a solo activity — it requires instrumentation from developers, infrastructure from DevOps, data from DBAs, and prioritization from product. A performance engineer without coordination is optimizing in a vacuum.

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Backend Developers** | Code-level profiling, query optimization, memory leaks | Flame graph results, hot path identification, N+1 query locations, memory allocation profiles |
| **Frontend Developers** | Bundle size, rendering performance, Core Web Vitals | Lighthouse/WebPageTest results, bundle analysis, LCP/INP optimization targets |
| **DBA / Database Team** | Query optimization, indexing, connection pooling | Slow query logs, EXPLAIN plans, index recommendations, connection pool sizing |
| **DevOps / Infrastructure** | CDN, caching layers, auto-scaling, resource allocation | Cache hit rates, CDN configuration, instance right-sizing, scaling trigger tuning |
| **System Architect** | Caching strategy, async processing, architecture bottlenecks | System bottleneck analysis, sync-to-async migration, caching architecture |
| **QA Engineer** | Load testing, stress testing, performance regression testing | k6/JMeter test scripts, baseline metrics, regression thresholds |
| **Security Reviewer** | Performance impact of security controls, WAF latency | WAF overhead, TLS termination cost, security scanning performance impact |
| **Product Strategist** | Performance vs feature prioritization, user-perceived latency | Performance impact on conversion/retention, business case for optimization investment |
| **Project Manager** | Performance work prioritization, optimization sprints | Performance debt backlog, optimization ROI estimates, engineering capacity |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| P99 latency increases >2x baseline in production | Backend Developers, DevOps, Project Manager | Degraded user experience; investigation may block release |
| Database CPU sustained >80% for >15 minutes | DBA, Backend Developers, DevOps | Imminent database overload; query optimization or scaling needed |
| Memory leak detected in production (heap growth without plateau) | Backend Developers, DevOps | OOM crash risk; restart mitigation + root cause fix |
| Load test reveals system breaks at <2x current peak traffic | System Architect, DevOps, Project Manager | Capacity risk; scaling or optimization before next growth phase |
| Cache hit rate drops below 70% | DevOps, Backend Developers | Cache strategy failing; increased database load imminent |
| Core Web Vitals score drops below "Good" threshold (LCP>2.5s, INP>200ms) | Frontend Developers, Product Strategist | SEO impact (Google ranking factor); user experience degradation |
| Bundle size increases >20% in single deploy | Frontend Developers | Progressive bloat; bundle split or lazy loading needed |
| N+1 query pattern discovered in critical user path | Backend Developers | Easy optimization win; batch loading or eager loading fix |

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| Performance degradation causing revenue loss (checkout/payment path affected) | **CTO Advisor** + VP Engineering + Product Strategist | Revenue at risk; SEV-level incident response |
| Production outage caused by resource exhaustion (CPU/memory/connections) | **DevOps Lead** + CTO Advisor + Incident Commander | Production incident; immediate scaling or restart |
| Performance optimization blocked by product for >2 sprints (P99 >1s on critical path) | **CTO Advisor** + Product Strategist | Technical debt vs feature decision; executive trade-off |
| Architecture bottleneck requiring major refactor to resolve | **System Architect** + CTO Advisor | Multi-sprint investment; architecture decision required |
| Infrastructure cost from performance-inefficient architecture >30% of cloud bill | **CTO Advisor** + CFO/Finance | Cost optimization business case; infrastructure re-architecture |

## Production Checklist

- [ ] Performance baselines established: P50/P95/P99 latency, throughput, error rate per critical endpoint
- [ ] Profiling completed (CPU + memory + I/O) on production-similar staging; top 5 bottlenecks documented
- [ ] Load test suite built (k6/wrk2/Artillery) covering: baseline, load, stress, soak, spike scenarios
- [ ] Load test results: capacity ceiling, breaking point, scaling behavior
- [ ] Database slow queries (EXPLAIN ANALYZE) identified; missing indexes added; N+1 queries eliminated
- [ ] Connection pooling configured and tuned for database and external services
- [ ] Read replica routing implemented with replication lag monitoring
- [ ] Core Web Vitals measured via RUM; LCP < 2.5s, INP < 200ms, CLS < 0.1
- [ ] Bundle analyzed and optimized (code splitting, tree shaking, image/font optimization)
- [ ] Performance budgets defined and enforced in CI
- [ ] Automated load testing runs in CI on PRs; regressions caught before merge
- [ ] Multi-layer caching strategy: browser (Cache-Control), CDN (stale-while-revalidate), application (Redis), DB buffer pool
- [ ] CDN configuration optimized: cache hit ratio > 80%, TTLs appropriate, edge functions efficient
- [ ] SLOs defined with burn-rate alerts; APM and RUM dashboards operational
- [ ] Async/non-blocking I/O used for all external calls; timeouts set on every downstream call
- [ ] Memory leak detection automated — heap snapshots running in staging, trend monitored
- [ ] GC logs active and reviewed for pause time anomalies
- [ ] Race condition detection enabled in tests (Go -race, ThreadSanitizer)

## MVP vs Growth vs Scale

| Phase | Team Size | Priority | Performance Approach |
|-------|-----------|----------|---------------------|
| **MVP (0→1)** | 1-3 devs | It works. End of story. | No profiling, no load testing, no caching layers. If page loads in <3 seconds, ship. Use server logs for rough latency. Add a database index if a query is visibly slow. That's it. |
| **Growth (1→10)** | 3-15 devs, 1 backend specialist | Fix what's slow for real users | APM (Datadog free tier or New Relic). Profile top 5 slowest endpoints. Add Redis cache for hot queries. Run a baseline load test before major launches. CI performance budgets for frontend. |
| **Scale (10→N)** | 15+ devs, dedicated performance/infra team | Performance as feature | Full observability (tracing + profiling + RUM). Automated load testing in CI (k6). SLOs with burn-rate alerts. Multi-layer caching. CDN optimization. Database read replicas + query optimization. |

**MVP rule:** Premature optimization is still the root of all evil. The #1 performance problem in MVP is NOT your database query — it's that you don't have product-market fit. Ship. If something is slow enough that users complain, fix it in 1 hour with an index or cache. Move on.

## Cost-Effective Decision Table

| Decision | Free/Cheap Option | Paid Upgrade | When to Upgrade |
|----------|------------------|--------------|-----------------|
| APM / monitoring | Datadog free tier (1-day retention) or Signoz (self-hosted OSS) | Datadog APM ($31/host/mo) or New Relic ($0.30/GB) | Need >1-day retention, custom dashboards, or alerting |
| Profiling | `pprof` (Go), `py-spy` (Python), Chrome DevTools (JS) — all free | Datadog Continuous Profiler ($12/host/mo) | Need always-on profiling across all hosts, not ad-hoc |
| Load testing | k6 (free OSS) or Artillery (free OSS) | k6 Cloud ($50/mo) or Gatling Enterprise | Need managed test execution, geo-distributed load generation, or >100K VUs |
| Caching | Redis (self-hosted on app server, free) | Redis Cloud ($25/mo) or Elasticache | Need HA, managed failover, or >1GB datasets |
| CDN | CloudFlare free / Fastly free tier (up to $50 credit) | CloudFlare Pro ($20/mo) or Fastly | Need WAF, image optimization, or custom edge logic |
| Database optimization | EXPLAIN ANALYZE (free) + manual tuning | pganalyze ($99/mo) or SolarWinds DPA ($2K+) | >10 database instances or need automated index recommendations |
| Frontend performance | Lighthouse (free) + webpack-bundle-analyzer (free) | Calibre ($80/mo) or DebugBear ($49/mo) | Need per-page monitoring, CI integration, or trend alerts |

**Annual performance tool budget by phase:** MVP: $0. Growth: $0-5K. Scale: $10K-100K.

## Scalability Decision Tree

```
Is P95 latency >500ms for ANY user-facing endpoint?
├── YES → Profile that endpoint. Fix the #1 bottleneck. Re-measure. Don't profile 50 endpoints at once.
└── NO → You're fine. Ship features.

Is database CPU >70% sustained (not spikes)?
├── YES → Check: missing indexes? N+1 queries? Inefficient queries? Fix queries first.
│   If query-optimized and still high → Add read replica. If still high → Consider caching.
└── NO → DB is healthy.

Do you have a cache layer (Redis/Memcached)?
├── YES → What's the cache hit rate?
│   ├── <50% → You're adding latency for no benefit. Remove or reconfigure.
│   ├── 50-80% → Decent. Check if eviction policy or TTLs can be improved.
│   └── >80% → Healthy cache.
└── NO → Do you have a specific query/page that's slow and read-heavy?
    ├── YES → Add caching for that specific use case. Don't add a cluster-wide cache.
    └── NO → You don't need caching yet.

Is frontend bundle >200KB (compressed) for critical path?
├── YES → Run bundle analyzer. Split vendor chunk. Tree-shake. Lazy-load below-fold.
└── NO → Bundle size is healthy. Ship features.

Are you running load tests before major launches?
├── YES → Good. Do they catch regressions? Test results compared to baseline?
└── NO → Add a 30-minute load test to your pre-launch checklist. k6 script, 5-minute run.
```

## When NOT to Use This Skill (Overkill)

- **Pre-launch MVP with <100 users**: Profiling, load testing, caching layers, CDN optimization for a product nobody uses yet is waste. Add an index if a page takes >3 seconds. Move on.
- **Internal tool used by 5 people**: P95 latency optimization for a dashboard used by your team of 5 is not worth engineering time. If a page takes 5 seconds, they can wait 5 seconds.
- **Your performance is fine (all endpoints P95 <200ms, LCP <2s)**: Don't optimize for optimization's sake. Set baselines. Monitor. Only act when metrics degrade.
- **You can scale vertically (bigger server solves the problem)**: Before building a Redis cluster and read replicas, try upgrading to the next EC2 instance size. It costs $50 more per month and takes 5 minutes. Do that first.
- **The slow thing is used by 3 customers who haven't complained**: Fix problems that affect many users or critical paths. A slow admin report used monthly is not a priority.

## Token-Efficient Workflow

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

## References

- [Google — The Site Reliability Workbook](https://sre.google/workbook/slo-document/)
- [Brendan Gregg — Linux Performance](https://www.brendangregg.com/linuxperf.html)
- [k6 — Load Testing](https://k6.io/docs/)
- [Clinic.js — Node.js Performance Profiling](https://clinicjs.org/)
- [Async-profiler — Low-Overhead Java Profiler](https://github.com/async-profiler/async-profiler)
- [web.dev — Web Performance](https://web.dev/learn-core-web-vitals/)
- [Lighthouse CI — Performance Budgets](https://github.com/GoogleChrome/lighthouse-ci)
- [Use The Index, Luke! — SQL Indexing](https://use-the-index-luke.com/)
- [Redis — Caching Patterns](https://redis.io/docs/manual/patterns/)
- [pprof — Go Profiling](https://go.dev/blog/pprof)
- [py-spy — Python Sampling Profiler](https://github.com/benfred/py-spy)
