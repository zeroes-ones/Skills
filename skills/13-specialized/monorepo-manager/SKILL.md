---
name: monorepo-manager
description: >
  Use when designing monorepo architectures, selecting monorepo tooling, optimizing build
  orchestration, or migrating from polyrepo. Handles monorepo tooling (Turborepo, Nx, pnpm
  workspaces, Bazel, Lerna, Rush), repository structure patterns, build orchestration, dependency
  governance, CI/CD optimization, versioning strategies, and polyrepo migration. Do NOT use for
  package-level development, CI/CD pipeline construction, or individual project builds.
license: MIT
tags:
  - monorepo-manager
  - turborepo
  - nx
  - pnpm
  - bazel
  - lerna
  - build-orchestration
  - dependency-management
author: Sandeep Kumar Penchala
type: specialized
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 4000
chain:
  consumes_from: ["devops-engineer", "ci-cd-builder", "backend-developer"]
  feeds_into: ["ci-cd-builder", "backend-developer", "frontend-developer"]
---
# Monorepo Manager

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Veteran's playbook for designing, configuring, and optimizing monorepo architectures at scale. Covers every major tool in the JS/TS ecosystem — Turborepo, Nx, pnpm workspaces, Bazel, Lerna, and Rush — plus repository structure, build orchestration, dependency governance, CI/CD, versioning, and polyrepo migration.

