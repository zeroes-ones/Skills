#!/usr/bin/env bash
# ============================================================================
# verify-skill.sh — self-verification for equity-risk-and-capital-engineer
# ============================================================================
# Structural, provenance and gate checks. Bash 3.2 compatible, no third-party
# dependencies, no network. Exits 0 when every check passes, 1 otherwise.
#
# Usage: bash scripts/verify-skill.sh
# ============================================================================
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
SKILL_NAME="$(basename "$SKILL_DIR")"
REF_DIR="$SKILL_DIR/references"
EX_DIR="$SKILL_DIR/examples/backtest"
FAILURES=0
CHECKS=0

pass() { echo "  [PASS] $1"; CHECKS=$((CHECKS + 1)); }
fail() { echo "  [FAIL] $1"; CHECKS=$((CHECKS + 1)); FAILURES=$((FAILURES + 1)); }

count_matches() {
  # $1 = extended regex, $2 = file, $3 = optional -i flag
  local n
  if [ "${3:-}" = "-i" ]; then
    n=$(grep -oiE "$1" "$2" 2>/dev/null | wc -l | tr -d ' ')
  else
    n=$(grep -oE "$1" "$2" 2>/dev/null | wc -l | tr -d ' ')
  fi
  echo "${n:-0}"
}

count_lines() { wc -l < "$1" | tr -d ' '; }

check_section() {
  if grep -q "^## $1" "$SKILL_MD" 2>/dev/null; then
    pass "Section: $1"
  else
    fail "Section: $1 — MISSING"
  fi
}

check_ge() {
  # $1 = label, $2 = actual, $3 = minimum
  if [ "$2" -ge "$3" ] 2>/dev/null; then
    pass "$1: $2 (minimum $3)"
  else
    fail "$1: $2 (need at least $3)"
  fi
}

echo "=== Verifying $SKILL_NAME ==="
echo ""

# ── Block A: File existence ───────────────────────────────────────────────
echo "--- File Existence ---"
if [ -f "$SKILL_MD" ]; then pass "SKILL.md exists"; else fail "SKILL.md not found"; exit 1; fi
if [ -d "$REF_DIR" ]; then pass "references/ directory exists"; else fail "references/ directory MISSING"; fi
if [ -f "$EX_DIR/README.md" ]; then pass "examples/backtest/README.md exists"; else fail "examples/backtest/README.md MISSING"; fi
if [ -x "$SKILL_DIR/scripts/verify-skill.sh" ]; then pass "verify-skill.sh is executable"; else fail "verify-skill.sh is NOT executable (chmod +x)"; fi

# ── Block B: Required level-2 sections (23) ────────────────────────────────
echo ""
echo "--- Required Sections (23) ---"
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

# ── Block C: Frontmatter ───────────────────────────────────────────────────
echo ""
echo "--- YAML Frontmatter ---"
NAME_FIELD=$(grep -m1 '^name:' "$SKILL_MD" 2>/dev/null | awk '{print $2}' || true)
if [ "$NAME_FIELD" = "$SKILL_NAME" ]; then
  pass "name '$NAME_FIELD' matches directory '$SKILL_NAME'"
else
  fail "name '$NAME_FIELD' does not match directory '$SKILL_NAME'"
fi
for field in description license author type status version updated token_budget; do
  if grep -q "^$field:" "$SKILL_MD" 2>/dev/null; then
    pass "frontmatter field: $field"
  else
    fail "frontmatter field missing: $field"
  fi
done
for field in consumes_from feeds_into examples; do
  if grep -q "$field" "$SKILL_MD" 2>/dev/null; then
    pass "chain.$field present"
  else
    fail "chain.$field MISSING"
  fi
done
if grep -q 'feeds_into: \[equity-position-lifecycle\]' "$SKILL_MD" 2>/dev/null; then
  pass "chain.feeds_into is exactly [equity-position-lifecycle]"
else
  fail "chain.feeds_into is not the required exact block"
fi
if grep -q 'skills/14-finance/equity-risk-and-capital-engineer/examples/backtest' "$SKILL_MD" 2>/dev/null; then
  pass "chain.examples path points at this skill's backtest directory"
else
  fail "chain.examples path missing or wrong"
fi

# ── Block D: Structure and quality gates ───────────────────────────────────
echo ""
echo "--- Content Quality ---"

DT_COUNT=$(sed -n '/^## Decision Trees/,/^## Core Workflow/p' "$SKILL_MD" | grep -c '^### ' || true)
check_ge "Decision tree sub-headings" "${DT_COUNT:-0}" 3

