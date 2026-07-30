---
name: agent-persona-orchestrator
description: >-
  Use when orchestrating multiple agent personas (code-reviewer, security-auditor, test-engineer,
  web-perf-auditor) for complex workflows that require parallel auditing, gated deployment, or
  multi-dimensional quality gates. Handles a three-layer architecture (Skills → Personas → Commands),
  parallel fan-out with merge patterns, persona lifecycle management, tool-restriction enforcement,
  and failure-handling strategies. Do NOT use for single-persona tasks, trivial code review, or
  when the workflow does not require persona isolation.
license: MIT
tags:
  - persona
  - orchestration
  - multi-agent
  - fan-out
  - merge-patterns
author: Sandeep Kumar Penchala
type: framework
status: stable
version: 1.0.0
updated: 2026-07-27
token_budget: 3000
chain:
  feeds_into:
    - code-reviewer
    - security-reviewer
    - qa-engineer
    - performance-engineer
    - shipping-and-launch
    - release-manager
output: "reference"
---

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

# Agent Persona Orchestrator
A framework for orchestrating multiple agent personas in complex workflows. Defines a three-layer architecture (Skills → Personas → Commands), parallel fan-out patterns, persona lifecycle, and merge strategies. Use this to construct gated deployment pipelines, multi-dimensional quality checks, and audit workflows where persona isolation matters.

**Inspired by**: GitHub Copilot agent personas, Cursor rules system, multi-agent orchestration patterns, hexagonal architecture, and Unix pipeline composition.

---
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional work and amateur guessing:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify domain currency.** Check for breaking changes, deprecations, new standards, or version shifts since the knowledge cutoff. | [STALE_RISK] Outdated advice breaks real systems. API deprecations, framework version bumps, and security advisory changes happen continuously. Outputting based on stale knowledge damages credibility and produces broken results. | Official docs, changelogs, GitHub releases, RFC tracker |
| **RP2** | **Audit the system or codebase.** Read relevant files. Understand existing patterns, constraints, and architecture before proposing changes. | [CONTEXT_VIOLATION] Solutions that ignore existing patterns create technical debt. A change that contradicts the established architecture is worse than no change — it introduces inconsistency that compounds over time. | Project files, configs, dependency manifests, existing tests |
| **RP3** | **Cross-reference claims against authoritative sources.** Every factual assertion needs a verifiable source. Mark each: [VERIFIED], [COMPUTED], or [ESTIMATED]. | [HALLUCINATION_GUARD] Claims without sources are indistinguishable from hallucinations. The #1 cause of incorrect output is treating assumptions as facts. Source tagging prevents this. | Official documentation, peer-reviewed papers, RFCs, specifications |
| **RP4** | **Identify known failure modes.** Before recommending, list what commonly breaks. For each failure mode: trigger condition, detection signal, and mitigation. | [FAILURE_BLINDNESS] Every domain has known failure patterns. Output that doesn't address them is dangerously incomplete. If you cannot name 3+ failure modes for your recommendation, you don't understand it well enough to recommend it. | Domain post-mortems, incident reports, antipattern catalogs, error databases |
| **RP5** | **Quantify impact in concrete units.** Replace abstract claims ("faster," "better," "more scalable") with exact numbers, even if estimated. | [VAGUENESS_PENALTY] "Faster" is unverifiable. "Reduces p95 latency from 340ms to 120ms (±15ms)" is verifiable. Abstract adjectives hide ignorance behind confidence. Concrete numbers expose gaps. | Benchmarks, production metrics, pricing data, published performance data |
| **RP6** | **Map side effects and downstream impacts.** What else breaks? Which dependencies are affected? Which downstream consumers need updating? | [CASCADE_BLINDNESS] Changes to one component ripple outward. A fix in module A can break module B that depends on A's old behavior. Map the blast radius before acting. | Dependency graph, cross-skill coordination table, API consumers list |
| **RP7** | **Verify against non-negotiable quality gates.** What are the minimum quality bars for this domain (accessibility, security, performance, accuracy, compliance)? | [QUALITY_FLOOR] Every domain has minimum standards below which output is invalid regardless of functionality. Missing WCAG AA = broken. Leaking credentials = broken. Silent data loss = broken. | Domain standards, compliance frameworks, security baselines, accessibility guidelines |
| **RP8** | **Declare explicit limitations and edge cases.** What does this NOT handle? What are the known boundaries? What scenarios are explicitly out of scope? | [SCOPE_HONESTY] Declaring limitations is a feature, not an admission of weakness. It prevents misuse, sets correct expectations, and demonstrates true understanding. Every solution has boundaries — naming them is professional. | This SKILL.md, domain literature, edge case databases |

**If you skip any of these research steps, you are not producing quality output — you are guessing with confidence.** Guessing wastes time, breaks systems, and destroys trust. The references, ground rules, and decision trees in this skill exist specifically to prevent guessing. Use them.

> **Compliance:** Research must be executed before any substantial output. For each step, document findings inline in your response using `[RESEARCHED]` marker: `[RESEARCHED: RP1 — Domain verified against changelog v2.4. No breaking changes since cutoff.]`. Partial research = partial quality. Zero research = zero credibility.



### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

