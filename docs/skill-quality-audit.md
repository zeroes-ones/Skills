# Skill Quality Audit — Per-Skill, Measured

**Measured:** 2026-09-14 · **Method:** per-skill structural analysis of all 320 `SKILL.md` files against the repo's own two section standards, plus a peer-convergence gap scan against four cloned best-in-class libraries.

## 1. Headline

The library reports **9.8/10** and a green governance gate. Both are true **and** both are misleading:

| Claim | Source | Measured reality |
|---|---|---|
| 9.8/10, "0 flagged skills" | `scripts/audit-library.py` | Library-aggregate only; **no per-skill score exists**; exit always 0; not in CI |
| `PASS: 14  FAIL: 0` | `bash scripts/validate-skills.sh` | True — but the gate checks **12** sections, not the 22 the template defines |
| Template compliance | `scripts/lib/lint-template.py` (22 sections) | **149/320 pass; 171 have ≥1 gap** |

**The decisive finding:** the repo defines a 22-section quality bar but the blocking gate enforces only 12 of them, and the stricter check (G6, pre-commit) runs with `--delta` so pre-existing violations are grandfathered. That is precisely how 171 non-compliant skills coexist with a green build.

## 2. Structural quality, per skill

Measured against the full 22-section template in `scripts/lib/lint-template.py`, with prefix/alias matching to avoid false positives (e.g. `## Ground Rules — Read Before Anything Else` counts as `Ground Rules`).

| Tier | Count | Meaning |
|---|---|---|
| **Fully compliant** | **149/320 (47%)** | all 22 sections present |
| Has ≥1 gap | 171/320 (53%) | missing at least one required section |
| Pass the 12-section blocking gate | 311/320 | why CI is green |
| Pass neither standard | 9/320 | worst offenders |

### Most commonly missing sections

| Missing section | Skills | Notes |
|---|---|---|
| `When NOT to Use` | **165/320 (52%)** | the validator's frontmatter wants `Do NOT use…` in the description; most skills carry it *there* but not as a body section |
| `Anti-Rationalization` | **165/320 (52%)** | the excuse-and-rebuttal table — one of the library's most distinctive features |
| `Error Decoder` | 37/320 | |
| `Anti-Patterns` | 25/320 | |
| `The Expert's Mindset` | 6/320 | |
| `When to Use` | 4/320 | |
| `Best Practices` | 4/320 | |
| `State Log` | 3/320 | |
| `Operating at Different Levels` | 2/320 | |
| `Core Workflow` | 1/320 | |

### Worst individual skills

| Skill | Missing |
|---|---|
| `cross-skill-communication` | 7 — Expert's Mindset, Operating at Levels, When to Use, When NOT to Use, Error Decoder, Anti-Patterns, State Log |
| `apple-hig-expert` | 4 — When NOT to Use, Error Decoder, Anti-Patterns, Anti-Rationalization |
| `fintech-ui-designer`, `game-ui-designer`, `healthcare-ui-designer`, `material-design-expert`, `desktop-architecture-patterns`, `feature-flag-architect`, `secure-api-design`, `automation-engineer`, `content-strategist`, `financial-security`, `personal-finance`, `customer-success-manager` | 4 each — same set |

Verified by hand: `apple-hig-expert` has **zero** occurrences of "rationaliz" in the file and no `When NOT to Use` / `Anti-Patterns` heading. The negative routing exists only as a frontmatter `Do NOT use…` clause, which the description validator accepts.

### The pattern

**162 of the 165 skills missing `Anti-Rationalization` were last updated 2026-07-23 to 2026-07-26** — the corpus's founding batch. Skills added later (the `-engineer` wave, `verification-independence-engineer`, `caching-architect`) carry the full template. So this is not decay; it is **a large founding cohort that predates the 22-section standard and was never retrofitted**, plus a gate that was deliberately loosened (`--delta`) so retrofitting would not be forced.

## 3. Why the gates cannot see it

Three independent mechanisms hide the same gap:

1. **`validate-skills.sh` checks 12 sections, not 22.** Its `REQUIRED` set omits `Anti-Patterns`, `Anti-Rationalization`, `Best Practices`, `Error Decoder`, `Error Recovery`, `Gotchas`, `Production Checklist`, `State Log`, `Verification`, `When NOT to Use` — 11 of the 22. A skill can be maximally compliant with the gate and miss half the template.
2. **`lint-template.py` runs `--delta` in pre-commit.** A violation present at `HEAD` is reported as pre-existing and does not block. All 171 gaps are grandfathered by construction.
3. **`audit-library.py` scores the library, never a skill, and always exits 0.** Its `Progressive Disclosure: 9.3` and `Error Decoder: 9.8` dimensions also disagree with a direct count (37 skills lack an Error Decoder section). It is not in CI.

