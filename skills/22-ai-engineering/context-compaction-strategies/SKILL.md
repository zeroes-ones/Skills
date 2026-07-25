---
name: context-compaction-strategies
description: Manage token budgets, progressive disclosure, context window optimization, summarization strategies, dual-representation compilation (human-readable vs agent-optimized), structured context pruning, attention budget allocation, context retention policies across multi-turn conversations, state ledger design, and working memory vs long-term context separation. Use when maximizing agent performance under context window constraints, designing token-efficient skill instructions, implementing progressive disclosure pipelines, or optimizing multi-turn agent conversations. Handles token budget analysis, context pruning rules, summarization quality validation, and dual-representation compilation. Do NOT use for general text summarization, document compression for human readers, or optimizing non-AI text processing.
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
> **Portability target:** Spec-level (runs on Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI). No vendor-specific frontmatter fields.

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---:|
| "The model has a 200K context window — we don't need compaction." | Context window size is irrelevant to attention quality. Models attend effectively to ~70% of context. Beyond that, signal-to-noise degrades. A 200K window with 180K of noise is worse than a 10K window with 9K of signal. Compaction is about attention quality, not capacity. |
| "Progressive disclosure adds complexity — just load the full skill." | Loading a 4,500-token skill for a 150-token task burns 4,350 tokens of attention budget on irrelevant content. Across 500 invocations/day, that's 2.1M wasted tokens/day — $6.30/day at $3/M input. Progressive disclosure cuts this to 950 tokens average: $4,650/year saved per skill. |
| "Dual-representation compilation will introduce errors." | Done correctly, the minified form is semantically equivalent — it's a format transform, not summarization. XML tags like `<constraint>NEVER skip validation</constraint>` carry identical semantic payload to the markdown "NEVER skip validation." Validation via eval suite catches any regression before deployment. |
| "Context rotation defense is overengineering — we'll notice redundancy." | Redundancy is invisible without tooling. An agent repeating the same ground rule across 5 turns adds 0 information and consumes 5x the attention budget. Sentence embedding deduplication catches this automatically. Humans cannot track token-level redundancy across 20+ turns. |
| "We'll just summarize when we hit the limit." | Reactive summarization at 95% window saturation means the summarizer runs on a nearly-full context, produces lower-quality output, and the agent already suffered 15 turns of diluted attention. Proactive compaction at 70% yields better summaries and cleaner context. |

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|-------------------|---------------------|
| 1 | NEVER load Tier 3 content without exhausting Tier 1 + Tier 2 first | `jq '.loaded_tiers \| contains(["tier3"])' skill_state.json && jq '.loaded_tiers \| contains(["tier2"]) \| not' skill_state.json` | UNLOAD Tier 3; load Tier 2 decision trees; re-route |
| 2 | NEVER exceed 3 concurrent full-skill loads — attention fragmentation causes skill conflict | `jq '[.active_skills[] \| select(.tier=="full")] \| length' context.json \| awk '{if($1>3) exit 1}'` | EVICT lowest-priority full skill; downgrade to Tier 1 |
| 3 | NEVER compact security-critical sections (gotchas, ground rules, auth constraints) | `grep -c "NEVER\|MUST NOT\|SECURITY\|AUTH" compaction_diff.log \| awk '{if($1>0) exit 1}'` | REVERT compaction on flagged sections; preserve verbatim |
| 4 | NEVER allow context window saturation to exceed 95% — Tier 3 eviction trigger | `python -c "import sys; t=int(sys.stdin.read()); print('EVICT' if t > 0.95*int(sys.argv[1]) else 'OK')" $(cat context_window_size) < token_count.txt` | EVICT all Tier 3 content; compress Tier 2 to headlines only |
| 5 | NEVER compile dual-representation without eval-suite validation | `test -f compiled_skill.xml && python eval_runner.py --skill compiled_skill.xml --suite behavioral_equivalence --threshold 0.95 \| awk '{if($NF<0.95) exit 1}'` | REJECT compiled form; flag semantic drift; recompile |
| 6 | NEVER skip redundancy detection pass before context assembly | `python dedup_check.py --threshold 0.92 --input context_manifest.json \| awk '{if($1>0) exit 1}'` | DEDUPLICATE: remove lower-timestamp duplicate; retain canonical |
| 7 | NEVER allow unproductive loop beyond 3 identical-attempt cycles | `grep -c "ATTEMPT_IDENTICAL" agent_loop_audit.log \| awk '{if($1>=3) exit 1}'` | HALT agent; inject escalation context; require human triage |
| 8 | NEVER place critical guardrails in mid-context (positions 25%-75% of window) | `python attention_zone_check.py --input context_plan.json \| awk '/MID_CONTEXT_GUARDRAIL/{exit 1}'` | RELOCATE guardrails to first 200 tokens (primacy zone) |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

