# Skill Automation Platform — Build & Verification Log

> **Version 1.0.0** — the detailed, evidence-backed record of what was built, what was measured, what
> broke, and what remains open. Every number carries the command that produced it; every claim is
> either a command output or an artifact in this repository. Companion to
> [`skill-automation-platform.md`](skill-automation-platform.md), which holds the *design and gap
> plan*; this file holds the *record of execution*.
>
> **Provenance:** recorded against `HEAD = 64ee2fc2` with all changes uncommitted in the working
> tree. Counts were 304 skills / 37 domains at the time of writing.

## 1. What was built, at a glance

| # | Deliverable | Type | Status | Where |
|---|-------------|------|--------|-------|
| 1 | n8n-class platform design + gap register A1–A9 + 5-phase roadmap | design doc | delivered | `docs/skill-automation-platform.md` |
| 2 | Phase 1 items 1–2: a real agentic run, end to end, archived | measured evidence | **delivered** | `examples/phase1-agentic-node/` |
| 3 | Phase 1 item 3: the L2→L3 delta on one skill | analysis | **delivered** | `examples/phase1-agentic-node/README.md` §"The L2 → L3 delta" |
| 4 | Phase 1 item 4: node contracts **30 → 43** skills | 13 × `SKILL.md` | **delivered** | `skills/**/SKILL.md` |
| 5 | Defects **D1/D2/D3** found by the real run, fixed and guarded | engine + executor code | **fixed + tested** | `scripts/workflow-runner.py`, `scripts/executors/agent_executor.py` |
| 6 | Pre-existing CI failure (stale graph explorer) repaired | generated artifacts | **fixed** | `docs/graph-explorer/` |
| 7 | **Contract enforcement** implemented (`--enforce-contracts`) — the engine asserts declared criteria against a node's evidence | engine code + 4 tests | **delivered + tested** | `scripts/workflow-runner.py` |
| 8 | This log | record | delivered | `docs/skill-automation-platform-build-log.md` |
| 9 | Plain-language guide to the whole system | explainer | delivered | `docs/HOW-IT-WORKS.md` |

## 2. The real agentic run (Phase 1 items 1–2)

### 2.1 The command

```bash
cd <repo root>
AGENT_CMD='claude -p' AGENT_FALLBACK=0 \
  python3 scripts/workflow-runner.py \
    --manifest workflow/manifests/senior-dev-loop.yaml \
    --executor scripts/executors/agent_executor.py \
    --guardrail scripts/lib/guardrails.py \
    --memory examples/phase1-agentic-node/memory \
    --state examples/phase1-agentic-node/run-state.json
```

Result: **runner exit=0**.

`AGENT_FALLBACK=0` is mandatory for any claim drawn from this run: the executor's default (`1`)
returns a stub `pass` when an agent call fails or times out, so a "successful" run under the default
proves nothing about node content.

### 2.2 The three agent turns

Every turn is a genuine model call (`fallback=false` in the transcript), grounded in that node's
compiled skill excerpt injected into the prompt.

| Turn | Node | Skill injected | Skill words | Verdict | Seconds |
|------|------|----------------|-------------|---------|---------|
| 1 | `implement` | `incremental-implementation` | 405 | `changes_requested` | 331.2 |
| 2 | `review` | `code-reviewer` | 1,200 | **`pass`** | 60.5 |
| 3 | `ship-gate` | — (gate node) | 0 | `pass` | 115.4 |

### 2.3 Outcome and handoff

```
outcome      = complete
steps_used   = 3   (budget 40)
iterations   = micro-sdlc-loop: 1
nodes        = implement done/changes_requested · review done/pass · ship-gate done/pass
handoff      = {from: review, to: ship-gate, payload: handoff-v1, sha: 176099b50f3b}
open_questions = []
```

The loop exited on its **declared** condition `exit_when: review.verdict == pass` after one
iteration — not by exhaustion, and not by budget.

