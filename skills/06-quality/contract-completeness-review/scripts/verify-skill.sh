#!/usr/bin/env bash
# Verification harness for contract-completeness-review
#
# Run: bash scripts/verify-skill.sh              # structural checks on this skill
#      bash scripts/verify-skill.sh <repo-root>  # plus the eight contract checks on a target repo
#
# The structural half is automated. The contract half ECHOES the checks rather than
# pretending to run them: six of the eight need a human to decide what the system must be
# able to do, and a script that reported "PASS" for them would manufacture exactly the
# confidence this skill exists to remove.
set -euo pipefail

echo "=== Verifying contract-completeness-review ==="
echo ""

PASS=0
FAIL=0

check() {
    local name="$1"; shift
    if "$@"; then
        echo "  PASS $name"
        PASS=$((PASS + 1))
    else
        echo "  FAIL $name"
        FAIL=$((FAIL + 1))
    fi
}

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "--- Structural checks (automated) ---"
check "SKILL.md exists" test -f "$SKILL_DIR/SKILL.md"
check "references/ directory exists" test -d "$SKILL_DIR/references"
check "scripts/ directory exists" test -d "$SKILL_DIR/scripts"
check "examples/backtest exists" test -d "$SKILL_DIR/examples/backtest"
check "SKILL.md has frontmatter" grep -q "^---$" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "SKILL.md has token_budget" grep -q "token_budget:" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "SKILL.md has chain" grep -q "chain:" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "SKILL.md has consumes_from and feeds_into" \
    bash -c "grep -q 'consumes_from:' '$SKILL_DIR/SKILL.md' && grep -q 'feeds_into:' '$SKILL_DIR/SKILL.md'"

echo ""
echo "--- Required sections ---"
for section in \
    "Route the Request" \
    "Anti-Rationalization" \
    "Ground Rules" \
    "Anti-Hallucination" \
    "The Expert's Mindset" \
    "Deliberate Practice" \
    "Operating at Different Levels" \
    "When to Use" \
    "When NOT to Use" \
    "Decision Trees" \
    "Core Workflow" \
    "Best Practices" \
    "Error Decoder" \
    "Error Recovery" \
    "Cross-Skill Coordination" \
    "Proactive Triggers" \
    "Anti-Patterns" \
    "State Log" \
    "Production Checklist" \
    "What Good Looks Like" \
    "Verification" \
    "Verification Guardrails" \
    "References" \
    "Gotchas"
do
    check "Has section: $section" grep -q "^## $section" "$SKILL_DIR/SKILL.md" 2>/dev/null
done

echo ""
echo "--- Contract-specific checks (this skill's own gate rules) ---"
check "Ground Rules carry a Mechanical Trigger column" \
    grep -q "Mechanical Trigger" "$SKILL_DIR/SKILL.md"
check "Every Ground Rule violation begins with 'STOP. Respond:'" \
    bash -c "[ \"\$(grep -c 'STOP. Respond:' '$SKILL_DIR/SKILL.md')\" -ge 8 ]"
check "At least 3 decision trees under ## Decision Trees" \
    bash -c "[ \"\$(sed -n '/^## Decision Trees/,/^## Core Workflow/p' '$SKILL_DIR/SKILL.md' | grep -c '^### ')\" -ge 3 ]"
check "Decision Trees contain branching glyphs" \
    bash -c "sed -n '/^## Decision Trees/,/^## Core Workflow/p' '$SKILL_DIR/SKILL.md' | grep -qE '[├└│─]|\|--|\+--'"
check "Gotchas contain at least 5 dollar-quantified costs" \
    bash -c "[ \"\$(grep -cE '\\\$[0-9,]+' '$SKILL_DIR/SKILL.md')\" -ge 5 ]"
check "Production Checklist carries 12+ CR items" \
    bash -c "[ \"\$(sed -n '/^## Production Checklist/,/^## What Good Looks Like/p' '$SKILL_DIR/SKILL.md' | grep -c 'CR[0-9]')\" -ge 12 ]"
check "At least 8 'Complete when' statements" \
    bash -c "[ \"\$(grep -ci 'Complete when' '$SKILL_DIR/SKILL.md')\" -ge 8 ]"
check "Anti-Rationalization table has 4-6 rows" \
    bash -c "[ \"\$(sed -n '/^## Anti-Rationalization/,/^## Ground Rules/p' '$SKILL_DIR/SKILL.md' | grep -c '^| \"')\" -ge 4 ]"
check "Every Anti-Patterns data row starts with the cross glyph" \
    bash -c "[ \"\$(sed -n '/^## Anti-Patterns/,/^## State Log/p' '$SKILL_DIR/SKILL.md' | grep -c '^| ❌')\" -ge 5 ]"
check "Every Anti-Patterns data row carries the check glyph" \
    bash -c "[ \"\$(sed -n '/^## Anti-Patterns/,/^## State Log/p' '$SKILL_DIR/SKILL.md' | grep -c '✅')\" -ge 5 ]"