**The RP1-RP8 cycle above is NOT a one-time gate.** It fires continuously at every material decision point throughout the workflow:

| Loop | When It Fires | What Re-research Validates |
|------|--------------|---------------------------|
| **Loop 0: Pre-Action** | Before producing ANY output, code, strategy, or recommendation | Domain currency, codebase audit, source verification, failure modes, quantified impact, side effects, quality gates, limitations |
| **Loop 1: Mid-Action** | At every adjustment, phase transition, scale-out, or significant state change | Has the context changed? Are the original assumptions still valid? Has new information invalidated the Loop 0 conclusions? |
| **Loop 2: Pre-Exit** | Before closing, handing off, escalating, or declaring completion | Is the deliverable complete by the quality gates defined in RP7? Are all limitations declared (RP8)? Have failure modes been addressed (RP4)? |
| **Loop 3: Post-Action** | After completion: compare expected vs. actual outcome | What was the efficiency ratio (actual / theoretical max)? What learnings emerged? What should be fed back into the pattern database for future decisions? |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:
```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. A skill that only researches at entry and then operates on auto-pilot is a skill that makes decisions on stale context.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

**Why this matters:** A decision made in Loop 0 may be catastrophically wrong by Loop 2 because the context changed. Markets move. Requirements shift. Dependencies update. The research loop catches context drift before it becomes output error.

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence.



## <!-- QUICK: 30s --> Route the Request

```
What are you trying to do?
├── Understand the three-layer architecture → Jump to "The Expert's Mindset"
├── Define a new persona with tool restrictions → Jump to "Persona Definition Format"
├── Set up a parallel fan-out workflow → Jump to "Parallel Fan-Out Pattern"
├── Decide single persona vs. fan-out → Jump to "Decision Tree: Single vs. Fan-Out"
├── Handle a persona failure in a running pipeline → Jump to "Failure Handling"
├── Wire a slash command to persona+skill combos → Jump to "Core Workflow"
├── Audit an existing persona configuration → Jump to "Production Checklist"
└── Add a new persona to the registry → Jump to "Adding New Personas"
```

---

## The Expert's Mindset

Personas are isolated execution contexts, not just prompt prefixes. The orchestrator's job is to compose them without coupling them. A world-class orchestrator treats personas like microservices: each owns its domain, communicates through structured outputs, and never reaches into another persona's internals.

### Mental Models

| Model | Description |
|---|---|
| **Personas are containers** | A persona is a bounded context with explicit capabilities. It cannot import another persona's state, call its tools, or depend on its internal reasoning. The orchestrator is the only bridge. |
| **Merge is where value lives** | Fanning out is easy. Merging results — reconciling conflicting findings, de-duplicating issues, producing one actionable report — that's where orchestration delivers ROI. |
| **Hard constraints protect correctness** | Persona A cannot invoke Persona B. This is not a soft guideline — it's a structural invariant. Without it, you get cascading errors, circular dependencies, and unreproducible results. |
| **The orchestrator is the user** | Slash commands and human operators are the only entities that route between personas. No persona-to-persona delegation. Period. |

### Cognitive Biases in Orchestration

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Over-fan-out** | Spinning 8 personas for a 20-line PR because "more audits = more safety" | Each persona adds merge complexity and latency. Start with 2, justify each additional one with a concrete failure mode it catches. |
| **Persona creep** | Adding "just one more tool" to a read-only persona until it becomes indistinguishable from a general-purpose agent | Audit allowed_tools quarterly. If a persona can both read and write, justify why it's not two separate personas. |
| **Merge-as-afterthought** | Spending 90% of design time on fan-out and 10% on merge logic, then discovering merge is the bottleneck | Design merge first. Define the output schema before defining the personas that produce it. Merge is the product; fan-out is the supply chain. |
| **Orchestrator as bottleneck** | Human must manually run every persona and stitch results together | Automate the fan-out command, standardize output formats, and define merge rules declaratively. The orchestrator defines the pattern; slash commands execute it. |

### What Masters Know That Others Don't

- **The best orchestrators spend more time on merge than on fan-out.** Fan-out is a one-liner. Merge is a protocol: schema alignment, conflict resolution, severity normalization across personas, and single-source-of-truth report generation.
- **Persona isolation is the feature.** The constraint that personas can't call each other feels like a limitation. It's actually the architecture's superpower: it forces clean interfaces, reproducible runs, and debuggable failures.
- **Every persona should be replaceable.** If you can't swap the code-reviewer persona for a different implementation without changing the orchestrator, the interface is wrong.

---

## <!-- STANDARD: 3min --> Ground Rules — Read Before Anything Else

- **Personas cannot invoke other personas.** This is a hard constraint, not a guideline. Only the user or a slash command routes between personas.
- **Personas are tool-restricted by design.** A read-only persona that can write files has been misconfigured. Audit allowed_tools at persona creation and on every modification.
- **The orchestrator (user/slash command) is the only coupling point.** No shared state between personas. Each persona receives its full context independently.
- **Only one endorsed multi-persona pattern: parallel fan-out with merge.** Sequential chaining, nested delegation, and persona-to-persona handoffs are explicitly unsupported.
- **Every persona has exactly one default skill.** Multiple default skills create ambiguity in which skill drives the persona's behavior. Additional skills can be invoked explicitly through the orchestrator.
- **Merge output must be actionable.** The merge step produces a single report with clear pass/fail signals, prioritized findings, and de-duplicated issues. If the merge output is "here are 4 raw outputs," the orchestration has failed.

---

## <!-- STANDARD: 3min --> Three-Layer Architecture

```
┌─────────────────────────────────────────────┐
│  LAYER 3: Commands (the *when*)             │
│  Slash commands that route to persona+skill │
│  /review  /audit  /ship  /test             │
└──────────────┬──────────────────────────────┘
               │ routes to