### 2.4 What the nodes actually did

They did not summarise a handoff payload — they read the working tree:

- **`implement`** statically verified the in-flight D1/D2 changes and the regenerated
  `.sha256manifest`, and reported finding a defect of its own.
- **`review`** produced a line-level code review of ~110 changed lines: confirmed `_crash_checkpoint`
  soundness, that the exception is re-raised *after* checkpointing, and that `save_state` no-ops on a
  `None` path.

### 2.5 Archived evidence

| File | What it is |
|------|------------|
| `run-state.json` | The checkpoint: per-node status/verdict/iterations, budget, handoff, log |
| `agent-transcript.jsonl` | One JSON line per agent turn (node, verdict, seconds, `fallback`, prompt words, reply excerpt) |
| `run-traces.jsonl` | 4 OTel-shaped spans (`session.senior-dev-loop` + 3 node spans) |
| `sli-report.txt` | 1 run · 1 complete · **escalation rate 0.00** · avg 3.0 steps |
| `effectiveness.txt` | **100/100** |
| `run-summary.json` | The runner's JSON summary |
| `memory/senior-dev-loop.jsonl` | Durable run-memory entry (`trust: context_only`) |
| `README.md` | Narrative: command, results, defects, limits |

Effectiveness breakdown (`run-effectiveness.py --state … --memory`):

| Points | Dimension |
|--------|-----------|
| 25 | completion — reached a terminal `complete` state |
| 20 | clean — no escalation/guardrail in the log |
| 15 | exit-by-design — exit condition, not exhaustion |
| 15 | handoffs — payload present at the final boundary |
| 10 | questions — no dangling open questions |
| 10 | budget — `steps_used <= max_steps` |
| 5 | memory — run-memory entry written |
| **100** | **total** |

### 2.6 Reproduce the observability artifacts

```bash
python3 scripts/export-traces.py --state examples/phase1-agentic-node/run-state.json
python3 scripts/skill-sli-report.py --dir examples/phase1-agentic-node
python3 scripts/run-effectiveness.py --state examples/phase1-agentic-node/run-state.json --memory
```

## 3. Defects found by the run

The **first** attempt at the run failed (exit 1). That failure is the most valuable output of Phase 1:
it produced D1 and D2, both of which would have silently degraded every later phase.

### D1 — the default per-node timeout could never complete a real node

| | |
|---|---|
| **Symptom** | `subprocess.TimeoutExpired` on the loop's second `implement` call; run aborted |
| **Root cause** | `AGENT_TIMEOUT` defaulted to `90`s. Measured reality: 149.6s for one node, >180s for the next |
| **Fix** | Default raised to `600`s in `scripts/executors/agent_executor.py`, with the measurement recorded in the docstring |
| **Proof** | The subsequent full run completed all three turns (331.2 / 60.5 / 115.4s) within the new budget |

### D2 — a crashing node discarded the entire run-state

| | |
|---|---|
| **Symptom** | The run exited 1 with **no `run-state.json` on disk at all** — two completed nodes of real work lost |
| **Root cause** | `save_state` was called only *after* a loop pass returned. An exception inside the pass propagated out of `run()`, so the checkpoint was never written. `--state` resume was therefore impossible for exactly the runs that need it |
| **Fix** | New `Runner._crash_checkpoint(node, exc)` logs an `action: error` entry and checkpoints **before** re-raising; node execution is wrapped in `try/except BaseException` at both execution sites (`_run_loop_pass` and the non-loop path of `run()`); `save_state` now runs after **every** completed node |
| **Proof** | New `--selftest` fixture `t-crash-checkpoint`: a node raises mid-loop; asserts the run raised, the checkpoint exists, the earlier node is `done`, the crashed node is not, and an `error` entry is logged. Suite went 11 → **12 checks, 0 failed** |

Semantics after the fix: completed nodes keep `status=done`; the crashed node stays not-done and
re-runs on resume. The module docstring was corrected in the same change — it had claimed
"run-state is written after every node", which was false inside a loop pass.

