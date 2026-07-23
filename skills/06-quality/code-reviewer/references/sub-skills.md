# Sub-Skills

<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `security-review` | Auth, crypto, PII, payment code | Dimension 1 — injection, auth, data exposure, dependency CVEs |
| `performance-review` | Query-heavy, memory-intensive, latency-sensitive code | Dimension 2 — N+1, memory leaks, complexity, bundle size |
| `code-quality-review` | All PRs — readability, design, error-prone patterns | Dimension 3 — SRP, DRY, TypeScript strictness, cyclomatic complexity |
| `error-handling-review` | Error paths, external integrations, async code | Dimension 4 — propagation, graceful degradation, edge cases, transactions |
| `testing-review` | Test coverage gaps, test quality, flaky tests | Dimension 5 — behavior vs implementation, assertions, isolation |
| `documentation-review` | API docs, READMEs, architecture docs, comments | Dimension 6 — JSDoc, API specs, architecture decisions, TODOs |
| `language-specific` (Python/TS/Go/Rust) | Per-language anti-patterns | `references/language-specific-review-guides.md` |
| `dead-code-cleanup` | Dead code, commented-out code, stale flags, unused deps | `references/dead-code-cleanup-checklist.md` |
