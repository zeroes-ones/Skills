## Core Workflow

### Phase 1: Audit Threat Model (30 min)

Catalog all attack surfaces for the LLM application:
- **User input vectors:** Direct chat, file uploads, URL inputs, voice transcripts
- **Third-party content vectors:** Retrieved documents (RAG), API responses, web search results
- **Output exposure vectors:** Chat responses, API responses, generated code, generated emails

Map each vector to specific threats:
- Direct chat → jailbreak prompts, toxic content injection
- RAG documents → indirect prompt injection, poisoned data
- API responses → PII leakage, hallucinated authority, code injection

### Phase 2: Select Guardrail Architecture

Use the **Guardrail Layer Selection** decision tree below. Minimum viable deployment:
```
Input Layer → Output Layer
```

Production-ready deployment:
```
Input Layer → Prompt Layer → Runtime Layer → Output Layer
```

### Phase 3: Implement Input Layer

**Prompt Guard deployment pattern:**
```python
from transformers import pipeline

# Load Prompt Guard for jailbreak + injection detection
classifier = pipeline(
    "text-classification",
    model="meta-llama/Prompt-Guard-86M",
    device="cuda:0"
)

def input_guardrail(user_input: str, retrieved_context: list[str] = None) -> dict:
    """Input layer: jailbreak + indirect injection detection."""
    result = {"allow": True, "flags": [], "confidence": {}}

    # Check for direct jailbreak
    jailbreak = classifier(user_input)[0]
    result["confidence"]["jailbreak"] = jailbreak["score"]
    if jailbreak["label"] == "JAILBREAK" and jailbreak["score"] > 0.5:
        result["allow"] = False
        result["flags"].append("jailbreak_attempt")
        return result

    # Check for indirect injection via retrieved context
    if retrieved_context:
        for i, doc in enumerate(retrieved_context):
            injection = classifier(doc)[0]
            if injection["label"] == "INJECTION" and injection["score"] > 0.5:
                result["allow"] = False
                result["flags"].append(f"indirect_injection_doc_{i}")
                return result

    return result
```

### Phase 4: Implement Output Layer

**Guardrails AI + Presidio output validation:**
```python
from guardrails import Guard
from guardrails.hub import ToxicLanguage, DetectPII, ValidJson
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

presidio_analyzer = AnalyzerEngine()
presidio_anonymizer = AnonymizerEngine()

output_guard = Guard().use_many(
    ToxicLanguage(threshold=0.7, validation_method="sentence"),
    DetectPII(pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER", "SSN", "CREDIT_CARD"]),
    ValidJson(on_fail="reask")  # Retry with correction prompt
)

def output_guardrail(llm_response: str) -> dict:
    """Output layer: toxicity, PII, JSON validation."""
    result = {"allow": True, "redacted": None, "flags": [], "detail": {}}

    # Guardrails AI validation
    try:
        validated = output_guard.validate(llm_response)
        if validated.error:
            result["allow"] = False
            result["flags"].append(validated.error)
            result["detail"]["guardrails_error"] = str(validated.error)
            return result
    except Exception as e:
        # Guardrail failure — fail-closed for high-risk
        result["allow"] = False
        result["flags"].append("guardrail_execution_failure")
        return result

    # Presidio PII deep scan (catches what Guardrails AI misses)
    presidio_results = presidio_analyzer.analyze(
        text=llm_response,
        language="en",
        entities=["EMAIL_ADDRESS", "PHONE_NUMBER", "SSN", "CREDIT_CARD",
                   "US_BANK_NUMBER", "IBAN_CODE", "US_DRIVER_LICENSE"]
    )
    if presidio_results:
        result["redacted"] = presidio_anonymizer.anonymize(
            text=llm_response, analyzer_results=presidio_results
        ).text
        result["flags"].append("pii_detected_and_redacted")
        result["detail"]["pii_count"] = len(presidio_results)

    return result
```

### Phase 5: Test Adversarial

Run minimum adversarial test suite before deployment:
- 50 DAN-style jailbreak variants (from JailbreakChat corpus)
- 20 Crescendo multi-turn attack sequences
- 30 indirect injection payloads in synthetic RAG documents
- 15 Base64/ROT13 encoded prompt bypass attempts
- 25 multilingual toxic prompts (zh, ar, hi, ru, es)
- 10 PII-leakage prompts targeting specific entity types

Acceptance criteria: FPR < 0.1%, FNR < 5%, no critical bypasses in Layer 1.

### Phase 6: Deploy with Metrics

Instrument every guardrail layer:
```python
from opentelemetry import metrics

guardrail_fpr = metrics.create_counter("guardrail.false_positive", "FPR per layer")
guardrail_latency = metrics.create_histogram("guardrail.latency_ms", "p50/p99 latency")
guardrail_blocks = metrics.create_counter("guardrail.blocks", "Block decisions by reason")

# After each classification decision:
span.set_attribute("guardrail.layer", "input")
span.set_attribute("guardrail.decision", "block" if not result["allow"] else "allow")
guardrail_latency.record(elapsed_ms, {"layer": "input"})
if not result["allow"]:
    guardrail_blocks.add(1, {"reason": result["flags"][0]})
```
