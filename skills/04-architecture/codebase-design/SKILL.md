---
name: codebase-design
description: >
  Use when designing new modules, classes, or packages; when evaluating existing code for refactoring opportunities; when code review reveals shallow modules (large interface, little behavior) or pass-throughs; when planning a codebase reorganization; or when teaching software design principles. Handles deep module design vocabulary (depth, seam, adapter, leverage, locality), the deletion test for module evaluation, interface minimization patterns, seam identification and placement, adapter pattern application, complexity budget allocation, locality analysis, and deep module vs shallow module classification. Do NOT use for system architecture at the service level (route to system-architect), database schema design (route to database-designer), API contract design (route to api-designer), or monorepo structure (route to monorepo-manager).
license: MIT
author: Sandeep Kumar Penchala
type: architecture
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - codebase-design
  - deep-modules
  - software-design
  - deletion-test
  - interface-design
  - module-design
  - refactoring
  - code-organization
token_budget: 4000
chain:
  consumes_from:
    - system-architect
    - code-reviewer
  feeds_into:
    - backend-developer
    - frontend-developer
    - fullstack-developer
    - code-reviewer
  alternatives: []
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
---
# Codebase Design
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.
<!-- QUICK: 30s -->
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



## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---:|
| "It works — the module has 12 public methods but they're all small, so it's fine." | A shallow module with 12 public methods and 15 lines of behavior forces 10 developers to read 12 method signatures every time they touch related code. Hundreds of wasted cognitive cycles. At $150/hour blended rate, a team of 10 loses $15K-$45K annually on a single shallow module. |
| "I'll extract that pass-through module later — right now I need to ship." | A pass-through module that delegates every call without adding behavior still requires: dependency updates, security patches, documentation, tests, onboarding explanation, and code review attention. Over 2 years, maintenance cost exceeds deletion cost by 10-20x. Cost: $10K-$30K in maintenance drag per pass-through. |
| "Adding one more public method won't hurt — someone might need it." | Without active minimization, modules gain 1-2 public methods per quarter. After 2 years, a module that started with 5 methods has 13-21. Each addition seemed harmless at the time. Cumulative depth erosion makes the module progressively harder to understand and change. Cost: $5K-$15K/year in interface creep per ungoverned module. |
| "The seam placement doesn't need analysis — the module boundary feels natural here." | A seam at the wrong abstraction level will be moved within 6-18 months. Moving it requires updating every caller, rewriting tests, updating documentation, retraining the team. For 20+ callers across 5 services: 2-4 weeks of engineering at $12K-$20K per week. Cost: $25K-$75K in refactoring labor per wrong seam. |
| "Keeping related code in separate directories is how it's always been — don't fix what isn't broken." | When related concepts are spread across 5+ directories, new developers spend 2-3 extra weeks building a mental map through painful debugging sessions. For 4 new hires per year at $120K salary: $20K-$50K annually in onboarding overhead from scattered code that should be co-located. |

A vocabulary-driven approach to designing deep modules — units of code where a lot of behavior hides behind a small interface, placed at a clean seam, testable through that interface. Based on John Ousterhout's philosophy: complexity is the enemy, and the best way to fight it is through deep modules.

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|--------------------|--------------------|
| R1 | REFUSE to create shallow modules (large interface, little behavior) | New module has >7 public methods but <50 lines of implementation | Halt. Apply [Interface Minimization](references/interface-minimization.md). If depth still <1.0, decompose into smaller modules. |
| R2 | DETECT pass-through modules using deletion test | Module's public methods contain <3 lines of non-delegation logic AND call exactly one other module per method | Flag as pass-through. Propose removal with [Deletion Test](references/deletion-test.md). |
| R3 | REFUSE to place a seam at the wrong abstraction level | Seam candidate crosses 3+ different abstraction layers OR forces callers to know implementation details | Re-evaluate with [Seam Identification](references/seam-identification.md). Seam must align with natural cohesion boundaries. |
| R4 | DETECT hidden coupling through shared mutable state | Two modules mutate the same global/static state OR share a mutable config object | Extract state into a single owning module. Apply [Locality Analysis](references/locality-analysis.md). |
| R5 | REFUSE to skip interface minimization step | New module declared without first enumerating public surface and justifying each method | Pause. Run [Interface Minimization](references/interface-minimization.md) — every public method must earn its place. |
| R6 | DETECT when locality is violated (related code scattered) | Three or more files in different directories change together in >80% of commits touching any one of them | Co-locate scattered code. Apply [Locality Analysis](references/locality-analysis.md) — compute spatial distance. |
| R7 | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| R8 | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset
<!-- STANDARD: 3min -->

