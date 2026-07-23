# Core Workflow — Full Implementation

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

| Database | Best For | Scaling Model | Key Feature |
|----------|----------|---------------|-------------|
| Pinecone | Managed, zero-ops | Serverless pods | Fastest time-to-production |
| Weaviate | Hybrid search (vector + keyword) | Horizontal sharding | Native multi-tenancy, GraphQL |
| Qdrant | High-performance filtering | Raft consensus | Best payload filtering perf |
| pgvector | PostgreSQL shops | PostgreSQL scaling | No new infrastructure |
| Milvus | Billion-scale collections | Distributed (proxy + workers) | GPU-accelerated index build |
| Chroma | Prototyping, embedded | Single-process | Zero-config, in-memory |

**Index selection:**
- **HNSW**: best recall-speed tradeoff for <10M vectors; tune `ef_construction` (build time) and `ef_search` (query time)
- **IVF**: disk-friendly for >10M vectors; needs training step
- **DiskANN (Qdrant)**: when vectors don't fit in RAM

### Phase 2 (~30 min): Prompt Engineering at Scale

#### Prompt Templates with Versioning

1. **Template structure** — every prompt template must have:
   - `system_prompt`: role, constraints, output format, domain context
   - `user_prompt_template`: with `{variable}` placeholders
   - `few_shot_examples`: curated examples stored separately from template logic
   - `version`: semantic versioning (`1.2.0`) with changelog entries

2. **Versioning workflow:**
   ```
   templates/
   ├── summarization/
   │   ├── v1.0.0.yaml        # baseline
   │   ├── v1.1.0.yaml        # improved few-shot examples
   │   └── v1.2.0.yaml        # updated system prompt
   └── evaluation_results/
       ├── summarization_v1.0.0.json
       └── summarization_v1.1.0.json
   ```

3. **A/B test prompts like code** — deploy two template versions, route 10% traffic to variant, measure task-completion rate and user satisfaction before full rollout

#### Few-Shot Selection Strategies

1. **Static few-shot** — same examples for every request; simple but context-blind
2. **Semantic retrieval-based** — embed user query, retrieve K most similar examples from curated bank; best general-purpose approach
3. **Dynamic few-shot** — select examples based on difficulty (simple query → 0-shot, complex → 3-shot); reduces token waste
4. **Contrastive examples** — include both positive examples (what to do) and negative examples (what to avoid); especially effective for output format enforcement

#### Chain-of-Thought vs Tree-of-Thought

- **Chain-of-Thought (CoT)** — model explains reasoning step-by-step before final answer:
  - Best for: math, logic, multi-step reasoning, structured analysis
  - Prompt: "Let's think step by step." or "First, analyze... Then, evaluate... Finally, conclude..."
  - Zero-shot CoT works surprisingly well in modern models

- **Tree-of-Thought (ToT)** — model explores multiple reasoning branches, evaluates each, selects best:
  - Best for: planning, creative problem-solving, tasks with multiple valid approaches
  - Implementation: BFS/DFS over reasoning steps with LLM as heuristic evaluator
  - **Cost**: 5–10× more tokens than CoT; use only when CoT fails

#### System Prompt Governance

- All system prompts in version control (not hardcoded, not in environment variables)
- Approval process for system prompt changes affecting >10K daily users
- System prompt must include: role definition, output format specification, safety boundaries, and explicit DON'Ts
- Monitor system prompt effectiveness: track instruction-following rate, refusal rate, and format compliance over time

### Phase 3 (~30 min): Model Evaluation Frameworks

#### LLM-as-Judge

1. **Pairwise comparison**: present two outputs to judge LLM, ask "Which is better?" — most reliable format
2. **Reference-based scoring**: judge compares output against reference answer on multiple dimensions (accuracy, completeness, conciseness)
3. **Rubric-based scoring**: judge evaluates output against predefined rubric with 1–5 Likert scale per criterion