Context compaction is the art of maximizing decision quality per token. You are not compressing text — you are curating attention. Three principles govern everything:

**1. Attention is the scarcest resource.** A model's effective attention bandwidth is ~70% of its context window. Every token beyond that is invisible or dilutes focus on what matters. Treat each token as an attention allocation decision: "Does this token earn its place by improving the agent's next decision?"

**2. Information has a half-life.** A ground rule read at turn 1 is only 60% as likely to be followed at turn 15 (recency-weighted attention decay, λ=0.1 per turn). Repetition is not redundancy — it's attention renewal. The 12 context rotation defense patterns exist because stale context is as dangerous as missing context.

**3. Format is fungible; semantics are sacred.** Markdown is a human convention. XML and JSON-LD are machine conventions. The information payload is identical. Dual-representation compilation achieves 35-50% token reduction without semantic loss because it strips presentation, not meaning.

**Cognitive biases to guard against:**
- *Completeness bias* — "Include everything just in case" (the fastest path to attention dilution)
- *Recency anchoring* — over-weighting the last error vs. the systemic cause
- *Format attachment* — believing markdown carries information that XML doesn't

## Operating at Different Levels

### Quick Scan (~30s)
Check context window saturation. If > 85%, trigger Tier 3 eviction. Verify no skill conflicts (2+ active skills sharing domain keywords). Run: `python context_dashboard.py --quick`

### Standard Engagement (~5min)
Full compaction audit: redundancy detection (0.92 threshold), staleness scoring by last-access, attention zone verification (guardrails in primacy zone, output format in recency zone), unproductive-loop check, dual-representation validation. Run: `python context_dashboard.py --standard`

### Deep Dive (~30min)
Architecture review of the entire compaction pipeline. Includes: progressive disclosure tier calibration with real workload traces, token budget optimization across a 5-skill pipeline, dual-representation compiler refinement for new skill types, and attention allocation modeling with exponential decay simulation across 50-turn conversations.

## When to Use

**Triggers:**
- Skill instruction set exceeds 2,500 tokens — needs progressive disclosure tiering
- Multi-skill agent pipeline with 3+ skills loaded simultaneously
- Agent "forgets" skill instructions mid-conversation (context overflow, Tier 3 leak)
- Token costs exceed benchmark by 40%+ for equivalent tasks
- Agent exhibits looping behavior (3+ identical attempts on same problem)
- Designing a new skill — needs dual-representation compilation upfront
- Agent reasoning degrades after turn 12+ (attention dilution in mid-context)
- Skill conflict detected: 2+ skills share domain keywords, agent routes incorrectly
- Building a skill compiler pipeline for an agent platform

**When NOT to use:**
- Prompt engineering or instruction phrasing → route to `llm-engineer`
- Model fine-tuning or RLHF → route to `ml-ai-engineer`
- API-level token optimization (batch requests, streaming) → route to `backend-developer`
- General code performance optimization → route to `performance-engineer`
- Single-skill, single-turn, well-under-budget invocations

## Route the Request

```
                    ┌─────────────────────────────────┐
                    │    What artifact is present?      │
                    └─────────────┬───────────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
   ┌──────────────┐      ┌──────────────┐        ┌──────────────┐
   │ skill.md     │      │ context.json │        │ agent.log    │
   │ > 2500 tokens│      │ saturation   │        │ loop > 3     │
   └──────┬───────┘      └──────┬───────┘        └──────┬───────┘
          │                     │                       │
          ▼                     ▼                       ▼
   Tier Architecture      Saturation Response    Loop Diagnosis
   (→ Decision Tree 2)    (→ Decision Tree 1)    (→ Decision Tree 6)
```

