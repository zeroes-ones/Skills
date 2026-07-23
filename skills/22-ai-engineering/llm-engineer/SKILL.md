---
name: llm-engineer
description: >
  Use when designing RAG pipelines, engineering prompts at scale, building LLM evaluation
  frameworks, implementing function calling and tool use, or optimizing LLM latency and
  cost. Handles RAG pipeline design (chunking strategies, embedding models, vector
  databases), prompt engineering at scale (templates, versioning, few-shot selection,
  chain-of-thought, system prompt governance), model evaluation frameworks (LLM-as-judge,
  hallucination detection, RAGAS), latency and cost optimization (streaming, token
  budgeting, semantic caching, distillation), function calling and tool use (structured
  output, tool selection), safety guardrails (NeMo, PII detection, toxicity filtering),
  multi-agent architectures, and fine-tuning strategy (LoRA/QLoRA, data preparation).
  Do NOT use for AI safety evaluation, MLOps infrastructure, or traditional ML model
  development.
license: MIT
author: Sandeep Kumar Penchala
type: ai-engineering
status: stable
version: 1.1.0
updated: 2026-07-23
tags:
- llm
- rag
- prompt-engineering
- embeddings
- vector-database
- function-calling
- model-evaluation
- hallucination-detection
token_budget: 5000
chain:
  consumes_from:
  - ai-safety-engineer
  - backend-developer
  - ml-ai-engineer
  - mlops-engineer
  feeds_into:
  - ai-safety-engineer
  - ai-safety-health-reviewer
  - frontend-developer
  - mlops-engineer
  - product-manager
---

# LLM & AI Engineer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end LLM and AI engineering — from prompt design through production deployment of language model applications. Covers RAG pipeline architecture, prompt engineering at scale, model evaluation frameworks, latency and cost optimization, function calling and tool use patterns, safety guardrails, multi-agent orchestration, and fine-tuning strategies for production LLM systems.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to deploy an LLM to production without automated evaluation.** An LLM that works on 10 test prompts may fail catastrophically on the 11th. Every production LLM system MUST have automated eval (LLM-as-judge, RAGAS, or human review) running continuously. | Trigger: deployment config (k8s/docker/CI) references LLM endpoint AND `grep -rn "eval\|evaluate\|RAGAS\|llm.judge\|benchmark" --include="*.py" --include="*.ts"` returns 0 results | STOP. "No evaluation framework detected. I need automated evals before deployment: at minimum LLM-as-judge with multi-metric scoring (faithfulness, relevancy, correctness) and a CI gate that blocks deployment on eval degradation." |
| **R2** | **REFUSE to pass raw LLM output to users without guardrails.** Hallucinated medical advice, fabricated legal citations, and toxic completions are not edge cases — they are inevitable at scale. Every output path MUST have content filtering. | Trigger: generated code delivers LLM response to user AND `grep -rn "guardrail\|content_filter\|output_filter\|moderation\|NeMo\|toxicity"` returns 0 results | STOP. Insert guardrail before user delivery: input filtering (prompt injection, PII) + output filtering (toxicity, hallucination patterns, disallowed content). Guardrails must fail closed. |
| **R3** | **REFUSE to build LLM features without a token budget.** A 100K-token context window is not an invitation to dump everything in. Each token costs compute and latency. Every endpoint MUST have a hard token budget. | Trigger: generated code sends content to LLM AND `grep -rn "token_budget\|max_tokens\|tiktoken\|truncate\|context_window"` returns 0 results in the same file | STOP. Define per-endpoint token budgets: `max_context_tokens: 4000` (chat), `max_context_tokens: 8000` (summarization). Add `tiktoken` counting server-side. Reject oversized requests with clear message: "Document exceeds [N]K token limit — split into chapters." |
| **R4** | **STOP and ASK when choosing between RAG and fine-tuning without domain evaluation.** 80% of LLM use cases are solved with good retrieval. Fine-tune only when retrieval cannot provide the task format, reasoning pattern, or domain-specific style needed. | Trigger: user requests fine-tuning AND `grep -rn "RAG\|retrieval\|vector_store\|embedding"` returns 0 results in the project (no evidence RAG was attempted first) | STOP. Ask: "Have you tried RAG for this use case? Fine-tuning is expensive and fragile — it degrades on data outside the training distribution. If RAG can solve this with good retrieval + prompt engineering, that's a lower-maintenance path. Let's try RAG first, then fine-tune only for gaps RAG can't fill." |
| **R5** | **DETECT and WARN about prompts not versioned in git.** Prompt changes deployed via copy-paste have no rollback path, no changelog, and no audit trail. | Trigger: prompt text found in non-git-tracked files OR in database/config with no version tag OR `grep -rn "SYSTEM_PROMPT\|system_prompt" --include="*.tsx" --include="*.jsx"` returns matches in frontend code | WARN: "Prompts are stored outside git (or in frontend code). This means: no version history, no changelog, no rollback, and App Store review to fix a hallucination. Move all prompts to backend prompt catalog with versioned API. Store in git with semantic versioning. Gate deployment on eval pass." |
| **R6** | **DETECT and WARN about synchronous blocking LLM calls in request handlers.** Calling `openai.chat.completions.create()` synchronously blocks the request thread for 8 seconds — 4 concurrent users exhaust the thread pool. | Trigger: generated code contains `await openai.chat.completions.create(` OR `response = openai.ChatCompletion.create(` inside a route handler without streaming or async worker offload | WARN: "Blocking LLM call in request handler. At 8s per request, 4 concurrent users exhaust the thread pool. Use async streaming (SSE) from backend to frontend. Offload batch requests to queue. Use `AsyncOpenAI` client." |
| **R7** | **DETECT and WARN about hardcoded prompts in frontend code.** Fixing a hallucination bug should not require App Store review and user update. | Trigger: `grep -rn "system_prompt\|SYSTEM_PROMPT\|const.*prompt.*=" --include="*.tsx" --include="*.jsx"` returns matches | WARN: "Prompts hardcoded in frontend. Fixing any hallucination, bias, or safety issue requires a full app deploy. Move prompts to backend prompt catalog. Serve via API with version header. Enable hot-swap of prompt versions without client deploy." |

