---
name: monorepo-manager
description: Monorepo tooling (Turborepo vs Nx vs pnpm workspaces vs Bazel vs Lerna vs Rush), repository structure patterns, build orchestration, dependency governance, CI/CD optimization, versioning strategies, migration from polyrepo.
author: Sandeep Kumar Penchala
---

# Monorepo Manager

Veteran's playbook for designing, configuring, and optimizing monorepo architectures at scale. Covers every major tool in the JS/TS ecosystem — Turborepo, Nx, pnpm workspaces, Bazel, Lerna, and Rush — plus repository structure, build orchestration, dependency governance, CI/CD, versioning, and polyrepo migration.

## Sub-Skills

When the agent identifies a specific monorepo need, drill into the relevant sub-skill rather than reading the full SKILL.md. Each sub-skill has dedicated references, tooling, and checklists.

| Sub-Skill | What It Covers | Quick Command |
|-----------|---------------|---------------|
| **Workspace Configuration** | pnpm workspaces, Yarn workspaces, npm workspaces — `pnpm-workspace.yaml`, hoisting, `workspace:*` protocol | `pnpm list --depth=0 --recursive` |
| **Build Orchestration** | Turborepo `turbo.json` pipelines, Nx task graph, `dependsOn` topology, parallel execution limits | `npx turbo run build --dry-run=json` |
| **Dependency Governance** | Hoisting strategies, syncpack/manypkg enforcement, `pnpm.overrides`, peer dependency resolution, deduplication | `npx syncpack list-mismatches` |
| **Package Boundary Enforcement** | `@nx/enforce-module-boundaries`, ESLint `import/no-restricted-paths`, TypeScript path aliases, circular dependency detection with `dpdm`/`madge` | `npx dpdm --circular --tree=false src/**/*.ts` |
| **CI/CD for Monorepos** | Affected detection (`--filter=[main...HEAD]`), remote caching (Vercel, S3, Nx Cloud), GitHub Actions matrix builds, cache warm/restore | `npx turbo run build --filter=[main...HEAD]` |
| **Versioning & Release** | Changesets workflow, independent vs fixed versioning, `semantic-release` monorepo setup, changelog generation | `npx changeset version` |
| **Monorepo Migration** | Polyrepo → monorepo strategy, `git filter-repo` for history preservation, `git subtree`, gradual adoption risk mitigation | `git filter-repo --path packages/my-lib --to-subdirectory-filter packages/my-lib` |

> **Token-saving rule:** Load sub-skill references on demand. If debugging cache misses → only read the build orchestration section. If setting up CI → only read the CI/CD section.

## Tool Selection & Decision Matrix

### Comparison Across 8 Dimensions

| Tool | Build Speed | Caching Capability | Task Graph | Plugin Ecosystem | Learning Curve (1–10) | Community Size | Enterprise Readiness | Best For |
|------|-------------|-------------------|------------|------------------|-----------------------|----------------|---------------------|----------|
| **Turborepo** | Very Fast | Local + Remote (Vercel, S3) | Auto via `dependsOn` | Minimal (growing) | 3 | Very Large | Good | JS/TS teams wanting fast setup + remote cache |
| **Nx** | Fast | Local + Remote (Nx Cloud) | Advanced (explicit + implicit) | Extensive (200+) | 6 | Large | Excellent | Large monorepos needing generators, boundaries, DTE |
| **pnpm workspaces** | N/A (install only) | None (no build cache) | None (no orchestrator) | N/A | 2 | Very Large | Partial | Package management only; pair with Turborepo/Nx |
| **Bazel** | Fastest (hermetic) | Local + Remote + RE | Full DAG | Polyglot (Java, Go, TS, etc.) | 9 | Medium | Excellent | Polyglot repos, large scale, strict hermeticity |
| **Lerna** | Slow (legacy) | None (native) | Basic (`--since`) | Minimal | 3 | Large (legacy) | Low | Publishing + changelogs when paired with Turborepo/Nx |
| **Rush** | Fast | Local + Remote (Rush Cloud) | Custom (Rush plugins) | Moderate | 7 | Medium | Excellent | Enterprise .NET/TS monorepos needing policy enforcement |

### Decision Tree

```
Is your codebase 100% JavaScript/TypeScript?
├── Yes
│   ├── Fewer than 10 packages, simple dependency graph?
│   │   ├── Yes → pnpm workspaces alone (no build orchestrator needed)
│   │   └── No → Want the simplest setup with fast caching?
│   │       ├── Yes → Turborepo + pnpm workspaces
│   │       └── No → Need code generation, module boundaries, distributed builds?
│   │           ├── Yes → Nx + pnpm workspaces
│   │           └── No → Vercel ecosystem? → Turborepo
│   └── No (polyglot: Java + Go + TS + Python)
│       ├── Need hermetic builds and remote execution?
│       │   ├── Yes → Bazel
│       │   └── No → Nx (supports multiple languages via executors)
│
Is your org > 500 engineers, strict dependency governance required?
├── Yes → Rush (Microsoft-scale policy enforcement)
└── No → Use Turborepo or Nx

Are you migrating from Lerna?
├── Keep Lerna for publish/changelog, add Turborepo for builds
└── Full migration → Remove Lerna, use Turborepo + changesets
```

### When pnpm Workspaces Alone Is Enough

- **Small monorepos** (3–8 packages) with shallow dependency graphs
- **No need for caching** — build times are already < 30 seconds
- **No CI optimization needed** — full rebuilds are fast enough
- **Simple run scripts** — `pnpm --filter` and `pnpm -r` suffice
- **Example**: design system monorepo with 6 icon/component/theme packages

### When You Need More Than pnpm Workspaces

- Build times > 2 minutes locally or > 10 minutes in CI
- Packages share dependencies that cause rebuild cascades
- Need remote caching so CI and devs don't duplicate builds
- Need task orchestration (build deps before consumers, parallel tests)
- Need code generation for packages, components, configs
- Need dependency boundary enforcement (apps → libs, not libs → apps)
- **Rule of thumb**: if you're writing shell scripts to orchestrate build order, you need Turborepo or Nx.

## Repository Structure

### Structural Patterns

| Pattern | Layout | When to Use |
|---------|--------|-------------|
| **Package-first** | `packages/*` | Small–medium repos, simple ownership. Turborepo's default model. |
| **Domain-first** | `teams/core/`, `teams/billing/`, `teams/shared/` | Large orgs with clear team ownership. Each team owns their domain subtree. |
| **Hybrid (most common)** | `apps/*`, `packages/*`, `tools/*` | Teams of all sizes. Separates deployables (apps) from libraries (packages) from tooling (tools). |

