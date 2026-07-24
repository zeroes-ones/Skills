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

A vocabulary-driven approach to designing deep modules — units of code where a lot of behavior hides behind a small interface, placed at a clean seam, testable through that interface. Based on John Ousterhout's philosophy: complexity is the enemy, and the best way to fight it is through deep modules.

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|--------------------|--------------------|
| R1 | REFUSE to create shallow modules (large interface, little behavior) | New module has >7 public methods but <50 lines of implementation | Halt. Apply [Interface Minimization](references/interface-minimization.md). If depth still <1.0, decompose into smaller modules. |
| R2 | DETECT pass-through modules using deletion test | Module's public methods contain <3 lines of non-delegation logic AND call exactly one other module per method | Flag as pass-through. Propose removal with [Deletion Test](references/deletion-test.md). |
| R3 | REFUSE to place a seam at the wrong abstraction level | Seam candidate crosses 3+ different abstraction layers OR forces callers to know implementation details | Re-evaluate with [Seam Identification](references/seam-identification.md). Seam must align with natural cohesion boundaries. |
| R4 | DETECT hidden coupling through shared mutable state | Two modules mutate the same global/static state OR share a mutable config object | Extract state into a single owning module. Apply [Locality Analysis](references/locality-analysis.md). |
| R5 | REFUSE to skip interface minimization step | New module declared without first enumerating public surface and justifying each method | Pause. Run [Interface Minimization](references/interface-minimization.md) — every public method must earn its place. |
| R6 | DETECT when locality is violated (related code scattered) | Three or more files in different directories change together in >80% of commits touching any one of them | Co-locate scattered code. Apply [Locality Analysis](references/locality-analysis.md) — compute spatial distance. |

## The Expert's Mindset

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

| Level | Scope | Actions |
|-------|-------|---------|
| **L1 — Single Module** | One class, file, or small package (~50-500 LOC) | Classify depth, minimize interface, run deletion test, verify locality within module. |
| **L2 — Module Group** | 3-15 modules with high co-change frequency | Identify seams between modules, place adapters, analyze coupling graph, consolidate pass-throughs. |
| **L3 — Package/Domain** | 5-50 modules forming a bounded context or package | Reorganize by locality score, establish interface contracts at domain boundaries, apply anti-corruption layers. |
| **L4 — Codebase-wide** | Entire repository or monorepo | Complexity budget allocation, depth scoring across all modules, architectural seam validation, locality heatmap generation. |

## When to Use

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

### Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | File contains `class`/`struct`/`interface` with >10 public methods and <100 lines of logic | Shallow module detected. Jump to **Core Workflow** — Phase 1 (Module Inventory). |
| A2 | Multiple files in different directories change together in >80% of recent commits | Locality violation. Jump to **Decision Trees** — Refactoring Priority Matrix. |
| A3 | File contains pass-through pattern: method bodies are single delegation calls | Pass-through detected. Jump to **Core Workflow** — Phase 5 (Deletion Test). |
| A4 | New file added with `public` methods but no callers yet | Premature interface. Jump to **Decision Trees** — Interface Minimization Strategy. |
| A5 | Configuration class with >20 fields and individual getters | Trivial wrapper. Jump to **Core Workflow** — Phase 2 (Interface Minimization). |

### Intent Route (Ask the User)

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

```
DESIGN → MINIMIZE → SEAM → ADAPT → VERIFY
   ↑___________________________________|
              (iterate)
```

### Phase 1: Module Inventory

**Goal:** Catalog all modules in scope and classify each by depth.

```
┌──────────────────────────────────────────────────┐
│              MODULE INVENTORY                      │
│                                                    │
│  For each module:                                  │
│  1. Count public methods (interface cost)          │
│  2. Estimate lines of behavior (non-delegation)    │
│  3. Compute depth = behavior / interface           │
│  4. Classify:                                      │
│     ├── depth >= 3.0 → DEEP (keep, celebrate)      │
│     ├── 1.0 <= depth < 3.0 → MODERATE (investigate)│
│     └── depth < 1.0 → SHALLOW (mark for action)    │
│                                                    │
│  Output: depth scorecard for every module          │
└──────────────────────────────────────────────────┘
```

