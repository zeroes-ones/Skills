# Loop / Graph / Handoff / Routing — Superiority Assessment

Date: **2026-09-19** · Repo: `/Users/sp.vm/Documents/Projects/Skills` · Downstream consumer:
`/Users/sp.vm/Documents/Projects/Agent/AgentOrg`

Question asked: *is this library's loop/graph/node/handoff/routing strategy superior, and is it
sound when a downstream product consumes it?*

Method: every number below was produced in this checkout by the command named beside it. Where a
claim in the repo's own documents could not be reproduced, that is stated and the document is
named. Line citations are to the files as they exist today.

---

## 1. Executive verdict

**No — not yet.** The engine's *control-flow* core is genuinely well built: loop exit conditions,
iteration ceilings, stagnation detection and escalation are implemented and self-tested
(`scripts/workflow-runner.py:945-961`), per-node state is checkpointed atomically
(`:349-356`), a crashing node checkpoints before the exception escapes (`:893-909`), and cost is
tracked with an explicit "unmeasured, not free" flag (`:290-346`). That half is genuinely solid.

The *integration* half does not. Artifact typing is inert in the engine (zero `inputs` reads in
`workflow-runner.py`), and 14 of the 16 manifest nodes whose skill declared a contract declared node
`inputs`/`outputs` that contradicted it (88% — since corrected to 0). Handoff hashes were computed
and written three times and **never read or compared** (now partly remediated — see B1). And the
routing layer had **no vector or embedding implementation at all** — `scripts/build-skill-index.py:8-9`
says so in its own docstring — scoring **rank-1 55.6%** overall and **0.0%** on the 14
semantic-adversarial scenarios (now 58.7% and 14.3%).

> **Correction (B3, same day).** An earlier revision of this assessment claimed that "328 of 336
> chain edges (97.6%) connect a producer output to a consumer input that does not exist" and called
> the chain graph "semantically broken." **That finding was wrong, and it is retracted here.**
> `chain.consumes_from` is documented corpus-wide as **sequencing** — `README.md:27`:
> *"What must complete BEFORE this skill"*; `AGNOSTIC-PRINCIPLES.md:83`: *"Must run BEFORE this
> skill"* — not as a declaration of artifact supply. `workflow.artifacts` is a separate, optional
> node contract (64 of 327 skills). Comparing them measures two different invariants as though they
> were one. The evidence that settled it: applying the "correction" would have deleted **158
> `consumes_from` edges, all 158 currently symmetric and documented**, and 0 of 7 proposed additive
> edges survived a check of the skills' own coordination prose. The tool built to test this
> (`scripts/reconcile-artifacts.py`) reports the *real* defect below instead.

Because AgentOrg delegates traversal to this runner as a subprocess and treats it as authoritative
(`AgentOrg/engine/parallel.py:15-18`, `AgentOrg/engine/host.py:458-464`), every dead construct and
unverified handoff is a load-bearing promise the product is trusting. The library is a good engine
with a good control-flow core wearing an integration layer that is currently decorative.

---

## 2. What is genuinely sound

Verified by reading the code and by running the engine's own tests.

