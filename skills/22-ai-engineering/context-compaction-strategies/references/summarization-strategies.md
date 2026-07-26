# Summarization Strategies

## By Content Type

### Conversation History
**Strategy:** Hierarchical summarization
- Turns 1-5 → 2-3 sentence paragraph
- Turns 6-10 → Bullet points of key decisions
- Turns 11+ → 1-line per turn (action + outcome)
- Preserve: decisions, constraints, action items, errors

### Code Changes
**Strategy:** Diff-based summarization
- "Modified 3 files: auth.py (JWT validation), api.py (rate limiting), test_auth.py (7 new tests)"
- Replace file contents with `file:path:hash` references

### Decision Trees
**Strategy:** Path-based pruning
- Keep only the path the agent is currently on
- Prune unexplored branches
- Preserve entry conditions for each pruned branch

### Reference Documentation
**Strategy:** Index-based replacement
- Keep: filename + purpose + key concept (1-2 sentences)
- Remove: full file content
- Recovery: load on explicit reference

## Quality Metrics
- Decision preservation: % of decisions surviving summarization
- False positive rate: % of summaries that misrepresent original
- Recovery time: time to retrieve full context from summary