## The Expert's Mindset

Masters of LLM engineering don't just prompt — they **engineer systems where LLMs are a component, not the solution.** They think in failure modes, evaluation metrics, and cost curves.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Anthropomorphism** — attributing human reasoning to LLM outputs | Replace "the model thinks" with "the model predicts the next token." Always. |
| **Demo-driven development** — building what looks good in a demo, not what works at scale | Every demo must include: failure case, cost estimate at 1M requests, and latency p99 |
| **Benchmark overfitting** — optimizing for a public benchmark that doesn't match real use | Run your own domain-specific eval; a 5% improvement on MMLU means nothing if your users ask legal questions |
| **Latest-model syndrome** — assuming the newest model is the best for every task | Maintain a cost-vs-quality matrix for your actual tasks; the best model is often 2 versions behind |

### What Masters Know That Others Don't
- **The shape of the failure distribution** — LLMs don't fail randomly; they fail systematically on specific input patterns. Find the pattern.
- **That evals are a product decision, not a technical one** — what you measure defines what you ship; involve product in eval design
- **The unit economics of every API call** — know the cost-per-request down to the millicent; a 10% token savings at scale pays for a senior engineer

### When to Break Your Own Rules
- **Ship a simple prompt before building a complex pipeline.** If a single well-crafted prompt solves 80%, ship it today and iterate.
- **Use the most expensive model for evaluation, the cheapest for production.** Asymmetric quality investment is the hallmark of mature LLM systems.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single prompt/task | Craft prompts for defined tasks; run provided evaluation frameworks |
| **L2** | Feature or agent | Design and ship an LLM-powered feature; build eval suites; manage cost/quality trade-offs |
| **L3** | LLM system / platform | Architect multi-model, multi-stage LLM pipelines; define org-wide evaluation standards; mentor |
| **L4** | AI product strategy | Define the role of LLMs in the product portfolio; make build-vs-buy decisions on model providers |
| **L5** | Industry AI | Advance the field through novel architectures, training methods, or evaluation paradigms |

