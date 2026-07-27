#!/bin/bash
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0
echo "=== feature-flag-architect: Skill Verification ==="
[ -f "$SKILL_DIR/SKILL.md" ] && echo "PASS: SKILL.md" || { echo "FAIL: SKILL.md missing"; ERRORS=$((ERRORS+1)); }
for ref in per-platform-patterns.md testing-strategies.md; do
  [ -f "$SKILL_DIR/references/$ref" ] && echo "PASS: references/$ref" || { echo "FAIL: references/$ref missing"; ERRORS=$((ERRORS+1)); }
done
[ -f "$SKILL_DIR/templates/flag-registration.yaml" ] && echo "PASS: templates/flag-registration.yaml" || { echo "FAIL: templates/flag-registration.yaml missing"; ERRORS=$((ERRORS+1)); }
echo ""
[ $ERRORS -eq 0 ] && echo "All checks passed" && exit 0 || { echo "$ERRORS check(s) failed"; exit 1; }
