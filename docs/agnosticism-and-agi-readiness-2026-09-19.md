# Agnosticism, Independence and AGI-Readiness — Assessment

Date: **2026-09-19** · Repo: `/Users/sp.vm/Documents/Projects/Skills` · Corpus: **327 skills**, 37 domains
(`find skills -name SKILL.md | wc -l`, `ls -d skills/*/ | wc -l`)

Question asked: *(1) how agnostic is this corpus in fact, (2) can it build other products or only the
one it is used by, (3) does it provide solid foundations for robust agentic programs?*

Method: every number below was produced in this checkout by the command printed beside it. Where a
claim could not be reproduced, that is stated and the figure is marked **unverified**. Line citations
are to the files as they exist today. The working tree is dirty (several agents editing at once); §8
names the consequence.

---

## 1. Executive verdict

**The corpus is genuinely concept-agnostic and genuinely not delivery-agnostic.** Zero tracked files
reference the downstream consumer or its invented vocabulary (`git grep -l AgentOrg` → 0; `Posture` /
`UNATTENDED` / `auto-staffing` / `roster of agents` → 0 as consumer terms); all 327 skills carry
symmetric, product-neutral `chain:` blocks (`validate_chains.py` → PASSED); and the
Claude/Copilot/Cursor/Gemini mentions across all 327 files are portability *declarations*, not
coupling. That half is real and worth stating plainly.

What is not agnostic is how the skills reach the reader's machine. **206 of 327 skills instruct the
reader to run a script that exists only at this repository's root** — `scripts/calculate-roi.sh` in
196, `scripts/runtime-version-detect.sh` in 198 — and **not one of the 394 lines naming either script
says where it lives**; neither is shipped by an installer. Independent of delivery: **312 reference
files are the same 11-line stub under eight different filenames** in 39 skills (9.4% of all 3,303
reference files, zero domain content), and only one reference file in five names a regulation, vendor
or standard at all, so "specific by reference" is largely unmet.

As an AGI foundation it is a **strong design library and a weak implementation library**. All 334
code fences across 13,271 lines in `skills/22-ai-engineering/*/SKILL.md` include exactly **6
language-tagged fences**; the rest are ASCII decision trees. Only **12 of 328 skill directories ship
runnable tooling** beyond the generic `verify-skill.sh`, and the single thing every agentic design
assumes — a runnable agent loop — is a nine-line prose block at
`skills/22-ai-engineering/ai-engineer/SKILL.md:254-262` and nothing else. The engine's contract gate
is **unsatisfiable** with the shipped executor, its behavioural suite has **38 scenarios and 0
recorded outputs**, and its headline quality score comes from a script that cannot exit non-zero.

---

## 2. What is genuinely agnostic, and why

| # | Property | Evidence | Why it holds |
|---|---|---|---|
| 1 | Zero references to the downstream consumer | `git grep -l AgentOrg -- . \| wc -l` → **0** | The corpus does not name the product that consumes it. Nothing to decouple. |
| 2 | No consumer-invented vocabulary | `git grep -ril 'auto-staffing' -- skills \| wc -l` → 0; `'roster of agents'` → 0; `'UNATTENDED'` (case-sensitive) → 0; `\bPosture\b` hits are all `security posture` / `CSPM` / a Jetpack `Posture API` | The consumer's terms are absent. `unattended` appears case-insensitively in unrelated senses (`healthcare-ui-designer` idle-timeout prose, `incident-responder` on-call prose) — not the consumer's concept. |
| 3 | Symmetric, product-neutral chain blocks | `python3 scripts/validate_chains.py` → `Skills checked: 327` / `Chain validation PASSED` | 327/327 declare `consumes_from`/`feeds_into` and every edge is bidirectionally symmetric. `chain` is sequencing (`README.md:27`), not artifact supply. |
| 4 | Agent portability mentions are declarations | `grep -rlE 'Claude Code\|Copilot\|Cursor\|Gemini CLI\|Codex' skills --include=SKILL.md \| wc -l` → **327** | Naming the hosts a spec runs on is the opposite of coupling — it is the agnosticism claim. These are not imports, paths or host APIs. |
| 5 | Cross-skill coordination is by *name*, not by repo path | 96/327 SKILL.md contain a domain-qualified repo path (§3.2); the other 231 do not | Coordination via `chain` and skill names is portable; only the minority leak layout. |
| 6 | The engine is dependency-free and stdlib-first | `AGENTS.md` §3; `workflow-runner.py` and `validate-workflows.py` import only `lib/safe_yaml.py` | No product-specific runtime is required to run the graph executor. |