**Intent-based routing (no artifacts):**
- "My skill is too large" → Start at "Progressive Disclosure Architecture" (Core Workflow, Step 1)
- "Agent forgets instructions mid-conversation" → Start at "Context Rotation Defense Patterns" (Decision Tree 4)
- "Token costs are too high" → Start at "Token Budget Management" (Decision Tree 1)
- "Agent loops on the same error" → Start at "Unproductive-Loop Detection" (Decision Tree 6)
- "Building a skill compiler" → Start at "Dual-Representation Compilation" (Core Workflow, Step 5)
- "Multiple skills conflicting" → Start at "Context Fragmentation Prevention" (Decision Tree 5)

## Core Workflow
<!-- COMPRESSED: Full 213 lines extracted to references/core-workflow.md -->

### Step 1: Progressive Disclosure Architecture

Design the three-tier loading system for every skill:

```
...
> 📎 **Full content (213 lines):** [references/core-workflow.md](references/core-workflow.md)

## Decision Trees                        <decision_tree id="compaction_trigger">
                                         <branch>
├─ Token > 80%?                          <condition>token_count > 0.8 * window</condition>
│  └─ COMPACT NOW                        <action priority="emergency">COMPACT_NOW</action>
                                         </branch>
                                         </decision_tree>

## Gotchas                               <gotchas_json>[
{"id":1,"title":"Over-pruning decisions",
 "impact":"System inconsistency",
 "cost":"$10K-$50K","mitigation":"State ledger
 checkpoint before pruning"}]</gotchas_json>
```

**Compilation pipeline:**
```
1. EXTRACT frontmatter → JSON-LD structured metadata
2. PARSE decision trees → nested <branch> XML elements
3. CONVERT gotchas → JSON-LD array with id, impact, cost, mitigation
4. EXTRACT ground rules → <rule> elements with constraint, trigger, response
5. STRIP markdown formatting — remove **, __, >, blank lines, HTML comments
6. COMPRESS prose — remove filler phrases ("In this section we will...")
7. COMBINE into minified single-line format (no newlines, minimal whitespace)
8. VALIDATE semantic equivalence via eval suite (target: 97%+ behavioral match)
```

**Token reduction targets:**
- Simple skills (no code blocks): 45-50% reduction
- Complex skills (with code blocks): 35-40% reduction (code preserved verbatim)
- Reference-heavy skills: 50-55% reduction (links compressed to inline summaries)

### Step 6: Attention Placement Optimization

Position content for maximum model attention:

```
POSITION      EFFECT          CONTENT TYPE              REASON
──────────────────────────────────────────────────────────────────
First 200     Primacy         Ground Rules, "NEVER"     Model attends most
tokens                        constraints, safety        strongly to opening
                              guardrails                 content

Middle 25-75% Lost-in-middle   NONE — avoid placing     Model is 20-40% less
                               anything critical here   likely to attend to
                                                        mid-context content

Last 100      Recency         Output format spec,       Model's final context
tokens                        required structure,       shapes its response
                              next-step instruction     most directly

Tier 2/3      Lazy-loaded     Detailed examples,        Only loaded when
references                    gotchas, reference docs   specifically needed
```

## Decision Trees

### Decision Tree 1: Token Budget Saturation Response

**Phase 1 — Gather:**
- [ ] Model context window size (tokens)
- [ ] Current token count
- [ ] Active skills with tier level
- [ ] Conversation turn count
- [ ] Saturation % = current_tokens / window_size

**Phase 2 — Decide:**
```
Saturation level?
├── < 70% → HEALTHY — no action needed
│
├── 70-84% → WARNING
│   ├── Run redundancy detection (Pattern 1, 0.92 threshold)
│   ├── Score staleness (Pattern 2); flag sections > 5 turns unreferenced
│   ├── Prepare Tier 3 eviction candidates (lowest priority first)
│   └── Log: "Prepared {N} sections for eviction if saturation reaches 85%"
│
├── 85-94% → CRITICAL
│   ├── EVICT all Tier 3 content; downgrade to Tier 2 representation
│   ├── Compress conversation history (Pattern 3, λ=0.1 decay)
│   ├── Check for unproductive loops (Pattern 4, > 3 identical cycles)
│   ├── Downgrade > 3 active full skills to Tier 1 (Pattern 9)
│   └── Re-check saturation; if still > 85%, proceed to next level
│
└── ≥ 95% → OVERFLOW — EMERGENCY
    ├── EVICT all Tier 3 AND Tier 2 content; Tier 1 only
    ├── Emergency compression: conversation → 1-sentence summary per 5 turns
    ├── Remove all but 1 example per concept
    ├── Drop deliberate practice, references, verification sections
    └── Log complete eviction manifest for recovery
```

