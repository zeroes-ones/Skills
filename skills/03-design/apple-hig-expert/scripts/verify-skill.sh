#!/usr/bin/env bash
# verify-skill.sh — Template compliance check for apple-hig-expert
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_FILE="$SKILL_DIR/SKILL.md"
PASS=0; FAIL=0
check() { if grep -q "$2" "$SKILL_FILE"; then PASS=$((PASS+1)); else echo "  [FAIL] $1"; FAIL=$((FAIL+1)); fi; }
echo "=== Verifying apple-hig-expert ==="
check "Anti-Hallucination section" '^## Anti-Hallucination$'
check "Ground Rules section" '^## Ground Rules'
check "The Expert's Mindset section" '^## The Expert'"'"'s Mindset'
check "Decision Trees section" '^## Decision Trees'
check "Verification section" '^## Verification'
check "Gotchas section" '^## Gotchas'
check "Anti-hallucination: Admit uncertainty" 'Admit uncertainty'
check "Anti-hallucination: Flag knowledge cutoff" 'Flag your knowledge cutoff'
check "Anti-hallucination: Never guess security" 'Never guess security'
check "Anti-hallucination: VERIFIED" '\[VERIFIED\]'
COMPLETE_COUNT=$(grep -ci 'Complete when' "$SKILL_FILE" || echo 0)
DT_COUNT=$(grep -c '^### Decision Tree' "$SKILL_FILE" || echo 0)
GOTCHA_COUNT=$(grep -c '\$[0-9,]' "$SKILL_FILE" || echo 0)
echo "  [INFO] Complete when items: $COMPLETE_COUNT (min 8)"
echo "  [INFO] Decision trees: $DT_COUNT (min 3)"
echo "  [INFO] Dollar-quantified gotchas: $GOTCHA_COUNT (min 5)"
[ "$COMPLETE_COUNT" -ge 8 ] && PASS=$((PASS+1)) || { echo "  [FAIL] Insufficient completion criteria ($COMPLETE_COUNT < 8)"; FAIL=$((FAIL+1)); }
[ "$DT_COUNT" -ge 3 ] && PASS=$((PASS+1)) || { echo "  [FAIL] Insufficient decision trees ($DT_COUNT < 3)"; FAIL=$((FAIL+1)); }
[ "$GOTCHA_COUNT" -ge 5 ] && PASS=$((PASS+1)) || { echo "  [FAIL] Insufficient dollar-quantified gotchas ($GOTCHA_COUNT < 5)"; FAIL=$((FAIL+1)); }
echo ""
if [ "$FAIL" -eq 0 ]; then echo "✅ apple-hig-expert: ALL CHECKS PASSED"; else echo "❌ apple-hig-expert: $FAIL FAILURES"; fi
exit $FAIL
