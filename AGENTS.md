# AGENTS.md — Working in the Zeroes & Ones Skills Repository

> This file is for AI coding agents and new contributors who know nothing about this repository.
> It describes what the project is, how it is built and validated, and the conventions every
> change must follow. All commands below are the repo's own and were run against the current
> checkout unless a caveat is stated.

---

## 1. What this project is

This repository is **two things at once**:

1. **A skill library** — 322 written playbooks (`SKILL.md` files) that tell an AI agent how to do
   one professional job (review code, design a database, price a consulting engagement, audit
   accessibility, etc.). Each skill is a markdown file with YAML frontmatter, plus optional
   supporting `scripts/`, `references/`, `examples/`, and `evals/` directories.
2. **A workflow engine** — a small, dependency-free Python program that runs those playbooks as a
   graph of steps: it loops where work should retry, stops where a human must approve, and records
   evidence as it goes. The engine owns control flow; skills own content.

The library is meant to be **agent-agnostic**: it works with Claude Code, GitHub Copilot CLI,
Cursor, OpenClaw, Gemini CLI, Codex, Windsurf, Cline, OpenCode, Zed, and any agent that reads the
open `SKILL.md` format. It is distributed via shell installer, npm
(`@zeroes-ones/skills`), the skills.sh registry, and the Claude plugin marketplace.

- **Owner / author:** Sandeep Kumar Penchala
- **License:** MIT
- **Primary language of docs and comments:** English

### Current measured state (as of this checkout)

| Fact | Value | How to re-check |
|---|---|---|
| Skills | **322** in **37** domain directories | `find skills -name SKILL.md \| wc -l` |
| Flat discovery entries | 322 symlinks, no collisions | `python3 scripts/check-flat-index.py` |
| Library audit score | **9.8/10** (domain-calibrated) | `python3 scripts/audit-library.py` |
| Governance gate | `PASS: 14  FAIL: 0` | `bash scripts/validate-skills.sh` |
| Engine self-test | `selftest: 20 checks, 0 failed` | `python3 scripts/workflow-runner.py --selftest` |
| Workflow manifests | 6 in `workflow/manifests/` (+ examples) | `ls workflow/manifests/*.yaml` |
| Declared workflow contracts | 59 skills carry a `workflow:` block | `grep -rl '^workflow:' skills --include=SKILL.md \| wc -l` |
| Compiled corpus | 322/322 skills, **77.9%** measured token reduction | `python3 scripts/check-token-budget.py` |

> **Token-measurement caveat:** `scripts/_compile_skill.py:136` falls back to `len(text.split())`
> when `tiktoken` is absent (it is absent here), so the toolchain's "token" figures are **word
> counts** and understate real cost by 1.5–2.3×. Measured with a real BPE tokenizer
> (`cl100k_base`): reduction is **77.9%**, not 86%; mean raw 13,895 / compiled 3,066 tokens per
> skill. Full benchmark: [`docs/token-context-benchmark.md`](docs/token-context-benchmark.md).

> **Count caveat:** the docs were swept on 2026-09-14 and now state counts consistent with the
> corpus. The single source of truth is always the filesystem: **322 today**. When you touch a
> count, prefer computing it (or phrasing it count-free) over hardcoding; where a number is part of
> a historical narrative or a dated build log, leave it and add a dated note rather than rewriting.

---

## 2. Repository layout

