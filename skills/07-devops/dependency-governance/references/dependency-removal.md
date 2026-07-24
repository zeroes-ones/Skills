# Dependency Removal & Tree-Shaking Verification

Safe process for removing unused or bloated dependencies with verification that the removal is real.

## Detection: Find Removal Candidates

1. **depcheck / knip:** Static analysis to find unused dependencies in package.json.
2. **Import scanning:** `grep -rn "from 'package'" src/` and `grep -rn "require('package')" src/`.
3. **Config scanning:** Check webpack, babel, eslint, postcss, jest configs for plugin references.
4. **Bundle analysis:** webpack-bundle-analyzer or source-map-explorer to find large, removable dependencies.

## Removal Process

1. Remove from package.json.
2. Run `npm install` / `yarn install` to regenerate lockfile.
3. Build the project: does it compile?
4. Run tests: do they pass?
5. **Bundle verification (CRITICAL):** Compare bundle size before and after.
   - If bundle size did not decrease: the dependency is still pulled in transitively.
   - Investigate with `npm ls package-name` or `yarn why package-name`.
6. If tree-shaking does not work (CJS modules), consider replacing with an ESM-native alternative.

## Common Failure Modes

- **"Removed from package.json but still in bundle."** Another dependency requires it transitively. Find the parent.
- **"Tests pass but production breaks."** Dependency was used in a code path not covered by tests.
- **"Removed but config still references it."** Babel plugin removed from package.json but still in babel.config.js.
- **"Tree-shaking did not work."** Package uses CommonJS. Webpack/Rollup cannot tree-shake CJS. Use ESM alternative.

## Post-Removal Monitoring

- Monitor production error rates for 48h after removal.
- Monitor bundle size trend: did it creep back up?
- Document: why was this dependency added, why was it removed, what replaced it?
