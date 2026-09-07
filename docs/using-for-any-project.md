# Using the Workflow System for Any Project

Five steps to run any project's work as bounded, verified, measurable agent workflows — no
matter the domain. Everything here is project-agnostic: skills are portable prompts, the engine
is pure code, and all state (manifests, checkpoints, memory, traces, SLIs) is per-project.

## Step 1 — Attach the library to your project

- One command: `bash scripts/project-init.sh /path/to/project` — scaffolds `<project>/.agent/`
  (manifests/, state/, memory/, `.gitignore`, README with run/measure/improve commands) and a
  starter manifest you edit with your skills.
- Vendor or global-install this repo (`bash scripts/install.sh`, or `skills-init` per
  PROJECT-BOOTSTRAP.md).
- Add a project context file (the `CLAUDE.md`/`AGENTS.md` convention of your agent) pointing at
  the skills you use most.
- Router: ask `using-agent-skills` (or the router in your agent) which skills match your flow.
- Deploy to other agent terminals with `cross-agent-skills-packaging`.

## Step 2 — Model your flow as a workflow manifest

Any of the 297 skills is already a valid graph node in default mode (its Verification /
Production Checklist sections act as the completion source); add an optional `workflow:` contract
when a skill is central to the flow. Manifests are plain YAML:

```yaml
name: docs-review-loop
payloads:
  handoff-v1: [status, summary, artifacts, decisions, open_questions,
              verification_evidence, context, budget, next]
nodes:
  - id: writer
    skill: documentation-engineer
    outputs: [draft]
  - id: reviewer
    skill: code-reviewer
    inputs: [draft]
    outputs: [review-verdict]
gates:
  - id: release-gate
    type: gate
    kind: human
    requires: [draft]
loops:
  - id: draft-fix
    nodes: [writer, reviewer]
    exit_when: reviewer.verdict == pass
    max_iterations: 3
    escalate_to: release-gate
edges:
  - from: writer
    to: reviewer
    when: writer.status == done
    payload: handoff-v1
start: writer
end: [release-gate]
```

Validate it: `python3 scripts/validate-workflows.py --manifest your-workflow.yaml`.

## Step 3 — Run it with your agent

Replace the deterministic stub with your agent via the reusable executor
(`scripts/executors/agent_executor.py`), which works with **any LLM backend** through the
`AGENT_CMD="{prompt}"` template — claude, gemini, codex, ollama, or any CLI/wrapper that prints
the model reply to stdout — with a timeout and graceful fallback:

```bash
AGENT_CMD="claude -p" python3 scripts/workflow-runner.py \
  --manifest your-workflow.yaml \
  --executor scripts/executors/agent_executor.py \
  --guardrail scripts/lib/guardrails.py \
  --memory ./agent-memory \
  --state ./run-state.json
```

Add nodes for parallel work with `parallel:` (join: all) and watch the loop exit on
`reviewer.verdict == pass`, escalate to the human gate at `max_iterations`, or block at the edge
if the agent output trips a guardrail.

**On-demand skills & sub-agents:** if a flow needs a capability the library lacks, create a draft
instantly — `python3 scripts/skill-factory.py --name <skill> --description "…" --workflow` — then
validate (`--coverage`, `lint-workflow`), fill the TODO sections, and add golden cases. In a
manifest, every node is an agent invocation: supervisor nodes fan out to workers, so **sub-agents
are just nodes the supervisor routes to**, each run by your LLM backend via `agent_executor.py`.

## Step 4 — Measure it like a service

Per project, treat runs as telemetry:

```bash
python3 scripts/export-traces.py --state run-state.json        # OTel-shaped spans
python3 scripts/skill-sli-report.py --dir ./states \
  --gate-escalation 0.5                                        # fail CI on reliability regressions
bash scripts/eval-skill.sh <skill>                             # golden regression for skills you touch
python3 scripts/benchmark-skills.py --root skills --markdown   # corpus baseline
```

## Step 5 — Let the project improve itself

Every failure is raw material:

```bash
python3 scripts/skill-evolve-prep.py --dir ./states            # failure traces -> draft inbox
python3 scripts/skill-evolve-promote.py --state <failing>.json \
  --manifest your-workflow.yaml --executor <executor> \
  --loop draft-fix --field max_iterations --value 5 --pass-at 4
```

Only changes that pass the replay verifier get promoted; every promotion/rejection is audit-led.
Turn production incidents into "never-again" golden cases under `evals/golden/<skill>/cases.json`.

## Use it on THIS repo first

Dogfood before dogfooding others: the library maintains itself with its own machinery.

```bash
# repo quality gates run as a parallel graph (workflow-validation | skill-lints | golden-evals)
# and merge into a human release gate - same shape as multi-agent review, applied to the repo.
python3 scripts/workflow-runner.py \
  --manifest workflow/manifests/repo-self-check.yaml \
  --executor scripts/executors/repo_checks.py \
  --state /tmp/repo-state.json --memory /tmp/repo-memory

# then measure it like any workflow:
python3 scripts/export-traces.py --state /tmp/repo-state.json
python3 scripts/skill-sli-report.py --dir /tmp --gate-escalation 0.5
```

The runner + validator + golden-eval self-tests are themselves the "tests" those gates run
(validate-workflows --selftest/--all, lint-workflow --all, eval-skill --all). Live result:
5 steps, all gates pass, release-gate approved, escalation rate 0.00. Swap
`scripts/executors/repo_checks.py` for `agent_executor.py` when a gate needs an actual LLM.

## Start-small guidance

1. Pick ONE real flow and write ONE manifest over two or three skills.
2. Run it deterministically first (no executor = stub) to tune budgets and gates.
3. Add your agent executor, then guardrails, then memory, then the SLI gate.
4. Contract-ize (`workflow:` frontmatter) only the skills that prove central.
5. Only then widen to more manifests and more skills.

## Portability notes

- Engine, validators, exporters, and report scripts are stdlib-only — no framework install.
- Skills declare portability targets (Claude Code / Copilot CLI / Cursor / OpenClaw / Gemini CLI);
  `.skills-compiled/` holds token-optimized copies.
- Repo philosophy (AGNOSTIC-PRINCIPLES.md): universal patterns in the skill body, industry
  specifics in `references/`, so the same flow pattern works for software, finance, legal,
  healthcare, content, or ops.

## Related docs

- WORKFLOW-SYSTEM.md — the L0/L1/L2 model and semantics
- workflow/manifests/README.md — shipped starter manifests (serial, loop, parallel, efficiency)
- examples/workflow-runtime/ — runnable multi-agent example with checkpoints
- END-TO-END-EXCELLENCE.md / BEYOND-LOOPS-GRAPHS.md — quality rubric and next-frontier builds