```
Skills/
├── skills/<domain>/<name>/SKILL.md      # CANONICAL skill store — two levels deep, 37 domains
├── skills-flat/<name> -> ../skills/...  # committed flat discovery layer (322 symlinks)
├── .skills-compiled/<name>/             # compiled XML + metadata.json (gitignored build output)
├── workflow/
│   ├── manifests/*.yaml                 # 6 executable workflow manifests
│   ├── schema/                          # workflow-manifest + run-state schemas
│   ├── templates/                       # node prompt templates (handoff, verify, loop, escalate)
│   └── tests/fixtures/                  # valid/invalid manifests for the validator self-test
├── plugins/<domain>/plugin.json         # generated Claude plugin per domain (+ zeroes-ones-all,
│                                        #   flagship-senior-engineering) — 39 plugin dirs
├── flagship/senior-engineering.json     # curated 30-skill flagship set definition
├── personas/*.md                        # role layer: code-reviewer, security-auditor, test-engineer…
├── hooks/                               # agent lifecycle hooks (session-start, simplify-ignore, sdd-cache)
├── evals/                               # 3-tier eval corpus (see §6)
├── examples/<scenario>/                 # 25 worked, runnable scenarios
├── docs/*.md                            # 30 design/ops/usage documents
├── scripts/                             # ~60 top-level tools + scripts/lib/, scripts/executors/, scripts/references/
├── .github/workflows/                   # CI: validate.yml, test-plugin-install.yml, deploy-pages.yml
├── .githooks/                           # commit-msg, pre-commit (17 gates), pre-push (CI mirror)
├── package.json                         # npm package + bin entries (NOT the app build)
├── .mcp.json                            # MCP server registration for this repo
└── reasonix.toml                        # local agent runtime permissions/sandbox config
```

There is **no** `pyproject.toml`, `Cargo.toml`, `Makefile`, `go.mod`, `requirements.txt`,
`setup.py`, `node_modules/`, or lockfile. `package.json` exists only to publish the installer CLI —
there is no JavaScript build step.

### Domain directories (37)

`00-framework`, `01-strategy`, `02-product`, `03-design`, `04-architecture`, `05-development`,
`06-quality`, `07-devops`, `08-security`, `09-data`, `10-growth`, `11-legal`, `12-operations`,
`13-specialized`, `14-finance`, `15-sales`, `16-people`, `17-customer-success`,
`18-corporate-finance`, `19-governance`, `20-hardware`, `21-health-clinical`,
`22-ai-engineering`, `23-trust-safety`, `24-creative`, `25-engineering-leadership`, `26-web3`,
`27-creator-finance`, `28-social-impact`, `29-personal-finance`, `30-health-wellness`,
`31-personal-growth`, `32-relationship-family`, `33-real-estate`, `34-philosophy-wisdom`,
`35-home-domestic`, `36-travel-adventure`.

---

## 3. Technology stack and runtime requirements

The project is deliberately **dependency-light** so it runs in offline sandboxes and on any agent
host.

| Layer | Technology | Notes |
|---|---|---|
| Skill content | Markdown + YAML frontmatter | The product itself |
| Tooling | **Python 3** (stdlib-first) | Works on 3.10+; developed/tested here on Python 3.14 |
| Installers / gates | **Bash** | Must remain compatible with **bash 3.2** (macOS default) |
| Eval harnesses | **Node.js ≥ 16** (plain CommonJS) | No npm dependencies; uses `fs`, `path`, `child_process` only |
| CI | GitHub Actions (Ubuntu) | Python 3.11 + PyYAML installed in the workflow-graphs job |
| Compiled output | XML via `scripts/_compile_skill.py` | Written to `.skills-compiled/` (gitignored) |

**Optional dependency:** `PyYAML`. `scripts/validate_chains.py` and `scripts/emit-skill-graph.py`
require it and exit with `ERROR: PyYAML required. Install with: pip install pyyaml` when absent.
`scripts/validate-skills.sh` falls back to the stdlib shim `scripts/yaml_shim.py` when PyYAML is
missing, so the main governance suite still runs offline. Install PyYAML before working on chain
symmetry or the graph explorer:

```bash
python3 -m pip install pyyaml
```

> The engine and manifest validators (`workflow-runner.py`, `validate-workflows.py`,
> `lib/safe_yaml.py`) use a **strict stdlib-only YAML subset** — no PyYAML needed, and features
> outside the subset (anchors, flow maps, block scalars) are rejected loudly.

---

## 4. Build, index, and compile commands

There is no compile step required to use the skills. These commands regenerate derived artifacts;
**regenerate them in the same commit that changes their source** so CI never sees a stale pair.

