#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_FILE="$SKILL_DIR/SKILL.md"
REFS_DIR="$SKILL_DIR/references"
ERRORS=0

red() { echo -e "\033[31m$*\033[0m"; }
green() { echo -e "\033[32m$*\033[0m"; }
yellow() { echo -e "\033[33m$*\033[0m"; }

check() {
    local desc="$1" condition="$2"
    if eval "$condition"; then
        green "  PASS: $desc"
    else
        red "  FAIL: $desc"
        ERRORS=$((ERRORS + 1))
    fi
}

echo "=== Cryptographic Engineer Skill Verification ==="
echo ""

# ── Structural Checks ──────────────────────────────────────────
echo "[1] File structure"
check "SKILL.md exists" '[ -f "$SKILL_FILE" ]'
check "references/ directory exists" '[ -d "$REFS_DIR" ]'
check "scripts/ directory exists" '[ -d "$SKILL_DIR/scripts" ]'
echo ""

# ── Frontmatter ────────────────────────────────────────────────
echo "[2] Frontmatter validation"
check "name field present" 'grep -q "^name: cryptographic-engineer" "$SKILL_FILE"'
check "description field present" 'grep -q "^description:" "$SKILL_FILE"'
check "author field present" 'grep -q "^author: Sandeep Kumar Penchala" "$SKILL_FILE"'
check "license field present" 'grep -q "^license:" "$SKILL_FILE"'
check "portability field present" 'grep -q "^portability:" "$SKILL_FILE"'
check "type field present" 'grep -q "^type:" "$SKILL_FILE"'
check "status field present" 'grep -q "^status:" "$SKILL_FILE"'
check "version field present" 'grep -q "^version:" "$SKILL_FILE"'
check "tags field present" 'grep -q "^tags:" "$SKILL_FILE"'
check "token_budget field present" 'grep -q "^token_budget:" "$SKILL_FILE"'
check "chain.consumes_from present" 'grep -q "consumes_from:" "$SKILL_FILE"'
check "chain.feeds_into present" 'grep -q "feeds_into:" "$SKILL_FILE"'
echo ""

# ── Required Sections ──────────────────────────────────────────
echo "[3] Required sections (14+)"
check "Section 1: Overview" 'grep -q "^## 1. Overview" "$SKILL_FILE"'
check "Section 2: MPC Protocol Selection" 'grep -q "MPC Protocol Selection" "$SKILL_FILE"'
check "Section 3: FHE Scheme Selection" 'grep -q "FHE Scheme Selection" "$SKILL_FILE"'
check "Section 4: Threshold Signature Architecture" 'grep -q "Threshold Signature Architecture" "$SKILL_FILE"'
check "Section 5: TEE Platform Selection" 'grep -q "TEE Platform Selection" "$SKILL_FILE"'
check "Section 6: Post-Quantum Migration Path" 'grep -q "Post-Quantum Migration Path" "$SKILL_FILE"'
check "Section 7: Key Ceremony Design" 'grep -q "Key Ceremony Design" "$SKILL_FILE"'
check "Section 8: MPC Implementation Patterns" 'grep -q "MPC Implementation Patterns" "$SKILL_FILE"'
check "Section 9: FHE Implementation Patterns" 'grep -q "FHE Implementation Patterns" "$SKILL_FILE"'
check "Section 10: Threshold Signature" 'grep -q "Threshold Signature Implementation" "$SKILL_FILE"'
check "Section 11: TEE Attestation" 'grep -q "TEE Attestation" "$SKILL_FILE"'
check "Section 12: PQC Implementation" 'grep -q "Post-Quantum Cryptography Implementation" "$SKILL_FILE"'
check "Section 13: Key Management" 'grep -q "Key Management" "$SKILL_FILE"'
check "Section 14: Cryptographic Agility" 'grep -q "Cryptographic Agility Architecture" "$SKILL_FILE"'
check "Section 15: Anti-Rationalization" 'grep -q "Anti-Rationalization" "$SKILL_FILE"'
check "Section 16: Gotchas" 'grep -q "Gotchas.*Pitfalls" "$SKILL_FILE"'
check "Section 17: References" 'grep -q "^## 17. References" "$SKILL_FILE"'
echo ""

# ── Decision Trees (6+) ────────────────────────────────────────
echo "[4] Decision trees (minimum 6)"
TREE_COUNT=$(grep -c "┌──\|+--" "$SKILL_FILE" || true)
check "At least 6 decision trees (found $TREE_COUNT)" '[ "$TREE_COUNT" -ge 6 ]'
echo ""

# ── Gotchas (8+) ───────────────────────────────────────────────
echo "[5] Gotchas & pitfalls (minimum 8)"
GOTCHA_COUNT=$(grep -c "^| [0-9]" "$SKILL_FILE" || true)
check "At least 8 documented gotchas (found $GOTCHA_COUNT)" '[ "$GOTCHA_COUNT" -ge 8 ]'
echo ""