**Steps:**
1. List every module (class, file, package) in the target scope
2. For each, count public methods/symbols — this is the **interface cost**
3. Estimate lines of implementation (non-delegation, non-getter/setter logic) — this is **behavior**
4. Compute depth = behavior / interface cost
5. Classify modules as deep, moderate, or shallow

**Checkpoint:** Depth scorecard complete. All shallow modules flagged.

---

### Phase 2: Interface Minimization

**Goal:** Reduce the public surface of every module to the absolute minimum.

```
┌──────────────────────────────────────────────────┐
│           INTERFACE MINIMIZATION                   │
│                                                    │
│  For each method in the public interface:          │
│    Q1: Is this method called by external code?     │
│         NO → Make private (or delete)              │
│         YES → Continue                             │
│    Q2: Can this be combined with another method?   │
│         YES → Merge and reduce parameter count     │
│         NO → Continue                              │
│    Q3: Does this expose implementation detail?     │
│         YES → Hide behind abstraction              │
│         NO → Keep (justified)                      │
│                                                    │
│  After minimization: re-compute depth              │
└──────────────────────────────────────────────────┘
```

**Steps:**
1. List every public method/symbol
2. Apply the three questions above to each
3. Combine methods where possible (e.g., `setX()` + `setY()` → `configure(options)`)
4. Use default parameters instead of overloads
5. Narrow return types (return concrete types, not internal representations)
6. Hide implementation classes behind interfaces
7. Re-compute depth after minimization

**Checkpoint:** Interface minimized. Depth improved (ideally >3.0).

---

### Phase 3: Seam Identification

**Goal:** Find natural boundaries where modules can be cleanly separated.

```
┌──────────────────────────────────────────────────┐
│              SEAM IDENTIFICATION                   │
│                                                    │
│  Seam checklist for candidate boundary A|B:        │
│  ✓ A and B change at different rates               │
│  ✓ A can be tested independently from B            │
│  ✓ A has different performance characteristics     │
│  ✓ A has different error-handling needs            │
│  ✓ A serves different caller personas              │
│  ✓ B can be replaced without changing A            │
│                                                    │
│  Score: 6/6 = natural seam, 4-5/6 = candidate,     │
│         <4/6 = artificial boundary (reconsider)    │
└──────────────────────────────────────────────────┘
```

**Steps:**
1. Identify all candidate boundaries in the module inventory
2. Score each candidate against the seam checklist
3. Natural seams (5-6/6): proceed to Phase 4
4. Candidates (4/6): investigate — is the boundary worth formalizing?
5. Artificial (<4/6): do not add adapters here; look for better seams

**Checkpoint:** Seam map complete. Adapter targets identified.

---

### Phase 4: Adapter Placement

**Goal:** Place adapters at identified seams to decouple modules.

```
┌──────────────────────────────────────────────────┐
│              ADAPTER PLACEMENT                     │
│                                                    │
│  Module A  ───[raw]──→  Module B  (tight couple)  │
│       ↓                                ↑           │
│  Module A  ───[Adapter]──→  Interface  ←── Module B│
│                                                    │
│  Select adapter type by seam characteristics:      │
│  ├── Translation: different data formats           │
│  ├── Facade: simplify complex subsystem            │
│  ├── Anti-Corruption: protect domain from external │
│  └── Bridge: abstract over multiple implementations│
└──────────────────────────────────────────────────┘
```

**Steps:**
1. For each natural seam, select the appropriate adapter pattern
2. Define the interface that the adapter will expose
3. Implement the adapter with minimal surface area
4. Verify that Module A now depends only on the interface, not Module B
5. Update callers to use the adapter

**Checkpoint:** All natural seams have adapters. Coupling reduced.

---

### Phase 5: Deletion Test Verification

**Goal:** Validate that every module earns its existence.

```
┌──────────────────────────────────────────────────┐
│              DELETION TEST                         │
│                                                    │
│  For each module M:                                │
│  1. Imagine deleting M entirely                    │
│  2. What breaks?                                   │
│     ├── Nothing → M is dead code. Delete it.       │
│     ├── Only tests → M is test-only. Reassess.     │
│     ├── Callers can be trivially updated → Delete  │
│     └── Callers need significant rewrite → Keep    │
│  3. For kept modules:                              │
│     ├── Can callers use M's dependency directly?   │
│     │   YES → M is a pass-through. Delete it.       │
│     └── Does M add real behavior? → Keep, with     │
│         updated depth score                        │
└──────────────────────────────────────────────────┘
```