```bash
# Rebuild the flat discovery layer after adding/renaming/removing a skill
bash scripts/build-flat-index.sh          # -> skills-flat/<name> symlinks (committed)
python3 scripts/check-flat-index.py       # invariant check: count, collisions, broken links

# Compile human-readable SKILL.md -> minified XML for LLMs
bash scripts/compile-skills.sh --all      # -> .skills-compiled/**/skill.xml (gitignored)
bash scripts/compile-skills.sh --verify
python3 scripts/check-token-budget.py     # compile coverage + declared budget gate

# Regenerate committed generated artifacts
python3 scripts/emit-skill-graph.py       # -> docs/graph-explorer/{index.html,skill-graph.json}
python3 scripts/emit-skill-graph.py --check        # freshness gate (CI runs this)
python3 scripts/emit-marketplace.py       # -> .claude-plugin/marketplace.json + plugins/
python3 scripts/emit-marketplace.py --check
python3 scripts/emit-skill-registry.py --check
```

**Invariant:** `skills/` is nested two levels; agent scanners only look one level deep. The
committed `skills-flat/` symlink layer is what every installer links. If you add a skill, rebuild
it, or discovery silently breaks.

---

## 5. Linting and validation

### Fast, per-file gates (run after each edit)

```bash
python3 scripts/lib/lint-template.py skills/<domain>/<name>/SKILL.md   # 22-section compliance
python3 scripts/lib/lint-yaml.py     skills/<domain>/<name>/SKILL.md   # frontmatter
python3 scripts/lib/lint-markdown.py skills/<domain>/<name>/SKILL.md   # markdown style
python3 scripts/lib/lint-workflow.py skills/<domain>/<name>/SKILL.md   # workflow: block (if present)
python3 scripts/lib/lint-files.py    --changed                         # UTF-8/LF/whitespace
python3 scripts/lib/lint-shell.py    --changed                         # bash hygiene
```

### Full suite

```bash
bash scripts/lint.sh                  # changed files
bash scripts/lint.sh --all            # whole repo
bash scripts/lint.sh --fix            # auto-fix formatting
bash scripts/lint.sh --all --ci       # CI mode (--all --errors-only --json)
bash scripts/validate-skills.sh       # 14-gate governance suite (blocking)
python3 scripts/validate_chains.py    # chain symmetry (needs PyYAML)
python3 scripts/validate-workflows.py --all
```

`scripts/lint.sh` supports categories `markdown,yaml,shell,files,template`. Exit codes:
`0` clean, `1` errors, `2` linter crashed.

### Git hooks — install once per clone

```bash
git config core.hooksPath .githooks    # or: bash scripts/install-hooks.sh
```

- **`.githooks/commit-msg`** — strips `Co-authored-by: ... Copilot` trailers (Copilot CLI adds
  them automatically; human co-authors are preserved). Merge/rebase/cherry-pick are exempt.
