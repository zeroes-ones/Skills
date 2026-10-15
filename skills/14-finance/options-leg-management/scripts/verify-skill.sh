#!/usr/bin/env bash
# verify-skill.sh — structural self-check for the options-leg-management skill.
#
# Verifies this skill's own structure: required sections, frontmatter fields, content
# quality gates, reference links and file layout. No network access, no third-party tooling.
#
# Usage: bash scripts/verify-skill.sh
# Exit:  0 = all checks passed, 1 = at least one check failed
set -uo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
SKILL_NAME="$(basename "$SKILL_DIR")"
REF_DIR="$SKILL_DIR/references"
FAILURES=0
TOTAL=0
WARNINGS=0

pass() {
  TOTAL=$((TOTAL + 1))
  echo "  [PASS] $1"
}

fail() {
  TOTAL=$((TOTAL + 1))
  FAILURES=$((FAILURES + 1))
  echo "  [FAIL] $1"
}

warn() {
  WARNINGS=$((WARNINGS + 1))
  echo "  [WARN] $1"
}

# Evaluate an integer expression and record pass/fail.
check_num() {
  local label="$1" value="$2" op="$3" bound="$4"
  if [ "$value" "$op" "$bound" ] 2>/dev/null; then
    pass "$label"
  else
    fail "$label"
  fi
}

# grep -c that never aborts the script and always yields a number.
count_of() {
  local n
  n=$(grep -cE -- "$1" "$2" 2>/dev/null) || n=0
  printf '%s' "$n"
}

# Count lines matching $1 in $2, restricted to the section between $3 and $4.
count_in_section() {
  local n
  n=$(sed -n "/^## $3/,/^## $4/p" "$2" 2>/dev/null | grep -cE -- "$1" 2>/dev/null) || n=0
  printf '%s' "$n"
}

# Case-insensitive count of lines matching an extended regex.
count_of_ci() {
  local n
  n=$(grep -ciE -- "$1" "$2" 2>/dev/null) || n=0
  printf '%s' "$n"
}

check_section() {
  if grep -q "^## $1" "$SKILL_MD" 2>/dev/null; then
    pass "Section: $1"
  else
    fail "Section: $1"
  fi
}

echo "=== Verifying $SKILL_NAME ==="
echo ""

# ── Block A: File existence ────────────────────────────────────────────────
echo "--- File Existence ---"
if [ -f "$SKILL_MD" ]; then
  pass "SKILL.md exists"
else
  fail "SKILL.md exists"
  echo ""
  echo "SKILL.md not found at $SKILL_MD — cannot continue."
  exit 1
fi

# ── Block B: Required level-2 sections ─────────────────────────────────────
echo ""
echo "--- Required Sections ---"
check_section "Route the Request"
check_section "Anti-Rationalization"
check_section "Ground Rules"
check_section "The Expert's Mindset"
check_section "Deliberate Practice"
check_section "Operating at Different Levels"
check_section "When to Use"
check_section "When NOT to Use"
check_section "Decision Trees"
check_section "Core Workflow"
check_section "Best Practices"
check_section "Error Decoder"
check_section "Error Recovery"
check_section "Cross-Skill Coordination"
check_section "Proactive Triggers"
check_section "Anti-Patterns"
check_section "State Log"
check_section "Production Checklist"
check_section "What Good Looks Like"
check_section "Verification Guardrails"
check_section "References"
check_section "Gotchas"
check_section "Anti-Hallucination"

# ── Block C: YAML frontmatter fields ────────────────────────────────────────
echo ""
echo "--- YAML Frontmatter ---"
NAME_FIELD=$(grep -m1 '^name:' "$SKILL_MD" | awk '{print $2}')
if [ "$NAME_FIELD" = "$SKILL_NAME" ]; then
  pass "name '$NAME_FIELD' matches directory '$SKILL_NAME'"
else
  fail "name '$NAME_FIELD' does not match directory '$SKILL_NAME'"
fi
for field in description license type version status updated tags token_budget; do
  if grep -q "^$field:" "$SKILL_MD" 2>/dev/null; then
    pass "frontmatter field: $field"
  else
    fail "frontmatter field: $field"
  fi
done
if grep -q '^type: finance' "$SKILL_MD" 2>/dev/null; then
  pass "type is 'finance'"
else
  fail "type is not 'finance'"
fi
for chain_field in consumes_from feeds_into; do
  if grep -q "$chain_field" "$SKILL_MD" 2>/dev/null; then
    pass "chain.$chain_field present"
  else
    fail "chain.$chain_field MISSING"
  fi
done
if grep -q 'skills/14-finance/options-leg-management/examples/backtest' "$SKILL_MD" 2>/dev/null; then
  pass "chain.examples points at this skill's backtest dir"
else
  fail "chain.examples missing or pointing elsewhere"
fi

# ── Block D: Content quality gates ─────────────────────────────────────────
echo ""
echo "--- Content Quality ---"

DT_COUNT=$(count_in_section '^### ' "$SKILL_MD" 'Decision Trees' 'Core Workflow')
check_num "Decision Trees sub-headings >= 3 (found: $DT_COUNT)" "$DT_COUNT" -ge 3

