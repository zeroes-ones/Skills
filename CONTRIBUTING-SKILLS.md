# Contributing a New Skill

> **Target quality: 10/10.** Every skill in this library must pass all 13 pre-commit gates, 13 governance checks, and the 10/10 quality bar. This guide walks you through creating a new skill from scratch.

---

## Quick Reference

| What | Command | When |
|------|---------|------|
| Scaffold | `bash scripts/scaffold-skill.sh <domain>/<name>` | Before writing any content |
| Lint | `python3 scripts/lib/lint-template.py skills/<path>/SKILL.md` | After each section |
| Full validate | `bash scripts/validate-skills.sh` | Before committing |
| Chain check | `python3 scripts/validate_chains.py` | After setting chain |
| Library audit | `python3 scripts/audit-library.py` | Before PR |
| Pre-commit | Auto-runs on `git commit` | Every commit |

---

## Step 1: Scaffold the Skill

```bash
bash scripts/scaffold-skill.sh 05-development/my-new-skill
```

This generates:
```
skills/05-development/my-new-skill/
├── SKILL.md                    # Pre-populated with all 22 required sections
├── scripts/
│   └── verify-skill.sh         # Verification harness
└── references/
    └── additional-resources.md  # Deep-knowledge placeholder
```

The scaffolded SKILL.md has **every required section** with placeholder content and format hints. You fill in the domain expertise.

---

## Step 2: Fill the Frontmatter

Open `SKILL.md` and complete the YAML frontmatter:

```yaml
---
name: "my-new-skill"               # MUST match directory name
description: "Use when… Handles… Do NOT use…"  # ≤1024 chars
author: Your Name
type: development                   # strategy|product|design|architecture|development|quality|devops|security|data|growth|legal|operations|specialized
status: draft                       # draft → stable → deprecated
version: "1.0.0"
updated: 2026-01-15
tags: [tag1, tag2, tag3]
license: MIT
dependencies:
  tools: []
  packages: []
output:
  type: "text"
chain:
  consumes_from: ["upstream-skill"]  # Skills this depends on
  feeds_into: ["downstream-skill"]   # Skills that consume this output
token_budget: 3500                   # 2500-5000, based on body length
---
```

### Domain Codes
| Code | Domain |
|------|--------|
| `00-framework` | Framework meta-skills |
| `01-strategy` | Strategy & CEO |
| `02-product` | Product management |
| `03-design` | UI/UX design |
| `04-architecture` | System architecture |
| `05-development` | Software development |
| `06-quality` | Testing & QA |
| `07-devops` | DevOps & CI/CD |
| `08-security` | Security & compliance |
| `09-data` | Data & analytics |
| `10-growth` | Growth & marketing |
| `11-legal` | Legal & compliance |
| `12-operations` | Operations & support |
| `13-specialized` | Specialized domains |
| `14-finance` | Finance & trading |
| `15-health` | Healthcare |
| `16-gaming` | Game development |
| `17-social` | Social impact |
| `18-ai` | AI/ML engineering |
| `19-platform` | Platform engineering |
| `20-mobile` | Mobile development |
| `21-blockchain` | Blockchain & Web3 |
| `22-ai-engineering` | AI engineering |
| `23-creator` | Creator economy |
| `24-accessibility` | Accessibility |
| `25-education` | Education |
| `26-environment` | Environmental tech |
| `27-fintech` | Fintech |
| `28-marketplace` | Marketplace |
| `29-saas` | SaaS |

---

## Step 3: Fill Required Sections in Order

Work through these in priority order. Run lint-template after each section.

### Priority 1: Identity (do first)
1. **Route the Request** — Auto-route table + Intent Route questions
2. **When to Use** — 5+ concrete trigger scenarios
3. **When NOT to Use** — 3+ wrong-tool scenarios with redirections
4. **Ground Rules** — 5-8 rules with Mechanical Trigger + Violation Response

### Priority 2: Workflow (core value)
5. **Core Workflow** — 3-6 phases with time estimates
6. **Decision Trees** — ≥3 ASCII decision trees with YES/NO branches
7. **The Expert's Mindset** — How masters think in this domain
8. **Deliberate Practice** — Mermaid improvement loop + routine table

### Priority 3: Error Prevention (10/10 marker)
9. **Error Decoder** — 4-column table: Symptom | Root Cause | Fix | Lesson
10. **Error Recovery** — 5-row escalation table
11. **Anti-Patterns** — 5-8 ❌/✅ pairs with concrete examples

### Priority 4: Quality Gates (10/10 marker)
12. **Best Practices** — 10 numbered, domain-specific, actionable practices
13. **Production Checklist** — 12+ CR1-CR16+ items with verification methods
14. **Verification Guardrails** — Pre/post-generation checks
15. **What Good Looks Like** — Concrete output excellence description