### Hybrid Structure — Deep Dive

```
my-monorepo/
├── apps/
│   ├── web/                # Next.js app
│   │   └── package.json    # "name": "@myorg/web"
│   ├── api/                # Express/Fastify API
│   │   └── package.json    # "name": "@myorg/api"
│   └── mobile/             # React Native app
│       └── package.json
├── packages/
│   ├── ui/                 # Shared UI component library
│   │   └── package.json    # "name": "@myorg/ui"
│   ├── utils/              # Shared utility functions
│   │   └── package.json    # "name": "@myorg/utils"
│   ├── types/              # Shared TypeScript types/interfaces
│   │   └── package.json    # "name": "@myorg/types"
│   └── config/
│       ├── typescript-config/
│       ├── eslint-config/
│       ├── prettier-config/
│       └── jest-config/
├── tools/
│   ├── generators/         # Plop or custom code generators
│   └── scripts/            # CI helper scripts
├── pnpm-workspace.yaml
├── turbo.json
├── package.json            # Root — only dev tooling
└── .github/workflows/
```

### Package Entry Points — The `exports` Field

Do NOT rely on `main` + `module` alone. Use the `exports` field for proper encapsulation:

```jsonc
// packages/ui/package.json
{
  "name": "@myorg/ui",
  "type": "module",
  "main": "./dist/index.js",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.js",
      "types": "./dist/index.d.ts"
    },
    "./button": {
      "import": "./dist/button/index.mjs",
      "require": "./dist/button/index.js",
      "types": "./dist/button/index.d.ts"
    },
    "./styles.css": "./dist/styles.css"
  },
  // Anything NOT in exports is private — consumers cannot deep-import it
  "files": ["dist"],
  "publishConfig": {
    "access": "public"
  }
}
```

### Barrel Exports — Public API Surface

```typescript
// packages/ui/src/index.ts — public barrel
export { Button } from './button';
export { Card } from './card';
export { ThemeProvider } from './theme';
// NOT exported: internal hooks, utils, types — these are implementation details

// packages/ui/src/index.test.ts — barrel test ensures nothing is broken
import * as publicApi from './index';
describe('@myorg/ui public API', () => {
  it('should export Button', () => expect(publicApi.Button).toBeDefined());
  it('should export Card', () => expect(publicApi.Card).toBeDefined());
});
```

### Shared Config Packages

```jsonc
// packages/config/typescript-config/package.json
{
  "name": "@myorg/typescript-config",
  "version": "0.0.0",
  "private": true,
  "files": ["./base.json", "./nextjs.json", "./react-library.json"]
}
```

- **`@myorg/typescript-config/base.json`**: `strict: true`, `exactOptionalPropertyTypes: true`, `noUncheckedIndexedAccess: true`
- **`@myorg/typescript-config/nextjs.json`**: extends `base.json`, adds `"module": "ESNext"`, `"jsx": "preserve"`
- **`@myorg/eslint-config`**: extends `eslint-config-next`, `eslint-config-prettier`, with `@nx/enforce-module-boundaries` rule
- **`@myorg/prettier-config`**: single `module.exports = { semi: true, singleQuote: true, trailingComma: 'all' }`
- **`@myorg/jest-config`**: `jest-preset.js` exporting `{ testEnvironment: 'node', transform: { '^.+\\.ts$': 'ts-jest' } }`

All packages extend these:

```jsonc
// apps/web/package.json
{
  "prettier": "@myorg/prettier-config",
  "jest": { "preset": "@myorg/jest-config" }
}
// tsconfig.json
{
  "extends": "@myorg/typescript-config/nextjs.json"
}
// .eslintrc.js
module.exports = {
  root: true,
  extends: ["@myorg/eslint-config/next"]
};
```

### Internal Libraries vs Published Packages

| Category | Private | Published | Example |
|----------|---------|-----------|---------|
| **Shared config** | ✅ private | ❌ | `@myorg/typescript-config` |
| **Internal types** | ✅ private | ❌ | `@myorg/types` |
| **Shared utils** | ✅ private (or published) | depends | `@myorg/utils` — publish if other orgs use it |
| **UI components** | ⚠️ start private, publish when mature | ✅ eventually | `@myorg/ui` → `@acme/ui` |
| **SaaS platform libs** | ✅ private | ❌ | Business logic, API client wrappers |

**Rule**: Keep a package private until an external consumer explicitly needs it. Publishing prematurely creates a maintenance contract. Use `"private": true` and `"publishConfig": { "access": "restricted" }` for internal-only packages.

## Build System Deep Dive

### Task Orchestration

#### Dependency Graph Construction

Turborepo and Nx both build a dependency graph from your workspace configuration:

```
@myorg/web ──depends-on──> @myorg/ui ──depends-on──> @myorg/utils
@myorg/api ──depends-on──> @myorg/utils
                            @myorg/utils ──depends-on──> (none)
```

Nx's graph is richer — it distinguishes **npm dependencies** (package.json) from **implicit dependencies** (import statements in source code). Turborepo only walks package.json dependencies.

#### Pipeline Configuration — `turbo.json`

```jsonc
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [".env", "tsconfig.json", ".eslintrc.js"],
  "globalEnv": ["NODE_ENV", "API_URL", "VERCEL_ENV"],
  "pipeline": {
    "build": {
      // ^build = build dependencies first (topological order)
      "dependsOn": ["^build"],
      // Files to hash for cache key
      "inputs": ["src/**/*.ts", "src/**/*.tsx", "package.json", "tsconfig.json"],
      // Outputs to cache and restore
      "outputs": ["dist/**", ".next/**"],
      // Environment variables that affect the build output
      "env": ["NODE_ENV"],
      // How many tasks to run in parallel (default: # of CPUs)
      "concurrency": 8
    },
    "test": {
      // $ means "self" — wait for this package's build to finish first
      "dependsOn": ["build"],
      "outputs": ["coverage/**"],
      "inputs": ["src/**/*.test.ts", "src/**/*.spec.ts", "jest.config.ts"],
      "concurrency": 4
    },
    "lint": {
      // No dependsOn — lint can run independently
      "dependsOn": [],
      "outputs": [],
      "inputs": ["src/**/*.ts", "src/**/*.tsx", ".eslintrc.js"]
    },
    "type-check": {
      "dependsOn": ["^build"],
      "outputs": [],
      "inputs": ["src/**/*.ts", "src/**/*.tsx", "tsconfig.json"]
    },
    "dev": {
      "cache": false,  // Don't cache dev servers
      "persistent": true, // Mark as long-running
      "dependsOn": ["^build"]
    }
  }
}
```