GLYPHS=$(sed -n '/^## Decision Trees/,/^## Core Workflow/p' "$SKILL_MD" | grep -o '[├└│▼→]' | wc -l | tr -d ' ') || GLYPHS=0
GLYPHS=${GLYPHS:-0}
check_num "Decision-tree branch glyphs >= 8 (found: $GLYPHS)" "$GLYPHS" -ge 8

DOLLARS=$(grep -oE '\$[0-9][0-9,]*' "$SKILL_MD" | wc -l | tr -d ' ') || DOLLARS=0
DOLLARS=${DOLLARS:-0}
check_num "Dollar-quantified figures >= 5 (found: $DOLLARS)" "$DOLLARS" -ge 5

UNLABELLED=$(grep -nE '\$[0-9]' "$SKILL_MD" | grep -vcE '\[COMPUTED\]|\[ESTIMATED\]|\[VERIFIED\]|\[BROKER-VERIFIED\]|\[COMMON-PRACTICE\]') || UNLABELLED=0
UNLABELLED=${UNLABELLED:-0}
check_num "Every dollar line carries a provenance tag (unlabelled: $UNLABELLED)" "$UNLABELLED" -le 0

QUICK=$(count_of '<!-- QUICK:' "$SKILL_MD")
check_num "QUICK markers >= 3 (found: $QUICK)" "$QUICK" -ge 3
if grep -q '<!-- STANDARD:' "$SKILL_MD" 2>/dev/null; then pass "STANDARD marker present"; else fail "STANDARD marker present"; fi
if grep -q '<!-- DEEP:' "$SKILL_MD" 2>/dev/null; then pass "DEEP marker present"; else fail "DEEP marker present"; fi

CW=$(grep -ciE 'Complete when' "$SKILL_MD") || CW=0
CW=${CW:-0}
check_num "'Complete when' statements >= 8 (found: $CW)" "$CW" -ge 8

if grep -q 'Mechanical Trigger' "$SKILL_MD" 2>/dev/null; then pass "Ground Rules: Mechanical Trigger column"; else fail "Ground Rules: Mechanical Trigger column"; fi
if grep -q 'Violation Response' "$SKILL_MD" 2>/dev/null; then pass "Ground Rules: Violation Response column"; else fail "Ground Rules: Violation Response column"; fi

BP=$(count_in_section '^[0-9]+\. ' "$SKILL_MD" 'Best Practices' 'Error Decoder')
check_num "Best Practices numbered items >= 10 (found: $BP)" "$BP" -ge 10

CR=$(grep -oE 'CR[0-9]+' "$SKILL_MD" | sort -u | wc -l | tr -d ' ') || CR=0
CR=${CR:-0}
check_num "Production Checklist CR items >= 12 (found: $CR)" "$CR" -ge 12

ED_COLS=$(sed -n '/^## Error Decoder/,/^## Error Recovery/p' "$SKILL_MD" | grep -m1 '^|' | awk -F'|' '{print NF-2}' | tr -d ' ') || ED_COLS=0
ED_COLS=${ED_COLS:-0}
check_num "Error Decoder table has 4 columns (found: $ED_COLS)" "$ED_COLS" -ge 4

XMARK=$(count_in_section '❌' "$SKILL_MD" 'Anti-Patterns' 'State Log')
check_num "Anti-Patterns entries >= 5 (found: $XMARK)" "$XMARK" -ge 5

for phrase in 'Admit uncertainty' 'Flag your knowledge cutoff' 'Never guess security' '\[VERIFIED\]'; do
  if grep -q "$phrase" "$SKILL_MD" 2>/dev/null; then
    pass "Anti-hallucination phrase: $phrase"
  else
    fail "Anti-hallucination phrase MISSING: $phrase"
  fi
done

TAGS=$(count_of '\[VERIFIED\]|\[COMPUTED\]|\[ESTIMATED\]|\[BROKER-VERIFIED\]|\[COMMON-PRACTICE\]' "$SKILL_MD")
check_num "Provenance tags >= 9 (found: $TAGS)" "$TAGS" -ge 9

if grep -q 'Portability target' "$SKILL_MD" 2>/dev/null; then pass "Portability target declared"; else fail "Portability target declared"; fi

FAILMODES=$(count_of_ci 'failure mode|what goes wrong|worst case|exit condition|edge case|known limitation' "$SKILL_MD")
check_num "Failure-mode documentation >= 10 (found: $FAILMODES)" "$FAILMODES" -ge 10

if grep -q '| Upstream Skill |' "$SKILL_MD" 2>/dev/null; then pass "Cross-skill upstream table present"; else fail "Cross-skill upstream table present"; fi
if grep -q '| Downstream Skill |' "$SKILL_MD" 2>/dev/null; then pass "Cross-skill downstream table present"; else fail "Cross-skill downstream table present"; fi

for regime in 'bull market|bull regime|uptrend' 'correction|pullback' 'bear market|downturn|drawdown|recession' 'crash|tail event|black swan|march 2020|market collapse'; do
  if grep -qiE "$regime" "$SKILL_MD" 2>/dev/null; then
    pass "Regime coverage phrase: $regime"
  else
    fail "Regime coverage MISSING: $regime"
  fi
