# Beyond Loops and Graphs — Deep Research for 10/10 Superior Skills

> **Version 1.0.0** — Research synthesis answering: *once a skill can run as a node in a bounded,
> verified graph with clean handoffs (WORKFLOW-SYSTEM.md), what comes next to make skills 10/10
> superior?* Companion to `END-TO-END-EXCELLENCE.md`. Research is web-derived (2025-2026 agent
> literature and production practice); treat findings as directional input, verify before
> adopting. Repo-coverage claims were checked against this library's current skill set.

## 1. The short answer

Loops and graphs solved **deterministic control flow**. The next frontier is about the **other 80%
of agent quality**: durable memory, evidence-based self-improvement, eval-gated change, run-level
observability, guardrail-enforced handoffs, and semantic skill routing. Concretely, six capabilities
turn "a graph that terminates" into "a graph that gets better, is provable, and is safe at scale":

1. **Memory across runs** — the graph forgets nothing that matters and remembers nothing that rots.
2. **Evals as merge gates** — no skill or prompt change ships without passing regression evals.
3. **Self-improvement from traces** — runs distill into skills, gated by verification before promotion.
4. **Observability of agent runs** — every node/verdict/handoff is traceable to cost, latency, and outcome.
5. **Guardrails at graph edges** — output safety enforced between nodes, not just at the ends.
6. **Semantic skill retrieval** — the right skill for a task is found at scale, not by scrolling a router.

## 2. Research ground truth (what 2025-2026 work converged on)

