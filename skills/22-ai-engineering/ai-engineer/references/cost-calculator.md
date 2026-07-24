# AI Cost Calculator

## Cost Formulas

```
cost_per_request = (input_tokens × input_price) + (output_tokens × output_price)

daily_cost = cost_per_request × requests_per_day
monthly_cost = daily_cost × 30
```

## Typical Token Counts

| Content Type | Input Tokens | Output Tokens | Total |
|-------------|-------------|--------------|-------|
| Chat message | 200-500 | 200-800 | 400-1300 |
| RAG query | 500-2000 (context) + 50 (query) | 200-500 | 750-2550 |
| Summarization | 2000-8000 (document) | 200-500 | 2200-8500 |
| Agent step | 500-3000 (context + tool results) | 100-300 | 600-3300 |
| Embedding (per doc) | 500-1000 | N/A | 500-1000 |

## Cost Projection Examples

### Chat Application (GPT-4o-mini)
- 10,000 requests/day
- Average 500 input, 400 output tokens
- Input: 10K × 500 × $0.15/1M = $0.75/day
- Output: 10K × 400 × $0.60/1M = $2.40/day
- **Total: ~$3.15/day, ~$95/month**

### RAG System (GPT-4o)
- 1,000 requests/day
- Average 1500 input (context), 400 output tokens
- Input: 1K × 1500 × $2.50/1M = $3.75/day
- Output: 1K × 400 × $10.00/1M = $4.00/day
- **Total: ~$7.75/day, ~$233/month**

### Agent System (Claude 3.5 Sonnet, 5 steps avg)
- 100 tasks/day, 5 agent steps each = 500 LLM calls
- Average 2000 input, 300 output per step
- Input: 500 × 2000 × $3.00/1M = $3.00/day
- Output: 500 × 300 × $15.00/1M = $2.25/day
- **Total: ~$5.25/day, ~$158/month**

## Cost Optimization Strategies

1. **Model downgrade:** GPT-4o → GPT-4o-mini: 94% cost reduction
2. **Prompt compression:** Trim system prompt from 500 to 100 tokens: saves $0.60/day per 1K requests
3. **Semantic caching:** Cache identical/similar queries. 30% hit rate = 30% cost savings.
4. **Batch processing:** OpenAI batch API: 50% discount, 24h turnaround.
5. **Stream token counting:** Track tokens per request, alert on cost anomalies.
6. **Rate limiting:** Cap requests/user/hour to prevent cost spikes.