### Decision Tree 2: Progressive Disclosure Tier Assignment

**Phase 1 — Gather:**
- [ ] Skill token count (full markdown)
- [ ] Section breakdown: route, ground rules, workflow, decision trees, gotchas, examples, refs
- [ ] Usage frequency of each section (from agent telemetry)
- [ ] Criticality: which sections are MUST-HAVE vs NICE-TO-HAVE

**Phase 2 — Decide:**
```
For each section in skill:
├── Section is "Route the Request" or headline description?
│   └── TIER 1 (150 tokens) — always loaded for intent matching
│
├── Section is "Ground Rules" or "Decision Trees"?
│   └── TIER 2 (800 tokens total) — loaded on intent match
│       ├── Ground rules: full constraint table
│       ├── Decision trees: complete branch logic
│       └── Core workflow steps: numbered procedure
│
├── Section is "Gotchas", "Examples", "Verification", "Deliberate Practice"?
│   └── TIER 3 (lazy-loaded) — only on explicit branch traversal
│       ├── Gotchas: full table with costs
│       ├── Examples: loaded when agent uncertainty detected
│       └── References: loaded when decision tree references specific file
│
└── Section is "Anti-Rationalization" or "Expert's Mindset"?
    └── TIER 3 — motivational/contextual, not operational
```

### Decision Tree 3: Pruning Algorithm Selection

```
Content type to prune?
├── Conversation history (turns 1-N)
│   └── ALGORITHM: Summarization-based (LLM compression to 20%)
│       ├── Keep: decisions made, facts discovered, state changes, blockers
│       ├── Drop: intermediate reasoning, resolved errors, tool call details
│       └── Format: "Turn [N]: [Action] → [Outcome]. Decision: [X]."
│
├── Source code / implementation files
│   └── ALGORITHM: Rule-based truncation
│       ├── NEVER summarize code — paraphrased code is harmful
│       ├── Replace with: `file:path@hash` reference
│       └── If must include: function signatures + docstrings only
│
├── Skill reference files
│   └── ALGORITHM: Embedding-based retrieval (cosine > 0.85)
│       ├── Embed current task description
│       ├── Retrieve top-N reference sections above similarity threshold
│       └── Budget-fill: include until token budget exhausted
│
├── Ground rules / security constraints
│   └── ALGORITHM: NONE — NEVER prune
│       ├── These are the safety net; loss = potential catastrophe
│       └── If must reduce: compress format only (dual-representation), not content
│
└── Examples and illustrations
    └── ALGORITHM: Rule-based truncation by priority
        ├── Priority 1: keep 1 canonical example per concept
        ├── Priority 2+: drop; note "N examples available at [ref]"
        └── If 0 examples remain: flag for human review
```

### Decision Tree 4: Context Rotation Defense Activation

```
What pattern is triggered?
├── Redundancy detected? (Pattern 1, similarity > 0.92)
│   └── DEDUPLICATE: keep latest, drop older, log duplicate
│
├── Staleness detected? (Pattern 2, > 5 turns unreferenced)
│   └── DECAY: apply 0.5x relevance multiplier; evict if score < 0.3
│
├── Recency decay needed? (Pattern 3, every turn boundary)
│   └── RE-RANK: apply e^(-0.1 * turns_since_ref) to all section weights
│
├── Unproductive loop? (Pattern 4, > 3 identical attempts)
│   └── HALT + ESCALATE: stop agent, inject triage context, log incident
│
├── Guardrail in mid-context? (Pattern 5, position 25-75%)
│   └── RELOCATE: move to first 200 tokens (primacy zone)
│
├── Output format not in recency zone? (Pattern 6)
│   └── APPEND: add format spec to last 100 tokens
│
├── Skill conflict? (Pattern 8, > 3 shared keywords)
│   └── DOWNGRADE: lower-priority skill → Tier 1; log conflict
│
├── > 3 concurrent full skills? (Pattern 9)
│   └── EVICT: lowest-priority skill → Tier 1
│
├── Context fragmented? (Pattern 11, > 5 skill sources)
│   └── CONSOLIDATE: keep top 3; downgrade rest
│
└── Major decision completed? (Pattern 12)
    └── CHECKPOINT: serialize to state ledger; prune decision context
```