---

## 3. Agnosticism defects, ranked

### 3.1 Library-root tooling cited as if it were the reader's own (largest defect)

```
$ grep -rl 'calculate-roi\.sh'          skills --include=SKILL.md | wc -l   # 196
$ grep -rl 'runtime-version-detect\.sh' skills --include=SKILL.md | wc -l   # 198
$ union                                                                     # 198 of 327 skills
$ occurrences in SKILL.md                                                   # 391 + 206 = 597
$ grep -rn 'calculate-roi\.sh' skills --include=SKILL.md \
    | grep -c 'zeroes-ones\|repo root\|this library\|~/.zeroes'             #   0
```

Neither file is reachable from an installed project. `scripts/install.sh` clones the repo to
`$SKILLS_HOME` and links **only** `$SKILLS_HOME/skills-flat` (`scripts/install.sh:57`);
`init-project.sh` links the same flat layer (`scripts/init-project.sh:100-102`), and
`grep -n 'calculate-roi\|runtime-version-detect' scripts/install.sh scripts/init-project.sh` returns
nothing. A consumer following a skill's instruction runs a path that does not exist in their project,
and **zero of the 394 lines** naming either script says it is library tooling rather than project
tooling. The cited behaviour is reasonable — `skills/05-development/frontend-developer/SKILL.md:245`
runs `runtime-version-detect.sh [project-root] --skill-context` to anchor framework API calls;
`skills/14-finance/algorithmic-trader/SKILL.md:225` runs `calculate-roi.sh` to refuse unprofitable
work — but the skill never says the script ships with the library, and the library does not ship it.

> **Correction to the brief.** "594 citations across 206 of 327 skills": reproduced as **198** skills
> citing at least one of the two, with **594** being the occurrence count across the 394 lines. The
> count I stand behind: **198 of 327 skills, 676 library-root citations in total**.

### 3.2 Boilerplate stubs masquerading as reference material

```
$ find skills -path '*/references/*' -type f | wc -l            # 3303
$ find skills -path '*/references/research-sources.md' | wc -l  #   39  -> 312 non-README siblings
$ # normalised body hash, H1 stripped: 39 distinct bodies across 312 files; 312/312 (100%) share
$ # a body with a sibling
```

`skills/35-home-domestic/home-chef/references/` holds nine files. Eight (all bar `README.md`)
contain the identically wrong text `Research citation for home-chef v1.0. [VERIFIED] Sources from
industry standards and peer-reviewed literature.` A file named `compliance-checklist.md` holding a
*research citation* is not a compliance checklist; a `glossary.md` holding one is not a glossary. The
same eight-file set repeats across 39 skills in nine low-domain domains (`29-personal-finance` ×9,
`30-health-wellness` ×7, `31-personal-growth` ×8, plus `32`–`36`) — **312 of 3,303 reference files
(9.4%)** with zero domain content, the opposite of the library's own rule: "Keep industry-specific
guidance in `references/`" (`AGNOSTIC-PRINCIPLES.md:9`).

> **Resolved 2026-09-20.** All 312 stub files were **deleted** (39 skills × 8), because every one
> carried a false `[VERIFIED]` tag asserting sources that do not exist — worse than an absent file —
> and **0 were linked** from any `SKILL.md`. Reference total 3,303 → 2,991. The `references/`
> directories are retained (gate G11 requires the directory). Those 39 skills now have *no* domain
> references: the gap is honest rather than fake. See
> `docs/foundations-remediation-2026-09-20.md` §5.2.

### 3.3 "Specific by reference" is largely unmet

The library's named reference targets are referenced by **zero** skills:

```
$ grep -rl 'industry-compliance-matrix\|industry-patterns' skills --include=SKILL.md | wc -l   # 0
```

They are named in `AGNOSTIC-PRINCIPLES.md:14-15,34,39,63`. `industry-compliance-matrix.md` exists at
exactly one path (`skills/11-legal/regulatory-specialist/references/industry-compliance-matrix.md`);
`industry-patterns.md` exists nowhere. With the brief's own term list (FDA HIPAA GDPR SOC 2 ISO 27001
PCI DSS OAuth Kubernetes PostgreSQL Snowflake dbt Kafka FHIR HL7 SNOMED Dodd-Frank FASB ASC 606 IFRS
Reg T MiFID Basel III WCAG CCPA FERPA OSHA NIST Terraform Docker + 8 vendors):

