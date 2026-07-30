#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
SKILL_NAME="$(basename "$SKILL_DIR")"
REF_DIR="$SKILL_DIR/references"
FAILURES=0

check_section() {
  if grep -q "^## $1" "$SKILL_MD"; then
    echo "  [PASS] Section: $1"
  else
    echo "  [FAIL] Section: $1 — MISSING"
    FAILURES=$((FAILURES + 1))
  fi
}

echo "=== Verifying $SKILL_NAME ==="
echo ""

# ── Block A: File existence ──────────────────────────────────────────────
echo "--- File Existence ---"

# Check 1
if [ -f "$SKILL_MD" ]; then
  echo "  [PASS] SKILL.md exists"
else
  echo "  [FAIL] SKILL.md not found"
  exit 1
fi

# ── Block B: Required Sections (22 checks from lint-template.py) ──────────
echo ""
echo "--- Required Sections ---"

# Check 2-23
check_section "Route the Request"
check_section "Ground Rules"
check_section "The Expert's Mindset"
check_section "Operating at Different Levels"
check_section "When to Use"
check_section "When NOT to Use"
check_section "Decision Trees"
check_section "Core Workflow"
check_section "Best Practices"
check_section "Error Decoder"
check_section "Cross-Skill Coordination"
check_section "Proactive Triggers"
check_section "What Good Looks Like"
check_section "Deliberate Practice"
check_section "References"
check_section "Gotchas"
check_section "Anti-Patterns"
check_section "Verification"
check_section "Error Recovery"
check_section "State Log"
check_section "Production Checklist"
check_section "Anti-Rationalization"

# ── Block C: YAML Frontmatter Fields (5 checks) ──────────────────────────
echo ""
echo "--- YAML Frontmatter ---"

# Check 24: name matches directory
NAME_FIELD=$(grep -m1 '^name:' "$SKILL_MD" 2>/dev/null | awk '{print $2}' || echo "")
if [ "$NAME_FIELD" = "$SKILL_NAME" ]; then
  echo "  [PASS] name '$NAME_FIELD' matches directory '$SKILL_NAME'"
else
  echo "  [FAIL] name '$NAME_FIELD' does not match directory '$SKILL_NAME'"
  FAILURES=$((FAILURES + 1))
fi

# Check 25: description field
if grep -q '^description:' "$SKILL_MD"; then
  echo "  [PASS] description field present"
else
  echo "  [FAIL] description field MISSING"
  FAILURES=$((FAILURES + 1))
fi

# Check 26: version field
if grep -q '^version:' "$SKILL_MD"; then
  echo "  [PASS] version field present"
else
  echo "  [FAIL] version field MISSING"
  FAILURES=$((FAILURES + 1))
fi

# Check 27: chain.consumes_from
if grep -q 'consumes_from' "$SKILL_MD"; then
  echo "  [PASS] chain.consumes_from present"
else
  echo "  [FAIL] chain.consumes_from MISSING"
  FAILURES=$((FAILURES + 1))
fi

# Check 28: chain.feeds_into
if grep -q 'feeds_into' "$SKILL_MD"; then
  echo "  [PASS] chain.feeds_into present"
else
  echo "  [FAIL] chain.feeds_into MISSING"
  FAILURES=$((FAILURES + 1))
fi

# ── Block D: Content Quality Checks (10 checks) ──────────────────────────
echo ""
echo "--- Content Quality ---"

# Check 29: Decision trees (### subheadings across entire document) >= 3
# Risk Engineer embeds decision logic throughout Core Workflow; no dedicated ## Decision Trees section.
DT_COUNT=$(grep -c '^### ' "$SKILL_MD" 2>/dev/null || echo 0)
if [ "$DT_COUNT" -ge 3 ]; then
  echo "  [PASS] Decision sub-structures (### headings): $DT_COUNT (minimum 3)"
else
  echo "  [FAIL] Decision sub-structures (### headings): $DT_COUNT (need at least 3)"
  FAILURES=$((FAILURES + 1))
fi

# Check 30: Dollar-quantified gotchas >= 5
GOTCHA_COUNT=$(grep -c '\$[0-9]' "$SKILL_MD" 2>/dev/null || echo 0)
if [ "$GOTCHA_COUNT" -ge 5 ]; then
  echo "  [PASS] Dollar-quantified gotchas: $GOTCHA_COUNT (minimum 5)"
else
  echo "  [FAIL] Dollar-quantified gotchas: $GOTCHA_COUNT (need at least 5)"
  FAILURES=$((FAILURES + 1))
fi

# Check 31: QUICK markers >= 3
QUICK_COUNT=$(grep -c 'QUICK' "$SKILL_MD" 2>/dev/null || echo 0)
if [ "$QUICK_COUNT" -ge 3 ]; then
  echo "  [PASS] QUICK markers: $QUICK_COUNT (minimum 3)"
else
  echo "  [FAIL] QUICK markers: $QUICK_COUNT (need at least 3)"
  FAILURES=$((FAILURES + 1))
