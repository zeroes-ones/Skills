#!/usr/bin/env bash
# Skill Scaffold — Generate a new skill from the 10/10 template with all 22 sections
# Usage: bash scripts/scaffold-skill.sh <domain>/<skill-name>
# Example: bash scripts/scaffold-skill.sh 05-development/react-performance
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ $# -lt 1 ]; then
    echo -e "${RED}Usage: bash scripts/scaffold-skill.sh <domain>/<skill-name>${NC}"
    echo "Example: bash scripts/scaffold-skill.sh 05-development/react-performance"
    echo ""
    echo "Domain codes:"
    echo "  00-framework  01-strategy    02-product      03-design"
    echo "  04-architecture 05-development 06-quality    07-devops"
    echo "  08-security   09-data        10-growth       11-legal"
    echo "  12-operations 13-specialized 14-finance      15-health"
    echo "  16-gaming     17-social      18-ai           19-platform"
    echo "  20-mobile     21-blockchain  22-ai-engineering 23-creator"
    echo "  24-accessibility 25-education 26-environment 27-fintech"
    echo "  28-marketplace 29-saas"
    exit 1
fi

SKILL_PATH="$1"
DOMAIN_DIR=$(dirname "$SKILL_PATH")
SKILL_NAME=$(basename "$SKILL_PATH")
SKILLS_ROOT="$(cd "$(dirname "$0")/../skills" && pwd)"
FULL_PATH="$SKILLS_ROOT/$SKILL_PATH"
TODAY=$(date +%Y-%m-%d)

