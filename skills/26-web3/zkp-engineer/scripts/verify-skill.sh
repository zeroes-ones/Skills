#!/usr/bin/env bash
set -euo pipefail

# verify-skill.sh — Validate zkp-engineer skill completeness and quality
# Target: 10/10 best-in-class score

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_FILE="$SKILL_DIR/SKILL.md"
PASS=0
FAIL=0
WARN=0
TOTAL=0

red()   { printf "\033[31m%s\033[0m\n" "$*"; }
green() { printf "\033[32m%s\033[0m\n" "$*"; }
yellow(){ printf "\033[33m%s\033[0m\n" "$*"; }
cyan()  { printf "\033[36m%s\033[0m\n" "$*"; }

check() {
    local desc="$1"; shift
    TOTAL=$((TOTAL + 1))
    if "$@"; then
        green "  ✓ PASS: $desc"
        PASS=$((PASS + 1))
    else
        red "  ✗ FAIL: $desc"
        FAIL=$((FAIL + 1))
    fi
}

warn_check() {
    local desc="$1"; shift
    TOTAL=$((TOTAL + 1))
    if "$@"; then
        green "  ✓ PASS: $desc"
        PASS=$((PASS + 1))
    else
        yellow "  ⚠ WARN: $desc"
        WARN=$((WARN + 1))
    fi
}

echo ""
cyan "═══════════════════════════════════════════════════════════════"
cyan "  ZKP Engineer Skill — Verification Suite                    "
cyan "───────────────────────────────────────────────────────────────"
echo ""

# ─── File Existence ──────────────────────────────────────────
echo "$(cyan '[1/7]') File Structure"
check "SKILL.md exists"                    [ -f "$SKILL_FILE" ]
check "scripts/verify-skill.sh exists"     [ -f "$SKILL_DIR/scripts/verify-skill.sh" ]
check "references/ directory exists"       [ -d "$SKILL_DIR/references" ]

# ─── Required Reference Files (10) ───────────────────────────
echo ""
echo "$(cyan '[2/7]') Reference Files (10 required)"
REF_FILES=(
    "proof-system-comparison.md"
    "circom2-circuit-patterns.md"
    "noir-circuit-development.md"
    "halo2-custom-gates.md"
    "under-constraint-detection.md"
    "trusted-setup-ceremony.md"
    "recursive-proving-folding.md"
    "zkp-applications-architecture.md"
    "solidity-verifier-deployment.md"
    "zkp-security-hardening.md"
)
for ref in "${REF_FILES[@]}"; do
    check "Reference: $ref" [ -f "$SKILL_DIR/references/$ref" ]
done
REF_COUNT=$(ls "$SKILL_DIR/references/"*.md 2>/dev/null | wc -l | tr -d ' ')
warn_check "At least 10 reference files (found: $REF_COUNT)" [ "$REF_COUNT" -ge 10 ]

# ─── Frontmatter ─────────────────────────────────────────────
echo ""
echo "$(cyan '[3/7]') Frontmatter Validation"
FRONTMATTER=$(head -50 "$SKILL_FILE")

check "Has 'name: zkp-engineer'"           grep -q "name: zkp-engineer" "$SKILL_FILE"
check "Has 'description:'"                 grep -q "description:" "$SKILL_FILE"
check "Has 'author: Sandeep Kumar Penchala'" grep -q "author: Sandeep Kumar Penchala" "$SKILL_FILE"
check "Has 'license: MIT'"                 grep -q "license: MIT" "$SKILL_FILE"
check "Has 'portability:'"                 grep -q "portability:" "$SKILL_FILE"
check "Has 'version:'"                     grep -q "version:" "$SKILL_FILE"
check "Has 'tags:.*zkp.*circom.*noir'"     grep -qE "tags:.*zkp.*circom.*noir" "$SKILL_FILE"
check "Has 'chain:' section"               grep -q "chain:" "$SKILL_FILE"
check "Has 'consumes_from:'"               grep -q "consumes_from:" "$SKILL_FILE"
check "Has 'feeds_into:'"                  grep -q "feeds_into:" "$SKILL_FILE"
check "Has 'token_budget:'"                grep -q "token_budget:" "$SKILL_FILE"

# ─── Required 14 Sections ────────────────────────────────────
echo ""
echo "$(cyan '[4/7]') Required Sections (14 minimum)"
SECTIONS=(
    "Proof System Selection"
    "Circuit Language"
    "Constraint Security"
    "Range Check Strategy"
    "Recursive Proving"
    "Trusted Setup"
    "ZKP Applications"
    "Solidity Verifier Deployment"
    "Development Workflow"
    "Circuit Testing"
    "Proof System Performance"
    "Security Hardening"
    "Anti-Rationalization"
    "Portability Target"
)
for section in "${SECTIONS[@]}"; do
    check "Section: '$section'" grep -q "$section" "$SKILL_FILE"
done

# ─── Decision Trees (6 minimum) ──────────────────────────────
echo ""
echo "$(cyan '[5/7]') Decision Trees (6 minimum)"
DT_COUNT=$(grep -c "DECISION TREE" "$SKILL_FILE" || echo "0")
check "At least 6 decision trees (found: $DT_COUNT)" [ "$DT_COUNT" -ge 6 ]

check "Tree: Proof System Selection"       grep -q "PROOF SYSTEM SELECTION" "$SKILL_FILE"
check "Tree: Circuit Language"             grep -q "CIRCUIT LANGUAGE SELECTION" "$SKILL_FILE"
check "Tree: Under-Constraint Detection"    grep -q "UNDER-CONSTRAINT DETECTION" "$SKILL_FILE"
check "Tree: Range Check Strategy"         grep -q "RANGE CHECK STRATEGY" "$SKILL_FILE"
check "Tree: Recursive Proving"            grep -q "RECURSIVE PROVING DECISION" "$SKILL_FILE"
check "Tree: Trusted Setup"                grep -q "TRUSTED SETUP STRATEGY" "$SKILL_FILE"

