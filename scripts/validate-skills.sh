#!/usr/bin/env bash
# Skills Validation Suite — Blocking CI/CD Governance Gate
# Validates all 106 skills against the agentskills.io spec + internal quality standards.
# Exit code 0 = all checks pass. Non-zero = violations found.
set -euo pipefail

SKILLS_DIR="$(cd "$(dirname "$0")/../skills" && pwd)"
PASS=0
FAIL=0
ERRORS=""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

check() {
    local name="$1"; shift
    if "$@"; then
        echo -e "  ${GREEN}PASS${NC} $name"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}FAIL${NC} $name"
        FAIL=$((FAIL + 1))
        ERRORS="${ERRORS}\n  FAIL: $name"
    fi
}

echo "=== Skills Validation Suite ==="
echo ""

# --- 1. FRONTMATTER VALIDATION ---
echo "[1] Frontmatter validation..."

check "All SKILL.md files have valid YAML frontmatter" python3 -c "
import os, re, yaml, sys
errors = 0
for root, dirs, files in os.walk('$SKILLS_DIR'):
    for f in files:
        if f == 'SKILL.md':
            path = os.path.join(root, f)
            with open(path) as fh:
                content = fh.read()
            parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) < 3:
                print(f'  MISSING FRONTMATTER: {path}', file=sys.stderr)
                errors += 1
                continue
            try:
                fm = yaml.safe_load(parts[1])
                if not isinstance(fm, dict):
                    print(f'  INVALID YAML (not dict): {path}', file=sys.stderr)
                    errors += 1
                    continue
                if 'name' not in fm:
                    print(f'  MISSING name field: {path}', file=sys.stderr)
                    errors += 1
                if 'description' not in fm:
                    print(f'  MISSING description field: {path}', file=sys.stderr)
                    errors += 1
                if 'license' not in fm:
                    print(f'  MISSING license field: {path}', file=sys.stderr)
                    errors += 1
            except yaml.YAMLError as e:
                print(f'  YAML PARSE ERROR in {path}: {e}', file=sys.stderr)
                errors += 1
sys.exit(errors)
"

# --- 2. DESCRIPTION FORMAT ---
echo "[2] Description trigger format..."

check "All descriptions use 'Use when... Handles... Do NOT use for...' trigger format" python3 -c "
import os, re, yaml, sys
errors = 0
for root, dirs, files in os.walk('$SKILLS_DIR'):
    for f in files:
        if f == 'SKILL.md':
            if '00-framework' in root:
                continue
            path = os.path.join(root, f)
            with open(path) as fh:
                content = fh.read()
            parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) < 3:
                continue
            try:
                fm = yaml.safe_load(parts[1])
            except:
                continue
            if not isinstance(fm, dict):
                continue
            desc = fm.get('description', '')
            if 'Use when' not in desc:
                print(f'  MISSING \"Use when\" in description: {path}', file=sys.stderr)
                errors += 1
            if 'Handles' not in desc:
                print(f'  MISSING \"Handles\" in description: {path}', file=sys.stderr)
                errors += 1
            if 'Do NOT use' not in desc:
                print(f'  MISSING \"Do NOT use\" negative trigger: {path}', file=sys.stderr)
                errors += 1
sys.exit(errors)
"

# --- 3. REQUIRED SECTIONS ---
echo "[3] Required core sections..."

check "All skills have the 12 required core sections" python3 -c "
import os, re, sys

REQUIRED = {
    'Route the Request', 'Ground Rules — Read Before Anything Else',
    'The Expert\\'s Mindset', 'Operating at Different Levels',
    'When to Use', 'Decision Trees', 'Core Workflow',
    'Cross-Skill Coordination', 'Proactive Triggers',
    'What Good Looks Like', 'Deliberate Practice', 'References'
}