#### Turbo DependsOn Notation

| Syntax | Meaning | Example |
|--------|---------|---------|
| `"^build"` | Wait for dependency's `build` to finish | Build UI before web |
| `"build"` | Wait for this package's `build` (self) | Test after build |
| `["^build", "lint"]` | Wait for dep build + this package's lint | |
| `[]` | No dependencies — runs immediately | lint, type-check |
| `"$FOO"` | Await env var `FOO` | Environment-specific builds |

#### Nx Pipeline Configuration

```jsonc
// nx.json
{
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": [
        "{projectRoot}/src/**/*",
        "{projectRoot}/package.json",
        "{projectRoot}/tsconfig.json",
        "!{projectRoot}/src/**/*.test.ts"  // exclude test files from build cache keys
      ],
      "outputs": ["{projectRoot}/dist", "{projectRoot}/.next"]
    },
    "test": {
      "dependsOn": ["build"],
      "inputs": [
        "{projectRoot}/src/**/*",
        "{projectRoot}/jest.config.ts",
        "sharedGlobals"
      ],
      "outputs": ["{projectRoot}/coverage"]
    }
  },
  "namedInputs": {
    "sharedGlobals": ["{workspaceRoot}/tsconfig.json", "{workspaceRoot}/.eslintrc.js"],
    "production": ["{projectRoot}/src/**/*", "!{projectRoot}/src/**/*.test.ts"]
  }
}
```

### Caching Architecture

#### Input Hashing

Turborepo computes a SHA-256 hash from:
- File contents of all `inputs` glob matches
- Contents of `globalDependencies` files
- Values of `globalEnv` variables
- Contents of `turbo.json` itself

Nx does the same concept with `inputs` and `namedInputs` — the hash key includes every file in the input set.

**Cache key = `SHA256(input_files + global_deps + env_vars + task_definition)`**

#### Cache Hit/Miss Debugging

```bash
# Turborepo — verbose cache info
turbo build --verbos e --dry-run

# See what inputs were hashed
turbo build --dry-run=json | jq '.tasks[] | select(.package == "@myorg/web") | .hash'

# Nx — what changed
nx affected:build --base=main --verbose

# Nx — compare cache keys
nx graph --affected --base=main

# Manually verify inputs match
find packages/ui/src -type f -exec md5sum {} \;
```

#### Local Caching

```bash
# Default: local cache at node_modules/.cache/turbo
# Clear local cache
turbo clean

# Nx local cache at .nx/cache
nx reset
```

#### Remote Caching

```bash
# Turborepo — Vercel Remote Cache
npx turbo login
npx turbo link

# Turborepo — Custom S3 Remote Cache
# Set environment variables:
TURBO_API=https://your-cache.example.com
TURBO_TOKEN=your-token
TURBO_TEAM=your-team

# Nx — Nx Cloud
npx nx connect-to-nx-cloud

# Nx — Custom Remote Cache (shareable CLI)
# Configure in nx.json:
"tasksRunnerOptions": {
  "default": {
    "runner": "nx/tasks-runners/default",
    "options": {
      "cacheableOperations": ["build", "test", "lint"],
      "remoteCache": {
        "enabled": true,
        "url": "https://cache.example.com"
      }
    }
  }
}
```

### Incremental Builds

Turborepo and Nx only rebuild packages whose inputs changed PLUS all transitive consumers:

```
Change in @myorg/utils:
  └─ @myorg/utils is rebuilt
     └─ @myorg/ui is rebuilt (depends on utils)
        └─ @myorg/web is rebuilt (depends on ui)
        └─ @myorg/api is rebuilt (depends on utils)

No change in @myorg/types or @myorg/ui own code → they use cache
```

This is the **monorepo superpower** — a change in a utility function doesn't require rebuilding the entire codebase.

### What to Cache / What Not to Cache

| Cache | Don't Cache |
|-------|-------------|
| `dist/` | `node_modules/` (restore from lockfile) |
| `.next/` | `.env` files (secrets) |
| `coverage/` | OS-specific binaries |
| `build/` | Log files |
| `storybook-static/` | PID files |
| Compiled outputs | Lockfile itself |

## Dependency Management

### Hoisting Strategies

| Strategy | Package Manager | Behavior | Phantom Deps? | Disk Usage |
|----------|----------------|----------|---------------|------------|
| **Strict** | pnpm | Content-addressable store, nested `node_modules` via symlinks | ❌ No | Lowest |
| **Hoisted** | npm, Yarn Classic | All deps flat in root `node_modules` | ✅ Yes | Highest |
| **Flexible** | Yarn Berry (PnP) | Virtual filesystem via `.pnp.cjs` | ❌ No (configurable) | Low |

**Phantom dependencies** — when a package can import a dependency it didn't declare. pnpm's strict mode prevents this entirely. Example:

```bash
# This works in npm/Yarn Classic but breaks in pnpm — BAD!
# apps/web/src/api.ts
import { something } from 'dep-only-in-ui-package';  // works in npm, breaks in pnpm
```

**Always use pnpm for new monorepos.** The phantom dependency protection alone is worth the switch.

### Version Consistency Tooling

#### syncpack Configuration

```jsonc
// .syncpackrc.json
{
  "versionGroups": [
    {
      "label": "React must be 18.x across all packages",
      "packages": ["**"],
      "dependencies": ["react", "react-dom"],
      "pinVersion": "^18.2.0"
    },
    {
      "label": "TypeScript must be 5.x",
      "packages": ["**"],
      "dependencies": ["typescript"],
      "pinVersion": "^5.3.0"
    },
    {
      "label": "Internal packages must use workspace protocol",
      "packages": ["**"],
      "dependencies": ["@myorg/**"],
      "dependencyTypes": ["dev", "prod"],
      "isBanned": true,
      "banMessage": "Use workspace:* for @myorg internal dependencies"
    }
  ],
  "semverGroups": [
    {
      "label": "All React ecosystem must use same range type",
      "packages": ["**"],
      "dependencyTypes": ["prod"],
      "range": "^"
    }
  ]
}
```

```bash
# Check for version mismatches
pnpm syncpack list-mismatches

# Fix mismatches automatically
pnpm syncpack fix-mismatches

# In CI: lint only, don't auto-fix
pnpm syncpack lint
```

#### manypkg — Lightweight Alternative

```bash
# Install
pnpm add -Dw @manypkg/cli

# In package.json
{
  "scripts": {
    "lint:repro": "manypkg check"
  }
}
```

