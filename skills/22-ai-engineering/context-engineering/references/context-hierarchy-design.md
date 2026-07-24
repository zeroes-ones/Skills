# Context Hierarchy Design

## Overview

The 5-level context hierarchy is the foundational architecture for all context assembly decisions. Each level has a distinct purpose, inclusion rule, and failure mode.

## Level 1: Rules Files (Always Included)

**Purpose:** Define agent behavior, constraints, and operational boundaries.

**Examples:**
- `.cursorrules` — Cursor-specific behavior rules
- `CLAUDE.md` / `COPILOT.md` — Agent-specific instructions
- `SKILL.md` — Skill definitions and workflows
- `.github/copilot-instructions.md` — Organization-wide rules

**Inclusion rule:** ALWAYS. No exceptions. These files are the agent's constitution. If they don't fit, the token budget is wrong, not the inclusion decision.

**Token range:** 2K-8K tokens (should be kept tight; audit quarterly for bloat)

**Failure mode when excluded:** Agent operates without constraints. Produces output that violates org standards, security policies, or task-specific requirements.

## Level 2: Specs (Included When Relevant)

**Purpose:** Define what should be built and why.

**Examples:**
- PRDs (Product Requirement Documents)
- ADRs (Architecture Decision Records)
- API contracts (OpenAPI specs, GraphQL schemas)
- Data models (ERDs, schema definitions)
- Design documents, technical specs

**Inclusion rule:** Semantic relevance to current task. Use embedding similarity > 0.6 threshold. If the task mentions a feature name or component, include the corresponding spec.

**Token range:** 5K-20K tokens

**Failure mode when excluded:** Agent builds the wrong thing. Correct implementation of incorrect requirements.

## Level 3: Source Files (Selectively Included)

**Purpose:** The code the agent reads and modifies.

**Inclusion rule:** Relevance-scored with tiered priority (A/B/C). See `file-relevance-scoring.md` for methodology.

**Priority tiers:**
- **A (always):** Files the agent is currently editing or has edited in this session
- **B (conditional):** Direct dependencies (imports) of Priority A files  
- **C (stretch):** Same-module siblings, test files for Priority A

**Token range:** 30K-80K tokens (typically 60-70% of total context)

**Failure mode when over-included:** Context bloat, degraded reasoning, higher costs
**Failure mode when under-included:** Agent doesn't understand dependencies, writes conflicting code

## Level 4: Error Output (Debug Only)

**Purpose:** Diagnose failures.

**Inclusion rule:** Only when the task is debugging. Even then, trim aggressively.

**Sub-levels:**
- **4a:** Last 50 lines of error output + full stack trace
- **4b:** Last 3 attempted fixes and their outcomes
- **4c:** Relevant log entries (filtered by timestamp proximity to error)

**Token range:** 1K-10K tokens

**Failure mode when included unnecessarily:** Noise that distracts from correct code. Agent tries to fix errors that are already resolved.

## Level 5: Conversation History (Summarized)

**Purpose:** Maintain continuity across turns.

**Inclusion rule:** Raw for turns 1-10. Summarized for turns 11+. Fully compressed for turns 30+.

**What to keep in summary:**
- Decisions made and rationale
- Facts discovered (with file:line references)
- State changes (files modified, configs changed)
- Open questions or unresolved blockers

**What to drop:**
- Tool call internals (arguments, raw outputs)
- Resolved errors and dead-end explorations
- Thinking aloud and intermediate reasoning

**Token range:** 3K-15K tokens

## Cross-Level Rules

1. L1 must occupy the first N tokens (stable prefix for caching)
2. L4 may only be included after L1-L3 have been allocated
3. L5 grows monotonically; budget must accommodate growth
4. No level may borrow budget from L1