### D3 — `save_state` wrote no final newline

| | |
|---|---|
| **Symptom** | The archived `run-state.json` failed the repo's own `FMT004` (file does not end with a newline) |
| **Root cause** | `json.dump` writes no trailing newline; the repo's committed state files (`examples/workflow-runtime/state/*.json`) all end in `0a` |
| **Fix** | `save_state` writes `"\n"` after the JSON; the archived copy was normalised too |
| **Proof** | `lint-files.py` over all 8 archived artifacts: no formatting issues |

D3 was found *by running the repo's own linters against the new artifacts*, not by reading code.

## 4. Node contracts — coverage 30 → 43 (Phase 1 item 4)

### 4.1 The contract shape (L0, per `scripts/lib/lint-workflow.py`)

```yaml
workflow:
  artifacts:
    inputs: [name, ...]        # optional list of strings
    outputs: [name, ...]       # optional list of strings
  completion:
    criteria: ["...", ...]     # default source: the skill's Verification section
    evidence: required         # required | optional
  iteration:
    max: 3                     # int >= 1
    on_exhaustion: escalate    # escalate | next | fail
  escalate_to: [target, ...]   # node ids or skill names
```

Allowed top-level keys are exactly `artifacts`, `completion`, `iteration`, `escalate_to`; unknown
keys and type violations are **errors**, so typos fail loudly instead of silently changing loop
behaviour.

### 4.2 How the 14 targets were chosen

Not by guesswork — by asking the library which skills its own workflows exercise:

```bash
grep -rhoE "^ +skill: [a-z0-9-]+" workflow/manifests/*.yaml examples/*/*.yaml | sed 's/.*skill: //' | sort -u
```

minus the 30 that already declared a block = **exactly 14**, of which 13 shipped (§4.5).

### 4.3 The 14, with the source of their criteria

Every criterion was taken from that skill's existing Verification / Production Checklist. **No
criterion was invented.** Two skills (`token-efficiency`, `writing-great-skills`) appeared to have no
Verification section under a naive heading match; re-checking showed `token-efficiency` carries
criterion lines in its `## Production Checklist` and `writing-great-skills` has an annotated
`## <!-- DEEP: 10+min --> Verification` section.

| Skill | Criteria grounded in |
|-------|----------------------|
| `idea-to-spec` | data provenance, pre-launch success proxies, API contract validates |
| `incremental-implementation` | flag default false, tests both flag states, ADD-only schema |
| `secure-api-design` | pinned algorithms, explicit authorization, parameterized queries |
| `documentation-engineer` | zero-warning build, language-annotated code blocks, WCAG 2.2 AA |
| `deprecation-engineer` | sunset/replacement/migration guide, 30+ day zero-invocation, rollback path |
| `migration-architect` | row-count parity ±0.01%, tested rollback window, cutover runbook |
| `multi-agent-orchestration` | documented topology, typed state ownership, depth/turn caps |
| `release-manager` | owner + threshold per item, tested rollback, changelog with migration guide |
| `customer-support-engineer` | shared investigation doc, SLA acknowledgment, no prod debug modes |
| `agent-eval-pipeline` | same scenario set, deltas not absolutes, 100% safety-critical |
| `context-compaction-strategies` | declared token budget, security text verbatim, saturation band |
| `token-efficiency` | baseline within 10% of bill, caps per task type, cache hit rate |
| `writing-great-skills` | use-when description, mechanical ground rules, verify script passes |

### 4.4 Resulting coverage

```
$ python3 scripts/validate-workflows.py --coverage
coverage: 304 distinct skill names; 304 resolve as workflow nodes
readiness: 301 eligible (default-mode nodes), 43 declared workflow: blocks
```

| | Before | After |
|---|---|---|
| Declared contracts | 30 | **43** |
| `audit-library.py` Workflow Readiness | 1.0 | **1.5** |
| Skills eligible but undeclared | 271 | **258** |

