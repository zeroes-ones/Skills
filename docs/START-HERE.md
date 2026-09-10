# Start Here

> **This is the short version.** What this repo is, what we built, how it works, and what every
> skill is required to contain. No jargon without a translation. If you want the deep version
> afterwards, read [`HOW-IT-WORKS.md`](HOW-IT-WORKS.md).

---

## 1. The 30-second version

This repo is **two things**:

1. **304 "skills"** — written playbooks. Each tells an AI agent how to do one professional job
   (review code, design a database, price a consulting job, audit accessibility…).
2. **A workflow engine** — a small program that runs those playbooks as a *graph of steps*, so work
   actually starts, finishes, retries, and gets recorded.

The playbooks are the knowledge. The engine supplies the discipline. **Almost everything we did was
making those two work together with a real AI agent — and fixing what broke when they did.**

---

## 2. Three words, and you understand the design

| Word | What it is | Where it lives |
|---|---|---|
| **Skill** | A playbook for one job | `skills/<domain>/<name>/SKILL.md` (304 of them) |
| **Workflow** | A file describing a job as a graph of steps | `workflow/manifests/*.yaml` (6 of them) |
| **Node** | One step inside a workflow, pointing at one skill | a block inside a workflow file |

A **workflow** is a recipe. A **node** is one instruction. A **skill** is the expertise that carries
that instruction out.

```
  WORKFLOW FILE            ENGINE                      SKILLS
  what should happen  →  walks the graph,         →  the know-how each
  (nodes, loops,         retries, records,           step actually uses
   gates)                escalates
```

**Why split it this way?** The engine can't be clever, so it can't be wrong. The AI handles the part
that needs judgement. A loop that won't stop is a code bug; a bad review is a content problem — you
can fix them separately.

---

## 3. How it works, in five plain steps

1. You write (or generate) a **workflow file** listing steps and naming a skill for each.
2. The **engine** reads it, checks it's sensible, and starts.
3. At each step, the engine calls an **AI agent once** — and pastes that step's skill into the prompt,
   so the agent works from the playbook instead of improvising.
