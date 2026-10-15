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
    echo "  [FAIL] Section: $1 — MISSING"
    FAILURES=$((FAILURES + 1))
  fi
}

echo "=== Verifying $SKILL_NAME ==="
echo ""

# ── Block A: File existence ──────────────────────────────────────────────
echo "--- File Existence ---"

if [ -f "$SKILL_MD" ]; then
  echo "  [PASS] SKILL.md exists"
else
  echo "  [FAIL] SKILL.md not found"
  exit 1
fi

# ── Block B: Required Sections (22 template sections + Anti-Hallucination) ─
echo ""
echo "--- Required Sections ---"

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
check_section "Verification Guardrails"
check_section "Error Recovery"
check_section "State Log"
check_section "Production Checklist"
check_section "Anti-Rationalization"
check_section "Anti-Hallucination"

# ── Block C: YAML Frontmatter Fields ──────────────────────────────────────
echo ""
echo "--- YAML Frontmatter ---"

NAME_FIELD=$(grep -m1 '^name:' "$SKILL_MD" 2>/dev/null | awk '{print $2}' || echo "")
if [ "$NAME_FIELD" = "$SKILL_NAME" ]; then
  echo "  [PASS] name '$NAME_FIELD' matches directory '$SKILL_NAME'"
else
  echo "  [FAIL] name '$NAME_FIELD' does not match directory '$SKILL_NAME'"
  FAILURES=$((FAILURES + 1))
fi

if grep -q '^description:' "$SKILL_MD"; then
  echo "  [PASS] description field present"
else
  echo "  [FAIL] description field MISSING"
  FAILURES=$((FAILURES + 1))
fi

if grep -q '^version:' "$SKILL_MD"; then
  echo "  [PASS] version field present"
else
  echo "  [FAIL] version field MISSING"
  FAILURES=$((FAILURES + 1))
fi

if grep -q '^license: MIT' "$SKILL_MD"; then
  echo "  [PASS] license: MIT present"
else
  echo "  [FAIL] license: MIT MISSING"
  FAILURES=$((FAILURES + 1))
fi

if grep -q 'consumes_from' "$SKILL_MD"; then
  echo "  [PASS] chain.consumes_from present"
else
  echo "  [FAIL] chain.consumes_from MISSING"
  FAILURES=$((FAILURES + 1))
fi

if grep -q 'feeds_into' "$SKILL_MD"; then
  echo "  [PASS] chain.feeds_into present"
else
  echo "  [FAIL] chain.feeds_into MISSING"
  FAILURES=$((FAILURES + 1))
fi

if grep -q 'examples:' "$SKILL_MD"; then
  echo "  [PASS] chain.examples present"
else
  echo "  [FAIL] chain.examples MISSING"
  FAILURES=$((FAILURES + 1))
fi

# ── Block D: Content Quality Checks ──────────────────────────────────────
echo ""
echo "--- Content Quality ---"

DT_COUNT=$(sed -n '/^## Decision Trees/,/^## Core Workflow/p' "$SKILL_MD" | grep -c '^### ' 2>/dev/null || echo 0)
if [ "$DT_COUNT" -ge 3 ]; then
  echo "  [PASS] Decision trees: $DT_COUNT (minimum 3)"
else
  echo "  [FAIL] Decision trees: $DT_COUNT (need at least 3)"
  FAILURES=$((FAILURES + 1))
fi

BRANCH_GLYPHS=$(grep -c '[├└│▼→]' "$SKILL_MD" 2>/dev/null || echo 0)
if [ "$BRANCH_GLYPHS" -ge 8 ]; then
  echo "  [PASS] ASCII branch glyph lines: $BRANCH_GLYPHS (minimum 8)"
else
  echo "  [FAIL] ASCII branch glyph lines: $BRANCH_GLYPHS (need at least 8)"
  FAILURES=$((FAILURES + 1))
fi

DOLLAR_COUNT=$(grep -c '\$[0-9]' "$SKILL_MD" 2>/dev/null || echo 0)
if [ "$DOLLAR_COUNT" -ge 5 ]; then
  echo "  [PASS] Dollar-quantified references: $DOLLAR_COUNT (minimum 5)"
