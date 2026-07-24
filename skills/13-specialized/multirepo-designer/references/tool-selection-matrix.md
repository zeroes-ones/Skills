# Tool Selection Matrix: Monorepo vs Polyrepo Tooling

Choosing the right tool for your multirepo architecture depends on language ecosystem, team size, and operational maturity. Below is a comprehensive comparison.

## Primary Tool Comparison

| Feature | Nx | Turborepo | Rush | Lerna | Bazel | Pants |
|---------|----|-----------|------|-------|-------|-------|
| **Model** | Mono + distributed | Monorepo | Monorepo | Monorepo | Polyglot hermetic | Polyglot hermetic |
| **Languages** | JS/TS/Go/Python | JS/TS primarily | JS/TS | JS/TS | All major | Python/JVM/Go |
| **Caching** | Local + Cloud | Local + Remote | Local + Cloud | Local only | Local + Remote | Local + Remote |
| **Remote Exec** | Nx Cloud Agents | No | Rush Cloud | No | Yes (REAPI) | Yes |
| **Incremental** | Yes | Yes | Yes | Yes | Yes | Yes |
| **Dependency Graph** | Automatic | Automatic | Manual + auto | Manual | Automatic (Starlark) | Automatic |
| **Learning Curve** | Medium | Low | Medium | Low | Very High | High |
| **Setup Time** | 1 hour | 10 min | 1 hour | 10 min | 1-4 weeks | 1-2 weeks |
| **Best Team Size** | 5-200+ | 2-50 | 10-200 | 2-20 | 50-5000+ | 20-500 |

## Decision Flowchart

```
START
├── JS/TS only?
│   ├── < 10 repos? → Lerna or Turborepo
│   ├── 10-50 repos? → Nx or Rush
│   └── 50+ repos? → Nx with distributed task execution
│
├── Polyglot (JS + Go + Python + JVM)?
│   ├── < 50 repos? → Nx (polyglot plugins) or Pants
│   ├── 50-500 repos? → Bazel or Pants
│   └── 500+ repos? → Bazel (only option at this scale)
│
└── Need hermetic, reproducible builds?
    ├── Yes → Bazel or Pants
    └── No → Nx (best DX for most teams)
```

## Cross-Repo Specific Selection

For true polyrepo (separate git repos), not monorepo:

| Tool | Polyrepo Support | Mechanism |
|------|-----------------|-----------|
| **Nx** | Yes (`project.json` in each repo) | Nx graph can span repos via `nx.json` references |
| **Bazel** | Yes | `local_repository()` + `git_repository()` in WORKSPACE/MODULE |
| **Gradle** | Yes | Composite builds + included builds |
| **Cargo** | Yes | `[patch]` + path dependencies + workspace inheritance |
| **Go Modules** | Yes | `replace` directives + multi-module workspaces |

## Recommendation Matrix

| Scenario | Recommended Tool | Rationale |
|----------|-----------------|-----------|
| Startup, 3 JS repos | Lerna + Nx | Fast setup, grows with you |
| Mid-size, 15 mixed repos | Nx | Best DX-to-power ratio |
| Enterprise, 100+ repos | Bazel | Only hermetic option at scale |
| Go ecosystem | Go Workspaces + Buf | Native Go tooling |
| JVM ecosystem | Gradle Composite Builds | Native JVM tooling |
| Contract-heavy (Protobuf) | Buf + Bazel | Protobuf-native tooling |

## Anti-Recommendations

- **Don't use Bazel for < 10 repos.** The setup cost outweighs benefits.
- **Don't use Lerna for > 20 repos.** It doesn't scale well beyond that.
- **Don't mix build tools** across repos without a shared CI template. Consistency matters more than optimality.
