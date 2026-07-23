# Memory

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
