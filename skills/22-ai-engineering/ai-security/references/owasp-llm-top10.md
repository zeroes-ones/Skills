# OWASP LLM Top 10 v1.1 — Reference

## Overview

The OWASP Top 10 for Large Language Model Applications (v1.1, October 2024) catalogs the 10 most critical vulnerabilities in LLM-integrated applications.

## The 10 Categories

| # | Category | Core Vulnerability |
|---|----------|-------------------|
| LLM01 | Prompt Injection | Untrusted text enters model context, overrides system instructions |
| LLM02 | Insecure Output Handling | LLM output passed to downstream systems without validation |
| LLM03 | Training Data Poisoning | Malicious data injected during training or fine-tuning |
| LLM04 | Model Denial of Service | Resource exhaustion via malicious inputs or high-volume requests |
| LLM05 | Supply Chain Vulnerabilities | Compromised model weights, dependencies, or third-party components |
| LLM06 | Sensitive Information Disclosure | PII, secrets, or proprietary data in training data or model output |
| LLM07 | Insecure Plugin Design | LLM-invoked plugins with insufficient input validation or excessive permissions |
| LLM08 | Excessive Agency | LLM granted autonomous action capability beyond what is necessary |
| LLM09 | Overreliance | Systems treating LLM output as authoritative without verification |
| LLM10 | Model Theft | Unauthorized access to or extraction of proprietary model weights/IP |

## Mapping to Mitigations

Each category requires layered defense: input sanitization, prompt architecture, output
validation, plugin sandboxing, guardrails, and human-in-the-loop for high-risk actions.
No single control addresses all categories — defense-in-depth is mandatory.

## v1.1 Updates from v1.0

- LLM04 expanded from "Model Denial of Service" to include resource exhaustion techniques
- LLM05 refined supply chain scope to include model weight provenance
- LLM08 renamed from "Excessive Agency" to clarify scope — not just plugins, any autonomous action
- Added emphasis on multi-modal injection vectors (images, audio, documents)
