# Additional Resources — code-formatting-and-linting

> Deep knowledge loaded on demand. `SKILL.md` stays lean; extended material lives here and in the
> sibling reference files.

## Reference file map

| File | Covers |
|---|---|
| `formatting-vs-linting.md` | Why the two are different categories, the failures from conflating them, and where the bright line sits |
| `portable-policy.md` | `.editorconfig` as the intent layer, what belongs there, alignment with the formatter, and monorepo overrides |
| `tool-selection.md` | The per-language formatter and linter map, how to choose within a language, version pinning, config placement, and keeping the check fast |
| `enforcement-model.md` | The format-on-write → hook → CI → branch-protection ladder, why CI is the authority, and how to demonstrate each layer |
| `legacy-migration.md` | The isolated reformat, `.git-blame-ignore-revs`, branch coordination, and the incremental alternative |
| `suppression-policy.md` | Bounded suppressions, the report, budgets, stale-suppression review, global relaxations, and the security carve-out |
| `generated-and-vendored.md` | What to exclude, the golden-file caveat, header markers, and verifying the exclusion applies |
| `autofix-boundaries.md` | Which fixes are deterministic, the classic unsafe "safe" fixes, and the reviewed autofix set |
| `ci-integration.md` | The job shape, changed-files scoping, caching, branch protection, and the renamed-job trap |
| `monorepo-and-polyglot.md` | One policy across many languages: layout, CI shape, shared configs, and language onboarding |
| `anti-patterns.md` | Eighteen style anti-patterns with detection heuristics and a sweep script |
| `error-decoder.md` | Sixteen symptoms in long form: mechanism, diagnosis, fix, recurrence guard |
| `sub-skills.md` | When to split the session, and the boundary with adjacent skills |

## Extended example

`examples/backtest/README.md` runs a style-policy adoption against a stated scenario, with the arithmetic
shown and every figure provenance-tagged.

## Source material

Formatter options, linter rule sets and defaults change between versions, and several ecosystems are
mid-migration. Confirm the current behaviour against the installed version before configuring.

| Source | What it governs |
|---|---|
| EditorConfig specification and project documentation | Property semantics and cross-editor support |
| Formatter documentation (Prettier, Biome, Black, gofmt, rustfmt, swiftformat, ktlint, dart format, clang-format, shfmt, terraform fmt, Spotless) | Formatting behaviour, defaults and configuration |
| Linter documentation (ESLint, swiftlint, detekt, clippy, golangci-lint, ruff, clang-tidy, shellcheck, SpotBugs, Roslyn analyzers, buf lint) | Rule sets, severity, and which rules have safe autofixes |
| `git-blame(1)`, `git-config(1)` | `blame.ignoreRevsFile` and the ignore-revs file format |
| pre-commit documentation | Hook installation, behaviour, and skipping |
| CI provider documentation | Required checks, branch protection, job naming and caching |

## Verification harness

`scripts/verify-skill.sh` asserts this skill's own invariants: that all six ground rules are present with
enforcement columns, that formatting and linting are treated as separate categories, that CI is required
as the authority rather than a hook, that a legacy reformat must be isolated and blame-ignored, that
suppressions require a rule name and a reason with a visible count, that generated code is excluded, and
that the security carve-out on suppressible rules is stated. Run it before relying on the skill's output.