┌──────────────▼──────────────────────────────┐
│  LAYER 2: Personas (the *who*)              │
│  Isolated execution contexts with tool      │
│  restrictions and default skills            │
│  code-reviewer  security-auditor  ...       │
└──────────────┬──────────────────────────────┘
               │ invokes
┌──────────────▼──────────────────────────────┐
│  LAYER 1: Skills (the *how*)                │
│  Existing SKILL.md files providing domain   │
│  knowledge, workflows, and guidance         │
│  code-reviewer  security-reviewer  ...      │
└─────────────────────────────────────────────┘
```

| Layer | What It Provides | Change Frequency | Examples |
|---|---|---|---|
| **Layer 1 — Skills** | Domain knowledge, workflows, best practices | When domain knowledge evolves | `code-reviewer`, `security-reviewer`, `tdd-guide`, `performance-engineer` |
| **Layer 2 — Personas** | Execution context, tool restrictions, system prompts | When persona guardrails change | `code-reviewer`, `security-auditor`, `test-engineer`, `web-perf-auditor` |
| **Layer 3 — Commands** | User-facing entry points, routing rules | When workflows change | `/review`, `/audit`, `/ship`, `/test` |

**Key insight:** Skills evolve with domain knowledge. Personas evolve with guardrail requirements. Commands evolve with workflow needs. These three change at different rates — the architecture separates them so each can evolve independently.

---

## <!-- STANDARD: 3min --> The Four Initial Personas

### Persona Definition Format

Every persona is defined with this exact schema:

```yaml
name: <persona-name>
description: "<one-line purpose, including read-only vs. read-write declaration>"
allowed_tools: [<explicit tool list>]
prohibited_tools: [<explicit tool list>]
system_prompt_additions: "<injected into the persona's system prompt>"
default_skills: [<exactly one skill name>]
orchestration:
  can_invoke: []   # MUST be empty — personas cannot invoke other personas
  parallelizable: <true|false>
```

### 1. code-reviewer

```yaml
name: code-reviewer
description: "Read-only code reviewer. Identifies bugs, logic errors, and design issues. No code changes allowed."
allowed_tools: [Read, Grep, Glob]
prohibited_tools: [Edit, Write, Bash]
system_prompt_additions: "You are a read-only code reviewer. You may read files, search code, and analyze patterns. You cannot edit, create, or modify any file. Report findings with file paths, line numbers, severity, and actionable fix suggestions. Do not attempt to make changes yourself."
default_skills: [code-reviewer]
orchestration:
  can_invoke: []
  parallelizable: true
```

**When to use alone:** Standard PR review, pre-commit checks, architecture review of a single module.
**When to fan-out:** Combine with security-auditor for compliance-critical code, with test-engineer for coverage-gap analysis.

### 2. security-auditor

```yaml
name: security-auditor
description: "Read-only security auditor. Scans for vulnerabilities, insecure patterns, and compliance violations. No code changes allowed."
allowed_tools: [Read, Grep, Glob]
prohibited_tools: [Edit, Write, Bash]
system_prompt_additions: "You are a read-only security auditor. You may read files and search for vulnerabilities. You cannot edit, create, or modify any file. Report findings with CWE identifiers, severity (Critical/High/Medium/Low), exploitability assessment, and remediation guidance. Never attempt to fix vulnerabilities yourself."
default_skills: [security-reviewer]
orchestration:
  can_invoke: []
  parallelizable: true
```

**When to use alone:** Security audit of authentication flows, dependency vulnerability scan, secrets-in-code sweep.
**When to fan-out:** Combine with code-reviewer for secure code review of payment/sensitive-data modules.

### 3. test-engineer

```yaml
name: test-engineer
description: "Test engineer that can write tests but cannot modify source code. Finds coverage gaps and writes missing tests."
allowed_tools: [Read, Grep, Glob, Edit]
prohibited_tools: [Write, Bash]
system_prompt_additions: "You are a test engineer. You may read source code and edit or create test files only. You cannot modify application source code, configuration files, or build scripts. Generate tests that target uncovered paths, edge cases, and regression scenarios. Report coverage gaps even when you cannot write tests for them."
default_skills: [tdd-guide]
orchestration:
  can_invoke: []
  parallelizable: true
