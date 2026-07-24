# Conversation Summarization

## Overview

Strategies for compressing conversation history (Level 5) without losing the information the agent needs to maintain continuity.

## When to Summarize

| Turn Count | Strategy | Token Target |
|-----------|----------|-------------|
| 1-10 | Raw history (no summarization) | As-is |
| 11-20 | Light summarization — compress tool outputs > 2K tokens | 50% of raw |
| 21-30 | Medium summarization — decisions + facts only | 30% of raw |
| 30+ | Aggressive summarization — structured session summary | Fixed 3K-5K tokens |

## The KEEP/DROP Framework

**KEEP (essential for continuity):**
- Decisions made and their rationale (e.g., "Chose PostgreSQL over MongoDB because of ACID requirements")
- Facts discovered (e.g., "The auth middleware expects `X-User-Id` header — confirmed in `src/middleware/auth.ts:42`")
- State changes (files created, modified, deleted, or refactored)
- Current task goal and progress
- Open questions or unresolved blockers

**DROP (noise after 5 turns):**
- Raw tool call arguments and outputs (keep outcome, drop internals)
- Intermediate reasoning and thinking-aloud
- Resolved errors and dead-end explorations
- Repeated information (same file mentioned 3+ times → keep once)
- Salutations, acknowledgments, and conversational filler

## Summarization Template

```
## Session Summary (Turns 1-N)

**Current Goal:** [what the agent is working on right now]

**Key Decisions:**
- [Decision 1]: [Rationale]
- [Decision 2]: [Rationale]

**Facts Discovered:**
- [Fact] (source: [file:line])
- [Fact] (source: [file:line])

**State Changes:**
- Created: [file paths]
- Modified: [file paths]
- Deleted: [file paths]

**Active Files:** [files currently being edited]

**Unresolved:** [open questions or blockers]
```

## Progressive Summarization Algorithm

```
FUNCTION summarize_conversation(turns: List[Turn], target_tokens: int) -> str:

    IF len(turns) <= 10:
        RETURN raw_conversation(turns)

    // Extract structured facts from all turns
    decisions = extract_decisions(turns)
    facts = extract_facts(turns)
    changes = extract_state_changes(turns)

    // Keep last 3 turns raw (immediate context)
    recent = turns[-3:]

    // Build summary
    summary = format_template(decisions, facts, changes, recent)

    // Trim to target
    WHILE token_count(summary) > target_tokens:
        // Remove oldest decisions first, then oldest facts
        IF decisions:
            decisions.pop(0)
        ELSE IF facts:
            facts.pop(0)
        ELSE:
            BREAK
        summary = format_template(decisions, facts, changes, recent)

    RETURN summary
```

## Extraction Heuristics

**Decision detection:** Look for phrases like "Let's use...", "I'll go with...", "We should...", "opted for...", "chose..."

**Fact detection:** Look for patterns like "X is located at...", "The reason is...", "confirmed that...", "the error happens because..."

**State change detection:** Track all tool calls of type `edit`, `create`, `delete`, `bash` with `mv`/`rm`/`mkdir`

## Quality Metric

The summarization quality test: Can a fresh agent, given only the summary, correctly answer a question about turn N? Target: > 90% accuracy on fact-recall questions, > 80% on decision-context questions.
