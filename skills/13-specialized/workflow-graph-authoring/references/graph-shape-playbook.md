# Graph Shape Playbook — Worked Shapes

Deep-dive companion to `workflow-graph-authoring` Decision Trees. These are shapes, not recipes:
copy the *structure*, then re-derive exit conditions and budgets from the actual skills you use.

## Shape 1: Review-Fix Loop (quality rework)

```
                  ┌──────────────────────────────┐
   feature ──►    │  reviewers (parallel)        │
   (backend-      │  code-reviewer               │
   developer)     │  security-reviewer           │
                  └──────┬───────────────────────┘
                         │ join: all → findings
                         ▼
                  ┌───────────────┐        ┌──────────────┐
                  │ fixer         │◄───────│ exit_when:   │
                  │ (backend-     │        │ reviewers.   │
                  │  developer)   │        │ verdict ==   │
                  └──────┬────────┘        │ pass         │
                         │                 └──────────────┘
                         ▼                        │ not pass
              human-gate (requires:              │ (budget hit)
              findings + fix-report)◄────────────┘ escalate
```

Key choices: reviewers are parallel members with **disjoint outputs** (code findings vs. security
findings); the loop's gatekeeper is the review verdict; exhaustion escalates to the human gate that
would have reviewed the passing change anyway. Budget from history: if review-fix realistically
takes two rounds, `max_iterations: 3`.

## Shape 2: Security/Compliance Gate (irreversible step)

```
   build ──► security-reviewer ──► release-gate (human)
                                    requires: [security-report, release-candidate]
                                    pass → ship
                                    fail/blocked → fixer, bounded by a loop
```

The gate is not decorative: `requires` forces the artifacts to exist before the human sees
anything. If the human gate is a rubber stamp in practice, the graph is lying about where the
control lives — move the control into an auto gate and keep the human gate only for genuine
judgment.

## Shape 3: Parallel Verification (independent checks)

```
   artifact ──► [ qa-engineer | accessibility-auditor | performance-engineer ]
                          │  disjoint outputs
                          ▼
                     join: all
                          │
                          ▼
                 gate: needs_review? ──no──► done
                          │ yes
                          ▼
                 fixer (bounded loop back to checks)
```

Use `join: all` when every check is mandatory (accessibility, security, correctness). Use
`join: majority` only when the members are redundant opinions (e.g., multiple reviewers) and
`join: any` only for early-exit advisory scans. Parallelism is worth it only if the checks are
independent and each writes its own findings.

## Shape 4: Supervisor Review Board (multi-agent)

```
   supervisor (routing only)
      │  routing: parallel
      ▼
   [ architecture-review | security-review | domain-review ]   ← disjoint outputs
      │
      ▼
   join: all → consolidated verdict
      │
      ├── pass ──► continue
      └── conflict ──► escalation ladder: weighted vote → supervisor override → human gate
```

The supervisor routes and owns the outcome; it performs no content work (multi-agent-orchestration
ground rule). Workers write disjoint fields; the join consolidates. Conflict resolution follows the
ladder in `multi-agent-orchestration` (Section 7): vote → weighted → override → human.

## Shape 5: Ship-Only-When-Green (auto gate on quality)

```
   feature ──► ci-checks (parallel: unit, lint, security-scan)
                  │ join: all
                  ▼
            auto-gate: pass_when: ci-checks.verdict == pass
                  │
          ┌───────┴───────────┐
          │ pass              │ fail (N times)
          ▼                   ▼
        ship-node         fixer → back to ci-checks (loop, max_iterations from flake history)
```

An auto gate with `pass_when` + a fallthrough target replaces hand-written "if all checks passed"
logic in every downstream node. It is the manifest-native way to express a completion gate that
code can check — and the reason the condition vocabulary exists: the gate must be machine-decidable
or it belongs to a human.

## Anti-shapes (what these shapes must NOT become)

| Anti-shape | Why it breaks | Fix |
|------------|---------------|-----|
| Review loop with no exit value in practice | Reviewers always say "changes requested" because there is no pass bar | Define the pass bar (exit_when on a real verdict) before wiring the loop |
| Gate that requires nothing | Theater | `requires` artifacts; reject empty gates |
| Parallel checks writing one shared report | Last write wins | Disjoint findings + join merges |
| Supervisor doing the review itself | Bottleneck | Route, don't work |
| Polish loop with a huge budget | Context rot + wasted tokens | convergence window + budget from history |