Net: **there is no command anywhere in this repo that will tell you a named skill is not up to standard.**

## 4. Top skills missing — peer convergence scan

Method: cloned all four peer libraries and mapped every peer `SKILL.md` to this corpus as MATCHED / PARTIAL / MISSING. All four clones succeeded.

| Peer | Skills | Matched | Partial | Missing |
|---|---|---|---|---|
| anthropics/skills | 20 | 4 | 4 | 11 |
| obra/superpowers | 14 | 10 | 3 | 1 |
| addyosmani/agent-skills | 25 | 23 | 1 | 1 |
| mattpocock/skills | 37 | 19 | 7 | 11 |

**Software-process coverage is strong (~85–92% match).** No capability exists in all four peers that this library lacks.

### Ranked missing / partial capabilities

| # | Capability | Peers | Status | Nearest thing here |
|---|---|---|---|---|
| 1 | **Plan → task/ticket breakdown** (`writing-plans`, `planning-and-task-breakdown`, `to-tickets`) | **3 of 4** | PARTIAL | `idea-to-spec` (spec not plan), `wayfinder` (investigation only) |
| 2 | **Receiving/responding to code review** (`receiving-code-review`) | obra | **MISSING** | we own the reviewer half only |
| 3 | **Constraint-driven development** — write the quality bar, then catch agents *weakening* it (`@ts-ignore`, skipped tests, stripped assertions) | addyosmani | **MISSING** | nothing; `roi-gate` and `verification-independence-engineer` are different purposes |
| 4 | **Document-artifact family** (`docx`, `xlsx`, `pptx`, `pdf`) | anthropics (4 skills) | **MISSING** | **no analogue anywhere in 320 skills** — no `python-docx`, `openpyxl`, or `pptx` reference exists |
| 5 | **Issue/PR triage state machine** (`triage`) | mattpocock | **MISSING** | nothing handles inbound work |
| 6 | **Human-only setup wizard** (`wizard`) — interactive bash for credentials, CI secrets, dashboards, cutovers | mattpocock | **MISSING** | genuinely novel |
| 7 | **MCP server authoring** (`mcp-builder`) | anthropics | PARTIAL | `mcp-management` covers config/security, not build-out |
| 8 | **Multi-component web artifact builder** (`web-artifacts-builder`) | anthropics | PARTIAL | `frontend-developer` builds sites, not portable artifacts |
| 9 | **Internal comms formats** (`internal-comms`) | anthropics | PARTIAL | `email-composer` covers one format |
| 10 | **Doc co-authoring loop** (`doc-coauthoring`) | anthropics | PARTIAL | `technical-writer` writes, does not co-author |

**Highest-priority single gap:** #1, plan→ticket decomposition — the only capability where three independent top libraries converge and this one has only a partial answer. **Largest absolute gap:** #4, the document-artifact family — four entire skills with no analogue in the corpus.

Also worth noting from the corpus: `verification-independence-engineer` — the library's best answer to the "validator must be independent" thesis — is currently **untracked in git**, i.e. uncommitted work.

## 5. What to do

Ordered by leverage:

