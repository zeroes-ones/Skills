#!/usr/bin/env bash
# Test for session-start hook — verifies the always-on principles injection:
# non-empty output, all four operating rules + routing + key behaviors present,
# and the overlay stays within its token budget (<300 words, ~400 tokens).
set -euo pipefail

OUTPUT=$(bash hooks/session-start.sh)

if [[ -z "$OUTPUT" ]]; then
  echo "FAIL: session-start.sh produced empty output"
  exit 1
fi

# Word budget: the overlay is always-on context; it must stay tiny.
WORDS=$(echo "$OUTPUT" | wc -w | tr -d ' ')
if [[ "$WORDS" -gt 300 ]]; then
  echo "FAIL: always-on overlay is $WORDS words (budget: 300) — it loads every session"
  exit 1
fi

# Required content: routing pointer, the four operating rules, repo behaviors.
for keyword in \
  "using-agent-skills" \
  "Think Before Coding" \
  "Simplicity First" \
  "Surgical Changes" \
  "Goal-Driven Execution" \
  "Always-Context-First" \
  "Stop-Under-Confidence" \
  "No-False-Certainty"; do
  if ! echo "$OUTPUT" | grep -q "$keyword"; then
    echo "FAIL: session-start.sh missing expected keyword: $keyword"
    exit 1
  fi
done

echo "PASS: session-start.sh injects always-on principles ($WORDS words, all keywords present)"