| # | Capability | Evidence | Why it holds |
|---|---|---|---|
| 1 | Loop exit: `exit_when` → `max_iterations` → step budget → stagnation, in that order | `scripts/workflow-runner.py:945-961` | Each exit sets a distinct `_loop_exit_reason`; exhaustion routes to `escalate_to` or ends. No path returns "iterate" past a ceiling. |
| 2 | Stagnation detection | `:963-973` | Hashes the last `window` passes' evidence/verdict and treats identical stamps as exhaustion. `require_delta: false` disables it honestly rather than faking convergence. |
| 3 | Atomic per-node checkpoint | `:349-356` | Writes `path.tmp` then `os.replace` — a crash mid-write cannot truncate the previous good state. Called after every node in the main branch (`:1150`) and every loop member (`:941`), plus the crash path (`:909`). |
| 4 | Crash checkpoint before rethrow | `:893-909` | Logs `action: error` naming node + exception type, saves state, *then* re-raises. Completed nodes survive; only the failed node re-runs. Regression-tested (`:1546`). |
| 5 | Step and cost budgets, with honesty flag | `:290-346` | `record_usage` accumulates and records `measured: false` + `unreported_nodes`; `cost_exceeded` refuses to enforce a cap it could not measure (`:323-346`). An unmeasured run is never reported as cheap. |
| 6 | Parallel join-then-reconcile | `:1056-1085` | Group members are held until every member reaches a terminal status, then each member's satisfied edges fire. Verified by self-test §1b (`:1314-1332`). |
| 7 | Edge guardrail hook | `:603-626` | A blocked payload increments the step counter, records `action: guardrail`, marks the node `blocked`, sets `phase: escalated` and does not advance. Self-tested with a genuinely poisoned payload (`:1384-1404`). |
| 8 | Run-memory with `trust: context_only` | `:359-494` | Entries are labelled `trust: context_only` with provenance and `manifest_sha`; the recall renderer prints them as context, never as instructions. |
| 9 | Contract enforcement (`--enforce-contracts`) | `:628-696` | Checks `completion.evidence: required`, covers every declared criterion, and turns a violation into `needs_review` so loop/rework machinery handles it. Off by default = documented default mode. |

Gates re-run today, unmodified:

```
$ python3 scripts/workflow-runner.py --selftest
selftest: 27 checks, 0 failed

$ python3 scripts/validate-workflows.py --all
OK  ... (6/6 manifests)

$ python3 scripts/validate-workflows.py --selftest
selftest: 24 checks, 0 failed

$ python3 scripts/validate_chains.py
Skills checked: 327
✓ All chain references are symmetric. No dangling references.
```

---

## 3. What is broken

Ranked by blast radius on a downstream consumer.

