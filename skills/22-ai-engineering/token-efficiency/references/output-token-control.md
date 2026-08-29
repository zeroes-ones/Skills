# Output Token Control — Caps, Structure, and Truncation Monitoring

> Output tokens are the most expensive token class (3-5× the input rate on most providers). Controlling output is often the fastest lever — and the most ignored one.

## Default Output Caps by Task Type

| Task type | max_tokens | Rationale |
|-----------|-----------:|-----------|
| Classification / labeling | 64 | A label needs ≤ 20 tokens; 64 leaves room for a short justification |
| Extraction (structured) | 500-1,000 | JSON schema output; cap by schema size |
| Chat / support | 1,000 | Concise answer + follow-up handling |
| Code generation | 4,000 | Function-sized units; stream + early-stop on closing delimiter |
| Code review comments | 1,500 | Bullet-point findings, not essays |
| Summarization | 500-1,000 | A summary longer than the source is a bug |
| Open-ended creative | Generous + quality gate | Never truncate mid-thought; A/B a tighter variant instead |

## Structured Output Over Free Text

For extraction, classification, and any machine-consumed output, prefer **constrained generation**:

- OpenAI: `response_format={"type": "json_schema", ...}` or tool/function calling.
- Anthropic: tool use with an input schema.
- Gemini: `response_mime_type="application/json"` + `response_schema`.

A constrained 200-token JSON payload beats a 1,200-token prose paragraph with the same information — 6× fewer output tokens, plus it is parseable (no fragile text parsing).

## Truncation Monitoring

Cap → verify no truncation:

1. Log `finish_reason` per call (`stop` vs `length`).
2. `length` share < 1% over 100 sampled calls per task type = healthy.
3. If `length` rises: raise the cap for that task type (do not globally raise), or split the task, or tighten the prompt to shorten output.

Malformed-JSON-on-truncation is the classic symptom: `finish_reason: length` cuts the payload mid-JSON. Detect it, retry with a split task, and fix the cap — don't paper over it with a JSON-repair layer.

## The Unbounded-Output Tax

Without `max_tokens`, models pad: boilerplate closings, restated caveats, summaries-of-themselves, repeated disclaimers. Measured cases: chat endpoints 40-60% over their natural answer length; "short answer" tasks producing 1,500-3,000 tokens. At output prices 3-5× input, this routinely becomes 30-40% of total spend.

## Stream + Early-Stop

For long generations (code, documents), enable streaming and stop on the first complete output signal (closing delimiter, final code block fence). This bounds perceived latency and lets you abort early instead of paying for a full-length completion.
