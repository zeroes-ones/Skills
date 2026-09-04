# Mode-to-Skill Matrix & Chain Templates

> Deep reference for `senior-engineer-mode-router`. Full routing table, chain templates,
> output contracts, and handoff artifacts.

## Mode-to-Skill Matrix

| # | Mode | Primary skill(s) | Supporting chain | Output contract (deliverables) |
|---|------|------------------|------------------|-------------------------------|
| 1 | Build app from scratch | fullstack-developer | website-builder/mobile-developer (by target) → database-designer + api-designer → ui-ux-designer → code-reviewer | Architecture, file structure, DB schema, API endpoints, UI architecture, complete code |
| 2 | Understand & refactor codebase | codebase-design | code-simplification + code-reviewer | Architecture summary, problem areas, refactoring strategies, improved code (behavior unchanged) |
| 3 | Debug production issue | debugging-and-error-recovery | qa-engineer + verification-before-completion | Code functionality, problem, why it fails, edge cases, fixed production-ready code |
| 4 | System design + implementation | system-architect | api-designer → database-designer → event-driven-architect (if async) → backend/fullstack-developer | Architecture, components, data flow, API design, DB schema, caching strategy, code |
| 5 | Performance optimization | performance-engineer | observability-engineer + database-reliability-engineer | Bottlenecks, optimization strategies, improved code |
| 6 | Clean architecture rebuild | codebase-design | domain-modeling (+ mobile-architecture-patterns/desktop-architecture-patterns by platform) | New folder structure, architecture description, refactored code (behavior unchanged) |
| 7 | Multi-agent workflow | agent-persona-orchestrator | multi-agent-orchestration + agent-handoff-protocol + agent-eval-pipeline | Architecture, implementation, review feedback, final optimized version |
| 8 | Production UI components | frontend-developer | ui-ux-designer + accessibility-auditor + accessibility-testing | Component architecture, props design, implementation, usage examples |

## Chain Templates with Handoff Artifacts

### Mode 1 — Build from scratch
```
router (contract) → fullstack-developer (MVP code)
  → database-designer + api-designer (schema + API)
  → ui-ux-designer (UI spec) → code-reviewer (review)
Artifacts: contract → design/architecture doc → schema.sql + OpenAPI → UI spec → reviewed code
```

### Mode 2 — Understand & refactor
```
router (target repo) → codebase-design (architecture map)
  → code-simplification (cleanups) → code-reviewer (verify behavior unchanged)
Artifacts: architecture summary → problem list → refactor plan → refactored code + tests
```

### Mode 3 — Debug
```
router (repro + context) → debugging-and-error-recovery (root cause)
  → qa-engineer (verify fix) → verification-before-completion
Artifacts: repro + logs → root-cause analysis → fixed code + regression test
```

### Mode 4 — System design + impl
```
router (requirements) → system-architect (design + ADRs)
  → api-designer → database-designer → event-driven-architect (if async)
  → backend-developer/fullstack-developer (implementation)
Artifacts: design doc → API spec → schema → event map → code
```

### Mode 5 — Performance
```
router (baseline) → performance-engineer (profile + bottlenecks)
  → observability-engineer (measurement) → database-reliability-engineer (DB-specific)
Artifacts: baseline report → bottleneck list → optimized code → before/after numbers
```

### Mode 6 — Clean architecture rebuild
```
router (target repo) → codebase-design (boundaries) → domain-modeling (domain seams)
  → platform patterns if mobile/desktop → code (behavior unchanged) + tests
Artifacts: current-state map → target folder structure → refactored code
```

### Mode 7 — Multi-agent
```
router (task) → agent-persona-orchestrator (spawn Architect/Engineer/Reviewer/Optimizer)
  → multi-agent-orchestration (sequencing) → agent-handoff-protocol (transitions)
  → agent-eval-pipeline (quality)
Artifacts: plan → implementation → review findings → optimized final version
```

### Mode 8 — Production UI components
```
router (component brief) → ui-ux-designer (design tokens + spec)
  → frontend-developer (implementation) → accessibility-auditor + accessibility-testing
Artifacts: component spec → code + props → a11y audit → usage examples
```

## Output-Contract Template (paste before any chain)

```
Routing Mode {N} ({mode name}).
Target: {repo / app / product / greenfield — name it}.
Deliverables: {sections from the matrix}.
Quality bar: {scalable / production-ready / minimal-but-scalable / behavior unchanged}.
Chain: {skill A → skill B → skill C}.
Handoffs: {artifact per step}.
Checkpoint: {after which step / between which modes we confirm}.
```

## Compound-Request Examples

- **"Debug it and make it faster"** → Mode 3 first (fix correctness), checkpoint, then Mode 5 (perf on the fixed code). Never perf-first on broken code.
- **"Design + build a scalable X"** → Mode 4 as one flow (design → implement), no split needed.
- **Full 8-mode pack** → propose order: 2 (understand) → 6 (clean) → 4 (design) → 1 (build) → 8 (UI) → 5 (perf) → 3 (debug) → 7 (multi-agent last, once everything else is stable) — checkpoint between each.
- **"Think like a senior engineer" with no verb** → ask: build, refactor, debug, design, optimize, rebuild, orchestrate, or UI components?