```
brief's exact term list: 725 / 3303 (21.9%)
```

Narrower sets score lower (regulation names only: 400 files, 12.1%). The brief's **7.9% is not
reproducible** — it is below even the narrowest set I could build — so I report **21.9%** for the
specified list. Either way, four reference files in five are domain-neutral prose.

### 3.4 Cited scripts that do not exist

```
cited as scripts/<name> : 58 distinct    # 17 exist in repo scripts/, 41 absent
  absent but per-skill  : 28  -> 74 citations
  absent NOWHERE        : 13  -> 13 citations
```

The 13 named nowhere: `attrition-by-manager.sh`, `benchmark_embeddings.py`, `bootstrap_eval.py`,
`check-external-visibility.sh`, `detect-select-star.sh`, `eval_retrieval.py`, `ioc-health-check.py`,
`pre-push-check.sh`, `redirect-audit.sh`, `sanitization-audit.py`, `verify-citations.sh`,
`verify-code-examples.sh`, `verify-x.sh` (each confirmed at zero locations via
`find . -name '<n>' -not -path './.git/*' | wc -l`). Example: `ai-engineer/SKILL.md:120` tells the
reader to "Run `python scripts/bootstrap_eval.py` to scaffold the eval harness" — the file does not
exist.

> **Corrections to the brief.** (a) `run_eval.py` and `check_calibration.py` **do exist**; the real
> defect is §3.1 one level down — `llm-engineer/SKILL.md:721` and `ml-engineer/SKILL.md:532` write
> `python scripts/<name>.py`, reading as *repo-root* `scripts/` when the file is per-skill. (b) The
> "broken relative links at `skills/14-finance/personal-finance/SKILL.md:495-498`" **resolve** — all
> six cited targets exist under the skill directory (checked with `-e` on each).

### 3.5 US locale baked in

`skills/14-finance/personal-finance/SKILL.md:251,276-278` hardcode the 2025 US limits — "Roth IRA
($7K limit)", "HSA max ($4,300/$8,550, 2025)", "Roth IRA max ($7,000/year)", "401(k) to annual limit
($23,500)" — with no jurisdiction qualifier on the line; the checklist at `:432` restates them.
`skills/29-personal-finance/retirement-planner/SKILL.md:18,39,62,380` treats 401k/IRA/Social
Security/PIA as the default retirement vocabulary, and the qualifier it does carry is generic and
buried (`retirement-planner/SKILL.md:164`: "laws vary by location"), not attached to the figures.
Currency: **7,343** dollar-magnitude tokens (`\$[0-9]+(\.[0-9]+)?[KMB]`) across **258** skills;
`\$50K` alone appears **1,032** times — the brief's figure, reproduced.

### 3.6 The portability banner is a claim nothing checks

All **327** SKILL.md print a portability banner (`grep -rl 'Portability target' … → 327`); only
**83** declare the matching `portability:` frontmatter key (`grep -rl '^portability:' … → 83`). The
validator checks only the banner string: `scripts/lib/lint-template.py:228-231` requires "a
portability target declaration (e.g., '> **Portability target:** Spec-level.')" and
`scripts/validate-skills.sh:200-212` greps for the banner. Nothing reads the frontmatter key, and 244
skills have the banner without the field. The banner is a *claim about the skill*, not a *field the
machine can act on* — which is why "Spec-level" can be asserted by a skill whose only executable path
is an unshipped root script.

---

## 4. Independence verdict

**Clean.** Zero coupling to the consumer's identity or vocabulary:

```
$ git grep -l 'AgentOrg' -- . | wc -l                 # 0
$ git grep -l 'reasonix' -- . | wc -l                 # 3 — all metadata (.gitignore:34,38; AGENTS.md:83)
$ git grep -ril 'auto-staffing' -- skills | wc -l     # 0
$ git grep -ril 'roster of agents' -- skills | wc -l  # 0
```

The three `reasonix` hits are a local agent-runtime config entry and its documentation, not a skill
dependency. The concept layer is portable.

**Coupled — three ways, in increasing severity.**

1. **Delivery coupling (198/327 skills, 676 citations).** §3.1. Every skill saying "run
   `scripts/calculate-roi.sh`" is written for a reader standing inside *this repository*.
