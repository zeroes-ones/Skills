#!/usr/bin/env bash
# ============================================================================
# verify-skill.sh — self-verification for trading-decision-data-catalogue
# ============================================================================
# Structural, provenance, depth and orphan-reference checks. Bash 3.2
# compatible, no third-party dependencies, no network, no git.
# Exits 0 when every check passes, 1 otherwise.
#
#   Usage: bash scripts/verify-skill.sh
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
  # $1 = extended regex, $2 = file, $3 = optional -i
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
  if grep -q "^## $1\$" "$SKILL_MD" 2>/dev/null; then
    pass "Section: $1"
  else
    fail "Section: $1 — MISSING or not an exact level-2 heading"
  fi
}

check_ge() {
  # $1 = label, $2 = actual, $3 = minimum
  if [ "${2:-0}" -ge "$3" ] 2>/dev/null; then
    pass "$1: $2 (minimum $3)"
  else
    fail "$1: ${2:-0} (need at least $3)"
  fi
}

check_token() {
  # $1 = token, $2 = human label
  if grep -qF "$1" "$SKILL_MD" 2>/dev/null; then
    pass "$2 present"
  else
    fail "$2 MISSING: $1"
  fi
}

echo "=== Verifying $SKILL_NAME ==="
echo ""

# ── Block A: File existence ────────────────────────────────────────────────
echo "--- File Existence ---"
if [ -f "$SKILL_MD" ]; then pass "SKILL.md exists"; else fail "SKILL.md not found"; exit 1; fi
if [ -d "$REF_DIR" ]; then pass "references/ directory exists"; else fail "references/ directory MISSING"; fi
if [ -f "$EX_DIR/README.md" ]; then pass "examples/backtest/README.md exists"; else fail "examples/backtest/README.md MISSING"; fi
if [ -x "$SKILL_DIR/scripts/verify-skill.sh" ]; then pass "verify-skill.sh is executable"; else fail "verify-skill.sh is NOT executable (chmod +x)"; fi

# ── Block B: The 23 required level-2 headings ──────────────────────────────
echo ""
echo "--- Required Level-2 Headings (23) ---"
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

# ── Block C: Frontmatter and the chain block ────────────────────────────────
echo ""
echo "--- YAML Frontmatter ---"
NAME_FIELD=$(grep -m1 '^name:' "$SKILL_MD" 2>/dev/null | awk '{print $2}' || true)
if [ "$NAME_FIELD" = "$SKILL_NAME" ]; then
  pass "name '$NAME_FIELD' matches directory '$SKILL_NAME'"
else
  fail "name '$NAME_FIELD' does not match directory '$SKILL_NAME'"
fi
for field in description license author type status version updated token_budget tags; do
  if grep -q "^$field:" "$SKILL_MD" 2>/dev/null; then
    pass "frontmatter field: $field"
  else
    fail "frontmatter field missing: $field"
  fi
done
if grep -q '^type: finance$' "$SKILL_MD" 2>/dev/null; then
  pass "type is finance"
else
  fail "type is not 'finance'"
fi
DESC_LEN=$(sed -n '/^description:/,/^[a-z_]*:/p' "$SKILL_MD" | awk 'NR>1 && /^[a-z_]*:/{exit} {printf "%s ", $0}' | sed 's/description:[[:space:]]*//' | wc -c | tr -d ' ')
if [ "${DESC_LEN:-0}" -le 1024 ]; then
  pass "description length ${DESC_LEN} chars (maximum 1024)"
else
  fail "description is ${DESC_LEN} chars (maximum 1024)"
fi
for phrase in "Use when" "Handles" "Do NOT use"; do
  if sed -n '/^description:/,/^license:/p' "$SKILL_MD" | grep -qF "$phrase"; then
    pass "description trigger phrase: $phrase"
  else
    fail "description missing trigger phrase: $phrase"
  fi
done
if grep -q 'feeds_into: \[equity-position-lifecycle, options-position-lifecycle, market-data-engineer\]' "$SKILL_MD" 2>/dev/null; then
  pass "chain.feeds_into is exactly the required block"
else
  fail "chain.feeds_into is not the required exact block"
