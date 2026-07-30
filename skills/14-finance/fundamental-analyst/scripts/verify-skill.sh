#!/usr/bin/env bash
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
REFS_DIR="$SKILL_DIR/references"
ERRORS=0; WARNINGS=0
check() { local desc="$1"; shift; if "$@"; then echo "  ✅ $desc"; else echo "  ❌ $desc"; ERRORS=$((ERRORS + 1)); fi; }

echo "=== verify-skill: fundamental-analyst ==="

check "SKILL.md exists" [ -f "$SKILL_MD" ]
check "8 reference files" [ "$(ls -1 "$REFS_DIR"/*.md 2>/dev/null | wc -l)" -ge 8 ]

check "YAML frontmatter present" grep -q "^---$" "$SKILL_MD"
check "name field" grep -q "^name: fundamental-analyst" "$SKILL_MD"
check "description field" grep -q "^description:" "$SKILL_MD"
check "license field" grep -q "^license:" "$SKILL_MD"
check "token_budget field" grep -q "^token_budget:" "$SKILL_MD"
check "chain section present" grep -q "feeds_into:" "$SKILL_MD"

check "[VERIFIED] token" grep -q "\[VERIFIED\]" "$SKILL_MD"
check "Never guess" grep -q "Never guess\|NEVER" "$SKILL_MD"
check "Anti-Hallucination section" grep -q "## Anti-Hallucination" "$SKILL_MD"

for section in "Route the Request" "Ground Rules" "Core Workflow" "Decision Trees" "Gotchas" "Cross-Skill Coordination" "Verification Guardrails" "Production Checklist" "Error Recovery" "What Good Looks Like" "References"; do
  check "Section: $section" grep -q "## $section" "$SKILL_MD"
done

check "DCF mentioned" grep -q "DCF" "$SKILL_MD"
check "Piotroski F-Score" grep -q "Piotroski\|F-Score" "$SKILL_MD"
check "Altman Z-Score" grep -q "Altman.*Z-Score" "$SKILL_MD"
check "Beneish M-Score" grep -q "Beneish\|M-Score" "$SKILL_MD"
check "PE ratio" grep -q "PE\|P/E" "$SKILL_MD"
check "ETF fundamentals" grep -q "ETF" "$SKILL_MD"
check "Margin of safety" grep -q "margin.of.safety" "$SKILL_MD"

for ref in valuation-methods financial-ratios quality-scores earnings-quality dividend-analysis etf-fundamentals red-flags-checklist screening-methodology; do
  check "Reference link: $ref" grep -q "$ref" "$SKILL_MD"
  check "Reference file exists: $ref" [ -f "$REFS_DIR/$ref.md" ]
done

check "Ground rules have Mechanical Trigger" grep -q "Trigger:" "$SKILL_MD"
check "Dollar-quantified gotchas" grep -qE '\$[0-9]+K|\$[0-9]+M' "$SKILL_MD"

echo ""
echo "=== Results: $ERRORS errors, $WARNINGS warnings ==="
if [ "$ERRORS" -gt 0 ]; then echo "❌ VERIFICATION FAILED"; exit 1; else echo "✅ ALL CHECKS PASSED"; fi
