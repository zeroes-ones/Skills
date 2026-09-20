# Authenticity Remediation — 2026-09-19

> **Status:** complete. All governance gates green at the end of the work
> (`PASS: 14  FAIL: 0`, chains symmetric, 0 workflow failures, both engine selftests passing).
> **Scope:** the skill corpus (`skills/`). Every change is a content correction — no
> skill was added or removed, and no gate threshold was lowered.
> **Eight phases (A–H)** across **~280 changed files**: six classes of defect —
> fabricated citations, injected boilerplate, self-contradicting claims, a software-only rule
> blanket-applied to 29 domains, domain-folder names used as subject nouns, and 50 duplicate
> required sections.
> **Owner of record:** Sandeep Kumar Penchala.

## 1. Why this work happened

The library was audited against the question *"do these skills actually say true things?"* rather
than *"do these skills pass the linters?"* The linters were green throughout. The corpus was not
honest.

Three classes of defect were found, all of them invisible to the gate suite:

1. **Citations to artifacts that do not exist.** 196 skills instructed an agent to run
   `scripts/roi-gate.sh`, which has never existed in this repository. The real artifact is
   `scripts/calculate-roi.sh`, and it does not "return negative" — it computes a payback period.
   The gate suite only validates `(references/...)` markdown links, so a fabricated
   `scripts/...` path passed every check for months.
2. **Blanket-injected boilerplate.** An injector had written identical rows into many skills:
   eight `Complete when output is scoped to the request and grounded in evidence N` rows and ten
   `CRnn | Check: inputs pinned and sourced | Evidence: record result` rows. In several skills
   this boilerplate was the *only* thing satisfying gate G7 (≥ 8 "Complete when" statements) —
   deleting it without substitution would have failed the gate that was supposed to catch
   missing content.
3. **Self-contradicting and stale claims.** Stated corpus counts (223 skills / 457 broken chains)
   contradicted the filesystem and the governance gate. One skill asserted it had no upstream
   dependencies while its own frontmatter listed nine. Dollar figures carried fabricated
   precision with no derivation, including a broken template string rendering as
   `cost $40,000 cost`.

## 2. What was changed

### Phase A — mechanical authenticity sweep (182 files)

| Defect | Resolution | Files |
|---|---|---|
| `scripts/roi-gate.sh` cited (nonexistent) | Repointed to `scripts/calculate-roi.sh`; the "returns negative" claim corrected to the payback-period test the script actually implements | 182 |
| Stale corpus counts in prose (223 skills / 457 broken chains / 210+ skills / 28 domains) | Made to match verified reality or phrased count-free | 16 |

Automation: a one-shot `scripts/_phase_a_authenticity.py` (`--report` / `--apply`) performed the
sweep and was removed afterwards so it does not become an untracked entry in the script-integrity
manifest. It also *reported* the
dev-effort ROI rule's presence in non-code domains rather than blanket-editing them, since
whether a gardening or relationship skill wants a developer ROI gate is a per-skill judgement.
That judgement was then made — see Phase F.

### Phase F — the ROI rule made domain-agnostic (196 files)

Phase A fixed the *citation*. Phase F fixed the *scope*, which was the larger agnosticism defect:
the rule had been blanket-injected as a **software** rule into 196 skills across 29 domains,
including clinical, legal, HR and sales skills. It read:

> RUN the ROI Gate before any non-emergency **code** change. Every **code change** that is not
> (a) a security fix, (b) a compliance requirement, or (c) an active production incident must be
> evaluated with `scripts/calculate-roi.sh`. If the computed payback period exceeds 2 years,
> refuse to **write the code**.

A paediatric-clinical skill was therefore instructing its agent to weigh a *code change* against
an *active production incident*. The underlying principle — estimate the effort, compare it to the
annual value, refuse work whose payback exceeds two years — is universal and sound; only the
vocabulary was wrong. The rule now reads:

> RUN the ROI Gate before any non-emergency **change**. Every change that is not (a) a safety or
> compliance fix, (b) a regulatory requirement, or (c) an active incident must be evaluated…
> If the computed payback period exceeds 2 years, refuse to **do the work**.

The tool is retained where it is genuinely applicable: *"For software work,
`scripts/calculate-roi.sh` computes this from the files affected; otherwise apply the same
cost-vs-value judgement by hand."* 25 distinct line variants were normalised across all 196 files.
Verified residual: **0** occurrences of "non-emergency code change", "refuse to write the code",
or "code change that is not" anywhere in the corpus.

### Phase G — placeholder domain labels (29 skills across 6 domains)

