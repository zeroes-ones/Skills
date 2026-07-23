#!/usr/bin/env bash
# =============================================================================
# Eval Harness Runner — executes scenarios from evals/evals.json
#
# Usage:
#   ./scripts/run-evals.sh              # Run all suites
#   ./scripts/run-evals.sh --suite frontmatter-compliance  # Single suite
#   ./scripts/run-evals.sh --json       # JSON output for CI
#   ./scripts/run-evals.sh --summary    # Summary only
#
# Exit code: non-zero if any scenario fails
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
EVALS_FILE="$REPO_ROOT/evals/evals.json"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

TARGET_SUITE=""
OUTPUT_MODE="text"
SUMMARY_ONLY=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --suite) TARGET_SUITE="$2"; shift 2 ;;
        --json) OUTPUT_MODE="json"; shift ;;
        --summary) SUMMARY_ONLY=true; shift ;;
        *) echo "Unknown flag: $1"; exit 1 ;;
    esac
done

if [[ ! -f "$EVALS_FILE" ]]; then
    echo "ERROR: evals.json not found at $EVALS_FILE" >&2
    exit 2
fi

# ---------------------------------------------------------------------------
# Parse evals.json and run all scenarios
# ---------------------------------------------------------------------------
cd "$REPO_ROOT"

total=0
passed=0
failed=0
skipped=0
declare -a results_json

run_validator() {
    local scenario_id="$1"
    local validator="$2"
    local suite_id="$3"

    if [[ -z "$validator" || "$validator" == "N/A" ]]; then
        return 2  # skipped (no validator)
    fi

    # Execute the validator command
    local cmd_output
    cmd_output=$(eval "$validator" 2>&1) && local cmd_rc=$? || local cmd_rc=$?

    if [[ $cmd_rc -eq 0 ]]; then
        return 0  # pass
    else
        # Capture output for failure reporting
        echo "$cmd_output" >&2
        return 1  # fail
    fi
}

# Read suites from evals.json
if [[ -n "$TARGET_SUITE" ]]; then
    SUITE_FILTER=".suites[] | select(.id == \"$TARGET_SUITE\")"
else
    SUITE_FILTER=".suites[]"
fi

if [[ "$OUTPUT_MODE" == "json" ]]; then
    echo '{ "results": ['
fi

while IFS=$'\t' read -r suite_id suite_desc scenario_id scenario_validator; do
    if [[ -z "$suite_id" ]]; then continue; fi

    if [[ "$SUMMARY_ONLY" != true ]]; then
        echo -e "${BLUE}[${suite_id}/${scenario_id}]${NC} ${scenario_validator:-"manual check"}"
    fi

    total=$((total + 1))

    if [[ -z "$scenario_validator" || "$scenario_validator" == "N/A" ]]; then
        skipped=$((skipped + 1))
        if [[ "$SUMMARY_ONLY" != true ]]; then
            echo -e "  ${YELLOW}SKIP${NC} (no automated validator)"
        fi
        if [[ "$OUTPUT_MODE" == "json" ]]; then
            results_json+=("{\"suite\":\"$suite_id\",\"scenario\":\"$scenario_id\",\"status\":\"skipped\",\"reason\":\"no validator\"}")
        fi
        continue
    fi

    # Run the validator
    val_output=""
    if val_output=$(eval "$scenario_validator" 2>&1); then
        passed=$((passed + 1))
        if [[ "$SUMMARY_ONLY" != true ]]; then
            echo -e "  ${GREEN}PASS${NC}"
        fi
        if [[ "$OUTPUT_MODE" == "json" ]]; then
            results_json+=("{\"suite\":\"$suite_id\",\"scenario\":\"$scenario_id\",\"status\":\"pass\"}")
        fi
    else
        failed=$((failed + 1))
        if [[ "$SUMMARY_ONLY" != true ]]; then
            echo -e "  ${RED}FAIL${NC}"
            echo "$val_output" | head -5 | sed 's/^/    /'
        fi
        if [[ "$OUTPUT_MODE" == "json" ]]; then
            # Escape the output for JSON
            escaped=""
            escaped=$(echo "$val_output" | head -5 | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
            results_json+=("{\"suite\":\"$suite_id\",\"scenario\":\"$scenario_id\",\"status\":\"fail\",\"error\":$escaped}")
        fi
    fi
done < <(python3 -c "
import json, sys
with open('$EVALS_FILE') as f:
    d = json.load(f)
for suite in d['suites']:
    sid = suite['id']
    target = '$TARGET_SUITE'
    if target and sid != target:
        continue
    for sc in suite['scenarios']:
        v = sc.get('validator', '')
        print(f'{sid}\t{suite[\"description\"]}\t{sc[\"id\"]}\t{v}')
")

if [[ "$OUTPUT_MODE" == "json" ]]; then
    echo "$(IFS=,; echo "${results_json[*]}")"
    echo '], '
    echo "\"summary\": {\"total\": $total, \"passed\": $passed, \"failed\": $failed, \"skipped\": $skipped}"
    echo '}'
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "========================================"
echo "  Eval Results: $total scenarios"
echo -e "  ${GREEN}PASS${NC}: $passed  ${RED}FAIL${NC}: $failed  ${YELLOW}SKIP${NC}: $skipped"
echo "========================================"

if [[ $failed -gt 0 ]]; then
    echo -e "${RED}Some scenarios failed.${NC}"
    exit 1
fi

if [[ $skipped -gt 0 ]]; then
    echo -e "${YELLOW}$skipped scenarios lack automated validators.${NC}"
    echo "Trigger-routing and behavioral scenarios require agent-based evaluation."
fi

echo -e "${GREEN}All automated scenarios passed.${NC}"
exit 0