**Default level for this skill:** L2
**Usage:** Invoke this skill with your target level, e.g., "as an L3 LLM engineer, design an evaluation framework for..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.


## When to Use

| Scenario | Use This Skill |
|----------|---------------|
| Building a RAG pipeline with vector embeddings | ✅ |
| Fine-tuning an open-source LLM for domain tasks | ✅ |
| Designing prompt chains with tool use | ✅ |
| Evaluating LLM outputs for quality and safety | ✅ |
| Optimizing inference latency and cost | ✅ |
| Building a general-purpose chatbot from scratch | ❌ Use a managed platform or existing framework |
| Setting up infrastructure for model serving | ❌ Use mlops-engineer |
| Designing the product UX around LLM features | ❌ Use product-manager + ux-researcher |

## Route the Request

<!-- Machine-executable routing: 8 file_contains/file_exists rows A1-A8 + Intent Route fallback -->

| # | Detect Condition | Route To | Intent Route Fallback |
|---|-----------------|----------|----------------------|
| **A1** | `file_contains("*.py", "AsyncOpenAI\|openai\.chat\.completions\|anthropic\.messages\|tiktoken\|Instructor")` | LLM Engineer skill (this) | "I detect LLM API client code — staying in LLM Engineer for prompt/cost/latency optimization." |
| **A2** | `file_contains("*.py", "RAG\|RetrievalQA\|vector_store\|retriever\|embedding\|Chroma\|Pinecone\|Weaviate\|Qdrant")` | LLM Engineer skill (this) | "I detect RAG pipeline code — routing to LLM Engineer for retrieval quality and hallucination mitigation." |
| **A3** | `file_exists("*guardrails*\|*guard_rails*\|NeMoGuardrails\|input_rails\|output_rails")` | LLM Engineer skill (this) | "I detect guardrails configuration — routing to LLM Engineer for safety pipeline and red-teaming." |
| **A4** | `file_contains("*.yml", "model_name\|llm_model\|openai_model\|anthropic_model\|prompt_template")` | LLM Engineer skill (this) | "I detect LLM model configuration — routing to LLM Engineer for prompt versioning and model selection." |
| **A5** | `file_exists("*prompt*.yml\|*prompt*.yaml\|*prompt*.json\|prompts/*.yaml")` | LLM Engineer skill (this) | "I detect prompt catalog files — routing to LLM Engineer for prompt evaluation and versioning." |
| **A6** | `file_contains("*.py", "vLLM\|Triton\|k8s.*deploy\|GPU\|CUDA\|torch\.cuda")` | MLOps Engineer skill | "I detect model serving infrastructure — routing to MLOps Engineer for deployment and scaling." |
| **A7** | `file_contains("*.py", "train\|fine.tune\|LoRA\|QLoRA\|peft\|SFTTrainer\|RLHF\|DPO")` | ML/AI Engineer skill | "I detect model fine-tuning code — routing to ML/AI Engineer for training strategy." |
| **A8** | `file_contains("*.py", "guardrail\|safety\|red.team\|prompt.injection\|jailbreak\|toxicity")` | AI Safety Engineer skill | "I detect AI safety code — routing to AI Safety Engineer for adversarial evaluation." |