fi
if grep -q '^  consumes_from: \[\]$' "$SKILL_MD" 2>/dev/null; then
  pass "chain.consumes_from is exactly []"
else
  fail "chain.consumes_from is not the required empty list"
fi
if grep -q 'skills/14-finance/trading-decision-data-catalogue/examples/backtest' "$SKILL_MD" 2>/dev/null; then
  pass "chain.examples points at this skill's backtest directory"
else
  fail "chain.examples path missing or wrong"
fi

# ── Block D: Structure and content quality ──────────────────────────────────
echo ""
echo "--- Content Quality ---"

DT_COUNT=$(sed -n '/^## Decision Trees/,/^## Core Workflow/p' "$SKILL_MD" | grep -c '^### ' || true)
check_ge "Decision-tree sub-headings" "${DT_COUNT:-0}" 3

DT_GLYPHS=$(sed -n '/^## Decision Trees/,/^## Core Workflow/p' "$SKILL_MD" | grep -oE '├|└|│|→|▼' | wc -l | tr -d ' ')
check_ge "Decision-tree branch glyphs" "${DT_GLYPHS:-0}" 8

DT_FENCES=$(sed -n '/^## Decision Trees/,/^## Core Workflow/p' "$SKILL_MD" | grep -c '^```' || true)
check_ge "Decision-tree code fences" "${DT_FENCES:-0}" 2

check_ge "Dollar figures" "$(count_matches '\$[0-9][0-9,]*' "$SKILL_MD")" 5
check_ge "QUICK markers" "$(count_matches 'QUICK: 30s' "$SKILL_MD")" 3
check_ge "STANDARD markers" "$(count_matches 'STANDARD: 3min' "$SKILL_MD")" 3
check_ge "DEEP markers" "$(count_matches 'DEEP: 10' "$SKILL_MD")" 1
check_ge "'Complete when' statements" "$(count_matches 'Complete when' "$SKILL_MD")" 8

if grep -q "Mechanical Trigger" "$SKILL_MD"; then pass "Ground Rules: Mechanical Trigger column"; else fail "Ground Rules: missing Mechanical Trigger column"; fi
if grep -q "Violation Response" "$SKILL_MD"; then pass "Ground Rules: Violation Response column"; else fail "Ground Rules: missing Violation Response column"; fi
if grep -q '^| Upstream Skill |' "$SKILL_MD"; then pass "Cross-Skill Coordination: Upstream table header"; else fail "Cross-Skill Coordination: missing '| Upstream Skill |' table"; fi
if grep -q '^### Downstream' "$SKILL_MD"; then pass "Cross-Skill Coordination: Downstream table present"; else fail "Cross-Skill Coordination: Downstream table missing"; fi
if grep -q "Portability target" "$SKILL_MD"; then pass "Portability target declared"; else fail "Missing Portability target declaration"; fi

BP_COUNT=$(sed -n '/^## Best Practices/,/^## Error Decoder/p' "$SKILL_MD" | grep -cE '^[0-9]+\. ' || true)
check_ge "Best Practices numbered items" "${BP_COUNT:-0}" 10

CR_COUNT=$(sed -n '/^## Production Checklist/,/^## What Good Looks Like/p' "$SKILL_MD" | grep -oE 'CR[0-9]+' | wc -l | tr -d ' ')
check_ge "Production Checklist CR items" "${CR_COUNT:-0}" 10

AP_COUNT=$(sed -n '/^## Anti-Patterns/,/^## State Log/p' "$SKILL_MD" | grep -c '❌' || true)
check_ge "Anti-Patterns entries" "${AP_COUNT:-0}" 5

ED_COLS=$(sed -n '/^## Error Decoder/,/^## Error Recovery/p' "$SKILL_MD" | grep -m1 '^|' | awk -F'|' '{print NF-2}')
check_ge "Error Decoder columns" "${ED_COLS:-0}" 4

FM_ITEMS=$(sed -n '/^### Failure Modes/,/^## Best Practices/p' "$SKILL_MD" | grep -cE '^[0-9]+\. \*\*' || true)
check_ge "Numbered failure modes in SKILL.md" "${FM_ITEMS:-0}" 10

