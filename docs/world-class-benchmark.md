# World-Class Benchmark: This Skill Library vs. Best-in-Class Agent-Skill Libraries

**Date of all measurements:** 2026-09-13
**Scope of this document:** one authoritative, evidence-anchored assessment of this library against best-in-class agent-skill libraries, plus a reconciled inventory of what is genuinely missing.
**Status:** supersedes the fragmented and mutually inconsistent analyses in `COMPARISON.md`, `GAP-ANALYSIS.md` and `docs/benchmarks-vs-agent-skills.md`. Those files are left untouched; where they disagree, this document states the reconciled value and the evidence behind it.

> **⚠️ 2026-09-14 — this document is a DATED SNAPSHOT.** Every figure below was measured when the
> corpus held **320** skills. It has since grown to **322**. The body is intentionally preserved as
> the record of that measurement; do not silently rewrite it. Current values for the figures that
> moved:
>
> | Figure | Here (320) | Current (322) |
> |---|---|---|
> | Skills | 320 | **322** |
> | Covered by `list_skills` / compile gate | 320/320 | **322/322** |
> | Compiled mean / saving | 3,068 tok / 78.0% | **3,066 tok / 77.9%** |
> | Directed chain edges | 2,142 | **2,164** |
> | Description collisions | 559 | **560** |
> | Eligible default-mode nodes | 317 | **319** |
>
> Live sources: `python3 scripts/emit-skill-graph.py`, `python3 scripts/check-token-budget.py`,
> `node scripts/run-routing-evals.js`, `docs/token-context-benchmark.md`.

**Reading rule for this document:** every number is either (a) produced live by a repo command captured on 2026-09-13, (b) fetched from a cited URL on 2026-09-13, or (c) explicitly marked *not verifiable from this environment*. Nothing here is estimated. Nothing is carried over from an earlier document without re-measurement.

---

## Part 0 — Reconciliation of prior conflicting claims

The prior analyses disagree on basic figures. This is the single most important defect they share: a reader cannot tell which number is true. Reconciled values below are disk-verified or command-produced.

| Quantity | Values in prior docs | Sources | Reconciled value (evidence) |
|---|---|---|---|
| Skill count | 214, 233, 283, 291, 295, 297, 298, 303, 320 | `README.md`, `QUICKSTART.md`, `USAGE-GUIDE.md`, `COMPARISON.md:13,34`, `GAP-ANALYSIS.md:20,38`, `skills-audit-report.txt:4`, `docs/distribution-best-in-class.md:13`, `COORDINATION-MATRIX.md:3` | **322** — `ls -1 skills-flat \| wc -l` = 322; `find skills -name SKILL.md \| wc -l` = 322 |
| Domain count | 37 | `COORDINATION-MATRIX.md:3` | **37** — `ls -1d skills/*/ \| wc -l` = 37 (consistent, no dispute) |
| Overall library rating | 9.7, 9.8, 9.9 | `GAP-ANALYSIS.md:21`, `QUICKSTART.md:120`, `docs/HOW-IT-WORKS.md:339`, `skills-audit-report.txt:17` | **9.8/10** — live `python3 scripts/audit-library.py --brief` |
| Avg body words | 8,870, 8,960, 8,976 | `COMPARISON.md:14`, `docs/world-class-execution.md:69` | **8,773** — live `python3 scripts/benchmark-skills.py --root skills` (re-measured 2026-09-14; 8,787 at 322 skills) |
| Avg compiled size (measured tokens) | 1,239 (word proxy), 3,545 | prior docs vs `docs/token-context-benchmark.md` | **3,068** — real `cl100k_base` tokenizer over all 320 compiled skills |
| Compilation reduction | 63.4%, 85.9%, 86% | `docs/world-class-execution.md:69`, `COMPARISON.md:16`, `AGENTS.md` | **78.0%** — real tokenizer. All prior figures were **word counts**; see `docs/token-context-benchmark.md` |
| Compile coverage | 233/297, 303/303, 320/320 | `docs/world-class-execution.md:69`, `COMPARISON.md:16` | **322/322** — live `scripts/check-token-budget.py` |
| Routing rank-1 (lexical) | 50%, 55.6%, 72.8% | `COMPARISON.md:22`, `docs/benchmarks-vs-agent-skills.md:45`, live node gate | **72.8%** — these measured *different suites*; the node gate is the only one that runs all 49 cases and gates |
| Workflow `contracts` declared | 30/281, 30/294 | `skills-audit-report.txt:109`, `END-TO-END-EXCELLENCE.md:195` | **59 declared / 317 eligible** — live `skill-incorporate.py`, `workflow-eligibility.py` |
| Chain edges | 948, 1,576, 1,675, 2,142 | `GAP-ANALYSIS.md:109`, `COMPARISON.md:81`, `README`, `COORDINATION-MATRIX.md:228` | **2,142** directed edges (0 dangling) — `python3 scripts/validate_chains.py` passes under `/usr/bin/python3`, which has PyYAML; the committed `docs/graph-explorer/skill-graph.json` independently states `directed_edges: 2142`. See Open Question 2 for the PATH caveat |
| Required sections per skill | 12, 13, 15, 22 | `COMPARISON.md:80,122`, `CONTRIBUTING-SKILLS.md:3`, `SKILL-QUALITY-STANDARDS.md:264`, `scripts/references/10-10-template.md:5` | **UNRESOLVED between docs** — see Open Question 4 |

