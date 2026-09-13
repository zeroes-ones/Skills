# Tool Selection

<!-- DEEP: 5+min -- the per-language formatter and linter map, and how to choose within a language -->

> **Verification note.** Tool capabilities, rule sets and defaults change between versions, and
> several ecosystems are mid-migration (ESLint's flat config, the Prettier-versus-Biome question).
> Confirm the current behaviour against the installed version's documentation before configuring.

## The map

One formatter and one linter per language. The pair below is a defensible default; the reasoning after it is what matters more than the specific choice.

| Language | Formatter | Linter | Note |
|---|---|---|---|
| TypeScript / JavaScript | **Prettier** or **Biome** | **ESLint** (or Biome's rules) | Biome covers both for many projects; ESLint remains more extensible |
| Swift | **swiftformat** | **swiftlint** | different tools, different scopes; both are normal |
| Kotlin | **ktlint** (format) | **ktlint** + **detekt** | ktlint formats and lints style; detekt covers complexity and smells |
| Rust | **rustfmt** | **clippy** | both are first-party and effectively mandatory |
| Go | **gofmt** / **goimports** | **golangci-lint** | gofmt is non-negotiable in the ecosystem |
| Python | **ruff format** (or Black) | **ruff check** | ruff now covers both; Black remains a safe formatter |
| C / C++ | **clang-format** | **clang-tidy** | both from the LLVM project; `.clang-format` is the shared config |
| C# / .NET | **dotnet format** | **dotnet format analyzers** / Roslyn analyzers | one tool, two modes |
| Java | **google-java-format** or Spotless | **SpotBugs**, **ErrorProne** | Spotless can drive the formatter |
| Ruby | **rubocop -a** (format) | **rubocop** | one tool, both jobs, distinct modes |
| Dart / Flutter | **dart format** | **dart analyze** | first-party; `analysis_options.yaml` configures |
| Shell | **shfmt** | **shellcheck** | both are the de-facto standard |
| YAML / JSON / Markdown | **prettier** | **yamllint**, **markdownlint** | config and docs are code too |
| Terraform / HCL | **terraform fmt** | **tflint** | first-party formatter |
| SQL | **sqlfluff format** | **sqlfluff lint** | one tool, both modes |
| Protobuf | **clang-format** | **buf lint** | buf's rules are the ecosystem standard |

**The pattern:** in most ecosystems the formatter and linter are *separate tools with separate purposes* — Go, Rust, Swift, Kotlin, C++, Shell. In a few, one tool does both in two modes — `dotnet format`, `rubocop`, `ruff`, `sqlfluff`. Know which you have, because the enforcement model differs slightly: a one-tool setup can be a single CI job with two commands; a two-tool setup must not be conflated into one job with one message.

## How to choose within a language

```text
1. Is there a first-party or ecosystem-default tool?
   ├── Yes → use it, unmodified
   │   (gofmt, rustfmt, dart format, Black, terraform fmt, google-java-format)
   │   └── Deviation needs a written reason; the ecosystem's tooling assumes the default
   └── No ↓
2. Are there two credible options (Prettier vs Biome, Black vs ruff format)?
   ├── Evaluate on: coverage of your syntax, editor integration, speed on your repo size,
   │   autofix breadth, and whether one tool covers format+lint
   ├── Prefer the one with fewer tools to maintain, IF it covers your rules
   └── Do not switch tools mid-migration without a plan
3. Does the linter need project-specific rules (custom AST rules, framework rules)?
   ├── Yes → ESLint-family extensibility matters; choose accordingly
   └── No  → the fastest and simplest tool that covers the rules wins
4. Is the language compiled with a first-party analyzer?
   └── Yes → prefer it over a third-party general analyser (clippy, dart analyze, Roslyn)
```

## The version-pinning rule

A formatter is a tool whose output is a **contract**. A version change can reformat the whole repo.

| Practice | Why |
|---|---|
| Pin the formatter version in the repo (lock file, devDependency, toolchain file) | an unpinned formatter reformats unexpectedly on upgrade |
| Pin the linter version | a new rule can turn a passing build red on a version bump |
| Upgrade deliberately, as its own commit | the reformat it causes should be isolated (see `legacy-migration.md`) |
| Never let CI and local versions differ | the disagreement is invisible until CI fails on working code |

**The invisible failure:** a formatter that resolves differently in CI than locally — a different version, a different config path, a different plugin set. The developer sees a clean local check and a failing CI check, and concludes the CI is broken. Pin and resolve the config from the repository root.

## Plugin and preset management

| Rule | Detail |
|---|---|
| Every plugin is a dependency with an owner | an unmaintained plugin becomes a security and correctness risk |
| A preset is a starting point, not a policy | adopt it, then record any deviation |
| Fewer plugins is better | each adds install time, resolution complexity and a version to keep aligned |
| A custom rule must earn its maintenance | a hand-written rule that nobody maintains is a rule that will be wrong |

## Config placement

| Tool | Conventional location |
|---|---|
| Prettier | `prettier.config.js` / `.prettierrc` at the root |
| Biome | `biome.json` at the root |
| ESLint | `eslint.config.js` (flat config) at the root |
| swiftlint | `.swiftlint.yml` at the repo or package root |
| ktlint / detekt | `.editorconfig` section and `detekt.yml` |
| ruff / Black | `pyproject.toml` (single source of truth) |
| clang-format | `.clang-format` at or above the source tree |
| Cargo / rustfmt | `rustfmt.toml` or `Cargo.toml` |
| Go | no config by default — `gofmt` has no options, deliberately |

**The Go case is instructive**: `gofmt` deliberately has almost no configuration. That is the ecosystem's way of ending the argument, and it is worth copying as a principle — prefer the tool with no options over the tool with forty.

## Keeping the check fast

| Technique | Effect |
|---|---|
| Scope to changed files | the single biggest win on a large repo |
| Run format and lint as separate jobs | each can be cached and parallelised |
| Cache the tool's own cache directory | for tools that support it (ESLint, ruff, ktlint) |
| Do not lint generated output | remove the work entirely (see `generated-and-vendored.md`) |
| Run the full check on the main branch, the scoped check on PRs | full coverage without slowing every PR |

A gate that takes longer than a few minutes is a gate people route around. Speed is a correctness property here, not an optimisation.

## Checklist

- [ ] Every language maps to exactly one formatter and one linter (R5)
- [ ] Ecosystem-default tools are adopted unmodified, with deviations recorded
- [ ] Formatter and linter versions are pinned in the repository, not floating
- [ ] CI and local resolve the same config from the same path
- [ ] One-tool setups are understood as one tool in two modes, not one combined check
- [ ] Plugins are few, owned and maintained
- [ ] Config lives at the conventional location for each tool
- [ ] The check is scoped to changed files where the tool supports it
- [ ] Tool upgrades are their own commit, with any reformat isolated