| # | Defect | Severity | Evidence (reproducible) | Blast radius |
|---|---|---|---|---|
| B1 | **Handoff `sha` is written but never verified.** `_sha()` exists and is stamped into the handoff record at three sites; no code path reads `state["handoff"]["sha"]`, and there is no hash comparison anywhere in the file. | **Critical** | Write sites: `workflow-runner.py:1073-1074`, `:1080-1081`, `:1195-1197`. `_sha` def: `:184-185`. Stamped node record: `:578`. Zero comparisons: searching `scripts/workflow-runner.py` for a sha comparison or a `mismatch` branch returns no matches. | The documented corruption guard does not exist. Both specs claim it does (see B2). Any consumer relying on "no handoff without state-hash verification" is relying on nothing. |
| B2 | **Two documents assert behaviour the engine does not implement.** | **High** | `workflow/schema/run-state.schema.yaml:151-153` — R3: "sender's state hash is compared with receiver's observed hash; mismatch aborts the run". `WORKFLOW-SYSTEM.md:339-340` — "The runner compares hashes across a handoff — a mismatch aborts with a state-corruption error". No such comparison exists (B1). | A spec that overstates is worse than a missing spec: an engineer reads R3, believes the property holds, and builds on it. |
| B3 | ~~**Chain graph ↔ artifact typing are disjoint.**~~ **RETRACTED — see the correction in §1.** The measurement is real (of 336 `chain` edges where both ends declare `workflow.artifacts`, only **8 (2.4%)** name-match) but the *interpretation* was wrong: `chain.consumes_from` is sequencing (`README.md:27`), not artifact supply, so the two fields were never meant to agree. **The genuine defect this surfaced instead:** **107 of 119 declared `artifacts.inputs` have no producer anywhere in the corpus** — e.g. `design-system` is declared as an input by 4 skills and produced by none; 52 consumers declare inputs no skill outputs. That is a producer-side vocabulary gap, fixable only by authoring contracts, not by editing chain data. | **Medium** (was mis-rated High) | `python3 scripts/reconcile-artifacts.py` → 336 judged, 8 CONFIRMED, 17 PLAUSIBLE, 311 ORPHAN, and `107 declarations no skill produces`. Applying the originally-proposed chain rewrite would delete 158 symmetric, documented edges. | Chain data must **not** be rewritten to satisfy artifacts — that destroys the sequencing graph routing and regression tooling depend on. The real fix is to align or retire the unproduced `inputs` (see R3). |
| B4 | **Manifest node contracts contradict skill contracts.** 14 of the 16 manifest nodes whose skill declares `workflow.artifacts` declare node `inputs`/`outputs` that differ from the skill's own contract (**88%**). | **High** | Script over `workflow/manifests/*.yaml` × skill frontmatter. Examples: `serial-feature-delivery.yaml` node `architect` (skill `system-architect`) declares `inputs: [spec]` while the contract says `[non-functional-requirements, requirements]`; `parallel-audits-merge.yaml` node `qa-engineer` declares `outputs: [qa-findings]` while the contract says `[qa-report]`. | `--enforce-contracts` warns on every one of these runs ("declared artifacts.outputs not produced"). The repo's own flagship manifests are the counter-example to its own contract model. |
| B5 | **The payload registry is validated but never populated by the engine.** Nine canonical payload keys are declared and checked; the runner never assembles a payload *object* at all. The handoff record's `payload` field holds only the edge's payload *name* (a string, `null` in a real run), and `verification_evidence` and `context` appear as literals **zero** times in `workflow-runner.py` and in both bundled executors. | **Medium-High** | `scripts/validate-workflows.py:36-39` and `AgentOrg/engine/planner.py:257-260` define the nine-key set; `validate-workflows.py:424-441` rejects any key outside it. Payload names are passed through, not resolved to keys: `workflow-runner.py:1073-1074`, `:1080-1081`, `:1196`. A real run's handoff: `{"from": "a", "to": "gate-human", "payload": null, "sha": "…"}`. Literal counts in the runner: `verification_evidence`=0, `context`=0. | The registry governs the *names* of payloads, not their contents, and no engine code writes them. Only AgentOrg's own executor populates the nine keys (`AgentOrg/engine/executor.py:1109-1127`). A consumer reading `verification_evidence` from library-produced state gets nothing, with no error. |
| B6 | **Artifact typing is inert in the engine.** There is no read of `inputs` anywhere in `workflow-runner.py`; declared `outputs` are only checked as a non-blocking *warning*. | **Medium-High** | `grep -n 'inputs' scripts/workflow-runner.py` → no matches. Outputs treated as warning, explicitly: `:633-635`, `:665-673`. | The engine will happily run a graph whose edges connect incompatible artifact types. Type errors are discoverable only by reading a log line. |
| B7 | **Declared-but-dead constructs.** Documented and validated, never executed by the engine. | **Medium** | `supervisor`: in `NODE_TYPES` (`validate-workflows.py:34`) and validated (`:314-327`), zero occurrences in the runner. `task`: same enum, zero runner occurrences. Auto gate `pass_when`/`else_go`: in schema (`workflow-manifest.schema.yaml:118-125`) and condition-checked (`validate-workflows.py:284-286`), but in the runner only inside self-test fixtures (`:1320`, `:1429`). Node-level `escalate_to`: schema `:100-102`, runner never reads a node's `escalate_to` (only loop/gate ones: `:1203`, `:1218`). Node-level `on_exhaustion`: schema `:95-99`, **zero** occurrences in the runner. `control.state.merge`: schema `:34-44`, zero occurrences in the runner. Parallel `join: any/majority`: schema `:201-204`, parsed into `group["join"]` (`:531-534`) and never read — the docstring concedes it degrades to `all` (`:1058-1059`). | Eight constructs a manifest author can declare, get validated, and reasonably expect to fire. None do. |
| B8 | **Human gates do not pause.** A `kind: human` gate is executed as an ordinary node in the traversal loop; with the bundled stub executor it resolves `status: done`. | **Medium** | Probe manifest with `a → gate-human (kind: human)`, run `python3 scripts/workflow-runner.py --manifest <m> --state <s>` → `outcome: "complete"`, `nodes["gate-human"] = {"status": "done", "verdict": "pass", "iterations": 1}`. The runner's `run()` loop (`:1085-1177`) reads `manifest["gates"]` only for the *agent* reroute path (`:1205`). | "Stops where a human must approve" (§1 of `AGENTS.md`) is not enforced by the engine. Approval is enforced only if the executor chooses to block. Four of six manifests declare a human gate. |
| B9 | **Routing: rank-1 55.6%, adversarial 0.0%, no embeddings.** | **Medium-High** | `python3 scripts/eval-routing.py` → `rank-1 hit rate 55.6%`, `routing-semantic-adversarial: n=14 rank1=0.0%`. `scripts/build-skill-index.py:8-9` — "No embeddings here". `evals/tier2-routing-adversarial.json:3` — "Paraphrased, keyword-poor prompts". | Every downstream component that must pick a skill without a human inherits a router that fails on 44.4% of ordinary prompts and 100% of paraphrased ones. |
| B10 | **The downstream planner ignores the chain graph for composition, and discards its own type-mismatch findings.** `AgentOrg/engine/planner.py` contains zero direct `consumes_from` reads; its composition comes from hand-written `_DOMAIN_SHAPES` tables. Computed mismatches are stored on `self._last_dropped` and never read. | **Medium** | `grep -c 'consumes_from' AgentOrg/engine/planner.py` → `0`. Graph use is `_graph_review` (`:601-621`), whose own docstring says it "never changes the manifest". Type notes computed at `:842`, `:876`; stored at `:963` (`self._last_dropped = [*dropped, *type_notes]`); `grep -rn 'last_dropped' AgentOrg/ --include=*.py` returns only that line — no reader, no test. | The product computes an artifact-type diagnosis and throws it away, while planning from a static table that has no relationship to the corpus's own dependency graph. |

