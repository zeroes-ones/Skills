# Bundle Optimization Guide

> **Author:** Sandeep Kumar Penchala

Production-grade bundle optimization strategies covering analysis, splitting, tree shaking, asset optimization, and dependency auditing. These techniques directly support the frontend-developer skill's performance and deployment readiness phases.

## Bundle Analysis

### webpack-bundle-analyzer

Visualize what's in your bundle — sizes, composition, and duplicate dependencies.

```bash
# Install
npm install -D webpack-bundle-analyzer

# webpack.config.js
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
module.exports = {
  plugins: [new BundleAnalyzerPlugin({ analyzerMode: 'static', reportFilename: 'bundle-report.html' })],
};
```

### source-map-explorer

Works with any bundler (webpack, Vite, Rollup) — analyzes source maps to show code by file origin.

```bash
npm install -D source-map-explorer
# Add to package.json:
"scripts": { "analyze": "source-map-explorer 'dist/assets/*.js'" }
```

### Vite Bundle Visualizer

```bash
npm install -D rollup-plugin-visualizer
```

```typescript
// vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer';
export default defineConfig({
  plugins: [visualizer({ open: true, gzipSize: true, brotliSize: true })],
});
```

## Code Splitting

### Route-Based Splitting

Each route becomes its own chunk — users download only the code for pages they visit.

```tsx
// React Router v6
const Home = lazy(() => import('./pages/Home'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Reports = lazy(() => import('./pages/Reports'));

<Routes>
  <Route path="/" element={<Home />} />
  <Route path="/dashboard/*" element={<Dashboard />} />
  <Route path="/reports" element={<Reports />} />
</Routes>
```

### Component-Based Splitting

Split heavy, infrequently-used components:

```tsx
const PDFViewer = lazy(() => import('./components/PDFViewer'));
const VideoPlayer = lazy(() => import('./components/VideoPlayer'));

// With preload on hover
<button onMouseEnter={() => import('./components/HeavyEditor')}>Open Editor</button>
```

### Dynamic Import Patterns

```typescript
// Conditional feature loading
if (user.hasFeature('advanced-analytics')) {
  const { AdvancedDashboard } = await import('./advanced-dashboard');
}

// Named exports with magic comments (webpack)
const { Chart } = await import(/* webpackChunkName: "charts" */ './charts');

// Vite glob import for i18n
const messages = import.meta.glob('./locales/*.json');
```

### Splitting Thresholds

| Bundle Size | Action |
|-------------|--------|
| < 50 KB (gzipped) | No action needed |
| 50-100 KB (gzipped) | Consider splitting if not on critical path |
| 100-200 KB (gzipped) | Split; defer non-critical parts |
| > 200 KB (gzipped) | Immediate split required; audit dependencies |

## Tree Shaking

Tree shaking eliminates dead code. It requires ESM syntax — `import`/`export`, not `require`/`module.exports`.

### Ensuring Tree Shaking Works

```jsonc
// package.json — tell bundlers this package has no side effects
{ "sideEffects": false }
// Or be specific:
{ "sideEffects": ["*.css", "*.scss", "./src/polyfills.ts"] }
```

```typescript
// BAD — imports entire library
import _ from 'lodash';
_.debounce(fn, 300);

// GOOD — imports only what's needed
import debounce from 'lodash/debounce';
debounce(fn, 300);

// BEST — use tree-shakeable alternatives
import { debounce } from 'lodash-es';
```

### Common Tree Shaking Pitfalls

| Pitfall | Why It Breaks | Fix |
|---------|--------------|-----|
| `import * as X` | Imports entire namespace | Named imports |
| Dynamic property access | Bundler can't statically analyze | Static access only |
| Side-effectful barrel files | `export * from` pulls everything | Direct imports or `sideEffects` config |
| CommonJS interop | `require()` can't be tree-shaken | Use ESM packages only |

## Asset Optimization

### Image Format Comparison

| Format | Lossy | Transparency | Animation | Browser Support | Best For |
|--------|-------|-------------|-----------|----------------|----------|
| WebP | Yes | Yes | Yes | 97% | General replacement for JPEG/PNG |
| AVIF | Yes | Yes | Yes | 93% | Smallest file size, HDR support |
| PNG | No | Yes | No | 100% | Logos, screenshots requiring pixel-perfect |
| SVG | N/A | Yes | Yes | 100% | Icons, illustrations, logos |