**Critical validation rules:**
- Judge model must be stronger than the model being evaluated (GPT-4 judges GPT-3.5; Claude Opus judges Claude Sonnet)
- Validate LLM-as-judge against human ratings — correlation must be >0.7 before trusting automated judgments
- Position bias: randomize output order in pairwise comparisons
- Verbosity bias: longer outputs score higher; control with explicit conciseness criterion

#### Why BLEU/ROUGE Are Inadequate for LLMs

- **BLEU** measures n-gram overlap with reference — penalizes valid paraphrases, rewards formulaic text
- **ROUGE** measures recall of reference n-grams — same limitations, slightly better for summarization
- Both were designed for machine translation (BLEU) and summarization (ROUGE) of pre-LLM systems
- **Modern alternatives**: BERTScore (semantic similarity), BLEURT (learned metric), G-Eval (LLM-based with chain-of-thought)

#### Hallucination Detection

1. **SelfCheckGPT**: sample multiple outputs from same prompt; if outputs are inconsistent, hallucination likely
2. **NLI-based (Natural Language Inference)**: decompose output into atomic claims, check each against retrieved context using NLI model (entailment/contradiction/neutral)
3. **Retrieval-augmented verification**: for RAG outputs, verify each factual claim against the retrieved chunks
4. **Uncertainty quantification**: use token-level log probabilities to identify low-confidence spans

#### RAGAS for RAG Quality

RAGAS evaluates RAG pipelines on three dimensions:
- **Faithfulness**: do claims in the answer follow from retrieved context? (% of claims with NLI entailment)
- **Answer Relevance**: does answer address the question? (cosine similarity of question to generated reverse-questions)
- **Context Relevance**: is retrieved context on-topic? (sentence-level relevance scoring)

**RAGAS pipeline:**
```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_relevancy

results = evaluate(
    dataset=eval_dataset,
    metrics=[faithfulness, answer_relevancy, context_relevancy]
)
# Thresholds: faithfulness > 0.85, answer relevancy > 0.80, context relevancy > 0.75
```

### Phase 4 (~30 min): Latency and Cost Optimization

#### Streaming vs Batch

| Pattern | Latency (TTFT) | Use Case | Cost |
|---------|---------------|----------|------|
| Streaming (SSE) | <200ms | Chat, real-time assistants | Per-token, same as batch |
| Batch | 2–30s | Document processing, batch summarization | Batch API discount (50% off) |
| Async streaming | 500ms–2s | "Typewriter" effect for long-form | Same as streaming |

**Key metrics:**
- **TTFT (Time to First Token)**: must be <500ms for conversational UX; <200ms for voice
- **TPOT (Time per Output Token)**: target <50ms/token; >100ms/token feels sluggish
- **End-to-end latency**: TTFT + (output_tokens × TPOT); budget 2–5s total for most use cases

#### Token Budgeting

1. **Prompt compression**: LLMLingua, selective context; compress retrieved documents before sending to LLM
2. **Context window management**: sliding window for long conversations, summarization of earlier turns
3. **Token counting**: use tiktoken (OpenAI) or equivalent to exactly measure tokens before API call
4. **Budget allocation rule**: system prompt <500 tokens, retrieved context <2000 tokens, conversation history <1000 tokens, output <1000 tokens

#### Caching Strategies

1. **Exact-match cache**: store (prompt_hash → response) pairs; simple but low hit rate
2. **Semantic cache (GPTCache)**: embed incoming query, find K nearest cached queries with cosine similarity >0.95, return cached response
   - **GPTCache**: pluggable embedding backend, eviction policies (LRU, FIFO), configurable similarity thresholds
   - **Hit rate expectation**: 30–50% for customer support, 5–15% for creative tasks
3. **Prompt template cache**: cache responses keyed on (template_version, variables_hash) — higher hit rate than raw prompt cache

#### Model Distillation and Quantization