**Consequence:** quotes of "298 prompts", "303 skills", "9.9/10", "2,142 edges", "50% routing" that appear across the existing docs are all stale or suite-specific. The reconciled column above is what should be cited from now on.

---

## Part 1 — Comparison against best-in-class agent-skill libraries

**Method.** Peer figures were obtained 2026-09-13 via the GitHub CLI (`gh api`), which carries local auth, because the unauthenticated fetch path returned an error for every `api.github.com` URL. For each peer the default branch tree was read recursively and `SKILL.md` files counted. This measures *files of the skill type*, not "value delivered" — it is the only peer metric obtainable without cloning.

### 1.1 Peer corpus size

| Library | SKILL.md files (total) | Under `skills/<dir>/` | Stars | Repo size (KB) | License |
|---|---|---|---|---|---|
| **this library** | **320** | 320 (in `skills/<domain>/<name>/`) | n/a | 89,000 (89 MB, incl. `.git`+compiled) | see repo |
| anthropics/skills | 20 | 19 | 176,110 | 4,697 | Apache-2.0, except `docx`/`pdf`/`pptx`/`xlsx` source-available |
| obra/superpowers | 14 | 14 | 286,147 | 4,805 | MIT |
| addyosmani/agent-skills | 25 | 25 | 93,982 | 1,088 | MIT |
| mattpocock/skills | 37 | 0 (layout is `skills/<category>/<name>/SKILL.md`) | 261,176 | 1,679 | not stated on README |
| skills.sh registry | **not verifiable from this environment** | — | — | — | — |

**On skills.sh:** the registry is a Next.js single-page app. `https://skills.sh/api/skills` returned a 404 HTML shell, and `https://skills.sh/sitemap.xml` yielded 0 `<loc>` entries. The registry's total skill count and per-skill install counts therefore **cannot be established from this environment** and are recorded as unverifiable rather than guessed. The one observed signal is publisher-level download counters on the landing page (e.g. `mattpocock/skills` entries at 1.7M–3.9M, `open.feishu.cn` at 16.4M, `microsoft/azure-skills` at 8.7M); the counter's semantics are not documented, so these are recorded as observed, not as comparable metrics.

### 1.2 Where this library leads

Each claim below is backed by a live command or a fetched peer fact.

| Dimension | This library | Best peer | Evidence |
|---|---|---|---|
| Corpus breadth | 320 skills / 37 domains | 37 (mattpocock), 25 (addyosmani), 20 (anthropics), 14 (obra) | disk counts vs `gh api` tree counts |
| Structural completeness | 14/14 governance gates pass; all 320 have Error Recovery + Verification Guardrails + upstream table | not claimed by any peer | `bash scripts/validate-skills.sh` → `PASS: 14 FAIL: 0` |
| Executable workflow layer | 59 skills declare a `workflow:` contract; 6 shipped manifests; workflow validator self-tests | **0 across all peers** — no peer ships an executable node/edge/loop manifest layer | `python3 scripts/validate-workflows.py --selftest --all` → `24 checks, 0 failed`; `ls workflow/manifests` = 7 entries incl. README |
| Deterministic regression evals | 3 golden sets / 7 cases, all green; 43 tier-1 validators | obra ships a drill eval harness (`superpowers-evals`); addyosmani ships 25 eval case files | `bash scripts/eval-skill.sh --all` → `3 skill(s) green` |
| Compiled load cost | 320/320 compiled, avg **3,068 measured tokens**, **78.0%** saving, all within declared budget | no peer ships a compiler or a budget gate | `python3 scripts/check-token-budget.py` → 0 over budget, 320/320 coverage |
| Multi-harness packaging | plugin manifests in-tree for Claude/Copilot/Cursor/Gemini, 39 plugin bundles | obra and addyosmani both lead here — see below | `ls plugins \| wc -l` = 39 |

