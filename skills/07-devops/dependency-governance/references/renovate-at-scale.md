# Renovate at Scale

Configuring Renovate (or Dependabot) for consistent dependency management across 10+ repositories.

## Shared Configuration Architecture

```
github.com/org/renovate-config/
  default.json          # Base preset applied to all repos
  frontend.json         # React/Vue-specific rules
  backend.json          # Node/Python/Java-specific rules
  security.json         # Security-critical deps (no auto-merge)
```

All repos extend: `{ "extends": ["github>org/renovate-config"] }`.

## Grouping Strategy

Group related packages to reduce PR noise. Example groups:

- **React:** react, react-dom, @types/react, @types/react-dom
- **ESLint:** eslint, all eslint-plugin-*, @typescript-eslint/*
- **Testing:** jest, @testing-library/*, jest-environment-jsdom, @jest/globals
- **Babel:** @babel/core, @babel/preset-env, @babel/preset-react, babel-loader
- **TypeScript:** typescript (alone — major updates are breaking)

## Auto-Merge Rules

| Dependency Type | Patch | Minor | Major |
|----------------|-------|-------|-------|
| Dev tools (eslint, prettier) | Auto-merge | Auto-merge | Manual |
| Testing (jest, testing-library) | Auto-merge | Auto-merge | Manual |
| Type definitions (@types/*) | Auto-merge | Auto-merge | Manual |
| Runtime utilities (lodash, date-fns) | Auto-merge | Grouped PR | Manual |
| Frameworks (React, Next.js, Angular) | Auto-merge | Manual | Manual |
| Security (auth, crypto, JWT) | Auto-merge | Manual | Manual |

## Scheduling

Stagger updates to avoid CI thundering herd and to ensure engineers are available.

| Priority | Day | Time | Notes |
|----------|-----|------|-------|
| Critical | Mon-Wed | 6 AM UTC | Engineers online |
| High | Mon-Thu | 8 AM UTC | Standard work hours |
| Medium | Tue-Fri | 10 AM UTC | Off-peak CI |
| Low | Fri | 12 PM UTC | Merge failures -> fix Monday |

## Noise Reduction

- `stabilityDays: 3` — Wait 3 days after release before proposing update.
- `minimumReleaseAge: 3 days` — Skip brand-new releases.
- `automergeType: "pr"` — Use PR-based auto-merge (not branch).
- `rebaseWhen: "behind-base-branch"` — Only rebase when needed.
- `prConcurrentLimit: 5` — Maximum 5 open Renovate PRs per repo.

## Monitoring

- Dashboard: open PRs per repo, aging PRs, auto-merge success rate.
- Alert: >20 open PRs in a repo -> review grouping and auto-merge rules.
- Alert: auto-merge failure rate >10% -> review auto-merge eligibility.