DT_GLYPHS=$(sed -n '/^## Decision Trees/,/^## Core Workflow/p' "$SKILL_MD" | grep -oE '├|└|│|┌|→|->|──' | wc -l | tr -d ' ')
check_ge "Decision tree branch glyphs" "${DT_GLYPHS:-0}" 8

FENCES=$(sed -n '/^## Decision Trees/,/^## Core Workflow/p' "$SKILL_MD" | grep -c '^```' || true)
check_ge "Decision tree code fences" "${FENCES:-0}" 2

DT_SECTION_COUNT=$(grep -c '^### DT' "$SKILL_MD" || true)
check_ge "Numbered decision trees (### DTn)" "${DT_SECTION_COUNT:-0}" 3

check_ge "Dollar figures" "$(count_matches '\$[0-9][0-9,]*' "$SKILL_MD")" 5
check_ge "QUICK markers" "$(count_matches 'QUICK: 30s' "$SKILL_MD")" 3
check_ge "STANDARD markers" "$(count_matches 'STANDARD: 3min' "$SKILL_MD")" 3
check_ge "DEEP markers" "$(count_matches 'DEEP: 10' "$SKILL_MD")" 1
check_ge "'Complete when' statements" "$(count_matches 'Complete when' "$SKILL_MD")" 8

if grep -q "Mechanical Trigger" "$SKILL_MD"; then pass "Ground Rules: Mechanical Trigger column"; else fail "Ground Rules: Missing Mechanical Trigger column"; fi
if grep -q "Violation Response" "$SKILL_MD"; then pass "Ground Rules: Violation Response column"; else fail "Ground Rules: Missing Violation Response column"; fi
if grep -q '^| Upstream Skill |' "$SKILL_MD"; then pass "Cross-Skill Coordination: Upstream table header"; else fail "Cross-Skill Coordination: missing '| Upstream Skill |' table"; fi
if grep -q "Portability target" "$SKILL_MD"; then pass "Portability target declared"; else fail "Missing Portability target declaration"; fi
if grep -q '^\*\*Downstream' "$SKILL_MD" || grep -q '### Downstream' "$SKILL_MD"; then pass "Cross-Skill Coordination: Downstream table present"; else fail "Cross-Skill Coordination: Downstream table missing"; fi

BP_COUNT=$(sed -n '/^## Best Practices/,/^## Error Decoder/p' "$SKILL_MD" | grep -cE '^[0-9]+\. ' || true)
check_ge "Best Practices numbered items" "${BP_COUNT:-0}" 10

CR_COUNT=$(sed -n '/^## Production Checklist/,/^## What Good Looks Like/p' "$SKILL_MD" | grep -oE 'CR[0-9]+' | wc -l | tr -d ' ')
check_ge "Production Checklist CR items" "${CR_COUNT:-0}" 10

CROSS_COUNT=$(sed -n '/^## Anti-Patterns/,/^## State Log/p' "$SKILL_MD" | grep -c '❌' || true)
check_ge "Anti-Patterns entries" "${CROSS_COUNT:-0}" 5

ED_COLS=$(sed -n '/^## Error Decoder/,/^## Error Recovery/p' "$SKILL_MD" | grep -m1 '^|' | awk -F'|' '{print NF-2}')
check_ge "Error Decoder columns" "${ED_COLS:-0}" 4

# ── Block E: Anti-hallucination guardrails ──────────────────────────────────
echo ""
echo "--- Anti-Hallucination ---"
for phrase in "Admit uncertainty" "Flag your knowledge cutoff" "Never guess security" "\[VERIFIED\]"; do
  if grep -q "$phrase" "$SKILL_MD" 2>/dev/null; then
    pass "guardrail phrase present: $(echo "$phrase" | sed 's/\\//g')"
  else
    fail "guardrail phrase MISSING: $phrase"
  fi
done
if grep -q '^## Anti-Hallucination$' "$SKILL_MD"; then
  pass "Anti-Hallucination is a level-2 heading"
else
  fail "Anti-Hallucination heading must be exactly '## Anti-Hallucination'"
fi
if grep -qi 'knowledge cutoff' "$SKILL_MD"; then pass "knowledge cutoff declared"; else fail "knowledge cutoff not declared"; fi

# ── Block F: Tag discipline ────────────────────────────────────────────────
echo ""
echo "--- Tag Discipline ---"
VERIFIED_ANY=$(grep -oE '\[VERIFIED —[^]]*\]' "$SKILL_MD" | grep -v 'name it' | wc -l | tr -d ' ')
VERIFIED_SOURCED=$(grep -oE '\[VERIFIED —[^]]*\]' "$SKILL_MD" | grep -v 'name it' | grep -cE '(CFR|FINRA Rule|IRC §|U\.S\.C\.|SEC Release|Nasdaq Rule|Indices Methodology|FTSE Russell)' || true)
VERIFIED_ANY=${VERIFIED_ANY:-0}
VERIFIED_SOURCED=${VERIFIED_SOURCED:-0}
if [ "${VERIFIED_ANY:-0}" -gt 0 ] && [ "${VERIFIED_SOURCED:-0}" -ge "${VERIFIED_ANY:-0}" ]; then
  pass "every citation-style [VERIFIED — ...] names a checkable source ($VERIFIED_SOURCED of $VERIFIED_ANY)"