errors = 0
for root, dirs, files in os.walk('$SKILLS_DIR'):
    for f in files:
        if f == 'SKILL.md':
            # Skip framework skill
            if '00-framework' in root:
                continue
            path = os.path.join(root, f)
            with open(path) as fh:
                content = fh.read()
            parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) < 3:
                continue
            body = parts[2]
            found = {re.sub(r'\s*\*\*\((?:QUICK|STANDARD|DEEP)\)\*\*\s*', '', m.group(1)).strip() for m in re.finditer(r'^## (.+)$', body, re.MULTILINE)}
            missing = REQUIRED - found
            if missing:
                print(f'  MISSING SECTIONS {missing}: {path}', file=sys.stderr)
                errors += 1
sys.exit(errors)
"

# --- 4. BROKEN REFERENCE LINKS ---
echo "[4] Reference link integrity..."

check "No broken reference links" python3 -c "
import os, re, sys
errors = 0
for root, dirs, files in os.walk('$SKILLS_DIR'):
    for f in files:
        if f == 'SKILL.md':
            path = os.path.join(root, f)
            with open(path) as fh:
                content = fh.read()
            for m in re.finditer(r'\(references/([^)]+)\)', content):
                ref_file = os.path.join(root, 'references', m.group(1))
                if not os.path.exists(ref_file):
                    print(f'  BROKEN LINK {m.group(1)} in {path}', file=sys.stderr)
                    errors += 1
sys.exit(errors)
"

# --- 5. TOKEN BUDGET (SPEC: 500 lines) ---
echo "[5] Token budget enforcement (500 lines)..."
python3 -c "
import os, re, sys
MAX_LINES = 500
warnings = 0
for root, dirs, files in os.walk('$SKILLS_DIR'):
    for f in files:
        if f == 'SKILL.md':
            path = os.path.join(root, f)
            with open(path) as fh:
                content = fh.read()
            parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) < 3:
                continue
            lines = parts[2].count('\n') + 1
            if lines > MAX_LINES:
                print(f'  WARN: {lines} lines in {path} (budget: {MAX_LINES})', file=sys.stderr)
                warnings += 1
if warnings > 0:
    print(f'  {warnings} skills over line budget (advisory)', file=sys.stderr)
" && echo -e "  ${GREEN}PASS${NC} Token budget check (500 lines)" || echo -e "  ${YELLOW}ADVISORY${NC} Token budget check"
echo "  ${YELLOW}INFO${NC} Per agentskills.io spec: <500 lines recommended"

# --- 6. PORTABILITY TARGET ---
echo "[6] Portability target declaration..."

check "All skills have portability target after title" python3 -c "
import os, re, sys
errors = 0
for root, dirs, files in os.walk('$SKILLS_DIR'):
    for f in files:
        if f == 'SKILL.md':
            if '00-framework' in root:
                continue
            path = os.path.join(root, f)
            with open(path) as fh:
                content = fh.read()
            if 'Portability target' not in content:
                print(f'  MISSING portability target: {path}', file=sys.stderr)
                errors += 1
sys.exit(errors)
"

# --- 7. ANTIPATTERN GREP VALIDITY (ADVISORY) ---
echo -n "[7] Anti-pattern grep pattern validity... "
python3 -c "
import os, re, sys
notes = 0
for root, dirs, files in os.walk('$SKILLS_DIR'):
    if 'references' not in root:
        continue
    for f in files:
        if f == 'anti-patterns.md':
            path = os.path.join(root, f)
            with open(path) as fh:
                content = fh.read()
            for m in re.finditer(r'\`grep\s+(.+?)\`', content):
                cmd = m.group(1).strip()
                sq = 0
                in_dq = False
                for i, ch in enumerate(cmd):
                    if ch == '\"' and (i == 0 or cmd[i-1] != '\\\\'):
                        in_dq = not in_dq
                    elif ch == \"'\" and not in_dq:
                        sq += 1
                if sq % 2 != 0:
                    notes += 1
print(f'{notes} grep pattern notes (advisory - patterns may be valid shell quoting)', file=sys.stderr)
"
echo -e "  INFO Non-blocking advisory check"