<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Design a RAG pipeline → Jump to "Core Workflow > Phase 1"
├── Engineer prompts at scale → Jump to "Core Workflow > Phase 2"
├── Evaluate LLM outputs → Jump to "Core Workflow > Phase 3"
├── Optimize latency/cost → Jump to "Core Workflow > Phase 4"
├── Implement function calling → Jump to "Core Workflow > Phase 5"
├── Add safety guardrails → Jump to "Core Workflow > Phase 6"
├── Design multi-agent system → Jump to "Core Workflow > Phase 7"
├── Fine-tune a model → Jump to "Core Workflow > Phase 8"
├── Need ML infrastructure for this? → Invoke mlops-engineer skill instead
├── Need health/medical AI safety review? → Invoke ai-safety-health-reviewer skill instead
└── Not sure? → Describe the problem in plain language and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Cross-Skill Coordination

<!-- STANDARD: 3min -->

<!-- NEIGHBORS: LLM engineering depends on upstream infrastructure and feeds into downstream safety, product, and UX -->

| Upstream Skill | What You Receive | Decision Gate |
|---|---|---|
| `mlops-engineer` | Model serving infrastructure (vLLM/Triton), GPU optimization, deployment pipelines, monitoring dashboards | Validate latency/cost at target throughput before committing to architecture |
| `ml-ai-engineer` | Model selection guidance, training data, fine-tuning strategies, embedding model benchmarks | Align on model capabilities vs requirements; avoid over-engineering for simple tasks |
| `backend-developer` | API design patterns, service architecture, database schemas, authentication/authorization | Integrate LLM calls into service boundaries; define error handling and retry contracts |
| `ai-safety-engineer` | Safety evaluation criteria, guardrail specs, red-teaming findings, bias audit results | Gate deployment on safety evaluation pass; integrate guardrails into output pipeline |

| Downstream Skill | What You Provide | Artifacts |
|---|---|---|
| `ai-safety-health-reviewer` | LLM pipeline architecture, prompt templates, RAG retrieval patterns, evaluation results | Prompt catalog with safety annotations, RAG retrieval quality reports, hallucination rate dashboards |
| `mlops-engineer` | Model serving requirements (latency SLAs, throughput targets, GPU needs), monitoring metrics | Serving configs, monitoring metric definitions, cost-per-request estimates |
| `product-manager` | Feature feasibility assessments, latency/cost trade-offs, capability demonstrations | Prototype demos, cost-per-feature estimates, latency UX impact analysis |
| `frontend-developer` | Streaming response contracts, function call schemas, error states, loading patterns | API contracts, streaming event types, tool use response schemas, typing indicators |

**Coordination cadence:**
- **Pre-implementation:** Architecture review with `mlops-engineer` on serving feasibility
- **Weekly:** Sync with `backend-developer` on API contract changes and integration issues
- **Per deployment:** Safety gate with `ai-safety-engineer` — no model change skips evaluation
- **Bi-weekly:** Review with `product-manager` on feature readiness and cost projections
- **Monthly:** Cross-functional review with all downstream consumers on pipeline health

## Proactive Triggers

<!-- DEEP: 10+min — when to intervene before someone asks -->

