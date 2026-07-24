# Context Failure Postmortem Template

## Overview

A structured template for diagnosing why an agent produced a wrong answer, missed a requirement, or degraded in performance. Use this when context engineering is the suspected root cause.

## Template

### 1. Incident Summary

- **Date/Time:** [when the failure occurred]
- **Agent/Model:** [e.g., Claude 3.5 Sonnet via Copilot CLI]
- **Task:** [what the agent was asked to do]
- **Expected behavior:** [what should have happened]
- **Actual behavior:** [what actually happened]
- **Severity:** [Critical / High / Medium / Low]

### 2. Context Snapshot at Time of Failure

```
Turn number: [N]
Context window utilization: [X%]
Token budget allocation:
  L1 (Rules):    [tokens] / [budget]
  L2 (Specs):    [tokens] / [budget]
  L3 (Source):   [tokens] / [budget]
  L4 (Errors):   [tokens] / [budget]
  L5 (History):  [tokens] / [budget]
Cache hit: [Yes/No]
```

### 3. Root Cause Classification

- [ ] **Missing critical context** — Required information was excluded from context
  - Which level was missing? [L1 / L2 / L3 / L4 / L5]
  - What specific file/information was needed?
  - Why was it excluded? (relevance score too low / budget exhausted / summarization dropped it)

- [ ] **Context pollution** — Irrelevant information confused the agent
  - What polluted the context?
  - Which pollution pattern does this match? (see `context-polution-patterns.md`)

- [ ] **Context window overflow** — Instructions or critical context were truncated
  - What was truncated?
  - At what utilization did the truncation occur?

- [ ] **Conversation history degradation** — Summarization dropped critical information
  - What was lost in summarization?
  - At which turn was the information originally present?

- [ ] **Cache-induced staleness** — Agent operated on stale cached context
  - What changed between cache creation and the failure?
  - Was the cache TTL exceeded?

### 4. Dollar Cost Analysis

```
Tokens wasted on irrelevant context: [N]
Cost of wasted tokens: $[X.XX]
Extra turns caused by the failure: [N]
Cost of extra turns: $[X.XX]
Engineering time to fix the resulting issue: [N hours] × $[rate] = $[X.XX]
TOTAL INCIDENT COST: $[XXX.XX]
```

### 5. Fix and Prevention

- **Immediate fix:** [what to change right now]
- **Systemic fix:** [what to change in the context pipeline]
- **Detection rule:** [what monitoring to add to catch this next time]
- **Ground Rule update:** [does a new Ground Rule need to be added?]

### 6. Before/After Comparison

**Before (failing context assembly):**
- [list files included, token counts, relevance scores]

**After (fixed context assembly):**
- [list files included, token counts, relevance scores]

### Example Postmortem

**Incident:** Agent refactored auth middleware but removed CSRF protection because `csrf.ts` was excluded from context.

**Root cause:** Missing critical context (L3). `csrf.ts` had relevance score 0.38 (below 0.4 threshold) because it wasn't a direct dependency of the edited file — it was invoked via middleware chain, invisible to static import analysis.

**Cost:** 3 hours engineering time to re-add CSRF + 1 hour code review + $0.12 wasted tokens = ~$612.

**Fix:** Add "middleware chain" detection to proximity scoring. Files in the same middleware/plugin chain get a +0.2 proximity boost regardless of static import visibility.