### Decision Tree 5: Context Fragmentation Prevention

**Phase 1 — Gather:**
- [ ] Active skills list with tier levels
- [ ] Domain keywords per skill
- [ ] Current attention allocation (% of context per skill)
- [ ] Agent's current task description

**Phase 2 — Decide:**
```
How many skills have Tier 2+ content loaded?
├── 1-3 → HEALTHY — no fragmentation risk
│
├── 4-5 → MODERATE RISK
│   ├── Check for keyword overlap (Pattern 8)
│   │   ├── Overlap detected → Downgrade lower-priority skill to Tier 1
│   │   └── No overlap → Monitor but allow
│   └── Enforce attention slot limit (Pattern 9)
│
└── > 5 → HIGH RISK — FRAGMENTATION
    ├── Consolidate: keep top 3 skills at Tier 2+
    ├── Downgrade remaining skills to Tier 1 (headline only)
    ├── Log fragmented skills for post-hoc analysis
    └── Re-check saturation; may trigger eviction (Decision Tree 1)
    
Attention distribution check:
├── Any single skill > 40% of context?
│   └── Potential over-focus — verify skill relevance to current task
│
└── All skills < 10% of context each?
    └── Context too fragmented — agent lacks depth on any single domain
```

### Decision Tree 6: Unproductive-Loop Diagnosis

```
Agent appears stuck in loop
├── STEP 1: Hash last 5 (action, outcome) pairs
│
├── STEP 2: Count identical pairs
│   ├── 3+ identical → UNPRODUCTIVE LOOP CONFIRMED
│   │   ├── HALT agent immediately
│   │   ├── Inject escalation context:
│   │   │   "You have attempted the same action 3+ times with the same
│   │   │    outcome. The previous attempts were: [list]. The outcome
│   │   │    each time was: [outcome]. STOP. Consider: (a) is there a
│   │   │    different approach? (b) is the goal achievable? (c) do you
│   │   │    need more context?"
│   │   ├── Log incident with full loop trace
│   │   └── If loop continues after escalation → require human triage
│   │
│   └── < 3 identical → Continue monitoring
│
├─ STEP 3: Root cause analysis
│   ├── Missing context? → Lazy-load Tier 3 references
│   ├── Conflicting ground rules? → Check for skill conflict (Pattern 8)
│   ├── Attention dilution? → Check saturation; evict if > 85%
│   └── Stale context? → Rotate via recency-weighted re-rank (Pattern 3)
│
└─ STEP 4: Prevention
    ├── Set loop detection threshold per task complexity
    ├── Simple tasks: > 2 identical = halt
    ├── Standard tasks: > 3 identical = halt
    └── Complex tasks: > 4 identical = halt (allow more exploration)
```

## Error Recovery

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Cross-Skill Coordination

| Scenario | Coordinate With | Handoff |
|----------|----------------|---------|
| Skill instruction design for token efficiency | `llm-engineer` | Token budget, tier architecture, prompt placement within skill |
| Multi-agent pipeline context distribution | `system-architect` | Context partitioning strategy, handoff state schema |
| Agent-to-agent state serialization | `agent-handoff-protocol` | State ledger format, decision checkpointing, recovery paths |
| Validating compaction doesn't degrade behavior | `agent-eval-pipeline` | Behavioral equivalence test suite, regression detection |
| Platform-level context infrastructure | `platform-engineer` | Compiler pipeline, token monitoring, eviction policies as platform service |
| Strategic token budget across organization | `staff-engineer` | Per-skill budget allocation, cost modeling, optimization roadmap |
| Prompt engineering within compacted skills | `llm-engineer` | Instruction phrasing for attention optimization, primacy/recency placement |
| Skill conflict resolution at architecture level | `system-architect` | Domain keyword taxonomy, skill boundary definitions |