| Trigger | Action | Why |
|---------|--------|-----|
| Frontend team requests a chat feature with sub-2-second response expectation | Propose streaming (SSE) over batch; design token-by-token rendering contract with `frontend-developer`; include `text` and `finish_reason` event types | Users perceive streaming as 2× faster than batch; SSE is simpler than WebSocket for unidirectional LLM output; `frontend-developer` needs event schema to build progressive UI rendering with typing indicators and error recovery on connection drop |
| Mobile team requests offline-capable LLM features | Propose client-side model fallback (llama.cpp, MediaPipe) for latency-critical path; push notification for async cloud completions; sync with `mobile-developer` on model size budget (<500MB) | Mobile networks are unreliable — streaming over cellular drops mid-response; local model handles 80% of queries (classification, extraction) while cloud model handles complex reasoning; push notification bridges async gap when user is backgrounded |
| Product asks "which model should we use?" without latency/cost context | Recommend model selection matrix based on latency budget: <200ms TTFT → smallest capable model, <1s → mid-tier, >2s → best available; include cost-per-1K-tokens comparison; sync with `product-manager` on UX latency tolerance | Model selection without latency budget produces $0.50/request GPT-4 calls where GPT-3.5-Turbo at $0.002/request would suffice; TTFT (time-to-first-token) is the UX metric, not total completion time |
| Codebase hits 100+ hardcoded prompt strings across 15 frontend components | Propose centralized prompt catalog with versioned templates; migrate prompts to backend API; sync with `frontend-developer` on prompt API contract | Hardcoded prompts in frontend require app store deployment to fix a typo; backend prompts allow hotfix in seconds; versioning enables A/B testing and rollback |
| Monthly LLM API bill spikes 3× without traffic increase | Propose semantic caching (GPTCache/Redis) at API gateway; enforce per-request token budgets; implement cost attribution per feature/user; sync with `backend-developer` on API gateway middleware | 40-60% of LLM requests are semantically similar; caching $0.01/request × 1M requests/month = $4K saved; token budget enforcement at gateway prevents unbounded context growth |
| User reports LLM generating harmful or off-policy content | Propose layered guardrail architecture: input rails (prompt injection, PII) → content rails (domain policy) → output rails (hallucination, harm); sync with `ai-safety-engineer` on guardrail specs and `observability-engineer` on violation logging | A single guardrail fails open; layered defense catches what upstream misses; output rails are the last line — they must detect what input+content rails let through; log which layer catches each violation |
| Observability team reports no LLM-specific metrics in dashboards | Propose LLM observability stack: tokens/sec, TTFT p50/p95/p99, cost-per-request, hallucination rate, cache hit rate, completion tokens per request; sync with `observability-engineer` on metric pipeline | Generic API latency metrics hide LLM-specific issues: a 500ms API call could be 450ms TTFT (users waiting) or 50ms TTFT + 450ms generation (users reading); hallucination rate tracked per model version enables rollback decisions |
| Backend team reports 429 rate limit errors from LLM provider | Propose token bucket rate limiter with exponential backoff + jitter; implement request queuing with priority tiers (interactive > batch); sync with `backend-developer` on retry contract | LLM APIs have hard RPM/TPM limits; naive retry amplifies the problem; priority queuing ensures user-facing requests don't starve behind batch jobs; exponential backoff with jitter avoids thundering herd on retry |

## Core Workflow

<!-- STANDARD: 3min -->

### Phase 1 (~30 min): RAG Pipeline Design

#### Chunking Strategies

1. **Fixed-size chunking** — simplest approach; split documents into N-character chunks with overlap:
   - Typical sizes: 256–1024 tokens for dense retrieval, 512–2048 for generative models
   - Overlap: 10–20% of chunk size prevents context fragmentation at boundaries
   - **When to use**: homogeneous documents (documentation, articles, manuals) where semantic boundaries are less critical
   - **Pitfall**: splits sentences mid-thought, breaking semantic coherence

2. **Semantic chunking** — split at natural boundaries using sentence embeddings:
   - Compute cosine similarity between consecutive sentences; split when similarity drops below threshold
   - Threshold range: 0.5–0.8 depending on domain cohesion
   - **When to use**: heterogeneous documents, narrative content, or when context integrity matters
   - **Tools**: LangChain `SemanticChunker`, LlamaIndex `SentenceSplitter`

3. **Recursive chunking** — apply separators hierarchically (`\n\n` → `\n` → `. ` → ` `):
   - Produces chunks that respect document structure (paragraphs, sentences) before falling back to character splits
   - **When to use**: general-purpose RAG; works well across document types
   - **Recommendation**: start here unless domain-specific needs dictate otherwise

4. **Agentic chunking** — let an LLM decide chunk boundaries based on semantic completeness:
   - LLM reads document and outputs chunk start/end markers
   - Highest quality but slowest and most expensive
   - **When to use**: high-stakes applications where chunk quality directly impacts user safety (medical, legal)

#### Embedding Model Selection