### Priority 5: Integration (10/10 marker)
16. **Cross-Skill Coordination** — Upstream + downstream tables
17. **Proactive Triggers** — 5-8 patterns with severity indicators (🔴🟡🟠)
18. **Operating at Different Levels** — L1-L5 mastery with scope/autonomy/impact

### Priority 6: Polish
19. **Anti-Rationalization** — 3-5 AR-XX hard rules
20. **State Log** — Decision ledger schema
21. **References** — ≥2 files in references/ with descriptions
22. **Progressive Disclosure** — QUICK/STANDARD/DEEP markers on every major section

---

## Step 4: Validate Continuously

Run after every section:

```bash
# Fast — checks only the one skill
python3 scripts/lib/lint-template.py skills/<domain>/<skill-name>/SKILL.md
python3 scripts/lib/lint-yaml.py skills/<domain>/<skill-name>/SKILL.md
python3 scripts/lib/lint-markdown.py skills/<domain>/<skill-name>/SKILL.md
```

Run before committing:

```bash
# Full governance suite
bash scripts/validate-skills.sh

# Chain symmetry — ensures bidirectional references
python3 scripts/validate_chains.py
```

---

## Step 5: Set Chain References (Bidirectional)

Every skill must have bidirectional chain references:

```yaml
chain:
  consumes_from: ["upstream-skill"]  # This skill depends on upstream-skill
  feeds_into: ["downstream-skill"]   # This skill feeds into downstream-skill
```

**The chain MUST be symmetric:**
- If `skill-A` has `feeds_into: ["skill-B"]`
- Then `skill-B` MUST have `consumes_from: ["skill-A"]`

Run `python3 scripts/validate_chains.py` to verify 0 asymmetries before committing.

---

## Step 6: Test with an Agent

Before submitting a PR, test the skill with at least one AI agent:

```bash
# With Claude Code
claude "use skill my-new-skill to [task]"

# With Copilot CLI
copilot "invoke skill my-new-skill for [scenario]"
```

Verify:
- [ ] The skill auto-routes correctly (Route the Request works)
- [ ] Decision trees guide the agent to correct branches
- [ ] Error decoder catches real failures
- [ ] Output format matches what downstream skills expect

---

## Step 7: Open a PR

```bash
git checkout -b skill/my-new-skill
git add skills/<domain>/my-new-skill/
git commit -m "feat: add my-new-skill"
git push origin skill/my-new-skill
```

Create the PR. The PR template will prompt you to confirm all checklist items.

**CI will run automatically:**
- 13 pre-commit gates (G0–G12)
- validate-skills.sh (13 governance checks)
- markdownlint on SKILL.md
- Chain symmetry validation
- Token budget report
- Plugin manifest validation

All gates are **blocking** — the PR cannot merge if any fail.

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Missing token_budget | CI fails on frontmatter validation | Add `token_budget: 3500` to frontmatter |
| Asymmetric chain | `validate_chains.py` reports orphans | Update the other skill's consumes_from/feeds_into |
| Description too long | YAML lint: >1024 chars | Trim to essentials; move details to body |
| <3 decision trees | Template lint fails | Add decision trees under `## Decision Trees` |
| <5 dollar-quantified gotchas | `Only N dollar-quantified references` | Add `$X,XXX` cost estimates to gotchas |
| Missing DEEP markers | Library audit < 9.5 | Add `**(DEEP)**` to 3+ sections |
| Duplicate headings | Markdown lint warns | Merge or differentiate headings |
| verify-skill.sh not executable | `chmod +x` error | Run `chmod +x scripts/verify-skill.sh` |

---

## Quality Bar Reference

| Grade | What It Means |
|-------|---------------|
| **10/10** | All 22 sections, all progressive disclosure markers, error decoder, bidirectional chains, agent-tested |
| **A (9/10)** | All required sections, basic progressive disclosure, chains present |
| **B (7-8/10)** | Most sections present, usable but lacks depth |
| **C (5-6/10)** | Draft — basic structure, needs filling |
| **F (<5/10)** | Reject — generic, missing structure |

**Target: Every new skill must be 10/10 before merge.** The scaffold gives you a 7/10 skeleton. You add the remaining 3 points through domain expertise.

---

## Need Help?

- **Template reference:** `scripts/references/10-10-template.md` — canonical 22-section spec
- **Quality standards:** `SKILL-QUALITY-STANDARDS.md` — quality bar + domain calibration
- **System design:** `skill-system-design.md` — architecture of the skill system
- **Meta-skills:** Invoke `writing-great-skills` or `dynamic-skill-creator` for AI-assisted skill creation
