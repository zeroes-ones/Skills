#!/usr/bin/env bash
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
REFS_DIR="$SKILL_DIR/references"
ERRORS=0; WARNINGS=0
check() { local desc="$1"; shift; if "$@"; then echo "  ✅ $desc"; else echo "  ❌ $desc"; ERRORS=$((ERRORS + 1)); fi; }
warn() { echo "  ⚠️  $1"; WARNINGS=$((WARNINGS + 1)); }

echo "=== verify-skill: technical-signals-engineer ==="

# File structure
check "SKILL.md exists" [ -f "$SKILL_MD" ]
check "8 reference files" [ "$(ls -1 "$REFS_DIR"/*.md 2>/dev/null | wc -l)" -ge 8 ]

# YAML frontmatter
check "YAML frontmatter present" grep -q "^---$" "$SKILL_MD"
check "name field" grep -q "^name: technical-signals-engineer" "$SKILL_MD"
check "description field" grep -q "^description:" "$SKILL_MD"
check "license field" grep -q "^license:" "$SKILL_MD"
check "token_budget field" grep -q "^token_budget:" "$SKILL_MD"
check "chain section present" grep -q "feeds_into:" "$SKILL_MD"

# Anti-hallucination
check "[VERIFIED] token" grep -q "\[VERIFIED\]" "$SKILL_MD"
check "Never guess" grep -q "Never guess\|NEVER guess" "$SKILL_MD"
check "Anti-Hallucination section" grep -q "## Anti-Hallucination" "$SKILL_MD"

# Required sections
for section in "Route the Request" "Ground Rules" "Core Workflow" "Decision Trees" "Gotchas" "Cross-Skill Coordination" "Verification Guardrails" "Production Checklist" "Error Recovery" "What Good Looks Like" "References"; do
  check "Section: $section" grep -q "## $section" "$SKILL_MD"
done

# Technical domain-specific
check "SMA formula" grep -q "SMA" "$SKILL_MD"
check "EMA formula" grep -q "EMA" "$SKILL_MD"
check "RSI(14)" grep -q "RSI.*14" "$SKILL_MD"
check "MACD" grep -q "MACD" "$SKILL_MD"
check "Bollinger Bands" grep -q "Bollinger" "$SKILL_MD"
check "ETF classification" grep -q "ETF\|leveraged ETF" "$SKILL_MD"
check "Earnings window" grep -q "earnings" "$SKILL_MD"
check "Volume confirmation" grep -q "volume.*confirmation\|Volume.*SMA" "$SKILL_MD"
check "Golden cross" grep -q "Golden Cross\|golden cross" "$SKILL_MD"
check "Regime detection" grep -q "regime\|ADX" "$SKILL_MD"

# Reference links resolve
for ref in indicator-formulas signal-patterns etf-classification regime-detection corporate-actions confidence-scoring volume-analysis multi-timeframe; do
  check "Reference link: $ref" grep -q "$ref" "$SKILL_MD"
  check "Reference file exists: $ref" [ -f "$REFS_DIR/$ref.md" ]
done

# Ground rules have mechanical triggers
check "Ground rules have Mechanical Trigger" grep -q "Trigger:" "$SKILL_MD"

# Decision trees present
check "3+ decision trees" [ "$(grep -c "^### " "$SKILL_MD" | head -1)" -ge 3 ] 2>/dev/null || warn "Count decision trees manually"

# Gotchas are dollar-quantified
check "Dollar-quantified gotchas" grep -qE '\$[0-9]+K|\$[0-9]+\s*K' "$SKILL_MD"

echo ""
echo "=== Results: $ERRORS errors, $WARNINGS warnings ==="
if [ "$ERRORS" -gt 0 ]; then echo "❌ VERIFICATION FAILED"; exit 1; else echo "✅ ALL CHECKS PASSED"; fi