| Model | Dimensions | Max Tokens | Best For | Cost |
|-------|-----------|------------|----------|------|
| text-embedding-3-small | 512/1536 | 8191 | General RAG, cost-sensitive | $0.02/1M tokens |
| text-embedding-3-large | 256/1024/3072 | 8191 | High-accuracy retrieval | $0.13/1M tokens |
| Cohere Embed v3 | 1024 | 512 | Multilingual, classification | $0.10/1M tokens |
| Voyage AI voyage-2 | 1024 | 32000 | Long documents, code | $0.10/1M tokens |
| BGE-large-en (open-source) | 1024 | 512 | Self-hosted, privacy-critical | Free (compute only) |

**Selection criteria:**
- **MTEB leaderboard ranking** for retrieval task on your domain language
- **Max token limit** must exceed your chunk size (embedding models truncate silently)
- **Matryoshka representation** (OpenAI, Voyage) allows dimension reduction without re-embedding — useful for cost-performance tradeoffs
- **Always benchmark on your actual data** — MTEB rankings don't predict domain-specific performance

#### Vector Database Selection

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.

## Cross-Skill Integration

<!-- STANDARD: 3min -->

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | ml-ai-engineer | ML problem framing, baseline models, training infrastructure |
| **Before** | api-designer | API contracts for LLM service endpoints, rate limiting design |
| **Before** | database-designer | Vector database schema, indexing strategy, hybrid search design |
| **This** | llm-engineer | RAG pipeline, prompts with versioning, evaluation framework, guardrails |
| **After** | ai-safety-health-reviewer | Safety review of LLM outputs, medical claim verification, bias audit |
| **After** | mlops-engineer | Production deployment, monitoring, drift detection, retraining pipelines |
| **After** | frontend-developer | LLM-powered UI components, streaming integration, user feedback collection |

Common chains:
- **Chain**: ml-ai-engineer → llm-engineer → ai-safety-health-reviewer — ML baseline feeds into LLM pipeline design; safety reviewer validates outputs before user exposure
- **Chain**: api-designer → llm-engineer → mlops-engineer — API contracts define LLM service boundaries; MLOps deploys and monitors the service
- **Chain**: database-designer → llm-engineer → frontend-developer — Vector DB schema designed for retrieval patterns; frontend integrates streaming responses

## Decision Trees

<!-- QUICK: 60s -- flowchart-style logic for fork-in-the-road decisions -->

### RAG vs Fine-Tuning vs Prompt Engineering
<!-- Decision tree for choosing the right LLM adaptation strategy based on task requirements -->

```
START: You need to adapt an LLM for a specific task or domain
  │
  ├─ Is the task knowledge-intensive with facts that change over time (docs, policies, product catalog)?
  │    ├─ YES → RAG. Retrieval keeps knowledge fresh without retraining.
  │    └─ NO → Continue
  │
  ├─ Does the task require the model to learn a new style, tone, format, or behavior that cannot be described in a prompt?
  │    ├─ YES → FINE-TUNING. Prompts can't teach consistent JSON structure across 100K calls.
  │    └─ NO → Continue
  │
  ├─ Is latency budget <200ms end-to-end and the task is narrow (classification, extraction, routing)?
  │    ├─ YES → FINE-TUNING. Smaller fine-tuned model beats large model + complex prompt.
  │    └─ NO → Continue
  │
  ├─ Are you in exploration/prototype phase with <100 examples and uncertain requirements?
  │    ├─ YES → PROMPT ENGINEERING. Iterate fast. Graduate to RAG or fine-tuning when stable.
  │    └─ NO → Continue
  │
  ├─ Does the task require citing specific sources with verifiable provenance for each claim?
  │    ├─ YES → RAG. Fine-tuned models can't prove where knowledge came from.
  │    └─ NO → Continue
  │
  ├─ Is cost per token the dominant constraint and you can accept ~90% quality of largest model?
  │    ├─ YES → FINE-TUNING. Fine-tune a smaller model to match larger model performance on your domain.
  │    └─ NO → Continue
  │
  └─ Does the task require combining real-time data with domain expertise (e.g., "analyze today's market data using our proprietary framework")?
       ├─ YES → RAG + PROMPT ENGINEERING (hybrid). Retrieve fresh data, apply expertise via prompt.
       └─ NO → RAG for knowledge, FINE-TUNE for behavior. Most production systems use both.
```