**Steps:**
1. Run the deletion test on every module in inventory
2. Delete modules that fail (dead code, pass-throughs, trivial wrappers)
3. Update callers of deleted modules to use the underlying dependency directly
4. Re-run depth analysis on remaining modules
5. Document decisions in ADR format

**Checkpoint:** All remaining modules pass the deletion test. Codebase is leaner.

---

### Iterate

After Phase 5, return to Phase 1 with the leaner codebase. Each iteration should increase the average module depth.

## Decision Trees

### Module Depth Classification

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

### Interface Minimization Strategy

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

### Seam Placement Decision

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

### Adapter Pattern Selection

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

### Refactoring Priority Matrix

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

## Cross-Skill Coordination

| Direction | Skill | What's Exchanged | Decision Gate |
|-----------|-------|------------------|---------------|
| **Upstream** | system-architect | Component boundaries, bounded contexts, architecture decision records | ADR must define component seam before codebase-design refines module boundaries within the component |
| **Upstream** | code-reviewer | Code review flags for shallow modules, pass-through detection | Review flags trigger codebase-design evaluation — confirm or dismiss with depth analysis |
| **Downstream** | backend-developer | Deep module designs with minimized interfaces, adapter specifications | Backend dev implements the designed interfaces — do not add public methods without revisiting codebase-design |
| **Downstream** | frontend-developer | Module interface contracts, adapter patterns for API consumption | Frontend dev uses the designed facades — report back if interface is insufficient |
| **Downstream** | fullstack-developer | End-to-end module designs spanning frontend and backend | Fullstack dev validates that designed seams work across the stack |
| **Downstream** | code-reviewer | Depth scorecards for review context, deletion test results | Reviewer checks new code against established depth standards |

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|-------------------|---------------|
| T1 | User opens a file with >15 public methods | "This module has high interface cost. Run depth analysis? [Y/n]" |
| T2 | User creates a new file with `public` keyword | "Before adding public methods, have you defined the module's depth target?" |
| T3 | User writes a method body that is a single delegation call | "This looks like a pass-through. Does this method add behavior, or can callers use the dependency directly?" |
| T4 | User adds a getter/setter pair | "Getters/setters expose implementation. Is there a behavior method that would serve callers better?" |
| T5 | User creates a module in a new directory | "Is this directory a natural seam, or does this module belong with its co-changing peers?" |
| T6 | User imports from 5+ different packages in one file | "High fan-in detected. This module may have low locality. Consider splitting or consolidating dependencies." |
| T7 | Git diff shows 3+ files in different directories changing together | "Locality alert: these files co-change but live apart. Should they be co-located?" |

## What Good Looks Like

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

### Exercise 1: Depth Scoring (15 min)
Take any module in your current codebase. Count its public methods. Count its lines of actual behavior (not delegation, not getters/setters). Compute depth. Classify it. If shallow, identify the 3 most important changes to increase depth. Timebox: 15 minutes.

### Exercise 2: Deletion Test Sprint (20 min)
Take a package or directory. Run the deletion test on every file in it. For each file, answer: "If I delete this, what breaks?" Create a list: files to delete, files to keep, files to refactor. Timebox: 20 minutes.

### Exercise 3: Interface Minimization Kata (25 min)
Choose a module with 8+ public methods. Apply Phase 2's three questions to every method. Combine, hide, or delete until the interface is ≤5 methods. Re-compute depth. Compare before/after. Timebox: 25 minutes.

### Exercise 4: Seam Mapping (20 min)
Pick a feature that spans 3+ files. Draw the dependency graph. Identify where changes propagate. Score each boundary using the seam checklist. Mark natural seams. Propose adapter placements. Timebox: 20 minutes.

### Exercise 5: Locality Heatmap (30 min)
Run `git log --name-only` on your repo for the last 50 commits. Group files that co-change. For each group, compute spatial distance (directory tree distance). Identify files with high co-change frequency but high spatial distance — these are locality violations. Propose a reorganization. Timebox: 30 minutes.