## Route the Request
<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("pnpm-workspace.yaml")` OR `file_exists("lerna.json")` OR `file_exists("nx.json")` OR `file_exists("turbo.json")` OR `file_exists("rush.json")` OR `file_contains("package.json", "\"workspaces\"")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_exists("turbo.json")` AND `file_contains("turbo.json", "\"dependsOn\"\|\"outputs\"\|\"inputs\"")` | Jump to **Sub-Skills** — Build Orchestration (pipeline config). |
| A3 | `file_exists("pnpm-workspace.yaml")` AND `file_contains("pnpm-workspace.yaml", "packages:")` AND NOT `file_exists("turbo.json\|nx.json")` | Jump to **Decision Trees** — Tool Selection (need build orchestrator). |
| A4 | `file_contains(".github/workflows/*.yml", "affected\|--filter=\|nx affected")` | Jump to **Sub-Skills** — CI/CD for Monorepos. |
| A5 | `file_exists(".changeset/config.json")` OR `file_contains("package.json", "\"@changesets/cli\"")` | Jump to **Sub-Skills** — Versioning & Release. |
| A6 | `file_contains("package.json", "\"syncpack\"\|\"manypkg\"\|\"check-dependency-version-consistency\"")` OR `file_contains(".eslintrc*", "import/no-restricted-paths\|\"@nx/enforce-module-boundaries\"")` | Jump to **Sub-Skills** — Dependency Governance & Package Boundary Enforcement. |
| A7 | `file_contains("*.yml", "git subtree\|git filter-repo\|git submodule\|polyrepo")` AND `file_contains("*.md", "monorepo\|mono.repo\|migrate")` | Jump to **Sub-Skills** — Monorepo Migration (polyrepo → monorepo). |
| A8 | `file_exists("WORKSPACE")` OR `file_exists("BUILD.bazel\|BUILD")` OR `file_contains("*", "bazel build\|bazel test")` | This is a Bazel monorepo — jump to **Tool Selection & Decision Matrix** — Bazel row. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Choose monorepo tooling (Turborepo/Nx/pnpm/Bazel/Lerna/Rush) → Jump to "Tool Selection & Decision Matrix"
├── Design repository structure and package boundaries → Jump to "Sub-Skills" — Workspace Configuration
├── Set up build orchestration with caching and affected detection → Jump to "Sub-Skills" — Build Orchestration
├── Enforce dependency governance and prevent circular dependencies → Jump to "Sub-Skills" — Dependency Governance
├── Optimize CI/CD — affected-only builds, remote caching, parallel jobs → Jump to "Sub-Skills" — CI/CD for Monorepos
├── Set up versioning and release workflow with Changesets → Jump to "Sub-Skills" — Versioning & Release
├── Migrate from polyrepo to monorepo → Jump to "Sub-Skills" — Monorepo Migration
├── Need CI/CD pipeline setup first → Invoke ci-cd-builder skill instead
└── Not sure? → Describe your team size, package count, and current pain points
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else
<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to recommend a monorepo for < 3 packages sharing code.** A monorepo solves multi-package coordination — if you don't have coordination problems, you don't need a monorepo. | Trigger: `find . -name "package.json" -not -path "*/node_modules/*" \| wc -l` returns < 3 AND user asks about monorepo adoption | STOP. Respond: "You have fewer than 3 packages. A `lib/` or `packages/` folder with workspace references is sufficient. Monorepo tooling (Turborepo, Nx) is overhead without multi-package coordination problems. Do you have cross-package PRs weekly?" |
| **R2** | **REFUSE to set up a monorepo without build caching.** Without remote caching, CI times grow linearly with package count. A 50-package monorepo without caching = 50-minute CI builds. | Trigger: `turbo.json` or `nx.json` exists but `grep -rn "remoteCache\|REMOTE_CACHE\|Nx Cloud\|vercel.*cache" --include="*.json" --include="*.yml" .` returns 0 | STOP. Respond: "Build caching is not optional. Configure remote caching: S3 bucket ($5/mo), Vercel Remote Cache, or Nx Cloud. Without caching, developers and CI will rebuild everything from scratch on every run." |
| **R3** | **STOP and ASK about package boundaries before creating packages.** Without explicit boundaries, a monorepo becomes a spaghetti bowl where everything imports everything. | Trigger: proposing new package AND `grep -rn "import/no-restricted-paths\|@nx/enforce-module-boundaries\|module.boundar" --include="*.js" --include="*.json" .` returns 0 | STOP. Ask: "What are the package boundaries? Which packages can import from which? Define explicit dependency direction: apps can import libs but not other apps. Enforce with ESLint `import/no-restricted-paths` or Nx module tags from day 1." |
| **R4** | **DETECT and WARN about circular dependencies.** Circular deps break tree-shaking, cause runtime errors, and make dependency graphs impossible to reason about. Zero tolerance. | Trigger: `npx dpdm --circular --tree=false "packages/**/*.ts" 2>&1 \| grep -c "circle"` returns > 0 OR `npx madge --circular --extensions ts,tsx packages/` finds cycles | WARN: "Circular dependencies detected. Run `npx madge --circular --extensions ts,tsx packages/` to see them. Break cycles by extracting shared code to a lower-level package or inverting the dependency. Never merge circular deps." |
| **R5** | **DETECT and WARN about version mismatches for shared dependencies.** Two packages depending on conflicting React/TypeScript versions cause runtime errors that are nearly impossible to debug. | Trigger: `npx syncpack list-mismatches 2>&1 \| grep -c "✘"` returns > 0 OR `grep -rn "\"react\":\|\"typescript\":" packages/*/package.json \| awk -F: '{print $NF}' \| sort -u \| wc -l` returns > 1 for any shared dep | WARN: "Version mismatches found for shared dependencies. Run `npx syncpack fix-mismatches` to align versions. Add `npx syncpack list-mismatches` to CI lint step. Mismatched React versions cause 'works on my machine' bugs." |
| **R6** | **STOP and ASK before using wildcard workspace globs.** `packages/*` includes everything — test fixtures, build outputs, abandoned experiments. Every package in the workspace pays the install cost. | Trigger: `grep -rn "packages/\*\|\"packages/\*\"" pnpm-workspace.yaml\|package.json` returns a match with no `!packages/` exclusions | STOP. Ask: "Your workspace glob matches every directory. Are there test fixtures, build outputs, or abandoned packages included? Add exclusions: `!packages/e2e` and list packages explicitly if < 10." |
| **R7** | **REFUSE to migrate to a monorepo without benchmarking CI time before and after.** If migration makes CI slower for any team, the migration is NOT complete. Monorepo must make development faster, not just more centralized. | Trigger: monorepo migration proposed AND no CI benchmark data: `grep -rn "benchmark\|CI.time\|build.*before\|build.*after" migration-plan.md \| wc -l` returns 0 | STOP. Respond: "Benchmark before migration: `git clone`, install, build, test for each repo. Set targets for the monorepo: clone < 90s, install < 60s, affected build < 3min. Migration isn't done until CI is FASTER than before." |
## The Expert's Mindset

Masters of monorepo manager don't just build — they build **the right thing, at the right time, with the right trade-offs**. They think in systems, not tasks.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Shiny object syndrome** — chasing new tools without evaluating fit | Before adopting any new tool, write the "why this over the incumbent" justification |
| **Over-engineering** — building for hypothetical scale | Default to simplest solution; add complexity only when the current solution actually breaks |
| **Not-invented-here** — preferring to build rather than compose | Always evaluate 2 existing solutions before building custom |
| **Sunk cost fallacy** — sticking with a technology because you already invested in it | Re-evaluate tech choices every quarter; migration cost vs. staying cost |

### What Masters Know That Others Don't
- The **failure modes** of every component in their stack — not just the happy path
- When **not** to use their favorite tool (every tool has a misuse zone)
- That **data/model quality decays over time** — monitoring is not optional, it's foundational

### When to Break Your Own Rules
- **Move fast on reversible decisions.** Data format? Hard to change. Dashboard layout? Easy. Know the difference.
- **Skip the abstraction until the third use case.** Two is coincidence, three is a pattern.
## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single component/module | Implement a well-defined piece following established patterns |
| **L2** | Feature or service | Design and build a complete feature; make tech choices within team conventions |
| **L3** | System or product area | Define architecture for a product area; set team tech standards; mentor L1-L2 |
| **L4** | Multiple systems / platform | Define org-wide architecture patterns; make build-vs-buy decisions; influence industry practice |
| **L5** | Industry / ecosystem | Create new architectural patterns adopted across the industry; redefine what's possible |

**Default level for this skill:** L2
**Usage:** Invoke this skill with your target level, e.g., "as an L3 monorepo manager, design..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

- You are choosing a monorepo tool (Turborepo vs. Nx vs. Bazel vs. pnpm workspaces) and need a comparison matrix
- You need to configure build orchestration — task pipelines, caching, parallel execution, and affected detection
- Your monorepo CI is slow and you need to set up remote caching, incremental builds, and matrix-based pipelines
- You are enforcing dependency governance — version consistency, hoisting rules, and peer dependency resolution
- You need to detect and prevent circular dependencies or enforce package boundary rules between modules
- You are setting up versioning and release workflows with Changesets, independent versioning, and changelog generation
- You are migrating from polyrepo to monorepo and need a strategy for history preservation and gradual adoption
- Your monorepo has grown to 50+ packages and you need to refactor the structure, tooling, or dependency graph


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | system-architect | Software architecture, module boundaries, dependency graph, technology stack decisions |
| **This** | monorepo-manager | Repository structure, build orchestration config, dependency governance rules, CI/CD pipeline |
| **After** | ci-cd-builder | Optimized CI pipelines with caching, affected detection, and parallel builds |

Common chains:
- **Chain**: system-architect → monorepo-manager → ci-cd-builder — Architect defines module boundaries; monorepo manager implements them in tooling; CI/CD builder optimizes the pipeline.
- **Chain**: devops-engineer → monorepo-manager → frontend-developer — DevOps provisions infrastructure; monorepo manager configures the workspace; frontend dev benefits from shared tooling and fast builds.

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
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

> **Token-saving rule:** Load sub-skill references on demand. If <!-- DEEP: 10+min -->
debugging cache misses → only read the build orchestration section. If setting up CI → only read the CI/CD section.

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

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### 1. Monorepo Tool Selection
```
                     ┌────────────────────────┐
                     │ START: What's your     │
                     │ primary stack?         │
                     └───────────┬────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
    ┌─────▼──────┐       ┌───────▼───────┐       ┌──────▼──────────┐
    │ JavaScript │       │ Polyglot      │       │ Mobile + Web    │
    │ / Type-    │       │ (JS + Python  │       │ (React Native   │
    │ Script     │       │ + Go + etc.)  │       │ + Web)          │
    └─────┬──────┘       └───────┬───────┘       └──────┬──────────┘
          │                      │                      │
    ┌─────▼──────────┐   ┌───────▼───────┐       ┌──────▼──────────┐
    │ <15 packages?  │   │ Bazel or      │       │ Nx with         │
    └──┬─────────┬───┘   │ Pantsbuild.   │       │ @nx/react-native│
       │YES      │NO     │ Best for      │       │ + @nx/web.      │
  ┌────▼────┐ ┌──▼─────┐ │ multi-lang    │       │ Excellent       │
  │ pnpm    │ │ Turbore│ │ + monorepo.   │       │ React Native    │
  │ works-  │ │ po or  │ └───────────────┘       │ monorepo        │
  │ paces   │ │ Nx     │                         │ support.        │
  └─────────┘ └────────┘                         └─────────────────┘
```
**pnpm workspaces alone:** <15 packages, simple dependency graph, no build orchestration needed.  
**Turborepo:** JS/TS, need parallel task execution + caching. Lighter than Nx.  
**Nx:** JS/TS, need generators, plugin ecosystem, advanced affected detection, or mobile+web.  
**Bazel/Pants:** Polyglot (JS + Python + Go + Rust), large org, need reproducible builds.

### 2. Package Boundary Decision
```
                  ┌──────────────────────────┐
                  │ START: Will this package │
                  │ be consumed externally?  │
                  └───────────┬──────────────┘
                              │
                   ┌──────────▼──────────┐
                   │ YES → Publishable   │
                   │ package. Strict API │
                   │ via `exports` field.│
                   │ Semantic versioning │
                   │ with Changesets.    │
                   └─────────────────────┘
                   ┌──────────▼──────────┐
                   │ NO → Internal-only? │
                   └────┬───────────┬────┘
                        │YES        │NO
                   ┌────▼────┐ ┌───▼──────────┐
                   │ `"private│ │ Extract to   │
                   │ ": true` │ │ separate repo│
                   │ in       │ │ with its own │
                   │ package. │ │ CI/CD +      │
                   │ json.    │ │ release cycle│
                   │ No semver│ └──────────────┘
                   │ needed.  │
                   └──────────┘
```
**Published externally → strict `exports` field, semver, Changesets.**  
**Internal shared code → `"private": true`, no versioning overhead.**  
**Truly independent → separate repo. Don't force into monorepo if it ships independently.**

### 3. Versioning Strategy
```
                   ┌──────────────────────────┐
                   │ START: Are packages      │
                   │ coupled (always release  │
                   │ together)?               │
                   └───────────┬──────────────┘
                               │
                    ┌──────────▼──────────┐
                    │ YES → Fixed/Locked  │
                    │ versioning. Single  │
                    │ version bump for    │
                    │ all packages.        │
                    └─────────────────────┘
                    ┌──────────▼──────────┐
                    │ NO → Independent    │
                    │ versioning with     │
                    │ Changesets. Each    │
                    │ package versioned   │
                    │ by its own changes. │
                    └─────────────────────┘
```
**Fixed/Locked:** All packages share one version. Use when packages are tightly coupled (e.g., React + ReactDOM).  
**Independent with Changesets:** Each package versioned independently. Use when packages have different release cadences.

### 4. Migration Path: Polyrepo → Monorepo
```
                  ┌──────────────────────────┐
                  │ START: How many repos    │
                  │ are you merging?         │
                  └───────────┬──────────────┘
                              │
                   ┌──────────▼──────────┐
                   │ <5 repos, <500K     │
                   │ LOC total?          │
                   └────┬───────────┬────┘
                        │YES        │NO
                   ┌────▼────┐ ┌───▼──────────┐
                   │ Big-bang│ │ Gradual      │
                   │ merge   │ │ adoption:    │
                   │ over a  │ │ start with   │
                   │ weekend.│ │ shared config │
                   │ Use     │ │ + utilities. │
                   │ git-    │ │ Add packages │
                   │ subtree │ │ incrementally│
                   │ merge.  │ │ over weeks.  │
                   └─────────┘ └──────────────┘
```
**<5 repos → big-bang over a weekend.** Use subtree merge strategy to preserve history.  
**>5 repos or >500K LOC → gradual adoption.** Start with shared configs and utilities; add one repo at a time.

### 5. CI/CD Affected Detection
```
                   ┌──────────────────────────┐
                   │ START: PR changes files  │
                   │ in which packages?       │
                   └───────────┬──────────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Run affected graph  │
                    │ detection (Nx       │
                    │ affected / Turborepo│
                    │ --filter)           │
                    └────┬───────────┬────┘
                         │           │
                    ┌────▼────┐ ┌───▼──────────┐
                    │ Root    │ │ Only changed │
                    │ config  │ │ packages +   │
                    │ changed?│ │ their         │
                    └──┬───┬──┘ │ dependents    │
                       │YES│NO  │ are built/    │
                  ┌────▼─┐┌▼────┐│ tested.      │
                  │ Build││Build│└──────────────┘
                  │ all  ││ only│
                  │pack- ││aff- │
                  │ ages ││ected│
                  └──────┘└─────┘
```
**Root config change (tsconfig/eslint/CI) → build ALL packages.**  
**Package-level change → build only changed + dependents. Dramatically reduces CI time.**

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): Repository Setup and Tool Selection
1. Assess current state: number of packages, team size, build times, CI bottlenecks, polyglot requirements.
2. Choose toolchain using the Decision Matrix above: Turborepo (fastest setup) vs Nx (most features) vs Bazel (polyglot/hermetic).
3. Initialize workspace: `pnpm-workspace.yaml` with package globs, root `package.json` with dev tooling only.
4. Configure shared tooling: TypeScript base config, ESLint, Prettier, Jest/Vitest — all as shared packages.
5. Set up the repository structure: `apps/` for deployables, `packages/` for libraries, `tools/` for generators/scripts.

<!-- DEEP: 10+min -->
### Phase 2 (~20 min): Dependency Governance
1. Install dependencies at the correct level: framework/runtime deps in each package, dev tooling in root.
2. Configure `pnpm.overrides` or `resolutions` to force single versions of critical dependencies (React, TypeScript, etc.).
3. Run `syncpack` or `manypkg` to detect version mismatches across packages. Set up CI check.
4. Enable `strict-peer-dependencies` in `.npmrc` to catch peer dependency violations at install time.
5. Detect circular dependencies with `dpdm` or `madge`. Break cycles before they become entrenched.

<!-- DEEP: 10+min -->
### Phase 3 (~25 min): Build Orchestration and Caching
1. Design the task pipeline: `turbo.json` or `nx.json` with `dependsOn` topology (e.g., `build` depends on `^build`).
2. Configure remote caching: Vercel (Turborepo), Nx Cloud, or S3-backed custom cache. This is the #1 CI speedup.
3. Set up local caching: enable filesystem cache in CI with restore/save pattern. Use `--cache-dir` for CI isolation.
4. Define `outputs` per task: `.next/**`, `dist/**`, `coverage/**`. Without outputs defined, caching doesn't work.
5. Measure: `turbo run build --dry-run=json` or `nx graph` to verify task topology before committing.

<!-- DEEP: 10+min -->
### Phase 4 (~20 min): CI/CD Pipeline
1. Implement affected detection: `--filter=[base...HEAD]` in CI to only build/test changed packages.
2. Configure GitHub Actions matrix builds: spawn one job per affected package, converge for integration tests.
3. Set up cache warming: build `main` branch on push to warm the remote cache for all PRs.
4. Add dependency boundary checks: `@nx/enforce-module-boundaries` or ESLint `import/no-restricted-paths`.
5. Implement merge queue: require green CI on all affected packages before merge. No "skip CI" on monorepo PRs.

<!-- DEEP: 10+min -->
### Phase 5 (~15 min): Versioning and Release
1. Choose versioning strategy: independent (each package versions separately) vs fixed (all packages share one version).
2. Set up Changesets: `@changesets/cli` for changelog generation, version bumping, and publishing.
3. Configure release workflow: GitHub Action that runs `changeset version` on merge to main, creates Release PR.
4. Publish to registry: `changeset publish` with `--no-private` to skip non-publishable packages.
5. Automate changelog: link to PRs, categorize changes (feat/fix/breaking), notify affected teams.

## Build System & CI/CD

Deep dives on task orchestration, caching architecture, and CI/CD pipelines are in **[references/monorepo-tooling.md](references/monorepo-tooling.md)**:

| Section | What's Covered |
|---------|---------------|
| **Task Orchestration** | Turborepo pipeline config, Nx task executor, pnpm workspace protocols, parallel vs sequential execution strategies |
| **Caching Architecture** | Local + remote caching (Nx Cloud, Turborepo Remote Cache), hash computation (inputs/outputs), cache invalidation rules, what to cache/not cache |
| **CI/CD** | Affected detection (build only what changed), GitHub Actions pipeline with remote caching, remote cache strategies (S3, GCS), CI cache optimization, parallel pipeline strategies (fan-out per package) |

**Quick Reference:**
- **Local dev:** `turbo dev --filter=@myorg/web` — runs only web + dependencies
- **CI affected:** `turbo build --filter=[origin/main...HEAD]` — builds only changed packages
- **Remote cache:** Cut CI times 60-90% with shared read/write cache across CI runs

## Dependency Management & Package Architecture

Deep dives on dependency strategies, package boundaries, versioning, and migration are in **[references/monorepo-patterns.md](references/monorepo-patterns.md)**:

| Section | What's Covered |
|---------|---------------|
| **Dependency Management** | Hoisting strategies (auto vs strict), version consistency tools (syncpack, manypkg), peer dependency resolution, depcheck/audit commands |
| **Code Sharing & Boundaries** | Barrel exports pattern, package boundary enforcement (ESLint import rules, module tags), circular dependency detection (madge, dpdm) |
| **Version Management** | Independent vs fixed versioning, Changesets workflow with CLI commands, semantic-release in monorepos, release pipeline summary |
| **Migration Path** | Polyrepo→monorepo strategy, big-bang (subtree merge), gradual adoption step-by-step, git history preservation, risk mitigation |
| **Developer Experience** | Local dev setup, shared ESLint/TS config, VSCode workspace config, Git hooks (Husky + lint-staged), editor integration |

**Quick Reference:**
- **Hoisting:** `"hoist": true` in `.npmrc` unless you have conflicting peer deps
- **Version sync:** `syncpack list-mismatches` in CI — fail on any discrepancy
- **Circular deps:** `madge --circular packages/` — zero tolerance policy
- **New package:** `pnpm exec changeset` → describe change → commit → CI auto-opens Release PR
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


**What good looks like:** `npm run build -- --filter=[changed]` completes in under 3 minutes. Remote cache hit rate > 70%. CI pipeline runs only affected projects. Developer onboarding to add a new package is documented and takes < 30 minutes.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Monorepo management touches every development team. A monorepo tooling change affects everyone's daily workflow — coordination isn't optional.

### Decision Gates & Artifacts

- **Gate 1 — Infrastructure Ready:** Monorepo tooling requires CI/CD infrastructure and caching layers provisioned by `devops-engineer`. Artifact: infrastructure readiness checklist.
- **Gate 2 — CI/CD Pipeline Defined:** Build orchestration depends on pipeline configuration from `ci-cd-builder`. Artifact: turbo.json or nx.json with task pipelines.
- **Gate 3 — Project Structures Defined:** Workspace configuration requires backend and frontend project structures from `backend-developer` and `frontend-developer`. Artifact: workspace boundary map.
- **Gate 4 — Dependency Governance Enforced:** Package boundaries and dependency rules validated across all consumer teams. Artifact: dependency graph audit with zero circular deps.
- **Artifact:** Monorepo tooling selection rationale, workspace configuration (pnpm-workspace.yaml, turbo.json), dependency graph visualization.

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


## Error Decoder
<!-- DEEP: 5min -- each entry includes a console-string matcher for automatic recovery loops -->

| 🖥️ Console Match (grep pattern) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|---|---|---|---|---|
| `Error: cache miss on all tasks\|FULL TURBO.*0%\|remote cache disabled` + `npx turbo run build --dry-run=json 2>&1 \| jq '.packages \| length'` > 5 AND `grep -c "\"remoteCache\"" turbo.json` returns 0 | CI builds take 25+ minutes — every PR rebuilds all packages from scratch regardless of what changed | No remote caching configured. Each CI agent starts with a cold cache. With 15 packages, each one rebuilds on every PR even if only 1 package changed | Configure remote caching: S3 bucket (`turbo.json` → `"remoteCache": {"signature": true}` + env vars), Vercel Remote Cache, or Nx Cloud. Verify: `npx turbo run build --remote-only 2>&1 \| grep "cache hit"` should show cache hits on second run | 1. Check cache state: `npx turbo run build --dry-run=json \| jq '.tasks[].cache.state' \| sort \| uniq -c` 2. If all `local: false, remote: false`, set up S3 cache: `aws s3 mb s3://turborepo-cache` + set `TURBO_TOKEN`, `TURBO_TEAM`, `TURBO_REMOTE_CACHE_URL` 3. Run first build (populate cache): `npx turbo run build` 4. Run second build (should be all cache hits): `npx turbo run build --verbosity=1 2>&1 \| grep "cache hit" \| wc -l` 5. CI: add cache warm/restore steps before `turbo run` |
| `Error: Cannot find module '@org/shared'\|Module not found: Error: Can't resolve '@org/shared'` + `grep -c "\"workspace:\*\|\"workspace:\^" packages/*/package.json` returns 0 | Package A imports from `@org/shared` but installs a stale npm-published version instead of the local workspace version | Cross-package dependencies use `"@org/shared": "^1.0.0"` instead of `"workspace:*"`. pnpm installs from the npm registry (stale version) instead of linking to the local package | Use `workspace:*` protocol for all cross-package deps: `"@org/shared": "workspace:*"`. This tells pnpm to always link to the local package. Verify: `pnpm list --depth=0 --recursive \| grep "@org/shared"` — must show `link:../shared` | 1. Find non-workspace internal deps: `grep -rn "\"@org/" packages/*/package.json \| grep -v "workspace:"` 2. Replace each: `"@org/shared": "^1.0.0"` → `"@org/shared": "workspace:*"` 3. Reinstall: `rm -rf node_modules pnpm-lock.yaml && pnpm install` 4. Verify linkage: `ls -la node_modules/@org/shared` → must be symlink to `packages/shared` 5. CI lint: `scripts/check-workspace-protocols.sh` — fails if any `@org/*` dep doesn't use `workspace:*` |
| `Error: Task graph cycle detected\|circular dependency detected\|dependency cycle` + `npx madge --circular --extensions ts,tsx packages/ 2>&1` shows A → B → A | Package A imports from Package B, and Package B imports from Package A — neither can build first, both fail | Someone added a cross-import without checking the dependency graph. Common cause: shared types in Package A imported by Package B, but Package B's utilities imported by Package A | Break the cycle: extract the shared dependency into a lower-level package C. A → C and B → C (never A ↔ B). Use `dpdm --circular --tree=false` to detect before commit | 1. Detect cycle: `npx madge --circular --extensions ts,tsx packages/` 2. Identify shared imports in both directions: `npx dpdm packages/A/src/index.ts --circular` 3. Extract shared code to new package: `mkdir packages/shared-types` with its own `package.json` 4. Update both A and B to import from `@org/shared-types` instead of each other 5. Verify no cycles: `npx madge --circular --extensions ts,tsx packages/` → must return no output 6. CI: `npx madge --circular --extensions ts,tsx packages/` as lint step — fails if cycles found |
| `Error: Invalid hook call\|React version mismatch\|multiple copies of React` + `pnpm why react --recursive 2>&1 \| grep "version" \| sort -u \| wc -l` returns > 1 | React hooks throw "Invalid hook call" — multiple versions of React loaded in the bundle | Hoisting resolved React to different versions for different packages. Package A uses React 18.2.0 (hoisted), Package B uses React 18.3.1 (nested in its own node_modules). At runtime, two React instances exist | Force single version: add to root `package.json` → `"pnpm": {"overrides": {"react": "18.2.0", "react-dom": "18.2.0"}}`. Verify with `pnpm why react --recursive` — should show one version. Run `pnpm install --force` | 1. Audit versions: `pnpm why react --recursive 2>&1 \| grep "version:" \| sort \| uniq -c` 2. If > 1 version, add overrides: `pnpm.overrides.react = "18.2.0"` in root `package.json` 3. Clean install: `rm -rf node_modules packages/*/node_modules pnpm-lock.yaml && pnpm install` 4. Verify single version: `find . -path "*/node_modules/react/package.json" -exec jq -r '"{}: " + .version' {} \; \| sort -u` → must be 1 entry 5. CI: `scripts/check-react-singleton.sh` — fails if multiple React versions detected |
| `Error: CI concurrency: cancel-in-progress killed all jobs\|stale PR runs queued for 20 minutes` + `grep -c "concurrency:" .github/workflows/*.yml` returns 0 | Developer pushes 3 commits in 5 minutes — CI queues 3 builds for 73 packages each. 219 builds in queue, latest push waits 45 minutes | No concurrency control. Every push triggers a full CI run. Without `cancel-in-progress: true`, stale runs consume queue slots and block the latest commit | Add to every CI workflow: `concurrency: {group: ${{ github.workflow }}-${{ github.ref }}, cancel-in-progress: true}`. This cancels stale runs when a new commit is pushed to the same PR/branch | 1. Check current concurrency: `grep -rn "concurrency:" .github/workflows/*.yml` 2. If missing, add to each workflow YAML: `concurrency: group: ci-${{ github.ref }}, cancel-in-progress: true` 3. Also set `fetch-depth: 0` for affected detection: `actions/checkout@v4 with: fetch-depth: 0` 4. Verify: push 2 commits quickly to a PR — second commit should cancel first CI run 5. Monitor: `gh run list --workflow=ci --branch=feature-branch \| head -5` — should show only the latest run as active |
| `Error: pnpm install: ENOENT\|pnpm-lock.yaml out of date\|ERR_PNPM_OUTDATED_LOCKFILE` + `git diff --name-only HEAD~1 \| grep "pnpm-lock.yaml"` on every unrelated PR | Every PR has merge conflicts in `pnpm-lock.yaml` — 12K-line lockfile changed on every dependency update | `pnpm-lock.yaml` changes on every `pnpm install` even for unrelated dependency updates. In a monorepo with Renovate/Dependabot, the lockfile changes continuously | Accept `pnpm-lock.yaml` changes from Renovate PRs and use merge queues. Don't require lockfile review — use `pnpm install --frozen-lockfile` in CI to validate. For merge conflicts: always regenerate from latest main | 1. Use merge queue: GitHub Settings → "Require merge queue" on main branch 2. CI: `pnpm install --frozen-lockfile` to validate lockfile, never regenerate in CI 3. Auto-merge lockfile-only PRs: Renovate config → `"lockFileMaintenance": {"automerge": true}` 4. For manual conflicts: `git checkout main -- pnpm-lock.yaml && pnpm install && git add pnpm-lock.yaml` 5. Pre-commit: `scripts/check-lockfile.sh` — warns if lockfile changed but no `package.json` changed (unexpected lockfile churn) |

## Proactive Triggers
<!-- QUICK: 30s — when to proactively notify stakeholders -->

| Trigger | Notify | Why |
|---------|--------|-----|
| Circular dependency detected by CI lint step | System Architect, Affected Package Owners | Build-breaking architecture violation; immediate refactor required |
| Build times increase >30% in any pipeline week-over-week | DevOps, DX, Engineering Leads | Developer productivity degradation; cache or pipeline investigation needed |
| Shared package release with breaking change (major version bump) | All Consumer Teams, System Architect | Migration guide needed; all consumers must update imports/APIs |
| Dependency version conflict between two workspaces (different React/TypeScript versions) | Affected Teams, DX | Runtime errors possible; syncpack override or version alignment required |
| Flaky test rate exceeds 5% in shared package test suite | QA, Package Owners | CI trust eroding; test quarantine, fix, or removal decision needed |
| Orphan package detected (zero consumers, zero imports) | Package Owner, System Architect | Unmaintained code in repo; removal or documentation of purpose required |
| Monorepo tool migration proposed (Lerna→Nx, Yarn→pnpm) | All Teams, DevOps, DX, CTO Advisor | 2-4 week migration window; training, CI reconfiguration, and workflow changes needed |

## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | Workspace configured — `pnpm-workspace.yaml` with explicit package paths, `.npmrc` with `strict-peer-dependencies=true` and `hoist=true` | `pnpm list --depth=0 --recursive 2>&1 \| grep -c "ERR_PNPM"` → must return 0 | `pnpm install --frozen-lockfile` in CI; any drift fails the build |
| **[S2]** | Build orchestrator configured — `turbo.json` or `nx.json` with correct `dependsOn`, `outputs`, `inputs`, and `env` for every task | `npx turbo run build --dry-run=json 2>&1 \| jq '.tasks \| length'` → must be > 0 | Template: `templates/turbo.json` with pre-configured pipelines for build, test, lint, typecheck |
| **[S3]** | Affected-only CI operational — PRs only rebuild/test changed packages and their dependents | `npx turbo run build --filter=[main...HEAD] --dry-run=json \| jq '.packages \| length'` → must be LESS THAN total package count | CI: `turbo run build test lint --filter=[${{ github.base_ref }}...HEAD]` in workflow plus `fetch-depth: 0` |
| **[S4]** | Remote caching configured and verified — cache hits > 80% on second run | `npx turbo run build --verbosity=1 2>&1 \| grep -c "cache hit"` → must be > 80% of total tasks on second run | S3 cache: `turbo.json` → `"remoteCache": {}` + `TURBO_TOKEN` + `TURBO_REMOTE_CACHE_URL` env vars |
| **[S5]** | Circular dependencies enforced — zero tolerance; CI fails if any cycle detected | `npx madge --circular --extensions ts,tsx packages/ 2>&1 \| grep -c "✖"` → must return 0 | CI lint: `npx madge --circular --extensions ts,tsx packages/` as required step before build |
| **[S6]** | Package boundaries enforced — apps cannot import other apps; libraries follow dependency direction | `npx eslint packages/ --rule '{"import/no-restricted-paths": ["error", {"zones": [{"target": "./packages/apps/", "from": "./packages/apps/"}]}]}' 2>&1 \| grep -c "error"` → must return 0 | ESLint config: `import/no-restricted-paths` rules for each app boundary; Nx: `@nx/enforce-module-boundaries` in `.eslintrc.json` |
| **[S7]** | Cross-package dependencies use `workspace:*` protocol — never a published version number | `grep -rn "\"@org/" packages/*/package.json \| grep -v "workspace:" \| wc -l` → must return 0 | Script: `scripts/fix-workspace-protocols.sh` — replaces `"@org/package": "^X.Y.Z"` with `"@org/package": "workspace:*"` in all `package.json` files |
| **[S8]** | Version consistency enforced — shared dependencies (React, TypeScript, Next.js) have single version across all packages | `npx syncpack list-mismatches 2>&1 \| grep -c "✘"` → must return 0 | CI: `npx syncpack list-mismatches` as lint step. Fix: `npx syncpack fix-mismatches && pnpm install` |
| **[S9]** | pnpm overrides configured for critical shared dependencies — React, React DOM, TypeScript, Next.js | `grep -c "\"pnpm\".*\"overrides\"" package.json` → must be ≥ 1 with at least React and TypeScript entries | Add to root `package.json`: `"pnpm": {"overrides": {"react": "18.2.0", "react-dom": "18.2.0", "typescript": "5.3.0"}}` |
| **[S10]** | Changesets configured for versioning — `npx changeset version` generates bump PR with changelogs | `test -d .changeset && test -f .changeset/config.json && echo "OK"` → must return "OK" | `pnpm add -Dw @changesets/cli && npx changeset init` then configure `.changeset/config.json` with `"baseBranch": "main"` and `"commit": false` |
| **[S11]** | Release pipeline automated — changeset consumption → version PR → publish on merge | `grep -rn "changesets/action\|changeset.*version\|changeset.*publish" .github/workflows/*.yml \| wc -l` → must be ≥ 1 | GitHub Actions: `changesets/action@v1` with `publish: pnpm release` and `version: pnpm changeset version` |
| **[S12]** | Git hooks active — commitlint for message conventions, lint-staged for pre-commit lint/format | `grep -c "\"husky\"\|\"lint-staged\"\|\"commitlint\"" package.json` → must be ≥ 2 (at least 2 of 3 configured) | `pnpm add -Dw husky lint-staged @commitlint/cli @commitlint/config-conventional && npx husky init` + add `commit-msg` and `pre-commit` hooks |

## Scale Depth
<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person) → Small (2-10) → Medium (10-50) → Enterprise (50+)

| Dimension | Solo | Small | Medium | Enterprise |
|-----------|------|-------|--------|------------|
| **Repo Structure** | Single repo, `src/` + `lib/` folders | pnpm workspaces + Turborepo, 3-15 packages | Nx/Turborepo + remote caching, 15-100 packages | Nx/Bazel + distributed CI, 100+ packages |
| **Build System** | No orchestration, just `pnpm build` | Turborepo with local caching | Remote caching (Nx Cloud/S3), affected-only CI | Distributed build agents, multi-region caching |
| **Dependency Mgmt** | Single `package.json` | pnpm + syncpack version enforcement | Renovate + automated dep updates | Custom package registry + dependency governance board |
| **Package Boundaries** | No enforcement needed | ESLint import rules | Nx module tags + lint rules | Automated boundary enforcement + architecture fitness functions |
| **Versioning** | `npm version patch` | Changesets with independent versioning | Automated release PRs + changelogs | Semantic-release per package + multi-channel releases |
| **CI/CD** | Build all on push | Affected-only builds | Remote cache + parallel pipelines | Distributed CI with Nx Cloud agents or BuildJet |
| **Developer Experience** | VS Code, single config | Shared ESLint/TS config | VSCode workspace + git hooks | Automated generator scripts for new packages |

### Transition Triggers

| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo → Small | 3+ packages sharing code, cross-package PRs weekly | Adopt pnpm workspaces + Turborepo, set up shared configs |
| Small → Medium | >10 packages, CI >15 min, >5 developers | Remote caching, affected-only CI, module boundary enforcement |
| Medium → Enterprise | >100 packages, multi-team, CI >30 min | Distributed CI, architecture governance, automated package scaffolding |

## What Good Looks Like

> When monorepo management is optimized, CI only builds and tests packages affected by each change, remote caching delivers sub-5-minute CI for most PRs, circular dependencies are caught at lint time with zero tolerance, package boundaries are enforced so teams own their domains without friction, dependency versions are kept consistent across all packages, and new developers scaffold a working dev environment in under 10 minutes — the monorepo is a force multiplier, not a bottleneck.

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

## Best Practices
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

## Anti-Patterns
<!-- DEEP: 5min -- each anti-pattern includes machine-detectable patterns -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| Every PR rebuilds all packages regardless of what changed — CI time grows linearly with package count | Implement affected-only detection: `turbo build --filter=[main...HEAD]` or `nx affected:build`. With 20 packages changing 1, CI should build 1 package + its dependents (~3-5 total). | `grep -c "\--filter=\|affected" .github/workflows/ci.yml` → must be ≥ 1. If 0, no affected detection in CI | CI template: `templates/ci-affected.yml` with `turbo run build test lint --filter=[${{ github.base_ref }}...HEAD]` |
| No package boundary enforcement — any package can import any other, spaghetti dependency graph within weeks | ESLint `import/no-restricted-paths` or Nx module tags from day 1. CI fails on boundary violations. Define explicit dependency direction: apps can import libs, not other apps. | `grep -rn "import/no-restricted-paths\|@nx/enforce-module-boundaries\|module.boundar" --include="*.js" --include="*.json" . \| wc -l` → must be ≥ 1 | Add to `.eslintrc.js`: `'import/no-restricted-paths': ['error', { zones: [{ target: './packages/apps/', from: './packages/apps/', message: 'Apps cannot import other apps' }] }]` |
| Manual version bumps with `npm version` in each package — inevitably forget one package, changelogs diverge | Use Changesets: `pnpm exec changeset` → describe change → CI opens Release PR with all version bumps and changelogs automatically computed from the dependency graph. | `grep -rn "\"version\"\s*:" packages/*/package.json \| wc -l` vs `grep -c "\"@changesets/cli\"" package.json` → if packages > 5 and no changesets, manual versioning pain ahead | `pnpm add -Dw @changesets/cli && npx changeset init` + GitHub Actions workflow: `changesets/action@v1` |
| Skipping remote caching because "local cache is fast enough" — each CI agent and developer rebuilds from scratch | S3 bucket remote cache costs < $5/month. 80%+ cache hit rate. Pays for itself in developer time in days. Configure via Turborepo: `turbo.json` → `"remoteCache": {}` | `npx turbo run build --verbosity=1 2>&1 \| grep "cache miss" \| wc -l` → if > 50% on CI, remote cache not configured or not working | S3 setup: `aws s3 mb s3://turbo-repo-cache` → set `TURBO_REMOTE_CACHE_URL`, `TURBO_TOKEN`, `TURBO_TEAM` env vars in CI and local `.env` |
| One massive shared utility package that everything depends on — changing `@org/utils` rebuilds everything, deep chains form (A→B→utils, C→A→utils) | Split utils by domain: `@org/dates`, `@org/strings`, `@org/api-client`, `@org/hooks`. Keep fan-out under 15 consumers per package. Monitor with `nx graph` or `turbo run build --graph`. | `find packages/ -name "package.json" -exec jq -r '.name' {} \; \| while read pkg; do echo "$pkg: $(grep -rn "\"$pkg\"" packages/*/package.json \| wc -l) consumers"; done \| sort -t: -k2 -rn \| head -5` → packages with > 15 consumers need splitting | CI lint: `scripts/check-fanout.sh` — fails if any package has > 15 consumers, flags for splitting |
| Adopting monorepo because "Google and Meta do it" without coordination problems — monorepo solves multi-package coordination, if you don't have it, you don't need it | Evaluate objectively: do you have > 3 packages sharing code? Cross-package PRs weekly? Build order dependencies? Coordination problems between teams? If no to all, stay polyrepo. | `find . -name "package.json" -not -path "*/node_modules/*" \| wc -l` → if < 4, monorepo overhead exceeds benefit. `git log --oneline --since="1 month" \| grep -c "cross-package\|workspace\|link"` → if 0, no cross-package work | Decision tree: `scripts/should-monorepo.sh` — scores on package count, team count, cross-package PR frequency, CI pain → outputs recommendation with rationale |
| Running `pnpm install` in CI from scratch every build — 2-5 minutes wasted per CI run on dependency installation | Cache `node_modules` using `actions/cache@v4` with `pnpm-lock.yaml` as cache key. `pnpm install --frozen-lockfile --prefer-offline`. Install step < 30 seconds on cache hit. | `grep -c "actions/cache\|cache:" .github/workflows/ci.yml` → must be ≥ 1 with `pnpm-lock.yaml` as part of cache key | GitHub Actions cache: `uses: actions/cache@v4 with: path: node_modules, key: pnpm-${{ hashFiles('pnpm-lock.yaml') }}` before `pnpm install` |
| Publishing packages manually with `npm publish` — order dependencies, forgot private flag, published internal package to npm | Changesets with `private: true` in `package.json` for non-publishable packages. CI-only publishing. `pnpm publish -r --filter=./packages/*` only publishes packages where `private: false`. | `grep -c "\"private\"\s*:\s*true" packages/*/package.json` → all internal packages should be private. `grep -rn "\"private\"\s*:\s*false" packages/*/package.json \| wc -l` → only publishable packages show here | Pre-publish hook: `scripts/check-publish-config.sh` — ensures `"private": true` on internal packages, `"publishConfig": {"access": "public"}` on public packages, fails if misconfigured |

