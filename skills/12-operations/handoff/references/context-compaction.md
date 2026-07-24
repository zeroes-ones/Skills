# Context Compaction

## What Happens During Compaction

When an agent's context window approaches its token limit, the runtime compacts the conversation history. Compaction summarizes earlier turns into condensed representations, preserving the gist but losing specifics — exact file paths, line numbers, command arguments, and micro-decisions.

## What Survives

* High-level topic of conversation
* General approach and major decisions
* Named entities (file names, function names if mentioned frequently)
* Attached files and artifacts

## What Is Lost

* Exact line numbers and code positions
* Command arguments and flags
* Alternative approaches considered and rejected
* The rationale chain: why decision A over B over C
* Mental state: "I was about to edit line 47 to add the null check"
* Test cases thought of but not written
* Blocker resolution conditions and ETAs

## Preparation Protocol

1. **Detect compaction window:** Monitor token usage. At 70-80% consumed, initiate handoff preparation.
2. **Freeze the ledger:** Update `.handoff/ledger.md` with all current state.
3. **Capture mental state:** Record exact line, exact edit planned, and reasoning.
4. **Generate resume command:** One command that puts the next agent exactly where you are.
5. **Verify restartability:** Can a colleague resume in <5 minutes?

## Compaction Signals

* Agent responses become shorter or less detailed
* Agent begins summarizing earlier context
* Agent asks "what were we working on?" more frequently
* Explicit token count warnings from the runtime

## Post-Compaction Recovery

1. Read `.handoff/ledger.md` first — do not rely on compacted context
2. Run the resume command
3. Verify state matches ledger: `git diff --stat ledger_commit..HEAD`
4. If >50 lines changed since ledger commit, rebuild context from git log
