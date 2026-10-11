#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
SKILL_NAME="$(basename "$SKILL_DIR")"
REF_DIR="$SKILL_DIR/references"
FAILURES=0

check_section() {
  if grep -q "^## $1" "$SKILL_MD"; then
    echo "  [PASS] Section: $1"
  else
    echo "  [FAIL] Section: $1 - MISSING"
    FAILURES=$((FAILURES + 1))
  fi
}

echo "=== Verifying $SKILL_NAME ==="
echo ""
echo "--- File Existence ---"
if [ -f "$SKILL_MD" ]; then
  echo "  [PASS] SKILL.md exists"
else
  echo "  [FAIL] SKILL.md not found"
  exit 1
fi

echo ""
echo "--- Required Sections ---"
for s in "Route the Request" "Ground Rules" "The Expert's Mindset" "Operating at Different Levels" \
         "When to Use" "When NOT to Use" "Decision Trees" "Core Workflow" "Best Practices" \
         "Error Decoder" "Cross-Skill Coordination" "Proactive Triggers" "What Good Looks Like" \
         "Deliberate Practice" "References" "Gotchas" "Anti-Patterns" "Verification" \
         "Error Recovery" "State Log" "Production Checklist" "Anti-Rationalization"; do
  check_section "$s"
done

echo ""
echo "--- YAML Frontmatter ---"
NAME_FIELD=$(grep -m1 '^name:' "$SKILL_MD" | awk '{print $2}')
if [ "$NAME_FIELD" = "$SKILL_NAME" ]; then
  echo "  [PASS] name '$NAME_FIELD' matches directory '$SKILL_NAME'"
else
  echo "  [FAIL] name '$NAME_FIELD' does not match directory '$SKILL_NAME'"
  FAILURES=$((FAILURES + 1))
fi
for f in description version consumes_from feeds_into; do
  if grep -q "$f" "$SKILL_MD"; then
    echo "  [PASS] $f present"
  else
    echo "  [FAIL] $f MISSING"
    FAILURES=$((FAILURES + 1))
  fi
done

echo ""
echo "--- Content Quality ---"
DT_COUNT=$(grep -c '^### ' "$SKILL_MD" || true)
if [ "$DT_COUNT" -ge 3 ]; then echo "  [PASS] Decision sub-structures: $DT_COUNT (min 3)"; else echo "  [FAIL] Decision sub-structures: $DT_COUNT"; FAILURES=$((FAILURES + 1)); fi
GOTCHA_COUNT=$(grep -c '\$[0-9]' "$SKILL_MD" || true)
if [ "$GOTCHA_COUNT" -ge 5 ]; then echo "  [PASS] Dollar-quantified items: $GOTCHA_COUNT (min 5)"; else echo "  [FAIL] Dollar-quantified items: $GOTCHA_COUNT"; FAILURES=$((FAILURES + 1)); fi
QUICK_COUNT=$(grep -c 'QUICK' "$SKILL_MD" || true)
if [ "$QUICK_COUNT" -ge 3 ]; then echo "  [PASS] QUICK markers: $QUICK_COUNT (min 3)"; else echo "  [FAIL] QUICK markers: $QUICK_COUNT"; FAILURES=$((FAILURES + 1)); fi
CW_COUNT=$(grep -ci 'Complete when' "$SKILL_MD" || true)
if [ "$CW_COUNT" -ge 8 ]; then echo "  [PASS] Complete when statements: $CW_COUNT (min 8)"; else echo "  [FAIL] Complete when statements: $CW_COUNT"; FAILURES=$((FAILURES + 1)); fi
if grep -q "Mechanical Trigger" "$SKILL_MD"; then echo "  [PASS] Ground Rules: Mechanical Trigger column"; else echo "  [FAIL] Mechanical Trigger MISSING"; FAILURES=$((FAILURES + 1)); fi
if grep -q "Violation Response" "$SKILL_MD"; then echo "  [PASS] Ground Rules: Violation Response column"; else echo "  [FAIL] Violation Response MISSING"; FAILURES=$((FAILURES + 1)); fi
for phrase in "Admit uncertainty" "Flag your knowledge cutoff" "Never guess security"; do
  if grep -q "$phrase" "$SKILL_MD"; then echo "  [PASS] Anti-hallucination: '$phrase'"; else echo "  [FAIL] Anti-hallucination: '$phrase' MISSING"; FAILURES=$((FAILURES + 1)); fi
done
if grep -q '\[VERIFIED\]' "$SKILL_MD"; then echo "  [PASS] Anti-hallucination: '[VERIFIED]'"; else echo "  [FAIL] '[VERIFIED]' MISSING"; FAILURES=$((FAILURES + 1)); fi

echo ""
echo "--- References & Files ---"
if [ -d "$REF_DIR" ]; then echo "  [PASS] references/ directory exists"; else echo "  [FAIL] references/ MISSING"; FAILURES=$((FAILURES + 1)); fi
REF_COUNT=$(find "$REF_DIR" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
if [ "$REF_COUNT" -ge 1 ]; then echo "  [PASS] Reference files on disk: $REF_COUNT"; else echo "  [FAIL] No reference files"; FAILURES=$((FAILURES + 1)); fi
BROKEN=0
for ref in $(grep -oh '(references/[^)]*\.md)' "$SKILL_MD" 2>/dev/null | sed 's|(references/||;s|)||' || true); do
  if [ -n "$ref" ] && [ ! -f "$REF_DIR/$ref" ]; then
    echo "  [FAIL] Broken reference: references/$ref"
    BROKEN=$((BROKEN + 1))
  fi
done
if [ "$BROKEN" -eq 0 ]; then echo "  [PASS] All reference links resolve (0 broken)"; else FAILURES=$((FAILURES + BROKEN)); fi
if [ -x "$SKILL_DIR/scripts/verify-skill.sh" ]; then
  echo "  [PASS] verify-skill.sh is executable"
else
  echo "  [WARN] verify-skill.sh is not executable (chmod +x it)"
fi

echo ""
echo "=============================================="
if [ "$FAILURES" -eq 0 ]; then
  echo "$SKILL_NAME: ALL CHECKS PASSED"
  exit 0
else
  echo "$SKILL_NAME: $FAILURES check(s) FAILED"
  exit 1
fi
