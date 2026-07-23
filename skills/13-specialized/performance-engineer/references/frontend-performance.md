# Frontend Performance

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