## Gotchas

**Total cost: $15,000-$45,000 in developer productivity per year.** A shallow module with 12 public methods and 15 lines of behavior forces 10 developers to read 12 method signatures every time they touch related code. Over a year, that's hundreds of wasted cognitive cycles. Each wasted minute compounds: reading the interface, tracing to the implementation, discovering there's nothing there, and going back. At $150/hour blended rate, a team of 10 loses $15K-$45K annually on a single shallow module.

**Total cost: $25,000-$75,000 in refactoring labor per wrong seam.** Placing a seam at the wrong abstraction level means it will be moved within 6-18 months. Moving a seam requires updating every caller, rewriting tests, updating documentation, and retraining the team. For a module with 20+ callers across 5 services, that's 2-4 weeks of engineering effort at $12K-$20K per week, plus cascading integration issues.

**Total cost: $30,000-$100,000 in ripple-effect debugging per year.** Tight coupling through shared mutable state means a bug in Module A manifests as a failure in Module D, three layers away. The debugging cost explodes: developers must understand the full chain, reproduce the exact state mutation order, and fix without breaking Modules B and C. Each incident costs 4-16 hours of senior engineer time. At 2 incidents per month, that's $30K-$100K annually.

**Total cost: $10,000-$30,000 in maintenance drag per pass-through module.** A pass-through module that delegates every call to a dependency without adding behavior still requires: dependency updates, security patches, documentation, tests, onboarding explanation, and code review attention. Over 2 years, the accumulated maintenance cost of keeping it around exceeds the one-time cost of deleting it by 10-20x.

**Total cost: $20,000-$50,000 in onboarding overhead per scattered module group.** When related concepts are spread across 5+ directories, new developers spend 2-3 extra weeks building a mental map. They discover connections through painful debugging sessions, not through reading coherent code. At a $120K salary, that's $5K-$8K per new hire. For a team that onboards 4 developers per year, that's $20K-$50K annually.

**Total cost: $5,000-$15,000 in interface creep per ungoverned module per year.** Without active minimization, modules gain 1-2 public methods per quarter. After 2 years, a module that started with 5 methods has 13-21. Each addition seemed harmless at the time, but the cumulative depth erosion makes the module progressively harder to understand and change.

## Verification

```bash
# 1. Depth scorecard: every module should have depth > 1.0
grep -rn "public " src/ | wc -l  # Count public surface area
# For each module, compute depth = behavior_lines / public_methods

# 2. Pass-through detection: methods that are single delegation calls
grep -rn "return .*\." src/ | grep -v "return this" | head -20

# 3. Locality co-change check (last 30 days)
git log --since="30 days ago" --name-only --oneline | sort | uniq -c | sort -rn | head -20

# 4. Interface bloat: files with >10 public methods
grep -c "public " src/**/*.java | awk -F: '$2 > 10 {print}'

# 5. Verify all adapters are at verified natural seams
# Manual: score each adapter boundary against seam checklist (Phase 3)

# 6. Deletion test: confirm no dead modules exist
# For each module, verify at least one production caller exists
```

## References

- [Depth Vocabulary](references/depth-vocabulary.md) — Definitions: depth, shallow module, deep module, interface cost, behavior value, seam, leverage, locality
- [Deletion Test](references/deletion-test.md) — Step-by-step deletion test protocol with pass-through and trivial wrapper examples
- [Seam Identification](references/seam-identification.md) — Finding natural seams: extension points, test boundaries, config boundaries, rate-of-change boundaries
- [Adapter Patterns](references/adapter-patterns.md) — Adapter catalog: translation adapter, facade, anti-corruption layer, bridge, when to use each
- [Leverage Calculation](references/leverage-calculation.md) — Measuring leverage: caller count, benefit per caller, maintenance cost, depth vs leverage trade-off
- [Locality Analysis](references/locality-analysis.md) — Locality score: co-change frequency, spatial distance, conceptual distance, co-location decision framework
- [Shallow Module Detection](references/shallow-module-detection.md) — Detection patterns: pass-through, trivial wrapper, config pass-through, excessive getters/setters, god class
- [Interface Minimization](references/interface-minimization.md) — Techniques: combine methods, default parameters, narrow return types, hide implementation classes, method justification checklist
