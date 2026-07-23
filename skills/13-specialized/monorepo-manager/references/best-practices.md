# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
1. **Don't adopt a monorepo before you have 3 packages:** `lib/` folder with relative imports works perfectly for 1-2 shared packages. A monorepo solves multi-package coordination — don't create the problem to justify the solution.
2. **Start with pnpm workspaces + Turborepo:** This is the 80/20 solution. You can always migrate to Nx/Bazel later if you outgrow it. Most teams never do.
3. **Affected-only builds are the killer feature:** Don't rebuild everything on every PR. `turbo build --filter=[origin/main...HEAD]` cuts CI time 60-90%.
4. **Enforce package boundaries from day 1:** ESLint `import/no-restricted-paths` or Nx module tags. Without enforcement, your monorepo becomes a spaghetti bowl where everything imports everything.
5. **Zero tolerance for circular dependencies:** Run `madge --circular packages/` in CI. Circular deps break tree-shaking, cause runtime errors, and make dependency graphs impossible to reason about.
6. **Hoist dependencies aggressively:** Set `"hoist": true` in `.npmrc`. Manual hoisting is error-prone. Only opt specific packages out when they have conflicting peer dependencies.
7. **Use Changesets for versioning:** Manual version bumps in monorepos are a nightmare. Changesets automate: `pnpm exec changeset` → describe change → CI opens Release PR.
8. **Remote caching pays for itself immediately:** If CI goes from 20 min to 5 min, that saves 15 min × developer × builds per day. At 5 developers, that's hours per day. S3 bucket caching costs <$5/mo.
9. **Shared configs, not shared codebases:** Extract ESLint/TS/Vite configs into shared packages. Consistent tooling across packages reduces cognitive load more than shared utility code ever will.
10. **Keep one package per team's ownership domain:** If Team A and Team B both modify the same package frequently, split it. Monorepo ≠ shared ownership of everything.
