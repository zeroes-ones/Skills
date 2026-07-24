# Progressive Disclosure Architecture

## Tier 1: Route + Headline (150 tokens)

Intent matching layer. The absolute minimum needed to determine if this skill applies.

**Content:**
- Skill name and 1-line purpose
- Trigger keywords (exact string matches)
- Exclusion keywords (when NOT to invoke)
- Route table: which intent maps to which workflow

**Example:**
```yaml
name: context-compaction-strategies
tier: 1
route: context_overflow OR token_budget_exceeded OR skill_conflict_detected
exclude: prompt_engineering, model_fine_tuning, api_optimization, code_optimization
```

**When to upgrade:** Route matched AND complexity score > 3/10.

---

## Tier 2: Core Workflow + Decision Trees (800 tokens)

Skill execution layer. All content needed to perform the standard workflow.

**Content:**
- Ground rules (mechanical triggers with violation responses)
- Core workflow steps (numbered, executable)
- Decision trees (all branches, conditions, actions)
- Key gotchas (top 5, one-line each with severity)
- Cross-skill handoff instructions
- Verification checklist (top 10 items)

**Example:** Full decision tree with all branches expanded, executable ground rules with shell commands.

**When to upgrade:** Adversarial input detected OR prior execution failed at Tier 2 OR error rate > 5%.

---

## Tier 3: Full Skill (4000 tokens)

Complete reference. Gotchas, edge cases, examples, reference files.

**Content:**
- Full gotcha catalog (all entries with cost estimates)
- Reference file summaries and load-on-demand triggers
- Deliberate practice exercises
- Anti-rationalization table (all entries)
- Proactive triggers (all 10 automated conditions)

**Load triggers:**
- Agent explicitly requests full skill
- Tier 2 execution failed with non-trivial error
- Adversarial input pattern matched
- Domain complexity score > 7/10
- Audit or compliance review context

---

## Transition Rules

| From | To | Trigger | Guard |
|------|----|---------|-------|
| Tier 1 | Tier 2 | Route matched + complexity > 3 | Verify route correctness before loading |
| Tier 2 | Tier 3 | Execution failure OR adversarial pattern | Confirm Tier 2 exhaustively attempted |
| Tier 3 | Tier 1 | Task completed OR timeout | Archive execution context to state ledger |
| Any | Evicted | Context saturation > 95% | Dump to state ledger; set recovery path |

---

## Token Budget Allocation by Tier

| Tier | Tokens | % of Budget | Cumulative |
|------|--------|------------|------------|
| 1 | 150 | 3.3% | 3.3% |
| 2 | 800 | 17.8% | 21.1% |
| 3 | 3,550 | 78.9% | 100% |

**Aggressive mode (high-volume pipelines):**
- Tier 1: 100 tokens
- Tier 2: 500 tokens
- Tier 3: on-demand only (never pre-loaded)

---

## Implementation Reference

```python
class ProgressiveDisclosure:
    TIERS = {
        1: {"tokens": 150, "threshold": 0.3},
        2: {"tokens": 800, "threshold": 0.5},
        3: {"tokens": 3550, "threshold": 0.7},
    }

    def resolve(self, complexity: float, prior_failure: bool, adversarial: bool) -> int:
        if adversarial or prior_failure or complexity > 0.7:
            return 3
        if complexity > 0.3:
            return 2
        return 1
```