# ─── Gotchas (8 minimum) ─────────────────────────────────────
echo ""
echo "$(cyan '[6/7]') Gotchas (8 minimum) with Code Snippets"
GOTCHA_COUNT=$(grep -c "Gotcha #" "$SKILL_FILE" || echo "0")
check "At least 8 gotchas (found: $GOTCHA_COUNT)" [ "$GOTCHA_COUNT" -ge 8 ]

check "Gotcha: Under-constrained circuit"    grep -q "Under-Constrained Circuit" "$SKILL_FILE"
check "Gotcha: Missing range check"          grep -q "Missing Range Check" "$SKILL_FILE"
check "Gotcha: Bit decomposition"            grep -q "Bit Decomposition" "$SKILL_FILE"
check "Gotcha: Trusted setup compromise"     grep -q "Trusted Setup Compromise" "$SKILL_FILE"
check "Gotcha: Non-deterministic witness"    grep -q "Non-Deterministic Witness" "$SKILL_FILE"
check "Gotcha: Gas cost underestimation"     grep -q "Gas Cost Underestimation" "$SKILL_FILE"
check "Gotcha: Nullifier collision"          grep -q "Nullifier Collision" "$SKILL_FILE"
check "Gotcha: Public input side channels"   grep -q "Public Input Exposure" "$SKILL_FILE" || grep -q "Side Channels" "$SKILL_FILE"

# ─── Code Snippets ───────────────────────────────────────────
echo ""
echo "$(cyan '[7/7]') Code Snippets & Quality Checks"
CIRCOM_COUNT=$(grep -c "pragma circom" "$SKILL_FILE" || echo "0")
NOIR_COUNT=$(grep -c "use dep::std" "$SKILL_FILE" || echo "0")
RUST_COUNT=$(grep -c "impl Circuit" "$SKILL_FILE" || echo "0")
SOLIDITY_COUNT=$(grep -c "pragma solidity" "$SKILL_FILE" || echo "0")

check "Circom 2 code snippets (found: $CIRCOM_COUNT)"    [ "$CIRCOM_COUNT" -ge 2 ]
check "Noir code snippets (found: $NOIR_COUNT)"           [ "$NOIR_COUNT" -ge 1 ]
check "Halo2/Rust code snippets (found: $RUST_COUNT)"     [ "$RUST_COUNT" -ge 1 ]
check "Solidity verifier snippets (found: $SOLIDITY_COUNT)" [ "$SOLIDITY_COUNT" -ge 1 ]

# Quality: VULNERABLE/FIXED pattern for gotchas
VULN_COUNT=$(grep -c "VULNERABLE" "$SKILL_FILE" || echo "0")
FIXED_COUNT=$(grep -c "FIXED:" "$SKILL_FILE" || echo "0")
check "Vulnerable + Fixed code pattern (V: $VULN_COUNT, F: $FIXED_COUNT)" \
    [ "$VULN_COUNT" -ge 2 ] && [ "$FIXED_COUNT" -ge 2 ]

# Quality: Tables for comparison
TABLE_COUNT=$(grep -c "^|" "$SKILL_FILE" || echo "0")
warn_check "Comparison tables present (found: $TABLE_COUNT table lines)" [ "$TABLE_COUNT" -ge 20 ]

# Quality: Anti-Rationalization section
check "Anti-Rationalization Clauses section" grep -q "Anti-Rationalization" "$SKILL_FILE"

# Line count check
LINE_COUNT=$(wc -l < "$SKILL_FILE" | tr -d ' ')
check "SKILL.md at least 500 lines (found: $LINE_COUNT)" [ "$LINE_COUNT" -ge 500 ]
warn_check "SKILL.md at least 700 lines (target: 700-800, found: $LINE_COUNT)" [ "$LINE_COUNT" -ge 700 ]

# Verify reference files have non-trivial content
echo ""
echo "$(cyan 'Reference File Quality')"
MIN_REF_SIZE=1000
for ref in "${REF_FILES[@]}"; do
    ref_path="$SKILL_DIR/references/$ref"
    if [ -f "$ref_path" ]; then
        ref_size=$(wc -c < "$ref_path" | tr -d ' ')
        check "Reference $ref has content (>${MIN_REF_SIZE} bytes, actual: $ref_size)" \
            [ "$ref_size" -ge "$MIN_REF_SIZE" ]
    fi
done

# ─── Summary ─────────────────────────────────────────────────
echo ""
cyan "═══════════════════════════════════════════════════════════════"
cyan "  Verification Summary                                       "
cyan "───────────────────────────────────────────────────────────────"
printf "  Total checks:  %d\n" "$TOTAL"
printf "  $(green "Passed:")       %d\n" "$PASS"
printf "  $(yellow "Warnings:")     %d\n" "$WARN"
printf "  $(red "Failed:")       %d\n" "$FAIL"
cyan "───────────────────────────────────────────────────────────────"

SCORE=$(( PASS * 100 / TOTAL ))
if [ "$FAIL" -eq 0 ]; then
    green "  SCORE: $SCORE% — ALL CHECKS PASSED ✓"
    echo ""
    green "  Rating: 10/10 Best-in-Class"
    exit 0
else
    red "  SCORE: $SCORE% — $FAIL checks FAILED ✗"
    echo ""
    if [ "$FAIL" -le 3 ]; then
        yellow "  Rating: 9/10 — Minor issues to fix"
    else
        red "  Rating: <9/10 — Significant issues to address"
    fi
    exit 1
fi