```

**When to use alone:** Filling coverage gaps, writing tests for a new feature, regression test generation.
**When to fan-out:** After code-reviewer approves logic — test-engineer writes tests for the approved code.

### 4. web-perf-auditor

```yaml
name: web-perf-auditor
description: "Read-only performance auditor. Analyzes web performance metrics, bundle size, rendering patterns. No code changes allowed."
allowed_tools: [Read, Grep, Glob]
prohibited_tools: [Edit, Write, Bash]
system_prompt_additions: "You are a read-only web performance auditor. You may read files, analyze bundle sizes, inspect rendering patterns, and evaluate Core Web Vitals impact. You cannot edit, create, or modify any file. Report findings with metric targets (LCP, FID, CLS), severity, and non-destructive optimization suggestions."
default_skills: [performance-engineer]
orchestration:
  can_invoke: []
  parallelizable: true
```

**When to use alone:** Performance audit of a page/component, bundle-size analysis, render-path review.
**When to fan-out:** Combine with code-reviewer for performance-sensitive feature review.

---

## <!-- STANDARD: 3min --> Parallel Fan-Out Pattern

The only endorsed multi-persona pattern. No sequential chaining. No persona-to-persona handoffs. No nested delegation.

### Pattern Definition

```
User/Slash Command (Orchestrator)
         │
         ├──► Persona A (parallel) ──► Output A
         ├──► Persona B (parallel) ──► Output B
         └──► Persona C (parallel) ──► Output C
         │
         ▼
    MERGE STEP (Orchestrator)
         │
    ┌────┴────┐
    ▼         ▼
  PASS      FAIL
    │         │
    ▼         ▼
 Deploy    Report + Block
```

### Example: `/ship` Command

```
/ship → spawns [code-reviewer, security-auditor, test-engineer] in parallel
     → await all three outputs
     → merge: de-duplicate findings, normalize severities, produce unified report
     → gate check:
         ├── all pass (no Critical/High findings) → proceed to deploy
         └── any fail → report findings, block deployment, surface actionable fixes
```

### Merge Strategies

| Strategy | When to Use | Merged Output |
|---|---|---|
| **Union (default)** | All findings matter; nothing should be lost | Single report with all findings from all personas, de-duplicated by file+line |
| **Intersection** | Only issues flagged by 2+ personas are worth acting on | Report containing only findings confirmed by multiple personas |
| **Weighted** | Some personas' findings carry more weight | Findings scored by persona authority weight; threshold-based gating |
| **Priority-only** | Merge latency must be minimal; only high-severity matters | Critical + High findings only; Medium/Low archived for later |

### Failure Handling

| Failure Mode | Detection | Response |
|---|---|---|
| **Persona times out** | Orchestrator timeout per persona (default: 120s) | Mark persona as `degraded`; proceed with remaining outputs; flag in merge report: "Incomplete: auditor timed out" |
| **Persona returns malformed output** | Schema validation on persona output | Mark persona as `invalid`; skip merge contribution; log for debugging; do NOT block deployment on unparseable output |
| **All personas fail** | All outputs are degraded/invalid | Halt pipeline. Report: "All auditors failed. Manual review required before deployment." Never auto-pass on total failure. |
| **Merge conflict (contradictory findings)** | Two personas flag same line with opposite severities | Escalate to human. Report both findings with context. Flag as "Needs Human Decision." |

---

## <!-- STANDARD: 3min --> Decision Tree: Single Persona vs. Fan-Out

```
What's the risk profile of this change?
├── Low risk (docs, formatting, comments)
│   └── Single persona or skip audit entirely
├── Medium risk (feature code, refactoring, new tests)
│   └── Single persona (code-reviewer OR security-auditor depending on domain)
├── High risk (auth, payments, PII, data migration, public API)
│   └── Fan-out: code-reviewer + security-auditor (minimum)
└── Critical risk (crypto, compliance, financial settlement, auth infrastructure)
    └── Fan-out: code-reviewer + security-auditor + test-engineer (full suite)
```

```
How many personas can this workflow support?
├── 1 persona → Single invocation (no orchestration needed)
├── 2-3 personas → Parallel fan-out with union merge
├── 4+ personas → Parallel fan-out with priority-only merge (reduce noise)
└── N/A (sequential dependency required) → Redesign workflow. Sequential persona chains are unsupported.
```

---

## <!-- STANDARD: 3min --> Core Workflow

### Step 1: Identify the Trigger

| Trigger | Action |
|---|---|
| User runs `/review` | Route to code-reviewer persona → code-reviewer skill |
| User runs `/audit` | Route to security-auditor persona → security-reviewer skill |
| User runs `/ship` | Fan-out: code-reviewer, security-auditor, test-engineer → merge → gate |
| User runs `/perf` | Route to web-perf-auditor persona → performance-engineer skill |
| User requests multi-audit | Select personas from registry, fan-out, merge |

### Step 2: Select Personas

Match the task to personas from the registry. Prefer the minimum set that provides adequate coverage. Each additional persona costs merge complexity.

### Step 3: Configure Context

Each persona receives independently:
- The task description (what to audit/review/test)
- File scope (which files/directories to examine)
- Severity thresholds (Critical/High/Medium/Low)
- Output schema (what format to return findings in)

### Step 4: Execute Fan-Out

All personas run in parallel with independent timeouts. No persona waits for another. No shared state.

### Step 5: Merge Results

1. Collect all persona outputs
2. Validate schema on each output
3. De-duplicate findings (same file + line + category → merge into one)
4. Normalize severities across personas
5. Resolve conflicts (escalate to human where needed)
6. Produce unified report with pass/fail gate signal

### Step 6: Gate Decision

```
if critical_or_high_findings > 0:
    BLOCK deployment
    Return unified report with actionable fixes
