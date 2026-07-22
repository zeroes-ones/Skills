# Frontend Performance Cookbook

Practical recipes and deep dives for optimizing frontend performance — from the critical rendering path to JavaScript execution, images, fonts, and beyond.

---

## Critical Rendering Path

### Step-by-Step

The browser converts HTML/CSS/JS to pixels in these sequential steps:

```
1. HTML → DOM (Document Object Model)
2. CSS → CSSOM (CSS Object Model)
3. DOM + CSSOM → Render Tree (visible nodes only)
4. Render Tree → Layout (box model: position, size)
5. Layout → Paint (pixel filling)
6. Paint → Composite (layer compositing, GPU-accelerated)
```

### Optimization Per Step

| Step | Optimization |
|------|-------------|
| **DOM** | Minimize HTML size, server-side render, stream HTML |
| **CSSOM** | Inline critical CSS in `<head>`, defer non-critical CSS (`<link rel="preload" as="style" onload="this.rel='stylesheet'">`) |
| **Render Tree** | Reduce DOM depth, avoid `display: none` misuse |
| **Layout** | Avoid layout thrashing (batch DOM reads then writes), use `will-change` sparingly |
| **Paint** | Use `transform` and `opacity` for animations — compositor-only |
| **Composite** | Promote elements to their own layer (`will-change: transform`, `contain: layout style paint`) |

### Avoiding Layout Thrashing

Layout thrashing happens when you read a layout property (e.g., `element.offsetHeight`) then write a DOM change, forcing the browser to recalculate layout before resolving the read.

**Bad** (read/write interleaving):
```javascript
// Read → Write → Read → Write (4 layout recalculations)
const h1 = el1.offsetHeight;
el2.style.height = h1 + 'px';
const h2 = el3.offsetHeight;
el4.style.height = h2 + 'px';
```

**Good** (batch reads, then writes):
```javascript
// Batch reads
const h1 = el1.offsetHeight;
const h2 = el3.offsetHeight;
// Batch writes
el2.style.height = h1 + 'px';
el4.style.height = h2 + 'px';
```

Use `fastdom` library to automate read/write batching if the pattern is widespread.

---

## Core Web Vitals Deep Dive

### LCP (Largest Contentful Paint) — Target: < 2.5s

**What it measures**: The render time of the largest image or text block visible within the viewport.

**Sub-parts breakdown**:

```
TTFB → Resource Load Delay → Resource Load Time → Element Render Delay
 ├──── Time to 1st byte ────┤
 │     (server + CDN +      │
 │      network latency)     │
 ├──── When browser knows ───┤
 │      it needs the LCP     │
 │      resource              │
 ├──── Download time ────────┤
 │      (image/font/HTML)    │
 └──── Render time ──────────┘
                            └──→ LCP
```

**Optimization per sub-part**:

| Sub-part | Optimization |
|----------|-------------|
| **TTFB** | Server-side rendering, CDN caching, faster backend logic, edge computing |
| **Resource Load Delay** | `<link rel="preload">` the LCP resource, eliminate render-blocking resources before LCP |
| **Resource Load Time** | Optimize image (compress, serve WebP/AVIF), use responsive images, use `fetchpriority="high"` |
| **Element Render Delay** | Inline critical CSS, avoid complex CSS selectors on LCP element |