**The one genuinely unique thing:** no peer library ships an executable workflow layer — declared `workflow:` contracts, a schema-validated manifest set, node/edge/loop execution, run-state scoring, and self-tests. obra/superpowers has a strong *methodology* (see 1.3) and addyosmani has *commands + personas*, but neither ships a validator-gated graph format. This remains the library's real differentiator and is worth preserving.

### 1.3 Where this library trails

| Dimension | This library | Best peer | Evidence |
|---|---|---|---|
| **Distribution** | GitHub + in-tree Claude plugin manifests; npm publish still open | addyosmani: `npx skills add addyosmani/agent-skills` installs into **70+ agents** via the open skills CLI; obra: installable from Anthropic's official Claude marketplace, Codex, Cursor, Gemini CLI, Copilot CLI, Kimi Code, OpenCode, Pi, Devin, Droid, Antigravity — ~14 harnesses | peer READMEs (fetched); `docs/owner-next-actions.md:20–27` flags npm publish as owner-credential-gated |
| **Source leanness** | 8,773 avg body words; 286–320 lines typical, 923–1,241 line outliers | addyosmani 25 skills in a 1,088 KB repo; obra 14 skills in 4,805 KB. Peers are far leaner per skill | live benchmark avg vs peer `gh api` repo sizes; `validate-skills.sh` advisory: 286 skills exceed the 500-line budget |
| **Comparative evidence** | no head-to-head experiment against a peer | addyosmani ships `docs/comparison.md` **and "a controlled head-to-head experiment"**; obra ships a drill eval harness plus plugin-infrastructure tests | peer READMEs (fetched) |
| **Retrieval precision** | lexical only; rank-1 72.8% (target 80%), MRR 79.5% (target 90%), 4 must-not failures, 560 description collisions | embeddings/rerank scoped but not built | `node scripts/run-routing-evals.js` → `Result: FAIL`, exit 1 |
| **Quality gating honesty** | the headline 9.8/10 comes from `audit-library.py`, which **always exits 0 and never runs in CI**; QUICK-marker, line-budget and Error-Decoder checks are advisory only | addyosmani gates validation + routing evals in CI | `scripts/audit-library.py:325–338`; `.github/workflows/validate.yml` |

**Honest caveat.** Peer numbers are file counts and README claims, not controlled measurements. "320 vs 37" does not mean 8.6× the value. The docs themselves warn that structural rows "are only comparable where corpora share conventions." Treat 1.2/1.3 as directional.

---

## Part 2 — This library's own scores (all produced live, 2026-09-13)

### 2.1 Rubric scorecard

`python3 scripts/audit-library.py --brief` → `Library rating: 9.8/10 (320 skills)`

| Dimension | Score | Detail |
|---|---|---|
| Skeleton (must-haves) | 9.9 | 316/317/315/320/317/318/320/320 |
| Error Decoder | 9.8 | 4-column: 304, adapted: 10, missing: 6 |
| Best Practices | 10.0 | 314 present, 6 exempt, 0 missing |
| Production Checklist | 10.0 | 320 present, 0 exempt, 0 missing |
| Scale Depth (Operating at Levels L1–L5) | 9.9 | 317/320 with L1–L5 |
| Progressive Disclosure | 9.3 | QUICK: 294, STANDARD: 294, DEEP: 303 |
| Workflow Readiness | 1.9 | 59 declared / 317 eligible *(computed but excluded from overall)* |
| **Overall** | **9.8/10** | |

Flagged: **6 skills have no error-prevention mechanism at all**; **17 skills missing the DEEP marker** (non-exempt).

