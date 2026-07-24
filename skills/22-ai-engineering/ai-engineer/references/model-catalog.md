# Foundation Model Catalog — Pricing, Context Windows, Use Cases

Last updated: July 2026. Verify pricing at provider websites.

## GPT Series (OpenAI)

| Model | Context | Input $/1M tokens | Output $/1M tokens | Best For |
|-------|---------|-------------------|--------------------|----------|
| GPT-4o | 128K | $2.50 | $10.00 | Complex reasoning, agents |
| GPT-4o-mini | 128K | $0.15 | $0.60 | High-volume, cost-sensitive |
| o1 | 200K | $15.00 | $60.00 | Math, coding, deep reasoning |
| o3-mini | 200K | $1.10 | $4.40 | Budget reasoning tasks |
| text-embedding-3-small | 8K | $0.02 | — | Embeddings (1536d) |
| text-embedding-3-large | 8K | $0.13 | — | Embeddings (3072d) |

## Claude Series (Anthropic)

| Model | Context | Input $/1M tokens | Output $/1M tokens | Best For |
|-------|---------|-------------------|--------------------|----------|
| Claude 3.5 Sonnet | 200K | $3.00 | $15.00 | Coding, agents, complex tasks |
| Claude 3 Haiku | 200K | $0.25 | $1.25 | Fast, cheap, high-volume |
| Claude Opus 4 | 200K | $15.00 | $75.00 | Hardest reasoning tasks |

## Gemini Series (Google)

| Model | Context | Input $/1M tokens | Output $/1M tokens | Best For |
|-------|---------|-------------------|--------------------|----------|
| Gemini 2.5 Flash | 1M | $0.15 | $0.60 | Long context, cheap |
| Gemini 2.5 Pro | 1M | $1.25 | $10.00 | Complex reasoning, 1M context |

## Open-Source (Self-Hosted)

| Model | Params | Context | GPU Required | Best For |
|-------|--------|---------|-------------|----------|
| Llama 3.1 | 8B | 128K | 1x A10G (24GB) | Classification, extraction |
| Llama 3.1 | 70B | 128K | 4x A100 (320GB) | Complex reasoning |
| Qwen 2.5 | 7B | 128K | 1x A10G | Multilingual, coding |
| Qwen 2.5 | 72B | 128K | 4x A100 | Complex tasks, air-gapped |
| Mixtral 8x22B | 141B (39B active) | 64K | 2x A100 | MoE efficiency |
| DeepSeek V3 | 671B (37B active) | 128K | 8x H100 | MoE, coding, math |

## Embedding Models

| Model | Dim | Max Tokens | Cost/1M tokens | Self-Hosted | MTEB Score |
|-------|-----|-----------|----------------|-------------|------------|
| text-embedding-3-small | 1536 | 8191 | $0.02 | No | 62.3 |
| text-embedding-3-large | 3072 | 8191 | $0.13 | No | 64.6 |
| voyage-2 | 1024 | 32000 | $0.10 | No | 63.8 |
| Cohere embed-v3 | 1024 | 512 | $0.10 | No | 64.2 |
| bge-large-en-v1.5 | 1024 | 512 | Free | Yes | 63.3 |
| gte-large | 1024 | 512 | Free | Yes | 63.1 |
| E5-mistral-7b | 4096 | 32768 | Free | Yes | 66.6 |

## Model Selection Heuristic

```
Need cheap + fast? → GPT-4o-mini or Gemini Flash
Need reasoning quality? → Claude 3.5 Sonnet or GPT-4o
Need on-premise/air-gapped? → Llama 3.1 70B or Qwen 2.5 72B
Need 1M context? → Gemini 2.5 Pro
Need embeddings on YOUR data? → Benchmark 3 models; choose by recall@5
Need multi-modal? → GPT-4o or Gemini 2.5 Flash
```