**Common mistakes**:
- Not preloading the LCP image (letting the browser discover it through CSS or late-rendered HTML)
- Lazy-loading the LCP image (it's above-the-fold — should load immediately)
- Using `loading="lazy"` on a hero image
- Server-side rendering that blocks TTFB with slow API calls

### INP (Interaction to Next Paint) — Target: < 200ms

**What it replaces**: FID (First Input Delay). INP measures the longest interaction latency across the entire page visit, not just the first one.

**How interaction latency is measured**:
```
User taps/clicks/types
       │
       ▼
Input delay (browser processing the event)
       │
       ▼
Event handler execution (JavaScript runs)
       │
       ▼
Next paint (browser renders the result)
       │
       ▼
INP = total duration from input → next paint
```

**Optimization**:

1. **Break up long tasks**: Any task > 50ms delays the next interaction. Use `setTimeout()` to defer non-critical work, or `scheduler.yield()` (Chrome 115+).
   ```javascript
   // Instead of:
   processLargeArray(items);  // blocks for 200ms

   // Do:
   for (const item of items) {
     processItem(item);
     if (performance.now() % 50 < 5) {
       await new Promise(r => setTimeout(r, 0));
     }
   }
   ```

2. **Reduce JS execution time**: Shorter callbacks, avoid complex computations in event handlers.
   - Use `requestAnimationFrame` for visual updates
   - Use passive event listeners for scroll/touch: `element.addEventListener('scroll', handler, { passive: true })`

3. **Optimize event callbacks**: Debounce/throttle as appropriate. Avoid triggering layout in event handlers (reading `offsetHeight` in a scroll handler causes layout recalculation).

4. **Prefer `content-visibility: auto`**: Defers rendering of off-screen elements, reducing input lag on visible content.

5. **Avoid pointer lockup**: Render-blocking state updates in event handlers. Use `isInputPending()` to defer non-urgent work.

### CLS (Cumulative Layout Shift) — Target: < 0.1

**What causes layout shifts**:

| Cause | Fix |
|-------|-----|
| Images without dimensions | Always set `width` and `height` attributes, or use CSS `aspect-ratio` |
| Ads/videos/embeds without reserved space | Reserve a container with explicit size, use placeholder |
| Web fonts causing FOIT/FOUT | Use `font-display: optional` or `swap` with preload |
| Dynamic content injected above existing content | Insert below existing content or reserve space above |
| Late-loading third-party widgets | Load in a positioned container with fixed dimensions |

**Measurement**: Layout Shift Score = `impact_fraction × distance_fraction`. A score of 0.1 means the viewport shifted by 10% of its area.

**Fixing images** (the most common CLS culprit):
```html
<!-- ✅ Always set dimensions -->
<img src="photo.jpg" width="800" height="600" alt="...">

<!-- ✅ Or use aspect-ratio CSS -->
<img src="photo.jpg" style="aspect-ratio: 800/600" alt="...">
```

**Fixed-sizing for dynamic content**:
```css
.ad-container {
  width: 300px;
  height: 250px;  /* reserve exact space */
  background: #eee; /* show placeholder */
}
```

**Avoid inserting above existing content**: If you must show a banner, inline it before page render, or reserve space and populate after render.

---

## Image Optimization Pipeline

### Format Selection (by preference)

| Format | Compression | Browser Support | Use Case |
|--------|-------------|----------------|----------|
| **AVIF** | Best (~50% smaller than WebP) | Chrome, Firefox, Safari 16.4+ | Photos with transparency, high-detail images |
| **WebP** | Very good (~30% smaller than JPEG) | All modern browsers | Default — wide support, good quality |
| **JPEG XL** | Competitive with AVIF | Chrome (experimental), Safari 17+ | Emerging — best quality/size ratio |
| **JPEG** | Good | Universal | Fallback for older browsers, photographs |
| **PNG** | Lossless | Universal | Graphics with transparency, screenshots |
| **SVG** | Vector | Universal | Icons, logos, illustrations (scales infinitely) |

**Delivery strategy**: `<picture>` element with AVIF → WebP → JPEG/PNG fallback:

```html
<picture>
  <source srcset="photo.avif" type="image/avif">
  <source srcset="photo.webp" type="image/webp">
  <img src="photo.jpg" alt="..." width="1200" height="800" loading="lazy">
</picture>
```

### Responsive Images

**Use `srcset` and `sizes` to serve the right resolution for the user's viewport**:

```html
<img
  srcset="photo-320.jpg 320w,
          photo-640.jpg 640w,
          photo-1280.jpg 1280w,
          photo-1920.jpg 1920w"
  sizes="(max-width: 600px) 100vw,
         (max-width: 1200px) 50vw,
         33vw"
  src="photo-1920.jpg"
  alt="..."
  width="1920" height="1080"
>
```

- `srcset` **width descriptors** (`320w`, `640w`, etc.): Tell the browser the _actual width_ of each image version.
- `sizes` attribute: Tells the browser _how much of the viewport_ the image will occupy at different breakpoints.
- The browser picks the best match based on device pixel ratio (DPR) and current viewport width.

**`srcset` with density descriptors** (simpler, for fixed-size images):
```html
<img src="photo@1x.jpg" srcset="photo@2x.jpg 2x, photo@3x.jpg 3x" alt="...">
```

### Lazy Loading

**Native lazy loading** (simplest — works in all modern browsers):
```html
<img src="photo.jpg" loading="lazy" alt="...">
<iframe src="widget.html" loading="lazy"></iframe>
```

- `loading="lazy"`: Defer loading until the element approaches the viewport (typically ~1250px before).
- `loading="eager"`: Load immediately (default for above-the-fold content).
- **Never** use `loading="lazy"` on the LCP element — it will delay the LCP time.

**Intersection Observer** (for custom control):
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      observer.unobserve(img);
    }
  });
}, { rootMargin: '200px' });

