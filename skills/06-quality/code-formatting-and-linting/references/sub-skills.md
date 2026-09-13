# Sub-Skills

<!-- QUICK: 30s -- when to split into a narrower session -->

| Sub-skill | When to use it | Where it lives |
|---|---|---|
| `format-vs-lint` | Separating the two categories in config, CI and vocabulary | `references/formatting-vs-linting.md` — R1 |
| `portable-policy` | `.editorconfig`, and what belongs there versus in a tool | `references/portable-policy.md` |
| `tool-selection` | Which formatter and linter per language | `references/tool-selection.md` — R5 |
| `enforcement` | Where the check lives, and why CI is the authority | `references/enforcement-model.md` — R2 |
| `legacy-migration` | Reformatting an existing codebase safely | `references/legacy-migration.md` — R3 |
| `suppressions` | Bounded exceptions, budgets, and the visible count | `references/suppression-policy.md` — R4 |
| `exclusions` | Generated, vendored and build output | `references/generated-and-vendored.md` — R6 |
| `autofix` | Which findings may be fixed automatically | `references/autofix-boundaries.md` |
| `ci` | Scoping, caching and job shape | `references/ci-integration.md` |
| `polyglot` | One policy across many languages | `references/monorepo-and-polyglot.md` |

## Split when

- **One concern dominates.** "Where should the check run?" is `enforcement`; it does not need the migration or polyglot work.
- **The task is a legacy reformat** — that is `legacy-migration` plus `enforcement`, and it is bounded.
- **The task is a suppression cleanup** — that is `suppressions` alone.
- **The question is one tool's configuration** — `tool-selection`, then finish.
- **The question is the build's speed** — hand to `build-system-design`; this skill owns the check, not the build graph.

## Stay whole when

- **A repo is adopting a style policy for the first time.** The intent layer, the tools, enforcement, exclusions and the suppression rule are one policy; splitting them produces a formatter with no gate, or a gate with no exclusions (which is how it gets disabled).
- **A polyglot org is standardising.** The portable policy and the per-language tool map are the same decision, and doing them separately produces five standards instead of one.

## Adjacent skills, and the boundary

| Neighbour | They own | This skill owns |
|---|---|---|
| `code-reviewer` | Reviewing the substance of a change | Removing style from the review entirely |
| `code-simplification` | Reducing complexity while preserving behaviour | The mechanical and static checks around it |
| `repo-scaffolding` | Scaffolding a new repository | The style policy a scaffold inherits |
| `build-system-design` | Build speed, caching, task graphs | The check's scope and speed, not the build system |
| `ci-cd-builder` | The pipeline's construction | The exact commands, the failure conditions, and the authority model |
| `git-workflow` | Branching and commit conventions | The reformat isolation and the blame-ignore entry |
| `dependency-governance` | Dependency versions, CVEs, licences | Excluding generated code and pinning tool versions |
| `appsec-engineer` | The security threat model | Never suppressing a security-relevant lint rule |
| `merge-conflict-resolver` | Resolving conflicts | Identifying formatting-only commits so conflicts are mechanical |

The pattern: the neighbours own *the change* and *the pipeline*; this skill owns *how style is decided,
enforced and excepted* — so that no human ever has to make a style decision twice.
