#!/usr/bin/env bash
# =============================================================================
# eval-skill.sh — run a skill's deterministic golden cases (Frontier B2).
#
# Usage:
#   bash scripts/eval-skill.sh qa-engineer           # one skill
#   bash scripts/eval-skill.sh --all                 # every evals/golden/<skill>
#   bash scripts/eval-skill.sh qa-engineer transcript.txt   # score live output
#
# Exit 0 iff every executable case passes. Wiring point for the CI eval gate (G3).
# =============================================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GOLDEN_DIR="$REPO_ROOT/evals/golden"
HARNESS="$REPO_ROOT/scripts/lib/eval-golden.py"

FAILURES=0
RAN=0

run_one() {
    local skill="$1"
    local cases="$GOLDEN_DIR/$skill/cases.json"
    local output_arg=""
    if [ -n "${2:-}" ]; then
        output_arg="--output $2"
    fi
    if [ ! -f "$cases" ]; then
        echo "no golden cases for '$skill' at $cases"
        FAILURES=$((FAILURES + 1))
        return
    fi
    RAN=$((RAN + 1))
    if python3 "$HARNESS" --cases "$cases" $output_arg; then
        echo "  [PASS] golden: $skill"
    else
        echo "  [FAIL] golden: $skill"
        FAILURES=$((FAILURES + 1))
    fi
}

if [ "${1:-}" = "--all" ]; then
    for cases in "$GOLDEN_DIR"/*/cases.json; do
        [ -e "$cases" ] || continue
        skill="$(basename "$(dirname "$cases")")"
        run_one "$skill"
    done
elif [ -n "${1:-}" ]; then
    run_one "$1" "${2:-}"
else
    echo "usage: bash scripts/eval-skill.sh <skill> | --all"
    exit 2
fi

if [ "$FAILURES" -eq 0 ]; then
    echo "eval-skill: ${RAN} skill(s) green"
    exit 0
else
    echo "eval-skill: ${FAILURES} failure(s)"
    exit 1
fi