The scaffold had substituted the **name of each skill's domain folder** into its body wherever the
body needed to name the skill's actual subject. `home-chef` — a cooking skill — contained 109 uses
of the phrase "home domestic", including a hard gate reading *"REFUSE to provide home domestic-specific
advice without verifying current regulations, tax laws, or guidelines"* and a keyword row reading
*"Search terms: 'Home Chef strategy', 'Home Domestic planning', 'Home Domestic basics'"*.

The same damage ran through the health-wellness, personal-growth, relationship-family,
philosophy-wisdom and travel-adventure domains. Each occurrence was replaced with wording from the
individual skill's real craft — cooking, gardening, interior design, decision-making, negotiation,
sleep, nutrition, Stoicism, relocation — rather than a single mechanical substitution.

| Domain label | Skills | Occurrences each | Residual |
|---|---|---|---|
| `home domestic` | 4 | ~109 | 0 |
| `personal growth` | 8 | ~105 | 0 |
| `health wellness` | 7 | ~105 | 0 |
| `relationship family` | 2 | ~105 | 0 |
| `philosophy wisdom` | 4 | ~105 | 0 |
| `travel adventure` | 3 | ~105 | 0 |

A corpus-wide follow-up scan found the same pattern in `33-real-estate`, where the label is the
genuine subject — correctly left alone.

### Phase H — duplicate required sections (50 instances)