# ── Code Snippets ──────────────────────────────────────────────
echo "[6] Real code snippets"
PYTHON_SNIPPETS=$(grep -c '```python' "$SKILL_FILE" || true)
RUST_SNIPPETS=$(grep -c '```rust' "$SKILL_FILE" || true)
CPP_SNIPPETS=$(grep -c '```cpp\|```c' "$SKILL_FILE" || true)
TOTAL=$((PYTHON_SNIPPETS + RUST_SNIPPETS + CPP_SNIPPETS))
check "Python code snippets (found $PYTHON_SNIPPETS)" '[ "$PYTHON_SNIPPETS" -ge 3 ]'
check "Rust code snippets (found $RUST_SNIPPETS)" '[ "$RUST_SNIPPETS" -ge 2 ]'
check "C/C++ code snippets (found $CPP_SNIPPETS)" '[ "$CPP_SNIPPETS" -ge 2 ]'
check "Total code blocks >= 10 (found $TOTAL)" '[ "$TOTAL" -ge 10 ]'
echo ""

# ── Content Quality ────────────────────────────────────────────
echo "[7] Content quality"
check "Contains 'MP-SPDZ' reference" 'grep -q "MP-SPDZ" "$SKILL_FILE"'
check "Contains 'TFHE' scheme reference" 'grep -q "TFHE" "$SKILL_FILE"'
check "Contains 'CKKS' scheme reference" 'grep -q "CKKS" "$SKILL_FILE"'
check "Contains 'FROST' threshold reference" 'grep -q "FROST" "$SKILL_FILE"'
check "Contains 'BLS' threshold reference" 'grep -q "BLS" "$SKILL_FILE"'
check "Contains 'SGX' TEE reference" 'grep -q "SGX" "$SKILL_FILE"'
check "Contains 'SEV-SNP' TEE reference" 'grep -q "SEV-SNP" "$SKILL_FILE"'
check "Contains 'Nitro Enclaves' reference" 'grep -q "Nitro Enclaves" "$SKILL_FILE"'
check "Contains 'ML-KEM' PQC reference" 'grep -q "ML-KEM" "$SKILL_FILE"'
check "Contains 'ML-DSA' PQC reference" 'grep -q "ML-DSA" "$SKILL_FILE"'
check "Contains 'SLH-DSA' PQC reference" 'grep -q "SLH-DSA" "$SKILL_FILE"'
check "Contains 'Shamir Secret Sharing' reference" 'grep -q "Shamir" "$SKILL_FILE"'
check "Contains 'Garbled Circuit' reference" 'grep -q "Garbled Circuit" "$SKILL_FILE"'
check "Contains 'Oblivious Transfer' reference" 'grep -q "Oblivious Transfer" "$SKILL_FILE"'
check "Contains 'HEIR' compiler reference" 'grep -q "HEIR" "$SKILL_FILE"'
check "Contains 'Concrete' (Zama) reference" 'grep -q "Concrete" "$SKILL_FILE"'
check "Contains 'SEAL' (Microsoft) reference" 'grep -q "Microsoft SEAL" "$SKILL_FILE"'
check "Contains 'OpenFHE' reference" 'grep -q "OpenFHE" "$SKILL_FILE"'
check "Contains 'HSM' reference" 'grep -q "HSM" "$SKILL_FILE"'
check "Contains 'PKCS#11' reference" 'grep -q "PKCS#11" "$SKILL_FILE"'
check "Contains 'remote attestation' reference" 'grep -q "remote attestation\|Remote Attestation" "$SKILL_FILE"'
check "Contains 'cryptographic agility' reference" 'grep -q "[Cc]ryptographic [Aa]gility" "$SKILL_FILE"'
check "Mentions downgrade attack" 'grep -q "downgrade" "$SKILL_FILE"'
check "Contains bootstrapping analysis" 'grep -q "[Bb]ootstrap" "$SKILL_FILE"'
check "Contains entropy sourcing guidance" 'grep -q "entropy\|Entropy" "$SKILL_FILE"'
echo ""

# ── Reference Files ────────────────────────────────────────────
echo "[8] Reference files (10+)"
REF_FILES=(
    "mpc-protocol-comparison.md"
    "fhe-scheme-selection.md"
    "threshold-signature-patterns.md"
    "tee-attestation-workflow.md"
    "post-quantum-migration-guide.md"
    "key-management-ceremony.md"
    "cryptographic-agility-patterns.md"
    "mpc-security-hardening.md"
    "fhe-performance-optimization.md"
    "threshold-key-resharing.md"
)
REF_COUNT=0
for f in "${REF_FILES[@]}"; do
    if [ -f "$REFS_DIR/$f" ]; then
        check "Reference: $f" "true"
        REF_COUNT=$((REF_COUNT + 1))
    else
        red "  MISSING: references/$f"
        ERRORS=$((ERRORS + 1))
    fi
done
check "All 10 reference files present ($REF_COUNT/10)" '[ "$REF_COUNT" -eq 10 ]'
echo ""

# ── Line Count ─────────────────────────────────────────────────
echo "[9] Content size"
LINES=$(wc -l < "$SKILL_FILE" | tr -d ' ')
echo "  SKILL.md: $LINES lines (target: 700-800+)"
if [ "$LINES" -ge 700 ]; then
    green "  PASS: Content meets minimum line requirement"
else
    red "  FAIL: Content too short ($LINES < 700 lines)"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# ── Summary ────────────────────────────────────────────────────
echo "============================================================="
if [ "$ERRORS" -eq 0 ]; then
    green "ALL CHECKS PASSED — Skill is 10/10 ready for deployment"
    exit 0
else
    red "$ERRORS ERRORS FOUND — Skill requires fixes before deployment"
    exit 1
fi