Masters of codebase design don't think in terms of "clean code" or "SOLID" alone. They think in terms of **depth**: the ratio of behavior provided to interface cost. A deep module does a lot with a little — think of the `fopen()` call in C: one function that handles disk I/O, buffering, encoding, permissions, and error reporting. Its interface is one function; its behavior spans thousands of lines of kernel and driver code.

Shallow modules are the enemy. They cost as much to learn and maintain as deep ones but deliver almost nothing — pass-through methods, trivial getters, configuration wrappers that just shuffle data. Every shallow module is a tax on every developer who reads the codebase. The master's goal: maximize the depth of every module in the system.

The expert also thinks in terms of **seams**: places where one module can be separated from another. A good seam is where behavior changes independently, where testing boundaries naturally form, and where the adaptation cost is low. Placing a seam badly — slicing through the middle of a cohesive concept — forces downstream consumers to reconstruct the whole from scattered fragments.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Over-abstraction bias** — extracting a module for a pattern that "might be useful" rather than a proven seam | Apply the deletion test: if you can't name three concrete callers, don't create it. |
| **Completeness bias** — feeling every field needs a public getter/setter | Start with zero public methods. Add only what callers actually need. Default to private. |
| **Symmetry bias** — making Module A's interface mirror Module B's because they "feel" related | Design each interface independently. Symmetry is a smell, not a goal. |
| **Future-proofing bias** — adding parameters, hooks, or extension points "just in case" | YAGNI applied ruthlessly. Add extension points only when the second caller arrives. |
| **Co-location inertia** — keeping related code apart because "that's how it's always been" | Run locality analysis quarterly. Co-locate code that changes together. |

## Operating at Different Levels
<!-- STANDARD: 3min -->

| Level | Scope | Actions |
|-------|-------|---------|
| **L1 — Single Module** | One class, file, or small package (~50-500 LOC) | Classify depth, minimize interface, run deletion test, verify locality within module. |
| **L2 — Module Group** | 3-15 modules with high co-change frequency | Identify seams between modules, place adapters, analyze coupling graph, consolidate pass-throughs. |
| **L3 — Package/Domain** | 5-50 modules forming a bounded context or package | Reorganize by locality score, establish interface contracts at domain boundaries, apply anti-corruption layers. |
| **L4 — Codebase-wide** | Entire repository or monorepo | Complexity budget allocation, depth scoring across all modules, architectural seam validation, locality heatmap generation. |

## When to Use
<!-- STANDARD: 3min -->