### Responsive Images

```html
<picture>
  <source srcset="/hero.avif" type="image/avif" />
  <source srcset="/hero.webp" type="image/webp" />
  <img src="/hero.jpg" alt="Hero" loading="lazy" width="1200" height="600" />
</picture>

<!-- srcset for resolution switching -->
<img
  src="/photo-800.jpg"
  srcset="/photo-400.jpg 400w, /photo-800.jpg 800w, /photo-1200.jpg 1200w"
  sizes="(max-width: 600px) 100vw, 50vw"
  loading="lazy"
  alt="Photo"
/>
```

### Image Build Pipeline

```bash
# Sharp CLI for build-time image conversion
npm install -D sharp-cli
sharp -i ./src/images/*.jpg -o ./public/images/ --format webp --quality 80
sharp -i ./src/images/*.jpg -o ./public/images/ --format avif --quality 65
```

## Dependency Auditing

### depcheck — Find Unused Dependencies

```bash
npx depcheck
# Output: Unused dependencies: lodash, moment
#         Unused devDependencies: eslint-plugin-old
#         Missing dependencies: zod
```

### bundlephobia — Check Cost Before Adding

```bash
# CLI check
npx bundlephobia lodash
# Size: 69.4 KB minified, 24.3 KB min+gz
# Composition: ...
```

### import Cost (VS Code Extension)

Install "Import Cost" extension — shows size inline next to each import statement.

### Dependency Health Checklist

```bash
# Find heavy dependencies
npx cost-of-modules

# Check for duplicates with different versions
npx npm-dedupe --dry-run

# Find outdated packages
npm outdated --long
```

### Common Size Offenders & Alternatives

| Heavy Package | Size (min+gz) | Lighter Alternative | Size (min+gz) |
|---------------|---------------|-------------------|----------------|
| moment | 72 KB | date-fns / dayjs | 8 KB / 2 KB |
| lodash (full) | 72 KB | lodash-es (cherry-picked) | Varies |
| axios | 14 KB | ky / native fetch | 5 KB / 0 KB |
| redux + react-redux | 16 KB | Zustand | 1 KB |
| aws-sdk (full) | Varies | @aws-sdk/client-{service} | Modular |

## Build Tooling Speed Comparison

| Tool | Cold Start | HMR | Production Build | Bundle Size Efficiency |
|------|-----------|-----|-----------------|----------------------|
| Vite | ~300ms | <50ms | Fast (Rollup) | Good |
| webpack 5 | ~2-5s | 100-500ms | Moderate | Excellent (configurable) |
| Turbopack | ~200ms | <10ms | Fast | Good |
| Parcel | ~1s | <100ms | Moderate | Good |
| esbuild | ~50ms | N/A (bundler only) | Fastest | Good |

### Vite Production Tuning

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    target: 'es2020',            // Modern browsers — smaller output
    minify: 'esbuild',           // Fastest minifier; use 'terser' for legacy
    cssMinify: 'lightningcss',   // Faster than PostCSS
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          charts: ['recharts', 'd3'],
        },
      },
    },
    chunkSizeWarningLimit: 500,  // KB — raise if you accept larger chunks
  },
});
```

### Webpack Production Tuning

```javascript
module.exports = {
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: { test: /[\\/]node_modules[\\/]/, name: 'vendors', chunks: 'all' },
        common: { minChunks: 2, priority: -20, reuseExistingChunk: true },
      },
    },
    runtimeChunk: 'single',                       // Separate webpack runtime
    minimize: true,
    minimizer: [new TerserPlugin({ parallel: true }), new CssMinimizerPlugin()],
  },
};
```

## Continuous Bundle Monitoring

### Bundle Size CI Check

```yaml
# .github/workflows/bundlewatch.yml
- name: Check bundle size
  run: npx bundlewatch --config .bundlewatch.config.js
```

```javascript
// .bundlewatch.config.js
module.exports = {
  files: [
    { path: './dist/**/*.js', maxSize: '200kb' },
    { path: './dist/**/*.css', maxSize: '50kb' },
  ],
  ci: { trackBranches: ['main'] },
};
```

These optimization strategies align with the frontend-developer skill's production checklist: every kilobyte saved in the bundle directly improves Time to Interactive (TTI) and Core Web Vitals scores.
