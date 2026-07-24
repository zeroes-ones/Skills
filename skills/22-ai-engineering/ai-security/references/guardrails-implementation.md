# Guardrails Patterns & Tools — Reference

## Overview

AI guardrails enforce safety and security policies at runtime by intercepting,
validating, and transforming LLM inputs and outputs. They form a critical
defense-in-depth layer between the application and the model.

## Tool Ecosystem

| Tool | Strengths | Primary Use Case |
|------|-----------|-----------------|
| NeMo Guardrails | Colang DSL, dialog flows, topical rails | Conversational AI with structured dialog control |
| Guardrails AI | Pydantic-style validators, re-asking on failure | Structured output validation with LLM self-correction |
| LLM Guard | Regex + ML-based scanners, PII redaction | Input/output scanning, prompt injection detection |

## Architecture Patterns

- **Fail-closed topology:** Guardrail failure blocks the request — never let a
  failed guardrail pass unsafe content (availability risk vs. safety risk)
- **Pre-model input rail:** Sanitize, classify, and redact inputs before they
  reach the model context window
- **Post-model output rail:** Validate structure, scan for PII/hallucinations,
  enforce schema compliance before returning to the caller
- **Dialog rails:** Maintain conversation state machine to prevent jailbreak
  sequences spanning multiple turns

## Implementation Guidelines

- Compose guardrails as independent, testable filters rather than a monolithic check
- Log all guardrail decisions with full context for audit and false-positive tuning
- Test guardrail bypass with automated adversarial probes (garak, PyRIT, manual red-teaming)
- PII redaction must preserve entity type markers for downstream processing (e.g.,
  `[REDACTED-PHONE]` vs. blank replacement)
- Rate-limit guardrail bypass attempts independently from application rate limits