---

## 4. The vector / routing strategy

### 4.1 What exists

A lexical index only. `scripts/build-skill-index.py` indexes each skill's **name, description and
tags** plus a `body_words` count and a `chain_degree` — the body itself enters only as a word count
(`scripts/build-skill-index.py:100-113`). The documented canonical evaluator indexes name +
description + tags at weight 1.0 and the body's "When to Use" section at weight 0.15
(`scripts/eval-routing.py:7-8`).

Measured coverage of the corpus vocabulary:

```
corpus distinct body tokens       : 29797
indexed (name+desc+tags) tokens   : 5422
body vocab absent from index      : 24456  (82.1%)
body vocab absent from index+WTU  : 22349  (75.0%)
```

So **~75-82% of the corpus's working vocabulary is not reachable by the router**, even in the
upgraded profile. That is the mechanical reason the adversarial suite scores 0.0%.

### 4.2 What B6 promised

`docs/BEYOND-LOOPS-GRAPHS.md:115-124` (frontier B6) specifies embedding every skill **body** plus
descriptions into an index, top-K retrieval, a rerank stage, and dependency-aware bundle expansion
over the chain graph. `docs/B6-ROUTING-SCOPE.md:14-18` records the honest status: negative-trigger
routing shipped without an embedding API; the embedding + rerank layer is "still open" and requires
a model-API environment. Acceptance targets (`B6-ROUTING-SCOPE.md:54-60`) are rank-1 ≥ 75% overall
and ≥ 50% on the adversarial suite.

Current, reproduced today:

```
$ python3 scripts/eval-routing.py
corpus skills indexed : 327
scenarios scored      : 63
rank-1 hit rate       : 55.6%
top-N hit rate        : 63.5%
MRR                   : 0.618
must-not violations   : 5
  routing-semantic-adversarial: n=14 rank1=0.0% topN=0.0% mrr=0.076 viol=0
```

### 4.3 The measured ceiling, and what is *not* measured