- **Distillation**: train smaller "student" model on outputs of larger "teacher"; preserves 90–95% quality at 10% cost
- **Quantization**: reduce model precision from FP16 to INT8/INT4:
  - **GPTQ**: post-training quantization, good for GPU deployment
  - **GGML/GGUF**: CPU-friendly quantization (Q4_K_M is sweet spot for quality/size)
  - **AWQ**: activation-aware; better perplexity than GPTQ at same bit-width
- **When to use each**: distillation when you have thousands of high-quality teacher outputs; quantization when you need to run model on consumer hardware or reduce GPU cost

### Phase 5 (~25 min): Function Calling and Tool Use

#### OpenAI Function Calling Pattern

```python
tools = [{
    "type": "function",
    "function": {
        "name": "search_patient_records",
        "description": "Search patient records by name, MRN, or date range",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "field": {"type": "string", "enum": ["name", "mrn", "dob"]},
                "limit": {"type": "integer", "default": 10}
            },
            "required": ["query", "field"]
        }
    }
}]
```

#### Tool Selection Strategies

1. **Tool router pattern**: lightweight classifier determines which tool to invoke before calling LLM — reduces latency and token cost
2. **Parallel tool calling**: when multiple independent tools are needed (get_weather + get_events), call them simultaneously
3. **Tool result verification**: validate tool output before feeding back to LLM — catch API errors, empty results, or unexpected formats
4. **Fallback chain**: tool_timeout → retry_with_backoff → fallback_model → graceful_degradation_response

#### Structured Output

| Method | Reliability | Latency | Flexibility |
|--------|------------|---------|-------------|
| JSON mode (OpenAI) | High (constrained tokens) | +10–20% | Limited to JSON Schema |
| Instructor (Python) | Very high (retry + validation) | +5–15% | Full Pydantic model support |
| Outlines (open-source) | Highest (grammar-constrained) | +5% | Regular expression + JSON Schema |
| TypeChat (Microsoft) | High (TypeScript types) | +10–20% | TypeScript schema |

**Best practice**: use Pydantic models with Instructor for Python; validates and retries on parse failure automatically:
```python
from pydantic import BaseModel
import instructor
from openai import OpenAI

class PatientSummary(BaseModel):
    name: str
    age: int
    conditions: list[str]
    medications: list[str]

client = instructor.from_openai(OpenAI())
summary = client.chat.completions.create(
    model="gpt-4",
    response_model=PatientSummary,
    messages=[{"role": "user", "content": "Summarize: Jane Doe, 45, diabetes..."}]
)
```

### Phase 6 (~25 min): Guardrails

#### NeMo Guardrails

- **Colang language**: define conversational flows, safety rails, and topic boundaries
- **Input rails**: block/rewrite toxic, PII-containing, or off-topic user inputs before they reach the LLM
- **Output rails**: block/rewrite hallucinated, toxic, or disallowed LLM outputs before they reach the user
- **Dialog rails**: enforce conversation structure — require greetings, confirmations, handoffs

Example Colang rail:
```
define user express self harm
  "I want to hurt myself"
  "I don't want to live anymore"

define flow
  user express self harm
  bot provide crisis resources
  bot offer to connect with human
```

#### Input/Output Validation

1. **Input validation**: schema check (expected types), content filter (prohibited topics), PII scanner (Presidio, AWS Comprehend), injection detection (prompt injection patterns)
2. **Output validation**: schema compliance (JSON parse check), factual grounding verification, toxicity classifier (Perspective API, OpenAI moderation), length/format constraints
3. **Validation gates**: input_gate → model → output_gate; either gate can block or rewrite

#### PII Detection

- **Microsoft Presidio**: open-source, customizable, detects 50+ entity types (names, SSNs, credit cards, medical terms)
- **AWS Comprehend PII**: managed service, HIPAA-eligible, async batch mode for large documents
- **Regex-based**: fast but brittle; supplement with ML-based detection for production
- **Rule**: never log or store LLM inputs/outputs without PII scanning first

#### Toxicity Filtering

