# Context Pruning Rules

## Pruning Priority (Remove First)
1. **Resolved conversations** — Issues that have been addressed and closed
2. **Duplicate examples** — Same pattern shown multiple times
3. **Verbose explanations** — Prose that can be compressed to structured format
4. **Historical exploration** — Paths considered but not chosen (archive to ledger)
5. **Boilerplate text** — Standard disclaimers, repeated context

## Never Prune (Keep Always)
1. **Active decisions** — Any decision with `status: active`
2. **Negative constraints** — All "NEVER", "MUST NOT", "DO NOT" rules
3. **Security requirements** — Authentication, authorization, data protection
4. **Current task context** — The immediate problem being solved
5. **Error state** — Active errors and their context

## Pruning Triggers
| Condition | Action | Target Reduction |
|-----------|--------|-----------------|
| Context > 80% window | Emergency prune | 30% |
| Context > 60% window | Proactive prune | 15% |
| Turn count > 15 | Summarize early turns | 40% of history |
| Agent-to-agent handoff | Full compaction | 50% |
| Idle > 5 turns | Archive resolved items | 20% |
