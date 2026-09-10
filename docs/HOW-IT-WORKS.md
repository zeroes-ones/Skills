# How It Works — The Plain-Language Guide

> **Read this if you want to understand what exists in this repository and what it does, without
> reading code.** It assumes no prior knowledge of the workflow machinery. Every number here was
> measured in this repository, and the command that produced it is given so you can check.
>
> Deeper material, if you want it later: [`WORKFLOW-SYSTEM.md`](../WORKFLOW-SYSTEM.md) (the formal
> spec), [`skill-automation-platform.md`](skill-automation-platform.md) (the design + gap plan),
> [`skill-automation-platform-build-log.md`](skill-automation-platform-build-log.md) (the technical
> build record).

---

## 1. The one-paragraph version

This repository contains **304 "skills"** — written playbooks that tell an AI agent how to do a
specific professional job (review code, design a database, price a consulting engagement, audit
accessibility…). A playbook on its own is just text: nothing makes the agent *start*, *finish*, or
*prove it finished*. So this repo also contains a small **workflow engine**: you describe a job as a
graph of steps, each step naming one skill, and the engine runs that graph — looping where it should
retry, stopping where it should ask a human, and writing down evidence as it goes. In this session we
proved that engine works with a **real AI agent** doing the actual step work, found and fixed three
real bugs in it, labelled 14 more skills as engine-ready, and turned on a long-promised check that
the engine had never actually enforced.

---

## 2. The problem this solves

Imagine you hand an AI agent a 300-page manual and say "review my code". Three things go wrong:

1. **Nothing starts it.** The agent waits for you to type something. There is no "every night at 2am,
   review the open PRs" or "when someone files a ticket, triage it".
2. **Nothing defines "done".** The agent says "looks good to me" and stops. There is no checklist it
   must satisfy, and no proof it satisfied it.
3. **Nothing handles "not done".** If the work is wrong, nobody retries it, and nobody gets told. The
   agent either declares victory or trails off.

The engine in this repo is the answer to those three problems. The skills supply the *knowledge*; the
engine supplies the *discipline*.

---

## 3. Three words explain everything

| Word | What it means here | Where it lives |
|---|---|---|
| **Skill** | A playbook for one job: when to use it, the steps, the failure modes, the checklist for "done" | `skills/<domain>/<name>/SKILL.md` — 304 of them |
| **Workflow** | A description of a job as a graph: which skills, in what order, what may loop, where a human must approve | `workflow/manifests/*.yaml` — 6 of them |
| **Node** | One step *inside* a workflow, bound to exactly one skill | a block inside a workflow file |

A **workflow** is a recipe. A **node** is one instruction in it. A **skill** is the expertise used
to carry out that instruction.

### The picture

```
        WORKFLOW  (a file: what should happen)
   ┌───────────────────────────────────────────────────────┐
   │  node A ──▶ node B ──▶ node C ──▶ GATE (human decides) │
   │  skill:X     skill:Y    skill:Z                        │
   └───────────────────────────────────────────────────────┘
                     │           │           │
                     ▼           ▼           ▼
        SKILLS   (the know-how the node runs, 304 available)

        ENGINE   (a program that walks the graph, retries, records, escalates)
```

---

## 4. The three layers, with a concrete example

The system is deliberately split into three layers. Here is the same idea at each layer, using one
real example — a "build it, then review it" loop:

### Layer 1 — the plan (`workflow/manifests/senior-dev-loop.yaml`)

```yaml
nodes:
  - id: implement
    skill: incremental-implementation     # node 1 uses this skill
  - id: review
    skill: code-reviewer                  # node 2 uses this skill
loops:
  - id: micro-sdlc-loop
    nodes: [implement, review]            # these two repeat…
    exit_when: review.verdict == pass     # …until the reviewer says pass
    max_iterations: 4                     # …but never more than 4 times
    escalate_to: ship-gate                # …then hand to the ship gate
```

Read it as English: *"Implement, then review. If the reviewer isn't happy, do it again — up to four
times. If it's still not right, stop and hand it to the ship gate."*

### Layer 2 — the execution (`scripts/workflow-runner.py`)

A program that reads that file and walks the graph. It owns everything **mechanical**: which node is
next, how many times the loop has run, whether a node's output satisfies the next node's condition,
where the run's state is written after each step, and what to do when a limit is hit. It makes no
judgements about the work itself.

### Layer 3 — the content (`scripts/executors/agent_executor.py`)

When the engine reaches a node, something has to *do the work*. That is the executor. The one that
matters calls a **real AI agent** once per node, and — this is the important part — pastes that
node's skill into the prompt, so the agent is working from the playbook rather than improvising:

```
You are executing the node 'implement' …
YOUR OPERATING SKILL (compiled excerpt, 405 words; follow it for this node):
---
<the incremental-implementation skill>
---
Do the node's work and finish your reply with exactly one line:
'Verdict: pass' … otherwise 'Verdict: changes_requested'
```

**This split is the whole design.** The engine cannot be clever, so it can't be wrong. The agent
handles the part that needs judgement. A loop that can't terminate is a code bug; a review that
misses a bug is a content problem. Keeping them apart means you can debug each one on its own.

---

## 5. A real run, step by step

This is what actually happened when we ran the above workflow with a real AI agent. Times are
measured, not estimated.

| When | What the system did |
|---|---|
| t = 0s | Engine loads the workflow, checks it is valid, creates a run-state file |
| | Engine reaches node **`implement`** and calls the agent, handing it the `incremental-implementation` skill (405 words) |
| t = 331s | Agent replies. Verdict: `changes_requested` (it reviewed the pending changes and wanted more) |
| | Engine asks the loop: *is the exit condition met?* (`review.verdict == pass`) — `review` hasn't run yet, so **no**. Move to the next member |
| | Engine reaches node **`review`**, calls the agent with the `code-reviewer` skill (1,200 words) |
| t = 392s | Agent replies with a real line-level review of ~110 changed lines. Verdict: **`pass`** |
| | Engine asks the loop again: exit condition met? **Yes.** Loop exits |
| | Engine attaches the handoff record (which node produced what, and a fingerprint of it) and moves to **`ship-gate`** |
| t = 507s | Ship gate — declared as a *human* gate. In this headless test nothing was there to approve it, so it was auto-approved (see §10, known gaps) |
| | Engine writes the final state and exits `0` |

**Result:** outcome `complete`, 3 steps used out of a budget of 40, one loop iteration, a recorded
handoff (`handoff-v1`, fingerprint `176099b50f3b`), a 0/100–100/100 quality score of **100/100**, and
an escalation rate of **0.00**.

**What the agent did that matters:** it did not summarise a handoff message. The `review` node read
the actual files in the working tree and reviewed the real diff. That is the difference between a
node that "runs an integration" and a node that *does a job*.

### The single most useful number from that run

| Layer | Time taken |
|---|---|
| The **engine** (all the walking, looping, recording) | **0.228 seconds** |
| The **agent turns** (the actual thinking) | **507 seconds** |

More than 99.9% of the time is the AI thinking, not the machinery. Which means: optimising the
engine is pointless; improving the skill and the prompt is everything.

---

## 6. The tools, in plain English

You do not need to read code to use these. Each is a command you run from the repository root.

| Command | What it does | When you'd use it |
|---|---|---|
| `python3 scripts/validate-workflows.py --all` | Checks every workflow file is well-formed: no impossible loops, every skill exists, every loop is bounded | Before trusting a workflow you just wrote |
| `python3 scripts/validate-workflows.py --coverage` | Reports how many skills are usable as steps, and how many are "fully labelled" | To see how much of the library is wired up |
| `python3 scripts/workflow-runner.py --selftest` | Runs the engine's own 16 self-tests | After changing the engine |
| `python3 scripts/workflow-runner.py --manifest <file>` | **Runs** a workflow | To actually do the work |
| `python3 scripts/goal-to-graph.py --goal "…"` | Turns a one-line goal into a ready-made workflow file | When you don't want to write the plan by hand |
| `python3 scripts/export-traces.py --state <file>` | Converts a run into standard observability "spans" | To feed a monitoring tool |
| `python3 scripts/skill-sli-report.py --dir <dir>` | Reports reliability stats across runs: how many completed, how many escalated | To answer "is this workflow reliable?" |
| `python3 scripts/run-effectiveness.py --state <file>` | Scores a run 0–100 | To check a run actually did its job |
| `python3 scripts/audit-library.py` | Produces the quality scorecard for all 304 skills | To see the health of the library |
| `python3 scripts/emit-skill-graph.py` | Rebuilds the interactive picture of how skills depend on each other | After adding or moving skills |

---

## 7. What changed in this session

All of it is in the working tree, uncommitted, ready to review. In plain terms:

| Change | Why it matters |
|---|---|
| **A real run was performed and archived** (`examples/phase1-agentic-node/`) | Before this, nobody had proved the engine works with a real AI agent. Now there is a run with its full evidence: the state file, the transcript of all three agent turns, spans, reliability stats, and its 100/100 score |
| **Three bugs found and fixed** (see §8) | The first attempt at that run *failed*. The failure exposed real defects that would have broken every later phase |
| **13 more skills labelled engine-ready** (30 → 43) | A skill can declare what it consumes, what it produces, its checklist for "done", and where to escalate. Previously only 30 did |
| **The engine now enforces those labels** (new, off by default) | Until this session the labels were decoration — the engine never looked at them. Now it can (see §10) |
| **A broken CI check repaired** | The repository's own picture of the skill graph was stale, failing a CI job. Regenerated; the check passes again |
| **Everything documented** | A design doc, a build log, a rewritten example, and this guide |