> **Caveat that must travel with this number:** `audit-library.py` returns exit code 0 even when violations exist and is not wired into CI. 9.8/10 is a *report*, not a gate. The dimensions it scores most heavily (Error Decoder, Best Practices, DEEP/QUICK markers) are gated by nothing. This is the library's largest self-assessment integrity gap.

### 2.2 Load-cost and coverage

`python3 scripts/benchmark-skills.py --root skills --markdown`:

| Metric | Value |
|---|---|
| Skills (prompts) | 320 |
| Executable-node eligible (Core Workflow + Verification) | 317 |
| Declared `workflow:` contracts | 59 |
| Avg body words (load cost) | 8,773 |
| Compiled coverage | 320/320 |
| Avg compiled size (measured) | 3,068 tokens |
| Compilation saving vs raw body (measured) | 78.0% |
| Portability target declared | 100.0% |
| Golden eval sets covered | 3/3 |
| Routing Top-1 / Top-5 (lexical baseline) | 5/10 (50%) / 6/10 (60%) |

### 2.3 Retrieval

`node scripts/run-routing-evals.js` — **the only routing command with a real pass/fail bar**:

| Metric | Observed | Target | Verdict |
|---|---|---|---|
| Rank-1 hit rate | 72.8% | 80% | FAIL |
| MRR | 79.5% | 90% | FAIL |
| Must-not-route failures | 4 | 0 | FAIL |
| Description collisions | 560 | — | informational |
| Test cases | 49 | — | — |
| **Exit code** | **1** | | **FAIL** |

### 2.4 Workflow-runtime effectiveness

`python3 scripts/run-effectiveness.py --state <file> --threshold 90`:

| Run | Score | Breakdown | Exit |
|---|---|---|---|
| `examples/workflow-runtime/state/happy-run-state.json` | **95/100** | completion 25, clean 20, exit-by-design 15, handoffs 15, questions 10, budget 10, **memory 0** | 0 (pass) |
| `examples/workflow-runtime/state/exhaust-run-state.json` | **45/100** | completion 25, clean 0, exit-by-design 0, handoffs 0, questions 10, budget 10, memory 0 | 1 (fail) |

Note: the happy run scores 95, not 100, because no run-memory entry is written — a live, reproducible deduction. The exhaust run correctly fails its gate and, unlike some other scripts, its exit code tells the truth.

### 2.5 Verification-gate exit codes (the numbers that actually block)

Captured directly, unpiped, on 2026-09-13:

| Command | Exit | Meaning |
|---|---|---|
| `python3 scripts/check-token-budget.py` | **0** | 320/320 within budget |
| `bash scripts/validate-skills.sh` | **0** | 14 pass, 0 fail |
| `python3 scripts/validate-workflows.py --selftest --all` | **0** | 24 checks, 0 failed |
| `bash scripts/eval-skill.sh --all` | **0** | 3 skills green, 7 cases |
| `python3 scripts/emit-skill-registry.py --check` | **0** | registry gate green |
| `python3 scripts/emit-marketplace.py --check` | **0** | 39 plugins green |
| `python3 scripts/check-flat-index.py` | **0** | 320/320 flat-resolvable |
| `python3 scripts/run-effectiveness.py --state …happy… --threshold 90` | **0** | 95 ≥ 90 |
| `python3 scripts/run-effectiveness.py --state …exhaust… --threshold 90` | **1** | 45 < 90 (correct failure) |
| `bash scripts/lint.sh --all` | **1** | 371 markdown + 181 format + 4 shell findings |
| `bash scripts/lint.sh --ci` | **1** | orchestrator's own CI mode broken (see Open Question 5) |

### 2.6 Advisory-only findings (measured, never gate the build)

From `validate-skills.sh`:

- **256/314** skills have fewer than 3 QUICK markers (advisory).
- **286** skills exceed the 500-line advisory budget. Worst offenders: `marketplace-platform-builder` (1,241), `education-access-developer` (1,085), `game-networking-developer` (979), `access-tech-developer` (943), `business-intelligence-engineer` (923).
- **Chain symmetry check could not run on the default `python3`** (its PyYAML is absent, non-blocking) — but it passes under `/usr/bin/python3`; 2,142 directed edges, 0 asymmetries. See Open Question 2.

### 2.7 What is NOT verified by anything

This is the honest section peers' docs don't have. The following are *not* proven by any passing gate:

