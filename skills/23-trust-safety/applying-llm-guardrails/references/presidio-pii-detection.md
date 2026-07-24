# Microsoft Presidio — PII Detection in LLM Contexts

## LLM-Specific PII Challenges

LLMs generate free-form text that may contain PII not explicitly present in training data. Hallucinated PII (fake but realistic SSNs, phone numbers, emails) must also be detected. Presidio uses pattern matching + ML-based recognition to catch both.

## Entity Recognition Configuration

```python
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider

# Custom NLP engine for domain-specific PII
nlp_config = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "en", "model_name": "en_core_web_lg"}]
}
provider = NlpEngineProvider(nlp_configuration=nlp_config)

# Custom recognizer registry with LLM-specific entities
registry = RecognizerRegistry()
registry.load_predefined_recognizers()

# Add custom recognizer for LLM-specific patterns
from presidio_analyzer import PatternRecognizer, Pattern

api_key_pattern = PatternRecognizer(
    supported_entity="API_KEY",
    patterns=[
        Pattern("OpenAI Key", r"sk-[A-Za-z0-9]{32,48}", 0.9),
        Pattern("GitHub Token", r"ghp_[A-Za-z0-9]{36}", 0.9),
        Pattern("Generic API Key", r"[A-Za-z0-9]{32,64}", 0.5),
    ]
)
registry.add_recognizer(api_key_pattern)

analyzer = AnalyzerEngine(registry=registry, nlp_engine=provider.create())
```

## LLM Output Scanning

```python
from presidio_anonymizer import AnonymizerEngine

anonymizer = AnonymizerEngine()

def scan_llm_output(text: str) -> dict:
    """Scan LLM-generated text for PII and redact if found."""
    results = analyzer.analyze(
        text=text,
        language="en",
        entities=[
            "EMAIL_ADDRESS", "PHONE_NUMBER", "SSN", "CREDIT_CARD",
            "US_BANK_NUMBER", "IBAN_CODE", "US_DRIVER_LICENSE",
            "PERSON", "LOCATION", "DATE_TIME", "API_KEY"
        ],
        score_threshold=0.5
    )

    if not results:
        return {"has_pii": False, "text": text, "findings": []}

    redacted = anonymizer.anonymize(text=text, analyzer_results=results)

    return {
        "has_pii": True,
        "text": redacted.text,
        "findings": [
            {"type": r.entity_type, "score": r.score, "start": r.start, "end": r.end}
            for r in results
        ]
    }
```

## Anonymization Strategies

| Strategy | Behavior | Use Case |
|----------|----------|----------|
| `replace` | Replace with entity type: `<EMAIL_ADDRESS>` | Safe for most contexts |
| `redact` | Replace with `[REDACTED]` | Maximum privacy, breaks readability |
| `hash` | Replace with SHA-256 hash | Re-identifiable for audit, not readable |
| `mask` | Show first/last chars: `j***@e***.com` | Balances privacy and readability |
| `encrypt` | Encrypt with key, decrypt for authorized viewers | Full reversibility for internal systems |

## Production Integration Pattern

```python
# Always run Presidio after Guardrails AI as a second-pass PII check
# Guardrails AI catches structured PII; Presidio catches unstructured PII
# and LLM-hallucinated PII that Guardrails AI misses

def output_guardrail_with_cascade(response: str) -> str:
    # Pass 1: Guardrails AI structured validation
    validated = composite_guard.validate(response)
    if validated.error:
        return handle_guardrails_failure(validated.error)

    # Pass 2: Presidio deep scan for residual PII
    scan = scan_llm_output(validated.validated_output)
    if scan["has_pii"]:
        log_pii_detection(scan["findings"])
        return scan["text"]  # Redacted version

    return validated.validated_output
```