**Files touched:** 21 modified, 2 documents added, 1 example folder added. Nothing committed.

---

## 8. The three bugs, in plain English

### Bug 1 — every real step was doomed to time out

The engine gave each AI step **90 seconds** before declaring failure. A real step — reading a
1,200-word skill, examining a codebase, writing a review — took **149 seconds**, then **180+**
seconds. So the first real run died partway through.

*Fixed:* the limit is now 600 seconds.

### Bug 2 — a crash erased all the work

This is the serious one. The engine records progress to a file after each step. But that recording
happened only *after a whole loop finished*. On the first run, step 2 crashed — and because the crash
happened mid-loop, **the progress file was never written at all.** Two completed steps of real AI work
were gone, and the run could not be resumed, precisely in the situation where you most want to resume.

*Fixed:* progress is now saved after **every** step, and a crash records what crashed before
handing the error up. Proven by a new self-test: *"crash mid-loop checkpoints the run"*.

### Bug 3 — an artifact that would fail the repo's own checks

The newly archived run file didn't end with a newline. The repository's linter requires one, so the
file would have been rejected the moment anyone committed it. Found by running the repo's own linters
against the new artifacts rather than assuming.

*Fixed:* the engine now writes the trailing newline, and the archived file was corrected.

---

## 9. What a "contract" is, and why we added 14

A skill can optionally carry a small block of labels at the top of its file. Here is a real one:

```yaml
workflow:
  artifacts:
    inputs: [spec]                 # what this step needs to start
    outputs: [change]              # what it promises to produce
  completion:
    criteria:                      # the checklist for "this step is done"
      - Every slice ships behind a feature flag defaulting to false
      - Tests pass with the flag both ON and OFF
      - No destructive schema changes (ADD only, no DROP or ALTER)
    evidence: required             # proof must be supplied, not just claimed
  escalate_to: [human-gate]        # who to hand to if it can't be finished
```

Without this block, a step is a black box: it says "done" and you take its word. With it, the step
has declared inputs, declared outputs, a named checklist, and a required proof.

**Why 14 were added:** we asked the repository *which* skills its own workflows actually use, and
labelled the ones that weren't labelled yet. That took "fully labelled" from **30 to 43** skills. The
criteria were copied from each skill's own existing checklist — none were invented.

---

## 10. The check the engine never actually made

Everything above describes labels. Here is the catch we found and fixed. Until this session:

> The engine read **only** the name of the skill attached to a step. It never opened the skill, never
> read the criteria, and never checked the evidence. A step could declare *"evidence required: proof
> must be supplied"* and then supply none — and the engine would mark it done.

That is the difference between a guarantee and a claim. We fixed it, and — this is the honest part —
it was designed deliberately **off by default**, because many existing executors don't report the
detail it checks.

### What it now does when switched on (`--enforce-contracts`)

The engine refuses to mark a step done unless the step substantiates its own completion:

1. If the skill says `evidence: required`, the step must supply evidence.
2. If the skill declares criteria, the step must report which ones it met — and **all** of them must
   be covered. Naming a criterion that doesn't exist is also a violation.
3. Declared outputs that weren't produced are recorded as a **warning**, not a block.

And the failure behaves sensibly rather than just stopping: inside a retry loop, the step is retried
and the loop's own limit applies; outside a loop, the run escalates instead of quietly moving on.

### Watching it work

We ran the same workflow twice — once normally, once with the check enabled. The stub executor used
for this demonstration reports no evidence, so it gets caught:

| | Default (check off) | With `--enforce-contracts` |
|---|---|---|
| Steps marked done with a passing verdict | all | **none** — both marked `contract-violation` |
| Log entries naming what was missing | — | *"completion.evidence is 'required' but the node reported no evidence; completion.criteria declares 3 criteria (c1, c2, c3) but the node reported no criteria_met coverage"* |
| What the loop did | exited normally | retried, then escalated as designed |
| **Effectiveness score** | **95 / 100** | **45 / 100** |

The 95 → 45 collapse is the point: an unsubstantiated run now *looks* unsubstantiated instead of
looking identical to a real one.

---

## 11. How to run it yourself