document.querySelectorAll('img[data-src]').forEach(img => observer.observe(img));
```

### Placeholders

| Type | What It Is | How To |
|------|-----------|--------|
| **Dominant color** | Single background color matching image | Extract via sharp: `sharp(image).resize(1).toBuffer()` → set as `background-color` |
| **LQIP** (Low Quality Image Placeholder) | Tiny blurred version (e.g., 20px wide) | Generate via sharp, base64 encode, inline in CSS `background-image` |
| **Blur-up** | LQIP that sharpens as full image loads | Show LQIP blurred initially, crossfade to full image on load |
| **Solid color** | Simplest — neutral gray or average color | For purely decorative images where UX impact is minimal |

**LQIP generation with sharp**:
```javascript
const sharp = require('sharp');
const lqip = await sharp('photo.jpg')
  .resize(20)
  .blur()
  .jpeg({ quality: 30 })
  .toBuffer();
// base64 encode and inline
const base64 = `data:image/jpeg;base64,${lqip.toString('base64')}`;
```

### Tooling

| Tool | Purpose | Command |
|------|---------|---------|
| **sharp** | Node.js image processing (resize, format convert, LQIP) | `npm install sharp` |
| **imagemin** | Build-time image compression | `npm install imagemin` |
| **Squoosh** | Web-based image optimizer (CLI available) | `npx @squoosh/cli photo.jpg --webp '{"quality": 75}'` |
| **next/image** | Next.js automatic optimization | Built into Next.js — serves WebP/AVIF by default, responsive sizes |
| **Cloudinary / Imgix** | Image CDNs — transform on the fly | `https://res.cloudinary.com/demo/image/upload/w_400,q_auto,f_auto/photo.jpg` |

---

## Font Loading Strategies

### font-display Rules

```css
@font-face {
  font-family: 'Inter';
  src: url('Inter.woff2') format('woff2');
  font-display: swap;    /* <-- controls loading behavior */
}
```

| Value | Behavior | Best For |
|-------|----------|----------|
| **`swap`** | Show fallback immediately, swap when font loads | Content text where brand font matters. Risk: FOIT avoided, FOUT (flash of unstyled text) occurs. |
| **`optional`** | Show fallback, keep it if font loads within ~100ms | Performance-critical text. Users on fast connections get the font; slow connections see fallback permanently. Zero flicker. |
| **`block`** | Invisible until font loads (long timeout) | Hero headings, logos — visible text is worse than invisible. Risk: long blank text. |
| **`fallback`** | Brief invisible (~100ms), then fallback, swap if font loads within ~3s | Compromise — short FOIT, then swap if loaded. |

