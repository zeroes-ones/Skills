#!/usr/bin/env bash
set -euo pipefail
# =============================================================================
# project-init.sh — attach the workflow system to ANY project in one command.
#
#   bash scripts/project-init.sh /path/to/project                 # symlink-first (default)
#   bash scripts/project-init.sh /path/to/project --mode copy     # standalone snapshot
#   bash scripts/project-init.sh /path/to/project --no-lib        # manifest only (no library link)
#
# Symlink-first, copy-if-required (matches the repo's install philosophy and the
# cross-agent-skills-packaging symlink conventions):
#   - default mode links the library once into <project>/.agent/lib, so every project always
#     sees the latest skills/scripts without duplication; broken links are detected and reported
#     (never a silent "deployed but invisible" failure).
#   - when symlinks are unavailable (e.g. Windows Git Bash without Developer Mode) it falls back
#     automatically to a copy, so the flow works on every OS.
#   - --mode copy forces a standalone snapshot (network shares, packaging/CI artifacts, immutable
#     copies).
# Cross-OS: run every python3 command as-is on macOS/Linux; on Windows use `python` instead
# (or `export PY=python` — the scripts respect the `PY` env var where used).
# =============================================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT="${1:-}"
MODE="symlink"
PY="${PY:-python3}"

while [ $# -gt 1 ]; do
    case "$2" in
        --mode) MODE="${3:-symlink}"; shift 2 ;;
        --no-lib) MODE="none"; shift ;;
        *) shift ;;
    esac
done

if [ -z "$PROJECT" ]; then
    echo "usage: bash scripts/project-init.sh /path/to/project [--mode symlink|copy] [--no-lib]"
    exit 2
fi
case "$MODE" in symlink|copy|none) ;; *) echo "unknown --mode '$MODE' (symlink|copy)"; exit 2 ;; esac

mkdir -p "$PROJECT"
AGENT_DIR="$PROJECT/.agent"
mkdir -p "$AGENT_DIR/manifests" "$AGENT_DIR/state" "$AGENT_DIR/memory"

cat > "$AGENT_DIR/.gitignore" <<'EOF'
state/*.json
memory/*.jsonl
agent-transcript.log
lib/             # library link/snapshot is environment, not project state
EOF

# --- attach the library: symlink-first, copy-if-required, cross-OS -------------
case "$MODE" in
    symlink)
        if ln -s "$REPO_ROOT" "$AGENT_DIR/lib" 2>/dev/null; then
            if [ ! -e "$AGENT_DIR/lib/skills" ]; then
                echo "✗ broken symlink detected at $AGENT_DIR/lib (target missing?)"
                rm -f "$AGENT_DIR/lib"
                exit 1
            fi
            LIB_MODE="symlink -> $REPO_ROOT"
        else
            # symlinks unavailable (e.g. Windows Git Bash without developer mode):
            # copy-if-required fallback so the workflow still works everywhere
            echo "⚠ symlinks not available here — falling back to a library copy (standalone snapshot)"
            echo "  (on Windows, enable Developer Mode or use Git Bash/WSL for true symlinks)"
            cp -R "$REPO_ROOT" "$AGENT_DIR/lib"
            LIB_MODE="snapshot copy (symlink unavailable)"
        fi
        ;;
    copy)
        echo "copying library snapshot into $AGENT_DIR/lib (standalone mode)..."
        cp -R "$REPO_ROOT" "$AGENT_DIR/lib"
        LIB_MODE="snapshot copy"
        ;;
    none)
        LIB_MODE="none (manifest-only scaffold)"
        ;;
esac

cat > "$AGENT_DIR/manifests/your-workflow.yaml" <<'EOF'
name: your-workflow
version: "1.0.0"
description: "Starter manifest. Replace the skill names below with your own flow (any library skill is a valid node; add a workflow: contract for central skills)."
payloads:
  handoff-v1:
    - status
    - summary
    - artifacts
    - decisions
    - open_questions
    - verification_evidence
    - context
    - budget
    - next
nodes:
  - id: producer
    skill: idea-to-spec        # replace with your first step's skill
    outputs: [work]
  - id: reviewer
    skill: code-reviewer       # replace with your gatekeeper skill
    inputs: [work]
    outputs: [review-verdict]
gates:
  - id: release-gate
    type: gate
    kind: human
    requires: [work]
loops:
  - id: fix-loop
    nodes: [producer, reviewer]
    exit_when: reviewer.verdict == pass
    max_iterations: 3
    escalate_to: release-gate
edges:
  - from: producer
    to: reviewer
    when: producer.status == done
    payload: handoff-v1
  - from: reviewer
    to: release-gate
    when: reviewer.status == done
    payload: handoff-v1
start: producer
end: [release-gate]
EOF

LIBPATH="$AGENT_DIR/lib/scripts"
cat > "$AGENT_DIR/README.md" <<EOF
# .agent — workflow layer for this project

Created by \`scripts/project-init.sh\` (library: $LIB_MODE).
This folder keeps only project state; the library stays a symlink (auto-updates) unless you
chose \`--mode copy\` for a standalone snapshot.

## Run (deterministic stub first, then your agent)

\`\`\`bash
# stub: verify loop/budgets/handoffs
python3 $LIBPATH/workflow-runner.py \\
  --manifest "$PROJECT/.agent/manifests/your-workflow.yaml" \\
  --state "$PROJECT/.agent/state/run-state.json"

# your agent as the content leg (ANY LLM backend via AGENT_CMD="{prompt}"):
#   claude : AGENT_CMD='claude -p "{prompt}"'
#   gemini : AGENT_CMD='gemini -p "{prompt}"'
#   codex  : AGENT_CMD='codex exec "{prompt}"'
#   ollama : AGENT_CMD='ollama run llama3.1 "{prompt}"'
#   other  : any CLI/wrapper that prints the model reply to stdout
AGENT_CMD="claude -p" python3 $LIBPATH/workflow-runner.py \\
  --manifest "$PROJECT/.agent/manifests/your-workflow.yaml" \\
  --executor $LIBPATH/executors/agent_executor.py \\
  --guardrail $LIBPATH/lib/guardrails.py \\
  --memory "$PROJECT/.agent/memory" \\
  --state "$PROJECT/.agent/state/run-state.json"
\`\`\`

## Measure (beyond the run)

\`\`\`bash
python3 $LIBPATH/export-traces.py --state "$PROJECT/.agent/state/run-state.json"
python3 $LIBPATH/skill-sli-report.py --dir "$PROJECT/.agent/state" --gate-escalation 0.5
python3 $LIBPATH/validate-workflows.py --manifest "$PROJECT/.agent/manifests/your-workflow.yaml"
\`\`\`

## Improve (closed loop)

Failing runs become candidates: \`$LIBPATH/skill-evolve-prep.py --dir ...\` then
\`$LIBPATH/skill-evolve-promote.py --state ... --manifest ... --executor ...\`
(promotion is verifier-gated). Incidents become \`evals/golden/<skill>/cases.json\` entries.

Docs: docs/using-for-any-project.md, examples/efficiency-in-action.md.
EOF

echo "✔ attached workflow layer to $PROJECT  (library: $LIB_MODE)"
echo "  manifests: $AGENT_DIR/manifests/your-workflow.yaml"
echo "  lib:       $AGENT_DIR/lib"
echo ""
echo "next:"
echo "  python3 $LIBPATH/workflow-runner.py --manifest \"$PROJECT/.agent/manifests/your-workflow.yaml\" --state \"$PROJECT/.agent/state/run-state.json\""
