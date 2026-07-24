# Context Pruning Rules

Priority-based truncation with section-level eviction policies.

## Priority Hierarchy

| Priority | Section Type | Eviction Rule | Recovery |
|----------|-------------|---------------|----------|
| P10 | Ground Rules, Security Constraints | NEVER evict | N/A |
| P9 | Decision Trees | Last to evict (95%+ saturation) | Rebuild from state ledger |
| P8 | Gotchas (top 3) | Keep verbatim | File reference |
| P7 | Core Workflow Steps | Summarize to 30% | Expand from reference |
| P5 | Cross-Skill Handoff Tables | Keep headers, drop body | Reload on handoff |
| P4 | Gotchas (4-8) | Drop; keep one-line summary | File reference |
| P3 | Examples | First to drop | Reload on demand |
| P2 | Deliberate Practice | Drop entirely | Skip section |
| P1 | Prose/Filler Text | Strip unconditionally | N/A |

## Eviction Triggers

1. **70% saturation:** Warn; begin stripping P1-P2 content
2. **85% saturation:** Prune P3-P4; summarize P7 to headlines
3. **95% saturation:** Emergency eviction of all P5-P9 except P10; P10 stays verbatim

## Rule-Based Truncation Algorithm

```
function prune(sections, saturation_pct):
    if saturation_pct < 0.70: return sections  # healthy
    if saturation_pct < 0.85:
        return drop(sections, [P1, P2])
    if saturation_pct < 0.95:
        return drop(sections, [P1, P2, P3, P4]) + summarize(P7, 0.30)
    # Emergency
    return keep(sections, [P10]) + one_line_summaries(sections, [P8, P9])
```

## Security Preservation
Sections matching `NEVER|MUST NOT|SECURITY|AUTH|COMPLIANCE|PII` are flagged
as P10 regardless of declared priority and are NEVER pruned.