**Recommendation**: Use `swap` for body text (content priority), `optional` for UI elements (stability priority).

### Subsetting

Most fonts include glyphs for many languages/locales you don't need. Subsetting removes them:

```bash
# With glyphhanger (HTTP-based subsetting)
glyphhanger https://example.com --subset=*.woff2

# With pyftsubset (manual)
pyftsubset Inter-Regular.woff2 --unicodes="U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC"
```

Subsetting typically reduces font file size by 70-90%.

### Preloading

```html
<!-- Preload the critical font — discovers it early -->
<link rel="preload" as="font" href="/fonts/Inter-Reginal.woff2" crossorigin>

<!-- Note: `crossorigin` is REQUIRED for fonts, even same-origin fonts using CDN -->
```

Without preload, the browser discovers the font in CSS, which is loaded after HTML parsing. The font request starts late — preload moves it to the beginning of the critical path.

### Self-Hosting

**Avoid Google Fonts CDN** for production performance:
- Extra DNS lookup (fonts.googleapis.com + fonts.gstatic.com)
- Separate origin — SSL negotiation, connection warmup
- Multiple redirects (font URL rotates)

**Self-host with subset fonts instead**:
```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-Regular-subset.woff2') format('woff2');
  font-display: swap;
}
```

Faster by 200-500ms on first load, no external origin overhead.

### Font Loading Checklist

- [ ] Fonts self-hosted (no Google Fonts CDN)
- [ ] Subsetted to required characters only
- [ ] `font-display: swap` or `optional` set
- [ ] Preloaded with `<link rel="preload" as="font" crossorigin>`
- [ ] WOFF2 format (modern, best compression)
- [ ] Variable font if multiple weights needed (single file, smaller total)

---

## JavaScript Performance

### Bundle Splitting

**Strategy**: Split the single JS bundle into multiple chunks that can be loaded independently:

| Chunk Type | Contains | Why |
|------------|----------|-----|
| **Vendor** | React, lodash, moment, etc. | Rarely changes → long cache lifetime |
| **Common** | Shared modules between pages | Cached once, used everywhere |
| **Page chunks** | Route-specific code | Load only what the current page needs |

**Manual split (webpack)**:
```javascript
// webpack.config.js
module.exports = {
  optimization: {
    splitChunks: {
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendor',
          chunks: 'all',
        },
        common: {
          minChunks: 2,
          name: 'common',
          chunks: 'all',
        },
      },
    },
  },
};
```

**Automatic (Next.js)**:
Next.js automatically splits per-page — each page in `pages/` or `app/` gets its own chunk.

### Tree Shaking

Dead-code elimination relies on ES module static analysis:

- **Use ES imports**: `import { debounce } from 'lodash-es'` — tree-shakeable.
- **Avoid CommonJS**: `const { debounce } = require('lodash')` — NOT tree-shakeable (dynamic requires).
- **Set `sideEffects: false`** in `package.json`: Tells webpack/Rollup it's safe to remove unused exports.
- **Avoid barrel imports**: `import { Button, Card, Modal } from './components'` (re-exports everything). Import directly instead: `import { Button } from './components/Button'`.

**Checking tree-shaking**: Use `webpack-bundle-analyzer` or `rollup-plugin-visualizer` to see if unused modules are included.

### Dynamic Imports

Load code on-demand — not at initial page load:

```javascript
// React: lazy load component
const HeavyChart = React.lazy(() => import('./HeavyChart'));

// Vanilla: load on scroll
element.addEventListener('mouseenter', async () => {
  const { Tooltip } = await import('./Tooltip');
  showTooltip(Tooltip);
});

// Load after page is idle
window.addEventListener('load', () => {
  requestIdleCallback(async () => {
    const { PrefetchData } = await import('./prefetch');
    PrefetchData.init();
  });
});
```

**Ideal candidates for dynamic imports**:
- Heavy components below the fold
- Modals, dropdowns, tooltips (not visible on load)
- Charts, maps, rich text editors
- Admin panels only visible to admins
- "Load more" paginated content

