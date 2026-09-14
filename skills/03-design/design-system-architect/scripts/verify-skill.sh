#!/usr/bin/env bash
# Verification harness for design-system-architect
#
# This script encodes the checks THIS SKILL'S OUTPUT must pass. It does not lint the
# SKILL.md (that is scripts/lib/lint-template.py); it verifies a design-token system it
# was applied to. Point TOKENS at the project's machine-readable token source, or run it
# with no arguments to self-check the skill's own artifacts.
#
# Usage:
#   bash scripts/verify-skill.sh                    # self-check the skill directory
#   TOKENS=design/tokens.json bash scripts/verify-skill.sh   # check a token source
set -euo pipefail

PASS=0
FAIL=0
SKIP=0

check() {
    local name="$1"; shift
    if "$@" >/dev/null 2>&1; then
        echo "  PASS $name"
        PASS=$((PASS + 1))
    else
        echo "  FAIL $name"
        FAIL=$((FAIL + 1))
    fi
}

skip() {
    echo "  SKIP $1"
    SKIP=$((SKIP + 1))
}

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TOKENS="${TOKENS:-}"

echo "=== Verifying design-system-architect ==="
echo ""

# ── Skill artifacts ───────────────────────────────────────────────────────────
echo "[Skill artifacts]"
check "SKILL.md exists"                       test -f "$SKILL_DIR/SKILL.md"
check "references/ directory exists"          test -d "$SKILL_DIR/references"
check "scripts/ directory exists"             test -d "$SKILL_DIR/scripts"
check "examples/backtest/README.md exists"    test -f "$SKILL_DIR/examples/backtest/README.md"
check "token-tiers reference exists"          test -f "$SKILL_DIR/references/token-tiers.md"
check "cross-platform-mapping reference"      test -f "$SKILL_DIR/references/cross-platform-mapping.md"
check "platform-floors reference"             test -f "$SKILL_DIR/references/platform-floors.md"
check "generated-documentation reference"     test -f "$SKILL_DIR/references/generated-documentation.md"
check "gate-calibration reference"            test -f "$SKILL_DIR/references/gate-calibration.md"
echo ""

# ── R1: tiers ────────────────────────────────────────────────────────────────
echo "[R1] Token tiers — no screen reads a primitive"
if [[ -n "$TOKENS" && -f "$TOKENS" ]]; then
    # Every palette entry must be used by a semantic role, or be a DECLARED exemption. An
    # entry that is neither is either dead weight or being read directly from a screen — the
    # defect this rule exists for. Two ways an entry can be "used": referenced by name, or its
    # value expressed inline in the semantic block. A domain scale that is identical in every
    # appearance (a clinical severity ramp) is legitimately exempt, but only by name and only
    # with a stated reason: an allow-list entry with no reason outlives its justification.
    check "every palette entry is used by a semantic role or declared exempt with a reason" python3 -c "
import json, sys, re
t = json.load(open('$TOKENS'))
palette = (t.get('color', {}).get('palette') or {})
if not palette:
    sys.exit(0)
sem = t.get('color', {}).get('semantic') or {}
sem_text = json.dumps(sem)
used = set()
for name, value in palette.items():
    by_name = '@' + name in sem_text
    # An inline restatement of the value is a use, though the duplication is itself worth
    # noticing — it is how a palette edit stops reaching the role that copied it.
    if by_name or (isinstance(value, str) and value.lower() in sem_text.lower()):
        used.add(name)
notes = json.dumps(t)
exempt = {}
for name in palette:
    m = re.search(r'[\"\x27]?' + re.escape(name) + r'[\"\x27]?\s*:\s*\"([^\"]{20,})\"', notes)
    if m and re.search(r'severit|clinical|emergenc|identical in every appearance', m.group(1), re.I):
        exempt[name] = m.group(1)
unused = sorted(set(palette) - used - set(exempt))
for name in unused:
    print(f'    palette entry {name!r} is used by no semantic role and is not a declared exemption', file=sys.stderr)
for name, reason in sorted(exempt.items()):
    print(f'    exempt by name with a stated reason — {name}: {reason[:70]}', file=sys.stderr)
sys.exit(1 if unused else 0)
"
else
    skip "R1 token source checks (set TOKENS=/path/to/tokens.json)"
fi
echo ""

# ── R2: mapping ──────────────────────────────────────────────────────────────
echo "[R2] Cross-platform mapping — rank assertion and tolerance"
if [[ -n "$TOKENS" && -f "$TOKENS" ]]; then
    check "every scale step declares a per-platform mapping" python3 -c "
import json, sys
t = json.load(open('$TOKENS'))
scale = (t.get('typography', {}).get('scale') or {})
if not scale:
    sys.exit(0)
missing = [k for k, v in scale.items()
           if isinstance(v, dict) and v.get('px') and not (v.get('iosTextStyle') or v.get('materialSlot'))]
for k in missing:
    print(f'    step {k!r} has a px size and no platform mapping', file=sys.stderr)