A blanket injection had appended a second copy of a required section heading to many skills.
Because both copies carried the *same required heading*, every linter passed — but the document
stated the section twice and a reader could not tell which was authoritative. `Ground Rules`
accounted for 41 of the 50 instances (the injected twin was titled
`Ground Rules — Read Before Anything Else` and carried a generic two-row table alongside the
skill's real negative-constraint table).

Each pair was merged into one section: the skill-specific table stays as the main body, the generic
table folds in beneath a `### Baseline rules` sub-heading, and the duplicate heading is removed.
No rule rows were deleted — the two tables are disjoint.

One trap surfaced and is worth recording: `scripts/validate-skills.sh:124` requires the **literal**
heading string `Ground Rules — Read Before Anything Else`, while `scripts/lib/lint-template.py:91`
fuzzy-matches on the `Ground Rules` prefix. Merging to the bare heading therefore keeps the
template linter green while failing the governance gate. That asymmetry is precisely why the
duplicate shipped undetected.

Verified: **0** duplicate required sections remain, scan-confirmed fence-aware (headings inside
```markdown example blocks are correctly not counted).

### Phase J — the dangling script citations (199 files, follow-up on 2026-09-19)

Phases A and F fixed *which* script the ROI rule names and *what scope* the rule has. Neither fixed
**where the script lives**. Counting all markdown under `skills/`, `scripts/calculate-roi.sh`
(392 citations across 197 files) and `scripts/runtime-version-detect.sh` (206 citations across 198
files) exist only at this library's root `scripts/`; neither `scripts/install.sh` nor
`scripts/init-project.sh` deploys them (`grep` over both installers returns nothing), and no citing
skill said so. An agent in a consumer project was instructed to run a path that does not exist —
the rule silently failed and the skill's own gate became theatre.

Every citation now states the universal procedure in words and mentions the helper only
conditionally ("if your project ships `scripts/calculate-roi.sh`, run it; otherwise …"). Residual
counts are unchanged — 196 `calculate-roi.sh` and 198 `runtime-version-detect.sh` occurrences —
because the task is to qualify the citation, not delete it. What changed is that **0** of those
occurrences now sit on a line lacking the conditional phrase (before: 392 and 206, i.e. every one).
No gate threshold was lowered and no "Complete when" criterion was removed (the per-skill
`grep -c 'Complete when'` count is unchanged in all 327 files).

### Phase I — verification

Re-run after every phase; final state below.


### Phase B — the loop/graph core cluster (11 files)

The skills whose subject matter *is* loops, graphs, nodes and orchestration were fixed first,
because they are the load-bearing ones.

| Skill | Defect fixed |
|---|---|
| `workflow-graph-authoring` | Cited validator rules V1–V9; the schema defines V10 (agent-gate contract). Updated at 5 sites, added V10 as an enumerated rule, and added the skill's own `workflow:` contract — the skill about node contracts had no contract. |
| `iterative-task-execution` | Added its `workflow:` contract, with criteria drawn from its own G1–G7. Verified end-to-end under `--enforce-contracts`: a stub executor missing evidence now produces `outcome: contract-violation`. |
| `cross-skill-communication` | Removed the false "223 skills, 457 broken chains" premise throughout; added an **Implementation status** table separating tooling-backed mechanisms (the payload registry, enforced by `validate-workflows.py`) from conventions the reader must build (the message envelope, pub/sub registry, circuit breaker — none exist in this repo). Removed three fabricated `[VERIFIED]` tags. |
| `agent-handoff-protocol` | Resolved the "no upstream dependencies" contradiction against 9 declared `consumes_from` entries. Rewrote R9/R10 from generic bolted-on template rules into handoff-specific ones. Stated the `~/.agents/state/handoffs/` path as a **convention** — no tool creates or verifies it. |
| `agent-persona-orchestrator` | Corrected "personas cannot invoke personas / sequential chains unsupported" into the precise, true rule: no persona spawns another persona, but a workflow MAY sequence personas behind an explicit artifact. Replaced auto-generated filler tables. |
| `multi-agent-orchestration` | Repaired four ASCII diagrams that contained a literal `...` where art was cut (content recovered from the skill's own `references/`). Resolved the `max_depth` contradiction (3 in rules, 5 in code sample, 5 in a gotcha) to a single value. |
| `using-agent-skills` | Fixed a wrong `wayfinder` path, replaced three one-line "decision trees" with real branching trees, removed identical boilerplate rows, fixed a malformed Cross-Skill Coordination table. |
| `wayfinder` | Rebuilt a degenerate Anti-Rationalization table in which the rationalization column read `"It is faster to skip this: <failure description>"` and the "why it is wrong" column repeated that same text — the failure was pasted where the excuse belonged. |
| `agentic-complexity-ladder` | Fixed the broken `cost $40,000 cost` string and tagged all 20 unsourced dollar figures `[ESTIMATED]` with an explicit scope-limiting note, following the convention already used in `agent-runtime-economy`. |
| `verification-independence-engineer` | Found "three properties" contradicting four elsewhere; added the missing **role** property and gave each of the four axes a mechanical enforcement test in `references/independence-properties.md` (only Information had one). |
| `incremental-implementation` | Fixed a `workflow.completion.criteria` entry that was both un-checkable and self-contradictory: it banned `ALTER`, which the skill's own body mandates as `ALTER TABLE ... ADD COLUMN`. |

Result: declared `workflow:` contracts went from **62 → 64**.

### Phase C — corpus-wide content repair (52 files)

| Defect | Resolution | Files |
|---|---|---|
| Injected `Complete when … grounded in evidence N` rows | Replaced with criteria specific to each skill's own subject (options structures, backtesting, mortgage math, commodities spreads, …) | 17 |
| Injected `CRnn \| Check: inputs pinned and sourced \| Evidence: record result` tables | Replaced with subject-specific checklist items drawn from each skill's body | 11 |
| Duplicate required sections (`Error Decoder` ×36, `Gotchas` ×7, `Production Checklist` ×5, `References` ×1) | Merged into one section each, preserving the richer content | 45 |
| Broken `**$N cost**` template strings and unsourced money ranges | Repaired and tagged `[ESTIMATED]` with the house scope note | 11 |
| Four independence properties named inconsistently (`authority` vs `role`) | Unified to model / context / information / **role**; authority kept where it means enforcement power, but no longer listed as an independence axis | 4 |
| Citations to nonexistent tooling (`verify-skill.sh --ground-rules`, `run_agent_eval.py`, `check-dag.sh`) | Repointed to real harnesses or marked as tooling the reader must build | 3 |

Verified after Phase C: **zero** occurrences of `Evidence: record result`,
`Check: inputs pinned and sourced`, `grounded in evidence N`, `**$N cost**`, or `roi-gate.sh`
anywhere in the corpus, and **zero** non-framework skills below the 8-criterion G7 minimum.

### Phase D — documentation truth

`AGENTS.md` carried stale counts (322 skills, 59 contracts, 317/322 references, 128/322 examples).
Refreshed against the filesystem: **327 skills, 37 domains, 64 contracts, 326 references,
133 examples, 224 evals, 7 assets** — each with the command that re-checks it.

## 3. How the work was verified

Every gate was run before and after, and nothing was marked done on the strength of a diff alone.

| Gate | Before | After |
|---|---|---|
| `bash scripts/validate-skills.sh` | `PASS: 14  FAIL: 0` | `PASS: 14  FAIL: 0` |
| `python3 scripts/validate_chains.py` | 0 asymmetries | 0 asymmetries |
| `python3 scripts/validate-workflows.py --all` | 6/6 OK | 6/6 OK, 0 FAIL |
| `python3 scripts/validate-workflows.py --selftest` | 24 checks, 0 failed | 24 checks, 0 failed |
| `python3 scripts/workflow-runner.py --selftest` | 27 checks, 0 failed | 27 checks, 0 failed |
| `lint-markdown` on changed files | clean | clean (327 files, whole corpus) |
| `lint-template` errors | 0 | 0 (warnings are pre-existing) |
| `lint-files` on changed files | clean | clean (275 files) |
| Generated artifacts (`emit-skill-graph`, `emit-marketplace`, `emit-skill-registry`) | fresh | fresh |
| `check-flat-index.py` | 327/327 resolve | 327/327 resolve |
| Declared `workflow:` contracts | 62 | 64 |
| Library audit | 9.8/10 | 9.8/10 (327 skills) |

Four verification results are worth recording because each is stronger than a lint pass:

- The new `iterative-task-execution` contract was proven **live**: a throwaway manifest run with
  `--enforce-contracts` over a stub executor produced `outcome: contract-violation`, and turned
  green only when the executor returned evidence and covered the declared criteria.
- The `roi-gate.sh` sweep was proven **complete**: the residual count went to 0 across all 327
  skills, not merely down.
- The duplicate-section class was proven **cleared** by a fence-aware scan of all 22 required
  headings across all 327 skills, returning 0. A naive scan reports false positives because
  several skills legitimately contain a `## References` heading inside a fenced example block.
- The placeholder-label class was proven **cleared** by `grep -ci` returning 0 for all six domain
  labels, plus a corpus-wide sweep for the same pattern in every other domain.

## 4. Deliberate non-changes

These were found, judged, and left — recorded so they are not rediscovered as surprises:

1. ~~**The dev-effort ROI rule (R9/R10) still appears in ~150 skills including non-code domains.**~~
   **Resolved in Phase F** — the rule is now domain-agnostic and the software tool is scoped to
   software work.
2. **`scripts/verify-skill.sh` exists in 330 copies and is largely self-referential** — it greps
   the skill's own text for required phrases rather than testing behaviour. That is a design
   limitation worth a separate project.
3. **`cross-skill-communication/references/verify-skill.sh` still greps for the string `457`.**
   It passes only because the alternation also matches "broken chain". Latent trap; left because
   the file is covered by `scripts/.sha256manifest` and editing it is a separate hash-affecting
   decision.
4. **`writing-great-skills` is genuinely missing `## Best Practices`** — pre-existing, and the
   template linter only warns on it for `00-framework` skills. Adding a section is authoring work,
   not a correction.
5. **290+ skills exceed the 500-line advisory body budget.** Pre-existing and unchanged; the
   corpus-wide remedy is a pruning pass, not an authenticity fix.
6. **The dollar magnitudes remain unmeasured.** They are now *labelled* `[ESTIMATED]` with a scope
   note, which is honest. A defensible number would need a cited source or a stated derivation
   (engineer-days × loaded day rate) per figure — still open.

## 5. Conventions this work established

- **Provenance tags for any quantified claim.** `[VERIFIED <date>]`, `[COMPUTED]`, `[ESTIMATED]`,
  `[COMMON-PRACTICE]`, `[UNKNOWN]`. An untagged dollar figure is now a defect.
- **Never cite a script as existing without checking.** If a skill needs a tool that is not in the
  repository, say so and describe the shape the reader must build.
- **Boilerplate that satisfies a gate is worse than a missing section**, because it makes the gate
  lie. Every checklist row must be specific enough that it could not appear in another skill.
- **Counts are computed, not remembered.** `AGENTS.md` now pairs every figure with its command.

## 6. Follow-up work (not in this remediation)

| # | Item | Why it is separate |
|---|---|---|
| 1 | ~~Scope the ROI rule per domain~~ | **Done in Phase F** |
| 2 | Make `verify-skill.sh` test behaviour, not phrasing | 330 files; a tooling project |
| 3 | Prune the 290+ over-budget skill bodies | Content work, not correction |
| 4 | Give every `[ESTIMATED]` figure a source or derivation | Needs per-figure research |
| 5 | Convert the remaining 263 skills to declare a `workflow:` contract | Authoring; 64 of 327 done |
| 6 | Execute the 38 Tier-3 behavioural eval scenarios (currently 0 run) | Needs a live agent harness |
| 7 | **Reconcile the duplicate-heading gate asymmetry** — `validate-skills.sh:124` requires the literal `Ground Rules — Read Before Anything Else` while `lint-template.py:91` fuzzy-matches the prefix. That mismatch is what let 50 duplicate sections ship undetected. | Touches a blocking gate script; needs the owner's call on which form is canonical |
| 8 | **Add a corpus gate for domain-agnosticism** — nothing currently detects a domain-folder name being used as a subject noun, which is how ~640 placeholder occurrences reached production | New gate; needs an owner decision on the heuristic |