There is no BM25 or BM25F implementation anywhere in the repo's tooling — every BM25 hit in the tree
is inside a *skill's prose*, not a script. So the figure "a stdlib BM25F reaches ~59-62% rank-1" is
not a repo-published number. I implemented BM25F (k1=1.5, b=0.75) inline, as a throwaway probe over
the same 63 scenarios, weighting head fields (name+description+tags), the "When to Use" section, and
the full body, and swept the body weight:

| Body weight | rank-1 | top-N | adversarial rank-1 |
|---|---|---|---|
| 0.0 (lexical-equivalent) | 58.7% | 63.5% | 0.0% (0/14) |
| 0.6 | 60.3% | — | 0.0% |
| 0.8 | **61.9%** | 76.2% | 0.0% |
| 1.0 | 61.9% | — | 0.0% |
| 3.0 | 57.1% | — | 0.0% |

The band **58.7% → 61.9%** (best 61.9% at body weight 0.8) sits in the ~59-62% range and confirms
the conclusion: **body-weighted lexical retrieval moves rank-1 by ~3 points and does not approach
the ≥75% target, and it moves the adversarial suite by exactly zero.** The adversarial prompts are
constructed to avoid the target skill's obvious trigger keywords
(`evals/tier2-routing-adversarial.json:4`), so no surface-matching scheme can recover them — by
construction, not by tuning.

> **Unverified / out of scope:** this BM25F probe is a one-off measurement, not committed tooling;
> it is not covered by any repo gate, and the exact percentages will shift with tokenization and
> weighting choices. It is evidence for the *ceiling*, not a proposal. The separate claim that a
> stdlib-only router can reach ≥50% on the adversarial suite remains **unverified** — nothing in
> this repo measures it, and on these prompts surface matching cannot reach it.

---

## 5. The dependency risk

The library is not a dependency of AgentOrg — it *is* the engine. `AgentOrg/engine/parallel.py:15-18`
states the runner "is shared with other tools and is not ours to change"; `AgentOrg/engine/host.py`
spawns it as a subprocess (`:458-464`) and forwards `--executor`, `--guardrail`, `--state`,
`--memory`, optionally `--enforce-contracts` and `--contract-rework` (`:440-454`). The engine
therefore cannot correct any of the above on its own side.

Specific places the product assumes behaviour the engine does not provide:

| Assumption held by the product | Reality in the library | Citation |
|---|---|---|
| The payload registry is shared and authoritative. AgentOrg defines the same nine required fields and populates them in its own assembly. | The library defines the same nine keys and validates payload *names* against them, but no engine code assembles a payload object; the library relies on the executor to do what AgentOrg's executor chose to do. | `AgentOrg/engine/org/handoff.py:53-63` vs `validate-workflows.py:36-39`, `:424-441`; `AgentOrg/engine/executor.py:1109-1127`; §3 B5 |
| `constraints` is a structured handoff field. AgentOrg assembles it as its own payload key and says "rule R2 compares them against what upstream carried". | `constraints` is **absent from the library's `CANONICAL_PAYLOAD_KEYS`** and appears nowhere in `workflow-runner.py` or the schemas. A manifest declaring it would be rejected; nothing validates or carries it. | `AgentOrg/engine/executor.py:1124-1126`; `grep -rn 'constraints' scripts/workflow-runner.py workflow/schema/` → no matches |
| Manifest node `phase` and `tools` are part of the manifest contract. | Neither key exists in the library's node schema — which lists `id, type, skill, kind, description, inputs, outputs, max_iterations, on_exhaustion, escalate_to, workers, routing, select, executor, safety, gate` (`workflow/schema/workflow-manifest.schema.yaml:64-125`). The library validator neither rejects unknown keys nor defines these, so the drift is silent: a real product manifest with `phase`/`tools` is accepted (`python3 scripts/validate-workflows.py --manifest AgentOrg/understand-indian-market.yaml` → `OK`). | `AgentOrg/engine/planner.py:806`, `:818`, `:860`; live example `AgentOrg/understand-indian-market.yaml` (nodes carry `phase` and `tools`) |
| Human approval gates stop the run. | A `kind: human` gate is traversed as a normal node; §3 B8 probe returns `outcome: complete`. | §3 B8 |
| `join: any` / `join: majority` are honoured. | Parsed into the group and never read; the docstring concedes degradation to `all`. | `workflow-runner.py:531-534`, `:1058-1059` |
| Handoffs are hash-verified. | The hash is stamped and never compared. | §3 B1, B2 |