#### pnpm Overrides

```jsonc
// root package.json
{
  "pnpm": {
    "overrides": {
      "react": "^18.2.0",
      "next": "^14.0.0",
      // Force a single version of a transitive dependency
      "semver": "^7.5.4"
    },
    "peerDependencyRules": {
      "allowedVersions": {
        "react": "^18.2.0",
        "react-dom": "^18.2.0"
      }
    }
  }
}
```

### Peer Dependency Resolution

```jsonc
// packages/ui/package.json — DECLARE PEER DEPS!
{
  "name": "@myorg/ui",
  "peerDependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  },
  "devDependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
```

With pnpm, enable strict peer dep checking:
```yaml
# .npmrc
strict-peer-dependencies=true
auto-install-peers=true
```

### Dependency Audit Commands

```bash
# Why does this package depend on X?
pnpm why react
pnpm why --recursive typescript

# List dependency tree with depth limit
pnpm list --depth=3 --filter=@myorg/web

# Find duplicate versions
pnpm list -r --depth=1 | grep "react@" | sort | uniq -c

# Visualize dependency graph (requires graphviz)
pnpm list --depth=5 --json | pnpx dependency-tree --output graph.html

# Check for outdated dependencies across all packages
pnpm outdated -r

# Find packages that depend on a specific internal package
pnpm ls -r --filter=@myorg/utils --depth=0
```

## Code Sharing & Package Boundaries

### Barrel Exports Pattern

```typescript
// packages/ui/src/index.ts — PUBLIC API
export { Button } from './button/Button';
export { Card, CardHeader, CardBody } from './card';
export { useTheme } from './theme/hooks';

// packages/ui/src/button/index.ts — internal barrel
export { Button } from './Button';
export type { ButtonProps } from './types';
```

**Why barrels matter in monorepos**: They define the public contract. If `packages/utils` exports `{ add, subtract }` from `index.ts`, consumers import from `@myorg/utils` — never from `@myorg/utils/src/math/add`. Internal refactoring (renaming files, splitting modules) doesn't break consumers.

### Enforcing Package Boundaries

#### Nx `enforce-module-boundaries`

```jsonc
// .eslintrc.json (root)
{
  "rules": {
    "@nx/enforce-module-boundaries": [
      "error",
      {
        "enforceBuildableLibDependency": true,
        "allow": [],
        "depConstraints": [
          {
            "sourceTag": "scope:shared",
            "onlyDependOnLibsWithTags": ["scope:shared"]
          },
          {
            "sourceTag": "scope:ui",
            "onlyDependOnLibsWithTags": ["scope:shared", "scope:ui"]
          },
          {
            "sourceTag": "scope:app",
            "onlyDependOnLibsWithTags": ["scope:shared", "scope:ui", "scope:api"]
          }
        ]
      }
    ]
  }
}
```

Tag each package:
```jsonc
// packages/ui/package.json { "nx": { "tags": ["scope:ui"] } }
// apps/web/package.json { "nx": { "tags": ["scope:app"] } }
// packages/utils/package.json { "nx": { "tags": ["scope:shared"] } }
```

#### ESLint `import/no-restricted-paths`

```jsonc
// apps/web/.eslintrc.json
{
  "rules": {
    "import/no-restricted-paths": [
      "error",
      {
        "zones": [
          // apps/web cannot import from other apps
          { "target": "./src", "from": "../apps", "message": "Apps cannot import from other apps" },
          // apps/web cannot import from packages/internal
          { "target": "./src", "from": "../packages/internal", "message": "Apps cannot import internal packages" }
        ]
      }
    ]
  }
}
```

#### TypeScript Path Restrictions

```jsonc
// packages/ui/tsconfig.json
{
  "compilerOptions": {
    "paths": {
      "@myorg/utils": ["../../packages/utils/src"],  // allowed
      "@myorg/apps/*": []  // not accessible (empty array = no resolution)
    }
  }
}
```

### Circular Dependency Detection

```bash
# dpdm — Dependency graph with cycle detection
pnpm add -Dw dpdm
dpdm --circular packages/ui/src/index.ts

# Madge — Visual circular dependency detection
pnpm add -Dw madge
madge --circular --extensions ts,tsx packages/
madge --image graph.png packages/ui/src/

# Nx — Built-in circular dependency check
nx graph --focus=@myorg/ui
# Look for cycles in the interactive graph

# Turborepo — check with graph output
turbo run build --graph=graph.html
# Open graph.html and look for cycles
```

**Rule**: A package should NEVER import from a package that imports from it, directly or transitively. Caught early, circular deps are easy to fix. Caught late, they require major refactors.

## CI/CD for Monorepos

### Affected Detection

```bash
# Turborepo — build only what changed vs main
turbo build --filter=[main...HEAD]

# Turborepo — filter by specific package + dependents
turbo build --filter=@myorg/utils...  # includes dependents
turbo build --filter=...@myorg/utils  # includes dependencies

# Nx — affected commands
nx affected:build --base=main
nx affected:test --base=main
nx affected:lint --base=main

# Nx — graph affected tasks
nx affected:graph --base=main

# pnpm — manual affected (no cache, but works)
pnpm --filter=[origin/main...HEAD] run build
```

### Complete CI Pipeline — GitHub Actions

```yaml
# .github/workflows/ci.yml
name: Monorepo CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true

env:
  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
  TURBO_TEAM: ${{ vars.TURBO_TEAM }}
  TURBO_REMOTE_CACHE: true

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Required for affected detection

      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      # Lint only affected packages
      - run: pnpm lint --filter=[main...HEAD]

      # Type-check only affected packages
      - run: pnpm type-check --filter=[main...HEAD]

      # Build affected packages + dependents
      - run: pnpm build --filter=[main...HEAD]...

  test:
    runs-on: ubuntu-latest
    needs: quality
    strategy:
      fail-fast: false
      matrix:
        # Split CI into parallel test jobs per app/package
        package:
          - --filter=@myorg/web
          - --filter=@myorg/api
          - --filter=@myorg/ui
          - --filter=@myorg/utils
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm test ${{ matrix.package }}

  e2e:
    runs-on: ubuntu-latest
    needs: [quality, test]
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm e2e --filter=[main...HEAD]...

  size-limit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm build --filter=@myorg/affected...
      - run: pnpm size-limit
```

### Remote Caching Strategies