- **`.githooks/pre-commit`** — runs the gate suite on staged files (G0–G16; the header text calls
  it "17 gates", the banner says "16-Gate" — the gate list in the file is authoritative):
  G0 script SHA256 integrity, G1 file format, G2 shell, G3 JSON, G4 YAML frontmatter, G5 markdown,
  G6 template compliance (with `--delta` so pre-existing violations don't block), G7 ≥8
  "Complete when" criteria, G8 ≥3 decision trees, G9 chain connectivity, G10 reference link
  integrity, G11 per-skill artifacts, G12 portability target, G13 example validation, G14 deep
  research gate, G15 workflow contracts + engine self-tests, G16 golden evals for changed skills.
- **`.githooks/pre-push`** — blocks on any commit containing a Copilot co-author trailer, then runs
  `scripts/run-ci-locally.sh`, a local mirror of `validate.yml`.

### CI

`.github/workflows/validate.yml` ("Skills Governance Gate") runs jobs: `validate`, `hooks`, `lint`
(markdownlint + reference link check), `graph-explorer` (freshness), `workflow-graphs`
(manifest selftest + `--all`, engine selftest, golden evals, a repo self-check dogfood run,
benchmark), and `measurement` (compile + token budget + registry + routing + session-start guard).
`.github/workflows/test-plugin-install.yml` does end-to-end install tests asserting skill counts
(computed from the corpus, 8 solo, 18 grow) and npm tarball contents. `.github/workflows/deploy-pages.yml`
publishes `docs/graph-explorer/` to GitHub Pages.

> **Count drift:** the install E2E now **computes** the expected count from the corpus rather than
> hardcoding it, so adding a skill cannot break it. Prefer computed counts everywhere for this
> reason — a frozen number rots silently (it once asserted 298 against a 322-skill corpus).

---

## 6. Testing and evaluation

The repo has a **3-tier evaluation system**, all runnable locally:

```bash
bash scripts/run-evals.sh                 # Tier 1: structural (default)
bash scripts/run-evals.sh --tier all      # all tiers
bash scripts/run-evals.sh --tier 2        # TF-IDF routing precision
bash scripts/run-evals.sh --tier 3        # behavioral (headless agent)
bash scripts/run-evals.sh --suite <suite-id>
bash scripts/run-evals.sh --json          # CI-friendly
```

| Tier | What it tests | Driver | Corpus |
|---|---|---|---|
| 1 | Structural: frontmatter, sections, validators | `evals/evals.json` via `run-evals.sh` | `evals/evals.json` |
| 2 | Routing: does a prompt reach the right skill? | `scripts/run-routing-evals.js` | `evals/tier2-routing-evals.json`, `evals/tier2-routing-adversarial.json` |
| 3 | Behavioral: headless agent output vs expectations | `scripts/run-behavioral-evals.js` | `evals/tier3-behavioral/` |

Additional harnesses:

```bash
bash scripts/eval-skill.sh --all          # golden per-skill regression cases (CI merge gate)
bash scripts/eval-skill.sh <skill> transcript.txt   # score a live output
python3 scripts/behavioral-evals.py
python3 scripts/benchmark-skills.py --root skills --markdown
python3 scripts/run-effectiveness.py      # score any run 0-100
python3 scripts/audit-library.py --brief  # library quality score
```

`npm test` is wired to `bash scripts/run-evals.sh`; `npm run validate` and `npm run lint` map to the
governance suite and master linter. `prepublishOnly` runs lint + validate.

**The engine's own tests are the fastest confidence check** (no agent, no cost):

```bash
python3 scripts/workflow-runner.py --selftest     # expect: selftest: 20 checks, 0 failed
python3 scripts/validate-workflows.py --selftest
python3 scripts/validate-workflows.py --all
python3 scripts/workflow-runner.py --manifest workflow/manifests/senior-dev-loop.yaml
```

---

## 7. Skill authoring conventions

This is the most important section if you are adding or editing a skill.

### Directory shape (`skills/<domain>/<name>/`)

```
<name>/
├── SKILL.md           # required — instructions, workflow, checklist
├── scripts/           # per-skill deterministic tools (verify-skill.sh lives here)
├── references/        # deep knowledge loaded on demand (317/322 skills have this)
├── examples/          # worked scenarios (128/322)
├── evals/             # per-skill eval data (224/322)
└── assets/            # templates/samples (7/322)
```

### Frontmatter

Required by validators: `name`, `description`, `license`.
Conventional and expected: `tags`, `author`, `type`, `status`, `version`, `updated`,
`token_budget`, `chain`.

Key rules:
- `name` **must equal the directory name** and be kebab-case.
- `description` must use the `Use when… Handles… Do NOT use…` trigger format and be **≤1024
  characters** (a warning fires at ≥900).
- `token_budget` is typically **2500–5000**, proportional to body length.
- `chain.consumes_from` and `chain.feeds_into` must both be present and **bidirectionally
  symmetric**: if A `feeds_into` B, then B must `consumes_from` A. Verify with
  `python3 scripts/validate_chains.py` (requires PyYAML).
- Optional `workflow:` block declares a node contract for graph use: `artifacts.inputs/outputs`,
  `completion.criteria`, `completion.evidence: required|optional`, `iteration.max`,
  `iteration.on_exhaustion`, `escalate_to`. This is **additive** — a skill without it lints clean
  and runs in default mode. Lint with `scripts/lib/lint-workflow.py`.

### Required body sections

`scripts/lib/lint-template.py` enforces this set (22 headings; see
`scripts/references/10-10-template.md` for the canonical spec and `CONTRIBUTING-SKILLS.md` for the
authoring walkthrough):

Route the Request · Ground Rules · The Expert's Mindset · Operating at Different Levels · When to
Use · When NOT to Use · Decision Trees · Core Workflow · Best Practices · Error Decoder ·
Error Recovery · Cross-Skill Coordination · Proactive Triggers · Anti-Patterns · State Log ·
Production Checklist · What Good Looks Like · Verification Guardrails · Deliberate Practice ·
References · Gotchas · Anti-Rationalization

Additional gates: **≥3 decision trees** under `## Decision Trees`, **≥8 "Complete when"**
completion criteria, anti-patterns/gotchas present, and progressive-disclosure markers
`<!-- QUICK: 30s -->`, `<!-- STANDARD: 3min -->`, `<!-- DEEP: 10+min -->`.

`00-framework` skills are excluded from several template checks in `validate-skills.sh` and the
pre-commit hook (they are meta-skills with a different shape).

### Authoring workflow

```bash
bash scripts/scaffold-skill.sh 05-development/my-new-skill   # scaffold with all sections
# …fill frontmatter and body, linting after each section…
bash scripts/validate-skills.sh
python3 scripts/validate_chains.py
bash scripts/build-flat-index.sh
python3 scripts/check-flat-index.py
python3 scripts/emit-marketplace.py
```

Then test with at least one real agent before opening a PR. New skills are expected to be **10/10**
on the quality bar (`SKILL-QUALITY-STANDARDS.md`), not merely structurally valid.

### Design principles for skill content

- **Universal by default, specific by reference** (`AGNOSTIC-PRINCIPLES.md`) — write domain-agnostic
  guidance; keep industry/regulatory specifics in `references/`.
- **Scale-aware** (`SCALE-DEPTH-FRAMEWORK.md`) — every skill covers Solo → Small → Medium → Enterprise.
- **Actionable, concrete, opinionated** — decision trees, tables, metrics, code patterns; no
  hand-waving. "No fluff — if a sentence doesn't help someone DO something, cut it."

---

## 8. Workflow engine (loops and graphs)

Control flow is **code**; content is **agentic**. The engine walks a manifest, and an executor
supplies node content.

```bash
python3 scripts/validate-workflows.py --all        # structure, cycles, budgets, payloads, reachability
python3 scripts/validate-workflows.py --coverage   # prove all skills resolve as nodes
python3 scripts/validate-workflows.py --selftest
python3 scripts/workflow-runner.py --manifest workflow/manifests/<name>.yaml \
    --executor scripts/executors/repo_checks.py --state /tmp/state.json --memory /tmp/memory
python3 scripts/workflow-runner.py --manifest <path> --enforce-contracts   # opt-in contract gate
```

Semantics implemented by the runner (see `WORKFLOW-SYSTEM.md` for the formal spec):
- A node runs when incoming edges are satisfied; edges inside an active loop are suppressed until
  the loop exits.
- A loop pass runs each member once in declared order; `exit_when`, `max_iterations`, and
  stagnation (`convergence.window` identical diagnostics) govern exit; exhaustion routes to
  `escalate_to` or ends.
- Run state is checkpointed after **every** node, so a crash keeps completed work and resumes only
  the failed node.
- Handoffs are recorded as `{from, to, payload, sha}`.
- `--enforce-contracts` (off by default) requires declared evidence and criterion coverage; a
  violation retries inside a loop or escalates outside one.
- Executors may report `usage = {tokens_in, tokens_out, cost_usd}`; unmeasured cost is flagged, never
  treated as free. Manifests can cap `budget.max_steps` and `budget.max_cost_usd`.

Manifest shapes covered by the 6 committed manifests: serial single-agent, bounded loop with an
agent gate then a human gate, parallel multi-agent fan-out with join, and the flagship micro-SDLC
loop. `workflow/tests/fixtures/` powers the validator self-test.

The **MCP server** (`scripts/mcp-skill-server.py`, registered in `.mcp.json`, documented in
`docs/mcp-server.md`) exposes 8 tools over stdio — `list_skills`, `get_skill`,
`get_skill_contract`, `search_skills`, `get_skill_graph`, `list_workflows`, `validate_manifest`,
`run_workflow` — reusing the repo's own parsers and validator rather than re-implementing them.

---

## 9. Distribution and installation

Single source of truth: `scripts/init-project.sh` (project activation) and `scripts/install.sh`
(global install). All install channels delegate to these.

```bash
# Shell install (global) — clones to ~/.zeroes-ones/skills + global agent symlinks
curl -sSL https://raw.githubusercontent.com/zeroes-ones/Skills/main/scripts/install.sh | bash

# npm
npx @zeroes-ones/skills init

# Project activation (from an installed library)
skills-init                # all skills (one symlink to skills-flat)
skills-init --solo         # 8 skills  (SOLO_SKILLS list in init-project.sh)
skills-init --grow         # 18 skills (SOLO + 10 more)
skills-init --status       # report current tier
skills-update              # pull latest library
```

Activation links 10 agent directories: `.agents/skills`, `.claude/skills`, `.copilot/skills`,
`.github/skills`, `.cursor/skills`, `.codex/skills`, `.gemini/skills`, `.windsurf/skills`,
`.cline/skills`, `.opencode/skills`. Full mode symlinks the whole `skills-flat`; tier modes symlink
individual skill dirs by name. Existing non-symlink directories with content are **never deleted** —
the installer skips them with a notice. Mode switching replaces only the installer's own links.
`npm` bin entries (`package.json`): `skills`, `skills-init`, `skills-update`, `skills-validate`,
`skills-lint`; `scripts/npx-skills.sh` dispatches `init | update | validate | lint`.

Install exit criteria and the external (owner-owned) publish/index gates are enumerated in
`docs/install-exit-criteria.md`.

---

## 10. Code and file style

Enforced by `.editorconfig`, the lint suite, and CI:

| Rule | Value |
|---|---|
| Encoding / line endings | UTF-8, **LF** |
| Final newline | required |
| Trailing whitespace | forbidden |
| Tabs | forbidden (indent with spaces) |
| Indent | 2 spaces (default and Markdown/shell/YAML/JSON/JS), **4 spaces for Python** |
| Shell | shebang, `set -euo pipefail`, `[[ ]]` over `[ ]`, `$()` over backticks, `read -r`, trap cleanup; must run under bash 3.2 |
| Python | stdlib-first; keep tools dependency-free unless unavoidable |
| Markdown | `.markdownlint.json` config (many rules disabled by design — 30 explicit opt-outs) |

Commit messages follow a conventional-commit style observed in history:
`feat(skills): …`, `fix(hooks): …`, `chore(integrity): …`, `docs+mcp: …`, `test(examples): …`.
Commits are expected to be atomic; do not bundle formatting churn with logic changes.

Script integrity: `scripts/generate-sha256-manifest.sh` maintains `scripts/.sha256manifest` (~430
hashed entries; the file's own header comment says 415). The pre-commit G0 gate regenerates and
verifies it whenever scripts change — if you edit a script, expect the manifest to be re-staged.

---

## 11. Commit / push cadence and CI cost

Policy lives in `docs/git-ci-efficiency.md`. The short version:

1. Run cheap local gates per edit; run the expensive full suite once per push, not per commit.
2. Local checks are free; CI credits are not. `bash scripts/run-ci-locally.sh` mirrors CI.
3. Batch related pushes — CI uses `concurrency` with `cancel-in-progress: true`.
4. Keep generated artifacts fresh in the same commit as their source.
5. Push when the touched scope is green and the change is one logical unit; skip re-runs for
   docs-only or regenerated-artifact-only changes.

---

## 12. Security considerations

- **Secrets:** this repo contains no credentials and handles none. `.gitignore` excludes `.env*`;
  the dedicated tools refuse to read secret files. Never introduce a real secret or token.
- **Script integrity:** `scripts/.sha256manifest` + G0 gate detect tampered tooling. Treat a
  manifest mismatch as a real signal, not noise.
- **Installer safety:** installers never delete pre-existing user skill directories, and reset
  logic only removes symlinks pointing back into this library's own store paths. Preserve that
  property in any installer change.
- **Local execution permissions:** `reasonix.toml` declares allow-listed Bash patterns and a narrow
  `sandbox.allow_write` list. It is a local agent-runtime config, not part of the shipped library —
  update it only when you deliberately need a new local capability.
- **Hook guardrails:** `hooks/always-on-principles.md` (single source of truth, injected at session
  start) and `hooks/SIMPLIFY-IGNORE.md` protect marked code from accidental deletion;
  `hooks/SDD-CACHE.md` caches WebFetch responses with HTTP revalidation. Hook tests:
  `bash hooks/session-start-test.sh`, `bash hooks/simplify-ignore-test.sh`.
- **Untrusted input:** manifest parsing deliberately uses a strict, small YAML subset
  (`scripts/lib/safe_yaml.py`) that rejects anchors/aliases/flow maps and fails with a line number —
  keep it strict; do not swap in a permissive parser.
- **Publishing gates:** `npm publish` (EC-6) and skills.sh indexing (EC-9) are owner actions by
  design; they require credentials this repo must not hold.

---

## 13. Known discrepancies and gotchas

These are real and observed in this checkout — do not be surprised by them:

1. **Skill counts in prose were stale** (297–304 vs actual). Trust the filesystem; see the
   caveat in §1.
2. **`validate-skills.sh` reports "314 skills"** for section checks because it excludes
   `00-framework` (6 skills) from several gates. The audit reports the full corpus.
3. **`validate_chains.py` and `emit-skill-graph.py` need PyYAML** and fail without it;
   `validate-skills.sh` falls back to `scripts/yaml_shim.py` and reports chain symmetry as
   "advisory (non-blocking)" in that case.
4. **The install E2E workflow now computes its expected count** from the corpus, so it cannot
   drift. (It previously asserted a hardcoded 298.)
5. **Pre-commit gate numbering** in the header (17) vs banner (16) disagree; the implemented gate
   list (G0–G16) is authoritative.
6. **`skills-flat/` and `plugins/` are committed generated artifacts.** Edit the source
   (`skills/`, `flagship/`), then regenerate; never hand-edit symlink layers.
7. **`.skills-compiled/` is gitignored** build output and can drift from `skills/`; regenerate
   with `compile-skills.sh --all` when you need it.
8. **Working tree may be dirty** with in-flight skill additions (e.g. new `caching-architect`,
   `verification-independence-engineer`) and regenerated artifacts. Check `git status` before
   assuming a clean baseline, and do not revert unrelated in-progress work.

---

## 14. Quick-reference command card

```bash
# Confidence checks (fast)
python3 scripts/workflow-runner.py --selftest
python3 scripts/validate-workflows.py --all
bash hooks/session-start-test.sh

# Authoring a skill
bash scripts/scaffold-skill.sh <domain>/<name>
python3 scripts/lib/lint-template.py skills/<domain>/<name>/SKILL.md
python3 scripts/lib/lint-workflow.py skills/<domain>/<name>/SKILL.md
bash scripts/build-flat-index.sh && python3 scripts/check-flat-index.py

# Before commit / push
bash scripts/lint.sh --all
bash scripts/validate-skills.sh
bash scripts/run-ci-locally.sh
bash scripts/eval-skill.sh --all

# Library health
python3 scripts/audit-library.py --brief
python3 scripts/check-token-budget.py
python3 scripts/emit-skill-graph.py --check
python3 scripts/emit-marketplace.py --check
```

### Where to read more

| Topic | Document |
|---|---|
| Plain-language overview | `docs/START-HERE.md`, `docs/HOW-IT-WORKS.md` |
| Skill authoring walkthrough | `CONTRIBUTING-SKILLS.md` |
| Quality bar / scoring rubric | `SKILL-QUALITY-STANDARDS.md` |
| Canonical 22-section template | `scripts/references/10-10-template.md` |
| Workflow spec | `WORKFLOW-SYSTEM.md`, `workflow/manifests/README.md` |
| MCP server | `docs/mcp-server.md` |
| Agent discovery layout | `docs/agent-support-matrix.md` |
| Install exit criteria | `docs/install-exit-criteria.md` |
| Git/CI cost policy | `docs/git-ci-efficiency.md` |
| Cross-skill dependency graph | `COORDINATION-MATRIX.md`, `SUB-SKILL-MAP.md` |