> **Partial premise correction.** The task brief states AgentOrg's planner "ignores the chain graph
> entirely (zero `consumes_from` hits)". The zero-hits figure is correct *for `planner.py`*
> (`grep -c 'consumes_from' AgentOrg/engine/planner.py` → `0`), but AgentOrg does read the graph:
> `AgentOrg/engine/skills/graph.py:1-40` is a purpose-built reader, and
> `AgentOrg/engine/planner.py:601-621` calls `SkillGraph.plan_review` for a read-only coherence
> diagnosis surfaced through `Plan.graph_review` (`:298`, `:369-388`). The accurate statement is
> narrow: **plan composition is driven by hand-written `_DOMAIN_SHAPES` tables, not by the chain
> graph; the graph is used only as an advisory review that by design "never changes the manifest".**
> This is a deliberate, documented design choice, not an omission — but it means the product's
> pipeline shape and the corpus's declared dependency graph can disagree with nothing to catch it.

---

## 6. Ranked remediation plan

Highest leverage first. Each item names the artifact it touches and a measurable acceptance test.

| # | Fix | Artifact | Acceptance test | Effort |
|---|---|---|---|---|
| R1 | ✅ **DONE — handoff integrity verification shipped.** Rather than the originally-proposed (and unsound) comparison of the live sender `sha` — which would false-positive because loop re-entry and rework legitimately rewrite the sender record — the handoff now carries an `integrity` block holding a frozen snapshot plus a digest over `{from,to,payload,frozen,budget}`. Verified at send time and on every resume; a mismatch aborts with `StateCorruption` naming the handoff. `sha` is unchanged for backward compatibility. | `scripts/workflow-runner.py` | 5 new selftests; suite grew **32 → 41 checks, 0 failed**. Detects: tampered/truncated handoff record, edited hop metadata, deleted digest. **Does not detect:** edits to `nodes[...]` themselves (needs a whole-state Merkle digest; not built, and the code says so). | — |
| R2 | ✅ **DONE — spec made honest.** `run-state.schema.yaml` and `WORKFLOW-SYSTEM.md` now describe the implemented mechanism and carry a "Declared but not yet implemented" table. | both docs | No sentence in either file asserts a comparison `grep` cannot find in the runner. | — |
| R3 | ✅ **DONE — but the finding was retracted, so ship it as advisory only.** `scripts/check-chain-coherence.py` and `scripts/reconcile-artifacts.py` exist and report; neither should ever gate a build, because the chain-vs-artifact comparison measures two different invariants (see the §1 correction). The real actionable output is **107 declared `inputs` with no producer** — fix by aligning or retiring those declarations, **never** by rewriting `consumes_from`. | new `scripts/check-chain-coherence.py`, `scripts/reconcile-artifacts.py` | Both run clean and agree on 336 judged edges. Ratchet only on the unproduced-input count, not on the orphan-edge count. | — |
| R4 | **Wire artifact typing into the engine.** Read node/contract `inputs`; on an edge whose producer declares outputs disjoint from the consumer's declared inputs, record a blocking `action: artifact-mismatch` under `--enforce-contracts` (warning in default mode, preserving backward compatibility). | `scripts/workflow-runner.py:628-696`, new helper near `:1056` | Selftest: a fixture edge `a(outputs:[x]) → b(inputs:[y])` under `--enforce-contracts` fails without advancing; the same fixture without the flag completes with a warning. | 1–2 days |
| R5 | ✅ **DONE — BM25F routing shipped.** `scripts/eval-routing.py` now indexes full skill bodies with a field-weighted BM25F plus a `Do NOT use` negative-trigger penalty, and gained a `--check` gate that exits non-zero below the floor. | `scripts/eval-routing.py`, `docs/benchmarks-vs-agent-skills.md`, `docs/B6-ROUTING-SCOPE.md` | Measured: **rank-1 55.6% → 58.7%**, top-N 63.5% → 71.4%, MRR 0.618 → 0.672, adversarial **0.0% → 14.3%** (2 of 14). The 75% target is **not reachable** stdlib-only and is stated as unreachable. PPMI query expansion was prototyped and **rejected**: it lifted adversarial to 14.3% but cost 14pp of overall rank-1 (55.6→41.3). | — |
| R6 | **Real mid-loop human interrupt.** Give `kind: human` gates pause semantics: stop traversal with `phase: awaiting-human`, write resume metadata to run-state, and accept a resume verdict. | `scripts/workflow-runner.py:1085-1177` | New selftest: a graph reaching a human gate returns `awaiting-human` with downstream nodes `pending`; resuming with an approve verdict completes the graph. | 2–3 days |
| R7 | **Delete or implement the dead constructs.** For each of `supervisor`, `task`, auto-gate `pass_when`/`else_go`, node `escalate_to`, `on_exhaustion`, `control.state.merge`, `join: any/majority`: either implement, or remove from the schema and flag it in the validator as unsupported. Silence is not an option — all eight currently validate. | `workflow/schema/workflow-manifest.schema.yaml`, `scripts/validate-workflows.py` | For every construct: either a selftest proves it fires, or `validate-workflows.py` reports it as unsupported on a fixture that uses it. | 3–5 days (all eight) |
| R8 | **Reconcile the 14 manifest nodes with their skill contracts.** Either the manifest declares the contract's own `inputs`/`outputs`, or the skill's `workflow.artifacts` is corrected. Add a validator gate so the next manifest cannot drift. | `workflow/manifests/*.yaml`, `scripts/validate-workflows.py` | A validator run over `workflow/manifests/` reports 0 node/contract contradictions; `--enforce-contracts` runs the flagship manifests with zero `contract-warning` entries. | 1 day + the content edits |
| R9 | **Make the payload registry real, or drop it.** Either have the engine assemble and validate the nine-key payload object (so the registry governs content, not just names), or reduce `CANONICAL_PAYLOAD_KEYS` to the keys any engine path actually produces. | `scripts/validate-workflows.py:36-39`, `:424-441`, `scripts/workflow-runner.py` | Every key in `CANONICAL_PAYLOAD_KEYS` has at least one engine-side write site, asserted by a selftest; or the registry is documented as name-only. | 1–2 days |
| R10 | **Give the chain graph composition authority in AgentOrg.** Replace (or gate) the static `_DOMAIN_SHAPES` chain with `SkillGraph.topological_order` over the goal's skills, falling back to the table when the graph cannot be built. | `AgentOrg/engine/planner.py:780-900` | Plan for a goal whose table chain contradicts the graph produces the graph's order; a new test asserts it. | 3–5 days |
| R11 | **Surface `_last_dropped`.** Serialise it into `Plan.as_dict()` alongside `dropped` and `graph_review` so the Owner sees the type mismatches the planner computed. | `AgentOrg/engine/planner.py:963`, `:398-402` | `Plan.as_dict()` contains `type_notes`; a test asserts a mismatched pair appears in it. | 0.5 day |
| R12 | **Adversarial routing set becomes a hard gate.** Once R5 lands, add the adversarial suite to `run-ci-locally.sh` with an honest floor (currently 0.0% — gate on *no regression*, not on the 50% target) so an embedding upgrade is measured against it. | `scripts/run-ci-locally.sh`, `scripts/eval-routing.py` | CI reports the adversarial number explicitly; it may not silently disappear from the report. | 0.5 day |

