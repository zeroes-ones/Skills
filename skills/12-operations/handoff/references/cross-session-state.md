# Cross-Session State

## What to Persist

State that survives session boundaries is stored in `.handoff/ledger.md`. The ledger is the only mechanism for cross-session state — there is no shared memory, no database, no file cache beyond what is explicitly written.

## What the Ledger Stores

| Data | Format | Recovery |
|------|--------|----------|
| Task progress | DONE:/DOING:/TODO: prefixes | Read Remaining section, order by priority |
| Decisions | DECIDED: with options, rationale, tradeoffs | Read Decisions section before questioning approach |
| Blockers | BLOCKED: with resolution, ETA, escalation | Check Blockers before starting new work |
| File manifest | Path + operation + purpose | Use to understand what files are in play |
| Mental state | DOING: line number + state description | Resume at exact line, continue thought |

## What NOT to Store in Ledger

* Code snippets > 10 lines — reference the file and line instead
* Conversation transcripts — summarize decisions, don't archive chat
* Personal notes not relevant to task completion
* Speculative todos beyond top 5 — archive to backlog.md

## Coordination with Wayfinder

When using wayfinder investigation tickets, each ticket gets its own ledger. The wayfinder ticket state (pending/active/done) maps to ledger sections:
- pending → no ledger yet
- active → In Progress section is populated
- done → Completed section has DONE: entries

## State Recovery Sequence

1. Read `.handoff/index.md` for active sessions
2. Open the most recent active ledger
3. Check Blockers — any still active?
4. Read In Progress — resume from there
5. Verify git state matches ledger commit
6. Execute Next Steps item #1

## Ledger Merging

When two sessions produce conflicting ledgers (parallel work on same task):
1. Merge Completed sections (union)
2. Merge Decisions sections (if conflict, keep most recent with rationale)
3. Merge Blockers (keep all, deduplicate)
4. Re-prioritize Remaining (critical path first)
5. Add MERGE note with timestamp