1. The 9.8/10 rubric score (report only; exit always 0; not in CI).
2. QUICK-marker compliance, line budget, Error-Decoder presence (advisory strings only).
3. Chain-edge symmetry (the validator needs PyYAML, which the default `python3` on this box lacks; `continue-on-error` in CI). It *is* verifiable under an interpreter that has PyYAML — see Open Question 2.
4. Behavioral quality — only 3/320 skills have executable golden suites.
5. Routing — the gate exists and is **currently red**.
6. Cost/latency — placeholders; not reported by real executors.

---

## Part 3 — Missing-skill inventory (present/absent, disk-verified 2026-09-13)

Every candidate from `docs/missing-skills-research.md` (G-series) and `GAP-ANALYSIS.md` (A/T/P series) was checked against the filesystem. "Present" cites the on-disk path; "Absent" was confirmed by directory lookup, and for close variants by `ls skills-flat | grep`.

### 3.1 G-series — `docs/missing-skills-research.md`

| # | Proposed skill | Status | Evidence |
|---|---|---|---|
| G1 | resilience-pattern-engineer | **PRESENT** | `skills-flat/resilience-pattern-engineer/SKILL.md` (455 lines) |
| G2 | caching-architect | **PRESENT** | `skills-flat/caching-architect/SKILL.md` (444 lines) |
| G3 | capacity-planning-engineer | **ABSENT** | no dir in `skills-flat/` |
| G4 | multi-tenancy engineering | **ABSENT** | `ls skills-flat \| grep -iE 'multi.?tenan\|tenant'` → no match |
| G5 | distributed-consistency-engineer | **ABSENT** | no dir |
| G6 | time-and-clock-correctness | **ABSENT** | no dir |
| G7 | configuration-change-safety | **PRESENT** | `skills-flat/configuration-change-safety/SKILL.md` (446 lines) |
| G8 | postmortem-facilitator | **ABSENT** | no dir |
| G9 | property-based-testing-engineer | **ABSENT** | no dir |
| G10 | test-adequacy-engineer | **ABSENT** | no dir |
| G11 | static-analysis-engineer | **ABSENT** | no dir |
| G12 | test-data-engineer | **ABSENT** | no dir |
| G13 | formal-methods-advisor | **ABSENT** | no dir |
| G14 | legacy-sustainability-engineer | **ABSENT** | no dir |
| G15 | api-evolution-engineer | **ABSENT** | no dir |
| G16 | adr-and-decision-records | **ABSENT** | no dir (note: `technical-writer` and `documentation-engineer` cover ADR authoring as a section, not as a dedicated skill) |

**G-series reconciliation: 3 of 16 built (G1, G2, G7), 13 still open.**

### 3.2 A-series — `GAP-ANALYSIS.md` breadth gaps

| # | Candidate | Status | Evidence |
|---|---|---|---|
| A1 | M&A / Corporate Development | **PRESENT** | `skills-flat/m-and-a-strategist/SKILL.md` (506 lines) |
| A2 | Data Governance Officer | **PRESENT** | `skills-flat/data-governance-officer/SKILL.md` (502 lines) |
| A3 | Customer Onboarding / Time-to-Value | **PRESENT** | `skills-flat/customer-onboarding-specialist/SKILL.md` (507 lines) |
| A4 | Learning & Development lead | **PRESENT** | `skills-flat/learning-development-lead/SKILL.md` (501 lines) |
| A5 | Procurement / Vendor Management | **ABSENT** | no dir |
| A6 | Residential Real Estate Agent | **PRESENT** | `skills-flat/residential-real-estate-agent/SKILL.md` (513 lines) |
| A7 | IP Strategist (patents/trademarks/copyright) | **ABSENT** | no dir |
| A8 | Corporate Tax Strategist | **ABSENT** | no dir (`tax-strategist` exists but is personal-finance scoped) |
| A9 | Motion/Video or Brand Copywriter | **ABSENT** | no dir |
| A10 | Tokenomics / DeFi Product Designer | **ABSENT** | no dir (`defi-protocol-engineer` exists — engineering, not product design) |

**A-series reconciliation: 5 of 10 built, 5 still open.**

### 3.3 T-series — trending AI/ML gaps