---

## 7. What "superior" would require

The control-flow core is already the strongest part of this repository: bounded loops that genuinely
terminate, exhaustion that escalates to a named target, atomic checkpoints, and cost accounting that
refuses to call an unmeasured run cheap. Those are the hard parts of running an agent graph
unattended, and they are done.

What is missing is the layer that turns declared structure into enforced structure. "Superior" would
mean artifacts are typed end to end — a producer's declared output is *the* thing the consumer's
declared input is checked against, at the edge, blocking by default rather than warning in a log.
That first requires the input side to actually name things someone produces: **107 of 119 declared
`inputs` currently have no producer in the corpus at all**, so today there is nothing to check
against. It would mean handoffs are immutable and hash-verified with a receipt the receiver must
present — the frozen-snapshot digest now shipped is the first half of that, but it attests the
*hop*, not the node records, so a whole-state Merkle digest is still missing. It would mean a human
gate actually interrupts a run mid-loop and the run resumes from the checkpoint with a verdict,
rather than a `kind: human` node quietly resolving `done`. It would mean loops can nest or decompose
into subgraphs — today a loop's members are a flat set and every edge inside it is suppressed until the
loop exits, so "work until done" cannot itself contain "work until done". And it would mean
retrieval runs over the bodies, not over the metadata: three quarters of the corpus's vocabulary was
unreachable, and BM25F over bodies recovered part of that (rank-1 55.6% → 58.7%) while the
adversarial suite's remaining 85.7% failure rate stays the honest measure of the gap.