sys.exit(1 if missing else 0)
"
else
    skip "R2 mapping checks (set TOKENS=/path/to/tokens.json)"
fi
echo ""

# ── R3: axes ─────────────────────────────────────────────────────────────────
echo "[R3] Axis separation — size tokens are not spacing tokens"
if [[ -n "$TOKENS" && -f "$TOKENS" ]]; then
    # A size token whose value coincides with a spacing value is the dangerous case: the
    # coupling is invisible today. This does not fail the check, it requires the collision
    # to be visible, because the fix is a NAME that states what the size sizes.
    check "coincident size/spacing values are reported for naming review" python3 -c "
import json, sys
t = json.load(open('$TOKENS'))
sizes = {v['px'] for v in ((t.get('size') or {}).get('scale') or {}).values() if isinstance(v, dict) and 'px' in v}
spacing = {v['px'] for v in ((t.get('spacing') or {}).get('scale') or {}).values() if isinstance(v, dict) and 'px' in v}
shared = sorted(sizes & spacing)
for v in shared:
    print(f'    value {v} appears on both the size and spacing axes - confirm each size token is named for what it sizes')
# Reporting is not failing: a correctly named size token may legitimately coincide.
sys.exit(0)
"
else
    skip "R3 axis checks (set TOKENS=/path/to/tokens.json)"
fi
echo ""

# ── R4: floors ───────────────────────────────────────────────────────────────
echo "[R4] Platform floors — declared per platform, not unified"
check "SKILL.md states the per-platform floor rule" \
    grep -q "published platform minimum" "$SKILL_DIR/SKILL.md"
check "SKILL.md states the declared-not-unified rule" \
    grep -q "REFUSE to unify a per-platform accessibility floor" "$SKILL_DIR/SKILL.md"
echo ""

# ── R5: generated documentation ──────────────────────────────────────────────
echo "[R5] Generated documentation — no hand-written restatement"
check "SKILL.md requires generation from the source" \
    grep -q "ALWAYS generate every human-readable design document" "$SKILL_DIR/SKILL.md"
check "SKILL.md requires a drift check" \
    grep -q "drift check" "$SKILL_DIR/SKILL.md"
echo ""

# ── R6: gates ────────────────────────────────────────────────────────────────
echo "[R6] Gate calibration — vocabulary source and proven firing"
check "SKILL.md requires the gate to read the generated artifact" \
    grep -q "VERIFY that every conformance gate reads its vocabulary from the generated token artifact" "$SKILL_DIR/SKILL.md"
check "SKILL.md requires a demonstrated firing" \
    grep -q "shown failing on an injected violation" "$SKILL_DIR/SKILL.md"
check "SKILL.md requires exemptions to carry reasons" \
    grep -q "Every exemption carries a reason" "$SKILL_DIR/SKILL.md"
echo ""

# ── Structural completeness of the skill itself ──────────────────────────────
echo "[Skill structure]"
check "Ground Rules table has a Mechanical Trigger column" \
    grep -q "Mechanical Trigger" "$SKILL_DIR/SKILL.md"
check "Ground Rules table has a Violation Response column" \
    grep -q "Violation Response" "$SKILL_DIR/SKILL.md"
check "every violation response starts with STOP. Respond:" python3 -c "
import re, sys
body = open('$SKILL_DIR/SKILL.md', encoding='utf-8').read()
seg = re.search(r'^## Ground Rules.*?\n(.*?)(?=^## )', body, re.M | re.S)
rows = re.findall(r'^\|\s*\*\*R\d+\*\*', seg.group(1), re.M) if seg else []
bad = [r for r in re.findall(r'^\|.*\|$', seg.group(1), re.M) if r.startswith('| **R') and 'STOP. Respond:' not in r]
sys.exit(1 if bad else 0)
"
check "at least 3 decision trees with branch glyphs" python3 -c "
import re, sys
body = open('$SKILL_DIR/SKILL.md', encoding='utf-8').read()
seg = re.search(r'^## Decision Trees.*?\n(.*?)(?=^## )', body, re.M | re.S).group(1)
trees = len(re.findall(r'^### ', seg, re.M))
glyphs = len(re.findall(r'[\u251c\u2514\u2502\u250c]|\|--|\+--|-->', seg))
sys.exit(0 if trees >= 3 and glyphs >= 8 else 1)
"
check "at least 8 'Complete when' criteria" python3 -c "
import sys
n = open('$SKILL_DIR/SKILL.md', encoding='utf-8').read().count('Complete when')
sys.exit(0 if n >= 8 else 1)
"
check "at least 5 dollar-quantified costs" python3 -c "
import re, sys
n = len(re.findall(r'\\\$[\d,]+', open('$SKILL_DIR/SKILL.md', encoding='utf-8').read()))
sys.exit(0 if n >= 5 else 1)
"
echo ""

echo "========================================"
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
echo "  SKIP: $SKIP"
echo "========================================"

if [[ "$FAIL" -gt 0 ]]; then
    exit 1
fi