else
  echo "  [FAIL] Dollar-quantified references: $DOLLAR_COUNT (need at least 5)"
  FAILURES=$((FAILURES + 1))
fi

# Dollar figures in the $1,234 form must each carry a provenance tag.
TAGGED_DOLLARS=$(grep -c '\$[0-9],[0-9]\{3\}' "$SKILL_MD" 2>/dev/null || echo 0)
if [ "$TAGGED_DOLLARS" -ge 5 ]; then
  echo "  [PASS] Thousands-formatted dollar figures: $TAGGED_DOLLARS (minimum 5)"
else
  echo "  [FAIL] Thousands-formatted dollar figures: $TAGGED_DOLLARS (need at least 5)"
  FAILURES=$((FAILURES + 1))
fi

QUICK_COUNT=$(grep -c 'QUICK' "$SKILL_MD" 2>/dev/null || echo 0)
if [ "$QUICK_COUNT" -ge 3 ]; then
  echo "  [PASS] QUICK markers: $QUICK_COUNT (minimum 3)"
else
  echo "  [FAIL] QUICK markers: $QUICK_COUNT (need at least 3)"
  FAILURES=$((FAILURES + 1))
fi

for marker in 'QUICK: 30s' 'STANDARD: 3min' 'DEEP: 10+min'; do
  if grep -qF "$marker" "$SKILL_MD"; then
    echo "  [PASS] Progressive-disclosure marker: $marker"
  else
    echo "  [FAIL] Progressive-disclosure marker MISSING: $marker"
    FAILURES=$((FAILURES + 1))
  fi
done

CW_COUNT=$(grep -ci 'Complete when' "$SKILL_MD" 2>/dev/null || echo 0)
if [ "$CW_COUNT" -ge 8 ]; then
  echo "  [PASS] Complete when statements: $CW_COUNT (minimum 8)"
else
  echo "  [FAIL] Complete when statements: $CW_COUNT (need at least 8)"
  FAILURES=$((FAILURES + 1))
fi

BP_COUNT=$(sed -n '/^## Best Practices/,/^## Error Decoder/p' "$SKILL_MD" | grep -c '^[0-9]\+\. ' 2>/dev/null || echo 0)
if [ "$BP_COUNT" -ge 10 ]; then
  echo "  [PASS] Best Practices numbered items: $BP_COUNT (minimum 10)"
else
  echo "  [FAIL] Best Practices numbered items: $BP_COUNT (need at least 10)"
  FAILURES=$((FAILURES + 1))
fi

CR_COUNT=$(sed -n '/^## Production Checklist/,/^## What Good Looks Like/p' "$SKILL_MD" | grep -c 'CR[0-9]' 2>/dev/null || echo 0)
if [ "$CR_COUNT" -ge 12 ]; then
  echo "  [PASS] Production Checklist items: $CR_COUNT (minimum 12)"
else
  echo "  [FAIL] Production Checklist items: $CR_COUNT (need at least 12)"
  FAILURES=$((FAILURES + 1))
fi

FM_COUNT=$(sed -n '/^### Failure Modes/,/^### Regime Table/p' "$SKILL_MD" | grep -c '^[0-9]\+\. ' 2>/dev/null || echo 0)
if [ "$FM_COUNT" -ge 10 ]; then
  echo "  [PASS] Failure modes: $FM_COUNT (minimum 10)"
else
  echo "  [FAIL] Failure modes: $FM_COUNT (need at least 10)"
  FAILURES=$((FAILURES + 1))
fi

if grep -q "Mechanical Trigger" "$SKILL_MD"; then
  echo "  [PASS] Ground Rules: Mechanical Trigger column"
else
  echo "  [FAIL] Ground Rules: Missing Mechanical Trigger column"
  FAILURES=$((FAILURES + 1))
fi

if grep -q "Violation Response" "$SKILL_MD"; then
  echo "  [PASS] Ground Rules: Violation Response column"
else
  echo "  [FAIL] Ground Rules: Missing Violation Response column"
  FAILURES=$((FAILURES + 1))
fi

if grep -q "Portability target" "$SKILL_MD"; then
  echo "  [PASS] Portability target declared"
else
  echo "  [FAIL] Portability target MISSING"
  FAILURES=$((FAILURES + 1))