**Handoff protocol:** When delegating context compaction work that intersects another skill, include: (1) the current token budget and saturation %, (2) the active skill manifest with tier levels, (3) the compaction strategy selected and rationale, (4) the recovery path for pruned content.

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `system-architect` | System context, integration patterns, deployment constraints | Before designing AI/ML pipelines |
| `mlops-engineer` | Model lifecycle, deployment patterns, monitoring requirements | Before deploying ML models to production |

## Proactive Triggers

| Condition | Detection Mechanism | Automatic Action |
|-----------|-------------------|------------------|
| Context window saturation crosses 70% | `python context_monitor.py --check-saturation --threshold 0.70` | Triggers redundancy detection (0.92 threshold) + staleness scoring; prepares Tier 3 eviction candidates |
| Context window saturation crosses 85% | `python context_monitor.py --check-saturation --threshold 0.85` | EVICT all Tier 3 content; compress Tier 2 to decision tree headlines only if still > 85% |
| Context window saturation crosses 95% | `python context_monitor.py --check-saturation --threshold 0.95` | EMERGENCY: evict Tier 3 + Tier 2; Tier 1 only; log full eviction manifest; notify operator |
| Agent executes 3+ identical (action, outcome) cycles | `python loop_detector.py --threshold 3 --window 10` | HALT agent; inject escalation context; log incident; if persists, require human triage |
| 2+ active skills share > 3 domain keywords | `python skill_conflict_detector.py --keyword-threshold 3` | Downgrade lower-priority skill to Tier 1; log conflict; flag for architecture review |
| > 3 skills loaded at Tier 2+ simultaneously | `python attention_monitor.py --max-full-skills 3` | Evict lowest-priority full skill to Tier 1; log eviction |
| Guardrail found in mid-context (25-75% position) | `python attention_zone_check.py --input context_plan.json` | RELOCATE to primacy zone (first 200 tokens); log relocation |
| Section unreferenced for > 5 consecutive turns | `python staleness_monitor.py --threshold 5` | Apply 0.5x relevance decay; flag for eviction on next compaction pass |
| Dual-representation compilation completed | `python eval_runner.py --skill compiled_skill.xml --suite behavioral_equivalence` | Validate semantic equivalence; reject if behavioral match < 95% |
| Conversation exceeds 20 turns without summarization | `python turn_monitor.py --threshold 20` | Force conversation summarization to 20% token density; archive to state ledger |

## What Good Looks Like

✅ **Good — Token Budget Management:**
"Monitored 5-skill pipeline at 68% saturation. Proactive redundancy detection identified 3 duplicate ground rule sections (12% token waste). Deduplicated to canonical versions. Evicted 2 stale Tier 3 gotchas unreferenced for 8+ turns. Result: 62% saturation with no decision-quality loss. Projected savings: $1,240/month."

✅ **Good — Dual-Representation Compilation:**
"Compiled `security-reviewer` skill: 4,800 tokens markdown → 2,640 tokens minified XML (45% reduction). Frontmatter → JSON-LD, decision trees → nested `<branch>` elements, gotchas → JSON array. Eval suite: 98.2% behavioral match across 75 test scenarios. Deploying to production pipeline."

✅ **Good — Unproductive Loop Resolution:**
"Detected loop at turn 14: agent repeatedly attempted same SQL migration fix (3 identical cycles). Halted agent. Injected escalation context with alternative approaches. Agent pivoted to schema redesign approach. Resolved in 2 additional turns vs. projected 8+ turns without intervention. Saved ~$0.45 in loop tokens."