Use this skill when:
- Designing a new module and want it to be deep from day one
- Evaluating an existing module for refactoring (is it shallow? where's the real behavior?)
- Code review reveals a module with many public methods but thin implementation
- Planning a codebase reorganization around natural seams
- Teaching team members how to think about module depth
- Deciding whether to merge, split, or delete a module
- Assessing a pull request for interface bloat

**Do NOT use this skill for:**
- System-level architecture decisions (services, deployments, networks) — route to **system-architect**
- Database schema design (tables, indexes, normalization) — route to **database-designer**
- API contract design (REST, GraphQL, gRPC endpoints) — route to **api-designer**
- Monorepo tooling and workspace structure — route to **monorepo-manager**
- Build system or dependency graph optimization

## Route the Request
<!-- STANDARD: 3min -->


## Auto-Route by Artifacts (Check Filesystem First)
<!-- STANDARD: 3min -->

| # | Condition | Action |
|---|-----------|--------|
| A1 | File contains `class`/`struct`/`interface` with >10 public methods and <100 lines of logic | Shallow module detected. Jump to **Core Workflow** — Phase 1 (Module Inventory). |
| A2 | Multiple files in different directories change together in >80% of recent commits | Locality violation. Jump to **Decision Trees** — Refactoring Priority Matrix. |
| A3 | File contains pass-through pattern: method bodies are single delegation calls | Pass-through detected. Jump to **Core Workflow** — Phase 5 (Deletion Test). |
| A4 | New file added with `public` methods but no callers yet | Premature interface. Jump to **Decision Trees** — Interface Minimization Strategy. |
| A5 | Configuration class with >20 fields and individual getters | Trivial wrapper. Jump to **Core Workflow** — Phase 2 (Interface Minimization). |


## Intent Route (Ask the User)
<!-- STANDARD: 3min -->

```
What are you trying to do?
├── DESIGN a new module
│   ├── From scratch → Start at "Decision Trees > Module Depth Classification"
│   ├── Extracting from existing code → Start at "Core Workflow — Phase 3 (Seam Identification)"
│   └── Wrapping an external dependency → Start at "Decision Trees > Adapter Pattern Selection"
├── EVALUATE existing code
│   ├── Is this module shallow? → Jump to "Core Workflow — Phase 1 (Module Inventory)"
│   ├── Should I delete this module? → Jump to "Core Workflow — Phase 5 (Deletion Test)"
│   └── Is this interface too big? → Jump to "Decision Trees > Interface Minimization Strategy"
├── REORGANIZE codebase
│   ├── Move files between directories → Start at "Core Workflow — Phase 3 (Seam Identification)"
│   ├── Consolidate scattered logic → Jump to "Decision Trees — Refactoring Priority Matrix"
│   └── Split a too-large module → Start at "Decision Trees > Module Depth Classification"
└── TEACH / EXPLAIN
    ├── Deep module principles → Read [Depth Vocabulary](references/depth-vocabulary.md)
    ├── Deletion test technique → Read [Deletion Test](references/deletion-test.md)
    └── Adapter patterns → Read [Adapter Patterns](references/adapter-patterns.md)
```

## Core Workflow
<!-- STANDARD: 3min -->

**(STANDARD)**

<!-- Full 177 lines extracted to references/core-workflow.md -->

DESIGN → MINIMIZE → SEAM → ADAPT → VERIFY
   ↑___________________________________|
              (iterate)


## Phase 1: Module Inventory
<!-- STANDARD: 3min -->
...
> 📎 **[references/core-workflow.md](references/core-workflow.md)** — 177 lines of detailed guidance

## Decision Trees
<!-- STANDARD: 3min -->

**(QUICK)**

### Decision Tree 4: How Do I Apply the Deletion Test?

        ┌── INPUT: Module or class under evaluation
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
Delete the         Delete one         Delete all
entire module      public method      internal state
   │                 │                  │
   ▼                 ▼                  ▼
Does anything      Does any caller    Does any method
break that can't   break that can't   break that can't
be fixed in <1hr?  be fixed in <30min? be fixed in <15min?
   │                 │                  │
   ▼                 ▼                  ▼
YES: Module is     YES: Method is     YES: State is
essential. Keep.   essential. Keep.   essential. Keep.
   │                 │                  │
   ▼                 ▼                  ▼
NO: Module is      NO: Delete method. NO: Delete state.
dead code. Remove. Reduce interface.  Simplify internals.

### Decision Tree 5: How Do I Allocate Complexity Budget?

        ┌── INPUT: New feature requires complexity trade-off
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
Complexity in      Complexity in      Complexity in
interface          implementation     dependencies
(exposed API)      (internal logic)   (external coupling)
   │                 │                  │
   ▼                 ▼                  ▼
Worst place.       Acceptable if      Moderate risk.
Every caller       hidden behind      Prefer zero-cost
pays its cost      simple interface   abstractions.
forever.
   │                 │                  │
   ▼                 ▼                  ▼
REDUCE:            MONITOR:           QUESTION:
Can you make the   Does depth justify  Can you inline,
surface smaller?   the complexity?     vendor, or remove?

### Decision Tree 6: How Do I Place a Seam Between Modules?

        ┌── INPUT: Two modules need a boundary decision
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
Modules change      Modules have       Modules share
at different rates  different owners   tight coupling
   │                 │                  │
   ▼                 ▼                  ▼
Strong seam:        Strong seam:       Weak seam:
split now.          split by team.     keep together
Natural boundary.   Conway's Law.      or refactor first.
   │                 │                  │
   ▼                 ▼                  ▼
Use adapter         Use API contract   Inline and
pattern at          with versioning    redesign before
the seam            at the seam        extracting


## Module Depth Classification
<!-- STANDARD: 3min -->

```
Module under evaluation
│
├── Public methods ≤ 3 AND behavior lines > 100?
│   └── YES → DEEP (depth > 30). Likely a well-designed abstraction.
│
├── Public methods 4-7 AND behavior lines > 50?
│   └── YES → DEEP (depth 7-12). Solid module. Consider if further minimization possible.
│
├── Public methods ≤ 7 AND behavior lines 20-50?
│   └── YES → MODERATE (depth 3-7). Acceptable. Monitor for interface growth.
│
├── Public methods > 7 AND behavior lines < 100?
│   └── YES → SHALLOW (depth < 14). Run interface minimization.
│
├── Public methods > 10 AND behavior lines < 50?
│   └── YES → CRITICALLY SHALLOW. Immediate refactor or decompose.
│
└── Public methods = 0 AND behavior lines > 0?
    └── Impossible. A module with behavior must expose it. Re-check measurement.
```


## Interface Minimization Strategy
<!-- STANDARD: 3min -->

```
Module with N public methods
│
├── N ≤ 3?
│   ├── All methods called by external code?
│   │   └── YES → Interface is minimal. Move on.
│   └── Some uncalled?
│       └── Make private. Re-measure N.
│
├── 4 ≤ N ≤ 7?
│   ├── Can 2+ methods be combined?
│   │   └── YES → Merge. Use parameter objects, default values, or builder pattern.
│   ├── Are there getters/setters for internal state?
│   │   └── YES → Remove. If callers need state, expose a behavior method instead.
│   └── Are there "convenience" overloads?
│       └── YES → Keep one. Delete others. Add default parameters.
│
└── N > 7?
    ├── Immediate red flag.
    ├── Group methods by caller persona. Can the module split along persona lines?
    └── Apply deletion test to each method group. Keep only essential groups.
```


## Seam Placement Decision
<!-- STANDARD: 3min -->

```
Candidate boundary between Module A and Module B
│
├── Do A and B change at different rates?
│   └── NO → Artificial seam. Do not split. Score: 0/6.
│
├── Can A be tested without B?
│   └── NO → They're tightly coupled. Merge or refactor before seaming.
│
├── Do they have different performance profiles?
│   └── YES → Seam here enables independent optimization.
│
├── Do they serve different caller types?
│   └── YES → Seam here enables different interface styles.
│
├── Can B be swapped without changing A?
│   └── YES → Natural seam. Add adapter here.
│
└── Score < 4?
    └── Reconsider. Merging A and B may be better than forcing a seam.
```


## Adapter Pattern Selection
<!-- STANDARD: 3min -->

```
Seam characteristics → Adapter type
│
├── A and B use different data formats or protocols?
│   └── Translation Adapter
│       Example: A uses XML, B expects JSON. Adapter translates.
│
├── B is a complex subsystem with 10+ entry points but A only needs 2-3?
│   └── Facade
│       Example: A needs to send email. B is full SMTP library. Facade exposes send().
│
├── B is an external system / legacy code / third-party that could change?
│   └── Anti-Corruption Layer
│       Example: B is a vendor API. ACL insulates A from B's version changes.
│
├── A needs to work with multiple implementations of B's interface?
│   └── Bridge
│       Example: A needs storage. B could be S3, local FS, or in-memory. Bridge abstracts.
│
└── A and B share the same domain model but different packaging?
    └── No adapter needed. Just import. If packaging is the only difference, refactor packaging.
```


## Refactoring Priority Matrix
<!-- STANDARD: 3min -->

```
Priority = (CouplingDamage × ChangeFrequency) / RefactoringCost

HIGH PRIORITY (score > 10)
├── Shallow modules with 10+ callers
├── Pass-through modules in hot code paths
├── Locality violations spanning 5+ directories
└── Modules with depth < 0.5 and weekly changes

MEDIUM PRIORITY (score 5-10)
├── Shallow modules with 3-9 callers
├── Artificial seams that break test isolation
├── Interface bloat in moderately-used modules
└── Modules with depth 0.5-1.0 and monthly changes

LOW PRIORITY (score < 5)
├── Shallow modules with 1-2 callers
├── Minor locality violations (2-3 files)
├── Interface cruft in rarely-used modules
└── Modules with depth 1.0-2.0 (acceptable)

IGNORE
├── Deep modules (depth > 3.0) — don't touch what works
├── Stable, unchanging shallow wrappers — not worth the disruption
└── Generated code — depth analysis doesn't apply
```

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Best Practices
<!-- STANDARD: 3min -->

1. **Design deep modules from day one — don't refactor into depth later.** A module with 3 public methods and 150 lines of behavior is easier to maintain than one with 12 public methods and 15 lines of behavior. Write the implementation first, then extract the minimal interface. The interface is a cost to every caller; the implementation is a benefit to every caller. Maximize the benefit/cost ratio before the first commit.

2. **Run the deletion test on every module before it ships.** For every file or class, ask: "If I delete this, what breaks in production?" If the answer is "nothing," delete it now. If the answer is "one call site that could easily inline the 3 lines," delete it and inline. Only keep modules that earn their existence through nontrivial behavior depended on by multiple callers.

3. **Place seams at natural change boundaries, not at arbitrary layers.** A seam between two modules that always change together is an artificial seam — it adds complexity without benefit. Identify where change rates differ: domain logic changes weekly, persistence format changes annually, UI changes monthly. Those are natural seams. Score every seam boundary: co-change frequency, test isolation, caller independence, swappability. Minimum score of 4/6 before creating an adapter.

4. **Minimize interfaces relentlessly — every public method is a liability.** A method left public "just in case" will be called. Once called, removing it requires coordination across every caller. Default to private. Make something public only when: (a) an external caller needs it now, (b) the behavior is nontrivial (not a getter/setter), and (c) making it public doesn't expose internal state that could be corrupted. If all three aren't satisfied, keep it private.

5. **Use adapters at every external dependency boundary.** Third-party libraries, vendor APIs, legacy systems — these change on their schedule, not yours. An anti-corruption layer (ACL) translates their model to your model, so when they change, only the ACL changes. Without an ACL, a vendor API deprecation becomes a codebase-wide refactoring affecting every file that imports their types.

6. **Allocate a complexity budget and enforce it.** Not every module can be deep — some must be thin (controllers, DTOs, configuration). Define what percentage of modules are allowed to be shallow. Track it. When the shallow module count exceeds budget, refactor or consolidate. A codebase with 40% shallow modules is a codebase where most developer time is spent navigating indirection, not understanding behavior.

7. **Maximize locality — code that changes together should live together.** Run `git log --name-only` over the last 90 days. Files that appear together in the same commits should be in the same directory. Files that co-change but span 3+ directory levels are locality violations. Each violation costs every developer 30-60 seconds of context-switching per visit. At 20 visits per developer per month, a single violation costs 2+ hours per developer per year.

8. **Pass-through methods are code smell — delete or inline them.** A method whose body is a single delegation call (`return this.dependency.doX(args)`) adds no behavior. It exists only because the caller doesn't know about the dependency. Either: (a) make the dependency directly accessible to the caller, or (b) add real behavior (validation, transformation, error handling, logging) that justifies the delegation. A pass-through that survives 6 months will never be deleted.

9. **Measure depth, not lines of code.** A 500-line class with 3 public methods (depth ~167) is better designed than a 100-line class with 15 public methods (depth ~7). LOC tells you volume. Depth tells you design quality. Track depth per module over time. If depth is declining, the module is accumulating interface cost faster than behavioral value — it's rotting.

10. **Never add a public method "for future use."** YAGNI applies doubly to interfaces. A public method added speculatively costs every future reader the cognitive load of understanding it, every future maintainer the risk of breaking callers when changing it, and every newcomer the confusion of "who calls this and why?" Add public methods only when a real caller exists, and only the methods that caller actually needs.

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

| Direction | Skill | What's Exchanged | Decision Gate |
|-----------|-------|------------------|---------------|
| **Upstream** | system-architect | Component boundaries, bounded contexts, architecture decision records | ADR must define component seam before codebase-design refines module boundaries within the component |
| **Upstream** | code-reviewer | Code review flags for shallow modules, pass-through detection | Review flags trigger codebase-design evaluation — confirm or dismiss with depth analysis |
| **Downstream** | backend-developer | Deep module designs with minimized interfaces, adapter specifications | Backend dev implements the designed interfaces — do not add public methods without revisiting codebase-design |
| **Downstream** | frontend-developer | Module interface contracts, adapter patterns for API consumption | Frontend dev uses the designed facades — report back if interface is insufficient |
| **Downstream** | fullstack-developer | End-to-end module designs spanning frontend and backend | Fullstack dev validates that designed seams work across the stack |
| **Downstream** | code-reviewer | Depth scorecards for review context, deletion test results | Reviewer checks new code against established depth standards |

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `system-architect` | System design, C4 models, ADRs, scalability patterns | Before making architectural decisions that impact multiple systems |

## Proactive Triggers
<!-- STANDARD: 3min -->

| # | Trigger Condition | Auto-Response |
|---|-------------------|---------------|
| T1 | User opens a file with >15 public methods | "This module has high interface cost. Run depth analysis? [Y/n]" |
| T2 | User creates a new file with `public` keyword | "Before adding public methods, have you defined the module's depth target?" |
| T3 | User writes a method body that is a single delegation call | "This looks like a pass-through. Does this method add behavior, or can callers use the dependency directly?" |
| T4 | User adds a getter/setter pair | "Getters/setters expose implementation. Is there a behavior method that would serve callers better?" |
| T5 | User creates a module in a new directory | "Is this directory a natural seam, or does this module belong with its co-changing peers?" |
| T6 | User imports from 5+ different packages in one file | "High fan-in detected. This module may have low locality. Consider splitting or consolidating dependencies." |
| T7 | Git diff shows 3+ files in different directories changing together | "Locality alert: these files co-change but live apart. Should they be co-located?" |

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.


## How the State Log Works
<!-- STANDARD: 3min -->
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:

   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "codebase-design",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }

   ```

3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.


## State Log Schema
<!-- STANDARD: 3min -->

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |


## Anti-Drift Check
<!-- STANDARD: 3min -->
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## What Good Looks Like
<!-- STANDARD: 3min -->

```