| Storage | Turborepo | Nx | Cost | Best For |
|---------|-----------|-----|------|----------|
| **Vercel Remote Cache** | Built-in | — | Free tier + paid | Vercel users |
| **Nx Cloud** | — | Built-in | Free tier + paid | Nx users |
| **S3 / GCS** | Custom server | Custom runner | Storage costs | Self-hosted/air-gapped |
| **GitHub Actions Cache** | turborepo-remote-cache action | community actions | Free (GH plan) | GH-only teams |

Self-hosted S3 remote cache for Turborepo:
```bash
# Using turborepo-remote-cache server
# https://github.com/ducktors/turborepo-remote-cache
docker run -d \
  -e STORAGE_PROVIDER=s3 \
  -e AWS_ACCESS_KEY_ID=... \
  -e AWS_SECRET_ACCESS_KEY=... \
  -e S3_BUCKET=my-turbo-cache \
  ducktors/turborepo-remote-cache

# Point turbo.json at it
TURBO_API=https://turbo-cache.myorg.com
TURBO_TOKEN=cache-token
```

### CI Cache Optimization

```yaml
# GitHub Actions — restore turbo/nx cache
- name: Restore Turborepo Cache
  uses: actions/cache@v3
  with:
    path: node_modules/.cache/turbo
    key: turbo-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}
    restore-keys: |
      turbo-${{ runner.os }}-

- name: Restore Nx Cache
  uses: actions/cache@v3
  with:
    path: .nx/cache
    key: nx-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}
    restore-keys: |
      nx-${{ runner.os }}-
```

### Parallel Pipeline Strategies

**Strategy 1: Single agent, parallel tasks (fast for < 50 packages)**
```bash
turbo build test lint --parallel --concurrency=6
```

**Strategy 2: Matrix CI (scales to 100+ packages)**
```yaml
matrix:
  package:
    - --filter=@myorg/web...
    - --filter=@myorg/api...
    - --filter=@myorg/ui...
    - --filter=@myorg/utils...
```
Each job runs independently, failures are isolated, retries are per-package.

**Strategy 3: Nx Distributed Task Execution (1000+ packages)**
```bash
# Agent 1 (coordinator)
nx-cloud start-ci-run --stop-agents-after=build
nx affected:build --base=main

# Agents 2-N
nx-cloud start-agent
```

## Version Management

### Independent vs Fixed Versioning

| Aspect | Fixed/Locked | Independent |
|--------|-------------|-------------|
| **Version** | All packages share one version (e.g., `1.2.3`) | Each package has its own (e.g., `utils@1.0.0`, `ui@2.1.3`) |
| **Bump** | Release bumps everything | Bump only changed packages |
| **Changelog** | Single changelog | Per-package changelogs |
| **Best for** | Tightly coupled packages, single delivery | Loosely coupled, independent release cycles |
| **Tooling** | `standard-version`, `semantic-release` | Changesets |
| **Example** | React, Vue core monorepos | Design systems, utility libraries |

**Recommendation**: Use **Changesets with independent versioning** for most monorepos. Fixed versioning creates unnecessary version bumps for packages that haven't changed, and consumers of individual packages end up with confusing version gaps.

### Changesets — Complete Workflow

```bash
# 1. Developer adds a changeset
npx changeset
# Interactive: select changed packages, choose bump type, write summary

# 2. Changeset file created at .changeset/<random-name>.md
# Contents:
# ---
# "@myorg/ui": minor
# "@myorg/utils": patch
# ---
#
# Add new Button variants and fix utility edge case

# 3. Commit the changeset alongside code changes
git add packages/ui/ packages/utils/ .changeset/
git commit -m "feat(ui): add new Button variants"
```

#### Changeset Config

```jsonc
// .changeset/config.json
{
  "$schema": "https://unpkg.com/@changesets/config@3.0.0/schema.json",
  "changelog": ["@changesets/changelog-github", { "repo": "myorg/repo" }],
  "commit": false,
  "fixed": [],
  "linked": [],
  "access": "public",
  "baseBranch": "main",
  "updateInternalDependencies": "patch",
  "ignore": ["@myorg/internal-tooling"]
}
```

#### Version PR & Publish — GitHub Action

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    branches: [main]

concurrency: ${{ github.workflow }}-${{ github.ref }}

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      # Create/update "Version Packages" PR or publish
      - name: Create Release Pull Request or Publish
        uses: changesets/action@v1
        with:
          version: pnpm changeset version
          publish: pnpm changeset publish
          commit: "chore(release): version packages"
          title: "Version Packages"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Semantic Release in Monorepos

```bash
# Multi-semantic-release — per-package semantic release
pnpm add -Dw multi-semantic-release

# Configure commit message conventions on each package
# package.json > "release" > { "branches": ["main"] }

# Run
pnpm multi-semantic-release
```

Commit convention:
```
feat(ui): add new Button variant    → minor bump for @myorg/ui
fix(utils): correct edge case       → patch bump for @myorg/utils
feat(api)!: change auth flow        → major bump for @myorg/api
docs(readme): update API docs       → no release
```

### Release Pipeline Summary

```
Developer commits code + changeset → PR merged to main
  └─ GitHub Action triggers
      └─ changesets/action:
          ├─ If changesets exist → run "changeset version" → create "Version Packages" PR
          └─ If "Version Packages" PR merged → run "changeset publish"
              ├─ Publish packages to npm (with workspace:* replaced by actual versions)
              ├─ Create GitHub releases per package
              └─ Tag commits (v1.2.3, @myorg/ui@1.2.3, etc.)
```

## Migration Path: Polyrepo → Monorepo

### Strategy Selection

| Strategy | Best For | Risk | Timeline |
|----------|----------|------|----------|
| **Big-bang** | Starting fresh (no legacy), < 10 packages | High | Days |
| **Gradual** | Existing codebase, > 10 packages, multiple teams | Low | Weeks–months |

### Big-Bang Migration

```bash
# 1. Create new monorepo directory
mkdir my-monorepo && cd my-monorepo

# 2. Initialize pnpm workspace
pnpm init
# Create pnpm-workspace.yaml

# 3. Clone each package with history using git filter-repo
git clone --bare https://github.com/myorg/utils.git
cd utils.git
git filter-repo --path-rename :packages/utils/ --force
cd ..
git clone utils.git my-monorepo

# Repeat for each package...

# 4. Merge all histories into one repo
cd my-monorepo
git remote add utils ../utils.git
git fetch utils
git merge --allow-unrelated-histories utils/main
git remote remove utils

# 5. Install dependencies and verify
pnpm install
pnpm build
```

### Gradual Adoption — Step by Step

**Phase 1: Identify candidates (Week 1)**
- Pick 2–3 packages that are tightly coupled (e.g., shared UI lib, utils, types)
- These should have low risk and high cross-dependency value

