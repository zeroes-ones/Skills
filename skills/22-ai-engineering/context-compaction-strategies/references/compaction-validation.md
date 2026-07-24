# Compaction Validation

## Pre-Compaction Checklist
- [ ] State ledger backed up (all decisions recorded)
- [ ] Critical constraints identified (will NOT be pruned)
- [ ] Compaction target set (token count or % reduction)
- [ ] Recovery paths documented for all pruned content

## Post-Compaction Validation

### Structural Validation
- [ ] All required sections still present
- [ ] Ground Rules complete and unchanged
- [ ] Reference links still resolve
- [ ] No truncated sentences or broken markdown

### Semantic Validation
- [ ] Decision trees: same number of paths, same outcomes
- [ ] Gotchas: all dollar-quantified, no lost constraints
- [ ] Anti-Rationalization: all clauses preserved

### Behavioral Validation
- [ ] Run eval suite with compacted vs full context
- [ ] Compare decision outputs (should be identical)
- [ ] Compare code quality (should be equivalent)
- [ ] Any deviation → investigate and fix compaction rules

## Automated Validation Script
```bash
# Verify compaction quality
python scripts/validate-compaction.py \
  --original skills/system-architect/SKILL.md \
  --compacted .skills-compiled/system-architect.xml \
  --eval-suite evals/system-architect/
```
