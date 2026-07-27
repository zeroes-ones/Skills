# /webperf — Audit web application performance

Measure Core Web Vitals (LCP, INP, CLS), analyze bundle size, evaluate network efficiency, and identify rendering bottlenecks. Uses `web-perf-auditor` persona.

**When to use**: Before launch, after performance regressions, or during optimization sprints.

**Workflow**:
1. Invoke `web-perf-auditor` persona with `performance-engineer` skill
2. Measure Core Web Vitals: LCP < 2.5s, INP < 200ms, CLS < 0.1
3. Analyze: bundle size, code splitting, image optimization, font loading, render-blocking
4. Server-side: query performance, API latency, caching effectiveness
5. Output: Performance audit with quantified impact, prioritized fixes

**What it produces**: A performance report with current metrics vs targets, root causes, and fix recommendations ordered by user impact.