**Phase 2: Create monorepo shell (Week 1)**
```bash
mkdir my-monorepo
cd my-monorepo
git init
pnpm init
# pnpm-workspace.yaml pointing to packages/*
# Install Turborepo
pnpm add -Dw turbo
# Create turbo.json
turbo init
```

**Phase 3: Migrate packages (Weeks 2–3)**
- Copy each package into `packages/`
- Preserve git history per package (use `git filter-repo` if needed)
- Update all internal imports to use workspace protocol
- Update CI to run from monorepo root

**Phase 4: Expand (Weeks 4+)**
- Add more packages gradually
- Demonstrate value: faster CI (affected builds), atomic cross-package changes
- Document working patterns for teams adopting later

### Preserving Git History

```bash
# git filter-repo — Extract package with full history
brew install git-filter-repo  # macOS

# Create a directory-filtered copy of the repo
git clone --bare https://github.com/myorg/utils.git
cd utils.git
git filter-repo \
  --path src/ \
  --path package.json \
  --path tsconfig.json \
  --path LICENSE \
  --path-rename src/:packages/utils/src/ \
  --force

# git subtree — Simpler but loses history detail
git subtree add --prefix=packages/utils ../utils.git main

# git merge --allow-unrelated-histories — Preserves all history
git remote add utils ../utils.git
git fetch utils
git merge --allow-unrelated-histories utils/main
git remote remove utils
# Then move files to correct location with git mv
```

### Risk Mitigation

| Risk | Mitigation |
|------|------------|
| **CI breaks for everyone** | Start with low-risk packages. Gradual adoption keeps other CI pipelines untouched. |
| **Git history loss** | Use `git filter-repo` before merging. Never `rm -rf && cp`. |
| **Dependency conflicts** | Use pnpm's strict resolution. Pin critical shared deps (React, Next). Run `pnpm why` on conflicts. |
| **Build times explode** | Set up affected-only CI immediately. Don't skip caching setup. |
| **Team ownership confusion** | Keep CODEOWNERS per package/directory. Merge freely, but review per team. |

### What to Keep Separate

- **Secrets and environments** — never merge `.env` files. Use `sops` or vault for secrets.
- **Database schemas** — monorepo the code, not the data.
- **CI configurations for non-migrated repos** — leave them in their original repos until migrated.
- **Heavy binary assets** (ML models, large datasets) — use Git LFS or external artifact storage, not the monorepo.

### What to Bring In First

**Good first candidates:**
- Shared type definitions (`@myorg/types`)
- Shared utility libraries (`@myorg/utils`)
- Shared UI components (`@myorg/ui`)
- Internal tooling / CLI tooling
- Configuration packages

**Bring in later (after proving value):**
- Applications (apps/)
- Full domain packages
- Legacy packages that need refactoring

## Developer Experience

### Local Dev Setup

```bash
# Root package.json scripts
{
  "scripts": {
    "dev": "turbo dev --parallel",
    "dev:web": "turbo dev --filter=@myorg/web",
    "dev:api": "turbo dev --filter=@myorg/api",
    "build": "turbo build",
    "build:ui": "turbo build --filter=@myorg/ui",
    "test": "turbo test",
    "test:affected": "turbo test --filter=[main...HEAD]",
    "lint": "turbo lint",
    "type-check": "turbo type-check",
    "clean": "turbo clean && rm -rf node_modules",
    "format": "prettier --check \"**/*.{ts,tsx,json}\"",
    "format:fix": "prettier --write \"**/*.{ts,tsx,json}\""
  },
  "devDependencies": {
    "turbo": "latest",
    "prettier": "^3.0.0"
  }
}

# Developer workflow
git checkout -b feat/add-button-variant
# ... make changes in packages/ui ...
pnpm dev          # Starts all apps with hot reload
# ... verify in web and api apps ...
pnpm test --filter=@myorg/ui
pnpm build        # Full build to verify nothing is broken
pnpm changeset    # Add changeset
git add -A && git commit -m "feat(ui): add new variant"
git push -u origin HEAD
```

### Shared ESLint Configuration

```javascript
// packages/config/eslint-config/library.js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:import/recommended',
    'plugin:import/typescript',
    'prettier',
  ],
  plugins: ['@typescript-eslint', 'import'],
  rules: {
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    'import/no-default-export': 'error',
    'import/order': ['error', {
      groups: ['builtin', 'external', 'internal', 'parent', 'sibling', 'index'],
      'newlines-between': 'always',
    }],
  },
  settings: {
    'import/resolver': {
      typescript: {
        alwaysTryTypes: true,
      },
    },
  },
};
```

### VSCode Workspace Configuration

```jsonc
// my-monorepo.code-workspace
{
  "folders": [
    { "name": "root", "path": "." },
    { "name": "web", "path": "apps/web" },
    { "name": "api", "path": "apps/api" },
    { "name": "ui", "path": "packages/ui" },
    { "name": "utils", "path": "packages/utils" }
  ],
  "settings": {
    "typescript.tsdk": "node_modules/typescript/lib",
    "eslint.workingDirectories": [
      { "mode": "auto" }
    ],
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.codeActionsOnSave": {
      "source.fixAll.eslint": "explicit"
    },
    "npm.packageManager": "pnpm",
    "search.exclude": {
      "**/node_modules": true,
      "**/dist": true,
      "**/.next": true
    },
    "files.exclude": {
      "**/node_modules": true
    }
  },
  "extensions": {
    "recommendations": [
      "dbaeumer.vscode-eslint",
      "esbenp.prettier-vscode",
      "nrwl.angular-console",       // Nx extension
      "mikestead.dotenv",
      "bradlc.vscode-tailwindcss"
    ]
  }
}
```

### Git Hooks — Husky + lint-staged

```bash
# Install
pnpm add -Dw husky lint-staged
pnpm exec husky init

# .husky/pre-commit
pnpm exec lint-staged

# .husky/commit-msg
pnpm exec -- commitlint --edit $1

# package.json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,yaml}": [
      "prettier --write"
    ]
  }
}

# commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'scope-enum': [2, 'always', ['web', 'api', 'ui', 'utils', 'types', 'tools', 'release']],
  },
};
```

## Cross-Skill Coordination