fi

if grep -q '| Upstream Skill' "$SKILL_MD"; then
  echo "  [PASS] Cross-Skill Coordination: upstream table"
else
  echo "  [FAIL] Cross-Skill Coordination: upstream table MISSING"
  FAILURES=$((FAILURES + 1))
fi

if grep -q '| Downstream Skill' "$SKILL_MD"; then
  echo "  [PASS] Cross-Skill Coordination: downstream table"
else
  echo "  [FAIL] Cross-Skill Coordination: downstream table MISSING"
  FAILURES=$((FAILURES + 1))
fi

PROV_TAGS=$(grep -c '\[VERIFIED\]\|\[COMPUTED\]\|\[ESTIMATED\]\|\[BROKER-VERIFIED\]\|\[COMMON-PRACTICE\]' "$SKILL_MD" 2>/dev/null || echo 0)
if [ "$PROV_TAGS" -ge 9 ]; then
  echo "  [PASS] Provenance tags: $PROV_TAGS (minimum 9)"
else
  echo "  [FAIL] Provenance tags: $PROV_TAGS (need at least 9)"
  FAILURES=$((FAILURES + 1))
fi

CITE_COUNT=$(grep -ciE 'source:|data from|verified against|CBOE|Yahoo Finance|Bloomberg|published by|exchange rules' "$SKILL_MD" 2>/dev/null || echo 0)
if [ "$CITE_COUNT" -ge 8 ]; then
  echo "  [PASS] Data-source citations: $CITE_COUNT (minimum 8)"
else
  echo "  [FAIL] Data-source citations: $CITE_COUNT (need at least 8)"
  FAILURES=$((FAILURES + 1))
fi

REGIME_COUNT=0
grep -qiE 'bull market|bull regime|uptrend' "$SKILL_MD" && REGIME_COUNT=$((REGIME_COUNT + 1))
grep -qiE 'correction|pullback' "$SKILL_MD" && REGIME_COUNT=$((REGIME_COUNT + 1))
grep -qiE 'bear market|downturn|drawdown|recession' "$SKILL_MD" && REGIME_COUNT=$((REGIME_COUNT + 1))
grep -qiE 'crash|tail event|black swan|black-swan|march 2020|market collapse' "$SKILL_MD" && REGIME_COUNT=$((REGIME_COUNT + 1))
if [ "$REGIME_COUNT" -ge 3 ]; then
  echo "  [PASS] Market regimes referenced: $REGIME_COUNT/4 (minimum 3)"
else
  echo "  [FAIL] Market regimes referenced: $REGIME_COUNT/4 (need at least 3)"
  FAILURES=$((FAILURES + 1))
fi

# ── Block E: Equity Time Axes (this skill's core content) ─────────────────
echo ""
echo "--- Equity Time Axes ---"

for axis in "T+1" "220.4" "1222" "1091" "246(c)" "11140" "4210" "34-96930"; do
  if grep -qF "$axis" "$SKILL_MD"; then
    echo "  [PASS] Time-axis citation present: $axis"
  else
    echo "  [FAIL] Time-axis citation MISSING: $axis"
    FAILURES=$((FAILURES + 1))
  fi
done

if grep -qF 'not you' "$SKILL_MD"; then
  echo "  [PASS] Honest insider-scope line present"
else
  echo "  [FAIL] Honest insider-scope line MISSING"
  FAILURES=$((FAILURES + 1))
fi

if grep -qF 'manufacture the deadlines the market will not' "$SKILL_MD"; then
  echo "  [PASS] Stated failure mode (no clock forces an equity decision)"
else
  echo "  [FAIL] Stated failure mode MISSING"
  FAILURES=$((FAILURES + 1))
fi

if grep -qF 'tax never justifies a worse economic position\|Tax never justifies a worse economic position' "$SKILL_MD" \
   || grep -qiF 'never justifies a worse economic position' "$SKILL_MD"; then
  echo "  [PASS] Tax-precedence rule stated"
else
  echo "  [FAIL] Tax-precedence rule MISSING"
  FAILURES=$((FAILURES + 1))
fi

# ── Block F: Anti-Hallucination Guardrails ────────────────────────────────
echo ""
echo "--- Anti-Hallucination ---"