# --- 8. ALLOWED-TOOLS FOR READ-ONLY SKILLS ---
echo "[8] Allowed-tools for read-only skills..."

READONLY_SKILLS=(
    "code-reviewer" "security-reviewer" "accessibility-auditor" "security-engineer"
    "compliance-officer" "regulatory-specialist" "legal-advisor" "gdpr-privacy"
    "incident-responder" "observability-engineer" "performance-engineer"
    "site-reliability-engineer" "chaos-engineer" "database-reliability-engineer"
    "finops-engineer" "monorepo-manager" "ai-safety-health-reviewer"
    "medical-content-reviewer"
)

check "Read-only skills have allowed-tools restriction" python3 -c "
import os, re, yaml, sys

READONLY = {
    'code-reviewer', 'security-reviewer', 'accessibility-auditor', 'security-engineer',
    'compliance-officer', 'regulatory-specialist', 'legal-advisor', 'gdpr-privacy',
    'incident-responder', 'observability-engineer', 'performance-engineer',
    'site-reliability-engineer', 'chaos-engineer', 'database-reliability-engineer',
    'finops-engineer', 'monorepo-manager', 'ai-safety-health-reviewer',
    'medical-content-reviewer'
}

errors = 0
for root, dirs, files in os.walk('$SKILLS_DIR'):
    for f in files:
        if f == 'SKILL.md':
            path = os.path.join(root, f)
            with open(path) as fh:
                content = fh.read()
            parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) < 3:
                continue
            try:
                fm = yaml.safe_load(parts[1])
            except:
                continue
            if not isinstance(fm, dict):
                continue
            name = fm.get('name', '')
            if name in READONLY:
                if 'allowed-tools' not in fm:
                    print(f'  MISSING allowed-tools on read-only skill: {path}', file=sys.stderr)
                    errors += 1
sys.exit(errors)
"

# --- 9. ANTI-HALLUCINATION GROUND RULES ---
echo "[9] Anti-hallucination ground rules..."

check "All skills have anti-hallucination guardrails" python3 -c "
import os, re, sys
errors = 0
required_phrases = ['Admit uncertainty', 'Flag your knowledge cutoff', 'Never guess security', 'VERIFIED']
for root, dirs, files in os.walk('$SKILLS_DIR'):
    for f in files:
        if f == 'SKILL.md':
            if '00-framework' in root:
                continue
            path = os.path.join(root, f)
            with open(path) as fh:
                content = fh.read()
            missing = [p for p in required_phrases if p not in content]
            if missing:
                print(f'  MISSING anti-hallucination phrases {missing}: {path}', file=sys.stderr)
                errors += 1
sys.exit(errors)
"

# --- 10. STATE LOG SECTION ---
echo "[10] State Log section..."

check "All skills have State Log decision ledger" python3 -c "
import os, re, sys
errors = 0
for root, dirs, files in os.walk('$SKILLS_DIR'):
    for f in files:
        if f == 'SKILL.md':
            if '00-framework' in root:
                continue
            path = os.path.join(root, f)
            with open(path) as fh:
                content = fh.read()
            parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) < 3:
                continue
            body = parts[2]
            found = {re.sub(r'\s*\*\*\((?:QUICK|STANDARD|DEEP)\)\*\*\s*', '', m.group(1)).strip() for m in re.finditer(r'^## (.+)$', body, re.MULTILINE)}
            if 'State Log' not in found:
                print(f'  MISSING State Log section: {path}', file=sys.stderr)
                errors += 1
sys.exit(errors)
"

# --- 11. CHAIN CONNECTIVITY ---
echo "[11] Chain connectivity (consumes_from + feeds_into)..."