## Footguns
<!-- DEEP: 10+min — war stories from monorepo management at scale -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| Merged 47 repositories into a monorepo — `git clone` took 12 minutes, CI build time went from 4 minutes to 45 minutes because no one configured affected-files detection, and 3 teams threatened to fork back to polyrepo | A 150-person engineering org consolidated 47 repos into a monorepo using Turborepo in Q1 2024. Migration took 3 months. Day 1 post-migration: `git clone` took 12 minutes (up from 30 seconds). CI builds went from 4 minutes average to 45 minutes because the pipeline built ALL packages regardless of what changed. Two teams with low-touch packages (2 commits/week each) were waiting 45 minutes for CI. Three tech leads submitted proposals to revert to polyrepo. The platform team spent Q2 2024 implementing sparse checkout, affected-files detection, and remote caching before the monorepo became usable. | The team optimized for "everything in one place" without optimizing for "how do we build only what changed?" Turborepo was installed but `turbo.json` used `"**/*"` as inputs for every task — effectively disabling caching and affected-files detection. Git operations weren't considered — a 47-repo monorepo with full history is a massive clone. | **Monorepo migration is not complete when the code is merged — it's complete when CI is faster than before.** Before migration: (1) benchmark `git clone`, install, build, test for each repo, (2) set performance targets for the monorepo: clone <90s, install <60s, affected build <3min, (3) configure sparse checkout, shallow clone, and partial clone from day 1, (4) every `turbo.json` task must have precise `inputs` — never use `**/*`, (5) if any team's CI is slower post-migration, the migration is NOT done. The monorepo must make development faster, not just more centralized. |
| One package's `package.json` had `"react": "*"` — hoisted to root by pnpm, every app in the monorepo got React 19 alpha instead of React 18 LTS, 3 days of debugging "unexplained" crashes and broken SSR | A monorepo with 25 packages used pnpm workspaces with hoisting. In September 2024, a developer added a new internal package with `"react": "*"` in its `package.json`. Pnpm hoisted React 19.0.0-alpha.1 to the root `node_modules`. Every app — none of which had opted into React 19 — started using the alpha version. Server-side rendering broke with cryptic hydration errors. `useEffect` fired twice in development. Three teams spent 3 days debugging before someone ran `npm ls react` and discovered the version mismatch. The offending package wasn't even importing React — the dependency was a copy-paste artifact. | Unrestricted version ranges in a monorepo are time bombs. `"*"` means "give me the latest" — and the latest might be an alpha. Hoisting is powerful but dangerous: one package's bad dependency poisons every consumer. No CI check prevented incompatible version ranges. | **Lock down dependency versions in a monorepo with automation.** Use `syncpack` to enforce single versions of critical dependencies (React, TypeScript, Next.js) across all packages. Add a CI rule: any `package.json` with `"*"` or `">= "` fails the build. Run `pnpm why react` in CI to verify that only the intended version is resolved. For peer dependencies: use pnpm's `strictPeerDependencies=true` in `.npmrc` — if a package declares a peer dep but doesn't match the hoisted version, the install fails. Hoisting is powerful but must be policed. |
| No CODEOWNERS enforcement — any team could modify any package, a frontend team accidentally broke the shared auth library, blocked 8 teams from deploying for 2 days | A monorepo with 30 packages had no CODEOWNERS file. Any developer could approve PRs to any package. In March 2024, a frontend team refactored the shared `@org/auth` package to replace JWT parsing with a newer library. The PR was approved by another frontend developer. The change broke: token refresh logic (used by 5 backend services), session validation (used by the mobile API), and role-based access control (used by the admin dashboard). 8 teams couldn't deploy for 2 days while the auth team — who hadn't been notified of the change — diagnosed and reverted the refactor. | Shared packages are infrastructure, not just code. Without CODEOWNERS, there is no gate between "I changed my package" and "I changed everyone's package." The auth package had no test suite that covered the backend and mobile use cases. | **Every shared package gets CODEOWNERS and a cross-team test suite.** CODEOWNERS: `packages/auth/ @team-auth` — any PR to auth requires auth team approval. Critical shared packages (auth, logging, config, API client): require 2 approvals, one from the owning team and one from a consumer team. Add integration tests that cover ALL consumer use cases — if the mobile team depends on a specific token format, that format must be a test in the auth package. A change that breaks any consumer test cannot merge. |
| Turborepo cache inputs used `**/*` for every task — cache always missed, CI build repeated all tasks on every commit, CI costs hit $14K/month for what should have been $3K | A monorepo team configured Turborepo in May 2024. Every `turbo.json` task had `"inputs": ["**/*"]` — "rebuild if any file changes." Since every commit changed at least one file, the cache never hit. Every CI run rebuilt every package from scratch. CI costs (GitHub Actions minutes): $14K/month. Expected cost with proper caching: $3K/month. The team had enabled remote caching (S3 bucket) but the cache was never populated because inputs were too broad. The infra team flagged the cost anomaly in August — 3 months of unnecessary spend ($33K wasted). | The team copied `"**/*"` from a Turborepo tutorial without understanding that inputs define the cache key. "Any file change" means "never cache." The docs template should have been adapted to specify exactly which files matter (source code, config, not README changes). | **Every Turborepo input must be as narrow as possible.** For a build task: `"inputs": ["src/**", "tsconfig.json", "package.json"]` — not `**/*`. README changes shouldn't invalidate build caches. For a test task: `"inputs": ["src/**", "test/**", "jest.config.js"]`. For a lint task: `"inputs": ["src/**", ".eslintrc.js"]`. Validate cache effectiveness: `turbo run build --dry-run` shows what would be cached. If cache hit rate is <50% for the most common tasks, your inputs are too broad. Remote cache costs are negligible; CI compute costs from missed caches are not. |
| Monorepo without tooling standardization — 3 different test runners (Jest, Vitest, Mocha), 4 different TypeScript versions (4.9, 5.0, 5.1, 5.3), 2 different linter configs — impossible to enforce quality gates across packages | A 10-team monorepo started in January 2024 with "teams own their stack." By June: 3 test runners (Jest, Vitest, Mocha), 4 TypeScript versions (4.9 to 5.3), and 2 linter configs (ESLint 8 and ESLint 9 with flat config). The platform team tried to add a CI quality gate: "all tests must pass with coverage >80%." Couldn't implement it because each test runner had different output formats and configuration. TypeScript compilation at the root failed because packages used incompatible TS versions. A security team tried to add a package audit gate — blocked because different package managers resolved different dependency trees. | Monorepo without standardization defeats the purpose of having everything in one repo. The "team autonomy" argument was used to avoid the hard work of aligning on shared tooling. The platform team didn't set a migration deadline: "eventually we'll standardize." | **Tooling standardization is a monorepo requirement, not a nice-to-have.** Before merging packages: define the canonical test runner, TypeScript version, linter config, and build tool for the entire repo. Packages that can't migrate immediately get a 90-day exception with a documented migration plan. CI enforces that all packages use the canonical tooling. The value of a monorepo is proportional to the consistency of its tooling — inconsistent tooling in one repo is worse than consistent tooling in separate repos. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can set up a monorepo with Turborepo or Nx but every CI run takes >20 minutes and you think "that's just how monorepos work" | You've migrated an org from polyrepo to monorepo and CI build times (for affected packages) are faster post-migration than the average polyrepo build time — and you have the before/after data | An engineering org with 200 developers and 80 packages asks "should we monorepo or stay polyrepo?" — you model the trade-offs with actual build times, coordination costs, and dependency graphs from their specific codebase, and your recommendation is validated by outcomes 12 months later |
| You treat monorepo tooling as "install Nx/Turborepo and we're done" — you haven't configured sparse checkout, affected-files detection, or remote caching | You've instrumented your monorepo's performance: clone time, install time, affected build time, full build time, cache hit rate, CI cost per PR — and you review these metrics monthly | A team says "the monorepo is killing our productivity — our CI takes 30 minutes for a README change" — you diagnose the root cause (overbroad inputs, missing affected-files config) and fix it within a week, reducing their CI time by 85% |
| You enforce conventions manually — you review PRs and comment "please use the shared ESLint config" — and the same violations appear next sprint | You enforce conventions automatically — CI fails on non-standard tooling, CODEOWNERS gates changes to shared packages, and dependency version mismatches are caught at PR time | You design a monorepo governance model that scales to 50+ packages and 15+ teams — your CODEOWNERS, CI gates, and package boundaries prevent cross-team breakage without becoming a bottleneck, and teams self-serve within the guardrails |

