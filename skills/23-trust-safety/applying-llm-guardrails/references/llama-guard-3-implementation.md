# LlamaGuard 3 Implementation Patterns

## Hazard Taxonomy (14 Categories)

LlamaGuard 3 classifies content into 14 hazard categories across 3 risk levels:

**S1 — Violent Crimes (Critical)**
- S1.1: Violence — terrorist content, mass violence, physical harm instructions
- S1.2: Sexual Crimes — CSAM, sexual violence, trafficking
- S1.3: Child Exploitation — grooming, endangerment, CSAM facilitation

**S2 — Non-Violent Crimes (High)**
- S2.4: Illegal Weapons — manufacture, acquisition, use of illegal weapons
- S2.5: Controlled Substances — illegal drug production, distribution, use
- S2.6: Fraud/Deception — scams, financial fraud, identity theft instructions
- S2.7: Cybercrime — hacking, malware creation, DDoS instructions

**S3 — Regulated Content (Medium)**
- S3.8: Hate Speech — protected characteristics, dehumanization, incitement
- S3.9: Self-Harm — suicide, self-injury, eating disorders instruction
- S3.10: Sexual Content — non-criminal adult sexual content
- S3.11: Election Integrity — voter suppression, mis/disinformation campaigns
- S3.12: Privacy Violations — doxxing, unauthorized PII disclosure
- S3.13: Intellectual Property — copyright circumvention, counterfeiting
- S3.14: Unsafe Health — dangerous medical advice, unproven treatments

## Deployment Pattern

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_id = "meta-llama/Llama-Guard-3-8B"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id, torch_dtype=torch.bfloat16, device_map="auto"
)

def classify_safety(conversation: list[dict], custom_policy: str = None) -> dict:
    """Classify safety using LlamaGuard 3 with optional custom policy."""
    policy = custom_policy or DEFAULT_SAFETY_POLICY

    # Format conversation for LlamaGuard
    prompt = f"""<|begin_of_text|><|start_header_id|>user<|end_header_id|>

Task: Check if there is unsafe content in the following conversation according to our safety policy.

<BEGIN UNSAFE CONTENT CATEGORIES>
{policy}
<END UNSAFE CONTENT CATEGORIES>

<BEGIN CONVERSATION>
{format_conversation(conversation)}
<END CONVERSATION>

Provide your safety assessment:
- First line: "safe" or "unsafe"
- If unsafe: list the violated categories and explain<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_new_tokens=256, temperature=0.0)
    response = tokenizer.decode(output[0][inputs.input_ids.shape[1]:])

    lines = response.strip().split('\n')
    is_safe = lines[0].strip().lower() == "safe"
    violations = [l.strip() for l in lines[2:]] if len(lines) > 2 and not is_safe else []

    return {"safe": is_safe, "violations": violations, "raw": response}
```

## Threshold Tuning

- **Default:** binary classification (safe/unsafe) at 0.5
- **High-recall mode:** temperature 0.0, max_new_tokens=64 (faster, stricter)
- **Detailed mode:** temperature 0.1, max_new_tokens=256 (explanations for audit)

## Custom Policy Configuration

Replace DEFAULT_SAFETY_POLICY with domain-specific taxonomy:

```
S1: Medical Misinformation — unproven treatments, anti-vaccine content
S2: Financial Advice — unqualified investment recommendations, pump-and-dump
S3: Legal Advice — unauthorized legal counsel, contract interpretation
```
