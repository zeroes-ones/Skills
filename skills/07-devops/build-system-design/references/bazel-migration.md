# Bazel Migration Playbook

## Migration Cost Estimation

### Small Codebase (<50K LOC, single language)
```
Duration: 2-4 weeks, 1-2 engineers
Effort: 80-160 engineer-hours
Cost: $12K-$24K
Risk: Low
```

### Medium Codebase (50K-500K LOC, 2-3 languages)
```
Duration: 2-4 months, 2-3 engineers
Effort: 400-1200 engineer-hours
Cost: $60K-$180K
Risk: Medium — requires careful dependency analysis
```

### Large Codebase (>500K LOC, polyglot)
```
Duration: 6-12 months, 3-5 engineers
Effort: 2400-9600 engineer-hours
Cost: $360K-$1.4M
Risk: High — requires dedicated build team, continuous maintenance
```

## Migration Phases

### Phase 1: Preparation (2-4 weeks)
- Audit current build: identify all external dependencies, code generation steps, deploy process
- Set up Bazel workspace: WORKSPACE/MODULE.bazel, toolchain registration
- Migrate third-party dependencies to Bazel-native rules (http_archive, rules_jvm_external)

### Phase 2: Strangler Migration (ongoing)
- Convert module by module: each module gets a BUILD file alongside existing build config
- Both build systems must work during migration
- CI runs BOTH builds — new Bazel build is informational (not blocking) initially
- Gradual transition: Bazel build becomes blocking, old build becomes informational, then removed

### Phase 3: Optimization (after migration complete)
- Profile build: identify slow targets, optimize dependency graph
- Enable remote caching
- Evaluate remote execution

## Migration Tooling

| Tool | Purpose |
|------|---------|
| Kythe | Cross-language indexing and reference analysis |
| buildifier | Auto-format BUILD files to Bazel style |
| Buildozer | Programmatic BUILD file manipulation |
| Gazelle | Auto-generate BUILD files from Go source |
| Maven migration | rules_jvm_external + gmaven (Gradle-to-Bazel) |

## Migration Anti-Patterns

1. Big-bang migration on large codebase → weeks of broken builds
2. Migrating without dedicated build owner → BUILD file rot sets in immediately
3. Skipping team training → cargo-cult BUILD files with incorrect deps
4. Not measuring before/after → cannot justify the investment
5. Migrating when build pain < $100K/year → migration costs more than pain
