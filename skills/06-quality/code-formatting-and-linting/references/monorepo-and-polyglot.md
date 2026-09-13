# Monorepo and Polyglot

<!-- STANDARD: 3min -- one policy across many languages and packages -->

## The problem

An organisation with TypeScript, Go, Swift, Kotlin and Python in one repository. Four temptations, each wrong:

| Temptation | Why it fails |
|---|---|
| One tool for everything | the tool does not own every language; false positives get suppressed (R5) |
| One config file per package, no shared policy | five standards drift into five philosophies |
| No config at all, "each team decides" | every cross-team change is a negotiation |
| A single CI job for all languages | one failure message for five causes |

## The model: one policy, N tools

```
POLICY (portable, one per organisation)
├── .editorconfig              → line endings, final newline, whitespace, indentation intent
├── the enforcement model      → format-on-save → hook → CI (authority) → branch protection
├── the suppression rule       → rule named, reason required, minimal scope, visible count
├── the exclusion rule         → generated/vendored excluded the same way everywhere
├── the autofix boundary       → formatting yes; behaviour-changing lint fixes no
└── the naming convention      → "Check formatting" and "Lint" in every repo

TOOLS (per language, chosen once)
├── TypeScript  → Prettier or Biome + ESLint
├── Swift       → swiftformat + swiftlint
├── Kotlin      → ktlint + detekt
├── Go          → gofmt + golangci-lint
└── Python      → ruff format + ruff check
```

Everything in the policy block is identical across languages. Everything in the tools block is not — and that is fine, because a developer moving between languages keeps the *policy* and learns only the tool.

## Repository layout

```
/
├── .editorconfig                    ← root policy, root = true
├── .git-blame-ignore-revs           ← every formatting commit, all languages
├── CONTRIBUTING.md                  ← the policy, written down once
├── .github/workflows/style.yml      ← one workflow, a job per language
│
├── apps/web/
│   ├── .prettierrc                  ← tool config, package-local
│   └── eslint.config.js
├── services/api/
│   ├── pyproject.toml               ← ruff config lives with the package
│   └── mypy.ini
├── apps/ios/
│   └── .swiftlint.yml
└── apps/android/
    ├── .editorconfig                ← only if it differs from the root
    └── detekt.yml
```

**The rule for placement:** the portable policy at the root, the tool config with the package that uses it. A tool config at the root that only applies to one package is confusing; a policy split across packages is not a policy.

## The CI shape

One workflow, a job per language, so failures are attributable:

```yaml
jobs:
  format-web:      # npx prettier --check
  lint-web:        # npx eslint
  format-python:   # ruff format --check
  lint-python:     # ruff check
  lint-kotlin:     # ktlint + detekt
  lint-swift:      # swiftlint
```

Three rules:

1. **Name the job for the language and the category.** "Style" as one job means one opaque failure.
2. **Scope each job to its package.** A web lint job should not scan Python.
3. **Keep the failure message local.** "Formatting failed in `apps/web` — run `npm run fmt`" is actionable; a repo-wide message is not.

For a monorepo with many independent packages, a matrix parallelises this — but the *policy* is still one document (see `ci-integration.md`).

## Shared configuration without a shared tool

Where several packages use the same tool, share its config rather than duplicating it:

```js
// packages/web/eslint.config.js
import shared from '@org/eslint-config'
export default [...shared, { /* package-specific overrides */ }]
```

```toml
# services/api/pyproject.toml
[tool.ruff]
extend = "../../ruff-base.toml"     # or a published org config
```

**Two cautions:**

- **A shared config is a dependency.** Version it, and upgrade it deliberately — like any dependency (see `dependency-governance.md`).
- **Overrides must be minimal and local.** A package that overrides half the shared config either should not use it, or is revealing that the shared config is wrong.

## Onboarding a new language

The procedure that keeps the policy single:

```text
1. Which languages does the existing policy already cover?
   └── None of the new one → add a section to .editorconfig
2. Is there an ecosystem-default formatter?
   ├── Yes → use it unmodified (gofmt, rustfmt, dart format)
   └── No  → choose one, record the reasoning
3. Add the linter, with its rule set chosen deliberately (not "everything on")
4. Add the exclusions for generated output in that language
5. Add the CI job, named for the language and the category
6. Add the language to the suppression budget
7. Verify: a deliberately unformatted file in that language fails CI
8. Update the policy document
```

**Step 7 is the acceptance test.** A new language is onboarded when a deliberate formatting failure is caught, not when the config file exists.

## The cross-language consistency checks

Not everything can be identical, but these should be:

| Property | Why it should match |
|---|---|
| Line endings | a mixed repo produces spurious diffs across tools |
| Final newline | universal |
| Trailing whitespace | universal, with the Markdown exception |
| Indentation *intent* | the number differs (Go uses tabs), the consistency does not |
| Enforcement model | the same ladder in every language |
| Suppression form | rule named, reason required — the syntax differs, the rule does not |
| Exclusion policy | generated output excluded everywhere |
| CI job naming | same convention across languages |

## Anti-patterns in a polyglot repo

| Anti-pattern | Why it fails |
|---|---|
| Four configs, no shared policy document | each team re-derives the standard, and they diverge |
| One tool stretched across languages | false positives, then suppressions (R5) |
| A root tool config that only one package uses | other packages assume they are covered |
| Language-specific CI job names | nobody can tell what "style" failed |
| A suppression budget per team, not per language | growth becomes someone else's problem |
| A new language added without an exclusion policy | its generated files become noise |
| No policy document | a new hire asks the same question five times |

## Checklist

- [ ] The portable policy is identical across all languages, and written down in one place
- [ ] Each language has exactly one formatter and one linter, chosen deliberately (R5)
- [ ] Tool configs live with the packages that use them; the policy lives at the root
- [ ] `.editorconfig` covers every language present, and overrides are minimal
- [ ] CI has a job per language and per category, named so failures are attributable
- [ ] Shared configs are versioned dependencies, with minimal local overrides
- [ ] Each language has a suppression budget
- [ ] Generated output is excluded for every language
- [ ] A new language is onboarded by extending the policy, with a deliberate-failure test
- [ ] A developer moving between packages learns only the tool, not a new standard
