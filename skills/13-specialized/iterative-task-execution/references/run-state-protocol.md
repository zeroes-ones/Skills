# Run-State Protocol — Reference

Deep-dive companion to `iterative-task-execution` Phase 0-4. Canonical schema:
`workflow/schema/run-state.schema.yaml`; semantics: WORKFLOW-SYSTEM.md Section 4.

## 1. What run-state is

One JSON file per workflow run. It is the single source of truth an executing agent reads at
INTAKE and writes at every state change. It is not a transcript — it is a compressed, verifiable
picture: which node is active, how many passes remain, what fields/artifacts exist and who owns
them, what was decided, and what is still open.

```json
{
  "workflow": "review-and-fix",
  "manifest_sha": "9f2c1a…",
  "node": "fixer",
  "phase": "decide",
  "iteration": 2,
  "budget": { "max_steps": 40, "steps_used": 9,
              "iterations": { "review-fix-loop": 2 } },
  "nodes": {
    "code-reviewer": { "status": "done", "verdict": "changes_requested",
                       "iterations": 1, "evidence": ["review.md"] }
  },
  "fields": {
    "findings": { "value": [ {"severity": "high", "file": "src/auth.py"} ],
                  "writer": "reviewers" }
  },
  "artifacts": { "review.md": { "path": "artifacts/review.md",
                                "sha": "ab12cd…", "type": "doc" } },
  "decisions": [ { "at": "code-reviewer", "what": "auth refactor required",
                   "by": "code-reviewer" } ],
  "open_questions": [],
  "handoff": { "from": "reviewers", "to": "fixer",
               "payload": "handoff-v1", "sha": "77e0…" },
  "log": [ { "step": 8, "node": "code-reviewer", "action": "done" } ]
}
```

## 2. Lifecycle of a node record

```
pending → running → done            (all criteria met + evidence)
                 → blocked          (external blocker; escalation report written)
                 → needs_review     (partial work handed off with honest gaps)
                 → skipped          (edge condition never fired)
```

Transitions are prompted by the DECIDE step of the node protocol. A node in `done` is a no-op if
re-entered, unless the executor sets `force: true` (idempotency rule R6).

## 3. What the agent must write, and when

| Action | Record updated | When |
|--------|----------------|------|
| Intake acknowledged | `log` += {action: intake}; `node` = current | Phase 0 |
| Artifact produced | `artifacts[name]` = {path, sha, type} | Phase 1, as written |
| Decision made | `decisions` += {at, what, by} | Phase 1 |
| Question left open | `open_questions` += item | Phase 1 |
| Verify pass | `log` += {action: verify, detail: k/n criteria} | Phase 2 |
| Revise decided | `iteration` += 1; `log` += {action: revise, detail: root cause + change} | Phase 3 |
| Done | `nodes[id]` = {status: done, verdict, evidence, summary}; `handoff` = outbound | Phase 3 |
| Escalate | `phase` = escalated; escalation report referenced in `log` | Phase 3 |
| Reflect | `decisions` += learning entry | Phase 4 |

Every write updates `updated` (ISO-8601 UTC) and appends to `log`. `steps_used` increments per
material action; the runner halts at `budget.max_steps` regardless of what the agent believes.

## 4. Hash discipline

- `nodes.<id>.sha` covers that node record; `fields.<name>.sha` covers the field value;
  `artifacts.<name>.sha` is the sha256 of the artifact file (first 12 hex chars).
- On handoff, the sender's outgoing `handoff.sha` is compared against what the receiver observes.
  Mismatch ⇒ abort and replay from the last verified checkpoint (agent-handoff-protocol rule:
  no handoff without state-hash verification).
- Reasonable hashing: sha256 of the canonical JSON serialization of the record, truncated to 12
  hex chars — cheap, and catches silent drift.

## 5. Field ownership

Every `fields` entry carries `writer`. In a parallel block, members write disjoint fields; the join
merges them into the block's declared `outputs` (merge policy from the manifest `state.merge`,
default `append-unique`). An agent that finds itself writing a field owned by another live node
must stop and report — the manifest should have prevented this statically; if it slipped through,
the runner's merge check is the backstop.

## 6. Resume semantics

A run is resumable when: the manifest hash matches, every `done` node record still has its
artifacts present, and `log` is append-consistent with `nodes`. Resume = set `node` to the first
incomplete node reachable from the completed frontier and continue the loop protocol. No node is
re-executed unless `force: true`.

## 7. Common mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Using run-state as a chat log | Context bloat; hashes meaningless | Append only structured log entries + summaries |
| Rewriting history (editing old node records) | Broken hash chain; undetectable drift | Records are append/update-once; revise = new pass |
| Empty `open_questions` because "I resolved it silently" | Downstream makes the decision for you | A resolved question is a decision: write it to `decisions` |
| `summary` > 400 chars | Verify step drowns in prose | Summaries compress; detail lives in artifacts |
| Forgetting `updated` | No way to detect staleness between passes | Stamp every write |
