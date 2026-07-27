---
name: "New Skill or Skill Update"
about: "Submit a new skill or update an existing one"
title: "skill: "
labels: ["skill"]
assignees: []
---

## Skill Checklist (complete before submitting)

### Identity & Frontmatter
- [ ] `name` matches directory name (kebab-case)
- [ ] `description` uses "Use when… Handles… Do NOT use…" format, ≤1024 chars
- [ ] `token_budget` declared (2500–5000, proportional to body length)
- [ ] `chain.consumes_from` and `chain.feeds_into` present with valid skill slugs
- [ ] `type`, `status`, `version`, `updated`, `tags`, `license` all present
- [ ] `author` field set

### Required Sections (22 from 10-10-template.md)
- [ ] Route the Request
- [ ] Anti-Rationalization
- [ ] Ground Rules (with Mechanical Trigger + Violation Response columns)
- [ ] The Expert's Mindset
- [ ] Deliberate Practice
- [ ] Operating at Different Levels (L1–L5)
- [ ] When to Use
- [ ] When NOT to Use
- [ ] Decision Trees (≥3)
- [ ] Core Workflow (phased, with time estimates)
- [ ] Best Practices (10 numbered items)
- [ ] Error Decoder (4-column table or domain-adapted format)
- [ ] Error Recovery (5-row escalation table)
- [ ] Cross-Skill Coordination (upstream + downstream tables)
- [ ] Proactive Triggers (5–8 with severity indicators)
- [ ] Anti-Patterns (5–8 ❌/✅ pairs)
- [ ] State Log
- [ ] Production Checklist (12+ CR1–CR16+ items)
- [ ] What Good Looks Like
- [ ] Verification Guardrails
- [ ] References (≥2 files in references/)
- [ ] Gotchas merged into Anti-Patterns (no standalone Gotchas)

### Progressive Disclosure
- [ ] Every major section has `**(QUICK)**` marker
- [ ] At least 3 sections have `**(STANDARD)**` and `**(DEEP)**` markers

### Content Quality
- [ ] Anti-hallucination guardrails: "Admit uncertainty", "Flag your knowledge cutoff", "Never guess security", "[VERIFIED]"
- [ ] ≥8 "Complete when" statements
- [ ] ≥5 dollar-quantified gotchas ($X,XXX)
- [ ] Portability target declared
- [ ] No duplicate headings

### File Structure
- [ ] `scripts/verify-skill.sh` exists and is executable
- [ ] `references/` directory exists with ≥2 files
- [ ] All `references/*.md` links resolve

### Validation (run before pushing)
```bash
# Pre-commit gates (13 checks)
python3 scripts/lib/lint-template.py skills/<domain>/<skill-name>/SKILL.md
python3 scripts/lib/lint-yaml.py skills/<domain>/<skill-name>/SKILL.md
python3 scripts/lib/lint-markdown.py skills/<domain>/<skill-name>/SKILL.md

# Full governance suite
bash scripts/validate-skills.sh

# Chain symmetry check
python3 scripts/validate_chains.py

# Library audit
python3 scripts/audit-library.py
```

### Description of Changes
<!-- Brief description of what this skill does and what inspired it -->

### Domain Review
<!-- Which existing skills does this coordinate with? List upstream/downstream. -->

### Agent Testing
<!-- Which agent(s) did you test this with? (Claude Code, Copilot CLI, etc.) -->
- [ ] Tested with: ___________
- [ ] Skill produces correct output
- [ ] Error decoder catches real errors
- [ ] Decision trees route correctly

---

> **Pre-commit gates will block merge if any check fails.** Run `scripts/lint.sh --all` locally before pushing.