Monorepo management touches every development team. A monorepo tooling change affects everyone's daily workflow — coordination isn't optional.

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **All Frontend Teams** | Shared package updates, workspace changes, build config | Package version bumps, breaking changes in shared libs, workspace dependency rules |
| **All Backend Teams** | Shared service libraries, protobuf/gRPC schemas, database migrations | Shared library API changes, schema evolution, cross-service contract tests |
| **DevOps / Platform Team** | CI/CD pipeline, build caching, deployment orchestration | Build graph changes, cache invalidation rules, affected projects detection |
| **System Architect** | Repository boundaries, module extraction, dependency direction | Module ownership, dependency rules (e.g., no circular deps), extraction candidates |
| **CTO Advisor** | Monorepo vs polyrepo strategy, tooling investment | Tooling ROI, developer experience metrics, migration feasibility |
| **Security Reviewer** | Dependency scanning, vulnerability management, access control | CODEOWNERS rules, dependency audit strategy, secret detection scope |
| **QA Engineer** | Test orchestration, affected test detection, integration testing | Test dependency graph, affected test selection, cross-service integration test scope |
| **Developer Experience (DX)** | Local development setup, IDE integration, onboarding | Workspace setup time, hot reload experience, IDE project configuration |
| **Project Manager** | Migration timelines, team impact, rollout coordination | Sprint impact assessment, migration milestones, team communication plan |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Shared package major version bump (breaking change) | All Teams, System Architect | All consumers must update; migration guide needed |
| Build cache invalidation (full rebuild required for all projects) | DevOps, All Teams | CI times spike 5-10x; communicate expected duration |
| New workspace or project added to monorepo | DevOps, QA, DX | CI pipeline update, CODEOWNERS, test suite registration |
| Dependency vulnerability in shared package (Critical/High) | Security Reviewer, All Consumer Teams | Patch + propagation timeline; all consumers affected |
| Monorepo tool migration (e.g., Lerna → Nx, Yarn → pnpm) | All Teams, DevOps, DX, CTO Advisor | Breaking workflow change; requires training and migration window |
| Circular dependency detected between workspaces | System Architect, Affected Teams | Architecture violation; refactor or dependency rule change needed |
| Build times increase by >50% for any pipeline | DevOps, DX, Engineering Leads | Developer productivity impact; build optimization investigation |
| Flaky test rate exceeds 5% in shared packages | QA, All Consumer Teams | CI trust eroding; test quarantine or fix required |

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| Monorepo tooling causing >1 hour/day developer productivity loss | **CTO Advisor** + VP Engineering | Developer experience crisis; tooling investment or polyrepo evaluation |
| Tight coupling creating "distributed monolith" across packages | **System Architect** + CTO Advisor | Architecture degradation; bounded context enforcement needed |
| Build/deploy times exceeding business SLAs (e.g., >30 min to production) | **DevOps Lead** + CTO Advisor | CI/CD bottleneck; infrastructure or architecture investment needed |
| Proposal to split monorepo into polyrepo | **CTO Advisor** + System Architect + All Team Leads | Strategic architecture decision; 3-6 month migration impact |
| License compliance issue in shared dependency | **Legal Advisor** + Security Reviewer | Legal risk; may require dependency removal or legal review |

## Production Checklist

- [ ] **Monorepo tooling selected** with documented rationale (tool, package manager, versioning strategy)
- [ ] **Package manager (pnpm) configured** with `pnpm-workspace.yaml`, `.npmrc` (`strict-peer-dependencies=true`), and hoisting strategy
- [ ] **Pipeline configuration** (`turbo.json` or `nx.json`) with correct `dependsOn`, `outputs`, `inputs`, and `env` for every task
- [ ] **Global dependencies** defined — `globalDependencies` (config files) and `globalEnv` (env vars) in turbo.json
- [ ] **Shared config packages** exist and are active: `typescript-config`, `eslint-config`, `prettier-config`, `jest-config`
- [ ] **Dependency boundaries enforced** via ESLint (`@nx/enforce-module-boundaries` or `import/no-restricted-paths`) — apps don't import other apps; libraries follow dependency direction
- [ ] **Circular dependency detection running in CI** — `dpdm` or `madge` as a lint step; zero cycles allowed
- [ ] **Affected-only CI operational** — PRs only rebuild/test changed packages and their dependents (Turborepo `--filter=[main...HEAD]` or Nx `affected`)
- [ ] **Remote caching configured** and working across CI agents and developer machines (Vercel, Nx Cloud, or self-hosted S3)
- [ ] **Dependency graph visualized and audited** — no circular deps, no orphans (packages with zero consumers), reasonable fan-out (< 15 consumers per package)
- [ ] **Versioning strategy chosen** (independent via Changesets recommended) and fully automated in GitHub Actions
- [ ] **Release pipeline automated**: changeset consumption → version PR → publish on merge (changesets/action)
- [ ] **Dependency version consistency enforced** with `syncpack` or `manypkg` — no version mismatches for shared deps
- [ ] **pnpm overrides / resolutions configured** for critical shared deps (React, Next, TypeScript) to enforce single versions
- [ ] **Peer dependencies correctly declared** in all shared packages — especially React, React DOM, and framework-specific packages
- [ ] **Code generation tooling configured** (Turborepo generators, Nx generators, or Plop) for new packages/components
- [ ] **Root-level scripts provide unified commands**: `pnpm dev`, `pnpm build --filter=...`, `pnpm test`, `pnpm lint`
- [ ] **CI parallelization**: matrix tests split per package with independent retry capability
- [ ] **CI uses `fetch-depth: 0`** for proper affected detection on PRs
- [ ] **PR concurrency configured**: `concurrency` + `cancel-in-progress: true` to cancel stale PR runs
- [ ] **Git hooks active**: Husky + lint-staged pre-commit (lint/format), commitlint for commit message conventions
- [ ] **VSCode workspace file** with recommended extensions, folder layout, and formatter settings committed
- [ ] **`.gitignore` covers all build outputs**: `dist/`, `.next/`, `coverage/`, `node_modules/`, `.turbo/`, `.nx/`
- [ ] **Secrets never committed**: `.env` ignored by `.gitignore`; use vault/secrets manager for environment variables
- [ ] **Backup/migration plan documented**: if gradual migration, timeline and risk mitigation are written and shared with the team

## MVP vs Growth vs Scale

| Phase | Team Size | Priority | Monorepo Approach |
|-------|-----------|----------|-------------------|
| **MVP (0→1)** | 1-3 devs | Ship fast | **Don't use a monorepo.** Single repo with `src/`, `lib/`, `app/` folders. No workspaces. No build orchestration. Just import relative paths or a single `package.json`. Monorepo tooling for 3 people is over-engineering. |
| **Growth (1→10)** | 3-15 devs, 3-8 packages | Share code without chaos | Adopt monorepo when: you have 3+ packages that share code, cross-package PRs are common, or CI is rebuilding unchanged code. pnpm workspaces + Turborepo. Start with `packages/shared-*`. |
| **Scale (10→N)** | 15+ devs, 10-100+ packages | Build speed + dependency governance | Nx or Turborepo with remote caching. Module boundary enforcement. Distributed CI. Automated dependency updates (Renovate). Code generation for package scaffolding. |