else if medium_findings > threshold:
    WARN but allow deployment
    File medium issues as non-blocking follow-ups
else:
    PASS
    Proceed to deployment
```

---

## <!-- STANDARD: 3min --> Best Practices

| Practice | Rationale |
|---|---|
| **Design merge schema before personas** | Merge is the integration point. Define what the unified report looks like, then define what each persona must produce to feed it. |
| **Timeout every persona independently** | A hung security-auditor should not block the code-reviewer from delivering results. Each persona gets its own deadline. |
| **Normalize severity scales** | One persona's "High" is another's "Medium." Define a canonical severity scale (Critical → High → Medium → Low → Info) and map each persona's output to it during merge. |
| **De-duplicate by file+line+category** | Two personas flagging the same bug on the same line is one finding, not two. Merge on (file_path, line_number, category). |
| **Version persona definitions** | Persona configurations (allowed_tools, system_prompt_additions) change over time. Tag each persona version so audit trails are reproducible. |
| **Test the merge logic independently** | The merge step has its own correctness: de-duplication accuracy, conflict resolution, severity normalization. Test it with synthetic persona outputs before trusting it with real audits. |

---

## <!-- STANDARD: 3min --> Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|---|---|---|
| **Persona A calling Persona B** | Violates the hard constraint. Creates cascading failures, untraceable decisions, and circular dependencies. | Redesign as parallel fan-out from orchestrator. The orchestrator invokes both and merges. |
| **Shared state between personas** | One persona's intermediate state bleeding into another creates non-reproducible results. | Each persona receives its full context independently. No shared files, no shared database, no shared environment variables. |
| **Silent degradation** | A persona fails but the orchestrator proceeds without surfacing the failure in the merge report. | Every persona failure is surfaced in the merge output. "Incomplete" is a valid state; "silent" is not. |
| **Persona with no prohibited_tools** | A persona without explicit prohibitions is just a general-purpose agent with a different prompt. | Every persona must declare prohibited_tools. Read-only personas must have Edit/Write/Bash in prohibited_tools. |
| **Fan-out for trivial changes** | Spinning 3 personas to review a comment change wastes compute, adds latency, and produces empty findings. | Risk-calibrate the persona count. Low-risk changes skip the fan-out entirely. |
| **Merge that just concatenates** | Returning raw persona outputs as a "merged" report offloads integration work to the human. | The merge step must de-duplicate, normalize, prioritize, and gate. If the human has to cross-reference 3 reports, the orchestration failed. |

---

## <!-- STANDARD: 3min --> Production Checklist

Before deploying a persona-orchestrated workflow to production:

- [ ] **Every persona has allowed_tools AND prohibited_tools defined.** No persona is missing either list.
- [ ] **Every persona has can_invoke: [] (empty).** No persona-to-persona invocation paths exist.
- [ ] **Every persona has exactly one default_skill.** No zero-skill or multi-skill defaults.
- [ ] **Parallel fan-out is the only multi-persona pattern.** No sequential chains, nested calls, or handoffs.
- [ ] **Merge strategy is declared and tested.** Union, intersection, weighted, or priority-only — and tested with synthetic outputs.
- [ ] **Timeout per persona is configured.** Default: 120s. Adjusted per persona based on expected scope.
- [ ] **Severity normalization table exists.** Every persona's severity labels are mapped to the canonical scale.
- [ ] **De-duplication logic is tested.** Same finding from two personas produces one merged entry.
- [ ] **Failure modes are handled.** Timeout → degraded, malformed output → invalid, total failure → halt. None are silent.
- [ ] **Gate decision rules are explicit.** Which severities block, which warn, which auto-pass.
- [ ] **Audit trail is preserved.** Persona versions, inputs, outputs, and merge results are logged for reproducibility.

---

## <!-- DEEP: 10+min --> Gotchas

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| Same bug reported 3 times in merged output | De-duplication logic not applied. Each persona independently flags the same issue and merge concatenates raw outputs | Implement de-duplication on (file_path, line_number, category) during merge. Two personas flagging line 42 of auth.ts for SQL injection is one finding | **Merge without de-duplication is not merge.** It's aggregation — and it forces the human to do the actual merge work manually. |
| Persona produces findings outside its domain (code-reviewer flags CSP headers) | Persona's system_prompt_additions don't scope its domain. The persona acts like a general-purpose agent | Add domain scoping to system_prompt_additions: "You are a code reviewer. Report only on code correctness, design, and logic. Do not report on security, performance, or accessibility — those are handled by other auditors." | **A persona without domain boundaries is just noise.** Each persona must know what it owns AND what it explicitly does not own. |
| Orchestrator deadlocks waiting for a hung persona | No per-persona timeout configured. The fan-out blocks indefinitely on the slowest persona | Set independent timeouts per persona. Default 120s. Mark timed-out personas as degraded and proceed with available outputs | **The pipeline is only as fast as its slowest persona.** Timeouts protect throughput; degraded outputs are better than no outputs. |
| Severity mismatch: persona A says High, persona B says Low for same issue | Each persona uses its own severity scale with no normalization during merge | Define canonical scale (Critical/High/Medium/Low/Info). Each persona's output maps to it. During merge, resolve conflicting severities: take the higher severity and flag as "disputed severity" | **Severity is only actionable if it's comparable.** Without normalization, "High" means "this persona cares a lot" not "this is objectively severe." |
| Persona version drift: audit run with persona v1.2 but deployment gate expects v1.3 output format | Persona definitions changed without versioning the output schema. Downstream merge logic breaks on unexpected fields | Version persona output schemas. Merge logic validates schema version and rejects outputs from incompatible versions. Tag persona definitions with semver | **Version everything that reads or writes structured data.** Undocumented schema changes break merge pipelines silently. |
| Fan-out produces findings for files the orchestrator can't act on | Persona was given too broad a scope. It audited the entire repo when only src/auth/ was relevant | Scope each persona's file access explicitly. Pass file paths or glob patterns as part of persona context, not "the whole repo" | **A persona with unbounded scope produces unbounded noise.** Scope is a first-class parameter, not an afterthought. |

---

## <!-- STANDARD: 3min --> Error Recovery

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| Merge output is empty but personas ran successfully | Personas completed but produced no findings — either the code is perfect or the personas didn't understand the scope | Verify persona outputs individually. If all outputs are empty, the scope may be wrong. If some are empty, the code may genuinely pass. Document "zero findings" as a valid result, distinct from "persona failed" | **Zero findings ≠ failure.** Distinguish "audited and found nothing" from "didn't audit correctly." The merge report must surface which personas completed with zero findings vs. which degraded. |
| Human overrides the gate decision and deploys despite blocking findings | Gate rules exist but are advisory, not enforced. Orchestrator recommends blocking but doesn't prevent deployment | Make gate rules enforceable. Block deployment in CI/CD until all Critical+High findings are either resolved or explicitly waived with documented justification | **Advisory gates are gate theater.** If a gate can be bypassed without documentation, it doesn't exist. Require waivers, not overrides. |

---

## <!-- STANDARD: 3min --> Adding New Personas

### Checklist for New Persona Creation

1. **Define the domain:** What does this persona own? What does it explicitly NOT own?
2. **Choose allowed_tools:** Minimum set needed to perform the audit. Read-only by default unless write access is explicitly justified.
3. **Define prohibited_tools:** Everything the persona must not do. Write-capable personas must still prohibit mutation of source code.
4. **Select default_skill:** Exactly one skill from the skills registry. Must already exist as a SKILL.md.
5. **Write system_prompt_additions:** Domain scoping, output format, severity scale, and explicit boundaries.
6. **Set parallelizable: true:** All personas must be independently parallelizable. If the persona depends on another persona's output, redesign it.
7. **Test in isolation:** Run the persona alone against a known test case before adding it to any fan-out pipeline.
8. **Register in merge logic:** Add the persona's output schema to the merge step. Define its severity mapping and de-duplication categories.

### Persona Lifecycle

```
[Proposed] → [Drafted] → [Tested] → [Active] → [Deprecated]
                                │                    │
                                └── [Degraded] ←─────┘
