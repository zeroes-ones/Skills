# Flagship: Senior Engineering & Micro-SDLC

**The one coherent story we want to win:** *a senior engineer who executes tight, verified
build loops* — and the repo itself is the artifact of that loop (every push runs a 16-gate
pre-commit; the repo self-checks as a workflow graph in CI).

Source of truth: [`flagship/senior-engineering.json`](../flagship/senior-engineering.json)
(machine-readable — powers the `plugins/flagship-senior-engineering` Claude plugin and this
page). Install in one command inside Claude Code:

```
/plugin install flagship-senior-engineering@zeroes-ones-skills
```

Executable story: [`workflow/manifests/senior-dev-loop.yaml`](../workflow/manifests/senior-dev-loop.yaml)
— incremental-implementation → code-reviewer in a bounded loop that exits only on
`review.verdict == pass` and escalates to a human ship gate at exhaustion (validated by
`python3 scripts/validate-workflows.py`, engine self-tests green).

## The three axes (10 skills each)

| Axis | Idea | Skills |
|------|------|--------|
| **micro-sdlc** | The loop: plan → implement → test → review → verify → ship, iterated until verification passes | `incremental-implementation`, `tdd-guide`, `verification-before-completion`, `source-driven-development`, `iterative-task-execution`, `code-reviewer`, `qa-engineer`, `debugging-and-error-recovery`, `code-simplification`, `shipping-and-launch` |
| **senior-core** | Core senior engineering: architecture, design, secure-by-default, performance | `system-architect`, `codebase-design`, `api-designer`, `database-designer`, `event-driven-architect`, `backend-developer`, `networking-engineer`, `secure-api-design`, `performance-engineer`, `merge-conflict-resolver` |
| **senior-systems** | Systems & leadership: platform/codebase ownership, dependency governance, senior modes, staff/EM judgment | `senior-engineer-mode-router`, `staff-engineer`, `engineering-manager`, `platform-engineer`, `dependency-governance`, `monorepo-manager`, `repo-scaffolding`, `multi-agent-orchestration`, `cross-repo-refactoring`, `cloud-architect` |

## Measured baseline (2026-09-07, computed from the tree)

| Skill | Axis | Domain | token_budget | chain degree | body words |
|-------|------|--------|------|------|------|
| code-reviewer | micro-sdlc | quality | 3000 | 23 | 10,528 |
| code-simplification | micro-sdlc | quality | 4000 | 9 | 9,338 |
| debugging-and-error-recovery | micro-sdlc | quality | 5000 | 9 | 10,612 |
| incremental-implementation | micro-sdlc | development | 3500 | 9 | 4,045 |
| iterative-task-execution | micro-sdlc | specialized | 4700 | 7 | 5,356 |
| qa-engineer | micro-sdlc | quality | 4000 | 63 | 11,042 |
| shipping-and-launch | micro-sdlc | devops | 4000 | 13 | 9,595 |
| source-driven-development | micro-sdlc | development | 4000 | 4 | 8,062 |
| tdd-guide | micro-sdlc | quality | 3800 | 12 | 9,807 |
| verification-before-completion | micro-sdlc | quality | 4000 | 5 | 9,667 |
| api-designer | senior-core | architecture | 4000 | 28 | 9,714 |
| backend-developer | senior-core | development | 5000 | 85 | 9,655 |
| codebase-design | senior-core | architecture | 4000 | 7 | 8,474 |
| database-designer | senior-core | architecture | 4000 | 24 | 10,237 |
| event-driven-architect | senior-core | architecture | 4000 | 11 | 8,261 |
| merge-conflict-resolver | senior-core | devops | 4000 | 5 | 9,310 |
| networking-engineer | senior-core | architecture | 4000 | 12 | 11,050 |
| performance-engineer | senior-core | specialized | 4000 | 25 | 9,928 |
| secure-api-design | senior-core | architecture | 4500 | 4 | 11,727 |
| system-architect | senior-core | architecture | 4000 | 48 | 12,824 |
| cloud-architect | senior-systems | devops | 4000 | 18 | 8,585 |
| cross-repo-refactoring | senior-systems | specialized | 5000 | 6 | 10,071 |
| dependency-governance | senior-systems | devops | 4000 | 6 | 10,676 |
| engineering-manager | senior-systems | engineering-leadership | 5000 | 14 | 11,058 |
| monorepo-manager | senior-systems | specialized | 4000 | 13 | 9,728 |
| multi-agent-orchestration | senior-systems | specialized | 4700 | 10 | 7,943 |
| platform-engineer | senior-systems | devops | 3525 | 18 | 10,052 |
| repo-scaffolding | senior-systems | devops | 4000 | 4 | 10,900 |
| senior-engineer-mode-router | senior-systems | framework | 3500 | 12 | 5,090 |
| staff-engineer | senior-systems | engineering-leadership | 4000 | 11 | 10,184 |

Totals: 30 skills · Σ token_budget = 123,225 · Σ body words = 283,519. All 30 pass the
library's governance suite (14/0) as part of the 298. Note: these are **deep** skills; agents
never load full bodies — they load only the invoked skill's needed sections (progressive
disclosure) or the compiled excerpts (`.skills-compiled/`, 63.4% load saving), so the flagship
story is *density on demand*, not 283k tokens in context.

## What "superior" means here (acceptance criteria)

1. **Every flagship skill passes the full governance suite** (`bash scripts/validate-skills.sh`:
   14 checks) — enforced for the whole library already, tracked per skill in CI reports.
2. **The loop is executable and verified**: `senior-dev-loop.yaml` validates
   (`validate-workflows.py --all`) and the engine's loop protocol (exit_when / max_iterations /
   escalate_to / convergence) is covered by self-tests (23 checks green).
3. **The set is one command to install** in Claude Code: `plugins/flagship-senior-engineering`
   (30 skills), generated idempotently by `scripts/emit-marketplace.py` and checked fresh in CI.
4. **Improvements are measured, not claimed**: any depth/quality change to a flagship skill
   reports its delta on this table (token_budget, body words) and runs the golden evals before
   promotion (see BEYOND-LOOPS-GRAPHS.md §5 — measure before shipping, verification-gated
   promotion).

## Maintenance

- Edit the set in `flagship/senior-engineering.json`, then:
  `python3 scripts/emit-marketplace.py` (regenerates `plugins/flagship-senior-engineering/`
  and `.claude-plugin/marketplace.json`; CI's `emit-marketplace.py --check` fails on drift).
- Add the flagship manifest row to `workflow/manifests/README.md` when the story changes.