None of it is out of reach — R1 through R6 are a fortnight of work and would move the library from
"a good traversal engine with a decorative integration layer" to something a downstream product can
trust without re-verifying it. Until then, the honest description is this: the engine's control flow
is superior, and the promises wrapped around it are, at present, mostly unimplemented assertions.

---

## Appendix — reproduction commands

```bash
# Engine correctness (all run from this repo root)
python3 scripts/workflow-runner.py --selftest                 # 27 checks, 0 failed
python3 scripts/validate-workflows.py --all                   # 6/6 OK
python3 scripts/validate-workflows.py --selftest              # 24 checks, 0 failed
python3 scripts/validate_chains.py                            # symmetric, no dangling refs
python3 scripts/check-flat-index.py                           # 327/327 flat-resolvable

# Routing (the honest floor)
python3 scripts/eval-routing.py                               # rank-1 55.6%, adversarial 0.0%
python3 scripts/build-skill-index.py --eval                   # 10-task baseline 40%/60%
node scripts/run-routing-evals.js                             # 72.8% (different corpus: 49 core)

# Declared-but-dead constructs (all run from this repo root)
grep -c 'consumes_from' ../Agent/AgentOrg/engine/planner.py   # 0 in the planner
grep -n 'inputs'  scripts/workflow-runner.py                  # no matches (typing inert)
grep -nE 'sha[^"]*[=!]=|mismatch' scripts/workflow-runner.py  # no matches (hash never verified)
grep -rn 'constraints' scripts/workflow-runner.py workflow/schema/   # no matches

# A real manifest from the downstream product is accepted despite node keys the schema omits
python3 scripts/validate-workflows.py --manifest ../Agent/AgentOrg/understand-indian-market.yaml
# -> OK

# Human-gate probe (a kind:human gate completes rather than pausing).
# The manifest needs a file named <name>.yaml whose `name:` matches, or the runner rejects it:
#   name: human-gate-probe / nodes: [{id: a, skill: backend-developer}] / gates: [{id: gate-human,
#   type: gate, kind: human}] / edges: [{from: a, to: gate-human}] / start: a / end: [gate-human]
python3 scripts/workflow-runner.py --manifest /tmp/probem/human-gate-probe.yaml --state /tmp/probem/state.json
# -> {"outcome": "complete", ... "gate-human": {"status": "done", "verdict": "pass"}}
```