2. **Layout coupling (210/327 skills).** `skills/<domain>/<name>/…` paths are meaningful only in the
   nested store. The flat layer the consumer links
   (`skills-flat/<name> -> ../skills/<domain>/<name>`, `readlink skills-flat/code-reviewer`) exposes
   no `skills/<domain>` level. Installing one skill the way the installer does and resolving a cited
   path fails:

   ```
   $ ln -s .../skills/14-finance/options-automation-engineer /tmp/x/options-automation-engineer
   $ (cd /tmp/x && ls skills/14-finance/options-automation-engineer/examples/backtest)
   ls: skills/14-finance/options-automation-engineer/examples/backtest: No such file or directory
   ```

   210 SKILL.md contain a domain-qualified path (265 instances); 96 point at a *different* skill
   (`skills/00-framework/skill-levels/` alone is referenced by ~90 skills), and every one breaks under
   flat. The other 231 skills coordinate by name and are unaffected.
3. **One genuine cross-repo coupling — remediated in the working tree while this was written.**
   `skills/13-specialized/agent-handoff-protocol/SKILL.md:249-252` teaches a `constraints` array as a
   handoff payload field, and the consumer populates exactly that key
   (`AgentOrg/engine/executor.py:1124-1126`, read this checkout). At `HEAD`, `CANONICAL_PAYLOAD_KEYS`
   omitted it (`git show HEAD:scripts/validate-workflows.py:36-40`), so a manifest declaring it was
   rejected — running the `HEAD` validator against a probe gives `FAIL … payload hand: keys outside
   registry: constraints`. The tree now carries `"constraints"` at
   `scripts/validate-workflows.py:38` and the probe validates `OK`, but that change is
   **uncommitted** — it must land with the skills that teach the field.

**The single change that most improves independence.** Qualify or bundle the two root scripts: ship
them through `init-project.sh` (link them into the activated project), or rewrite the 394 citing lines
to name the library path and state the script lives in the library, not the project. One afternoon of
script edits plus one content sweep; it is the difference between "agnostic concepts,
repository-bound delivery" and a corpus that works from a flat install.

---

## 5. AGI-readiness: coverage matrix

Judged on what a skill *ships that can run*, not what it discusses. "Runnable tooling" = a `.py`/`.sh`
in `skills/<domain>/<name>/scripts/` other than the generic `verify-skill.sh`:

```
per-skill runnable scripts (excluding verify-skill.sh): 32
skills owning at least one                            : 12
```

`skills/22-ai-engineering` is 19 skills: **5** ship tooling (ai-engineer 5 files, mlops-engineer 4,
llm-engineer 4, context-optimizer 1, token-efficiency 1); the other **14 ship none**. Adding
`skills/00-framework` (6 skills, 0 files) gives 25 agent-adjacent skills, 5 with tooling. The brief's
"5 of 43" is right on the ratio but the denominator is not reproducible here without inventing
membership rules; the reproducible pair is **5 of 25** on the two domains owning the agentic surface,
**12 of 328** corpus-wide.

| Capability | Status | Evidence |
|---|---|---|
| Context management / compaction | **COVERED (design)** | `context-compaction-strategies`, `context-engineering`, `context-optimizer` (ships `context-audit.sh`), `token-efficiency` (ships `token-cost-calculator.py`) |
| Multi-agent coordination | **COVERED (design)** | `multi-agent-orchestration`, `agent-handoff-protocol`, `agent-persona-orchestrator`; concept-only, no tooling |
| Cost control | **COVERED (partial)** | `cost-accounting` (no tooling); `ai-engineer/scripts/estimate_cost.py`, `llm-engineer/scripts/estimate_cost.py` |
| Guardrails | **COVERED (design)** | `ai-security`, `ai-safety-engineer`, `applying-llm-guardrails`; engine-side `scripts/lib/guardrails.py`; no per-skill classifier ships |
| Agent loop control | **PARTIAL** | Nine-line spec at `ai-engineer/SKILL.md:254-262`; no implementation (§6.1) |
| Tool calling | **PARTIAL** | `ai-engineer/SKILL.md:258-260` names tool schema/selection; 7 skills mention "tool call"; no runnable harness |
| Structured output | **PARTIAL** | 6 skills mention it; `llm-engineer/scripts/validate_output.py` is the only shipped validator |
| RAG | **PARTIAL** | `llm-engineer`, `data-engineer`, `ai-engineer`; `eval_retrieval.py` cited by `ai-engineer` does **not exist** |
| Memory | **PARTIAL** | `agent-memory-architect` — no tooling |
| Evaluation | **PARTIAL** | `agent-eval-pipeline` (no tooling), `mlops-engineer` (4 files), `ai-engineer` (5 files); corpus-level see §6.2 |
| Observability | **PARTIAL** | `observability-engineer`, `mlops-engineer/scripts/profile_gpu.py`; no agent-trace tooling in `22-ai-engineering` |
| Human-in-the-loop | **PARTIAL** | Design only; the engine does not pause on a human gate (`docs/handoff-and-routing-assessment-2026-09-19.md` §3 B8) |
| Retries / backoff | **PARTIAL (boilerplate)** | `Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s)` appears in **179 of 327** skills — identical wording, no implementation |
| Tool-error handling | **ABSENT** | 2 of 19 `22-ai-engineering` skills mention a failing tool; no skill, no script |
| Planning / decomposition | **ABSENT** | 1 of 19 mentions decomposition |