check "Cross-Skill upstream table present" grep -q "| Upstream Skill |" "$SKILL_DIR/SKILL.md"
check "References point at references/*.md" grep -q 'references/[a-z-]*\.md' "$SKILL_DIR/SKILL.md"
check "No banned generic phrases" \
    bash -c "! grep -qE \"We'll catch this later in review|Common rationalizations that lead to the failure modes documented above|It is faster to skip this\" '$SKILL_DIR/SKILL.md'"

echo ""
echo "--- Reference files (each must be substantive, not a stub) ---"
for ref in "$SKILL_DIR"/references/*.md; do
    [ -e "$ref" ] || continue
    name="$(basename "$ref")"
    words="$(wc -w < "$ref" | tr -d ' ')"
    check "references/$name is substantive (>=400 words, has ${words})" \
        bash -c "[ '$words' -ge 400 ]"
done

echo ""
echo "--- Contract review checklist (MANUAL — echoed, not evaluated) ---"
echo "  These require a human decision. A script reporting PASS here would be the"
echo "  'gate that always reports clean' this skill exists to catch."
echo ""
cat <<'CHECKLIST'
  [ ] 1. Inventory — every shared contract named with its file path and implementation count
  [ ] 2. Operation set — derived from call sites, jobs, and persisted state; NOT read off the interface
  [ ] 3. Writer — every piece of shared state names its writer and the seam that writer uses
  [ ] 4. Symmetry — no contract can read and clear a datum it cannot create or update
  [ ] 5. Bypass map — every operation x implementation cell is 'through', 'bypass', or 'N/A'
  [ ] 6. Evidence — at least one assertion derives from behaviour, not from the interface
  [ ] 7. Reachability — every contract member has a call site, or a named owner and a reason
  [ ] 8. Reverse direction — the conformance check fails when the implementation is AHEAD of the declaration
  [ ] 9. Round-trip assertion written, and the removal check run (watched it FAIL without the fix)
  [ ] 10. Discovery ledger records what found each defect, including 'reading' where honest
CHECKLIST

echo ""
if [ $# -ge 1 ] && [ -d "$1" ]; then
    TARGET="$1"
    echo "--- Read-only probes against $TARGET (candidates, not verdicts) ---"
    echo "  Every hit below is a CANDIDATE. Confirming one requires reading whether the"
    echo "  operation the contract also exposes is performed there."
    echo ""
    # Exclude dependency and build trees. A probe that returns 40 vendored interfaces is
    # not a shorter review — it is a review nobody reads, which is the "gate that cries
    # wolf" failure this skill exists to catch.
    EXCLUDES=(--exclude-dir=node_modules --exclude-dir=.git --exclude-dir=build
              --exclude-dir=.build --exclude-dir=DerivedData --exclude-dir=Pods
              --exclude-dir=vendor --exclude-dir=.venv --exclude-dir=venv
              --exclude-dir=__pycache__ --exclude-dir=.gradle --exclude-dir=dist
              --exclude-dir=.next --exclude-dir=out --exclude-dir=coverage)

    # Judge by the OUTPUT, never by the exit code. `grep -r` returns non-zero when it
    # merely encounters an unreadable directory, so `|| echo "(none found)"` prints
    # "(none found)" beside real hits — a probe reporting clean while it found things,
    # which is the failure mode this whole skill is about. Count lines instead.
    probe() {
        local pattern="$1" limit="$2"; shift 2
        local hits
        hits="$(grep -rn "${EXCLUDES[@]}" "$@" -E "$pattern" "$TARGET" 2>/dev/null || true)"
        if [ -z "$hits" ]; then
            echo "    (none found — confirm this means 'no such code', not 'probe missed the convention')"
        else
            printf '%s\n' "$hits" | head -"$limit" | sed 's/^/    /'
            local n
            n="$(printf '%s\n' "$hits" | wc -l | tr -d ' ')"
            [ "$n" -gt "$limit" ] && echo "    ... and $((n - limit)) more candidate(s)"
        fi
    }

    echo "  Interfaces/protocols/traits in the target (dependencies excluded):"
    probe '^\s*(public\s+)?(interface|protocol|trait|abstract class)\s+[A-Z]\w+' 40 \
        --include='*.kt' --include='*.swift' --include='*.ts' --include='*.py'
    echo ""
    echo "  Direct storage access (bypass candidates — the contract should own these):"
    probe 'EncryptedSharedPreferences|getSharedPreferences|SecItemAdd|SecItemCopyMatching|UserDefaults|localStorage\.(set|get)Item' 20 \
        --include='*.kt' --include='*.swift' --include='*.ts'
    echo ""
    echo "  State accessors with no obvious opposite (writer/reader asymmetry candidates):"
    probe '(has|is|get|current)[A-Z]\w*\(\s*\)' 20 \
        --include='*.kt' --include='*.swift' --include='*.ts'
    echo ""
    echo "  Zero is not a pass: if these three probes are empty, the target may have no shared"
    echo "  contracts, or the probe may not match its conventions. Confirm which before recording"
    echo "  this as clean — a probe that finds nothing looks identical to a codebase that has nothing."
    echo ""
fi

echo "========================================"
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
echo "========================================"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi

echo "Structural checks passed. The manual checklist above is the review itself."