❌ **Bad — Reactive Truncation:**
"Agent hit 97% saturation so I truncated the oldest 40% of context. Unfortunately that included the database schema the agent needed for the current task. Agent generated queries against wrong column names. 3 hours of debugging." [[Violates Ground Rule #4 — never evict without priority scoring]]

❌ **Bad — Lossy Security Summarization:**
"Summarized the auth module's security constraints to save tokens. Summary said 'use secure auth' instead of the original 'NEVER store passwords in plaintext; MUST use bcrypt with cost factor ≥ 12.' Agent implemented MD5 hashing because 'secure auth' was ambiguous. Security regression in production." [[Violates Ground Rule #3 — never compact security-critical sections]]

❌ **Bad — Missing State Ledger:**
"Compacted context at turn 18 without checkpointing. Pruned 3 architecture decisions made at turns 5-8. At turn 22, agent needed to know why microservice A communicates via gRPC not REST. Decision was pruned, rationale lost. Agent proposed REST migration. $15K rework to revert." [[Violates Pattern 12 — always checkpoint before pruning decisions]]

## Deliberate Practice

1. **Token Budget Calibration Drill:** Take a real 10-skill agent pipeline trace. Calculate actual token consumption per skill vs. budgeted. Identify the top 3 budget overruns. Recalibrate tier boundaries. Target: all skills within 15% of budget.

2. **Dual-Representation Compilation Exercise:** Take a 5,000-token skill. Manually compile to minified XML: extract frontmatter → JSON-LD, decision trees → `<branch>` elements, gotchas → JSON array. Measure token reduction. Validate semantic equivalence by having another agent execute both versions on 10 test tasks. Target: ≥ 40% reduction with ≥ 95% behavioral match.

3. **Redundancy Detection Calibration:** Run sentence embedding deduplication on a 50-turn agent conversation. Tune the similarity threshold (start at 0.92). Find the sweet spot: maximize deduplication without removing semantically distinct content. Validate: no unique decisions lost.

4. **Attention Zone Audit:** Take a compiled context. Check: (a) are all "NEVER" constraints in first 200 tokens? (b) is output format in last 100 tokens? (c) is any critical content in positions 25-75%? Fix placement violations. Measure decision quality before/after.

5. **Loop Simulation Exercise:** Create an agent task that intentionally triggers an unproductive loop (e.g., circular dependency in config). Observe: how many cycles before detection? Does the escalation context break the loop? Tune the detection threshold. Document the optimal halt point.

6. **Eviction Recovery Drill:** Take a heavily compacted context (post-95% eviction). Simulate the agent needing pruned information. Can the agent recover from the state ledger? From file references? From conversation summary? Identify unrecoverable information. Strengthen the checkpoint strategy.

7. **Cross-Skill Fragmentation Test:** Load 8 skills simultaneously. Observe attention distribution. Detect keyword conflicts. Apply fragmentation prevention (Pattern 11). Measure: does consolidating to top 3 skills improve decision quality on the primary task?

## Gotchas

| # | Gotcha | Impact | Cost |
|---|--------|--------|------|
| 1 | **Over-pruning active decisions:** Archived a "temporary" architecture choice that later became foundational — agent proposes conflicting replacement | System inconsistency, rework of 3+ dependent components | $10K-$50K in rework |
| 2 | **Lossy security summarization:** Summarized "NEVER use ECB mode for AES; MUST use GCM with random IV" → "use secure encryption" — agent selects ECB mode | Cryptographic vulnerability in production | $100K-$1M+ in breach costs |
| 3 | **Compaction during active generation:** Context changed mid-response — agent's output references pruned sections inconsistently | Corrupted output, silent logical errors, broken references | $5K-$50K in debugging and rewrites |
| 4 | **Missing state ledger for pruned decisions:** No record of what was removed or why — agent cannot recover context when needed | Irreversible information loss, dead-end agent requiring full restart | $20K-$100K in lost context and rework |
| 5 | **False equivalence in dual-representation:** Minified version dropped a negation — "Do NOT use for X" became "Use for X" — agent applies skill to wrong domain | Agent produces garbage output in wrong domain, erodes trust | $10K-$100K in misapplied AI and reputation damage |
| 6 | **Attention dilution from over-caution:** Retained 15 edge-case gotchas "just in case" — agent's attention spread so thin it missed the 1 critical constraint | Critical constraint ignored; agent focused on irrelevant edge cases | $50K-$500K in missed primary concern |
| 7 | **Uniform pruning without priority scoring:** Removed 30% of tokens uniformly — lost 2 critical ground rules but kept 5 verbose examples | Agent violates pruned ground rules, introduces compliance issues | $20K-$200K in compliance/security violations |
| 8 | **Tier 3 loaded without Tier 2 grounding:** Agent received full gotchas but no decision tree context to understand when they apply — misapplied edge-case warnings to standard path | Over-cautious agent, unnecessarily complex solutions | $15K-$75K in over-engineering |

## Verification

| # | Check | Expected |
|---|-------|----------|
| 1 | Token budget per skill declared | All active skills have tier assignments with token budgets |
| 2 | Context saturation < 70% | Healthy operating band; no eviction needed |
| 3 | Context saturation < 85% | No Tier 3 eviction triggered; monitor for growth |
| 4 | Context saturation < 95% | Emergency eviction NOT triggered; Tier 2 content preserved |
| 5 | Redundancy detection passed | Zero duplicate sentences at 0.92 similarity threshold |
| 6 | No security sections compacted | All "NEVER", "MUST NOT", security/auth constraints preserved verbatim |
| 7 | Attention zones correct | Guardrails in primacy zone (first 200 tokens); output format in recency zone (last 100 tokens) |
| 8 | No unproductive loops | < 3 identical (action, outcome) pairs in any 10-turn window |
| 9 | ≤ 3 concurrent full-skill loads | Active skills at Tier 2+ do not exceed 3 |
| 10 | No skill conflicts | No two active skills share > 3 domain keywords |
| 11 | Dual-representation validated | Compiled skill passes behavioral equivalence at ≥ 95% |
| 12 | State ledger populated | All pruned decisions have recovery path recorded in ledger |
| 13 | Compaction logged | Metadata recorded: what was removed, why, when, recoverable? |
| 14 | Recovery tested | Simulated need for pruned information → successfully recovered from ledger or file reference |
| 15 | Code blocks preserved or referenced | No paraphrased code; all code either verbatim or file:hash reference |

## Verification Guardrails

Before delivering work, the agent must verify:

- [ ] **Self-check against What Good Looks Like:** All deliverables meet the quality bar defined above
- [ ] **No broken references:** All file paths, URLs, and skill references resolve correctly
- [ ] **Continuity with State Log:** No prior decisions contradicted without documented rationale
- [ ] **Anti-hallucination check:** No fabricated APIs, version numbers, or capabilities asserted
- [ ] **Error Recovery paths exercised:** Failure modes documented and recovery steps tested
- [ ] **Cross-skill dependencies satisfied:** All upstream skill outputs consumed as documented

If any checkbox fails, revise before delivering. When all pass, add to the state log.

## References

- [token-budget-allocation.md](references/token-budget-allocation.md) — Per-skill budget formulas, saturation thresholds, eviction policy implementation
- [progressive-disclosure-patterns.md](references/progressive-disclosure-patterns.md) — Tier 1/2/3 architecture, boundary enforcement, transition triggers
- [dual-representation-compiler.md](references/dual-representation-compiler.md) — Markdown → XML/JSON-LD compilation pipeline, validation suite
- [context-rotation-defense.md](references/context-rotation-defense.md) — All 12 defense patterns with implementation details and calibration guides
- [state-ledger-design.md](references/state-ledger-design.md) — Ledger schema, checkpoint triggers, recovery procedures
- [summarization-strategies.md](references/summarization-strategies.md) — LLM-based, embedding-based, and rule-based pruning algorithms
- [attention-dilution-metrics.md](references/attention-dilution-metrics.md) — Primacy/recency effect measurements, lost-in-the-middle quantification
- [context-pruning-rules.md](references/context-pruning-rules.md) — Priority-based truncation, section-level eviction rules
- [conversation-history-compaction.md](references/conversation-history-compaction.md) — Progressive summarization, turn boundary compaction
- [information-density-scoring.md](references/information-density-scoring.md) — Token importance classification: decisions > constraints > code > examples > prose
- [compaction-validation.md](references/compaction-validation.md) — Behavioral equivalence testing, semantic drift detection
- [loop-detection-patterns.md](references/loop-detection-patterns.md) — Action/outcome hashing, escalation context injection, prevention strategies

## State Log

This section documents every irreversible decision made during the session. It is non-negotiable and prevents the agent from revisiting settled questions.

| # | Decision | Rationale | Alternatives Considered | Timestamp |
|---|----------|-----------|------------------------|-----------|
| 1 | *[no decisions logged yet]* | — | — | — |

**Rules:**
- Append a new row for each irreversible or hard-to-reverse decision
- Never modify past rows — only append
- If revisiting a decision, add a NEW row (do not edit the old one)
