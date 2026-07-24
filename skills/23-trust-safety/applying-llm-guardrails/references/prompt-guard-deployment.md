# Prompt Guard Deployment Patterns

## Overview

Prompt Guard (Meta, 86M parameters) provides two complementary classifiers:
1. **Jailbreak detection** — identifies attempts to bypass safety guardrails via DAN-style, role-play, encoding-based attacks
2. **Indirect injection detection** — identifies malicious instructions embedded in third-party content (RAG documents, emails, web pages)

## Jailbreak Detection

The mSE (multi-state embedding) model classifies prompts as JAILBREAK or BENIGN:

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = "meta-llama/Prompt-Guard-86M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def detect_jailbreak(prompt: str) -> dict:
    """Detect jailbreak attempts in user input."""
    inputs = tokenizer(
        prompt, return_tensors="pt", truncation=True, max_length=512
    )
    outputs = model(**inputs)
    probabilities = torch.softmax(outputs.logits, dim=-1)
    jailbreak_score = probabilities[0][model.config.label2id["JAILBREAK"]].item()

    return {
        "jailbreak_score": jailbreak_score,
        "action": "block" if jailbreak_score > 0.9 else
                  "challenge" if jailbreak_score > 0.5 else "allow"
    }
```

## Indirect Injection Detection

Detect malicious instructions in third-party content before it enters the LLM prompt:

```python
def detect_indirect_injection(documents: list[str]) -> list[dict]:
    """Scan retrieved documents for hidden prompt injections."""
    results = []
    for i, doc in enumerate(documents):
        inputs = tokenizer(doc, return_tensors="pt", truncation=True, max_length=512)
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)
        injection_score = probs[0][model.config.label2id["INJECTION"]].item()

        results.append({
            "doc_index": i,
            "injection_score": injection_score,
            "flagged": injection_score > 0.5,
            "action": "strip" if injection_score > 0.9 else
                      "flag" if injection_score > 0.5 else "include"
        })
    return results

# Pattern: scan before prompt assembly
docs = retrieve_from_kb(query)
injection_results = detect_indirect_injection(docs)
safe_docs = [d for d, r in zip(docs, injection_results) if not r["flagged"]]

if len(safe_docs) < len(docs):
    log_injection_event(query, injection_results)
    # Optionally: re-retrieve, fallback, or respond that content is unavailable
```

## Threshold Tuning Guidelines

| Threshold | Action | Use Case |
|-----------|--------|----------|
| > 0.9 | Block | High-confidence jailbreak; silently reject |
| 0.5-0.9 | Challenge | Ambiguous; ask user to rephrase |
| < 0.5 | Allow | Benign; proceed to next guardrail layer |

## Production Patterns

- Run jailbreak and injection detection in parallel (independent classifiers, same model)
- Cache benign classifications for repeated prompts (TTL: 5 min)
- Batch document scanning for RAG pipelines (up to 32 docs per batch)
- GPU inference: 5-8ms per classification on A10G; CPU: 20-40ms