BEFORE (Shallow Module)                    AFTER (Deep Module)
┌─────────────────────┐                   ┌─────────────────────┐
│ UserService          │                   │ UserService          │
├─────────────────────┤                   ├─────────────────────┤
│ + getId(): string    │                   │ + register(email,     │
│ + getName(): string  │  Interface: 12   │     password): User   │
│ + getEmail(): string │  Behavior:  15   │ + authenticate(       │
│ + setId(id)          │  Depth:    ~1.2  │     email, password)  │
│ + setName(name)      │  ⚠ SHALLOW      │ + deactivate(userId)  │
│ + setEmail(email)    │                   │                       │
│ + save()             │                   │ Interface: 3          │
│ + delete()           │                   │ Behavior:  120+      │
│ + validate()         │                   │ Depth:    ~40        │
│ + toJson()           │                   │ ✅ DEEP              │
│ + fromJson(json)     │                   └─────────────────────┘
│ + notifyEmailChange()│
└─────────────────────┘

Metrics improvement:
  Interface cost:  12 → 3  (75% reduction)
  Behavior:        15 → 120 (8x increase — moved logic from callers into module)
  Depth:           1.2 → 40 (33x improvement)
  Caller LoC:      ~200 → ~30 (behavior consolidated into the module)

```

## Deliberate Practice
<!-- STANDARD: 3min -->


## Exercise 1: Depth Scoring (15 min)
<!-- STANDARD: 3min -->
Take any module in your current codebase. Count its public methods. Count its lines of actual behavior (not delegation, not getters/setters). Compute depth. Classify it. If shallow, identify the 3 most important changes to increase depth. Timebox: 15 minutes.


## Exercise 2: Deletion Test Sprint (20 min)
<!-- STANDARD: 3min -->
Take a package or directory. Run the deletion test on every file in it. For each file, answer: "If I delete this, what breaks?" Create a list: files to delete, files to keep, files to refactor. Timebox: 20 minutes.


## Exercise 3: Interface Minimization Kata (25 min)
<!-- STANDARD: 3min -->
Choose a module with 8+ public methods. Apply Phase 2's three questions to every method. Combine, hide, or delete until the interface is ≤5 methods. Re-compute depth. Compare before/after. Timebox: 25 minutes.


## Exercise 4: Seam Mapping (20 min)
<!-- STANDARD: 3min -->
Pick a feature that spans 3+ files. Draw the dependency graph. Identify where changes propagate. Score each boundary using the seam checklist. Mark natural seams. Propose adapter placements. Timebox: 20 minutes.


## Exercise 5: Locality Heatmap (30 min)
<!-- STANDARD: 3min -->
Run `git log --name-only` on your repo for the last 50 commits. Group files that co-change. For each group, compute spatial distance (directory tree distance). Identify files with high co-change frequency but high spatial distance — these are locality violations. Propose a reorganization. Timebox: 30 minutes.

## Anti-Patterns
<!-- STANDARD: 3min -->

**Total cost: $15,000-$45,000 in developer productivity per year.** A shallow module with 12 public methods and 15 lines of behavior forces 10 developers to read 12 method signatures every time they touch related code. Over a year, that's hundreds of wasted cognitive cycles. Each wasted minute compounds: reading the interface, tracing to the implementation, discovering there's nothing there, and going back. At $150/hour blended rate, a team of 10 loses $15K-$45K annually on a single shallow module.

**Total cost: $25,000-$75,000 in refactoring labor per wrong seam.** Placing a seam at the wrong abstraction level means it will be moved within 6-18 months. Moving a seam requires updating every caller, rewriting tests, updating documentation, and retraining the team. For a module with 20+ callers across 5 services, that's 2-4 weeks of engineering effort at $12K-$20K per week, plus cascading integration issues.

**Total cost: $30,000-$100,000 in ripple-effect debugging per year.** Tight coupling through shared mutable state means a bug in Module A manifests as a failure in Module D, three layers away. The debugging cost explodes: developers must understand the full chain, reproduce the exact state mutation order, and fix without breaking Modules B and C. Each incident costs 4-16 hours of senior engineer time. At 2 incidents per month, that's $30K-$100K annually.

**Total cost: $10,000-$30,000 in maintenance drag per pass-through module.** A pass-through module that delegates every call to a dependency without adding behavior still requires: dependency updates, security patches, documentation, tests, onboarding explanation, and code review attention. Over 2 years, the accumulated maintenance cost of keeping it around exceeds the one-time cost of deleting it by 10-20x.

**Total cost: $20,000-$50,000 in onboarding overhead per scattered module group.** When related concepts are spread across 5+ directories, new developers spend 2-3 extra weeks building a mental map. They discover connections through painful debugging sessions, not through reading coherent code. At a $120K salary, that's $5K-$8K per new hire. For a team that onboards 4 developers per year, that's $20K-$50K annually.

**Total cost: $5,000-$15,000 in interface creep per ungoverned module per year.** Without active minimization, modules gain 1-2 public methods per quarter. After 2 years, a module that started with 5 methods has 13-21. Each addition seemed harmless at the time, but the cumulative depth erosion makes the module progressively harder to understand and change.

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Deep module classified incorrectly, leading to wrong abstraction boundaries | $100K-$500K in rewrites from wrong abstraction boundaries | Apply the deletion test: if removing the module's interface breaks nothing, it's shallow. Score depth before committing to interface |
| Interface creep without governance — public methods accumulate unchecked | $50K-$200K per year in maintenance drag from bloated module APIs | Implement interface minimization reviews every quarter. Cap public methods at N per module. Document seam placement rationale |
| Pass-through modules kept alive instead of deleted | $30K-$100K per year in avoidable testing and dependency update costs | Apply the deletion test quarterly. If a module only delegates without adding behavior, delete it and let consumers call the dependency directly |
| Module locality violations causing circular dependencies | $200K-$500K in refactoring costs to untangle cyclic module graphs | Enforce strict dependency direction with architecture tests. Use dependency-cruiser or similar to fail CI on cycles |

## Verification
<!-- STANDARD: 3min -->

| # | Complete when... | Verify |
|---|-----------------|--------|
| ☐ | Complete when Depth scorecard generated for every module in scope — zero modules with depth < 0.5 without documented justification | `grep -rn "public " src/ | wc -l`; compute depth = behavior_lines / public_methods per module |
| ☐ | Complete when Deletion test run on all modules — every surviving module has at least one production caller with nontrivial dependency | For each module, verify at least one production caller exists; document any intentional pass-throughs |
| ☐ | Complete when Pass-through methods identified and resolved: each delegation-only method either inlined, enriched with behavior, or documented as intentional facade | `grep -rn "return .*\." src/ | grep -v "return this"` produces zero delegation-only methods |
| ☐ | Complete when All seams scored ≥4/6 on the seam checklist (co-change frequency, test isolation, caller independence, swappability, different change rates, different caller types) | Seam scorecard documented for every adapter boundary with scores per criterion |
| ☐ | Complete when Anti-corruption layers (ACLs) in place for every third-party dependency, external API, and legacy system integration | No direct vendor imports outside designated ACL modules; lint rule catches violations |
| ☐ | Complete when Interface minimization complete: every public method justified by an actual external caller, convenience overloads removed, getters/setters exposing internal state eliminated | No module has >7 public methods for core business logic; every method has a named production caller |
| ☐ | Complete when Complexity budget defined and enforced: ≤20% shallow modules for core domain, ≤10% for supporting, ≤5% for generic subdomains | Module inventory classifies all modules as Deep/Moderate/Shallow/Critically Shallow with refactoring priority scores |
| ☐ | Complete when Locality heatmap generated from last 90 days of git history — zero files with high co-change frequency spanning >2 directory levels | `git log --since="90 days ago" --name-only --oneline | sort | uniq -c | sort -rn` produces no cross-directory clusters |
| ☐ | Complete when Adapter type correctly selected per seam (Translation, Facade, ACL, or Bridge) — no adapter-less seam at external dependency boundaries | Each adapter boundary has a documented adapter type and rationale matching the seam checklist score |
| ☐ | Complete when No module has gained >2 public methods per quarter without corresponding behavior growth — depth trend is stable or improving | Track depth in CI; alert when depth drops >20% quarter-over-quarter |

## Verification Guardrails
<!-- STANDARD: 3min -->

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## Production Checklist
<!-- STANDARD: 3min -->

**(STANDARD)**

- [ ] **[CD1]** Depth scorecard generated for every module in scope — zero modules with depth < 0.5 without documented justification
- [ ] **[CD2]** Deletion test run on all modules — every surviving module has at least one production caller with nontrivial dependency
- [ ] **[CD3]** Pass-through methods identified and resolved: each delegation-only method either inlined, enriched with behavior, or documented as intentional facade
- [ ] **[CD4]** All seams scored ≥4/6 on the seam checklist (co-change frequency, test isolation, caller independence, swappability, different change rates, different caller types)
- [ ] **[CD5]** Anti-corruption layers (ACLs) in place for every third-party dependency, external API, and legacy system integration
- [ ] **[CD6]** Interface minimization complete: every public method justified by an actual external caller, convenience overloads removed, getters/setters exposing internal state eliminated
- [ ] **[CD7]** Complexity budget defined and enforced: ≤20% shallow modules for core domain, ≤10% for supporting, ≤5% for generic subdomains
- [ ] **[CD8]** Locality heatmap generated from last 90 days of git history — zero files with high co-change frequency spanning >2 directory levels without documented rationale
- [ ] **[CD9]** Adapter type correctly selected per seam (Translation, Facade, ACL, or Bridge) — no adapter-less seam at external dependency boundaries
- [ ] **[CD10]** Module inventory documented with depth classifications (Deep, Moderate, Shallow, Critically Shallow) and refactoring priority scores
- [ ] **[CD11]** No module has >7 public methods for core business logic — controllers/DTOs/configuration exempt with documented boundary
- [ ] **[CD12]** Complexity budget trend monitored: depth scores not declining quarter-over-quarter, shallow module count not increasing

## Error Decoder — War Stories from the Trenches
<!-- STANDARD: 3min -->

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|----------|-----------|------|------------|
| Module has 15+ public methods, each 1-3 lines of delegation | Developer added methods "just in case" or for future use. Each method seemed harmless individually, but the accumulated interface cost makes the module impossible to understand | Run interface minimization: group methods by caller, combine related methods, make uncalled methods private, delete pass-throughs. Target: ≤5 public methods | Gate in code review: every new public method requires a named production caller. "Future use" methods → rejected |
| Two modules always change together in the same commits | An artificial seam was placed where no natural change boundary exists. The seam adds indirection without enabling independent evolution | Merge the modules. Score the seam: if co-change frequency is >80%, the seam is artificial. Combine into a single module, then re-evaluate for a better seam | Before creating a seam, run `git log --follow` on both sides. If they change together >80% of the time, don't separate them |
| Bug fix in Module A breaks Module D three layers away | Tight coupling through shared mutable state. Module A modified state that D depends on, with no contract or validation layer between them | Insert an anti-corruption layer between A and the shared state. Make state immutable or access-controlled. Add integration tests at every layer boundary | Every cross-module state access must go through a defined interface. Direct state mutation across module boundaries is a compile-time or lint error |
| New hire takes 3 weeks to understand how 5 related files connect | Locality violation — files that conceptually belong together are scattered across the directory tree | Run locality heatmap on git history. Group co-changing files into the same directory. Create a package-level README explaining the domain concept and how files relate | Locality heatmap as CI check: files with high co-change frequency must be within 1 directory level of each other |
| Refactoring a vendor API integration requires changes in 20+ files | No anti-corruption layer. The vendor's types, method names, and error models are imported directly across the codebase | Create an ACL: define your own domain types, translate vendor responses at the boundary, expose only the 3-5 methods callers actually need. Vendor changes now only affect the ACL | Every third-party import must go through a single adapter module. Direct vendor imports outside the ACL are lint errors |
| Module depth declining: was 8.0 six months ago, now 1.5 | Interface creep — 1-2 public methods added per quarter without corresponding behavior growth. Each addition seemed harmless | Freeze the interface. Audit every public method: who calls it, what behavior does it add? Remove convenience methods, inline pass-throughs, merge thin methods | Track depth in CI. Alert when depth drops >20% quarter-over-quarter. Require architecture review for modules that cross the shallow threshold (depth < 1.0) |

## References
<!-- STANDARD: 3min -->

- [Depth Vocabulary](references/depth-vocabulary.md) — Definitions: depth, shallow module, deep module, interface cost, behavior value, seam, leverage, locality
- [Deletion Test](references/deletion-test.md) — Step-by-step deletion test protocol with pass-through and trivial wrapper examples
- [Seam Identification](references/seam-identification.md) — Finding natural seams: extension points, test boundaries, config boundaries, rate-of-change boundaries
- [Adapter Patterns](references/adapter-patterns.md) — Adapter catalog: translation adapter, facade, anti-corruption layer, bridge, when to use each
- [Leverage Calculation](references/leverage-calculation.md) — Measuring leverage: caller count, benefit per caller, maintenance cost, depth vs leverage trade-off
- [Locality Analysis](references/locality-analysis.md) — Locality score: co-change frequency, spatial distance, conceptual distance, co-location decision framework
- [Shallow Module Detection](references/shallow-module-detection.md) — Detection patterns: pass-through, trivial wrapper, config pass-through, excessive getters/setters, god class
- [Interface Minimization](references/interface-minimization.md) — Techniques: combine methods, default parameters, narrow return types, hide implementation classes, method justification checklist
