# Output Control — Per-Task Caps and Structured Output

## Why Output First

Output tokens are priced 3-5x input on most providers. Capping output is often the fastest savings lever — and the most ignored one. The optimizer's job includes the response side (Phase 6).

## Default Caps by Task Type

| Task type | max_tokens | Rationale |
|-----------|-----------:|-----------|
| Classification / labeling | 64 | A label needs <= 20 tokens |
| Extraction (structured) | 500-1,000 | JSON schema output |
| Chat / support | 1,000 | Concise answer + follow-up |
| Code generation | 4,000 | Function-sized units; stream + early-stop |
| Code review comments | 1,500 | Bullet findings, not essays |
| Summarization | 500-1,000 | A summary longer than the source is a bug |
| Open-ended creative | Generous + quality gate | Never truncate mid-thought; A/B a tighter variant |

## Structured Output Over Free Text

- OpenAI: `response_format={"type": "json_schema", ...}` or tool calls.
- Anthropic: tool use with an input schema.
- Gemini: `response_mime_type="application/json"` + `response_schema`.

A constrained 200-token JSON payload beats a 1,200-token prose paragraph with the same information — 6x fewer output tokens, plus it is parseable.

## Truncation Monitoring

1. Log `finish_reason` per call (`stop` vs `length`).
2. `length` share < 1% over 100 sampled calls per task type = healthy.
3. If `length` rises: raise the cap for that task type (do not raise globally), or split the task, or tighten the prompt.

Malformed JSON on truncation is the classic symptom: `finish_reason: length` cuts the payload mid-JSON. Detect it, retry with a split task, and fix the cap — don't paper over it with a JSON-repair layer.

## The Unbounded-Output Tax

Without `max_tokens`, models pad: boilerplate closings, restated caveats, summaries-of-themselves. Measured cases: chat endpoints 40-60% over their natural answer length; output share reaching 30-40% of total spend.