else
  fail "[VERIFIED — ...] citations without a named source: $(( ${VERIFIED_ANY:-0} - ${VERIFIED_SOURCED:-0} ))"
fi
BARE_VERIFIED=$(grep -c '\[VERIFIED\]' "$SKILL_MD" || true)
pass "bare '[VERIFIED]' occurrences: ${BARE_VERIFIED:-0} (tag-definition prose only; the citation-style test above is the gate)"
if grep -qE '\[VERIFIED — 12 CFR' "$SKILL_MD"; then pass "CFR citation carries its section reference"; else fail "CFR citation missing section reference"; fi
if grep -qE '\[VERIFIED — FINRA Rule' "$SKILL_MD"; then pass "FINRA rule citation present"; else fail "FINRA rule citation missing"; fi
if grep -qi 'could not be verified\|could not find\|not verif' "$SKILL_MD"; then
  pass "unverified claims are labelled as unverified"
else
  fail "no explicit unverified-claim disclosure found"
fi
if grep -qi 'not a regulatory requirement\|broker-set, not regulatory\|\[BROKER-VERIFIED\]' "$SKILL_MD"; then
  pass "portfolio-margin minimum labelled broker-set"
else
  fail "portfolio-margin minimum not labelled broker-set"
fi

# ── Block G: G14 depth gates ────────────────────────────────────────────────
echo ""
echo "--- G14 Depth (finance thresholds) ---"
PROV=$(count_matches '\[VERIFIED|\[COMPUTED|\[ESTIMATED|\[BROKER-VERIFIED|\[COMMON-PRACTICE' "$SKILL_MD")
check_ge "Provenance tags" "${PROV:-0}" 9

BULL=$(count_matches 'bull market|bull regime|bul regime|uptrend' "$SKILL_MD" -i)
CORR=$(count_matches 'correction|pullback|decline' "$SKILL_MD" -i)
BEAR=$(count_matches 'bear market|bear regime|downturn|drawdown|recession' "$SKILL_MD" -i)
CRASH=$(count_matches 'crash|black swan|black-swan|tail event|mar 2020|march 2020|market collapse' "$SKILL_MD" -i)
REGIMES=0
[ "${BULL:-0}" -gt 0 ] && REGIMES=$((REGIMES + 1))
[ "${CORR:-0}" -gt 0 ] && REGIMES=$((REGIMES + 1))
[ "${BEAR:-0}" -gt 0 ] && REGIMES=$((REGIMES + 1))
[ "${CRASH:-0}" -gt 0 ] && REGIMES=$((REGIMES + 1))
check_ge "Regime coverage (of 4; bull=$BULL correction=$CORR bear=$BEAR crash=$CRASH)" "$REGIMES" 3

CITE=$(count_matches 'source.*:|data from|verified against|CBOE|Yahoo Finance|Bloomberg|published by|exchange rules' "$SKILL_MD" -i)
check_ge "Research citations (source lines and named sources)" "${CITE:-0}" 8

# Mirrors G14's own failure-mode pattern. In POSIX bracket expressions the backslash is literal,
# so G14's `[\s-]` is written here as `[ -]` to mean the same set Python's re sees (whitespace or hyphen).
FAILMODE=$(count_matches 'failure[ -]mode|what[ -].*go[ -].*wrong|when[ -].*fails|when[ -].*break|loses[ -].*money|worst[ -]case|exit[ -]condition|stop[ -]loss|close[ -]position|edge[ -]case|known[ -]limitation|what[ -].*break' "$SKILL_MD" -i)
check_ge "Failure-mode matches" "${FAILMODE:-0}" 9

FM_LIST=$(sed -n '/^## Core Workflow/,$p' "$SKILL_MD" | grep -cE '^[0-9]+\. \*\*' || true)
check_ge "Numbered failure modes in reference files" "$(cat "$REF_DIR"/*.md | grep -cE '^[0-9]+\. \*\*' || true)" 10

if grep -q 'stop-loss\|stop loss\|exit condition\|exit plan' "$SKILL_MD"; then
  pass "exit conditions / exit plan documented"
else
  fail "no exit conditions documented"
fi