# ── Block E: The three kinds and the catalogue contract ─────────────────────
echo ""
echo "--- The Three Kinds ---"
for kind in "SIGNAL" "STATE" "CONSTRAINT"; do
  if grep -q "\*\*$kind\*\*" "$SKILL_MD" 2>/dev/null; then
    pass "kind defined: $kind"
  else
    fail "kind not defined as an emphasised term: $kind"
  fi
done
check_token "The Three Kinds" "three-kinds section"
check_token "nice-to-know" "the nice-to-know demotion rule"
check_token "a catalogue that ranks everything as useful is worthless" "the anti-ranking rule, stated verbatim"
for field in "Question it answers" "Kind" "Exact source" "Cost" "Update frequency" "How it lies" "What decision it changes" "Timestamp rule" "Rank"; do
  if grep -qF "$field" "$SKILL_MD" 2>/dev/null; then
    pass "catalogue record field: $field"
  else
    fail "catalogue record field MISSING: $field"
  fi
done

# ── Block F: Anti-hallucination guardrails ──────────────────────────────────
echo ""
echo "--- Anti-Hallucination ---"
for phrase in "Admit uncertainty" "Flag your knowledge cutoff" "Never guess security" "\[VERIFIED\]"; do
  if grep -qE "$phrase" "$SKILL_MD" 2>/dev/null; then
    pass "guardrail phrase present: $(echo "$phrase" | sed 's/\\//g')"
  else
    fail "guardrail phrase MISSING: $phrase"
  fi
done
if grep -q '^## Anti-Hallucination$' "$SKILL_MD"; then
  pass "Anti-Hallucination is an exact level-2 heading"
else
  fail "Anti-Hallucination heading must be exactly '## Anti-Hallucination'"
fi
if grep -qi 'knowledge cutoff' "$SKILL_MD"; then pass "knowledge cutoff declared"; else fail "knowledge cutoff not declared"; fi
if grep -q '^## Anti-Hallucination' "$SKILL_MD" && [ "$(grep -c '^## Anti-Hallucination' "$SKILL_MD")" -eq 1 ]; then
  pass "Anti-Hallucination appears exactly once (no duplicate level-2 headings)"
else
  fail "Anti-Hallucination heading missing or duplicated"
fi

# ── Block G: Tag discipline ─────────────────────────────────────────────────
echo ""
echo "--- Tag Discipline ---"
VERIFIED_ANY=$(grep -oE '\[VERIFIED —[^]]*\]' "$SKILL_MD" | wc -l | tr -d ' ')
VERIFIED_SOURCED=$(grep -oE '\[VERIFIED —[^]]*\]' "$SKILL_MD" | grep -cE '(CFR|FINRA|SEC|Federal Reserve|CFTC|Cboe|FRED|ALFRED|Atlanta Fed|Treasury|FTSE Russell|Indices Methodology|NYSE|Nasdaq|FR 2025|Accessing EDGAR|documentation|pricing page|Unusual Whales)' || true)
VERIFIED_ANY=${VERIFIED_ANY:-0}
VERIFIED_SOURCED=${VERIFIED_SOURCED:-0}
if [ "$VERIFIED_ANY" -gt 0 ] && [ "$VERIFIED_SOURCED" -ge "$VERIFIED_ANY" ]; then
  pass "every citation-style [VERIFIED — ...] names a checkable source ($VERIFIED_SOURCED of $VERIFIED_ANY)"
else
  fail "[VERIFIED — ...] citations without a named source: $(( VERIFIED_ANY - VERIFIED_SOURCED ))"
fi
for tag in "\[COMPUTED\]" "\[ESTIMATED" "\[BROKER-VERIFIED\]" "\[COMMON-PRACTICE\]" "\[ILLUSTRATIVE\]"; do
  if grep -qE "$tag" "$SKILL_MD" 2>/dev/null; then
    pass "provenance tag in use: $(echo "$tag" | sed 's/\\//g')"
  else
    fail "provenance tag never used: $tag"
  fi