4. The agent replies with a verdict. The engine decides what's next: continue, **loop again** (if the
   step said "needs work" and the loop has attempts left), or **escalate** (if it's out of attempts).
5. After every step, the engine **writes progress to a file**. That file is both the audit trail and
   the resume point.

---

## 4. What we actually did — plain list

| # | What | Why it mattered |
|---|---|---|
| 1 | **Ran it for real.** A "build it, then review it" workflow, with a real AI doing each step. Archived the evidence. | Nobody had ever proven the engine works with a real agent. It does: it finished cleanly, scored **100/100**, and the review step *actually read the changed files* instead of summarising a message. |
| 2 | **Found and fixed 3 real bugs.** The first attempt **failed**. | See §5 — two of these would have quietly broken everything that came after. |
| 3 | **Labelled 13 more skills** as engine-ready (30 → 43). | A label means "here's what I need, what I produce, my checklist for done, who to escalate to". |
| 4 | **Turned on a check the engine never made.** | Until now the engine read only a skill's *name* and took its "done" on faith. Now it can require the step to *prove* it. |
| 5 | **Fixed a broken CI check** someone had left stale. | The repo's own picture of the skill graph was out of date; the check was failing before we touched anything. |
| 6 | **Wrote the documentation.** | This file, plus the three in §8. |

---

## 5. The three bugs, in one line each

| Bug | What happened | Now |
|---|---|---|
| **Timeout** | Each step got 90 seconds. Real steps took **150–180+**. The run died mid-way. | 600 seconds |
| **Crash erased the work** | Progress was saved only *after a whole loop finished*. The crash was mid-loop, so **the progress file was never written** — two finished steps of real AI work, gone, and no way to resume. | Saved after **every** step, and a crash records itself before erroring out |
| **Bad file** | The archived run file didn't end with a newline, so the repo's own checker would reject it. | Fixed, and the engine now always writes it |

---

## 6. See it work in 60 seconds

No AI, no cost, no waiting:

```bash
cd <this repo>

# 1. Do the engine's own tests
python3 scripts/workflow-runner.py --selftest
# expect: selftest: 16 checks, 0 failed

# 2. Run a real workflow, no AI involved
python3 scripts/workflow-runner.py --manifest workflow/manifests/senior-dev-loop.yaml
# expect: "outcome": "complete"

# 3. Run it again with the new completeness check switched on
python3 scripts/workflow-runner.py --manifest workflow/manifests/senior-dev-loop.yaml --enforce-contracts
# expect: the steps are now flagged "contract-violation" and the score drops — see §7

# 4. Check the whole library is healthy
bash scripts/validate-skills.sh
# expect: PASS: 14, FAIL: 0
```

---

## 7. The check we turned on (the most interesting change)

**Before:** the engine read only the *name* of the skill attached to a step. It never opened the
skill, never read the checklist, never looked for proof. A step could declare *"evidence required"*
and supply none — and still be marked done.

**Now** (`--enforce-contracts`): a step is **not** marked done unless it substantiates itself —
evidence supplied, and every declared criterion accounted for. If it can't, the run doesn't quietly
move on: inside a loop it retries, outside a loop it escalates.

Same workflow, run two ways:

| | Check off | Check on |
|---|---|---|
| Steps that passed | all | **none** — both flagged `contract-violation` |
| Quality score | **95/100** | **45/100** |

It's **off by default** on purpose: most executors don't report the extra detail yet, so switching it
on everywhere would break existing runs.

---

## 8. What every skill is REQUIRED to have

This is the answer to "is this required in each skill?" — there are **two different questions**, and
they have **different answers**.

### 8a. Required on every skill — YES

| Requirement | Checked by | Notes |
|---|---|---|
| **Frontmatter**: `name`, `description`, `license` (minimum) | `lint-yaml.py` | `description` must follow the "Use when…" trigger format |
| **12 core sections** | `validate-skills.sh` gate 3 | see the list below |
| **`chain:` block** (what it consumes from / feeds into) | `validate-skills.sh` gates 11, 18 | must be **symmetric** — if A feeds B, B must consume A |
| **"Complete when" criteria** (≥8) | pre-commit G7 | advisory, not blocking |
| **No fabricated APIs/versions**, uncertainty admitted | `validate-skills.sh` gate 9 | |
| **File format**: UTF-8, LF endings, final newline, no tabs, no trailing whitespace | `lint-files.py` | |
| **Markdown style**: heading structure, blank lines, code-fence language | `lint-markdown.py` | |

The **12 core sections** every skill must contain:

```
1. Route the Request                       7. Core Workflow
2. Ground Rules — Read Before Anything Else 8. Cross-Skill Coordination
3. The Expert's Mindset                     9. Proactive Triggers
4. Operating at Different Levels           10. What Good Looks Like
5. When to Use                             11. Deliberate Practice
6. Decision Trees                          12. References
```

Plus, normally also present: `Error Decoder`, `Best Practices`, `Production Checklist`,
`Anti-Patterns` / `Gotchas`, `State Log`, `Verification`, `Error Recovery`, and
`token_budget` in the frontmatter.

> **One exception:** skills under `00-framework/` are **exempt** from the 12 core sections. That's
> why the router (`using-agent-skills`) and the taxonomy (`skill-levels`) have no `Core Workflow` —
> there is no single procedure to run.

### 8b. The `workflow:` contract — NO, not required

The `workflow:` block is **optional and additive**. The linter says so itself:

> *The block is OPTIONAL and ADDITIVE: a SKILL.md without it lints clean (default mode).*

**No governance gate requires it.** I checked every gate — none mentions it. Current state:

| | Count |
|---|---|
| Skills total | **304** |
| Usable as a workflow step | **304** (all of them) |
| Eligible "default-mode nodes" (Core Workflow + Verification) | **301** |
| **Declare the optional `workflow:` contract** | **43** |

So a skill without it **still works as a step**. The engine falls back to that skill's own
`Verification` table as the "done" checklist, at execution time.

### What you get by adding the contract

| With the contract | Without it (default mode) |
|---|---|
| Declares typed inputs and outputs | Nothing declared; inferred from the workflow file |
| Declares its own "done" checklist | Engine uses the skill's Verification table instead |
| Declares that evidence is required | Required only by convention |
| Declares who to escalate to | Uses the loop's escalation only |
| **Eligible for enforcement** (`--enforce-contracts`) | **Never checked** — its claims can't be verified |

**Should you add it?** Only where it earns its keep:

- **Yes** — for skills that workflows actually use, especially hubs (`backend-developer` is the most
  connected skill in the library). That's how we chose our 13: we asked the repo which skills its own
  workflows reference, and labelled the unlabelled ones.
- **No** — don't mass-add it. **The criteria must be real**, copied from the skill's own existing
  checklist. Inventing criteria to fill the field would make the contract a lie, and enforcement
  would then be enforcing fiction.
- **Not on meta-skills** — a router has no workflow, so a contract on it is meaningless. (We
  briefly did this, caught the inconsistency, and reverted it — see the build log §4.5.)

---

## 9. Where to read more

| File | What it's for |
|---|---|
| **`docs/START-HERE.md`** | this file — start here |
| `docs/HOW-IT-WORKS.md` | the longer plain-language guide: a real run walked through step by step, what every script does, what's real vs. not yet, glossary |
| `docs/skill-automation-platform.md` | the design: what an n8n-class version of this would need, and the gap list |
| `docs/skill-automation-platform-build-log.md` | the technical record: every change, every measurement, every defect, every open finding |
| `WORKFLOW-SYSTEM.md` | the formal specification of the workflow layer |

---

## 10. Honest status — what is NOT done

| Gap | Plain English |
|---|---|
| **Nothing starts a workflow by itself** | There are no schedules, no webhooks, no "when a ticket arrives". A human or an agent must invoke it. This is the biggest missing piece |
| **The engine is not a service** | It runs once and exits. No always-on process, no queue, no API |
| **A "human approval" step isn't really human** | Marking a step as needing human approval doesn't pause anything. In our real run, the "human ship gate" auto-approved and used an AI turn instead |
| **Enforcement is off by default** | And in headless mode a run with violations still reports "finished" — the violation is recorded and the score collapses, but the run doesn't fail loudly |
| **Only 3 of 304 skills have regression tests** | Changes to a skill are checked for *structure*, not for whether it still produces good work |
| **Tested against one AI provider** | The design is provider-neutral, but only one backend was actually exercised |

---

## 11. Glossary

| Term | Plain meaning |
|---|---|
| **Skill** | A written playbook for one job |
| **Workflow / manifest** | A file describing a job as a graph of steps |
| **Node** | One step in a workflow, pointing at one skill |
| **Executor** | The thing that performs a step (a real AI agent, or a stub for testing) |
| **Loop** | A repeating section, with a maximum number of attempts |
| **Gate** | A step that decides: approve, or route elsewhere |
| **Escalation** | Handing a problem to a human instead of failing silently |
| **Handoff** | The record of what one step produced, passed to the next |
| **Contract** | The optional labels a skill declares (inputs, outputs, checklist, proof, escalation) |
| **Guardrail** | A safety check applied to a step's output before it may flow onward |
| **Run-state** | The file recording everything a run has done; also its resume point |
| **Effectiveness score** | A 0–100 grade for a run |
| **SLI** | A reliability statistic across runs (e.g. share of runs that escalated) |
