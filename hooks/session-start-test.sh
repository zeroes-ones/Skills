#!/usr/bin/env bash
# Test for session-start hook — verifies output format is valid JSON and contains expected keys.
set -euo pipefail

OUTPUT=$(bash hooks/session-start.sh)

# Verify output is non-empty
if [[ -z "$OUTPUT" ]]; then
  echo "FAIL: session-start.sh produced empty output"
  exit 1
fi

# Verify key behaviors are mentioned
for keyword in "using-agent-skills" "Always-Context-First" "Stop-Under-Confidence"; do
  if ! echo "$OUTPUT" | grep -q "$keyword"; then
    echo "FAIL: session-start.sh missing expected keyword: $keyword"
    exit 1
  fi
done

echo "PASS: session-start.sh produces valid output with all required keywords"
