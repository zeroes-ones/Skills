# Manifest Field Reference

Deep-dive companion to `workflow-graph-authoring`. Canonical contract:
`workflow/schema/workflow-manifest.schema.yaml`. This file walks every section field-by-field.

## meta

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `name` | string | yes | — | Lowercase slug `[a-z0-9][a-z0-9-]*`; filename must equal `name + ".yaml"` |
| `version` | string | no | "1.0.0" | Semver-ish string |
| `description` | string | no | — | ≤ 1024 chars |

## control

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `start` | string | no | node with no incoming edges | Must resolve to a node id |
| `end` | list[string] | no | nodes with no outgoing edges | Terminal node ids |
| `state.shared` | bool | no | true | Typed shared state enabled |
| `state.schema` | string | no | — | Registered state-schema name |
| `state.merge` | string | no | append-unique | append-unique \| replace \| majority |
| `budget.max_steps` | int | no | — | Global step cap for the run |
| `payloads` | map | no | — | name → list of registry keys (see below) |

Payload keys must come from the canonical registry: `status`, `summary`, `artifacts`,
`decisions`, `open_questions`, `verification_evidence`, `context`, `budget`, `next`.

## nodes[]

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `id` | string | yes | — | Unique slug across nodes/loops/parallel/gates |
| `type` | string | no | skill | skill \| gate \| supervisor \| task |
| `skill` | string | for skill | — | Must resolve under `skills/` by frontmatter name |
| `kind` | string | for gate | — | human \| auto |
| `description` | string | no | — | Role statement |
| `inputs` | list[string] | no | [] | Run-state fields / artifact names consumed |
| `outputs` | list[string] | no | [] | Fields / artifacts produced (used for write-ownership checks) |
| `max_iterations` | int | no | 1 | Revision attempts for this node (1 = no loop) |
| `on_exhaustion` | string | no | escalate | escalate \| next \| fail |
| `escalate_to` | string | no | — | Node id (gate preferred) for exhaustion |
| `workers` | list[string] | for supervisor | — | Worker node ids |
| `routing` | string | for supervisor | parallel | parallel \| sequential \| select |
| `select` | string | for select routing | — | Single worker node id |
| `executor` | string | for task | — | Executor handler name (examples/stubs) |
| `gate.pass_when` | string | auto gates | — | Condition vocabulary |
| `gate.else_go` | string | auto gates | — | Node id when condition false |

## edges[]

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `from` | string | yes | — | Node id |
| `to` | string | yes | — | Node id |
| `when` | string | no | always | Condition vocabulary (§2.6) |
| `payload` | string | no | — | Registered payload name (required for artifact-carrying edges per G4) |

## loops[]

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `id` | string | yes | — | Unique slug |
| `nodes` | list[string] | yes | — | Node ids executed per pass, in order |
| `exit_when` | string | yes | — | Condition on the gatekeeper's status/verdict |
| `max_iterations` | int | yes | — | ≥ 1; hard stop |
| `escalate_to` | string | no | report+stop | Node id receiving exhaustion |
| `convergence.window` | int | no | 2 | Consecutive passes without delta ⇒ stagnation |
| `convergence.require_delta` | bool | no | true | Turn stagnation detection on/off |

A node may belong to at most one loop; loops must not nest or overlap.

## parallel[]

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `id` | string | yes | — | Unique slug (referenced by edges/loops as a group where allowed) |
| `nodes` | list[string] | yes | — | ≥ 2 member node ids |
| `join` | string | no | all | all \| majority \| any |
| `outputs` | list[string] | no | [] | Fields merged at the join |

Members of one parallel block must write disjoint fields (validator V6).

## gates[]

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `id` | string | yes | — | Unique slug; a gate is also a valid edge target |
| `type` | string | yes | — | Must be `gate` |
| `kind` | string | yes | — | human \| auto |
| `requires` | list[string] | human gates | — | Artifacts/fields that must exist before the gate |
| `pass_when` | string | auto gates | — | Condition deciding pass/fail |
| `description` | string | no | — | What the gate decides and why it needs attention |

## Condition vocabulary (exact)

| Form | Meaning |
|------|---------|
| `always` | unconditional |
| `NODE.status == done` / `!= done` | terminal status compare |
| `NODE.status in (a, b)` | membership |
| `NODE.verdict == VALUE` / `!= VALUE` | verdict equality (string) |
| `loop.iterations < N` | loop budget remaining |

Anything else fails validation. If your transition needs richer logic, express it as an auto gate
or a dedicated node — do not extend the vocabulary ad hoc.

## Writing a valid manifest from scratch (cheat sheet)

```yaml
name: my-workflow
version: "1.0.0"
description: One line.
payloads:
  handoff-v1: [status, summary, artifacts, decisions, open_questions,
              verification_evidence, context, budget, next]
start: spec
nodes:
  - id: spec
    skill: idea-to-spec
    outputs: [spec]
  - id: architect
    skill: system-architect
    inputs: [spec]
    outputs: [architecture]
edges:
  - from: spec
    to: architect
    when: spec.status == done
    payload: handoff-v1
end: [architect]
```

Then: `python3 scripts/validate-workflows.py --manifest my-workflow.yaml`.
