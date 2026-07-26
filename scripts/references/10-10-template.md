# 10/10 Skill Template — Canonical Reference

Every SKILL.md must have ALL sections below. Skills receive a grade A (10/10), B (8/10), C (6/10), or F (<6/10).

## Required Sections (22 total)

### 1. Route the Request
- **Auto-Route:** Table with conditions that trigger without user input
- **Intent Route:** Questions to ask user when auto-route doesn't match

### 2. Anti-Rationalization — No Excuses
- 3-5 hard rules that the agent CANNOT rationalize around
- Format: `**AR-XX [Topic]:** You CANNOT [violation]. [why].`

### 3. Ground Rules — Read Before Anything Else
- 5-8 mechanical rules (R1 through R8)
- Each has a concrete trigger condition

### 4. The Expert's Mindset
- 3-5 paragraphs on how world-class practitioners think
- Subsections: What [Domain] Masters Know, When to Break Your Own Rules

### 5. Deliberate Practice
- Mermaid graph showing improvement loop
- Table with level-based routines (Novice/Intermediate/Advanced/Expert)

### 6. Operating at Different Levels
- L1 through L5 mastery levels with scope, autonomy, impact
- Each level: what the practitioner does at that stage

### 7. When to Use
- 4-6 concrete scenarios (with file/dependency detection if possible)
- Each: Condition + Why this skill

### 8. When NOT to Use
- 3-5 scenarios where this skill is the WRONG tool
- Each: Condition + Which skill to use instead

### 9. Decision Trees
- 2-4 decision trees with ASCII art
- Each node has clear YES/NO branches

### 10. Core Workflow
- Phased workflow with time estimates per phase
- Phase 1 (~X min), Phase 2 (~Y min), etc.
- Each phase: concrete deliverables

### 11. Best Practices ⭐ (MISSING IN 184/189 SKILLS)
- **10 numbered domain-specific best practices**
- Format: `N. **Header sentence.** Explanation sentence or two.`
- Each must be actionable and specific to the domain
- NOT generic advice ("write tests" — too generic)
- Example: `1. **One event type per topic/queue** — Mixing forces filtering, breaks ordering.`

### 12. Error Decoder ⭐ (MISSING IN 68/189 SKILLS)
- 4-column table: Symptom | Root Cause | Fix | Lesson
- 5-6 domain-specific war stories with real failure narratives
- Each row tells a mini-story of a real production failure
- "Lesson" column captures the architectural insight

### 13. Error Recovery
- 5-row generic escalation table: Symptom | First Action | If That Fails | Last Resort
- Hard failure boundary after 3 approaches
- This is the ONLY generic section — it's intentionally the same across most skills

### 14. Cross-Skill Coordination
- Upstream table: Skill | Artifact | What You Need
- Downstream table: Skill | Deliverable | What They'll Do
- 3-5 upstream entries, 3-5 downstream entries

### 15. Proactive Triggers
- T1 through T10 patterns that auto-trigger this skill
- Each: detectable pattern + what to do

### 16. Anti-Patterns ⭐ (MISSING — often called "Gotchas")
- 5-8 common mistakes that even experienced practitioners make
- Each: Pattern + Why it fails + What to do instead
- NOT general advice — specific failure modes

### 17. State Log
- Schema: Turn | Action | Decision | Risk Accepted | Mitigation
- Anti-Drift Check instructions

### 18. Production Checklist ⭐ (MISSING IN 64/189 SKILLS)
- 12+ numbered checklist items (CR1 through CR16+)
- Format: `N. **Check:** Description — Verification method`
- Concrete, verifiable, not aspirational

### 19. What Good Looks Like
- 1-2 paragraphs describing output excellence
- Optional: Signs of Excellence / Signs of Dysfunction sub-tables

### 20. Verification Guardrails
- Pre-generation checks
- Post-generation validation

### 21. References
- At least 2 reference files in `references/` directory
- Each: path + one-line description

### 22. Gotchas (optional legacy section — can be merged into Anti-Patterns)
- Legacy skills have this. When upgrading, merge Gotchas content into Anti-Patterns.
- Remove standalone Gotchas section.

---

## Depth Markers ⭐ (MISSING FULL SET IN 160/189 SKILLS)

Every major section heading MUST carry a depth marker:
- `**(QUICK)**` — essential for basic output
- `**(STANDARD)**` — thorough for typical scenarios
- `**(DEEP)**` — exhaustive for critical/edge cases

At minimum, 3 sections must have all three markers:
- **Decision Trees** or **Core Workflow**
- **Error Decoder**
- **Production Checklist**

---

## Scale Depth ⭐ (MISSING IN 68/189 SKILLS)

Replace or augment `## Operating at Different Levels` with:

```
### Solo (0-10 users)
### Small Team (10-100 users)
### Medium Team (100-10K users)
### Enterprise (10K+ users)
### Transition Triggers
```

Each level describes what CHANGES at that scale (tooling, process, architecture).

---

## Upgrade Priority

When upgrading a skill, add elements in this order:
1. **Best Practices** (highest impact — defines domain wisdom)
2. **Depth Markers** on 3+ major sections (mechanical but critical for token efficiency)
3. **Anti-Patterns** (merge Gotchas if present, create fresh if not)
4. **Production Checklist** (if missing — 12+ numbered items)
5. **Scale Depth** (if missing — Solo/Small/Medium/Enterprise)
6. **Error Decoder** (if missing — 5-6 domain war stories)
