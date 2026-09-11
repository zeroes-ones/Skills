# Missing Skills — Deep Research and Build Plan

> **The question.** Which skills would this library need to build applications that are high
> performance, scalable, reliable and maintainable — and what does the evidence say about "zero
> bugs"?
>
> **Method.** Web-grounded research into (a) why production systems actually fail, (b) what
> measurably reduces defects, and (c) whether zero defects is achievable — then a coverage audit of
> all 304 skills to find which concerns have no owner. Every claimed gap was verified by name and
> content search; every claim about the library was checked against the files.
>
> **Read the caveat in §7 before quoting numbers.** Several sources are preprints, theses, or
> vendor surveys.

---

## 1. The short answer

**"Zero bugs" is not achievable, and the honest goal is better than it sounds.** The strongest
evidence — seL4, CompCert, NASA Cleanroom — shows that the real target is **zero *escaped* defects in
a bounded, high-risk core**, with the boundary made explicit. seL4's own FAQ says *"So does seL4 have
zero bugs? Yes, of course, and no, of course not."* Its proofs guarantee **no deviation from
specification**, resting on assumptions (in-kernel assembly, hardware, boot code, DMA) that are
themselves unverified.

The library is already strong where most teams are weak — architecture, security, testing, delivery.
The gaps are concentrated in **operational reality**: the things that actually cause outages at scale.
Research is unusually consistent on this:

| Finding | Source |
|---|---|
| **Over half of incidents stem from software changes**; deployments and config updates link disproportionately to *high severity* and *manual remediation* | TU Delft, 348 VOID incident reports, 2025 |
| **Roughly half of incidents are non-code** — capacity, manual deploy error, expired certificates | Microsoft Teams study, ACM |
| **>90% of incidents are mitigated without a code change** (rollback, config, reboot) | same |
| Top secondary contributors: **communication 48.2%, monitoring gaps 46.5%, documentation 41.1%** | TU Delft, 1,500 postmortems |
| **Only 16–17% of modules contain identified faults**; faults show long-tail lifetimes; most versions carry **3–10 simultaneous faults** | Defects4J/BugsInPy analysis, 2025 |
| **75% of flaky tests fail in clusters**; dominant causes are **networking and unstable external dependencies** — not the concurrency bugs older studies emphasised | EASE '25, 810 flaky tests |

So the highest-value missing skills are not more coding skills. They are the ones that address
**change, configuration, capacity, dependencies, and time** — precisely the categories the library
does not yet own.

---

## 2. Coverage audit — what already exists

Verified by scanning all 304 skills. The library is genuinely strong here; no gaps are claimed in
these areas.

