# Token & Context Benchmark

**Measured:** 2026-09-13 · **Re-measured:** 2026-09-14 after the corpus grew to 322 skills ·
**Method:** real BPE tokenizer (`tiktoken`, `cl100k_base`) over the actual corpus, vs. the repo's
own reported figures.

> Figures below are the 2026-09-14 re-measurement over **322** skills; the earlier 320-skill run is
> preserved in `docs/world-class-benchmark.md` as a dated snapshot.

## Headline correction — read this first

**The repository's `token_budget`, `original_tokens`, `compiled_tokens` and "86% reduction" numbers
are WORD COUNTS, not tokens.**

`scripts/_compile_skill.py:136` defines:

```python
def estimate_tokens(text):
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except ImportError:
        return len(text.split())          # <-- word count fallback
```

`tiktoken` is not installed, so every number the toolchain reports is `len(text.split())`. Verified
exactly on `code-reviewer`:

| Quantity | Repo reports | Ground truth (`cl100k`) | Factor |
|---|---|---|---|
| raw | 10,742 "tokens" | **16,269 tokens** | **1.51× understated** |
| compiled | 2,164 "tokens" | **4,908 tokens** | **2.27× understated** |

The understatement factor differs between raw and compiled because the compiler strips prose
(low tokens/word) but keeps structured XML tags and identifiers (high tokens/word). So **the reported
reduction % is also wrong.** Every token figure in the repo needs re-deriving.

## A. True compilation reduction (all 322 skills, real tokens)

| Metric | Repo reports (words) | **Measured (tokens)** |
|---|---|---|
| Overall reduction | 86.3% | **77.9%** |
| Mean per-skill reduction | 86.3% | **78.2%** |
| Median | 86.8% | **78.7%** |
| Range | 68.1 – 97.6% | **54.8 – 95.1%** |
| Total raw | — | **4,474,122 tokens** |
| Total compiled | — | **987,216 tokens** |
| Mean raw / skill | — | **13,895 tokens** |
| Mean compiled / skill | — | **3,066 tokens** |

The compiler is **effective but oversold by ~8 points**. Distribution of true reduction: 84 skills
≥90%, 191 at 80–90%, 40 at 70–80%, 5 below 70%.

Best/worst by true reduction: `options-quant-engineer` 95.1%, `writing-great-skills` 95.0% …
`llm-search-optimizer` 54.8%, `polyrepo-strategy` 56.7%.

## B. Ambient context — the biggest cost, and it isn't the skills

What an agent holds *before any skill is loaded* is the name+description listing for every installed
skill:

| Component | Tokens |
|---|---|
| 320 skill names | 1,312 |
| 320 skill descriptions | **41,849** |
| **Ambient listing total** | **43,161** |
| Always-on hook (`hooks/always-on-principles.md`) | 321 |

**43.2k tokens of ambient listing at full install.** Mean description is 131 tokens; the largest is
269. This is the dominant context cost — not the skill bodies, which only load on demand.

Proxy accuracy, for calibration:

