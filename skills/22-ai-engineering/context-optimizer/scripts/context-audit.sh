#!/usr/bin/env bash
# Context Audit — run the lever-ladder checklist + cost measurement for a payload.
# Usage:
#   bash scripts/context-audit.sh [requests.jsonl] [--strict]
# Delegates measurement to the shared token-cost-calculator and prints the
# lever-ladder checklist so every optimization follows the same discipline.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
CALC="$REPO_ROOT/skills/22-ai-engineering/token-efficiency/scripts/token-cost-calculator.py"
LOG="${1:-requests.jsonl}"
STRICT=""
for a in "$@"; do [ "$a" = "--strict" ] && STRICT="--strict"; done

echo "=== Context Audit ==="
echo "  log: $LOG"
echo ""

# 1. Measure (Ground Rule R1)
if [ -f "$LOG" ] && [ -f "$CALC" ]; then
    python3 "$CALC" --analyze "$LOG" 2>&1 | tail -12
else
    echo "  [WARN] no request log or calculator found — measure before optimizing (R1)."
fi

echo ""
echo "=== Lever-Ladder Checklist ==="
echo "  [ ] 1. Measure: per-level token ledger + \$/request baseline (provider usage fields)"
echo "  [ ] 2. Budget: per-task caps + 20% margin (budget.json, sum <= 80% window)"
echo "  [ ] 3. Reduce: dedup (Jaccard > 0.85), exclude noise, whitespace collapse"
echo "  [ ] 4. Stabilize: freeze the cache prefix byte-for-byte; hit rate >= 60%"
echo "  [ ] 5. Compress: lossy ONLY with a retention test >= 90%"
echo "  [ ] 6. Cap output: max_tokens per task type + structured output"
echo "  [ ] 7. Report: \$/request, \$/day, \$/done AND retention score"

if [ -n "$STRICT" ]; then
    echo ""
    echo "  RESULT: STRICT mode — any unchecked lever is a release-blocking gap."
    echo "  Complete the checklist or record documented exceptions before shipping."
else
    echo ""
    echo "  RESULT: checklist printed (advisory). Use --strict to enforce."
fi
