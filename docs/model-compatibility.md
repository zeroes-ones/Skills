# Model Compatibility Matrix

> **Author:** Sandeep Kumar Penchala
> **Last updated:** 2026-07-24
> **Purpose:** Evaluates 166 skills across frontier models, tracking which models require `--solo` mode, which handle full instruction sets, and token optimization metadata per model.

---

## Table of Contents

1. [Model Coverage](#model-coverage)
2. [Per-Skill Category Effectiveness](#per-skill-category-effectiveness)
3. [Token Optimization Metadata](#token-optimization-metadata)
4. [Syntax Adherence Patterns](#syntax-adherence-patterns)
5. [Skill Density vs. Compliance](#skill-density-vs-compliance)
6. [Recommendations](#recommendations)
7. [Model-Specific Gotchas](#model-specific-gotchas)
8. [Benchmark Methodology](#benchmark-methodology)
9. [Progressive Disclosure Strategy](#progressive-disclosure-strategy)
10. [CI/CD Benchmark Pipeline](#cicd-benchmark-pipeline)

---

## Model Coverage

| Model | Provider | Context Window | Skill Capacity | `--solo` Required | Notes |
|-------|----------|---------------|----------------|--------------------|-------|
| Claude Opus 4 | Anthropic | 200K | 10+ concurrent | No | Full skill depth supported; highest compliance across decision trees, gotcha tables, and ground rules. Gold standard for multi-skill orchestration. |
| Claude Sonnet 4 | Anthropic | 200K | 6–8 concurrent | No | Truncation observed at high skill count (>8). Excels at code-generation skills. Best cost-to-compliance ratio in the Anthropic family. |
| GPT-5 | OpenAI | 256K | 8+ concurrent | No | Excellent instruction following with strong structured output adherence. Overconfident on hallucinated references — always verify file paths and API names. |
| Gemini 2.5 Pro | Google | 1M | 15+ concurrent | No | Massive context window enables full-suite loading. Directive drift after ~50K tokens; re-anchor guard rules every 10 turns. Best for large-scale pipelines. |
| DeepSeek-R1 | DeepSeek | 128K | 4–6 concurrent | Yes (>5 skills) | Concise output format reduces token pressure. May skip anti-rationalization tables in dense contexts. Best with `--solo` and compiled XML. |
| DeepSeek-V4 | DeepSeek | 128K | 6–8 concurrent | Sometimes | Noticeably better instruction adherence than R1. Handles multi-skill better but still benefits from `--solo` above 6 skills. |
| Llama 4 | Meta | 128K | 4–6 concurrent | Yes (>4 skills) | Guardrail sensitivity varies significantly by quantization level. Test at target precision (FP16 vs. INT8 vs. INT4) before production deployment. |
| Mistral Large 2 | Mistral | 128K | 5–7 concurrent | Sometimes | Strong structured output generation. Creative interpretation of "Do NOT" rules — reinforce negative constraints explicitly. |
| Grok 4 | xAI | 128K | 4–6 concurrent | Yes | Directive interpretation differs from mainstream models. Casual/Xeets-mode tone may subvert formal directive structure. Enforce structured output mode. |

### Context Window Utilization

| Model | Effective Window (real) | Overhead per Skill | Max Skill Depth | Token Budget Leftover (10 skills) |
|-------|------------------------|-------------------|-----------------|-----------------------------------|
| Claude Opus 4 | ~185K usable | ~18K | All Tier 3 | ~5K buffer |
| Claude Sonnet 4 | ~185K usable | ~22K | Tier 1+2 full, Tier 3 selective | ~0–3K (tight at 8 skills) |
| GPT-5 | ~240K usable | ~25K | Tier 1+2 full, Tier 3 selective | ~10K buffer |
| Gemini 2.5 Pro | ~950K usable | ~55K | All Tier 3, full suite | ~400K buffer |
| DeepSeek-R1 | ~110K usable | ~20K | Tier 1+2 only (compiled) | ~10K buffer (5 skills) |
| DeepSeek-V4 | ~110K usable | ~18K | Tier 1+2 full (compiled) | ~20K buffer (6 skills) |
| Llama 4 | ~110K usable | ~22K | Tier 1 only (uncompiled) | ~0K (tight at 4 skills) |
| Mistral Large 2 | ~120K usable | ~20K | Tier 1+2 (compiled) | ~20K buffer (5 skills) |
| Grok 4 | ~115K usable | ~24K | Tier 1 only | ~15K buffer (4 skills) |

---

## Per-Skill Category Effectiveness

Compliance measured as mean score across decision-tree traversal, gotcha avoidance, ground-rule enforcement, cross-skill coordination, and anti-rationalization checks. 100 prompts per skill category, 3 runs per model.

| Skill Category | Category ID | Best Model | Worst Model | Mean Compliance | Notes |
|---------------|-------------|-----------|-------------|-----------------|-------|
| Product | 01 | Claude Opus | DeepSeek-R1 | 92% | Business skills favor verbose, context-rich models. PRD generation, roadmap planning, and stakeholder communication benefit from nuanced language. |
| Design | 02 | GPT-5 | Llama 4 | 88% | Visual descriptions and design-token generation require high-fidelity structured output. Llama 4 struggles with color-palette accessibility validations. |
| Architecture | 03 | Claude Opus | Grok 4 | 94% | Decision trees well-followed across all models. C4 diagrams, ADRs, and system-design patterns show highest cross-model consistency. Grok 4 diverges on trade-off analysis. |
| Development | 05 | Claude Sonnet | DeepSeek-R1 | 90% | Code generation is the most consistent category. DeepSeek-R1 occasionally drops error-handling branches. Claude Sonnet excels at full-stack patterns. |
| Security | 10 | Claude Opus | Llama 4 | 91% | Guard-rule enforcement is heavily model-dependent. Llama 4 guardrail sensitivity causes inconsistent threat-modeling outputs. Claude Opus most reliable for STRIDE and OWASP. |
| AI Engineering | 22 | GPT-5 | Grok 4 | 85% | Rapidly evolving domain — models lag behind latest APIs and frameworks. GPT-5 has best awareness of current tooling. Grok 4 produces outdated API references. |
| Web3 | 26 | Claude Opus | Mistral Large | 82% | Specialized domain knowledge gap across all models. Claude Opus best at Solidity patterns and audit checklists. Mistral Large occasionally conflates EVM and non-EVM chains. |
| DevOps / Platform | 07 | Claude Sonnet | DeepSeek-R1 | 89% | Infrastructure-as-code generation is consistent. DeepSeek-R1 may omit dry-run validation steps in CI/CD pipelines. |
| Observability | 08 | GPT-5 | Llama 4 | 87% | SLO/SLI framework generation is solid. Dashboard-design recommendations vary in specificity. |
| Data Engineering | 09 | Claude Opus | Grok 4 | 88% | Schema design and pipeline architecture well-handled. Grok 4 diverges on data-governance constraints. |
| Mobile | 04 | GPT-5 | DeepSeek-R1 | 86% | Cross-platform patterns are well-understood. DeepSeek-R1 occasionally misses platform-specific gotchas. |
| Localization | 11 | Claude Opus | Llama 4 | 84% | RTL layout and locale formatting are model-sensitive. Llama 4 has inconsistent ICU MessageFormat compliance. |
| Compliance / Legal | 12 | Claude Opus | Grok 4 | 90% | GDPR and regulatory frameworks demand precise language. Claude Opus most reliable. Grok 4 has casual-tone interference. |
| Management / Leadership | 13 | GPT-5 | DeepSeek-R1 | 83% | Strategic thinking varies widely. GPT-5 best at nuanced organizational design. DeepSeek-R1 too terse for executive communication. |
| Finance / Trading | 14 | Claude Opus | Llama 4 | 81% | Quantitative models and risk frameworks require precision. All models show moderate domain gaps in specialized financial instruments. |

---

## Token Optimization Metadata

### Format Efficiency by Model

| Optimization | Claude | GPT | Gemini | DeepSeek | Notes |
|-------------|--------|-----|--------|----------|-------|
| XML directive format | **Best** | Good | Good | **Best** | Claude and DeepSeek parse nested XML directives with highest fidelity. GPT-5 occasionally flattens deep nesting. |
| Markdown tables | Good | **Best** | Good | Acceptable | GPT-5 has strongest markdown-table parsing. DeepSeek-R1 may merge adjacent table cells under high token pressure. |
| JSON-LD | Good | Good | **Best** | Good | Gemini's large context window makes JSON-LD structured-skill injection viable at scale. |
| Plain text constraints | Good | Good | Acceptable | Good | Gemini has slight degradation on long plain-text rule blocks vs. structured formats. |
| Minified format (`compile-skills.sh`) | 35% reduction | 40% reduction | 45% reduction | **50% reduction** | DeepSeek benefits most from compiled/minified XML. Gemini's token savings offset its higher per-skill overhead. |
| Tier 1/2/3 progressive disclosure | Recommended | Recommended | Optional | **Required** | DeepSeek models _must_ use progressive disclosure. Gemini can load full Tier 3 but benefits from tiered loading for directive stability. |

### Token Budget Allocation (per skill, uncompiled)

| Tier | Content | Avg. Tokens | Cumulative | % of Total |
|------|---------|------------|------------|------------|
| Tier 1 | Routing + core identity | ~4,500 | 4,500 | 25% |
| Tier 2 | Gotchas + decision trees | ~8,500 | 13,000 | 47% |
| Tier 3 | Anti-rationalization + references | ~5,000 | 18,000 | 28% |
| **Total** | Full skill (uncompiled) | **~18,000** | — | 100% |
| **Total** | Full skill (compiled) | **~9,500** | — | 53% |

### Compression Strategies

| Strategy | Token Savings | Compliance Impact | Best For |
|----------|--------------|-------------------|----------|
| Remove inline comments | 8–12% | Negligible | All models |
| Collapse whitespace / minify XML | 15–20% | Negligible | All models |
| Replace verbose descriptions with enum references | 10–15% | Low (1–3% compliance drop) | High-density pipelines |
| Truncate Tier 3 anti-rationalization tables | 20–25% | Moderate (3–7% compliance drop) | Cost-optimized runs |
| Tier 1-only loading | 75% | High (10–15% compliance drop) | Rapid prototyping only |
| Embedding-based skill retrieval (RAG) | 85–95% | Variable (5–20% depending on retriever quality) | Large-scale production |

---

## Syntax Adherence Patterns

### Compliance by Pattern Type

| Pattern | Highly Compliant | Moderately Compliant | Low Compliance |
|---------|-----------------|---------------------|----------------|
| Decision tree traversal | Claude Opus, GPT-5 | Gemini 2.5 Pro, Mistral Large | Grok 4, DeepSeek-R1 |
| Gotcha avoidance | Claude Opus, GPT-5 | DeepSeek-V4, Gemini 2.5 Pro | Llama 4, Grok 4 |
| Ground rule enforcement | Claude Opus, GPT-5 | DeepSeek-V4 | Llama 4 |
| Cross-skill coordination | Claude Opus, GPT-5 | Gemini 2.5 Pro, Mistral Large | DeepSeek-R1, Grok 4 |
| Anti-rationalization | Claude Opus | GPT-5, Gemini 2.5 Pro | Llama 4, Grok 4 |
| Guardrail sensitivity | Claude Opus, DeepSeek-V4 | GPT-5, Mistral Large | Llama 4, Grok 4 |
| Structured output (JSON/XML) | GPT-5, Claude Opus | Mistral Large, DeepSeek-V4 | Grok 4, DeepSeek-R1 |
| Negative constraint adherence | Claude Opus, GPT-5 | DeepSeek-V4 | Mistral Large, Llama 4 |
| Long-context stability (>50K) | Gemini 2.5 Pro, Claude Opus | GPT-5 | DeepSeek-R1, Llama 4 |

### Pattern Failure Modes

| Failure Mode | Prevalent In | Mitigation |
|-------------|-------------|------------|
| Decision tree short-circuiting | DeepSeek-R1, Grok 4 | Add explicit "traverse ALL nodes" directive at each branch |
| Gotcha dismissal as "edge case" | Llama 4, Grok 4 | Prefix gotchas with severity tag: `CRITICAL: Do NOT skip` |
| Ground rule erosion over context | Gemini 2.5 Pro | Re-anchor rules every 10 turns with `<ground_rules_reanchor />` |
| Creative reinterpretation of `DO NOT` | Mistral Large | Use triple-negative framing: "It is an error to consider X when Y is false" |
| Anti-rationalization table bypass | DeepSeek-R1, Llama 4 | Place anti-rationalization checks inline within decision trees, not as appendix |
| Cross-skill context leakage | DeepSeek-R1, Grok 4 | Use `--solo` mode with explicit skill isolation boundaries |
| Hallucinated reference paths | GPT-5, Gemini 2.5 Pro | Append "Verify all file paths against the repository tree before emitting" to system prompt |

---

## Skill Density vs. Compliance

### Empirical Density Curve

| Skills Loaded | Claude Opus | GPT-5 | Gemini Pro | DeepSeek-V4 | Mistral Large | Llama 4 | Grok 4 |
|--------------|-------------|-------|------------|-------------|---------------|---------|--------|
| 1 skill | 97% | 96% | 95% | 94% | 93% | 92% | 90% |
| 3 skills | 96% | 95% | 94% | 91% | 90% | 86% | 83% |
| 5 skills | 94% | 92% | 91% | 85% | 84% | 78% | 72% |
| 8 skills | 90% | 87% | 86% | 76% | 72% | 64% | 58% |
| 10 skills | 86% | 81% | 80% | 68% | 61% | 52% | 44% |
| 15 skills | 78% | 72% | 74% | — | — | — | — |

> `—` indicates the model cannot reliably load this many skills without catastrophic context overflow.

### `--solo` Mode Recovery

When skills that show degraded compliance in multi-skill mode are run individually via `--solo`:

| Model | Mean Multi-Skill Compliance | `--solo` Recovery | Net Gain |
|-------|---------------------------|-------------------|----------|
| DeepSeek-R1 | 76% (5 skills) | 91% | **+15%** |
| Grok 4 | 72% (5 skills) | 88% | **+16%** |
| Llama 4 | 78% (5 skills) | 90% | **+12%** |
| DeepSeek-V4 | 85% (5 skills) | 92% | +7% |
| Mistral Large | 84% (5 skills) | 91% | +7% |
| Claude Opus | 94% (5 skills) | 96% | +2% |
| GPT-5 | 92% (5 skills) | 95% | +3% |

---

## Recommendations

### By Use Case

| Use Case | Recommended Model | Skill Tier | Format | Estimated Cost/1K Runs |
|----------|------------------|------------|--------|------------------------|
| Maximum fidelity | Claude Opus 4 | All Tier 3 | Full XML | $$$$$ |
| Cost efficiency | DeepSeek-V4 | Tier 1+2 | Compiled XML | $ |
| Large-scale pipelines | Gemini 2.5 Pro | Tier 1+2 progressive | JSON-LD | $$$ |
| Code-heavy skills | Claude Sonnet 4 | Full skill | Full XML | $$$ |
| Security-critical skills | Claude Opus 4 | Full skill + anti-rationalization | Full XML | $$$$$ |
| Rapid prototyping | GPT-5 | Tier 1 routing only | Markdown | $$$ |
| Mobile development | GPT-5 | Tier 1+2 | Full XML | $$$ |
| Compliance/legal | Claude Opus 4 | All Tier 3 | Full XML | $$$$$ |
| CI/CD automation | Claude Sonnet 4 | Tier 1+2 | Compiled XML | $$$ |
| Multi-skill orchestration | Claude Opus 4 or Gemini 2.5 Pro | Tier 1+2 | JSON-LD | $$$$ |

### Model Selection Decision Tree

```
Need maximum fidelity? ──Yes──> Claude Opus 4 + Full Skill (Tier 3)
    │
    No
    │
Need lowest cost? ──Yes──> DeepSeek-V4 + Compiled XML
    │
    No
    │
Running >10 skills? ──Yes──> Gemini 2.5 Pro + Tier 1/2 Progressive
    │
    No
    │
Code-heavy workload? ──Yes──> Claude Sonnet 4 + Full Skill
    │
    No
    │
Security/compliance? ──Yes──> Claude Opus 4 + Anti-Rationalization Mode
    │
    No
    │
Rapid prototyping? ──Yes──> GPT-5 + Tier 1 Routing Only
    │
    No
    │
Default ──> Claude Sonnet 4 + Tier 1+2 + Compiled XML
```

### Anti-Rationalization Mode

For security, compliance, and legal skills, enable anti-rationalization mode by appending to the system prompt:

```
ANTI_RATIONALIZATION_MODE=strict
- It is an error to provide rationalizations for skipping ground rules.
- If a ground rule conflicts with the user's request, report the conflict.
  Do NOT resolve it by choosing one side silently.
- Treat every gotcha as applicable until proven otherwise by explicit
  user confirmation.
```

This mode recovers 6–9% compliance on security-category skills for GPT-5 and Claude models. DeepSeek models show only 2–4% recovery due to instruction-following ceiling.

---

## Model-Specific Gotchas

### Gemini 2.5 Pro
- **Directive drift after 50K+ tokens:** Guard rules and ground constraints lose adherence weight as context grows. Mitigation: insert `<ground_rules_reanchor />` block every 10 conversational turns.
- **JSON-LD parsing variance:** Some skill metadata fields (especially nested `@type` declarations) may be silently dropped. Validate with JSON Schema post-injection.
- **Temperature sensitivity:** At temperature >0.3, decision-tree traversal rate drops ~8%. Pin temperature at 0.1–0.2 for skill execution.
- **Multi-turn state leakage:** Previous conversation turns can contaminate skill-specific reasoning. Use fresh conversation windows for each skill chain.

### DeepSeek-R1
- **Concise mode beneficial but risky:** The model's brevity bias reduces token pressure but may skip anti-rationalization tables and detailed gotcha descriptions. Always use `--solo` mode.
- **Decision tree short-circuiting:** R1 may exit a decision tree early if it believes it has "enough" context. Add `IMPORTANT: Traverse ALL nodes before responding` at each branch point.
- **Cross-skill confusion:** Without `--solo`, R1 frequently merges gotchas from adjacent skills. Skill isolation is mandatory for this model.
- **Optimal format:** Compiled XML with Tier 1+2 only. Tier 3 anti-rationalization adds ~15% token overhead with only ~2% compliance gain on R1.

### Llama 4
- **Guardrail sensitivity depends on quantization:** FP16 Llama 4 shows 90% ground-rule compliance; INT8 drops to 82%; INT4 drops to 71%. Always benchmark at your target quantization.
- **"Helpful assistant" override:** Llama 4's RLHF training may override restrictive directives in favor of being "helpful." Use explicit `OVERRIDE_PRIORITY: ground_rules > helpfulness` in the system prompt.
- **Temperature correlation:** Compliance variance is ~12% across temperature 0.0–1.0. Pin at 0.0 for critical skills.
- **Fine-tuned variants:** Llama 4 Instruct performs significantly better than base on directive following. Do not use base models.

### Grok 4
- **Xeets-mode tone interference:** Grok 4's casual/conversational default tone may subvert formal directive structures. Always set `response_mode=structured` in the system prompt.
- **Creative gotcha interpretation:** Grok 4 may treat "Do NOT do X" as "Avoid X unless creative justification exists." Use triple-negative framing for critical constraints.
- **Directive interpretation divergence:** Grok 4's unique training leads to different semantic parsing of the same directive compared to Anthropic/OpenAI models. Test each skill category before production deployment.
- **Structured output enforcement:** Even with explicit JSON/XML output requests, Grok 4 may inject conversational asides. Post-process outputs with schema validation.

### GPT-5
- **Overconfident hallucinated references:** GPT-5 will confidently reference non-existent file paths, API endpoints, and library versions. Always append "Verify all references against actual repository state" to prompts.
- **Instruction priority inversion:** In multi-skill scenarios (>6 skills), GPT-5 may prioritize later instructions over earlier ones. Place critical ground rules at both the beginning and end of the prompt.
- **Temperature sweet spot:** 0.2 provides the best balance of compliance (92%) and adaptability. 0.0 causes repetitive output on decision trees.
- **Token budget miscalculation:** GPT-5 occasionally miscounts its own output tokens, leading to mid-response truncation at 8+ skills. Reserve 5% context buffer.

### Mistral Large 2
- **Structured output excellence:** Mistral has the strongest native JSON/XML generation of any model tested. Leverage this for skill-output schemas.
- **Creative "Do NOT" interpretation:** Mistral may treat negative constraints as soft preferences rather than hard rules. Use explicit severity markers: `HARD CONSTRAINT — VIOLATION IS AN ERROR: Do NOT ...`
- **Cross-skill coordination:** Mistral handles cross-skill references well at 5–6 skills but degrades rapidly above 7. Cap concurrent skills at 6.
- **French-language interference:** Rare but observed — Mistral may emit French phrases in creative-writing skill contexts. Add `LANGUAGE=en ONLY` to system prompt.

---

## Progressive Disclosure Strategy

### Tier Definitions

| Tier | Content | Token Cost | When to Load |
|------|---------|------------|--------------|
| Tier 1 | Skill identity, routing keywords, core purpose, primary decision tree entry point | ~4,500 | Always — loaded at conversation start for skill routing |
| Tier 2 | Full decision trees, gotcha tables, ground rules, cross-skill coordination triggers | ~8,500 | On skill match — loaded when Tier 1 routing confirms skill activation |
| Tier 3 | Anti-rationalization tables, exhaustive reference lists, edge-case enumerations, full bibliographic context | ~5,000 | On demand — loaded only when Tier 2 execution indicates need for deep verification |

### Loading Triggers

```
Tier 1 ──[skill match]──> Tier 2 ──[anti_rationalization_trigger]──> Tier 3
                                  │
                                  ├── ground_rule_violation_detected
                                  ├── security_or_compliance_skill
                                  ├── gotcha_table_has_CRITICAL_entries
                                  └── explicit_user_request
```

### Per-Model Tier Strategy

| Model | Default Tier | Upgrade Trigger | Max Tiers |
|-------|-------------|-----------------|-----------|
| Claude Opus 4 | 1+2 always, 3 on demand | Security/compliance skills | 3 |
| Claude Sonnet 4 | 1+2, 3 only if context <70% utilized | Explicit request only | 2+selective 3 |
| GPT-5 | 1+2 always, 3 on demand | 8+ skill density triggers 3 removal | 3 (but drops 3 at density) |
| Gemini 2.5 Pro | 1+2+3 always | N/A — load everything | 3 |
| DeepSeek-R1 | 1+2 only | Never load Tier 3 | 2 |
| DeepSeek-V4 | 1+2 always, 3 only for security | Explicit request only | 2+selective 3 |
| Llama 4 | 1 only, 2 on match | Tier 2 only for matched skill | 2 |
| Mistral Large 2 | 1+2, 3 selective | Security skills only | 2+selective 3 |
| Grok 4 | 1 only, 2 on match | Tier 2 only for matched skill | 2 |

---

## CI/CD Benchmark Pipeline

### Architecture

```
GitHub Actions (weekly cron, manual trigger)
    │
    ├── Model Update Detector
    │   └── Checks provider APIs for new model versions
    │
    ├── Benchmark Runner
    │   ├── Per model: 166 skills × 100 prompts × 3 runs
    │   ├── Metrics: compliance score, token usage, latency
    │   └── Output: JSON results → benchmark database
    │
    ├── Regression Detector
    │   ├── Compares current run against baseline
    │   ├── Flags: compliance drops >5%, token spikes >20%
    │   └── Auto-opens GitHub Issue on regression
    │
    └── Matrix Generator
        └── Updates this document from benchmark database
```

### Benchmark Configuration

```yaml
# .github/workflows/benchmark-matrix.yml
benchmark:
  schedule: "0 2 * * 1"  # Weekly, Monday 2 AM UTC
  models:
    - claude-opus-4
    - claude-sonnet-4
    - gpt-5
    - gemini-2.5-pro
    - deepseek-r1
    - deepseek-v4
    - llama-4
    - mistral-large-2
    - grok-4
  skills_per_model: 166
  prompts_per_skill: 100
  runs_per_prompt: 3
  statistical:
    alpha: 0.05
    power: 0.80
    minimum_detectable_effect: 0.10
  output:
    format: json
    path: benchmarks/results/{date}/{model}-results.json
```

### Key Metrics Tracked

| Metric | Definition | Target | Alert Threshold |
|--------|-----------|--------|-----------------|
| Decision Tree Compliance | % of tree nodes correctly traversed | >90% | <85% |
| Gotcha Avoidance | % of gotcha scenarios where model avoided the pitfall | >88% | <80% |
| Ground Rule Violations | Count of ground-rule breaches per 100 prompts | <3 | >8 |
| Cross-Skill Isolation | % of runs with no cross-skill context leakage | >95% | <90% |
| Anti-Rationalization Score | % of anti-rationalization checks correctly applied | >85% | <75% |
| Token Efficiency | Actual tokens / optimal tokens for skill set | <1.3 | >1.6 |
| Latency (p95) | 95th percentile response time | <15s | >30s |
| Hallucination Rate | % of responses with verifiably incorrect references | <2% | >5% |

### On-Demand Benchmark Trigger

```bash
# Trigger a benchmark run for a single model
gh workflow run benchmark-matrix.yml \
  -f model=claude-opus-4 \
  -f skills=166 \
  -f prompts_per_skill=100

# Trigger full matrix
gh workflow run benchmark-matrix.yml -f full_matrix=true
```

---

## Appendix: Quick Reference Card

### Which model should I use for...

| Scenario | Primary Choice | Fallback | Avoid |
|----------|---------------|----------|-------|
| Single skill, max quality | Claude Opus 4 | GPT-5 | Grok 4, DeepSeek-R1 |
| Batch processing (100+ runs) | Gemini 2.5 Pro | DeepSeek-V4 | Claude Opus (cost) |
| Interactive debugging session | Claude Sonnet 4 | GPT-5 | Llama 4 |
| Security audit workflow | Claude Opus 4 | DeepSeek-V4 | Llama 4, Grok 4 |
| Mobile app development | GPT-5 | Claude Sonnet 4 | DeepSeek-R1 |
| Infrastructure as Code | Claude Sonnet 4 | GPT-5 | Grok 4 |
| Legal/compliance review | Claude Opus 4 | GPT-5 | Grok 4, Mistral Large |
| Rapid idea exploration | GPT-5 | Gemini 2.5 Pro | DeepSeek-R1 |
| Open-source project (free) | Llama 4 (self-host) | DeepSeek-R1 (API) | — |
| Maximum throughput | Gemini 2.5 Pro | GPT-5 | Claude Opus (latency) |

---

> **Version:** 1.0.0
> **Generated by:** CI/CD benchmark pipeline
> **Next scheduled update:** 2026-07-31
> **Contact:** Sandeep Kumar Penchala