| Estimator | Says | Error |
|---|---|---|
| `chars / 4` heuristic | 55,725 | **1.29× over** |
| word count (repo's method) | 26,774 | **0.62× under** |
| `cl100k` (truth) | 43,161 | — |

Neither shortcut is safe here. `chars/4` over-counts; word count under-counts by ~38%.

## C. Load cost per skill body

| Metric | Tokens |
|---|---|
| Total raw bodies (320) | 4,338,458 |
| Mean | 13,558 |
| Median | 13,892 |
| Min / Max | 4,336 / 32,486 |
| 90th percentile | 17,723 |

## D. Install tiers — the main context-management lever

| Tier | Skills | Ambient listing | All bodies loaded | **Compiled** | Reduction |
|---|---|---|---|---|---|
| `--solo` | 8 | 707 | 130,954 | **40,568** | 69.0% |
| `--grow` | 18 | 1,555 | 296,832 | **89,584** | 69.8% |
| full | 320 | 43,161 | 4,459,085 | **982,077** | 78.0% |

**Insight that cuts against the design:** solo/grow reduce *less* (69–70%) than the full corpus
(78%), and the solo skills are the *heaviest* — mean compiled 5,071 tokens vs 3,068 corpus-wide.
The 8 flagship skills (`ceo-strategist`, `code-reviewer`, `fullstack-developer`, …) are the most
expensive to load. The tier is cheap because it lists 8 skills (707 ambient tokens), not because
each skill is cheap.

## E. Minimum viable context for one routed task

| Setup | Before the model answers |
|---|---|
| Full install | 43,161 + 321 + 3,068 = **46,550 tokens** |
| Solo tier | 707 + 321 + 5,071 = **6,099 tokens** |

**Tiering is worth ~7.6× on context cost** — by far the single biggest saving available, larger than
compilation (which acts only on the one skill actually loaded).

## F. MCP surface

`scripts/mcp-skill-server.py` exposes 8 tools (`list_skills`, `get_skill`, `get_skill_contract`,
`search_skills`, `get_skill_graph`, `list_workflows`, `validate_manifest`, `run_workflow`) with
~384 tokens of descriptions. Its context value is **structural, not size**: it makes retrieval
*pull-based*, so the 43k ambient listing is never injected at all — the agent asks for what it needs.

## G. Context-management mechanisms, assessed

| Mechanism | Implemented? | Measured effect |
|---|---|---|
| Two-tier compile (SKILL.md → minified XML) | Yes | **78.0% true reduction**, 320/320 coverage |
| Tiered install (solo/grow/full) | Yes | **7.6× context saving** — best lever |
| MCP pull-based retrieval | Yes | avoids the full 43k ambient listing |
| Session-start hook | Yes | 321 tokens, always-on |
| Flat discovery layer | Yes | 320 symlinks, 0 collisions (enabler, not a saving) |
| Progressive disclosure (QUICK/STANDARD/DEEP) | Marker present | **256/314 skills have <3 QUICK markers** — advisory, never gates |
| Routing to the right skill | Yes, lexical | **72.8% rank-1 vs 80% target — FAILING** (4 must-not, 560 collisions) |

## H. Quality, measured

| Metric | Value | Gated? |
|---|---|---|
| `audit-library.py` | 9.8/10 (320 skills) | **No — exits 0 always, not in CI** |
| `validate-skills.sh` | PASS 14 / FAIL 0 | Yes (blocking) |
| `check-token-budget.py` | 320/320 within budget | Yes (blocking) |
| Golden evals | 3/320 skills, 7 cases, green | Yes |
| Workflow manifests | 6, selftest 24/24 | Yes |
| Skills >500-line advisory budget | **286** | No (advisory) |

## I. The honest bottom line

**What genuinely works**

1. Compilation is real and substantial — **78% fewer tokens** on load.
2. Tiered install is the strongest context lever — **~7.6×**.
3. The MCP server makes retrieval pull-based, sidestepping the ambient-listing problem entirely.
4. Zero-dependency tooling: the gates run offline on stdlib Python.

**What is broken or overstated**

1. **Every token number in the repo is a word count.** Reduction is 78%, not 86%; per-skill costs are understated 1.5–2.3×.
2. **Ambient listing is 43k tokens** at full install — the largest single context cost, and the docs don't discuss it.
3. **Routing fails its own gate** (72.8% < 80%). At 320 skills, lexical matching has hit its ceiling; embeddings were scoped but never built. This is the binding constraint — cheap compiled skills don't help if the wrong one is loaded.
4. **Progressive disclosure is largely unimplemented in practice** — 256/314 skills lack 3 QUICK markers, and the check cannot fail the build.
5. **The 9.8/10 is a report, not a gate** — the script always exits 0 and never runs in CI.
6. ~~`FULL_COUNT=298` was hardcoded in `scripts/init-project.sh`~~ — **fixed 2026-09-14**: the full
   count is now computed from the corpus, so it cannot drift. (It read 298 against a 322-skill
   checkout, and the MCP self-test asserted 304, and CI asserted 298 in four places.)

**Priority order if you want to fix it**

1. Make `estimate_tokens` fail loudly without `tiktoken`, or vendor a lightweight counter — every budget claim depends on it.
2. Gate routing (it's already red) — highest actual impact on context efficiency.
3. Make ambient listing a real concern: publish per-tier ambient token counts, and prefer MCP-only installs.
4. Gate the audit dimensions, or stop citing 9.8/10 as evidence.

## Reproduce

```bash
python3 -m venv /tmp/tokvenv && /tmp/tokvenv/bin/pip install tiktoken
/tmp/tokvenv/bin/python - <<'PY'
import pathlib, re, json, statistics, tiktoken
enc = tiktoken.get_encoding("cl100k_base"); tok = lambda s: len(enc.encode(s))
# true reduction
raw=comp=0
for p in pathlib.Path('skills').glob('*/*/SKILL.md'):
    x=pathlib.Path('.skills-compiled')/p.parent.name/'skill.xml'
    if x.exists(): raw+=tok(p.read_text()); comp+=tok(x.read_text())
print(f"true reduction {round((1-comp/raw)*100,1)}%  raw={raw:,} compiled={comp:,}")
# ambient listing
d=0
for p in pathlib.Path('skills').glob('*/*/SKILL.md'):
    m=re.search(r'^description:\s*(.*(?:\n\s{2,}.*)*)', p.read_text(), re.MULTILINE)
    d+=tok(re.sub(r'\s+',' ',m.group(1)).strip()) if m else 0
print(f"ambient descriptions ~{d:,} tokens")
PY
```