### Execution Cost

**Long tasks**: Any JavaScript execution over 50ms blocks the main thread.

| Duration | UX Impact | Action |
|----------|-----------|--------|
| < 50ms | Imperceptible | OK |
| 50-100ms | Slight delay, user may notice | Break up or defer |
| 100-300ms | Noticeable lag | Must break up — use `setTimeout` or `scheduler.yield()` |
| > 300ms | Users perceive broken site | Critical — refactor to offload or defer |

**requestIdleCallback**: Schedule non-urgent work for when the browser is idle:
```javascript
requestIdleCallback(() => {
  // Non-critical work: analytics, logging, deferred rendering
  logPerformanceMetrics();
}, { timeout: 2000 });
```

**Debounce/Throttle**:

| Event | Strategy | Example |
|-------|----------|---------|
| Scroll | Throttle (once per frame) | `lodash.throttle(callback, 16)` |
| Resize | Debounce (wait for pause) | `lodash.debounce(callback, 150)` |
| Keypress | Debounce (wait for pause) | `lodash.debounce(search, 300)` |
| Mouse move | Throttle (once per 50ms) | `lodash.throttle(callback, 50)` |

### Web Workers

Offload CPU-heavy computation to a separate thread:

```javascript
// main.js
const worker = new Worker('worker.js');
worker.postMessage({ data: largeArray });
worker.onmessage = (event) => {
  console.log('Result:', event.data);
};

// worker.js
self.onmessage = (event) => {
  const result = expensiveComputation(event.data);
  self.postMessage(result);
};
```

**Good candidates for Web Workers**:
- Image processing (resize, filter, format conversion)
- Data processing (JSON parse of large payloads, data transformation)
- Cryptography (hashing, encryption)
- Compression/decompression
- Code validation (syntax linting in browser IDE)

**Not good candidates**: DOM access (Workers can't touch the DOM), short operations (overhead of message passing > execution time).

---

## Performance Checklist

### Runtime (Every Page)

- [ ] LCP < 2.5s — preload LCP image, optimize TTFB, critical CSS inlined
- [ ] INP < 200ms — no long tasks blocking interactions, passive event listeners
- [ ] CLS < 0.1 — all images/videos have dimensions, no content injected above fold
- [ ] No render-blocking resources in the critical path
- [ ] JavaScript `defer` or `async` applied
- [ ] Lazy loading on all below-fold images (native `loading="lazy"`)

### Build/Bundling

- [ ] Bundle analyzed (webpack-bundle-analyzer) — no dead code, no duplicate libraries
- [ ] Code splitting implemented — per-route or per-component
- [ ] Tree shaking enabled (`sideEffects: false`, ES modules)
- [ ] Images optimized (WebP/AVIF, responsive srcset, compression)
- [ ] Fonts subsetted, self-hosted, preloaded with `crossorigin`

### CI/Monitoring

- [ ] Lighthouse CI running with performance budget assertions
- [ ] Bundle size budget enforced (< 200KB JS, < 50KB CSS compressed)
- [ ] RUM (Real User Monitoring) collecting CrUX / Web Vitals data
- [ ] Performance regression alerts configured (LCP > 2.5s, CLS > 0.1)

---

## References

- [web.dev — Learn Performance](https://web.dev/learn-core-web-vitals/)
- [web.dev — Optimize LCP](https://web.dev/optimize-lcp/)
- [web.dev — Optimize INP](https://web.dev/optimize-inp/)
- [web.dev — Optimize CLS](https://web.dev/optimize-cls/)
- [webpack-bundle-analyzer](https://github.com/webpack-contrib/webpack-bundle-analyzer)
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
- [Sharp — High-Performance Image Processing](https://sharp.pixelplumbing.com/)
- [MDN — Performance Guide](https://developer.mozilla.org/en-US/docs/Learn/Performance)