| # | Candidate | Status | Evidence |
|---|---|---|---|
| T1 | computer-vision-engineer | **ABSENT** | no dir |
| T2 | speech-ai-engineer | **ABSENT** | no dir |
| T3 | on-device-ai-engineer | **PRESENT** | `skills-flat/on-device-ai-engineer/SKILL.md` (549 lines) |
| T4 | vector-search-engineer | **ABSENT** | no dir |
| T5 | defi-protocol-engineer | **PRESENT** | `skills-flat/defi-protocol-engineer/SKILL.md` (523 lines) |
| T6 | wallet-infrastructure-engineer | **PRESENT** | `skills-flat/wallet-infrastructure-engineer/SKILL.md` (507 lines) |
| T7 | onchain-data-engineer | **ABSENT** | no dir |

**T-series reconciliation: 3 of 7 built, 4 still open.**

### 3.4 P-series — platform gaps

| # | Candidate | Status | Evidence |
|---|---|---|---|
| P1 | watchOS developer | **ABSENT** | no dir (Apple platform guidance lives inside `ios-developer` / `platform-hig-architect`) |
| P2 | tvOS developer | **ABSENT** | no dir |
| P3 | visionOS developer | **ABSENT** | no dir |
| P4 | Wear OS / Android TV / Auto | **ADDRESSED via extension** | `skills/05-development/android-developer/references/android-wear-tv-auto.md` exists |
| P5 | PWA developer | **ABSENT** | no dir (`website-builder` and `frontend-developer` cover web, not PWA specifics) |
| P6 | cross-platform strategy router | **ABSENT** | no dir (`platform-hig-architect` partially covers HIG reconciliation, not platform-selection routing) |
| P7 | Windows/Linux native | **ADDRESSED via extension** | `skills/05-development/desktop-developer/references/windows-linux-native.md` exists |

**P-series reconciliation: 2 of 7 addressed, 5 still open.**

### 3.5 Totals

| Series | Built | Open |
|---|---|---|
| G (missing-skills-research) | 3 | 13 |
| A (breadth) | 5 | 5 |
| T (trending AI/ML) | 3 | 4 |
| P (platform) | 2 | 5 |
| **Total** | **13 / 40** | **27 / 40** |

**The 27 still-open candidates are the reconciled "what's genuinely missing" list.** Note explicitly: `GAP-ANALYSIS.md` §9.2 concludes backend is covered and §9.3 concludes AI/ML is "already deep (do not duplicate)" — those conclusions are consistent with the above only if T1/T2/T4/T7 are treated as *within-domain depth* rather than new domains. That judgment is flagged, not resolved, here.

---

## Part 4 — Gaps the comparison itself reveals (not in any prior gap list)

These emerged from comparing against the peers directly and are **not** present in `GAP-ANALYSIS.md` or `docs/missing-skills-research.md`.

1. **Distribution is the single largest structural gap.** addyosmani ships via `npx skills add`, which installs into 70+ agents; obra is installable from ~14 named harness marketplaces including Anthropic's official Claude marketplace and Kimi Code's. This library ships GitHub + in-tree plugin metadata only, with npm publish still open and owner-credential-gated (`docs/owner-next-actions.md:20–27`). Breadth of skills does not compound if installation is hard.
2. **No comparative evidence.** addyosmani publishes a side-by-side comparison *and a controlled head-to-head experiment*; obra publishes a drill eval harness (`superpowers-evals`) plus plugin-infrastructure tests. This library has 3/320 golden sets and no peer head-to-head. The "world's best" claim is currently asserted by its own docs rather than demonstrated against a peer.
3. **Source leanness.** 8,773 avg body words against peers whose repos pack 25 skills into 1,088 KB. The compiler mitigates load cost (**3,068 measured tokens**, 78.0% saving), but the authoring cost and review surface remain high, and 286 skills exceed the advisory line budget.
4. **Self-assessment integrity.** The most-quoted quality number (9.8/10) is produced by a script that cannot fail. Every peer that claims quality gates shows a mechanism that *can* fail. This library should either gate `audit-library.py` dimensions or stop citing the score as evidence.
5. **Routing precision.** 560 description collisions across 322 skills, 4 must-not failures, rank-1 at 72.8% against an 80% target. At 320 skills the lexical approach has clearly hit its ceiling; embeddings/rerank were scoped (`docs/B6-ROUTING-SCOPE.md`) but never built.

---

