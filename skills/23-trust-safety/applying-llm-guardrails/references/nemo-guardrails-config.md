# NeMo Guardrails Configuration

## Colang Language Overview

Colang is NeMo's dialogue policy language. Rails are defined in `.co` files and organized into three types:

- **Input rails:** Validate user input before processing
- **Output rails:** Validate LLM output before delivery
- **Dialog rails:** Control conversation flow, topic boundaries, retry patterns

## Directory Structure

```
config/
├── config.yml              # Main configuration
├── rails/
│   ├── input.co            # Input validation rails
│   ├── output.co           # Output validation rails
│   └── dialog.co           # Dialog flow rails
├── prompts/
│   └── general.yml         # Prompt templates
└── actions/
    └── custom_actions.py   # Custom Python actions
```

## config.yml — Main Configuration

```yaml
models:
  - type: main
    engine: openai
    model: gpt-4o
  - type: embeddings
    engine: nvidia
    model: nv-embed-qa-4

rails:
  input:
    flows:
      - jailbreak check
      - self-check input
  output:
    flows:
      - check toxicity
      - check pii
      - self-check facts
  dialog:
    flows:
      - topic boundaries
      - off-topic handling
      - clarify ambiguous

config:
  sensitive_data_detection:
    entities:
      - EMAIL_ADDRESS
      - PHONE_NUMBER
      - SSN
      - CREDIT_CARD
```

## input.co — Input Rails

```colang
define flow jailbreak check
  $jailbreak_result = execute action detect_jailbreak($user_message)
  if $jailbreak_result.score > 0.9
    bot refuse to respond
    stop
  elif $jailbreak_result.score > 0.5
    bot "I notice your request contains unusual patterns. Could you rephrase?"
    stop
  else
    $allowed = True

define flow self-check input
  $check_result = execute action reflect_on_input($user_message)
  if not $check_result.safe
    bot refuse to respond
    stop
```

## output.co — Output Rails

```colang
define flow check toxicity
  $toxicity = execute action detect_toxicity($bot_message)
  if $toxicity.score > 0.7
    bot "I cannot provide that response. Let me rephrase."
    $bot_message = execute action regenerate_safe_response()

define flow check pii
  $pii_result = execute action detect_pii($bot_message)
  if $pii_result.has_pii
    $bot_message = execute action redact_pii($bot_message, $pii_result)

define flow self-check facts
  $facts_check = execute action check_facts($bot_message, $context)
  if $facts_check.hallucination_score > 0.5
    bot "I don't have enough information to answer that accurately."
    $bot_message = "Based on the available information, I cannot confirm that."
```

## dialog.co — Dialog Rails

```colang
define flow topic boundaries
  $topic_allowed = execute action check_topic($user_message, $allowed_topics)
  if not $topic_allowed
    bot "I'm designed to help with [allowed topics]. How can I assist within those areas?"
    stop

define flow off-topic handling
  if $off_topic_count >= 3
    bot "I've noticed we're moving away from my areas of expertise. Could we return to [primary topic]?"
    $off_topic_count = 0
```

## custom_actions.py — Python Integration

```python
from nemoguardrails.actions import action

@action()
async def detect_jailbreak(user_message: str) -> dict:
    from transformers import pipeline
    classifier = pipeline("text-classification", model="meta-llama/Prompt-Guard-86M")
    result = classifier(user_message)[0]
    return {"score": result["score"], "label": result["label"]}

@action()
async def detect_pii(text: str) -> dict:
    from presidio_analyzer import AnalyzerEngine
    analyzer = AnalyzerEngine()
    results = analyzer.analyze(text=text, language="en")
    return {"has_pii": len(results) > 0, "entities": [r.entity_type for r in results]}

@action()
async def redact_pii(text: str, pii_result: dict) -> str:
    from presidio_anonymizer import AnonymizerEngine
    anonymizer = AnonymizerEngine()
    return anonymizer.anonymize(text=text).text
```
