# workflow/manifests — Library-Wide Starter Manifests

Every manifest in this directory composes **ordinary library skills** into executable graphs. They
demonstrate that loops and graphs are not limited to the two workflow-native skills
(`iterative-task-execution`, `workflow-graph-authoring`) — **any skill with Core Workflow +
Verification is a valid node in default mode** (WORKFLOW-SYSTEM.md §8): the skill's Verification /
Production Checklist tables act as the completion-criteria source, and `scripts/workflow-runner.py`
enforces loop budgets, stagnation, step budgets, and handoff bookkeeping in code.

## Coverage legend (the four shapes)

| Manifest | Shape | What it proves |
|----------|-------|----------------|
| `serial-feature-delivery.yaml` | **Serial, single-agent** | idea-to-spec → system-architect → code-reviewer, one registered handoff payload per edge |
| `quality-fix-loop.yaml` | **Bounded loop, single-agent** | backend-developer ↔ qa-engineer until `qa.verdict == pass`; exhaustion escalates to a human gate |
| `parallel-audits-merge.yaml` | **Parallel, multi-agent** | three specialist auditors over one change, join: all, human gate fires after the last auditor |
| `agent-efficiency-pass.yaml` | **Serial, prompt/efficiency skills** | using-agent-skills → llm-engineer → context-compaction-strategies → token-efficiency |
| `senior-dev-loop.yaml` | **Bounded loop, single-agent (flagship)** | micro-SDLC over flagship skills: incremental-implementation ↔ code-reviewer until `review.verdict == pass`; exhaustion escalates to a human ship gate — see `docs/flagship-senior-engineering.md` |

Together they cover single- and multi-agent handoffs, serial and parallel work, and the
prompt-engineering + efficiency layers of the library — the shapes requested for library-wide
coverage.

## Making every skill graph-ready

1. **Default mode (today, no edits).** Any skill whose SKILL.md has Core Workflow + Verification
   can be referenced by a manifest. The library-wide readiness number is tracked by
   `python3 scripts/audit-library.py` (Workflow Readiness: declared vs. eligible).
2. **Node contracts (progressive).** Add an optional `workflow:` frontmatter block to the
   high-value skills your manifests exercise — typed artifacts, completion criteria, iteration
   budget, escalation target (`python3 scripts/lib/lint-workflow.py <skill>/SKILL.md`). Phases 1-2
   declare contracts on 24 delivery hubs (the 14 phase-1 set plus mobile-developer,
   compliance-officer, performance-engineer, ui-ux-designer, algorithmic-trader,
   incident-responder, legal-advisor, growth-engineer, data-scientist, analytics-engineer), and
   `python3 scripts/validate-workflows.py --coverage` proves all 297 skills resolve as nodes.
3. **Validate and run.** Every manifest here must stay valid:
   `python3 scripts/validate-workflows.py --all`. To run headless (stub executor):
   `python3 scripts/workflow-runner.py --manifest workflow/manifests/<name>.yaml`.

## Rules that keep this directory healthy

- Filename equals manifest `name` (validator V1).
- Manifests stay inside the Safe YAML Subset (no anchors, no flow maps, no block scalars).
- No undeclared cycles; every loop bounded; parallel members write disjoint outputs.
- A real agent replaces the stub executor: node bodies are the referenced SKILL.md prompts, run
  through `iterative-task-execution`'s intake → execute → verify → decide protocol with the
  boundary templates in `workflow/templates/`.