1. **Reconcile the two section standards.** Either raise `validate-skills.sh` to the full 22, or cut the template to what is actually enforced. Right now the repo documents a bar it does not check, and the gap is 171 skills wide.
2. **Retire `--delta` for template compliance**, or add a tracked grandfather list, so the 171 outstanding gaps are visible as a countable backlog rather than silently exempted.
3. **Add a per-skill scorecard.** `audit-library.py` cannot name a weak skill; a per-skill line (`name → sections present / missing`) would make the backlog actionable and give the 9.8/10 a verifiable basis.
4. **Retrofit `Anti-Rationalization` and `When NOT to Use`** to the 165 skills missing each — the two highest-frequency gaps, both from the July founding cohort.
5. **Build the plan→ticket decomposition skill** (#1 gap) and consider the document-artifact family (#4) as a new domain.

## 6. Update — 2026-09-14: top-2 missing capabilities built

The two highest-ranked gaps from §4 are now implemented, at full 22-section template compliance:

| Capability | Skill | Domain | Evidence |
|---|---|---|---|
| **#1 gap** — plan → task/ticket decomposition | `implementation-planner` | `12-operations` | `skills/12-operations/implementation-planner/SKILL.md` (457 lines), zero lint errors |
| **#4 gap** — document-artifact family | `document-specialist` | `24-creative` | `skills/24-creative/document-specialist/SKILL.md` (457 lines), zero lint errors |

Both carry: 6 hard Ground Rules with Mechanical Trigger + Violation Response columns, 4 decision trees, 22 sections with depth markers, dollar-quantified gotchas, 15-item production checklists, 10+ "Complete when" criteria, and `scripts/verify-skill.sh`.

Supporting artifacts: 6 reference files (task-plan schema, worked cross-service decomposition with DAG and critical path, slicing patterns; format-library selection, templating + fidelity checklist, reopen-and-assert recipes for all four formats).

**Corpus:** 320 → **322** skills. Chain graph: 2,142 → **2,164** directed edges, 0 dangling refs.

**All nine governance gates pass** after rebuild: `check-token-budget`, `validate-skills` (14/0), `validate-workflows --selftest --all`, `eval-skill --all`, `validate-chains`, `check-flat-index`, `emit-marketplace --check`, `emit-skill-graph --check`, `emit-skill-registry --check`.

**Template compliance: 149/320 → 151/322.** The new skills are compliant; the 171 pre-existing gaps from §2 are unchanged and remain the backlog.

### What remains open

1. §1's core defect is untouched: the **12-vs-22 section standard mismatch** and the `--delta` grandfathering still hide the 171 gaps. New skills cannot regress (G6 blocks new violations), but the founding cohort is still unretrofitted.
2. **`document-specialist` does not cover a live engine** — it teaches the discipline of producing and verifying document files; it does not bundle executable document-manipulation code beyond the reference recipes.
3. Still missing from §4: receiving code review (#2), constraint-driven development (#3), issue/PR triage (#5), human-only setup wizard (#6).

## 7. Re-audit — 2026-09-14 (322 skills)

Re-measured after the two new skills landed. The structural picture is unchanged, but two real
defects were found that the governance gates do **not** catch.

### 7.1 Structural quality (unchanged)

| Metric | 2026-09-13 (320) | 2026-09-14 (322) |
|---|---|---|
| Fully template-compliant | 149 | **151** (47%) |
| Has ≥1 missing section | 171 | **171** (53%) |
| Library audit rating | 9.8/10 | **9.8/10** |
| `When NOT to Use` missing | 165 | **165** |
| `Anti-Rationalization` missing | 165 | **165** |
| `Error Decoder` missing | 37 | **37** |
| `Anti-Patterns` missing | 25 | **25** |

**Gap distribution:** 151 skills clean · 2 with 1 gap · **119 with 2 gaps** · 31 with 3 · 18 with 4 · 1 with 7.

The dominant population is the **119 skills missing exactly 2 sections** — and in almost every case
those two are the same pair: `When NOT to Use` + `Anti-Rationalization`. That is a single, mechanical
retrofit, not 119 separate problems. Worst single skill: `cross-skill-communication` (7 gaps).

Notably, the largest skills are among the worst: `education-access-developer` (21,478 words),
`environmental-tech-developer` (17,438), `marketplace-platform-builder` (17,392) all lack
`Anti-Rationalization` — the section that stops an agent rationalizing its way past the rules.

### 7.2 Defect found: dangling skill references (gates do not catch this)

Cross-reference validation covers `chain:` edges only. Skill names cited in prose, in `Do NOT use`
routing clauses, and in routing tables are **never checked** — so a reference to a non-existent skill
sails through every gate. Three were found:

| Broken reference | Files affected | Root cause | Fix |
|---|---|---|---|
| `cryptography-engineer` | `cryptography` (**self-reference**), `financial-security`, `privacy-engineering` | The skill is named `cryptography`; the longer name was used everywhere it was cited, including its own `When to Use` | Renamed to `cryptography` (4 occurrences) |
| `capacity-planning-engineer` | `resilience-pattern-engineer`, `caching-architect` (7 occurrences) | A skill planned in `docs/missing-skills-research.md` (G3) that **was never built**, yet is cited as a live routing target | Routed to the real owners: `performance-engineer`, `site-reliability-engineer` |
| `doc-coauthoring` | `document-specialist` | **Introduced by the `document-specialist` rewrite** — it borrowed the peer skill name as a `Do NOT use` target | Routed to `technical-writer` / `content-strategist` |

The `cryptography` case is the most instructive: a skill referenced **itself** under a name that did
not exist, and passed 14 governance gates plus `validate_chains.py` without complaint.

**Zero dangling skill references remain** after the fix.

### 7.3 Remaining gaps vs peers (re-scanned against fresh clones)

All four peers re-cloned and every peer skill re-mapped against the 322. Corpus now covers 64 of 95
peer skills as MATCHED, 11 PARTIAL, 16 MISSING (4 of those genuinely not worth adding).

**No capability exists in all four peers that this library lacks.** The intersection is essentially
empty — the strongest genuinely-missing signal is 2-of-4.

| # | Gap | Peers | Why it ranks |
|---|---|---|---|
| 1 | **Receiving/responding to code review** | obra `receiving-code-review` | We own only the *issuing* side; an agent's loop is "get review → evaluate → push back or fix" |
| 2 | **Issue/PR triage → agent-ready briefs** | mattpocock `triage` | No coverage at all; core to maintaining a real repo |
| 3 | **Quality-bar contract + degradation detection** | addyosmani `constraint-driven-development` | Catches an agent silently lowering the bar (new suppressions, skipped tests) to reach green |
| 4 | **Research → written findings from primary sources** | mattpocock `research` | Delegated-research capability absent; `source-driven-development` is code-specific |
| 5 | **Branch finishing / integration decision** | obra `finishing-a-development-branch` | tests-green → merge/rebase/PR → worktree cleanup |
| 6 | **Interactive wizard for human-only steps** | mattpocock `wizard` | Provisioning, secrets, cutover — steps an agent cannot do alone |
| 7 | **Git worktree isolation** | obra `using-git-worktrees` | Referenced in two skills but not owned by one |
| 8 | **Subagent-per-task execution discipline** | obra `subagent-driven-development` | `multi-agent-orchestration` covers topology, not the concrete loop |
| 9 | **Session retro → agent-environment improvement** | mattpocock `retro` | Distinct agent-ops loop (token economy, steering instructions) |
| 10 | **Internal comms format library** | anthropics `internal-comms` | 3P updates, newsletters, leadership updates |

Explicitly **not worth adding**: `academy-guide`, `slack-gif-creator`, `claude-api` (vendor
references), `web-artifacts-builder` (host-specific), `migrate-to-shoehorn` / `setup-ts-deep-modules`
(one tool each), `wait-what` (better folded into `grilling`).

### 7.4 What still cannot be seen

The same three blind spots from §3, re-confirmed:
1. `validate-skills.sh` checks **12** sections, not the 22 the template defines.
2. Pre-commit G6 runs `lint-template.py` with **`--delta`** — all 171 gaps are grandfathered.
3. `audit-library.py` scores the library, never a skill, and always exits 0.

**Newly confirmed blind spot:** cross-reference validation does not cover prose skill names, which is
how three broken references survived. See §7.2.

## Reproduce

```bash
# full-template compliance, per skill
python3 scripts/lib/lint-template.py --all

# the blocking gate (checks only 12 sections)
bash scripts/validate-skills.sh

# alias-aware independent count (the numbers in §2)
python3 - <<'PY'
import pathlib, re
REQ=['Route the Request','Ground Rules',"The Expert's Mindset",'Operating at Different Levels',
'When to Use','When NOT to Use','Decision Trees','Core Workflow','Best Practices','Error Decoder',
'Cross-Skill Coordination','Proactive Triggers','What Good Looks Like','Deliberate Practice',
'References','Gotchas','Anti-Patterns','Verification','Error Recovery','State Log',
'Production Checklist','Anti-Rationalization']
n=0
for p in pathlib.Path('skills').glob('*/*/SKILL.md'):
    hs=[re.sub(r'^<!--\s*(?:QUICK|STANDARD|DEEP)[^>]*-->\s*','',
        re.sub(r'\s*\*\*\((?:QUICK|STANDARD|DEEP)(?::[^)]*)?\)\*\*','',m.group(1))).strip()
        for m in re.finditer(r'^##\s+(.+?)\s*$', p.read_text(errors='replace'), re.M)]
    miss=[r for r in REQ if not any(h==r or h.startswith(r+' ') or h.startswith(r+' —') for h in hs)]
    if miss: n+=1
print(f"skills with >=1 missing required section: {n}/320")
PY
```