```

| State | Meaning | Transition Trigger |
|---|---|---|
| **Proposed** | Idea submitted, not yet drafted | → Drafted: Persona definition written |
| **Drafted** | Definition exists, not yet tested | → Tested: Passes isolation tests |
| **Tested** | Passes isolation, ready for pipelines | → Active: Added to at least one slash command |
| **Active** | Running in production pipelines | → Degraded: Timeout rate >10% or invalid-output rate >5% |
| **Degraded** | Active but unreliable; flagged for review | → Active: Issues fixed; → Deprecated: Cannot be repaired |
| **Deprecated** | Removed from all pipelines. Retained for audit-trail reference only | Terminal state |

---

## <!-- STANDARD: 3min --> Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `skill-levels` | Level calibration for persona output depth | Before configuring persona system prompts — L2 depth for routine audits, L4 depth for architectural reviews |
| `security-reviewer` | Vulnerability taxonomy, CWE mappings, severity definitions | When defining security-auditor persona boundaries and output schema |
| `code-reviewer` | Bug categories, review checklist, code-quality rubric | When defining code-reviewer persona boundaries and output schema |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `code-reviewer` | Persona context: scope, severity thresholds, output format | Code-reviewer persona produces unfocused output without scoped context |
| `security-reviewer` | Persona context: audit scope, CWE filter, compliance requirements | Security-auditor persona scans wrong surface area or reports irrelevant findings |
| `qa-engineer` | Test-engineer persona configuration: coverage targets, test framework | Test-engineer writes tests for wrong framework or misses target coverage |
| `performance-engineer` | Web-perf-auditor persona configuration: metric targets, bundle thresholds | Web-perf-auditor flags performance issues below actionable threshold |
| `shipping-and-launch` | Gate rules: which severities block deployment, merge strategy | Deployment proceeds without quality gate enforcement |
| `release-manager` | Persona versioning for release audit trails | Release audit trails lose persona version provenance |

---

## <!-- DEEP: 10+min --> Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "We just need one more persona-to-persona call — just this once" | The hard constraint exists to prevent cascading dependencies. One exception becomes the pattern. If Persona A genuinely needs Persona B's output, refactor as parallel fan-out from the orchestrator. |
| "Shared state between personas would make this faster" | Shared state makes results non-reproducible. The orchestrator's isolation guarantee is what makes debugging possible. Speed gain is imaginary — the debugging cost of shared-state bugs exceeds any latency savings. |
| "This persona doesn't need prohibited_tools — it's read-only by convention" | Conventions are violated. Prohibited_tools are enforced. If a persona can write files, it will — either through prompt injection, model error, or future modification. Explicit prohibitions are the only defense. |
| "We can just concatenate persona outputs for now; we'll build merge later" | Concatenation is not merge. It offloads integration onto the human and guarantees inconsistency. The first persona output sets expectations; by the third raw output, the human is pattern-matching manually. Build merge first. |
| "All personas should have the same timeout" | Different personas audit different scopes. A security-auditor scanning 500 files needs more time than a code-reviewer examining 50. Uniform timeouts either starve thorough auditors or let fast ones idle. |

---

## <!-- STANDARD: 3min --> Proactive Triggers

| Trigger | Action | Why |
|---|---|---|
| New domain skill added to registry | Evaluate within 7 days: does this skill need a dedicated persona? If yes, follow "Adding New Personas" checklist | Skills without personas are invisible to orchestration. A new domain skill is a signal that specialized auditing may be needed. |
| Persona timeout rate exceeds 10% | Move persona to Degraded state. Investigate: is scope too broad? Timeout too short? Upstream latency? | Timeout rate above 10% means the persona is unreliable in automated pipelines. Degraded personas produce incomplete merge reports. |
| Third-party tool used by a persona changes its API | Within 48 hours: update persona's system_prompt_additions to reflect new tool capabilities. Test in isolation before re-promoting to Active | Personas that reference outdated tool APIs produce invalid outputs. The persona contract (tools + output schema) must match reality. |
| Merge produces >50 findings per 1000 lines of audited code | Signal-to-noise problem: personas are either too broad in scope or severity thresholds are too low. Recalibrate | Finding fatigue causes humans to ignore merge reports. A healthy pipeline flags 5-15 actionable findings per 1000 lines. |
| New slash command created that doesn't use persona orchestration | Audit within 30 days: should this command use a persona? If the command performs code review, security audit, or testing, it should route through personas | Persona-less commands bypass quality gates. Consistency requires all audit/review commands to use the persona framework. |

---

## What Good Looks Like

A world-class persona orchestration system produces:

- **Reproducible audits:** Same code + same persona versions → same findings. No non-determinism from shared state or persona-to-persona dependencies.
- **Actionable merge reports:** Unified output with de-duplicated findings, normalized severities, and clear pass/fail signals. Human reviews one report, not N.
- **Isolated failures:** A hung security-auditor doesn't block the code-reviewer. A malformed output from test-engineer doesn't corrupt the code-reviewer's findings. Degradation is surfaced, not hidden.
- **Versioned personas:** Every audit run references specific persona versions. Audit trails are reproducible months later.
- **Enforceable gates:** Critical/High findings block deployment. Waivers are documented, not bypassed. Gates are structural, not advisory.
- **Replaceable personas:** Any persona can be swapped for an improved implementation without changing the orchestrator or other personas.
- **Risk-calibrated fan-out:** Low-risk changes get one persona (or none). Critical changes get the full suite. Persona count matches risk profile.

The persona orchestrator doesn't audit code — it makes audits trustworthy. Trust comes from isolation, reproducibility, and clear failure boundaries.

---

## Deliberate Practice

To build persona orchestration instinct:

1. **Audit a simple PR with a single persona, then fan-out with two.** Compare the outputs. Where did the second persona add value? Where did it duplicate? This builds intuition for when fan-out produces signal vs. noise.
2. **Write a merge function by hand.** Take raw outputs from two personas on the same codebase. De-duplicate by hand. Normalize severities. Produce one unified report. Time yourself. This builds respect for merge complexity.
3. **Design a persona from scratch for a domain not covered by the four initial personas.** Write the full YAML definition. Define allowed_tools, prohibited_tools, system_prompt_additions, and default_skill. Have a peer review it against the "Production Checklist."
4. **Break a persona deliberately, then fix it.** Remove prohibited_tools. Run it. Observe what happens. Then remove the timeout. Run it against a large scope. Observe the deadlock. This builds understanding of WHY each constraint exists.
5. **Trace a production incident back to persona configuration.** When a pipeline fails, trace: was it a persona timeout? Merge conflict? Scope misconfiguration? Mapping failures to root causes builds diagnostic instinct.

---

## <!-- STANDARD: 3min --> Anti-Hallucination — Output Integrity Guardrails

Before delivering persona orchestration work, verify:

| Guardrail | Check | Consequence of Violation |
|---|---|---|
| No fabricated tools | Every tool name in `allowed_tools`/`prohibited_tools` is verified against the agent tool registry | Hallucinated tool names prevent personas from starting; the orchestrator produces unusable configurations |
| Severity with evidence | Every Critical/High finding cites specific file+line+pattern with CWE or equivalent tag | Uncited severities are opinions — two reviewers reach opposite conclusions on the same finding |
| Uncertainty tagged | Any claim without 100% certainty is tagged [ESTIMATED] or [LIKELY] with confidence bound | Untagged claims propagate as facts through merge pipelines, producing false confidence |
| Persona boundary respected | Output never recommends persona-to-persona calls, shared state, or sequential chaining | Boundary violations produce cascading failures that are untraceable — the orchestrator's isolation guarantee collapses |
| Version provenance | Every persona definition references a semver tag; audit trails are reproducible | Without versioning, regression investigations cannot determine which persona version introduced a finding pattern |

## <!-- STANDARD: 3min --> Verification Guardrails — Self-Check Before Delivery

Before delivering work, the agent must verify:

- [ ] **Self-check against What Good Looks Like:** All deliverables meet the quality bar defined above
- [ ] **No broken references:** All file paths, URLs, persona names, and skill references resolve correctly
- [ ] **No fabricated personas:** Every persona mentioned exists in the registry with matching YAML — zero hallucinated personas
- [ ] **Anti-hallucination check:** No fabricated APIs, version numbers, tool capabilities, or configuration options asserted
- [ ] **Error Recovery paths exercised:** Every failure mode (timeout, malformed output, total failure) has a documented recovery path
- [ ] **Cross-skill dependencies satisfied:** All upstream skill outputs consumed as documented in the upstream/downstream table

If any checkbox fails, revise before delivering.

## <!-- STANDARD: 3min --> Mechanical Triggers

| Trigger (grep-able phrase) | Action | Why |
|---|---|---|
| `persona timeout` | Run timeout diagnostic: check persona scope width, system load, upstream latency per persona | Timeout thresholds must be calibrated per-persona; uniform 120s timeouts mask real performance divergence |
| `merge conflict: severity mismatch` | Run merge de-duplication with verbose mode to identify contradictory findings across personas | Severity mismatches signal domain overlap or calibration drift between person versions |
| `degraded persona` | Move persona to Degraded lifecycle state; open investigation ticket with timeout/invalid-output rate | Degradation >10% of runs invalidates the gate reliability for any pipeline using that persona |
| `new skill in [domain]` | Evaluate within 7 days: does this skill produce structured findings needing persona isolation? | Skills without personas bypass quality gates; each new domain skill is a persona gap signal |
| `can_invoke: [...]` not empty | BLOCK — persona definitions with non-empty can_invoke violate the hard isolation constraint | Persona-to-persona calls are the #1 source of unreproducible audit results |

## Complete When

| # | Complete when... | Verify |
|---|---|---|
| ☐ | Every persona has `allowed_tools` AND `prohibited_tools` defined with zero empty lists | Audit each persona YAML definition; grep for `prohibited_tools: \[\]` — zero matches |
| ☐ | Every persona has `can_invoke: []` (empty array — no persona-to-persona invocation paths exist) | Grep for `can_invoke.*\[.*\w` across all persona definitions — zero matches |
| ☐ | Every persona has exactly one `default_skill` that references an existing SKILL.md in the filesystem | Cross-reference `default_skill` values against `skills/*/skill-name/SKILL.md` — every path resolves |
| ☐ | All fan-out workflows use parallel execution only — zero sequential chains, nested delegation, or persona-to-persona handoffs | Audit orchestrator code for sync/await patterns between personas; parallel fan-out is the only endorsed multi-persona pattern |
| ☐ | Merge logic de-duplicates on (file_path, line_number, category) — no raw concatenation of persona outputs | Test with synthetic inputs containing same finding from two personas; merged output has exactly one entry |
| ☐ | Every merge report surfaces degraded/invalid personas explicitly in the output — no silent ingestion of failures | Test with one persona configured to time out; merge output includes "⚠ Incomplete: [persona-name] degraded (timeout 120s)" |
| ☐ | Gate rules are enforceable in CI/CD — Critical+High findings block deployment with documented waiver requirement | Test deployment pipeline with simulated Critical finding; CI reports BLOCK, waiver mechanism exists |
| ☐ | Persona output schemas are versioned (semver) and merge logic validates schema version before processing | Test with v1.3 schema passed to v1.2 merge logic; merge rejects with "Schema version mismatch" |

## Gotchas

See the Gotchas section above for detailed failure modes with root causes and fixes.

## Anti-Hallucination
<!-- STANDARD: 3min -->

* Admit uncertainty. If you cannot determine the correct approach, ask — do not guess.
* Flag your knowledge cutoff. If this project uses tools or patterns you have not seen, state your assumptions.
* Never guess security. If work touches auth, payments, or PII, route to security-reviewer.
- [VERIFIED] — Confirmed against official documentation or published standards
- [COMMON-PRACTICE] — Widely used in the industry
- [INFERRED] — Reasonable extrapolation from general principles
- [UNKNOWN] — Requires verification against specific context

## References

Detailed reference material loaded on demand:

- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Persona Registry Schema**: Full JSON Schema for persona definitions
- **Merge Protocol Specification**: De-duplication algorithm, severity normalization tables, conflict resolution rules