fi

# Check 32: Complete when >= 8
CW_COUNT=$(grep -ci 'Complete when' "$SKILL_MD" 2>/dev/null || echo 0)
if [ "$CW_COUNT" -ge 8 ]; then
  echo "  [PASS] Complete when statements: $CW_COUNT (minimum 8)"
else
  echo "  [FAIL] Complete when statements: $CW_COUNT (need at least 8)"
  FAILURES=$((FAILURES + 1))
fi

# Check 33: Ground Rules — Mechanical Trigger column
if grep -q "Mechanical Trigger" "$SKILL_MD"; then
  echo "  [PASS] Ground Rules: Mechanical Trigger column"
else
  echo "  [FAIL] Ground Rules: Missing Mechanical Trigger column"
  FAILURES=$((FAILURES + 1))
fi

# Check 34: Ground Rules — Violation Response column
if grep -q "Violation Response" "$SKILL_MD"; then
  echo "  [PASS] Ground Rules: Violation Response column"
else
  echo "  [FAIL] Ground Rules: Missing Violation Response column"
  FAILURES=$((FAILURES + 1))
fi

# Check 35: Anti-hallucination — Admit uncertainty
if grep -q "Admit uncertainty" "$SKILL_MD"; then
  echo "  [PASS] Anti-hallucination: 'Admit uncertainty'"
else
  echo "  [FAIL] Anti-hallucination: 'Admit uncertainty' MISSING"
  FAILURES=$((FAILURES + 1))
fi

# Check 36: Anti-hallucination — Flag your knowledge cutoff
if grep -q "Flag your knowledge cutoff" "$SKILL_MD"; then
  echo "  [PASS] Anti-hallucination: 'Flag your knowledge cutoff'"
else
  echo "  [FAIL] Anti-hallucination: 'Flag your knowledge cutoff' MISSING"
  FAILURES=$((FAILURES + 1))
fi

# Check 37: Anti-hallucination — Never guess security
if grep -q "Never guess security" "$SKILL_MD"; then
  echo "  [PASS] Anti-hallucination: 'Never guess security'"
else
  echo "  [FAIL] Anti-hallucination: 'Never guess security' MISSING"
  FAILURES=$((FAILURES + 1))
fi

# Check 38: Anti-hallucination — [VERIFIED]
if grep -q '\[VERIFIED\]' "$SKILL_MD"; then
  echo "  [PASS] Anti-hallucination: '[VERIFIED]'"
else
  echo "  [FAIL] Anti-hallucination: '[VERIFIED]' MISSING"
  FAILURES=$((FAILURES + 1))
fi

# ── Block E: Reference and File Checks (4 checks) ─────────────────────────
echo ""
echo "--- References & Files ---"

# Check 39: references/ directory exists
if [ -d "$REF_DIR" ]; then
  echo "  [PASS] references/ directory exists"
else
  echo "  [FAIL] references/ directory MISSING"
  FAILURES=$((FAILURES + 1))
fi

# Check 40: Reference files on disk >= 8
if [ -d "$REF_DIR" ]; then
  REF_FILE_COUNT=$(find "$REF_DIR" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
else
  REF_FILE_COUNT=0
fi
if [ "$REF_FILE_COUNT" -ge 8 ]; then
  echo "  [PASS] Reference files on disk: $REF_FILE_COUNT (minimum 8)"
else
  echo "  [FAIL] Reference files on disk: $REF_FILE_COUNT (need at least 8)"
  FAILURES=$((FAILURES + 1))
fi

# Check 41: All reference links resolve (no broken internal links)
BROKEN=0
if [ -d "$REF_DIR" ]; then
  for ref in $(grep -oh '(references/[^)]*\.md)' "$SKILL_MD" 2>/dev/null | sed 's|(references/||;s|)||' || true); do
    if [ -n "$ref" ] && [ ! -f "$REF_DIR/$ref" ]; then
      echo "  [FAIL] Broken reference: references/$ref"
      BROKEN=$((BROKEN + 1))
    fi
  done
fi
if [ "$BROKEN" -eq 0 ]; then
  echo "  [PASS] All reference links resolve (0 broken)"
else
  FAILURES=$((FAILURES + BROKEN))
fi

# Check 42: verify-skill.sh is executable
if [ -x "$SKILL_DIR/verify-skill.sh" ]; then
  echo "  [PASS] verify-skill.sh is executable"
else
  echo "  [FAIL] verify-skill.sh is NOT executable"
  FAILURES=$((FAILURES + 1))
fi

# ── Summary ───────────────────────────────────────────────────────────────
echo ""
echo "=============================================="
if [ "$FAILURES" -eq 0 ]; then
  echo "✅ $SKILL_NAME: ALL 42 CHECKS PASSED"
  exit 0
else
  echo "❌ $SKILL_NAME: $FAILURES of 42 check(s) FAILED"
  exit 1
fi