done

if grep -q 'pattern-recognition-engine' "$SKILL_MD" 2>/dev/null; then
  pass "Pattern Recognition Engine meta-layer referenced"
else
  fail "Pattern Recognition Engine meta-layer referenced"
fi

# ── Block E: References and files ───────────────────────────────────────────
echo ""
echo "--- References & Files ---"
if [ -d "$REF_DIR" ]; then
  pass "references/ directory exists"
else
  fail "references/ directory exists"
fi

REF_COUNT=0
if [ -d "$REF_DIR" ]; then
  REF_COUNT=$(find "$REF_DIR" -maxdepth 1 -name '*.md' | wc -l | tr -d ' ') || REF_COUNT=0
fi
REF_COUNT=${REF_COUNT:-0}
check_num "Reference files on disk >= 9 (found: $REF_COUNT)" "$REF_COUNT" -ge 9

THIN=0
if [ -d "$REF_DIR" ]; then
  for ref in "$REF_DIR"/*.md; do
    [ -f "$ref" ] || continue
    ref_lines=$(wc -l < "$ref" | tr -d ' ')
    if [ "$ref_lines" -lt 80 ]; then
      warn "$(basename "$ref") is only $ref_lines lines (target >= 80)"
      THIN=$((THIN + 1))
    fi
  done
fi
check_num "No thin reference stubs (thin: $THIN)" "$THIN" -le 0

BROKEN=0
for ref in $(grep -oh '(references/[^)]*\.md)' "$SKILL_MD" 2>/dev/null | sed 's|(references/||;s|)||'); do
  if [ -n "$ref" ] && [ ! -f "$REF_DIR/$ref" ]; then
    fail "Broken reference link: references/$ref"
    BROKEN=$((BROKEN + 1))
  fi
done
if [ "$BROKEN" -eq 0 ]; then
  pass "All reference links resolve"
fi

if [ -f "$SKILL_DIR/examples/backtest/README.md" ]; then
  pass "examples/backtest/README.md exists"
else
  fail "examples/backtest/README.md exists"
fi

EXAMPLES_OK=1
EX_DIR="$SKILL_DIR/examples/backtest"
if [ -d "$EX_DIR" ]; then
  grep -rqE '\[VERIFIED\]|\[COMPUTED\]|\[ESTIMATED|\[BROKER-VERIFIED\]' "$EX_DIR" 2>/dev/null || EXAMPLES_OK=0
  grep -rqE '\$[0-9,]+' "$EX_DIR" 2>/dev/null || EXAMPLES_OK=0
  grep -riqE 'best.case|best outcome' "$EX_DIR" 2>/dev/null || EXAMPLES_OK=0
  grep -riqE 'worst.case|worst outcome' "$EX_DIR" 2>/dev/null || EXAMPLES_OK=0
  grep -riqE 'learning|lesson learned|key takeaway' "$EX_DIR" 2>/dev/null || EXAMPLES_OK=0
  check_num "examples/backtest carries tags + dollars + best/worst/learnings" "$EXAMPLES_OK" -eq 1
else
  fail "examples/backtest directory exists"
fi

if [ -x "$SKILL_DIR/scripts/verify-skill.sh" ]; then
  pass "verify-skill.sh is executable"
else
  fail "verify-skill.sh is executable"
fi

# ── Block F: Formatting hygiene ─────────────────────────────────────────────
echo ""
echo "--- Formatting Hygiene ---"
TRAILING=$(grep -rn '[[:space:]]$' "$SKILL_DIR" --include='*.md' --include='*.sh' | wc -l | tr -d ' ') || TRAILING=0
TRAILING=${TRAILING:-0}
check_num "No trailing whitespace (found: $TRAILING)" "$TRAILING" -le 0

TABS=0
while IFS= read -r hit; do
  [ -n "$hit" ] && TABS=$((TABS + 1))
done <<EOF
$(grep -rlP '\t' "$SKILL_DIR" --include='*.md' --include='*.sh' 2>/dev/null || true)
EOF
check_num "No tab characters (found: $TABS)" "$TABS" -le 0

LAST_BYTES=$(tail -c 2 "$SKILL_MD" | od -An -tx1 | tr -d ' \n')
if [ "${LAST_BYTES#*0a0a}" = "$LAST_BYTES" ] && [ "${LAST_BYTES%0a}" != "$LAST_BYTES" ]; then
  pass "SKILL.md ends with exactly one newline"
else
  fail "SKILL.md must end with exactly one newline (last bytes: $LAST_BYTES)"
fi

# ── Summary ─────────────────────────────────────────────────────────────────
echo ""
echo "=============================================="
if [ "$FAILURES" -eq 0 ]; then
  echo "PASS: $SKILL_NAME — all $TOTAL checks passed ($WARNINGS warning(s))"
  exit 0
else
  echo "FAIL: $SKILL_NAME — $FAILURES of $TOTAL check(s) failed ($WARNINGS warning(s))"
  exit 1
fi