done
if grep -qi 'could not be verified\|not verified\|could not find\|not verif' "$SKILL_MD"; then
  pass "unverified claims are labelled as unverified"
else
  fail "no explicit unverified-claim disclosure found"
fi
if grep -qF 'exempt until Jan 2, 2028' "$SKILL_MD" && grep -qF 'FR 2025-22158' "$SKILL_MD"; then
  pass "the Form SHO / Rule 13f-2 2028 exemption is stated with its release"
else
  fail "the Form SHO / Rule 13f-2 exemption is missing or unsourced"
fi
if grep -qF 'Sept 28, 2028' "$SKILL_MD" && grep -qF 'March 29, 2029' "$SKILL_MD"; then
  pass "the Rule 10c-1a exemption and dissemination dates are stated"
else
  fail "the Rule 10c-1a exemption dates are missing"
fi
if grep -qi 'not a regulatory requirement\|broker-set' "$SKILL_MD" || grep -qF '[BROKER-VERIFIED]' "$SKILL_MD"; then
  pass "broker-set values are labelled rather than asserted as rules"
else
  fail "broker-set values are not labelled"
fi

# ── Block H: G14 depth gates ────────────────────────────────────────────────
echo ""
echo "--- G14 Depth (finance thresholds) ---"
PROV=$(count_matches '\[VERIFIED|\[COMPUTED|\[ESTIMATED|\[BROKER-VERIFIED|\[COMMON-PRACTICE' "$SKILL_MD")
check_ge "Provenance-tagged lines" "${PROV:-0}" 9

BULL=$(count_matches 'bull market|bull regime|uptrend' "$SKILL_MD" -i)
CORR=$(count_matches 'correction|pullback' "$SKILL_MD" -i)
BEAR=$(count_matches 'bear market|downturn|drawdown|recession' "$SKILL_MD" -i)
CRASH=$(count_matches 'crash|tail event|black swan|march 2020|market collapse' "$SKILL_MD" -i)
REGIMES=0
[ "${BULL:-0}" -gt 0 ] && REGIMES=$((REGIMES + 1))
[ "${CORR:-0}" -gt 0 ] && REGIMES=$((REGIMES + 1))
[ "${BEAR:-0}" -gt 0 ] && REGIMES=$((REGIMES + 1))
[ "${CRASH:-0}" -gt 0 ] && REGIMES=$((REGIMES + 1))
check_ge "Regime coverage (of 4; bull=$BULL correction=$CORR bear=$BEAR crash=$CRASH)" "$REGIMES" 3

CITE=$(count_matches 'source.*:|data from|verified against|Cboe|Yahoo Finance|Bloomberg|published by|exchange rules' "$SKILL_MD" -i)
check_ge "Research citations (source lines and named publishers)" "${CITE:-0}" 8

FAILMODE=$(count_matches 'failure[ -]mode|what[ -].*go[ -].*wrong|when[ -].*fails|when[ -].*break|worst[ -]case|exit[ -]condition|stop[ -]loss|close[ -]position|edge[ -]case|known[ -]limitation|what[ -].*break' "$SKILL_MD" -i)
check_ge "Failure-mode matches" "${FAILMODE:-0}" 9

if grep -qi 'exit condition' "$SKILL_MD"; then
  pass "exit conditions documented"
else
  fail "no exit conditions documented"
fi
if grep -qE '\$[0-9][0-9,]*\s*(loss|cost|risk|value|premium|debit|credit|gain|saved|worth)' "$SKILL_MD"; then
  pass "dollar-quantified example present"
else
  fail "no dollar-quantified example"
fi