**The Litmus Test:** A company with 15 polyrepos and 80 developers asks you to design their monorepo strategy. You have 2 weeks to produce: (1) whether they should monorepo or not (with data, not opinion), (2) tooling selection with trade-offs, (3) migration plan with rollback strategy, (4) governance model for 15 teams. If your first instinct is "yes, monorepos are better," you're L1. Masters evaluate the specific coordination problems, code-sharing patterns, and build constraints before recommending — and sometimes recommend staying polyrepo.

## Deliberate Practice

```mermaid
graph LR
    A[Build] --> B[Measure<br/>failure modes] --> C[Study<br/>post-mortems] --> D[Re-build<br/>with constraints] --> A
```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Rebuild an existing system from scratch, then compare your design with the original | Monthly |
| **Competent** | Add a new constraint (10x data, zero downtime, etc.) to a familiar design and re-architect | Quarterly |
| **Expert** | Design the same system under 3 conflicting constraint sets; write a decision record for each | Quarterly |
| **Master** | Teach a junior to design a system; your role is to ask questions, not give answers | Monthly |

**The One Highest-Leverage Activity:** Every quarter, take a system you built 6+ months ago and redesign it from scratch with what you know now. Write down what changed and why.

## References
<!-- QUICK: 30s -- links to deeper reading -->
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