# Validate kebab-case
if ! [[ "$SKILL_NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    echo -e "${RED}Error: Skill name must be kebab-case (lowercase, hyphens, no special chars)${NC}"
    echo "Got: '$SKILL_NAME' — expected like 'react-performance' or 'api-designer'"
    exit 1
fi

# Validate domain directory exists
if [ ! -d "$SKILLS_ROOT/$DOMAIN_DIR" ]; then
    echo -e "${RED}Error: Domain directory 'skills/$DOMAIN_DIR' does not exist${NC}"
    echo "Available domains:"
    ls -d "$SKILLS_ROOT"/*/ | while read d; do echo "  $(basename "$d")"; done
    exit 1
fi

# Check if skill already exists
if [ -d "$FULL_PATH" ]; then
    echo -e "${RED}Error: Skill already exists at $FULL_PATH${NC}"
    exit 1
fi

echo -e "${GREEN}Scaffolding skill:${NC} $SKILL_PATH"
echo ""

# Create directory structure
mkdir -p "$FULL_PATH/scripts"
mkdir -p "$FULL_PATH/references"

# ── SKILL.md ──────────────────────────────────────────────────────────────
cat > "$FULL_PATH/SKILL.md" << 'SKILLEOF'
---
name: "SKILL_NAME_PLACEHOLDER"
description: "Use when… Handles… Do NOT use…"
author: ""
type: development
status: draft
version: "1.0.0"
updated: DATE_PLACEHOLDER
tags: []
license: MIT
dependencies:
  tools: []
  packages: []
output:
  type: "text"
chain:
  consumes_from: []
  feeds_into: []
token_budget: 3500
---

# SKILL_NAME_PLACEHOLDER

> **Portability target:** Spec-level. This skill encodes domain expertise, not tool-specific commands.

---

## Route the Request **(QUICK)**

| Condition | Action |
|-----------|--------|
| User asks about [TOPIC] | Route to this skill |
| File/dependency detected: [PATTERN] | Auto-activate this skill |

**Intent Route questions:**
1. [Question to narrow scope]
2. [Question to identify sub-domain]

---

## Anti-Rationalization — No Excuses **(QUICK)**

**AR-01 [Topic]:** You CANNOT [violation]. [Why this is non-negotiable.]

**AR-02 [Topic]:** You CANNOT [violation]. [Consequence of rationalizing this.]

**AR-03 [Topic]:** You CANNOT [violation]. [The correct alternative.]

---

## Ground Rules — Read Before Anything Else **(QUICK)**

| # | Rule | Mechanical Trigger | Violation Response |
|---|------|-------------------|-------------------|
| R1 | [Rule description] | [What triggers enforcement] | [What happens on violation] |
| R2 | [Rule description] | [What triggers enforcement] | [What happens on violation] |
| R3 | [Rule description] | [What triggers enforcement] | [What happens on violation] |
| R4 | [Rule description] | [What triggers enforcement] | [What happens on violation] |
| R5 | [Rule description] | [What triggers enforcement] | [What happens on violation] |
| R6 | [Rule description] | [What triggers enforcement] | [What happens on violation] |

## Anti-Hallucination **(QUICK)**

- **Admit uncertainty** — If you don't know, say "I don't know" and explain what you'd need to learn. Never fabricate.
- **Flag your knowledge cutoff** — If your training data predates the technology version, state it. e.g., "My knowledge cuts off at [DATE]."
- **Never guess security** — If a security question is ambiguous, refuse to answer and explain the ambiguity. Default to the safer interpretation.
- **[VERIFIED]** — Every factual claim must be traceable to a reference in `references/`. Tag unverifiable claims with `[UNVERIFIED]`.

---

## The Expert's Mindset **(QUICK)**

[3-5 paragraphs on how world-class practitioners think in this domain.]

### What [Domain] Masters Know **(STANDARD)**

[Key insights that separate experts from intermediates.]

### When to Break Your Own Rules **(DEEP)**

[Scenarios where even best practices get overridden. Include war stories.]

---

## Deliberate Practice **(STANDARD)**

```mermaid
graph TD
    A[Learn Concept] --> B[Apply in Real Scenario]
    B --> C[Review Output Against Standards]
    C --> D[Identify Gap]
    D --> E[Targeted Drill on Gap]
    E --> B
```

| Level | Routine | Time | Success Metric |
|-------|---------|------|---------------|
| Novice | [Routine] | [Duration] | [Metric] |
| Intermediate | [Routine] | [Duration] | [Metric] |
| Advanced | [Routine] | [Duration] | [Metric] |
| Expert | [Routine] | [Duration] | [Metric] |

---

## Operating at Different Levels **(STANDARD)**

### L1: Apprentice
- **Scope:** [What L1 handles]
- **Autonomy:** [Decision authority]
- **Impact:** [Typical outcomes]
- **Craft:** [Skill expectations]

### L2: Practitioner
- **Scope:** [What L2 handles]
- **Autonomy:** [Decision authority]
- **Impact:** [Typical outcomes]
- **Craft:** [Skill expectations]

### L3: Senior
- **Scope:** [What L3 handles]
- **Autonomy:** [Decision authority]
- **Impact:** [Typical outcomes]
- **Craft:** [Skill expectations]

### L4: Staff / Principal
- **Scope:** [What L4 handles]
- **Autonomy:** [Decision authority]
- **Impact:** [Typical outcomes]
- **Craft:** [Skill expectations]

### L5: Transformative
- **Scope:** [What L5 handles]
- **Autonomy:** [Decision authority]
- **Impact:** [Typical outcomes]
- **Craft:** [Skill expectations]

---

## When to Use **(QUICK)**

**Use this skill when:**

1. **[Condition 1]** — [Why this skill is the right choice]
2. **[Condition 2]** — [Why this skill is the right choice]
3. **[Condition 3]** — [Why this skill is the right choice]
4. **[Condition 4]** — [Why this skill is the right choice]
5. **[Condition 5]** — [Why this skill is the right choice]

---

## When NOT to Use **(QUICK)**

**Do NOT use this skill when:**

1. **[Condition 1]** — Use [other-skill] instead
2. **[Condition 2]** — Use [other-skill] instead
3. **[Condition 3]** — Use [other-skill] instead

---

## Decision Trees **(STANDARD)**

### Decision Tree 1: [Topic]

```
[Question]?
├─ YES → [Action]
│   ├─ [Sub-question]?
│   │   ├─ YES → [Action]
│   │   └─ NO  → [Action]
│   └─ [Sub-question]?
│       ├─ YES → [Action]
│       └─ NO  → [Action]
└─ NO  → [Action]
    ├─ [Sub-question]?
    │   ├─ YES → [Action]
    │   └─ NO  → [Action]
    └─ [Sub-question]?
        ├─ YES → [Action]
        └─ NO  → [Action]
```

### Decision Tree 2: [Topic]

```
[Question]?
├─ YES → [Action]
└─ NO  → [Action]
```

### Decision Tree 3: [Topic]

```
[Question]?
├─ OPTION A → [Action]
├─ OPTION B → [Action]
└─ OPTION C → [Action]
```

---

## Core Workflow **(STANDARD)**

### Phase 1: [Phase Name] (~X min)
1. **Do:** [Concrete action]
2. **Verify:** [How to check correctness]
3. **Output:** [What this phase produces]

### Phase 2: [Phase Name] (~X min)
1. **Do:** [Concrete action]
2. **Verify:** [How to check correctness]
3. **Output:** [What this phase produces]

### Phase 3: [Phase Name] (~X min)
1. **Do:** [Concrete action]
2. **Verify:** [How to check correctness]
3. **Output:** [What this phase produces]

### Phase 4: [Phase Name] (~X min)
1. **Do:** [Concrete action]
2. **Verify:** [How to check correctness]
3. **Output:** [What this phase produces]

---

## Best Practices **(STANDARD)**

1. **[Header sentence.]** Explanation sentence or two with concrete example.
2. **[Header sentence.]** Explanation sentence or two with concrete example.
3. **[Header sentence.]** Explanation sentence or two with concrete example.
4. **[Header sentence.]** Explanation sentence or two with concrete example.
5. **[Header sentence.]** Explanation sentence or two with concrete example.
6. **[Header sentence.]** Explanation sentence or two with concrete example.
7. **[Header sentence.]** Explanation sentence or two with concrete example.
8. **[Header sentence.]** Explanation sentence or two with concrete example.
9. **[Header sentence.]** Explanation sentence or two with concrete example.
10. **[Header sentence.]** Explanation sentence or two with concrete example.

---

## Error Decoder **(STANDARD)**

| Symptom | Root Cause | Fix | Lesson |
|----------|-----------|-----|--------|
| [Error message or behavior] | [What actually went wrong] | [Exact command or code fix] | [How to prevent recurrence] |
| [Error message or behavior] | [What actually went wrong] | [Exact command or code fix] | [How to prevent recurrence] |
| [Error message or behavior] | [What actually went wrong] | [Exact command or code fix] | [How to prevent recurrence] |
| [Error message or behavior] | [What actually went wrong] | [Exact command or code fix] | [How to prevent recurrence] |
| [Error message or behavior] | [What actually went wrong] | [Exact command or code fix] | [How to prevent recurrence] |

---

## Error Recovery **(QUICK)**

| Symptom | First Action | If That Fails | Last Resort |
|----------|-------------|--------------|------------|
| [Symptom 1] | [Immediate fix attempt] | [Fallback approach] | [Escalation or restart] |
| [Symptom 2] | [Immediate fix attempt] | [Fallback approach] | [Escalation or restart] |
| [Symptom 3] | [Immediate fix attempt] | [Fallback approach] | [Escalation or restart] |
| [Symptom 4] | [Immediate fix attempt] | [Fallback approach] | [Escalation or restart] |
| [Symptom 5] | [Immediate fix attempt] | [Fallback approach] | [Escalation or restart] |

**Hard failure boundary:** After 3 failed recovery attempts, escalate to human. Do not loop.

---

## Cross-Skill Coordination **(STANDARD)**

### Upstream (What This Skill Needs)

| Upstream Skill | Artifact Needed | What You'll Use It For |
|---------------|----------------|----------------------|
| `upstream-skill-1` | [File/format/API] | [How it feeds into this skill] |
| `upstream-skill-2` | [File/format/API] | [How it feeds into this skill] |
| `upstream-skill-3` | [File/format/API] | [How it feeds into this skill] |

### Downstream (What This Skill Produces)

| Downstream Skill | Deliverable | What They'll Do With It |
|-----------------|------------|------------------------|
| `downstream-skill-1` | [File/format/API] | [How they consume your output] |
| `downstream-skill-2` | [File/format/API] | [How they consume your output] |
| `downstream-skill-3` | [File/format/API] | [How they consume your output] |

---

## Proactive Triggers **(STANDARD)**

- **[Trigger condition 1]** → What to flag. Why it matters before being asked. 🔴
- **[Trigger condition 2]** → Description of what to surface proactively. 🟡
- **[Trigger condition 3]** → Context on why this matters for downstream quality. 🟠
- **[Trigger condition 4]** → What to flag before it becomes a problem. 🔴
- **[Trigger condition 5]** → Early warning sign to surface. 🟡
- **[Trigger condition 6]** → Pattern to detect and flag. 🟠

---

## Anti-Patterns **(STANDARD)**

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| [What NOT to do — with concrete example] | [The correct approach — with concrete example] |
| [What NOT to do — with concrete example] | [The correct approach — with concrete example] |
| [What NOT to do — with concrete example] | [The correct approach — with concrete example] |
| [What NOT to do — with concrete example] | [The correct approach — with concrete example] |
| [What NOT to do — with concrete example] | [The correct approach — with concrete example] |

---

## State Log **(QUICK)**

| Turn | Action | Decision | Risk Accepted | Mitigation |
|------|--------|----------|---------------|-----------|
| 1 | [Action taken] | [Decision made] | [Risk identified] | [How mitigated] |

**Anti-Drift Check:** Before each response, verify:
1. Did the last action match the plan?
2. Are we still within scope?
3. Has any new information invalidated prior decisions?

---

## Production Checklist **(STANDARD)**

- [ ] **CR1: [Check description]** — Verification method: [How to verify]
- [ ] **CR2: [Check description]** — Verification method: [How to verify]
- [ ] **CR3: [Check description]** — Verification method: [How to verify]
- [ ] **CR4: [Check description]** — Verification method: [How to verify]
- [ ] **CR5: [Check description]** — Verification method: [How to verify]
- [ ] **CR6: [Check description]** — Verification method: [How to verify]
- [ ] **CR7: [Check description]** — Verification method: [How to verify]
- [ ] **CR8: [Check description]** — Verification method: [How to verify]
- [ ] **CR9: [Check description]** — Verification method: [How to verify]
- [ ] **CR10: [Check description]** — Verification method: [How to verify]
- [ ] **CR11: [Check description]** — Verification method: [How to verify]
- [ ] **CR12: [Check description]** — Verification method: [How to verify]

---

## What Good Looks Like **(QUICK)**

[1-2 paragraphs describing what output excellence looks like. Concrete, visual, verifiable.]

**Signs of Excellence:**
- [Sign 1]
- [Sign 2]
- [Sign 3]

**Signs of Dysfunction:**
- [Sign 1]
- [Sign 2]
- [Sign 3]

---

## Verification Guardrails **(STANDARD)**

### Pre-Generation
- [ ] [Check before starting work]
- [ ] [Check before starting work]
- [ ] [Check before starting work]

### Post-Generation
- [ ] [Check after completing work]
- [ ] [Check after completing work]
- [ ] [Check after completing work]

---

## References **(QUICK)**

- `references/additional-resources.md` — Deep knowledge and extended examples

---

> **Skill version:** 1.0.0 | **Token budget:** 3500 | **Generated:** DATE_PLACEHOLDER
SKILLEOF

# Replace placeholders
sed -i '' "s/SKILL_NAME_PLACEHOLDER/$SKILL_NAME/g" "$FULL_PATH/SKILL.md"
sed -i '' "s/DATE_PLACEHOLDER/$TODAY/g" "$FULL_PATH/SKILL.md"

# ── scripts/verify-skill.sh ───────────────────────────────────────────────
cat > "$FULL_PATH/scripts/verify-skill.sh" << 'VERIFYEOF'
#!/usr/bin/env bash
# Verification harness for SKILL_NAME_PLACEHOLDER
# Run: bash scripts/verify-skill.sh
set -euo pipefail

echo "=== Verifying SKILL_NAME_PLACEHOLDER ==="
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

# Structural checks
check "SKILL.md exists" test -f "$SKILL_DIR/SKILL.md"
check "references/ directory exists" test -d "$SKILL_DIR/references"
check "scripts/ directory exists" test -d "$SKILL_DIR/scripts"

# Content checks
check "SKILL.md has frontmatter" grep -q "^---$" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "SKILL.md has token_budget" grep -q "token_budget:" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "SKILL.md has chain" grep -q "chain:" "$SKILL_DIR/SKILL.md" 2>/dev/null

# Section checks
check "Has Route the Request" grep -q "Route the Request" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has Ground Rules" grep -q "Ground Rules" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has Decision Trees" grep -q "Decision Trees" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has Core Workflow" grep -q "Core Workflow" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has Error Decoder" grep -q "Error Decoder" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has Best Practices" grep -q "Best Practices" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has Production Checklist" grep -q "Production Checklist" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has Cross-Skill Coordination" grep -q "Cross-Skill Coordination" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has Operating at Different Levels" grep -q "Operating at Different Levels" "$SKILL_DIR/SKILL.md" 2>/dev/null

echo ""
echo "========================================"
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
echo "========================================"

if [ $FAIL -gt 0 ]; then
    exit 1
fi
VERIFYEOF

sed -i '' "s/SKILL_NAME_PLACEHOLDER/$SKILL_NAME/g" "$FULL_PATH/scripts/verify-skill.sh"
chmod +x "$FULL_PATH/scripts/verify-skill.sh"

# ── references/additional-resources.md ────────────────────────────────────
cat > "$FULL_PATH/references/additional-resources.md" << REFEOF
# Additional Resources — SKILL_NAME_PLACEHOLDER

> Deep knowledge loaded on demand. Keep SKILL.md lean; put extended examples, war stories, and reference material here.

## Extended Examples

[Add detailed examples, code samples, configuration templates here.]

## War Stories

[Add real failure narratives — what happened, why, how it was fixed, and the lesson learned.]

## Reference Material

[Add links, specifications, standards documents, and further reading.]
REFEOF

sed -i '' "s/SKILL_NAME_PLACEHOLDER/$SKILL_NAME/g" "$FULL_PATH/references/additional-resources.md"

# ── Summary ───────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}✓ Skill scaffolded at:${NC} $FULL_PATH"
echo ""
echo "Generated files:"
echo "  $FULL_PATH/SKILL.md                    (22 sections, 3500 token budget)"
echo "  $FULL_PATH/scripts/verify-skill.sh     (verification harness)"
echo "  $FULL_PATH/references/additional-resources.md"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Fill frontmatter: author, description, tags, chain references"
echo "  2. Fill all sections marked with [brackets]"
echo "  3. Run: python3 scripts/lib/lint-template.py $FULL_PATH/SKILL.md"
echo "  4. Run: bash scripts/validate-skills.sh"
echo "  5. Run: python3 scripts/validate_chains.py"
echo ""
echo -e "${YELLOW}Quality target: 10/10 before merge.${NC} See CONTRIBUTING-SKILLS.md for the full guide."