Contracts by domain: development 6/28 · specialized 5/16 · architecture 4/12 · devops 4/17 ·
ai-engineering 4/15 · product 3/6 · quality 3/10 · security 3/11 · design 2/8 · data 2/9.

### 4.5 The one that was reverted — and why it matters

`using-agent-skills` was in the original 14, then removed. It is one of three skills that are **not**
default-mode eligible, because eligibility requires a `Core Workflow` section and it has none — it is
the library *router*, so it routes rather than executing a procedure. Declaring a completion contract
on a skill the readiness metric does not count produced an inconsistent tally: "44 declared" against
"301 eligible", with one declared skill sitting *outside* the eligible set.

Removing it restored the invariant **declared ⊆ eligible** — 43 declared, every one of them inside
the 301 eligible. The skill still works as a node (it is referenced by `agent-efficiency-pass.yaml`,
and coverage confirms all 304 skill names resolve); in default mode its criteria source is its own
Verification table rather than a declared contract. Readiness moved 1.5 → 1.4, which is the more
honest number.

**Generalisable lesson:** a declared-coverage metric is only meaningful when every declared skill is
also eligible. A numerator that can contain items outside its denominator will drift.

**Behavioural impact at run time: none unless enforcement is requested.** The block is additive, and
the engine ignores it in default mode (see §6). What changed is reviewability, machine-checkability,
and the readiness metric.

## 5. The L2 → L3 delta on one skill (Phase 1 item 3)

Specimen: `incremental-implementation` — the exact node the Phase 1 run executed at L2.

| | L2 — default mode (as run) | L3 — declared contract (now) |
|---|---|---|
| Declaration | no `workflow:` block | 12-line frontmatter block |
| Artifacts | unnamed, inferred from manifest `outputs: [change]` | typed `inputs: [spec]` → `outputs: [change]` |
| Definition of done | skill Verification table, consulted at execution time | three explicit criteria |
| Evidence | required only by convention | `evidence: required`, declared |
| Exhaustion | the loop's `escalate_to` only | node declares `escalate_to: [human-gate]` |
| Lint | nothing to lint | `scripts/lib/lint-workflow.py` |
| Counted by | — | `validate-workflows.py --coverage` |

What the run-state recorded for that node:

```
status=done  verdict=changes_requested  iterations=1
evidence=["agent-turn:implement"]  summary=(400 chars)
```

The evidence is real but **undifferentiated**: nothing in the checkpoint says *which* criterion the
verdict was judged against. That is the gap a contract closes.

## 6. Contract enforcement — the limit, and its closure

At the time of the run above, the engine read **only** `manifest.nodes[].skill` and never parsed the
`workflow:` block. Verified then by inspection:

```bash
grep -n "workflow\b\|contract" scripts/workflow-runner.py   # every hit was an unrelated identifier
grep -n "extract_workflow_block\|lint_workflow" scripts/validate-workflows.py   # no hits
```

So a contract bought reviewability, a lintable declaration, a named escalation target and a readiness
metric — **not runtime enforcement**. That limit has since been closed.

### 6.1 What enforcement now does (`--enforce-contracts`, off by default)

`Runner._contract_violations()` loads the node's skill contract and refuses to mark the node done
unless the node substantiates its own completion:

| Requirement | Behaviour |
|---|---|
| `completion.evidence == required` and no evidence reported | **violation** |
| `completion.criteria` declared and no `criteria_met` coverage reported | **violation** |
| `criteria_met` naming an unrecognized criterion | **violation** |
| `criteria_met` omitting one or more declared criteria | **violation**, naming the uncovered ones |
| declared `artifacts.outputs` not produced | `action: contract-warning` (recorded, never blocking) |

