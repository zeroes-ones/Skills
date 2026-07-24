# Build System & Cross-Repo Orchestration

Orchestrating builds across multiple repositories requires tooling that understands dependency graphs, caching, and incremental computation. Below are the dominant patterns.

## Tool Comparison

| Tool | Model | Best For | Caching | Remote Execution |
|------|-------|----------|---------|------------------|
| **Nx** | Monorepo-first, polyrepo via `nx graph` | TypeScript/Node, polyglot with plugins | Local + Nx Cloud | Nx Cloud Agents |
| **Turborepo** | Monorepo, lightweight | JS/TS ecosystem | Local + Remote Cache (Vercel) | No |
| **Bazel** | Polyglot, hermetic | Large orgs, multi-language | Local + Remote (BuildBarn) | Yes (REAPI) |
| **Lage** | Monorepo, Backfill | JS/TS, simpler than Nx | Local + Backfill | No |
| **Pants** | Polyglot, hermetic | Python/JVM/Go, similar to Bazel | Local + Remote | Yes |

## Cross-Repo Build Patterns

### 1. Contracts-Driven Build (Recommended)
```
1. contracts/ publishes schema v2.0.0
2. toolkit/ updates client generation, publishes toolkit v3.1.0
3. auth/ updates to toolkit v3.1.0, validates against contracts v2.0.0
4. CI gate: auth/ cannot merge if contracts compatibility test fails
```

### 2. Consumer-Driven Contracts (CDC)
Each downstream repo publishes its expected contract behavior. The upstream provider validates all consumers pass before releasing:
```
billing/ci:
  - Run CDC tests from auth/, gateway/, reporting/
  - Fail release if any consumer contract breaks
```

### 3. Distributed Task Execution
For Bazel setups across repos:
```python
# MODULE.bazel in each repo declares external deps
bazel_dep(name = "platform_contracts", version = "2.0.0")
bazel_dep(name = "org_toolkit", version = "3.1.0")
```

## Cross-Repo CI Pipelines

Use a "contracts-first" pipeline:
1. **contracts/**
   - Lint → Validate → Publish → Trigger downstream
2. **auth/, billing/, gateway/**
   - Lint → Validate against contracts → Build → Test → Deploy
3. **toolkit/**
   - Lint → Build → Publish → Notify consumers via PR comments

Key rule: **No repo's CI should depend on another repo's CI at runtime.** Use published artifacts, not live builds. This prevents the "distributed monolith CI" anti-pattern where pushing to any repo triggers builds in all repos — leading to cascading failures and debugging hell.
