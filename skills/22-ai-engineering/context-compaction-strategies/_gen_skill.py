import sys

SKILL_MD = r'''---
name: context-compaction-strategies
description: Use when optimizing token budgets across a multi-skill agent pipeline, implementing progressive disclosure loading (Tier 1/Tier 2/Tier 3), diagnosing context window overflow causing skill instruction loss, designing dual-representation skill compilers (markdown -> minified XML/JSON-LD for LLM execution), configuring context rotation defense patterns against redundancy and staleness, or setting up token budget monitoring with automatic eviction policies. Handles token budget management (per-skill allocation tracking, context window saturation monitoring at 70%/85%/95% thresholds, automatic Tier-3 eviction on overflow), progressive disclosure architecture (Tier 1: 150-token route+headline for intent matching, Tier 2: 800-token core workflow+decision trees for skill execution, Tier 3: full 4000-token skill with gotchas+references for complex cases), context pruning algorithms (summarization-based with LLM compression to 20% original tokens, embedding-based retrieval using cosine similarity > 0.85 for relevant section extraction, rule-based truncation by section priority tagged in frontmatter), 12 context rotation defense patterns (redundancy detection via sentence embedding deduplication at 0.92 threshold, staleness scoring by section last-access timestamp, recency-weighted attention allocation with exponential decay lambda=0.1 per conversation turn, unproductive-loop detection stopping >3 identical-attempt cycles), attention placement optimization (critical guardrails in first 200 tokens for primacy effect, output format specification in last 100 tokens for recency, mid-context avoidance for detailed examples), dual-representation compilation (extract frontmatter -> decision tree XML -> gotcha JSON-LD -> ground rule array -> combine into minified format at 35-50% token reduction), and context fragmentation prevention (skill conflict detection when 2+ skills share domain keywords, attention slot allocation with max 3 concurrent full skills, lazy-loading reference files only on explicit decision tree branch traversal). Do NOT use for prompt engineering (use llm-engineer), model fine-tuning (use ml-ai-engineer), API optimization (use backend-developer), or general code optimization (use performance-engineer).
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: infrastructure
status: stable
version: 1.0.0
updated: 2026-07-24
tags: [context-management, token-optimization, progressive-disclosure, attention-patterns, dual-representation, prompt-compression]
token_budget: 4500
chain:
  consumes_from:
    - llm-engineer
    - system-architect
    - agent-handoff-protocol
  feeds_into:
    - agent-eval-pipeline
    - platform-engineer
    - staff-engineer
---
'''

print("Script written OK")