References may be indices (`1`, `c2`) or the criterion's own text, so an executor need not invent an
index scheme. On violation the result is rewritten to `status: needs_review` /
`verdict: contract-violation` and an `action: contract` log entry names exactly what was missing, so
normal machinery takes over: **inside a loop** the node is retried and exhaustion escalates to the
loop's `escalate_to`; **outside a loop** the run escalates rather than advancing the graph.

Enforcement is **off by default** deliberately: `repo_checks.py` and the test stub report no
`criteria_met`, so enforcing unconditionally would break every existing run.

### 6.2 Evidence

Four self-tests were added (suite 12 → **16 checks, 0 failed**):

| Check | Proves |
|---|---|
| `contract enforcement blocks an unsubstantiated completion` | a node reporting no evidence is not marked done |
| `contract enforcement is opt-in (default mode unchanged)` | the same manifest still completes with the flag off |
| `a substantiated completion passes contract enforcement` | a node reporting evidence + full coverage still completes |
| `partial criteria coverage is detected and named` | the specific uncovered criterion is named in the log |

And a live A/B on `senior-dev-loop` with the deterministic stub executor:

| | Default (flag off) | `--enforce-contracts` |
|---|---|---|
| Node verdicts | all `pass` | **`contract-violation`** on both loop members |
| Log detail | — | `completion.evidence is 'required' but the node reported no evidence; completion.criteria declares 3 criteria (c1, c2, c3) but the node reported no criteria_met coverage` |
| `run-effectiveness.py` | **95 / 100** | **45 / 100** (clean 0, exit-by-design 0, handoffs 0) |

**Residual limit, stated plainly:** in headless mode the run still reported `outcome: complete`,
because the loop escalated to the terminal `ship-gate` and that human gate is auto-approved by the
headless runner (gap **A4**). The violation is fully recorded and the score collapses 95 → 45, but
"the run finished" and "the work was substantiated" remain two different questions until the human-gate
gap is closed.

Item 3's L2→L3 description therefore still holds for **default mode**: an L3 contract is *checkable*
only when enforcement is requested. It is no longer accurate to say the engine *cannot* check it.

## 7. CI repair — the graph explorer was already stale

| | |
|---|---|
| **Symptom** | `emit-skill-graph.py --check` → `skill-graph.json: STALE`, `index.html: STALE` |
| **Is it ours?** | **No.** Proven by generating a clean `git worktree` at `HEAD` with zero session changes: still stale |
| **Impact** | CI's `graph-explorer` job fails on `main` today |
| **Fix** | Regenerated both artifacts; `--check` now reports ✓ fresh |
| **Determinism** | A second regeneration produced an identical diff — output is idempotent |
| **Scope** | `index.html` 1 line · `skill-graph.json` 627 insertions / 612 deletions |

The generator emitted the **authoritative** graph figures, which also corrected the documentation:

| Metric | Measured (authoritative) | README claimed | COORDINATION-MATRIX.md claimed |
|---|---|---|---|
| Skills / nodes | **304** | 303 | 106 |
| Domains | **37** | 37 | 25 |
| Directed edges | **1,932** | 1,930 | 1,032 |
| Undirected edges | **1,577** | 1,567 | 1,130 |
| Dangling refs | **0** | — | — |
| Avg degree | **10.38** | — | — |