### When to Use Embeddings vs Keyword Search vs Hybrid
<!-- Decision tree for retrieval strategy selection in RAG pipelines -->

```
START: Designing retrieval for a RAG pipeline
  │
  ├─ Are queries short (<5 words), keyword-dense, and looking for exact matches (product codes, error messages, legal citations)?
  │    ├─ YES → KEYWORD SEARCH (BM25). Embeddings perform poorly on exact-match tasks.
  │    └─ NO → Continue
  │
  ├─ Are queries natural-language, long-form, or conceptual ("how do I handle a patient who presents with...")?
  │    ├─ YES → EMBEDDINGS (semantic search). These queries need meaning matching, not word matching.
  │    └─ NO → Continue
  │
  ├─ Does your corpus contain both structured fields (title, date, author) and unstructured text?
  │    ├─ YES → HYBRID. Filter on structured fields (keyword), rank by semantic similarity (embeddings).
  │    └─ NO → Continue
  │
  ├─ Is recall@10 below 85% with embeddings alone on your evaluation set?
  │    ├─ YES → HYBRID (BM25 + embeddings with reciprocal rank fusion). Embeddings alone are failing.
  │    └─ NO → Continue
  │
  ├─ Do you need to answer questions like "what was the revenue in Q3 2024?" where the answer requires aggregation across multiple documents?
  │    ├─ YES → EMBEDDINGS + structured data retrieval (Text-to-SQL + semantic search). RAG alone can't aggregate.
  │    └─ NO → Continue
  │
  └─ Is retrieval latency budget <50ms and corpus >10M documents?
       ├─ YES → KEYWORD SEARCH with semantic re-ranking (two-stage). Embeddings on 10M docs is too slow without approximate nearest neighbor (ANN), and ANN quality degrades at scale.
       └─ NO → HYBRID as default. Pure keyword fails on natural language. Pure embeddings fail on exact match. Hybrid covers both.
```

## What Good Looks Like

<!-- QUICK: 30s -- aspirational north star for this skill -->

> LLM engineering is not about making a model generate text — it's about building systems where the text is accurate, safe, fast, and cost-effective at scale. **What good looks like**: every prompt is versioned, tested, and monitored like production code; retrieval quality is measured and maintained, not assumed; guardrails fail closed, never open; token costs are tracked per feature and optimized continuously; evaluation is automated, correlated with human judgment, and run on every change; and when an LLM output is wrong, the system detects it before the user does. A pipeline that "usually works" but can't prove it, can't measure degradation, and can't prevent jailbreaks is a prototype, not a production system — no matter how impressive the demos look.

## Deliberate Practice

```mermaid
graph LR
    A[Build LLM<br/>pipeline] --> B[Evaluate<br/>rigorously] --> C[Find<br/>failure patterns] --> D[Re-architect<br/>for robustness] --> A
```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Take an existing prompt and systematically test it against 50 edge cases; document every failure mode | Weekly |
| **Competent** | Build the same RAG pipeline with 3 different frameworks (LangChain, LlamaIndex, raw); compare the trade-offs | Monthly |
| **Expert** | Design an evaluation framework for a novel LLM use case; correlate automated metrics with human judgment for 3 months | Quarterly |
| **Master** | Publish a case study of an LLM system failure in production: root cause, detection gap, and the architectural change that prevents recurrence | Semi-annually |

**The One Highest-Leverage Activity:** Maintain a "failure log" for every LLM system you operate. For each unexpected output: the input, the output, why it was wrong, and what guardrail would have caught it. Review before every architecture change.

## References

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)

