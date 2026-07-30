#!/usr/bin/env bash
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
REFS_DIR="$SKILL_DIR/references"
ERRORS=0
check() { local desc="$1"; shift; if "$@"; then echo "  ✅ $desc"; else echo "  ❌ $desc"; ERRORS=$((ERRORS + 1)); fi; }

echo "=== verify-skill: portfolio-signal-manager ==="

check "SKILL.md exists" [ -f "$SKILL_MD" ]
check "8 reference files" [ "$(ls -1 "$REFS_DIR"/*.md 2>/dev/null | wc -l)" -ge 8 ]

check "YAML frontmatter" grep -q "^---$" "$SKILL_MD"
check "name field" grep -q "^name: portfolio-signal-manager" "$SKILL_MD"
check "license field" grep -q "^license:" "$SKILL_MD"
check "token_budget" grep -q "^token_budget:" "$SKILL_MD"
check "chain consumes_from" grep -q "consumes_from:" "$SKILL_MD"
check "chain feeds_into" grep -q "feeds_into:" "$SKILL_MD"

check "[VERIFIED] token" grep -q "\[VERIFIED\]" "$SKILL_MD"
check "Never guess" grep -q "Never guess\|NEVER" "$SKILL_MD"
check "Anti-Hallucination section" grep -q "## Anti-Hallucination" "$SKILL_MD"

for section in "Route the Request" "Ground Rules" "Core Workflow" "Decision Trees" "Gotchas" "Cross-Skill Coordination" "Verification Guardrails" "Production Checklist" "Error Recovery" "Proactive Triggers" "What Good Looks Like" "References"; do
  check "Section: $section" grep -q "## $section" "$SKILL_MD"
done

check "Signal conflict resolution" grep -q "Weighted Decision\|conflict" "$SKILL_MD"
check "Position sizing" grep -q "Kelly\|position.*siz" "$SKILL_MD"
check "MCP broker" grep -q "MCP\|broker" "$SKILL_MD"
check "Risk monitoring" grep -q "VaR\|drawdown\|risk" "$SKILL_MD"
check "Correlation-aware" grep -q "correlation\|N_effective" "$SKILL_MD"
check "Circuit breaker" grep -q "circuit.breaker\|CIRCUIT" "$SKILL_MD"
check "Bidirectional communication" grep -q "BIDIRECTIONAL\|PUSH\|PULL" "$SKILL_MD"
check "Portfolio construction" grep -q "rebalance\|ETF.*STOCK" "$SKILL_MD"

check "Ground rules have Trigger:" grep -q "Trigger:" "$SKILL_MD"
check "Dollar costs in anti-hallucination" grep -qE '\$[0-9]+K|\$[0-9]+M' "$SKILL_MD"

for ref in position-sizing-methods signal-conflict-resolution mcp-broker-integration portfolio-risk-metrics correlation-diversification circuit-breakers tax-aware-management backtesting-validation; do
  check "Reference file: $ref" [ -f "$REFS_DIR/$ref.md" ]
done

echo ""
echo "=== Results: $ERRORS errors ==="
if [ "$ERRORS" -gt 0 ]; then echo "❌ VERIFICATION FAILED"; exit 1; else echo "✅ ALL CHECKS PASSED"; fi