**Hubs** (most-connected skills, i.e. where the library's dependency load concentrates):
`backend-developer` 85 · `using-agent-skills` 66 · `qa-engineer` 63 · `frontend-developer` 62 ·
`system-architect` 48 · `devops-engineer` 45 · `product-manager` 42 · `security-engineer` 42.

This also retires two wrong numbers produced during this session: two ad-hoc edge counters of mine
returned 1,862 and 147 and disagreed with each other. Both were parser bugs. The generator is the
single source of truth; the hand-rolled counters were removed.

## 8. Verification matrix — final state

| # | Gate | Command | Result |
|---|------|---------|--------|
| 1 | Governance (14 checks) | `bash scripts/validate-skills.sh` | **14 PASS / 0 FAIL** |
| 2 | Engine selftest | `python3 scripts/workflow-runner.py --selftest` | **16 checks, 0 failed** |
| 3 | Manifest validation | `python3 scripts/validate-workflows.py --all` | **20 / 20 OK** |
| 4 | Node coverage | `python3 scripts/validate-workflows.py --coverage` | 304/304 resolve · 301 eligible · 43 declared |
| 5 | Contract lint | `python3 scripts/lib/lint-workflow.py --all` | 304 scanned · **0 errors** |
| 6 | Script integrity | `bash scripts/verify-script-integrity.sh` | **412 passed · 0 tampered** |
| 7 | Chain symmetry | `python3 scripts/validate_chains.py` | **PASSED** · 0 asymmetries · 0 dangling |
| 8 | Graph freshness | `python3 scripts/emit-skill-graph.py --check` | **✓ fresh** (was failing — §7) |
| 9 | Markdown (changed docs) | `python3 scripts/lib/lint-markdown.py --errors-only …` | **0 issues** |
| 10 | File format (changed files) | `python3 scripts/lib/lint-files.py …` | **0 issues** on 11 files |

Gates 7 and 8 require PyYAML, which is absent from this environment; both were run by routing
`import yaml` to the repository's own `scripts/yaml_shim.py` — the module that exists for exactly
this case. This is a local-environment workaround, not a repository change.

**Known lint advisory (not introduced here):** `YML009` (frontmatter key ordering) fires on
untouched skills (`chaos-engineer`) and pre-existing declared ones (`code-reviewer`) alike, so it is
repo-wide and pre-existing. It is a warning, and the pre-commit gate runs `--errors-only`.

## 9. Library statistics

### 9.1 Corpus

| Metric | Value |
|---|---|
| Skills | **304** across **37 domains** |
| Avg body size | **8,852 words / 590 lines** |
| Total body | ~2.69M words |
| Portability declared | **100%** |
| Skills over the 500-line advisory | 273 (largest: `marketplace-platform-builder`, 1,186 lines) |
| Largest domains | development 28 · finance 26 · devops 17 · specialized 16 · ai-engineering 15 |

### 9.2 Quality (`python3 scripts/audit-library.py`)

| Dimension | Score | Detail |
|---|---|---|
| Skeleton (must-haves) | 9.9 | 300/301/299/304/301/302/304/304 |
| Error Decoder | 9.8 | 4-col 288 · adapted 10 · missing 6 |
| Best Practices | 10.0 | 298 present · 0 missing |
| Production Checklist | 10.0 | 304 present · 0 missing |
| Scale Depth (L1–L5) | 9.9 | 301/304 |
| Progressive Disclosure | 9.8 | QUICK 294 · STANDARD 294 · DEEP 303 |
| Workflow Readiness | 1.4 ↑ | 43 declared / 301 eligible |
| **OVERALL** | **9.9 / 10** | |

### 9.3 Operational readiness (`skill-incorporate.py`, `benchmark-skills.py`)

| Metric | Value |
|---|---|
| Node contracts | 43 / 304 |
| Default-mode eligible | 301 / 304 |
| Retrieval index | 304 / 304 (lexical) |
| **Golden eval sets** | **3 / 304** ← largest gap |
| Routing baseline (lexical) | Top-1 **50%** · Top-5 **60%** |
| Compiled coverage | 303 / 304 · avg **1,247 tokens** · **85.9%** effective saving |

## 10. Real-time performance profile

| Layer | Real-time cost | Source |
|---|---|---|
| Engine (control flow: traversal, loops, budgets, checkpoints, handoff) | **0.228s** for a 3-node run | live `time` on `quality-fix-loop.yaml`, deterministic stub executor |
| Node content (one real agent turn) | **60.5s – 331.2s** | Phase 1 transcript |
| Checkpoint writes | per node (since D2) | `--state` |

**Insight:** the engine is ~0.2s; agent turns are minutes. **More than 99.9% of wall time is node
content**, which is the concrete argument for the control/content split — optimising graph traversal
buys nothing; skill grounding and prompt design are where time and quality actually live.

### SLIs across archived checkpoints (`skill-sli-report.py`)

| Workflow | Runs | Done | Escalated | Esc rate | Avg steps |
|---|---|---|---|---|---|
| `multi-agent-review-graph` | 2 | 1 | 1 | **0.50** | 16.0 |
| `quality-fix-loop` | 1 | 1 | 0 | 0.00 | 3.0 |
| `senior-dev-loop` (Phase 1) | 1 | 1 | 0 | 0.00 | 3.0 |

The `0.50` is the archived *exhaustion* fixture — evidence that the escalation path fires and is
measurable, rather than merely asserted.

## 11. Open findings and known limits

| # | Finding | Severity | Notes |
|---|---|---|---|
| 1 | ~~Declared criteria are not enforced~~ → **enforcement shipped, opt-in** | Low | Closed in §6: `--enforce-contracts` asserts evidence + criteria coverage, guarded by 4 tests. Residual: off by default, and in headless mode the terminal gate auto-approves so the run still reports `complete` (finding 5) |
| 2 | **Golden eval sets exist for 3 of 304 skills** | High | 99% of the library is structurally but not behaviourally verified |
| 3 | **`COORDINATION-MATRIX.md` is badly stale** (106 skills / 25 domains / 1,032 edges) | Medium | No generator script exists; hand-editing a 29KB table document is risky, so it is recorded rather than patched |
| 4 | **README counts are stale** (303 skills, 1,930 / 1,567 edges) | Low | Correct values are in §7; the graph-explorer section was corrected in this change |
| 5 | **`kind: human` gates are not really human** | Medium | In headless mode the gate consumed an agent turn (transcript turn 3). This is gap **A4** |
| 6 | **Cost/latency are placeholders** | Low | `export-traces.py` carries 0-valued cost fields until a real executor reports them |
| 7 | **273 skills exceed the 500-line advisory** | Low | Advisory only; largest is 1,186 lines |
| 8 | **Single-run evidence** | Low | Phase 1 is one run on one agent backend (`claude -p`); it is a proof of mechanism, not of reliability at scale |
| 9 | **PyYAML absent locally** | Info | Two gates (7, 8) need the `yaml_shim` route in this environment |
| 10 | ~~Pre-existing markdown errors blocked committing the touched skills~~ → **fixed** | Low | 8 of the 13 skill files already carried `MD012`/`MD031` errors on `HEAD` (proved against a pristine worktree). Because the pre-commit `G5` gate runs `lint-markdown.py --changed --errors-only`, touching those files surfaced the latent errors and would have blocked the commit. Fixed fence-aware — whitespace only, no code-block content altered |
| 11 | ~~A declared-coverage metric can drift~~ → **fixed** | Info | `using-agent-skills` declared a contract while being ineligible as a default-mode node (it has no `Core Workflow`), so "44 declared" contained a skill *outside* the "301 eligible" denominator. Reverted; the invariant **declared ⊆ eligible** now holds at 43 (§4.5) |

## 12. File inventory

**Modified (20)** — totals: **1,106 insertions(+), 675 deletions(-)**:

| File | Change |
|---|---|
| `scripts/workflow-runner.py` | D2 (`_crash_checkpoint`, try/except at both execution sites, per-node `save_state`), D3 (final newline), **contract enforcement** (`load_contract`, `_criterion_index`, `_criteria_covered`, `_contract_violations`, `_apply_contract`, `--enforce-contracts`), docstring, 5 selftest fixtures |
| `scripts/executors/agent_executor.py` | +9 / −1 — D1 (`AGENT_TIMEOUT` 90 → 600s) with rationale |
| `scripts/.sha256manifest` | regenerated — 412 scripts |
| `skills/**/SKILL.md` × 13 | +11 lines each — `workflow:` contract (frontmatter only). 8 of them additionally had pre-existing `MD012`/`MD031` whitespace errors corrected (fence-aware; no code-block content altered) |
| `README.md` | +3 index rows (design doc, build log, HOW-IT-WORKS guide) |
| `examples/README.md` | +1 index row |
| `docs/graph-explorer/index.html` | regenerated |
| `docs/graph-explorer/skill-graph.json` | regenerated (627 / 612) |

**Added:**

| Path | Contents |
|---|---|
| `docs/HOW-IT-WORKS.md` | plain-language guide to the whole system |
| `docs/skill-automation-platform.md` | design + gap register + roadmap |
| `docs/skill-automation-platform-build-log.md` | this record |
| `examples/phase1-agentic-node/` | 9 files — run-state, transcript, traces, SLIs, effectiveness, memory, summary, README |

**Pre-existing, untouched:** `reasonix.toml` (untracked before this work began).

## 13. Reproduce everything

```bash
cd <repo root>

# --- the run (costs real agent calls; ~8-9 minutes) ---
AGENT_CMD='claude -p' AGENT_FALLBACK=0 \
  python3 scripts/workflow-runner.py \
    --manifest workflow/manifests/senior-dev-loop.yaml \
    --executor scripts/executors/agent_executor.py \
    --guardrail scripts/lib/guardrails.py \
    --memory examples/phase1-agentic-node/memory \
    --state examples/phase1-agentic-node/run-state.json

# --- gates ---
bash scripts/validate-skills.sh
python3 scripts/workflow-runner.py --selftest
python3 scripts/validate-workflows.py --all
python3 scripts/validate-workflows.py --coverage
python3 scripts/lib/lint-workflow.py --all
bash scripts/verify-script-integrity.sh

# --- PyYAML-less environments: run the two YAML gates via the repo shim ---
mkdir -p /tmp/yshim && printf 'from yaml_shim import *\n' > /tmp/yshim/yaml.py
PYTHONPATH=/tmp/yshim:scripts python3 scripts/validate_chains.py
PYTHONPATH=/tmp/yshim:scripts python3 scripts/emit-skill-graph.py --check

# --- statistics ---
python3 scripts/audit-library.py
python3 scripts/benchmark-skills.py --root skills
python3 scripts/skill-incorporate.py
python3 scripts/build-skill-index.py --build --eval

# --- observability over the archived run ---
python3 scripts/export-traces.py --state examples/phase1-agentic-node/run-state.json
python3 scripts/skill-sli-report.py --dir examples/phase1-agentic-node
python3 scripts/run-effectiveness.py --state examples/phase1-agentic-node/run-state.json --memory
```

## 14. Glossary

| Term | Meaning here |
|---|---|
| **Node** | One unit of work in a workflow graph, bound to a skill by name |
| **L0 contract** | The optional `workflow:` frontmatter block declaring artifacts, criteria, evidence, iteration, escalation |
| **L1 manifest** | A YAML file composing skills into a graph (`workflow/manifests/*.yaml`) |
| **L2 / L3** | Node-quality levels: L2 = agent runs the skill's procedure; L3 = L2 + declared criteria, evidence, bounded loop and named escalation |
| **SLI** | Service-level indicator computed from run checkpoints (completion, escalation rate, avg steps) |
| **Gate** | A node that halts or routes: `kind: human` (approval), `auto` (condition), `agent` (bounded reroute) |
| **Escalation** | Exhausting a bounded loop and routing to a named target instead of stopping silently |
| **Guardrail** | A classifier run at a graph edge; a non-allow verdict blocks the payload from advancing |
| **Effectiveness score** | 0–100 run score from `run-effectiveness.py` (completion, cleanliness, exit-by-design, handoffs, questions, budget, memory) |
| **D1 / D2 / D3** | The three defects recorded in §3 |