```bash
cd /Users/sp.vm/Documents/Projects/Skills

# 1. Check nothing is broken (fast, no AI calls)
python3 scripts/workflow-runner.py --selftest          # expect: 16 checks, 0 failed
python3 scripts/validate-workflows.py --all            # expect: 20 OK
bash scripts/validate-skills.sh                        # expect: 14 PASS, 0 FAIL

# 2. Run a workflow with no AI (deterministic stub) — proves the machinery
python3 scripts/workflow-runner.py --manifest workflow/manifests/senior-dev-loop.yaml

# 3. Run it with the enforcement check on
python3 scripts/workflow-runner.py --manifest workflow/manifests/senior-dev-loop.yaml \
  --enforce-contracts

# 4. Run it with a REAL AI agent (costs money and several minutes per step)
AGENT_CMD='claude -p' AGENT_FALLBACK=0 \
  python3 scripts/workflow-runner.py \
    --manifest workflow/manifests/senior-dev-loop.yaml \
    --executor scripts/executors/agent_executor.py \
    --guardrail scripts/lib/guardrails.py \
    --memory examples/phase1-agentic-node/memory \
    --state examples/phase1-agentic-node/run-state.json
```

> `AGENT_FALLBACK=0` in step 4 is not optional. By default the executor substitutes a fake "pass"
> when an AI call fails — so a run that "succeeded" under the default proves nothing.

---

## 12. What is real, and what isn't yet

Honest status. This matters more than the list of successes.

### Real — measured in this repository

- The engine runs workflows with real AI agents and completes them end to end (§5).
- Loops retry, respect limits, detect stagnation, and escalate instead of hanging (16 self-tests).
- Runs are scored, traced, and can be reported on (100/100, 4 spans, escalation rate 0.00).
- Declared completion criteria are now **enforced** when switched on (§10), verified by 4 tests.
- 304 skills, 37 domains, 9.9/10 quality score, 100% portability-declared.

### Not real yet — do not assume these

| Gap | Plain English |
|---|---|
| **Nothing starts a workflow by itself** | There are no time-based, webhook, or event triggers. A human, or an agent, must invoke it. This is the single biggest missing piece |
| **The engine is not a service** | It runs once and exits. There is no scheduler, no queue, no always-on process, no API |
| **A "human gate" isn't really human** | Declaring a step as needing human approval doesn't pause anything. In our real run, the "human ship gate" was auto-approved and consumed an AI turn instead. A real pause-and-approve queue does not exist |
| **Enforcement is off by default** | Turning it on requires every executor to report per-criterion evidence, which only the human-driven path does today |
| **Only 3 of 304 skills have regression tests** | A change to a skill is checked for structure, not for whether it still produces good work |
| **Reliance on one AI provider in testing** | The real run used one agent backend (`claude -p`). The design is provider-neutral but that is not yet exercised |
| **Cost and latency are placeholders** | Runs record tokens/latency fields that a real executor does not yet fill in |
| **`COORDINATION-MATRIX.md` is out of date** | It describes 106 skills / 25 domains; there are 304 / 37. There is no script to regenerate it |
| **The library has drifted numbers in places** | `README.md` says 303 skills; the measured count is 304. The graph section was corrected this session; other mentions were left |

### Known limitation in the enforcement we just added

In headless testing there is no human to see a contract violation, so the run still reported
`complete` — because the terminal gate auto-approved. The violation *is* recorded (the step is marked
`contract-violation` and the score collapses to 45), but "the run finished" and "the work was
substantiated" are still two different questions. Closing that means fixing the human-gate gap above.

---

## 13. Glossary

| Term | Plain meaning |
|---|---|
| **Skill** | A written playbook for one job |
| **Workflow / manifest** | A file describing a job as a graph of steps |
| **Node** | One step in a workflow, bound to one skill |
| **Executor** | The thing that actually performs a step (a real AI agent, or a stub for testing) |
| **Loop** | A repeating section of a workflow, with a maximum number of attempts |
| **Gate** | A step that makes a decision: approve, or route somewhere else |
| **Escalation** | Handing a problem to a human (or a bigger authority) instead of failing silently |
| **Handoff** | The record of what one step produced, passed to the next |
| **Contract** | The labels a skill declares: inputs, outputs, checklist, proof required, escalation |
| **Guardrail** | A safety check applied to a step's output before it is allowed to flow onward |
| **Run-state** | The file recording everything a run has done; also its resume point |
| **Effectiveness score** | A 0–100 grade for a run (finished? clean? exited by design? handed off? in budget?) |
| **SLI** | A reliability statistic across runs — e.g. the share of runs that had to escalate |
| **Span** | One timed unit in the standard observability format (one run, or one step) |
| **Self-test** | A test built into the engine that you can run with one command |