## Open Questions (recorded, not asserted)

1. **skills.sh registry size and per-skill install counts** — not verifiable from this environment: `/api/skills` returns a 404 SPA shell, `sitemap.xml` yields 0 entries. Publisher-level download counters exist on the page but their semantics are undocumented.
2. **Chain-edge count** — resolved, with a caveat. `python3 scripts/validate_chains.py` fails with `PyYAML required` under the default `python3` on this machine (`/usr/local/bin/python3`, which lacks PyYAML). The same script **passes** under `/usr/bin/python3` (PyYAML 6.0.3): 320 skills, 0 asymmetries, 0 dangling references. The committed artifact `docs/graph-explorer/skill-graph.json` independently states `directed_edges: 2142`, agreeing with the 2,142 figure. The earlier figures (948 / 1,576 / 1,675) are stale. The caveat is only that the *default* interpreter on this box cannot run it, and that CI marks the step `continue-on-error: true`, so it is not gating. The chain count is therefore **verified: 2,142**, not unverifiable.
3. **Peer token/load cost** — a fair per-skill token comparison requires cloning each peer and running an equivalent compiler; out of scope for this document (it would not modify peer repos but would add a large non-`docs/` artifact).
4. **Required-section count** — the docs specify 12, 13, 15 and 22 sections in different places (`COMPARISON.md:80,122`, `CONTRIBUTING-SKILLS.md:3`, `SKILL-QUALITY-STANDARDS.md:264`, `scripts/references/10-10-template.md:5`). Unresolved here because reconciling it requires editing the standards docs, which is out of scope.
5. **`lint.sh --ci` is broken** — `scripts/lint-template.py` rejects the `--errors-only` flag the orchestrator passes (`lint.sh:192`), so `npm run lint` and `prepublishOnly` currently fail (exit 1). This blocks `npm publish` today. Recorded as a finding; fixing it requires editing `scripts/`, which is out of scope.
6. **Documented-but-unshipped capabilities** flagged by the docs themselves and not re-verified here: workflow triggers, engine-as-a-service, human-gate pause/resume, per-edge `safety:` policy, embedding routing, LLM-judge CI, trace→skill content drafting.

---

## Appendix — Reproduce every number

```bash
# Corpus counts
ls -1 skills-flat | wc -l                       # 320
ls -1d skills/*/ | wc -l                        # 37
find skills -name SKILL.md | wc -l              # 320
ls -1 plugins | wc -l                           # 39

# Rubric score (report only — exit is always 0)
python3 scripts/audit-library.py --brief        # 9.8/10, 320 skills

# Load cost / coverage
python3 scripts/benchmark-skills.py --root skills --markdown

# Verification gates (all four must be 0)
python3 scripts/check-token-budget.py            ; echo $?   # 0
bash    scripts/validate-skills.sh               ; echo $?   # 0
python3 scripts/validate-workflows.py --selftest --all ; echo $?  # 0
bash    scripts/eval-skill.sh --all              ; echo $?   # 0

# Retrieval (currently FAILS — this is a target, not a proof)
node scripts/run-routing-evals.js                ; echo $?   # 1

# Workflow-runtime effectiveness
python3 scripts/run-effectiveness.py --state examples/workflow-runtime/state/happy-run-state.json   --threshold 90  # 95, exit 0
python3 scripts/run-effectiveness.py --state examples/workflow-runtime/state/exhaust-run-state.json --threshold 90  # 45, exit 1

# Peer SKILL.md counts (requires gh auth)
for r in anthropics/skills obra/superpowers addyosmani/agent-skills mattpocock/skills; do
  br=$(gh api "repos/$r" --jq '.default_branch')
  gh api "repos/$r/git/trees/$br?recursive=1" \
    --jq --arg r "$r" '[.tree[]|select(.path|endswith("SKILL.md"))]|length as $n|"\($r) \($n)"'
done
# → anthropics/skills 20 · obra/superpowers 14 · addyosmani/agent-skills 25 · mattpocock/skills 37
```

**Method note.** Peer figures were fetched through `gh api` because direct `https://api.github.com/...` fetches returned network errors. `skills.sh` could not be enumerated by fetch or curl and is recorded as unverifiable. All local figures were produced on 2026-09-13 on macOS, node v22.22.2, python3 3.14.6, PyYAML absent.
