#!/usr/bin/env bash
# ==============================================================================
# log-outcome.sh — Closed-Loop Feedback Mechanism for Skill Improvement
# ==============================================================================
# Records decisions, outcomes, failures, and trade-offs from skill execution
# into a structured log that downstream skills (especially code-reviewer and
# incident-responder) can query to prevent recurring bugs and pattern failures.
#
# Usage:
#   ./scripts/log-outcome.sh --skill <skill-name> --decision "<what>" \
#       --outcome <pass|fail|warn> --context "<why>" [--bug-signature "<pattern>"]
#
# The log is stored at .copilot/session-state/outcome-log.jsonl
# Each entry is one JSON line for efficient appending and querying.
# ==============================================================================
set -euo pipefail

SKILL=""
DECISION=""
OUTCOME=""
CONTEXT=""
BUG_SIGNATURE=""
LOG_FILE="${COPILOT_SESSION_DIR:-.copilot/session-state}/outcome-log.jsonl"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --skill) SKILL="$2"; shift 2 ;;
        --decision) DECISION="$2"; shift 2 ;;
        --outcome) OUTCOME="$2"; shift 2 ;;
        --context) CONTEXT="$2"; shift 2 ;;
        --bug-signature) BUG_SIGNATURE="$2"; shift 2 ;;
        --log-file) LOG_FILE="$2"; shift 2 ;;
        --help|-h)
            echo "Usage: log-outcome.sh --skill <name> --decision <text> --outcome <pass|fail|warn> --context <text> [--bug-signature <pattern>]"
            echo ""
            echo "Records skill execution outcomes for closed-loop feedback."
            echo "Skills downstream (code-reviewer, incident-responder) query this log"
            echo "to prevent recurring bugs and pattern failures."
            exit 0 ;;
        *) echo "Unknown flag: $1"; exit 1 ;;
    esac
done

# Validate required fields
if [[ -z "$SKILL" || -z "$DECISION" || -z "$OUTCOME" || -z "$CONTEXT" ]]; then
    echo "ERROR: --skill, --decision, --outcome, and --context are required."
    echo "Run with --help for usage."
    exit 1
fi

if [[ "$OUTCOME" != "pass" && "$OUTCOME" != "fail" && "$OUTCOME" != "warn" ]]; then
    echo "ERROR: --outcome must be one of: pass, fail, warn"
    exit 1
fi

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Build the JSON entry
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SESSION_ID="${COPILOT_SESSION_ID:-unknown}"

ENTRY=$(python3 -c "
import json, sys
entry = {
    'timestamp': '$TIMESTAMP',
    'session_id': '$SESSION_ID',
    'skill': '$SKILL',
    'decision': '''$DECISION''',
    'outcome': '$OUTCOME',
    'context': '''$CONTEXT''',
}
if '$BUG_SIGNATURE':
    entry['bug_signature'] = '$BUG_SIGNATURE'
print(json.dumps(entry))
")

# Append to log
echo "$ENTRY" >> "$LOG_FILE"
echo "Logged: [$OUTCOME] $SKILL — $DECISION"

# If outcome is "fail", also print a cross-reference for downstream skills
if [[ "$OUTCOME" == "fail" ]]; then
    echo ""
    echo "⚠️  FAILURE RECORDED. Downstream skills should query this log:"
    echo "   grep '\"skill\":\"$SKILL\"' $LOG_FILE | grep '\"outcome\":\"fail\"'"
    if [[ -n "$BUG_SIGNATURE" ]]; then
        echo "   Bug signature: $BUG_SIGNATURE"
        echo "   code-reviewer should scan for this pattern in all future reviews."
    fi
fi