**MVP rule:** A monorepo before you have 3 packages is complexity you don't need. A `lib/` folder with relative imports works perfectly for 1-2 shared packages. Upgrade when you can answer: "What cross-package problem does a monorepo solve for us?"

## Cost-Effective Decision Table

| Decision | Free/Cheap Option | Paid Upgrade | When to Upgrade |
|----------|------------------|--------------|-----------------|
| Package manager | pnpm workspaces (free) | — | pnpm is already the best free option |
| Build orchestration | Turborepo (free OSS) | Nx Cloud or Turborepo Remote Cache ($200-$500/mo) | >5 developers, >10 packages, CI times >15 min |
| Remote cache | Local-only or S3 bucket ($1-5/mo) | Vercel Remote Cache or Nx Cloud ($200/mo+) | >5 developers sharing cache or distributed CI |
| Dependency management | Renovate (free OSS) + syncpack (free) | — | Free options are sufficient for most teams |
| Code generation | Plop or Hygen (free OSS) | Nx generators (included) | Already using Nx; otherwise Plop is fine |
| CI parallelization | GitHub Actions matrix (free for public) | BuildJet ($0.004/min) or Nx Cloud agents | Private repos with >10 min CI or need distributed execution |
| Dependency graph visualization | `nx graph` or `turbo run build --graph` (free) | Nx Cloud dependency insights | Need historical trend data or team-level views |

**Annual monorepo tool budget:** MVP: $0 (don't use one). Growth: $0-3K (CI minutes). Scale: $5K-30K (remote cache + CI).

## Scalability Decision Tree

```
Do you have 3+ packages that need to share code?
├── NO → Don't adopt a monorepo. Relative imports or npm link for 1-2 shared packages.
└── YES → Proceed.

Do cross-package PRs happen more than once per week?
├── YES → Monorepo will save time. One PR changes all packages atomically.
└── NO → Polyrepo with versioned packages may work fine.

Is CI rebuilding unchanged packages?
├── YES → This is the monorepo's superpower. Use affected-only builds.
└── NO → CI is already fast enough. Don't add tooling to solve a non-problem.

Are any packages imported by apps they shouldn't be (e.g., app-web imports app-admin)?
├── YES → Enforce module boundaries (Nx tags or ESLint rules). This is a monorepo anti-pattern.
└── NO → Clean architecture. Good.

Is one package imported by >15 other packages?
├── YES → High blast radius. Treat changes here with extra care. Consider splitting the package.
└── NO → Fan-out is healthy.

Are dependency versions consistent across all packages?
├── YES → Good. Enforce with syncpack/manypkg to keep it that way.
└── NO → Run `pnpm dedupe`. Fix mismatches. This causes runtime bugs.
```

## When NOT to Use This Skill (Overkill)

- **Single repository with <3 packages**: A monorepo is the answer to multi-package coordination. With 1 repo, 1 package, there's nothing to coordinate. Use a normal repo structure.
- **Solo developer**: Monorepo tooling exists to coordinate teams. You are one person. You don't need Turborepo, Nx, workspace protocols, or dependency boundary enforcement.
- **Packages that evolve independently with different release cycles**: If package A releases weekly and package B releases quarterly, they don't benefit from atomic commits. Polyrepo with semver is better.
- **Mixed-language projects with no shared dependency graph**: If you have a Python service and a Go service that share nothing, monorepo gives you only the downsides (large clones, slow CI) without the benefits (shared code, atomic changes).
- **You're already successfully using a polyrepo**: Don't migrate for the sake of "modern best practice." If your polyrepo CI is fast, dependencies are versioned, and devs aren't frustrated, stay put.

## Token-Efficient Workflow

```
# Step 1: Monorepo health check
python3 scripts/monorepo_health.py --root . --output json
# Returns: {"packages": 12, "circular_deps": 0, "orphans": 1,
#           "avg_dep_depth": 2.1, "packages_no_tests": 3, "build_time_cold": 180}

# Step 2: Decision tree
# circular_deps > 0 → FIX IMMEDIATELY. This breaks builds.
# orphans > 0 → Identify and remove or document intentionally unused packages.
# avg_dep_depth > 3 → Refactor. Deep dependency chains slow builds and increase blast radius.
# build_time_cold > 300 → Invest in remote caching.

# Step 3: Quick fix — check what's affected by current change
npx turbo run build --filter=[main...HEAD] --dry-run=json | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'Packages to build: {len(data[\"packages\"])}')
"

# Step 4: Verify cache hit rate
npx turbo run build --verbosity=1 2>&1 | grep -c "cache hit"
# Track: cache hit % should be >80% for developers after first build
```

**Principle:** `monorepo_health.py` analyzes package.json files and dependency graph, outputs JSON. Agent reads structured data, follows decision tree. Affected detection verified via Turborepo dry-run (exit code + JSON). Never reads individual package.json files into context.

## References

- [Monorepo Tool Comparison — Deep Dive](./references/monorepo-tool-comparison.md)
- [Turborepo — Official Documentation](https://turbo.build/repo/docs)
- [Nx — Official Documentation](https://nx.dev/getting-started/intro)
- [pnpm — Workspace Documentation](https://pnpm.io/workspaces)
- [Changesets — Release Workflow](https://github.com/changesets/changesets)
- [Bazel — Build System](https://bazel.build/)
- [Rush — Microsoft's Monorepo Manager](https://rushjs.io/)
- [manypkg — Linting for Monorepo package.json Files](https://github.com/Thinkmill/manypkg)
- [syncpack — Consistent Dependency Versions](https://jamiemason.github.io/syncpack/)
- [Husky — Git Hooks](https://typicode.github.io/husky/)
- [lint-staged — Run Linters on Git Staged Files](https://github.com/okonet/lint-staged)
- [git-filter-repo — Git History Rewriting](https://github.com/newren/git-filter-repo)
- [dpdm — Dependency Tree Analyzer](https://github.com/acrazing/dpdm)
- [Madge — Dependency Graph Visualizer](https://github.com/pahen/madge)
- [Turborepo Remote Cache — Self-Hosted Server](https://github.com/ducktors/turborepo-remote-cache)
