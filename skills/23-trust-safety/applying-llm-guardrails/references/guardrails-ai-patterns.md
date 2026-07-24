# Guardrails AI — Structured Validation Patterns

## Overview

Guardrails AI provides composable validators for structured output validation, PII detection, and toxicity scoring. Validators are applied as a pipeline and can reask (retry with correction prompt) on failure.

## JSON Schema Enforcement

```python
from guardrails import Guard
from guardrails.hub import ValidJson

# Define expected output schema
response_schema = {
    "type": "object",
    "properties": {
        "summary": {"type": "string", "maxLength": 500},
        "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
        "key_points": {
            "type": "array",
            "items": {"type": "string"},
            "maxItems": 5
        },
        "confidence": {"type": "number", "minimum": 0, "maximum": 1}
    },
    "required": ["summary", "sentiment", "key_points", "confidence"]
}

json_guard = Guard().use(
    ValidJson(on_fail="reask")  # Retry with correction prompt
)

# Validator will reask the LLM up to 3 times if output is invalid JSON
result = json_guard.validate(llm_output, metadata={"schema": response_schema})
```

## Toxicity Scoring

```python
from guardrails.hub import ToxicLanguage

toxic_guard = Guard().use(
    ToxicLanguage(
        threshold=0.7,
        validation_method="sentence",  # Check per-sentence, not whole text
        on_fail="fix"                  # Request LLM to regenerate
    )
)

result = toxic_guard.validate(llm_response)
if result.error:
    # ToxicLanguage found a sentence with toxicity > 0.7
    log_toxicity_event(result.error, llm_response)
```

## PII Detection Integration

```python
from guardrails.hub import DetectPII

pii_guard = Guard().use(
    DetectPII(
        pii_entities=[
            "EMAIL_ADDRESS", "PHONE_NUMBER", "SSN",
            "CREDIT_CARD", "US_BANK_NUMBER", "IBAN_CODE",
            "US_DRIVER_LICENSE", "US_PASSPORT"
        ],
        on_fail="fix"
    )
)

result = pii_guard.validate(llm_response)
```

## Composite Validation Pipeline

```python
composite_guard = Guard().use_many(
    ValidJson(on_fail="reask"),
    ToxicLanguage(threshold=0.7, validation_method="sentence", on_fail="fix"),
    DetectPII(
        pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER", "SSN", "CREDIT_CARD"],
        on_fail="fix"
    )
)

# Single validation call runs all validators in sequence
validated = composite_guard.validate(llm_response)

if validated.error:
    # At least one validator failed
    log_validation_failure(validated.error, llm_response)
else:
    # All validators passed — safe to deliver
    deliver_to_user(validated.validated_output)
```

## Performance Notes

- Each validator adds 10-30ms latency
- Composite pipeline: 3 validators = 30-90ms
- Reask retries multiply latency: 3 retries × 30ms = 90ms per validator
- Use `on_fail="noop"` (just log) for non-blocking monitoring mode
- Use `on_fail="fix"` for correction-without-retry pattern
