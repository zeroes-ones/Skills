#!/usr/bin/env bash
# Structural verification harness for this skill (repo template gate G11).
# Verifies that SKILL.md declares the required sections, chain, and artifacts.
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL="$SKILL_DIR/SKILL.md"
fail=0
for needle in "## What Good Looks Like" "## Core Workflow" "## Error Recovery" "## State Log" "## Decision Trees"; do
  grep -qF "$needle" "$SKILL" || { echo "  missing section: $needle"; fail=1; }
done
grep -qE "^chain:" "$SKILL" || { echo "  missing chain:"; fail=1; }
[ -d "$SKILL_DIR/references" ] || { echo "  missing references/ dir"; fail=1; }
if [ "$fail" -eq 0 ]; then
  echo "OK: $(basename "$SKILL_DIR") structural invariants pass"
else
  echo "FAIL: $(basename "$SKILL_DIR")" >&2
fi
exit "$fail"