for phrase in "Admit uncertainty" "Flag your knowledge cutoff" "Never guess security" "[VERIFIED]"; do
  if grep -qF "$phrase" "$SKILL_MD"; then
    echo "  [PASS] Guardrail: '$phrase'"
  else
    echo "  [FAIL] Guardrail MISSING: '$phrase'"
    FAILURES=$((FAILURES + 1))
  fi
done

# ── Block G: References and Files ─────────────────────────────────────────
echo ""
echo "--- References & Files ---"

if [ -d "$REF_DIR" ]; then
  echo "  [PASS] references/ directory exists"
else
  echo "  [FAIL] references/ directory MISSING"
  FAILURES=$((FAILURES + 1))
fi

if [ -d "$REF_DIR" ]; then
  REF_FILE_COUNT=$(find "$REF_DIR" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
else
  REF_FILE_COUNT=0
fi
if [ "$REF_FILE_COUNT" -ge 9 ]; then
  echo "  [PASS] Reference files on disk: $REF_FILE_COUNT (minimum 9)"
else
  echo "  [FAIL] Reference files on disk: $REF_FILE_COUNT (need at least 9)"
  FAILURES=$((FAILURES + 1))
fi

THIN_REFS=0
if [ -d "$REF_DIR" ]; then
  for f in "$REF_DIR"/*.md; do
    [ -f "$f" ] || continue
    lines=$(wc -l < "$f" | tr -d ' ')
    if [ "$lines" -lt 80 ]; then
      echo "  [FAIL] Thin reference (under 80 lines): $(basename "$f") — $lines lines"
      THIN_REFS=$((THIN_REFS + 1))
    fi
  done
fi
if [ "$THIN_REFS" -eq 0 ]; then
  echo "  [PASS] All reference files are substantive (>= 80 lines)"
else
  FAILURES=$((FAILURES + THIN_REFS))
fi

BROKEN=0
if [ -d "$REF_DIR" ]; then
  for ref in $(grep -oh '(references/[^)]*\.md)' "$SKILL_MD" 2>/dev/null | sed 's|(references/||;s|)||' || true); do
    if [ -n "$ref" ] && [ ! -f "$REF_DIR/$ref" ]; then
      echo "  [FAIL] Broken reference link: references/$ref"
      BROKEN=$((BROKEN + 1))
    fi
  done
fi
if [ "$BROKEN" -eq 0 ]; then
  echo "  [PASS] All reference links resolve"
else
  FAILURES=$((FAILURES + BROKEN))
fi

# Every reference file on disk should be linked from SKILL.md (no orphans).
ORPHANS=0
if [ -d "$REF_DIR" ]; then
  for f in "$REF_DIR"/*.md; do
    [ -f "$f" ] || continue
    base="$(basename "$f")"
    if ! grep -qF "(references/$base)" "$SKILL_MD"; then
      echo "  [FAIL] Orphan reference file (not linked from SKILL.md): $base"
      ORPHANS=$((ORPHANS + 1))
    fi
  done
fi
if [ "$ORPHANS" -eq 0 ]; then
  echo "  [PASS] Every reference file is linked from SKILL.md"
else
  FAILURES=$((FAILURES + ORPHANS))
fi

EXAMPLE_README="$SKILL_DIR/examples/backtest/README.md"
if [ -f "$EXAMPLE_README" ]; then
  echo "  [PASS] examples/backtest/README.md exists"
else
  echo "  [FAIL] examples/backtest/README.md MISSING"
  FAILURES=$((FAILURES + 1))
fi

if [ -x "$SKILL_DIR/scripts/verify-skill.sh" ]; then
  echo "  [PASS] verify-skill.sh is executable"
else
  echo "  [FAIL] verify-skill.sh is NOT executable"
  FAILURES=$((FAILURES + 1))
fi

# ── Summary ───────────────────────────────────────────────────────────────
echo ""
echo "=============================================="
if [ "$FAILURES" -eq 0 ]; then
  echo "OK: $SKILL_NAME — all checks passed"
  exit 0
else
  echo "FAIL: $SKILL_NAME — $FAILURES check(s) failed"
  exit 1
fi