# ── Block I: References, line counts and the orphan check ───────────────────
echo ""
echo "--- References & Orphan Check ---"
REF_COUNT=$(find "$REF_DIR" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
check_ge "Reference files on disk" "${REF_COUNT:-0}" 12

THIN=0
for f in "$REF_DIR"/*.md; do
  [ -f "$f" ] || continue
  n=$(count_lines "$f")
  if [ "$n" -lt 90 ]; then
    echo "  [FAIL] Reference file under 90 lines: $(basename "$f") ($n lines)"
    FAILURES=$((FAILURES + 1)); CHECKS=$((CHECKS + 1)); THIN=$((THIN + 1))
  fi
done
if [ "$THIN" -eq 0 ]; then pass "every reference file carries at least 90 lines of content"; fi

BROKEN=0
for ref in $(grep -ohE '\(references/[^)]*\.md\)' "$SKILL_MD" 2>/dev/null | sed 's|(references/||;s|)||' || true); do
  if [ -n "$ref" ] && [ ! -f "$REF_DIR/$ref" ]; then
    echo "  [FAIL] Broken reference link: references/$ref"
    BROKEN=$((BROKEN + 1))
  fi
done
if [ "$BROKEN" -eq 0 ]; then pass "all reference links resolve (0 broken)"; else FAILURES=$((FAILURES + BROKEN)); CHECKS=$((CHECKS + BROKEN)); fi

# Orphan check: every reference file on disk must be linked from SKILL.md, and the
# examples README must be linked too. A file nobody can navigate to is dead weight.
ORPHANS=0
for f in "$REF_DIR"/*.md "$EX_DIR/README.md"; do
  [ -f "$f" ] || continue
  base=$(basename "$f")
  if [ "$base" = "README.md" ]; then
    if ! grep -qF 'examples/backtest/README.md' "$SKILL_MD"; then
      echo "  [FAIL] Orphan file (never linked from SKILL.md): examples/backtest/README.md"
      ORPHANS=$((ORPHANS + 1))
    fi
  else
    if ! grep -qF "(references/$base)" "$SKILL_MD"; then
      echo "  [FAIL] Orphan reference (never linked from SKILL.md): references/$base"
      ORPHANS=$((ORPHANS + 1))
    fi
  fi
done
if [ "$ORPHANS" -eq 0 ]; then pass "orphan check: no unlinked reference or example file"; else FAILURES=$((FAILURES + ORPHANS)); CHECKS=$((CHECKS + ORPHANS)); fi

for required in decision-to-data-map.md options-positioning-data.md equity-ownership-and-short-data.md insider-and-filing-data.md macro-and-liquidity-data.md constraint-data-and-calendars.md alternative-data-and-base-rates.md text-and-language-data.md data-quality-traps.md signal-validation-protocol.md free-and-underused-sources.md overrated-datasets.md; do
  if [ -f "$REF_DIR/$required" ]; then
    pass "required reference present: $required"
  else
    fail "required reference MISSING: $required"
  fi
done

# ── Block J: The two ranked lists ────────────────────────────────────────────
echo ""
echo "--- The Two Ranked Lists ---"
BEST_ROWS=$(grep -cE '^\| \*\*[0-9]+\*\* \|' "$REF_DIR/decision-to-data-map.md" || true)
check_ge "Best-datasets ranked rows (decision-to-data-map.md)" "${BEST_ROWS:-0}" 12
OVER_ROWS=$(grep -cE '^\| \*\*[0-9]+\*\* \|' "$REF_DIR/overrated-datasets.md" || true)
check_ge "Over-rated ranked rows (overrated-datasets.md)" "${OVER_ROWS:-0}" 12
if grep -qF 'ranked best first' "$SKILL_MD"; then
  pass "the best-first ranking is declared"
else
  fail "the best-first ranking is not declared in SKILL.md"
fi
if grep -qi 'over-rated\|overrated' "$REF_DIR/overrated-datasets.md"; then
  pass "the over-rated list is titled and maintained"
else
  fail "the over-rated list is missing"
fi
for token in 'Ranked Best First' 'Ranked'; do
  if grep -q "$token" "$REF_DIR/decision-to-data-map.md" 2>/dev/null; then
    pass "ranking declared in decision-to-data-map.md: $token"
    break
  fi
done

# ── Block K: The verified facts ─────────────────────────────────────────────
echo ""
echo "--- Verified Facts (each must survive a re-read) ---"
check_token "FR 2025-22158" "the exemptive-order citation"
check_token "Jan 2, 2028" "Form SHO / Rule 13f-2 effective date"
check_token "Sept 28, 2028" "Rule 10c-1a exemption date"
check_token "March 29, 2029" "FINRA dissemination date"
check_token "may result from either a short or a long sale" "the SEC's fail statement, verbatim"
check_token "is not necessarily a violation" "the SEC's naked-short-selling statement, verbatim"
check_token "FINRA Rule 4560" "FINRA short-interest rule"
check_token "7th business day" "the short-interest publication lag"
check_token "Revision Flag" "the short-interest revision flag"
check_token "TRF/ADF/ORF" "the daily short-sale-volume scope"
check_token "10,000 shares" "the threshold-list share leg"
check_token "0.5%" "the threshold-list percentage leg"
check_token "13 consecutive settlement days" "the threshold close-out clock"
check_token "242.204(a)" "the Rule 204 close-out clock citation"
check_token "within 45 days after quarter-end" "the 13F deadline"
check_token "5 business days" "the Schedule 13D deadline"
check_token "2 business days" "the Schedule 13D amendment window"
check_token "240.16a-3(g)" "the Form 4 deadline citation"
check_token "10 requests/second" "the EDGAR rate limit"
check_token "not backfilled" "EDGAR's non-backfill property"
check_token "3:30pm ET" "the COT publication time"
check_token "H.4.1" "the Fed balance-sheet release"
check_token "SLOOS" "the loan-officer survey"
check_token "0.77" "the GDPNow mean absolute error"
check_token "1.17" "the GDPNow RMSE"
check_token "ALFRED" "the vintage series"
check_token "Cboe DataShop" "the participant-capacity dataset"
check_token "VIX_History.csv" "the free Cboe index CSV"
check_token "4:15pm ET" "the options close"
check_token "1:00pm ET" "the early close"
check_token "34-96930" "the T+1 settlement release"
check_token "220.4(c)(3)(i)" "the Reg T payment window citation"
check_token "third Friday" "the index rebalance effective date"
check_token "semi-annual" "the Russell cadence change"
check_token "424B" "the only primary source for lock-up terms"

# ── Block L: The traps ──────────────────────────────────────────────────────
echo ""
echo "--- Traps ---"
TRAPS=$(sed -n '/^### The Traps/,/^### Two More/p' "$SKILL_MD" | grep -cE '^\| [0-9]+ \|' || true)
check_ge "Traps table rows (trap, how it bites, how to detect)" "${TRAPS:-0}" 20
if grep -q 'How to detect it' "$SKILL_MD"; then
  pass "traps carry a detection column"
else
  fail "traps table has no detection column"
fi
check_token "How it bites" "the trap-bite column"

# ── Block M: Scope discipline ───────────────────────────────────────────────
echo ""
echo "--- Scope Discipline ---"
if grep -qi 'does not build pipelines\|not build ingestion' "$SKILL_MD"; then
  pass "the build-vs-buy scope line is stated"
else
  fail "the pipeline scope line is missing"
fi
if grep -qi "choosing a security is not this skill" "$SKILL_MD"; then
  pass "the security-selection scope line is stated"
else
  fail "the security-selection scope statement is missing"
fi
for defer in 'market-data-engineer' 'equity-position-lifecycle' 'options-position-lifecycle' 'fundamental-analyst' 'portfolio-signal-manager' 'technical-signals-engineer' 'macro-strategist' 'quantitative-analyst' 'data-scientist' 'trade-performance-analyst'; do
  if grep -q "$defer" "$SKILL_MD" 2>/dev/null; then
    pass "defers to: $defer"
  else
    fail "no deferral to: $defer"
  fi
done

# ── Block N: Examples deliverable ────────────────────────────────────────────
echo ""
echo "--- Examples Deliverable ---"
EX_LINES=$(count_lines "$EX_DIR/README.md")
check_ge "examples/backtest/README.md lines" "${EX_LINES:-0}" 80
if grep -qi 'format, not a result\|is a FORMAT' "$EX_DIR/README.md"; then
  pass "the examples README declares itself a format, not a market result"
else
  fail "the examples README does not disclaim being a market result"
fi
if grep -qi 'grading rubric\|graded' "$EX_DIR/README.md"; then
  pass "the examples README contains a grading rubric"
else
  fail "the examples README has no grading rubric"
fi

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
