#!/usr/bin/env bash
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
REFS_DIR="$SKILL_DIR/references"
ERRORS=0
check() { local desc="$1"; shift; if "$@"; then echo "  ✅ $desc"; else echo "  ❌ $desc"; ERRORS=$((ERRORS + 1)); fi; }

echo "=== verify-skill: cross-skill-communication ==="

check "SKILL.md exists" [ -f "$SKILL_MD" ]
check "8 reference files" [ "$(ls -1 "$REFS_DIR"/*.md 2>/dev/null | wc -l)" -ge 8 ]

check "YAML frontmatter" grep -q "^---$" "$SKILL_MD"
check "name: cross-skill-communication" grep -q "^name: cross-skill-communication" "$SKILL_MD"
check "license field" grep -q "^license:" "$SKILL_MD"
check "token_budget" grep -q "^token_budget:" "$SKILL_MD"
check "chain consumes_from" grep -q "consumes_from:" "$SKILL_MD"
check "chain feeds_into" grep -q "feeds_into:" "$SKILL_MD"

check "[VERIFIED] token" grep -q "\[VERIFIED\]" "$SKILL_MD"
check "Never guess" grep -q "Never guess\|NEVER" "$SKILL_MD"
check "Anti-Hallucination section" grep -q "## Anti-Hallucination" "$SKILL_MD"

for section in "Route the Request" "Ground Rules" "Core Workflow" "Decision Trees" "Gotchas" "Cross-Skill Coordination" "Verification Guardrails" "Production Checklist" "Error Recovery" "Proactive Triggers" "What Good Looks Like" "References" "Deliberate Practice"; do
  check "Section: $section" grep -q "## $section" "$SKILL_MD"
done

check "6 Communication Patterns referenced" grep -qE "Pattern [1-6]:" "$SKILL_MD"
check "Message envelope schema" grep -q "message_id" "$SKILL_MD"
check "Chain integrity" grep -q "BILATERAL\|broken chain\|457" "$SKILL_MD"
check "Conflict resolution" grep -q "Conflict Resolution\|weighted decision" "$SKILL_MD"
check "Feedback loop" grep -q "Feedback Loop\|feedback" "$SKILL_MD"
check "Circuit breaker" grep -q "circuit.breaker\|CIRCUIT" "$SKILL_MD"
check "Handoff state schema" grep -q "Handoff.*state\|handoff" "$SKILL_MD"
check "Schema versioning" grep -q "schema_version\|MAJOR.*MINOR" "$SKILL_MD"

check "Ground rules have Trigger:" grep -q "Trigger:" "$SKILL_MD"
check "Dollar costs in anti-hallucination" grep -qE '\$[0-9]+K|\$[0-9]+M' "$SKILL_MD"

for ref in message-envelope communication-patterns chain-validator conflict-resolution schema-versioning circuit-breakers feedback-loops handoff-state-schema; do
  check "Reference file: $ref" [ -f "$REFS_DIR/$ref.md" ]
done

echo ""
echo "=== Results: $ERRORS errors ==="
if [ "$ERRORS" -gt 0 ]; then echo "❌ VERIFICATION FAILED"; exit 1; else echo "✅ ALL CHECKS PASSED"; fi