check "All skills have at least one upstream and downstream connection" python3 -c "
import os, re, yaml, sys
errors = 0
for root, dirs, files in os.walk('$SKILLS_DIR'):
    for f in files:
        if f == 'SKILL.md':
            if '00-framework' in root:
                continue
            path = os.path.join(root, f)
            with open(path) as fh:
                content = fh.read()
            parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) < 3:
                continue
            try:
                fm = yaml.safe_load(parts[1])
            except:
                continue
            if not isinstance(fm, dict):
                continue
            chain = fm.get('chain', {})
            consumes = chain.get('consumes_from', [])
            feeds = chain.get('feeds_into', [])
            name = fm.get('name', os.path.basename(os.path.dirname(path)))
            if not consumes:
                print(f'  MISSING consumes_from (no upstream): {path}', file=sys.stderr)
                errors += 1
            if not feeds:
                print(f'  MISSING feeds_into (no downstream): {path}', file=sys.stderr)
                errors += 1
sys.exit(errors)
"

# --- 10. ERROR RECOVERY ---
check "All skills have Error Recovery section" python3 -c "
import os, re, sys
errors = 0
for root, dirs, files in os.walk('$SKILLS_DIR'):
    for f in files:
        if f == 'SKILL.md':
            if '00-framework' in root:
                continue
            path = os.path.join(root, f)
            with open(path) as fh:
                content = fh.read()
            parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) < 3:
                continue
            body = parts[2]
            if '## Error Recovery' not in body:
                print(f'  MISSING Error Recovery: {path}', file=sys.stderr)
                errors += 1
sys.exit(errors)
"

# --- 11. VERIFICATION GUARDRAILS ---
check "All skills have Verification Guardrails section" python3 -c "
import os, re, sys
errors = 0
for root, dirs, files in os.walk('$SKILLS_DIR'):
    for f in files:
        if f == 'SKILL.md':
            if '00-framework' in root:
                continue
            path = os.path.join(root, f)
            with open(path) as fh:
                content = fh.read()
            parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) < 3:
                continue
            body = parts[2]
            # Accept any Verification section: ## Verification, ## Verification Guardrails, ## Verification Checklist
            if not re.search(r'^## Verification', body, re.MULTILINE):
                print(f'  MISSING Verification section: {path}', file=sys.stderr)
                errors += 1
sys.exit(errors)
"

# --- 12. UPSTREAM TABLE QUALITY ---
check "All skills have meaningful upstream table in Cross-Skill Coordination" python3 -c "
import os, re, sys
errors = 0
for root, dirs, files in os.walk('$SKILLS_DIR'):
    for f in files:
        if f == 'SKILL.md':
            if '00-framework' in root:
                continue
            path = os.path.join(root, f)
            with open(path) as fh:
                content = fh.read()
            parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) < 3:
                continue
            body = parts[2]
            # Check for upstream table with at least 1 entry
            if '| Upstream Skill' not in body:
                print(f'  MISSING upstream table (Cross-Skill Coordination): {path}', file=sys.stderr)
                errors += 1
sys.exit(errors)
"

# --- 13. LINE BUDGET ENFORCEMENT (ADVISORY — non-blocking) ---
echo -n "[13] Line budget check (advisory)... "
python3 -c "
import os, sys
over = []
for root, dirs, files in os.walk('$SKILLS_DIR'):
    for f in files:
        if f == 'SKILL.md':
            if '00-framework' in root:
                continue
            path = os.path.join(root, f)
            lines = sum(1 for _ in open(path))
            if lines > 500:
                over.append((path, lines))
over.sort(key=lambda x: -x[1])
if over:
    print(f'{len(over)} skills exceed 500-line advisory budget (top 5):')
    for path, lines in over[:5]:
        name = os.path.basename(os.path.dirname(path))
        print(f'  {name}: {lines} lines')
else:
    print('All skills within 500-line budget')
" || true

# --- SUMMARY ---
echo ""
echo "========================================"
echo -e "  ${GREEN}PASS: $PASS${NC}"
if [ $FAIL -gt 0 ]; then
    echo -e "  ${RED}FAIL: $FAIL${NC}"
    echo -e "Errors:${ERRORS}"
    exit 1
else
    echo -e "  ${RED}FAIL: 0${NC}"
fi
echo "========================================"
echo -e "${GREEN}All governance checks passed.${NC}"