| Frontier | Research signal | Sources (verify before relying) |
|----------|-----------------|---------------------------------|
| Memory | Context rot is real: accuracy degrades non-uniformly as context grows ("lost in the middle"); memory = **write–manage–read**, and *Manage* (consolidation, deletion, feedback) is what separates memory from RAG. Asynchronous "sleep-time" consolidation cuts test-time compute ~5× at equal accuracy; naive summary-merging drifts. Memory poisoning is a first-class threat (>95% injection success against naive stores). | Chroma context-rot work; Memory for Autonomous LLM Agents (write-manage-read); Letta "Sleep-time Compute" (arXiv 2504.13171); MemoryOS (EMNLP 2025); A-Mem (NeurIPS 2025); memory-poisoning analyses |
| Evals-as-gates | "An agent without evals is a demo, not a product." Evals are versioned artifacts run in CI; merge blocks on **delta vs. baseline** (not absolute scores); **golden datasets** (10-20 → 50-500 stratified cases); code-based graders first, calibrated LLM judges only where needed; every production incident becomes a new "never-again" regression eval; multi-stage gates (fast PR → integration → canary) with cost/latency budgets. | AOEpeople AI Radar EDD; Microsoft "Automate prompt regression & optimization" (gates: no metric degrades >2%, 100% safety-critical pass, prior tests still pass); Galileo CI fundamentals; Kinde CI/CD-for-evals; Evaluation-Driven Development of LLM Agents (arXiv 2411.13768) |
| Self-improvement | Traces → skills, **verifier-gated promotion**: ASG-SI compiles agents into "auditable skill graphs," promoting only after replay + contract checks (self-improvement should be measurable/reproducible, not opaque drift); ASI induces programmatic skills from traces (+23.5% WebArena, verified by re-execution); Contextual Experience Replay gives 31.9-36.7% SOTA without training; trajectory bootstrapping lifts ALFWorld 73%→89-93%. Unverified self-improvement risks hallucinated/overfit skills — the verification gate is the whole point. | ASG-SI (arXiv 2512.23760); ASI (CMU); CER (ACL 2025); SAMULE (EMNLP 2025); trajectory bootstrapping (arXiv 2505.00234); "Hidden costs of RLVR" |
| Observability | OTel is the standard: agent run = **tree of spans** (session → run → node/tool/model call) with stable span names, run_id correlation, token/cost/latency on every span; 100% sampling on guardrail trips/errors; redact PII instead of storing plaintext prompts; sessions are the missing layer for multi-turn evals. | OpenTelemetry GenAI conventions; LLM-Agents-Ecosystem-Handbook tracing; Arize agent observability; Skywork LLM observability |
| Guardrails/handoffs | Guardrails are **runner-lifecycle primitives**: input guardrails at start; output guardrails on the *final* output only, and streamed candidates stay hidden until the guardrail passes; handoff = control transfer with context filter. Layered defenses map to OWASP Top 10 for LLM apps (indirect injection #1). Treat agents like distributed systems: SLIs/SLOs, allow-listed tools, scoped credentials, HITL approvals, audit trails. | OpenAI Agents SDK runner lifecycle; OWASP Top 10 LLM (2025); genta.dev reliability engineering; GuardAgent (ICML 2025) |
| Semantic retrieval | Loading all tools/skills degrades accuracy 7-85% and bloats tokens 50-100×; embeddings + top-K is the base; **the skill body (not metadata) is the decisive routing signal** (removing it drops retrieval 29-44 points); dependency-aware "bundles" from a skill graph beat flat top-K; intra-skill retrieval (which section of a skill to load) cuts tokens ~47%. | vLLM Semantic Router analyses; BAAI SkillRouter; Graph-of-Skills; SkillPager |

## 3. Current library coverage vs. the frontier (checked, not assumed)

| Frontier | Already here | Genuine gap |
|----------|--------------|-------------|
| Memory | `context-engineering` (in-session context strategy), run-state decision ledger, `loop-reflect` | **No durable run-memory / experience bank** (across sessions/runs) — nothing manages write/consolidate/retrieve/forget; nothing in the runner reads past-run memory |
| Evals | `agent-eval-pipeline`, `evals/` suites, `loop-graph-behavior` scenarios, pre-commit G15 (structural) | **No golden-set regression gates over skill content**; behavioral scenarios exist as data but are not executed as merge-blocking CI gates with delta thresholds and judge calibration |
| Self-improvement | `loop-reflect` → ledger, `dynamic-skill-creator` (manual authoring), `doubt-driven-development`, engine replay/checkpoints | **No trace→skill pipeline** (auto-draft a skill from a successful/failed trajectory, re-run it on saved trajectories, promote only if verified). Audited-skill-graph ideas map 1:1 onto our manifest + coverage machinery — but the collector/promoter loop does not exist |
| Observability | Runner `log` + run-state checkpoints; `observability-engineer` (application infra) | **No agent-run telemetry convention** (OTel spans per node, cost/latency/verdict, stable span names, PII-safe logging, session-level evals) |
| Guardrails | `applying-llm-guardrails`, `ai-security`, payload registry + state-hash checks at handoff | **No guardrail hooks in the runner** (output classification between nodes; per-edge safety policy in manifests; injection defense across handoffs beyond hashes) |
| Semantic routing | `using-agent-skills` (static ASCII router), chain graph, `.skills-compiled` | **No retrieval layer** (embeddings + rerank over 298 skill bodies) and no routing evals (SkillRouter-style accuracy on a held-out task set); router accuracy is untested |
| Governance | `llm-engineer` prompt versioning, skill frontmatter semver | **No skill-version registry / A-B promotion** path with eval deltas tied to `version:` bumps |

## 4. The build map — what "10/10 superior" concretely adds next

> **Build status (this repo, current HEAD):** B1 delivered (`workflow-runner.py --memory`),
> B2 delivered (`evals/golden/<skill>/cases.json` + `scripts/eval-skill.sh` + `lib/eval-golden.py`),
> B3 delivered end-to-end (`scripts/skill-evolve-prep.py` raw-material inbox + `scripts/
> skill-evolve-promote.py` verifier-gated promotion, demoed accept/reject on the flagship
> exhaustion trace with an audit ledger; content auto-drafting is the next refinement),
> B4 delivered (`scripts/export-traces.py` + per-workflow SLI gate `scripts/skill-sli-report.py`,
> wired as CI step 1g; span-backend ingest is import-ready JSONL), B5 delivered
> (`--guardrail` hook + `lib/guardrails.py`; per-edge manifest policy still to build),
> B6 delivered (baseline `scripts/build-skill-index.py`: 298-skill index + lexical Top-1 30%
> routing baseline; embedding+rerank layer still to build). G2 parallel join landed in the
> engine; G3 wired golden evals into CI (run-ci step 1e + pre-commit G15).

Each item names the artifact, where it plugs into existing machinery, and the acceptance bar.

### B1 — Run memory & experience bank (Frontier 1)
**Build:** a `agent-run-memory` design + runner hook (`scripts/workflow-runner.py --memory <dir>`)
that at run end appends a structured memory entry (task, verdicts, artifacts, decisions,
cost/steps, outcome) to a per-domain store with write-manage-read semantics (append + weekly
consolidate job, not naive summary-merging).
**Why it beats a bigger context window:** context rot is empirical; durable, retrievable,
consolidated memory is the fix the literature converged on.
**Acceptance:** memory entry written per completed run; retrieval surface (grep/embedding later)
returns the prior run for "we did this before"; memory-poisoning guard: entries are never trusted
as instructions, only as context (documented provenance field).

### B2 — Eval-driven skill development (Frontier 2)
**Build:** per-skill **golden datasets** (`evals/golden/<skill>/cases.json`), a
`scripts/eval-skill.sh` runner, and a **merge-gate**: on any `SKILL.md` change, run the changed
skill's golden cases + the `loop-graph-behavior` behavioral suite; block on delta vs. baseline
(pass rate, safety-critical 100%, token budget). Every incident/postmortem adds a case.
**Why:** "evals as unit tests" is the strongest 2025 consensus; our pre-commit is structural today,
not behavioral.
**Acceptance:** a PR touching a skill body runs ≥1 golden case + behavioral scenario; CI shows
pass-rate delta vs. main; ≥1 "never-again" case pattern documented.

### B3 — Self-improvement from traces (Frontier 3)
**Build:** `skill-evolution` flow: runner records trajectories (already does, in run-state + log);
a distiller (using `writing-great-skills` + `dynamic-skill-creator` conventions) drafts a skill or
reference patch; **verification gate**: replay the new content against the recorded trajectories
(engine checkpoints make this cheap) plus golden evals; promote only on pass; reject with the
trace as evidence otherwise. Audited: every promotion links to the source run(s).
**Why:** matches ASG-SI/ASI/CER — trace distillation that is verifier-gated, auditable, and
reversible. This is the natural machine to close END-TO-END gap G5 (learning feedback).
**Acceptance:** one end-to-end demo: run flow → failure trace → auto-draft fix → replay passes →
promoted with source-run citation; regression detected by eval delta.

### B4 — Observability of agent runs (Frontier 4)
**Build:** `agent-observability` skill + exporter (`scripts/export-traces.py`) that turns a
run-state checkpoint into OTel-shaped spans (session = workflow, span per node with
`status/verdict/evidence/cost/tokens/latency`), stable span names (`workflow.<name>.node.<id>`),
PII-safe logging policy, and 100% sampling on guardrail trips/escalations.
**Why:** run-state is already a trace — it is one exporter away from Langfuse/Phoenix-class
visibility; without it, "10/10" is unprovable in production.
**Acceptance:** one run-state → OTel JSON with spans per node + totals (steps, tokens, cost);
session id joinable across runs; sample-on-escalation policy documented.

### B5 — Guardrails at graph edges (Frontier 5)
**Build:** runner output-guardrail hook (`--guardrail <module>`): after a node produces its
payload and before the handoff advances, an output classifier runs; streamed/failed output never
advances; per-edge safety policy field in manifests (`safety: inject-check | pii-check`), mapped
to `applying-llm-guardrails` classifiers; injection defense for indirect content arriving via
handoff payloads (context/artifacts) — the exact OWASP #1 vector.
**Why:** guardrail lifecycle semantics (final-output-only, hidden-until-pass, handoff filters) are
now SDK standards; our runner lacks the hook, so "safe graphs" is claimed, not enforced.
**Acceptance:** manifest edge with `safety: pii-check` blocks a poisoned payload before the next
node intake; log entry shows the guardrail trip; 100% sampled.

### B6 — Semantic skill retrieval & routing (Frontier 6)
**Build:** `skill-retrieval` layer: embed 298 skill **bodies** (research: body > metadata) +
descriptions into an index (`scripts/build-skill-index.py`, stdlib+optional embedder), top-K +
rerank, dependency-aware bundle expansion using the existing chain graph (prerequisite bundles);
routing evals on a held-out task→skill set to measure Top-1 accuracy and token savings.
**Why:** static routers stop scaling; 298 skills today, thousands tomorrow; accuracy degrades when
everything is loaded. This complements (not replaces) `using-agent-skills` as the interactive
fallback.
**Acceptance:** index build over all skills; routing eval reports Top-1/Top-5 on a held-out set;
bundle retrieval returns prerequisite skills (chain-backed); tokens-per-task vs. full-load measured.

## 5. Cross-cutting principles (apply to every build above)

1. **Measure before shipping** — every new capability ships with a metric and a baseline.
2. **Verification-gated promotion** — nothing (skill, memory entry, retrieved bundle) is trusted
   without a check; rejected promotions keep their evidence.
3. **Trace-first** — if it isn't in a span/run-state, it didn't happen; stable names, PII-safe.
4. **Delta over absolute** — gates compare candidate vs. baseline because judges and data drift.
5. **Treat agents like distributed systems** — SLOs, budgets, rollbacks, allow-lists, audit trails.
6. **Incidents become cases** — every failure adds a regression case; the suite compounds.
7. **Version everything** — prompts, skills, guardrail configs, golden sets, memory format.

## 6. Phased roadmap

| Phase | Scope | Reuses | Success signal |
|-------|-------|--------|----------------|
| **P0 (now, low risk)** | B4 exporter + B2 golden-set scaffolding + B6 index skeleton | run-state, `evals/`, chain graph, audit tooling | export-trace runs on both shipped checkpoints; ≥3 golden case files; index builds over 298 skills |
| **P1** | B5 edge guardrails + B2 merge gate wired into pre-commit G16 | runner hooks, lint-workflow/CI scripts | poisoned-payload fixture blocked; skill-body PR triggers eval gate in CI |
| **P2** | B1 run-memory + B3 auto-draft distiller (human-in-loop promote) | ledger, dynamic-skill-creator, engine replay | one end-to-end trace→draft→replay→promote demo with source citation |
| **P3** | Routing evals + retrieval routing in production; memory consolidation job | B6 index, run memory | Top-1 routing accuracy measured; tokens-per-task vs full-load published |

## 7. Honest caveats

- Research findings are web-derived and **untreated as ground truth** — each has a source link;
  validate before building policy on them.
- Six builds, not one: they are listed in dependency order (observe before improve; gate before
  trust; retrieve before scale). Doing B2 before B3 is deliberate — you cannot self-improve
  without an eval gate to protect against unverified "improvements".
- "10/10 superior" is a moving target: the acceptance bars above are what make each claim
  checkable, which is the only durable definition.

## 8. Sources (key)

- Context rot / memory: Chroma research synthesis; Memory for Autonomous LLM Agents
  (write-manage-read); Letta Sleep-time Compute arXiv:2504.13171; MemoryOS EMNLP 2025; A-Mem
  NeurIPS 2025; Hindsight/TEMPR.
- Evals-as-gates: AOEpeople AI Radar (EDD); Microsoft prompt regression automation; Galileo CI
  fundamentals; Kinde CI/CD for evals; Evaluation-Driven Development arXiv:2411.13768.
- Self-improvement: ASG-SI arXiv:2512.23760; ASI (CMU, WebArena +23.5%); CER ACL 2025; SAMULE
  EMNLP 2025; trajectory bootstrapping arXiv:2505.00234.
- Observability: OpenTelemetry GenAI conventions; LLM-Agents-Ecosystem-Handbook tracing.md;
  Arize; Skywork.
- Guardrails/handoffs: OpenAI Agents SDK runner lifecycle; OWASP Top 10 for LLM Applications
  2025; genta.dev reliability engineering; GuardAgent ICML 2025.
- Retrieval/routing: vLLM Semantic Router analyses; BAAI SkillRouter; Graph-of-Skills; SkillPager.

## 9. Verified status & decision (checked against the code, 2026-09-07)

Question asked: *should we integrate loops/graphs/handoff like real-world iteration, should we
use vectors too, and should every skill be created dynamically when something new appears?*

### Status — what is already built (verified, not assumed)

| Area | State | Where |
|---|---|---|
| Loops — per-loop `max_iterations`, `exit_when`, stagnation detection, `escalate_to` gate, global step budget | **Built** | `scripts/workflow-runner.py`; manifests incl. `quality-fix-loop.yaml` |
| Graphs — DAG edges, parallel blocks with `join`, group-join semantics | **Built** | runner + `parallel-audits-merge.yaml`; engine self-tests run in the `workflow-graphs` CI job (green) |
| Handoff — `{from, to, payload, sha}` records (sha covers the sending node) | **Built** | runner; `agent-handoff-protocol`, `multi-agent-orchestration` skills |
| Real-agent execution (the "content" leg) | **Built (opt-in)** | `scripts/executors/agent_executor.py` — `AGENT_CMD` with `{prompt}` for claude / gemini / codex / ollama |
| Run-memory (B1) | **Engine-level built** | runner `--memory <dir>` writes durable per-run JSONL |
| Trace exporter (B4) | **Built** | `scripts/export-traces.py`, wired into CI dogfood |
| Edge guardrails (B5) | **Hook built, policy unwired** | runner `--guardrail <module>` classify hook exists; manifest `safety:` edge policy is P1 |
| Semantic retrieval / vectors (B6) | **Lexical baseline built; embeddings NOT yet** | `scripts/build-skill-index.py` (name+description tokens, explicitly a baseline); `run-routing-evals.js` |
| Dynamic skill creation | **Tooling built; auto-draft NOT yet** | `skill-factory.py`, `skill-incorporate.py`, `skill-evolve-prep/promote.py`, `scaffold-skill.sh`; B3 trace→draft→replay→promote is P2 |

### Decisions

1. **Loops / graphs / handoff — already integrated.** The engine, five shipped manifests, CI
   self-tests, and the agent executor cover real-world iteration. *Improve next (P1):* wire
   `safety:` edge policies (B5) into manifests + add the golden-eval merge gate to pre-commit.
   Ship one *agent-in-the-loop* manifest demo (engine + `AGENT_CMD` loop that revises until
   verification passes) as the documented real-world pattern.
2. **Vectors — yes, next after P1.** Rationale: 298 skills today, thousands tomorrow; the static
   lexical router measures ~68.8% rank-1 and will degrade as the corpus grows. Build per B6:
   optional embedder over skill **bodies**, top-K + rerank, chain-bundle expansion, gated on
   beating the lexical baseline on held-out routing evals (acceptance: Top-1/Top-5 up,
   tokens-per-task down vs. full-load). Embedder stays pluggable (API or local ollama) so the
   default can be privacy-preserving/offline.
3. **Dynamic skill creation — yes, but verification-gated.** Create skills *for anything new*
   through a two-tier pipeline instead of unsupervised auto-creation:
   - deterministic on-demand scaffolding today (`skill-factory`/`scaffold-skill.sh` + the
     16-gate governance suite);
   - auto-draft from detected gaps (routing miss, failed node, explicit request) once B3 lands
     (P2) — trace → draft → **human-in-loop promote**; never auto-merge an unvetted skill
     (principle 2: verification-gated promotion).
   This satisfies "dynamic environment" without degrading the library's trust story.
4. **"Add if required"**: no code change is required to answer this question — the roadmap above
   (P1 → B6 → B3) is the add. Revisit status markers here after each phase lands.
