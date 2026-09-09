#!/usr/bin/env bash
# verify-skill.sh — structural self-check for this SKILL.md (no external deps).
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
file="$SKILL_DIR/SKILL.md"
errors=0
for heading in "Core Workflow" "Verification" "Decision Trees" "Ground Rules" "When NOT to Use"; do
  if ! grep -q "^## ${heading}" "$file"; then
    echo "missing section: ## ${heading}"
    errors=1
  fi
done
if ! grep -q "Portability target" "$file"; then echo "missing portability line"; errors=1; fi
exit $errors