- **Perspective API**: real-time toxicity scoring (toxicity, severe toxicity, identity attack, insult, profanity, threat)
- **OpenAI Moderation API**: free endpoint, scores across 11 categories
- **Threshold strategy**: block at toxicity >0.7, flag for review at 0.3–0.7, allow at <0.3
- **Language coverage**: evaluate toxicity classifier performance in your users' languages — most classifiers degrade significantly on non-English text

### Phase 7 (~25 min): Multi-Agent and Multi-Model Architectures

#### Routing Architecture

1. **LLM router**: classify user intent, route to specialized model/handler:
   - Summarization → smaller, faster model (GPT-3.5, Claude Haiku)
   - Complex reasoning → larger model (GPT-4, Claude Opus)
   - Domain-specific (medical, legal, code) → fine-tuned specialist model
2. **Cost savings**: routing 70% of queries to smaller models reduces cost by 40–60% with <2% quality degradation
3. **Fallback**: if router confidence <0.8, route to larger model

#### Multi-Agent Patterns

1. **Supervisor-worker**: supervisor LLM decomposes task, assigns to specialized agents, synthesizes results
2. **Debate**: two agents argue opposing positions, judge agent evaluates arguments and decides — reduces bias, improves reasoning accuracy
3. **Critique-refine**: generator agent produces output, critic agent reviews and provides feedback, generator revises
4. **Sequential pipeline**: agent_1 preprocesses → agent_2 analyzes → agent_3 formats → agent_4 validates

#### Specialized Models for Sub-Tasks

- **Embedding models** for retrieval (separate from generative model)
- **Classification models** for intent detection, toxicity, sentiment (faster and cheaper than LLM)
- **Reward models** for output ranking and preference optimization
- **Guard models** for input/output safety filtering

### Phase 8 (~25 min): Fine-Tuning Strategy

#### When to Fine-Tune vs RAG

| Criterion | Fine-Tune | RAG |
|-----------|-----------|-----|
| Need new facts/knowledge | ❌ (knowledge cut from training data) | ✅ (retrieve latest docs) |
| Need new task format/style | ✅ (learns pattern from examples) | ❌ (prompt alone may not suffice) |
| Need source attribution | ❌ (model can't cite its training data) | ✅ (return retrieved chunks) |
| Latency budget <100ms | ✅ (no retrieval round-trip) | ❌ (adds embedding search time) |
| Data changes frequently | ❌ (requires retraining) | ✅ (update vector DB) |
| Privacy/offline requirement | ✅ (model runs locally) | ⚠️ (vector DB may require network) |

#### LoRA and QLoRA

- **LoRA (Low-Rank Adaptation)**: freeze base model weights, train small adapter matrices (r=8–64)
  - Trainable params: 0.1–1% of base model; fits in single GPU
  - Merge adapters into base weights for inference (no latency penalty)
- **QLoRA**: LoRA + 4-bit quantization of base model; fine-tune 70B models on single 48GB GPU
- **Training recipe**: LoRA rank 16–32, alpha 2× rank, target all linear layers, learning rate 2e-4, 3–5 epochs

#### Data Preparation for Fine-Tuning

1. **Quality > quantity**: 100 high-quality, diverse examples outperform 1000 noisy, templated ones
2. **Diversity**: cover edge cases, failure modes, and rare scenarios — not just happy path
3. **Format consistency**: every example must follow exact same structure (system/user/assistant for chat models)
4. **Data split**: 80% train, 10% validation (for early stopping), 10% test (for final evaluation)
5. **Decontamination**: check against public benchmarks to avoid train-test leakage

#### Fine-Tuning Providers

| Provider | Models | Pricing | Best For |
|----------|--------|---------|----------|
| OpenAI | GPT-3.5, GPT-4 | Per-token | Easiest, fully managed |
| Anyscale | Llama, Mistral | Per-GPU-hour | Open-source models at scale |
| Together AI | Llama, Mistral, Falcon | Per-token | Fast iteration, many models |
| Self-hosted | Any open-source | GPU cost | Maximum control, privacy |