# ── Block H: References and files ───────────────────────────────────────────
echo ""
echo "--- References & Files ---"
REF_COUNT=$(find "$REF_DIR" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
check_ge "Reference files on disk" "${REF_COUNT:-0}" 9

THIN=0
for f in "$REF_DIR"/*.md; do
  [ -f "$f" ] || continue
  n=$(count_lines "$f")
  if [ "$n" -lt 80 ]; then
    echo "  [FAIL] Reference file under 80 lines: $(basename "$f") ($n lines)"
    FAILURES=$((FAILURES + 1)); CHECKS=$((CHECKS + 1)); THIN=$((THIN + 1))
  fi
done
if [ "$THIN" -eq 0 ]; then pass "every reference file has at least 80 lines of content"; fi

BROKEN=0
for ref in $(grep -ohE '\(references/[^)]*\.md\)' "$SKILL_MD" 2>/dev/null | sed 's|(references/||;s|)||' || true); do
  if [ -n "$ref" ] && [ ! -f "$REF_DIR/$ref" ]; then
    echo "  [FAIL] Broken reference link: references/$ref"
    BROKEN=$((BROKEN + 1))
  fi
done
if [ "$BROKEN" -eq 0 ]; then pass "all reference links resolve (0 broken)"; else FAILURES=$((FAILURES + BROKEN)); CHECKS=$((CHECKS + BROKEN)); fi

LINKED=$(grep -ohE '\(references/[^)]*\.md\)' "$SKILL_MD" 2>/dev/null | sort -u | wc -l | tr -d ' ')
if [ "${LINKED:-0}" -ge "${REF_COUNT:-0}" ]; then
  pass "every reference file is linked from SKILL.md ($LINKED linked, $REF_COUNT on disk)"
else
  fail "unlinked reference files: $(( REF_COUNT - LINKED ))"
fi

# ── Block I: The reserve floor worked example ───────────────────────────────
echo ""
echo "--- Reserve Floor Worked Example ---"
for token in '0.15 × NAV' '0.50 × WCSD' '1.5' 'R_tail' 'BINDING TERM' '190,000' '120,000' '70,000' 'BLOCKED' 'ALLOWED'; do
  if grep -q "$token" "$SKILL_MD" 2>/dev/null; then
    pass "worked example token present: $token"
  else
    fail "worked example token MISSING: $token"
  fi
done
if grep -q 'reserve_floor = max(0.15 × NAV, 0.50 × WCSD, 1.5 × exit_cost' "$SKILL_MD" 2>/dev/null; then
  pass "reserve floor formula stated in full"
else
  fail "reserve floor formula not stated in full"
fi
if grep -q 'worst liquidity first' "$SKILL_MD"; then
  pass "the wrong forced-selling order is named and rejected"
else
  fail "the wrong forced-selling order ('worst liquidity first') is not named"
fi

# ── Block J: The four clocks ────────────────────────────────────────────────
echo ""
echo "--- The Four Clocks ---"
for token in 'T+1' '34-96930' '220.4(c)(3)(i)' 'IRC §1222' 'IRC §1091' '78p(b)' '242.204(a)' '242.203(b)(3)'; do
  if grep -q "$token" "$SKILL_MD" 2>/dev/null; then
    pass "clock citation present: $token"
  else
    fail "clock citation MISSING: $token"
  fi
done

# ── Block K: Scope discipline ───────────────────────────────────────────────
echo ""
echo "--- Scope Discipline ---"
if grep -qi 'not you' "$SKILL_MD"; then
  pass "the insider/institutional scope line is stated ('not you')"
else
  fail "the insider/institutional scope statement is missing"
fi
if grep -qi '180.calendar.day\|180-day' "$SKILL_MD"; then
  if grep -qi '180.*could NOT be verified\|could not be verified' "$SKILL_MD"; then
    pass "the 180-day bid-price cure is flagged unverified"
  else
    fail "the 180-day bid-price cure is asserted without an unverified flag"
  fi
else
  fail "the 180-day bid-price cure is not addressed at all"
fi
for defer in 'equity-position-lifecycle' 'equity-tax-lot-and-exit-management' 'portfolio-signal-manager' 'algorithmic-trader' 'fundamental-analyst' 'options-risk-engineer'; do
  if grep -q "$defer" "$SKILL_MD" 2>/dev/null; then
    pass "defers to: $defer"
  else
    fail "no deferral to: $defer"
  fi
done

# ── Summary ────────────────────────────────────────────────────────────────
echo ""
echo "=============================================="
if [ "$FAILURES" -eq 0 ]; then
  echo "OK  $SKILL_NAME: all $CHECKS checks passed"
  exit 0
else
  echo "FAIL $SKILL_NAME: $FAILURES of $CHECKS check(s) failed"
  exit 1
fi