| Concern | Owner(s) | Verdict |
|---|---|---|
| Performance / profiling / load testing | `performance-engineer` | **Covered** — flame graphs, k6/wrk/Artillery, performance budgets, SLOs |
| Reliability / SLOs / error budgets / toil | `site-reliability-engineer` | **Covered** |
| Chaos / fault injection | `chaos-engineer` | **Covered** |
| Observability | `observability-engineer` | **Covered** |
| Architecture / API / DB design | `system-architect`, `api-designer`, `database-designer`, `codebase-design` | **Covered** |
| Testing (unit, TDD, API, browser) | `tdd-guide`, `qa-engineer`, `api-test-suite-builder`, `browser-testing-with-devtools` | **Covered** |
| Security (app, cloud, supply chain, IAM, crypto) | 12 skills in `08-security` | **Covered** |
| Delivery (CI/CD, containers, releases, cloud, IaC) | `ci-cd-builder`, `docker-kubernetes`, `release-manager`, `cloud-architect`, `automation-engineer` | **Covered** |
| Migration / deprecation / refactoring | `migration-architect`, `deprecation-engineer`, `cross-repo-refactoring` | **Covered** |
| Incident response | `incident-responder` | **Covered** (but see gap #8) |
| Build systems / dependencies / monorepo | `build-system-design`, `dependency-governance`, `monorepo-manager` | **Covered** |
| Documentation / technical writing | `documentation-engineer`, `technical-writer` | **Covered** |
| AI/LLM engineering + evals | 15 skills in `22-ai-engineering` | **Covered** |

**Important nuance.** Many gap keywords *appear* in existing skills — "circuit breaker" in 40 skills,
"idempotency" in 28, "rate limit" in 69. But **mentioning a concept inside another skill is not
owning it.** No skill is *named* for resilience patterns, caching, capacity, consistency,
multi-tenancy, configuration, or test-data. That is the distinction the gap list is built on: these
are concerns a practitioner must own deliberately, with their own decision trees, failure modes and
verification — not footnotes in a broader skill.

---

## 3. The gaps, ranked by evidence

Each gap: what's missing, why the research says it matters, and what the skill would own.

### Tier 1 — directly implicated in the majority of real outages

#### G1 · Resilience & Fault-Tolerance Patterns
- **Missing owner for:** circuit breakers, bulkheads, timeouts, retries with **jittered backoff**,
  load shedding, graceful degradation, hedging, fallback chains, blast-radius containment.
- **Evidence:** change- and dependency-induced failures dominate incident data; the AWS Oct 2025
  outage was a **race condition in DNS automation** cascading across EC2/Lambda (~$1.1B, 15h).
  Azure Oct 2025 was an *"inadvertent configuration change"* cascading to M365/Entra/Xbox. Cascading
  failure is the characteristic modern failure mode.
- **Why not covered:** `chaos-engineer` *finds* weaknesses; nothing *designs the defence*. 40 skills
  mention "circuit breaker" — none owns the pattern catalogue, the tuning math, or the
  failure-mode analysis.
- **Owns:** pattern selection tree (timeout → retry → circuit breaker → bulkhead → shed), the
  retry-storm math (why jitter is mandatory), degradation ladders, per-dependency budgets,
  verification criteria (chaos test per pattern).

#### G2 · Caching & Cache Correctness
- **Missing owner for:** cache invalidation strategy, TTL vs. event-driven invalidation, stampede /
  thundering-herd protection, negative caching, cache-key design, consistency windows, warm-up,
  multi-layer coherence.
- **Evidence:** "cache stampede" appears in **1 skill**, "cache invalidation" in 15 — as mentions.
  Capacity exhaustion is a leading root cause in the VOID analysis, and cache is the most common
  capacity lever. Cache bugs are also the archetypal *correctness* bug that tests rarely catch.
- **Why not covered:** `performance-engineer` treats caching as an optimisation technique, not as a
  correctness-critical subsystem with its own failure modes.
- **Owns:** invalidation decision tree, stampede defences (single-flight, probabilistic early
  expiry), key design, coherence rules per layer, staleness budget, verification (stale-read
  detection under load).

#### G3 · Capacity Planning & Load Modelling
- **Missing owner for:** demand forecasting, headroom policy, autoscaling policy design (and its
  failure modes), queueing-theory sizing, saturation detection, load-shed thresholds, capacity
  drills.
- **Evidence:** **capacity issues and code defects are the leading root causes** in the VOID study;
  capacity-driven outages form a distinct archetype. 23 skills mention "capacity plan" — none owns
  the model.
- **Why not covered:** `performance-engineer` answers *"is it fast?"*; capacity answers *"what load
  breaks it, and what do we do before that?"* Different artefact, different owner.
- **Owns:** load model from real traffic, headroom policy, autoscaling design + anti-patterns
  (flapping, cold-start stampede), saturation signals, capacity drill procedure, cost/latency
  trade-off table.

#### G4 · Multi-Tenancy Engineering
- **Missing owner for:** tenant isolation models (silo/pool/bridge), noisy-neighbour defence,
  per-tenant rate limits and quotas, tenant-scoped data access, per-tenant encryption, onboarding/
  offboarding, migration between isolation models, per-tenant cost attribution.
- **Evidence:** 14 skills mention multi-tenant; **none owns it**. This is the defining correctness
  *and* reliability risk of B2B SaaS — a cross-tenant data leak is an existential incident, and
  noisy-neighbour is the classic capacity failure.
- **Why not covered:** `saas-monetization-strategist` and `micro-saas-developer` cover business and
  build paths, not isolation engineering.
- **Owns:** isolation-model decision tree with cost/risk trade-offs, enforcement points, leak test
  design (the verification that actually matters), quota and fairness design.

### Tier 2 — correctness hazards that testing systematically misses

#### G5 · Data Consistency & Distributed Transactions
- **Missing owner for:** consistency models (strong/eventual/causal/read-your-writes),
  sagas and compensating transactions, outbox/inbox, exactly-once semantics, idempotency keys,
  dual-write problems, reconciliation, **isolation levels and their anomalies**.
- **Evidence:** 28 skills mention idempotency, 29 mention race conditions — but **"isolation level"
  appears in 1 skill**. Race conditions caused the AWS 2025 outage. Most system versions carry
  multiple simultaneous faults, and distributed state bugs are the hardest to detect.
- **Owns:** consistency-model selection tree, saga vs. 2PC decision, outbox pattern, idempotency
  key design, reconciliation job design, anomaly→isolation-level table.

#### G6 · Time, Clocks & Temporal Correctness
- **Missing owner for:** clock skew, NTP drift, monotonic vs. wall clocks, timezone/DST handling,
  leap seconds, expiry-related outages, scheduling across time zones, ordering without a global
  clock.
- **Evidence:** **"leap second" appears in 0 skills; "clock skew" in 1.** The incident taxonomy
  literature calls out *time-related* failures as a distinct, recurring category — certificate
  expiry, leap seconds, NTP — each capable of taking down a fleet. CrowdStrike-class events and
  cert-expiry outages share this shape.
- **Owns:** time-source rules (never wall-clock for durations), DST/timezone test matrix, expiry
  inventory and renewal automation, leap-second posture, ordering strategy.

#### G7 · Configuration & Change Safety
- **Missing owner for:** config-as-code, schema for config, validation before apply, progressive
  rollout of config, drift detection, blast-radius limits, config rollback, change-freeze windows.
- **Evidence:** this is the **strongest signal in the research.** Over half of incidents stem from
  changes; config updates correlate with *high severity*; ~half of incidents are non-code; Azure's
  outage was a config change; CrowdStrike was a **config artifact** (a channel file), not a driver.
  The literature repeatedly concludes: **treat configuration like code.**
- **Why not covered:** `devops-engineer`/`ci-cd-builder` cover pipelines, not the *safety properties
  of a change* as a first-class concern. "Config drift" and "config as code" appear in **1 skill
  each**.
- **Owns:** change-classification model (what can be rolled back, what cannot), config validation
  gates, staged rollout design, drift detection, the "unmanaged change" anti-pattern list.

#### G8 · Postmortem & Learning System
- **Missing owner for:** blameless postmortem facilitation, causal analysis beyond single
  "root cause" (multi-factor), action-item tracking to closure, incident taxonomy, learning loops,
  near-miss capture, recurring-pattern detection.
- **Evidence:** **communication failures 48.2%, monitoring gaps 46.5%, documentation 41.1%** are the
  top *secondary* contributors — and a companion study found **76% of reports disclose no specific
  technical solution**, capping cross-organisation learning. Most incidents have **multiple
  contributing factors**, which invalidates single-root-cause analysis.
- **Why not covered:** `incident-responder` handles the *live* incident. Nothing owns the
  *aftermath* — and the research says the aftermath is where the systemic weakness lives.
- **Owns:** facilitation guide, multi-factor causal model (contributing vs. triggering), action-item
  lifecycle with closure verification, taxonomy for pattern detection, near-miss programme.

### Tier 3 — the defect-prevention frontier

#### G9 · Property-Based & Generative Testing
- **Missing owner for:** property identification, generators/shrinking, invariants, metamorphic
  testing, model-based testing, stateful/property testing, oracle design.
- **Evidence:** the **strongest quantitative result found**: each property-based test finds
  **~50× as many mutations as the average unit test**; tests checking exceptions, collection
  inclusion and types are **>19× more effective**; **76% of mutations are found within the first 20
  random inputs**. Combining PBT with example-based testing lifted detection **68.75% → 81.25%**.
- **Why not covered:** `tdd-guide` is example-based. "Property-based" appears in 7 skills as a
  mention; **no skill owns it**.
- **Owns:** how to derive properties from a spec, generator design, shrinking, stateful model
  testing, when PBT beats examples (and vice versa).

#### G10 · Mutation Testing & Test-Suite Adequacy
- **Missing owner for:** mutation testing at scale, mutant selection, equivalent-mutant handling,
  using mutation score as a *suite-quality* gate, coverage's limits, test-suite health metrics.
- **Evidence:** mutants are a validated proxy for real faults (FSE 2014), but the coupling
  hypothesis is **contested** — one study recreated only **7% of real faults fully, 71% partially,
  and 22% not at all**. Statement coverage alone may yield only **~10% fault detection**. So: a
  suite-quality gate is needed, and its limits must be stated honestly.
- **Owns:** mutation gate design (incremental, change-scoped), equivalent-mutant triage, the
  coverage-is-not-adequacy argument with numbers.

#### G11 · Static Analysis & Code Quality Gates
- **Missing owner for:** choosing and tuning analysers, false-positive economics, treating issue
  *density* as a defect predictor, incremental adoption, custom rule authoring, gate design.
- **Evidence:** CodeQL across 258 embedded projects found **709 true defects (34% false positives)**
  — yet **only 3% of projects used anything beyond trivial compiler checks**. Conversely, Tencent
  found false alarms **>76%**, costing 10–20 min each; LLM-assisted triage cut them **94–98%**. And
  a key practical finding: **issue densities predict defect-prone modules (correlation 0.37–0.73)**
  better than individual findings.
- **Owns:** analyser selection, false-positive budget, density-as-predictor workflow, incremental
  rollout, LLM-assisted triage.

#### G12 · Test Data Management
- **Missing owner for:** synthetic data generation preserving production *shape* and statistical
  properties, anonymisation/pseudonymisation with re-identification resistance, referential
  integrity across environments, seed data versioning, data subsetting, PII-safe fixtures.
- **Evidence:** **75% of flaky failures cluster**, driven by unstable external dependencies and
  networking — and shared, mutable test data is a primary cause of exactly that instability.
  Privacy regulation (already covered by `gdpr-privacy`) makes production copies untenable.
- **Owns:** generation strategies, distribution-faithful synthesis, subsetting, PII-safe pipelines,
  fixture versioning, determinism rules.

#### G13 · Formal Specification & Verification (targeted)
- **Missing owner for:** when formal methods pay off, lightweight specification (TLA+/Alloy/
  Dafny/SPARK), model checking, invariants, property proofs, and **honest cost/benefit framing**.
- **Evidence:** **74% of recreated memory-safety defects detected** across four embedded OSes at
  ~20 proof lines / ~87 min per unit; SPARK discharged **98.76% of 152,927 verification conditions
  automatically**; CompCert has a machine-checked proof and Csmith found **no miscompilations** in
  its proven middle-end. But: **10–100× cost overhead**, seL4 at **~23 proof lines per line of code,
  ~20–25 person-years for ~9K lines, ~$350–1,000/line**, and most projects took **over a year**.
- **Owns:** a *decision framework* (what is worth proving), the lightweight-spec entry path, proof
  assumptions documentation, and the cost model — so teams stop treating formal methods as
  all-or-nothing.

### Tier 4 — sustainability (maintainability at scale)

#### G14 · Technical Debt & Legacy Sustainability Engineering
- **Missing owner for:** debt identification and **quantification in currency**, interest modelling,
  strangler-fig sequencing economics, refactoring ROI, debt registers with ownership, code-health
  trend tracking, "when to rewrite vs. rehabilitate".
- **Evidence:** faults have **long-tail lifetimes** — many persist months or years — and most
  versions carry multiple simultaneous faults. Debt compounds the same way. Note: **`debt-optimizer`
  already exists but it is a *personal-finance* skill** (avalanche vs. snowball) — a genuine
  engineering gap sits behind a confusing name.
- **Owns:** debt taxonomy with cost model, interest estimation, prioritisation by risk × interest,
  strangler sequencing, rewrite-vs-rehabilitate decision tree.

#### G15 · Backwards Compatibility & API/Data Evolution
- **Missing owner for:** compatibility policy, deprecation windows and telemetry, consumer-driven
  contract tests, schema evolution rules, dual-write/dual-read migration windows, breaking-change
  classification.
- **Evidence:** **external dependencies** are a named root-cause category, and API changes are the
  classic cross-team breakage. 21 skills mention "backward compatibility" — none owns the discipline.
- **Owns:** compatibility contract, consumer inventory, contract-test workflow, schema-evolution
  rules per datastore, breaking-change gate.

#### G16 · Architecture Decision Records & Rationale
- **Missing owner for:** ADR lifecycle, decision capture with context and consequences, superseding
  decisions, decision archaeology, linking decisions to code, "why is it like this?" recovery.
- **Evidence:** **documentation issues contribute to 41.1% of incidents.** Rationale loss is the
  most expensive form of that — it causes re-litigation and unsafe change. The library has
  `codebase-design` and `system-architect`, which *produce* decisions, but nothing owns the
  *record and lifecycle* of them.
- **Owns:** ADR format and lifecycle, when a decision warrants a record, supersession, archaeology
  workflow, linkage to code and incidents.

---

## 4. What "zero bugs" should mean here — a defensible target

Replace the unachievable slogan with a **measurable, layered target**. This is what the evidence
supports, and it maps onto the engine the library already has.

| Layer | Goal | Mechanism | Evidence basis |
|---|---|---|---|
| **L1 · Prevent** | No known-defect class survives to review | Static analysis on *changed* code, density-based hotspot targeting, type/lint gates | CodeQL: 709 true defects, 34% FP; densities predict defect-prone modules (0.37–0.73) |
| **L2 · Prove locally** | Invariants hold, not just examples pass | Property-based tests on pure/stateful logic; model checking on protocol cores | PBT ~50× mutations/test; PBT+EBT 68.75% → 81.25% |
| **L3 · Measure the suite** | Tests are adequate, not merely present | Change-scoped mutation gate; coverage treated as necessary-not-sufficient | Coverage alone ≈10% detection; mutation recreates 78% of real faults (7% full, 71% partial) |
| **L4 · Survive change** | No change reaches all users at once | Progressive delivery, config-as-code, drift detection, tested rollback | >50% of incidents are change-induced; >90% mitigated without code change |
| **L5 · Survive load** | Saturation is predicted, not discovered | Capacity model, headroom policy, load-shed thresholds, capacity drills | Capacity is a leading root cause; capacity-driven outages are a distinct archetype |
| **L6 · Survive failure** | No single dependency can take the system down | Circuit breakers, bulkheads, jittered retries, degradation ladders | Cascading failure is the characteristic modern mode (AWS/Azure/CrowdStrike 2024–25) |
| **L7 · Recover & learn** | Every incident makes the system stronger | Multi-factor postmortem, action-item closure, near-miss capture | Secondary issues: comms 48.2%, monitoring 46.5%, docs 41.1%; 76% of reports disclose no fix |
| **L8 · Bound the core** | The highest-risk core is *proved*, the rest is *tested* | Targeted formal verification with documented assumptions | seL4 74% memory-safety defect detection; SPARK 98.76% auto-discharge; 10–100× cost |

**The key discipline:** state the boundary explicitly. *"This component is proved against this
specification under these assumptions; everything outside is covered by layers L1–L7."* That is
honest, and it is the difference between a claim and a guarantee — the same distinction this
library's engine now enforces with `--enforce-contracts`.

---

## 5. The build plan

### Phase A — stop the bleeding (Tier 1: G1–G4)

These four address the failure modes with the most direct evidence and the largest blast radius.

| Order | Skill | Why first |
|---|---|---|
| 1 | `resilience-pattern-engineer` (G1) | Cascading failure is the characteristic mode; no owner today |
| 2 | `configuration-change-safety` (G7 — pulled forward) | The single strongest research signal: config + change = high-severity incidents |
| 3 | `caching-architect` (G2) | Cache correctness *and* the main capacity lever |
| 4 | `capacity-planning-engineer` (G3) | Capacity is a leading root cause; needs its own model |

**Acceptance per skill:** full template compliance; `workflow:` contract with ≥3 criteria grounded
in its own verification table; a decision tree per major choice; ≥3 named failure modes with
detection signals; a verification section whose checks are runnable; a worked backtest example;
chain edges declared both ways.

### Phase B — correctness under distribution (Tier 2: G5, G6, G8)

| Order | Skill | Why |
|---|---|---|
| 5 | `distributed-consistency-engineer` (G5) | The hardest correctness class; isolation-level coverage is near-zero today |
| 6 | `time-and-clock-correctness` (G6) | 0 skills mention leap seconds; expiry/time failures recur |
| 7 | `postmortem-facilitator` (G8) | Learning loop; addresses the top *secondary* incident factors |

### Phase C — defect prevention frontier (Tier 3: G9–G13)

| Order | Skill | Why |
|---|---|---|
| 8 | `property-based-testing-engineer` (G9) | Best measured defect-detection return |
| 9 | `test-adequacy-engineer` (G10) | Mutation gate; honest coverage limits |
| 10 | `static-analysis-engineer` (G11) | Cheapest prevention; density-as-predictor workflow |
| 11 | `test-data-engineer` (G12) | Removes a primary flakiness cause; privacy-safe |
| 12 | `formal-methods-advisor` (G13) | Decision framework + cost model, not advocacy |

### Phase D — sustainability (Tier 4: G14–G16)

| Order | Skill | Why |
|---|---|---|
| 13 | `legacy-sustainability-engineer` (G14) | Long-tail faults; debt interest compounds |
| 14 | `api-evolution-engineer` (G15) | Dependency breakage; contract tests |
| 15 | `adr-and-decision-records` (G16) | Rationale loss drives unsafe change |

### Phase E — wire them into the platform

The skills are only half the value; the other half is making them **executable nodes**:

1. Declare `workflow:` contracts on all 16 (artifacts, criteria, evidence, escalation).
2. Add **manifests** for the recurring shapes: a release-readiness graph
   (capacity → resilience → config-safety → canary → postmortem-on-failure) and a
   defect-prevention graph (static analysis → property tests → mutation gate → ADR update).
3. Add **golden eval sets** — the library currently has them for **3 of 304** skills. These 16 are
   the right place to start, because their outputs are checkable (a capacity model either has
   headroom math or it does not).
4. Extend `docs/HOW-IT-WORKS.md` with the L1–L8 model so the target is stated in one place.

**Realistic effort.** Phases A–D are 16 skills of substantial content. Based on this library's own
measured shape (~8,850 words per skill) and the fact that each needs a worked example and a
grounded contract, treat it as **16 focused sessions**, not a batch operation. Phase E is
incremental and can proceed skill-by-skill.

---

## 6. What I would *not* build, and why

Saying no is part of the plan:

| Candidate | Why not |
|---|---|
| A generic "microservices" skill | `system-architect` + `event-driven-architect` + `cloud-architect` already cover the design space; a fourth would fragment ownership |
| A "performance" skill | `performance-engineer` is strong and specific. Capacity (G3) is a genuinely different artefact — that is the one to add |
| A "testing" skill | `tdd-guide` + `qa-engineer` + `api-test-suite-builder` cover it. PBT (G9) and adequacy (G10) are the real missing pieces, not "testing" |
| A "DevOps" or "SRE" skill | Both exist and are specific. The gaps are config-safety (G7) and postmortem (G8) — narrower and different |
| A "clean code" / "SOLID" skill | Covered by `code-reviewer`, `code-simplification`, `codebase-design`; low marginal value |
| An "AI writes code safely" skill | Interesting and evidence-backed (DORA 2025 links AI usage to **delivery instability**; 72% of orgs reported an AI-related incident) — but it is a *policy* concern that cuts across existing skills. Better as a section in `code-reviewer` + `ai-safety-engineer` than a new skill |

---

## 7. Sourcing caveat

Weigh these findings accordingly — I am not presenting them as uniformly solid:

| Strength | Sources |
|---|---|
| **Peer-reviewed / industrial, strong** | ACM Microsoft Teams incident study; ISSTA 2024 (container runtime, Kubernetes operator bugs); ISSTA 2025 (CodeQL on embedded); OOPSLA 2025 (PBT, 426 programs); EASE '25 (systemic flakiness); TOSEM 2024 (database-access bugs); ISSRE 2025 (GenAI cloud incidents); FSE 2014 (mutation validity); seL4/CompCert verification results; NASA Cleanroom defect densities |
| **Preprints / theses — directionally useful** | TU Delft VOID analyses (348 and 1,500 reports); Defects4J multi-fault analysis; software-misconfiguration taxonomy; LLM false-positive reduction |
| **Vendor-sponsored surveys — treat as marketing-adjacent** | DORA 2025 (AI + instability), Harness, Tricentis, Temporal |
| **Widely repeated but secondary retellings** | seL4 cost figures (~$350–1,000/line, ~23 proof lines per LOC); exact LOC/person-year counts vary between sources |
| **Explicitly contested in the literature** | The mutation-testing *coupling effect* — one study recreated only 7% of real faults fully. Mutation score is a *proxy*, not proof |

Two claims I deliberately did **not** make: that any technique yields zero defects, and that these
sixteen skills are sufficient. The first is false by the evidence; the second would be a guess.

---

## 8. Recommended next action

Build **`resilience-pattern-engineer` (G1)** first, end to end, as the template for the rest:

1. Author it to full template compliance with a grounded `workflow:` contract.
2. Add a backtest example (a cascading-failure scenario, with the defence that would have stopped it).
3. Declare chain edges both ways and validate (`validate-chains.py`, `validate-workflows.py`).
4. Run it as a **real node** — the way Phase 1 proved `senior-dev-loop` — with
   `AGENT_CMD='claude -p'` and `AGENT_FALLBACK=0`, and archive the run under `examples/`.
5. Then decide, from a working exemplar, whether the remaining fifteen follow the same shape.

That order matters: this library's own evidence (Phase 1, defects D1–D3) is that a skill's real
problems only appear when an agent actually runs it. Authoring sixteen skills before proving one
would repeat a mistake already documented in the build log.