**Top gap.** One dominates: **there is no runnable agent loop.** Every other capability presupposes
one and the corpus does not contain it. The complete artefact is
`skills/22-ai-engineering/ai-engineer/SKILL.md:253-262` — nine lines of prose ("DESIGN THE AGENT LOOP:
1. Define tools… 6. Safety…"), and the only `while True` in any shipped per-skill script is in
`mlops-engineer/scripts/profile_gpu.py`. Tool-error handling and planning/decomposition are absent
outright. Second order: 6 of 334 `22-ai-engineering` fences are language-tagged, and 46 of 327 skills
contain any language-tagged fence (67 such fences corpus-wide).

---

## 6. The six foundational weaknesses, ranked

### 6.1 Contract enforcement is unsatisfiable with the shipped executor — and off by default

`_contract_violations` (`scripts/workflow-runner.py:849-895`) blocks a node when `completion.criteria`
is declared and `criteria_met` is empty, requiring every criterion be covered. **No shipped executor
emits `criteria_met`:** `grep -rn 'criteria_met' scripts/executors/ | wc -l` → **0**;
`grep -rln 'criteria_met' scripts/` → `scripts/workflow-runner.py` only. The real agent executor
returns `{"status": "done", "verdict": …, "summary": …, "evidence": […]}`
(`scripts/executors/agent_executor.py:420-422`) — evidence yes, `criteria_met` never. Under
`--enforce-contracts`, **every contract-declaring node with criteria is mechanically a violation**
regardless of work quality. The flag is also unused in CI: `grep -rn 'enforce-contracts'
.github/workflows/ | wc -l` → 0, and `grep -n 'enforce-contracts' scripts/run-ci-locally.sh` → nothing.

**Blast radius.** A consumer enabling the flag for contract enforcement gets a rework loop that never
converges or an escalation storm — and 64 skills declare a `workflow:` contract.
**Fix.** Have the executor emit `criteria_met` (it already receives the compiled criterion list; the
transcript can be parsed for coverage), then add one CI job running a flagship manifest with
`--enforce-contracts`.

### 6.2 No behavioural regression detection

`evals/tier3-behavioral/` holds **38 scenarios across 7 suites covering 17 skills, with 0
`recorded_output`**. `node scripts/run-behavioral-evals.js` → `Passed: 0 | Failed: 0 | Skipped: 38`,
`Result: NO EVIDENCE`. Golden cases cover **3 of 327 skills**
(`evals/golden/{code-reviewer,iterative-task-execution,qa-engineer}/cases.json`;
`bash scripts/eval-skill.sh --all` → `3 skill(s) green`).

> **Correction to the brief.** "all-skipped exits 0 (false green)" describes **`HEAD`**, not the
> working tree. `git show HEAD:scripts/run-behavioral-evals.js:379` →
> `process.exit(failed.length === 0 ? 0 : 1)`; running the `HEAD` file against a corpus copy gave
> `Total: 38 … Result: FAIL` → **`exit=0`**. The working-tree runner exits 1, and CI invokes it
> (`.github/workflows/validate.yml:224-225`). The fix is in flight, uncommitted.

**Blast radius.** "The skills behave as documented" is untested for 310 of 327 skills.
**Fix.** Record real agent sessions into `recorded_output` for a first tranche of ~20 scenarios
pinning the highest-risk behaviours (tool-error handling, escalation, negative constraints), then
ratchet the count like the routing floor.

### 6.3 Routing: below target, and the target gate is unwired

```
$ python3 scripts/eval-routing.py                  # 63 scenarios, full bodies, BM25F
rank-1 hit rate : 58.7%   top-N: 71.4%   MRR: 0.672   must-not violations: 6
  routing-semantic-adversarial: n=14 rank1=14.3% topN=35.7%

$ node scripts/run-routing-evals.js                # 49 core cases, TF-IDF
Rank-1 hit rate: 72.8% (target: 80%)   MRR: 79.9% (target: 90%)   Result: FAIL
```

Targets are `docs/B6-ROUTING-SCOPE.md:54-60`: rank-1 ≥ 75%, adversarial ≥ 50%, MRR ≥ 0.80. Neither
harness reaches them. CI runs the harness **only in ratchet mode**
(`.github/workflows/validate.yml:221-222`, `scripts/run-ci-locally.sh:190`), gating on the recorded
floor in `evals/routing-baseline.json` (rank-1 0.72, MRR 0.79) and exiting 0 while the target is
unmet. `eval-routing.py --check` exists and exits 0 today (`RANK1_FLOOR = 55.0`,
`scripts/eval-routing.py:280`) but **no CI job or hook invokes it**.

> **Correction to the brief.** "Routing is invoked by no CI job" is wrong for the harness: the ratchet
> **is** wired (two CI steps plus `run-ci-locally.sh`) and is honest about being a floor, not a target.
> What is unwired is the `--check` gate on the fuller 63-scenario harness.

**Blast radius.** Any component picking a skill without a human inherits 27% rank-1 failure on
ordinary prompts and 86% on paraphrased ones.
**Fix.** Wire `eval-routing.py --check` into the measurement job with the floor raised to the current
58.7%, so the reported number is gated against regression.

### 6.4 Progressive disclosure is declared but not implemented — and the budget gate is tautological

**307 of 327** skills carry `<!-- QUICK: 30s -->`, but **no script slices on it**: the only hits for
that marker in `scripts/` are `skill-factory.py` (emits it in a scaffold template),
`upgrade_to_10_v2.py` (injects it into existing skills) and `lint-template.py:82` (strips it for
linting). The compiled XML drops the headings entirely, and with `AGENT_SKILL_DEPTH=0` the executor's
documented fallback is a positional cut — `_truncate_words`
(`scripts/executors/agent_executor.py:252-257`): `words = words[:budget]`, "the first `budget` words,
whatever section that lands in". At the default 1,200-word budget (`AGENT_SKILL_WORDS`, `:61`) **all
327 bodies exceed the budget**, and in **285 of 327** the cut lands inside a section rather than at a
heading boundary. (The working tree adds a depth-aware priority-ranked selector with the positional
cut as fallback; also uncommitted.)

The budget gate cannot catch any of this because it cannot fail: `python3
scripts/check-token-budget.py` reports `327 within declared budget, 0 OVER` by comparing
`metadata.json:compiled_tokens` against the `budget="N"` attribute the compiler itself wrote
(`scripts/_compile_skill.py:389,402`) — both derived from the same `token_budget` frontmatter value.
`tiktoken` is absent (`python3 -c "import tiktoken"` → `ModuleNotFoundError`), so `estimate_tokens`
falls back to `len(text.split())` (`scripts/_compile_skill.py:136-141`) — "tokens" are word counts.
The gate asserts a word count against a declared budget with median headroom **2,856 words** and no
skill closer than 63 words to its ceiling. `compile-skills.sh` documents exit code 3 as "Token budget
exceeded" (`scripts/compile-skills.sh:281`) but **no code path returns it** (`grep -rn 'exit(3)\|exit
3' scripts/_compile_skill.py scripts/compile-skills.sh` → nothing).

**Blast radius.** "Progressive disclosure" is a documented property with no enforcement and, by
default, the opposite behaviour.
**Fix.** Compare a real-token measurement against a *derived* budget (or the previous release's
compiled size) and ratchet it; wire the marker-based selector as the only path.

> **Remediation 2026-09-20 (partial).** The budget gate no longer reports a tautological pass.
> `scripts/check-token-budget.py` now (a) refuses to compare `compiled_tokens` (a word count without
> a real tokenizer) against a real-token `token_budget`, exiting **2 / UNMEASURED** when tiktoken is
> absent, and (b) cross-checks the compiled `budget="N"` against the source frontmatter, failing on
> any disagreement. Compile coverage still gates as before. The CI step passes
> `--allow-unmeasured` because tiktoken is not installed in CI, so the budget comparison is not yet a
> live gate — it is now honestly *not measured* rather than falsely green. The real-token measurement
> + derived-budget ratchet remains open.

### 6.5 The quality score cannot fail, and is not in CI

```
$ python3 scripts/audit-library.py --brief ; echo "exit=$?"
Library rating: 9.8/10 (327 skills)
exit=0
```

`main()` (`scripts/audit-library.py:325-337`) parses two flags, prints, returns `None` — no threshold
branch, no `sys.exit`. `grep -rn 'audit-library' .github/workflows/ scripts/run-ci-locally.sh
.githooks/` returns nothing. **Blast radius.** "9.8/10" reads as a measured, enforced bar; it is an
unversioned print statement. **Fix.** Give it a `--check` with the current score as a ratchet floor
and add it to the measurement job — or stop quoting the number.

> **Remediation 2026-09-20.** The tool now states in its header, its brief output and an explicit
> trailing line that it is a **report, not a gate** (exit 0 by default, not wired into CI), and it
> gained an opt-in `--min-score FLOOR` that exits 1 below the floor. It is deliberately *not* wired
> into CI: the score is a weighted composite of structural proxies (section presence, marker counts),
> not a correctness check, so inventing a floor the current corpus cannot meet would be a fabricated
> gate. The "9.8/10" figure is now labelled as a report wherever it appears.

### 6.6 The 22-section template is human-shaped

Mean full `SKILL.md` is **642 lines** (median 635, max 1,297); **299 of 327** exceed the 500-line
advisory the validator itself prints (`scripts/validate-skills.sh:173-177`, `MAX_LINES = 500`;
advisory only). Compilation drops `references` (327/327), `what_good_looks_like` (327/327), `practice`
(326/327) and `when_to_use` (322/327) from every skill. A fifth is dropped **without being reported**:
the compiler's `trim_map` lists `("## The Expert.s Mindset", "mindset")`
(`scripts/_compile_skill.py:566-571`) — a regex dot where an apostrophe belongs — while the corpus
writes `## The Expert's Mindset` (326 skills). Result: `mindset` appears in **0** of 327 compiled
`skill.xml` files and **0** of 327 `sections_trimmed` lists. Five sections — mindset, practice,
what-good-looks-like, when-to-use, references — are compiled out of the artefact the agent actually
loads, and `mindset` is dropped silently on a typo.
**Fix.** Correct the `trim_map` literal to `"## The Expert's Mindset"` (one character), and either
accept the four trims in the authoring docs or stop requiring sections that are always discarded.

---

## 7. What "solid foundations for robust agentic programs" would actually require

Three things are load-bearing and none is present:

1. **A runnable agent loop.** Today it is nine lines of prose (`ai-engineer/SKILL.md:254-262`) plus a
   *design* pattern elsewhere. A foundation ships a loop with tool registration, a termination
   predicate, a step budget and a structured trace — as code, executed in CI against a stub model, so
   its behaviour is regression-tested. Every other capability in §5 depends on this existing first.
2. **A contract gate that can be satisfied.** The gate exists and self-tests
   (`workflow-runner.py:849-895`), but no executor emits the field it reads, so with a real agent it
   always fails and with the stub it proves nothing. A foundation has the executor produce
   `criteria_met` from the transcript, and a CI job running a flagship manifest with
   `--enforce-contracts` expecting **zero** violations.
3. **Behavioural regression detection.** 38 scenarios, 0 recorded, 17 skills covered, golden cases for
   3 of 327. A foundation records real sessions, ratchets the count, and gates a merge on behaviour
   not regressing — the discipline the routing floor already applies to retrieval.

Beyond those: bundle the two root scripts and fix the flat-layout paths (§4), replace or delete the
312 stubs (§3.2), and implement or withdraw the progressive-disclosure claim (§6.4). None of that is
out of reach; all of it is visible in the numbers above.

The honest summary: **this is a well-organised professional-knowledge corpus with a good control-flow
engine attached to it.** As a *design* reference for agentic systems it is genuinely useful — coverage
of context, coordination, cost and guardrails is real and specific. As an *implementation* foundation
for running agentic systems unattended it is close to empty: no loop, no satisfiable contract check,
no behavioural evidence, and a headline quality number that cannot fail.

---

## 8. Honest limits of this assessment

- **The working tree is dirty and agents are editing concurrently.** Three findings describe a
  *remediated* state that is **uncommitted**: the `constraints` payload key (§4, now at
  `scripts/validate-workflows.py:38`), the behavioural-eval false-green fix (§6.2), and the
  depth-aware executor selector (§6.4, `AGENT_SKILL_DEPTH`). Each is cited at `HEAD` as the defect and
  in the tree as the fix. If those changes are not committed, the `HEAD` behaviour is live.
- **`tiktoken` is absent**, so every token figure in the repo — including
  `metadata.json:compiled_tokens` and the budget gate — is a word count understating real cost. The
  77.9% reduction is quoted from `docs/token-context-benchmark.md:43` as a prior measurement I could
  not recompute (it required a real BPE tokenizer); this document's own counts are word and file
  counts, labelled as such.
- **No live agent was run**, so every behavioural and routing claim is about *declared* behaviour or
  *recorded harness output*, not about what a model does with the skills.
- **Claims I could not verify, stated as such:** (a) the brief's **262/3303 (7.9%)** concrete-term
  figure — I measure **725/3303 (21.9%)** for the brief's own list and cannot reach 7.9% with any term
  set tried; (b) **~45 cited scripts do not exist** — I find **13 exist in no location**, 41 absent
  from repo-root `scripts/` (28 of which exist per-skill); (c) **98 skills hardcode repo-path
  cross-references** — I measure **210** skills with a domain-qualified path, 96 of them cross-skill,
  all breaking under flat; (d) **43 agent-related skills / "5 of 43"** — reproducible equivalents are
  **19 in `22-ai-engineering` (5 with tooling)** and **25 across `22-ai-engineering` + `00-framework`
  (5 with tooling)**; (e) **594 citations** — reproduced as occurrences, but the correct *skill* count
  is **198 of 327**.

---

## Appendix — reproduction commands

All run from the repo root. §3.3 and §3.4 used inline Python scripts over
`skills/**/references/*.md` (the term-list regex is printed in §3.3) and over SKILL.md bodies
matching `scripts/<name>.py|sh|js` respectively; the rest are the literal commands below.

```bash
# §3.1 — the root-script defect
grep -rl 'calculate-roi\.sh'          skills --include=SKILL.md | wc -l   # 196
grep -rl 'runtime-version-detect\.sh' skills --include=SKILL.md | wc -l   # 198
grep -rnE 'calculate-roi\.sh|runtime-version-detect\.sh' skills --include=SKILL.md | wc -l  # 394
grep -rn 'calculate-roi\.sh' skills --include=SKILL.md \
  | grep -c 'zeroes-ones\|repo root\|this library'                        # 0
grep -n 'calculate-roi\|runtime-version-detect' scripts/install.sh scripts/init-project.sh  # nothing

# §3.2 — boilerplate stubs
find skills -path '*/references/*' -type f | wc -l                        # 3303
find skills -path '*/references/research-sources.md' | wc -l              # 39 (-> 312 non-README siblings)

# §4 — flat-layout breakage
readlink skills-flat/code-reviewer                                        # ../skills/06-quality/code-reviewer

# §5/§6 — AGI readiness and the six foundations
find skills/22-ai-engineering -name SKILL.md -exec cat {} \; | wc -l      # 13271
find skills/22-ai-engineering -name SKILL.md -exec cat {} \; | grep -c '^```'                             # 334
find skills/22-ai-engineering -name SKILL.md -exec cat {} \; | grep -cE '^```(python|py|bash|sh|js|ts)$' # 6
grep -rlF '1s, 2s, 4s, 8s' skills --include=SKILL.md | wc -l              # 180
grep -rn 'criteria_met' scripts/executors/ | wc -l                        # 0
grep -rn 'enforce-contracts' .github/workflows/ | wc -l                   # 0
node scripts/run-behavioral-evals.js                                      # Skipped 38, exit 1
bash scripts/eval-skill.sh --all                                          # 3 skills green
python3 scripts/eval-routing.py                                           # rank-1 58.7%
node scripts/run-routing-evals.js                                         # 72.8% vs 80% target
python3 scripts/eval-routing.py --check ; echo $?                         # 0 (floor 55.0)
python3 scripts/check-token-budget.py                                     # 327/327 within budget
python3 scripts/audit-library.py --brief ; echo $?                        # 9.8/10, exit 0
grep -rln 'QUICK: 30s' scripts/                                           # 3 emitters, no reader
python3 scripts/workflow-runner.py --selftest                             # 41 checks, 0 failed
python3 scripts/validate-workflows.py --selftest                          # 34 checks, 0 failed
python3 scripts/validate-workflows.py --all                               # 21/21 OK, 0 FAIL
```
