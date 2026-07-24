# 4-Layer Defense Model — Architecture

## Overview

Single-layer guardrails are always bypassable. Defense-in-depth requires four independently operating layers:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    INPUT     │ ──► │    PROMPT    │ ──► │   RUNTIME    │ ──► │    OUTPUT    │
│  Classifier  │     │  Semantic    │     │   Dialog     │     │  Validator   │
│  (jailbreak) │     │  (intent)    │     │  (flow)      │     │  (response)  │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
    10-30ms             10-20ms             10-20ms             20-50ms
```

## Layer 1: Input Guardrails

**Tool:** Prompt Guard (86M params)
**Threats addressed:**
- Direct jailbreak attempts (DAN, role-play, encoding-based)
- Indirect prompt injection via third-party content (RAG docs, emails)
- Malicious code injection in user prompts
- Tokenizer abuse (Unicode normalization attacks, BPE drop attacks)

**Design rules:**
- Run before any prompt assembly — raw user input only
- Block at score > 0.9, challenge at 0.5-0.9, allow at < 0.5
- Scan ALL third-party content before it enters the prompt context
- Hardened user input normalization (strip invisible chars, normalize Unicode)

## Layer 2: Prompt Guardrails

**Tool:** NeMo Guardrails (input rails)
**Threats addressed:**
- Semantically unsafe but syntactically clean inputs
- Multi-turn attack sequences (Crescendo pattern)
- Context boundary violations (off-topic steering)
- Prompt leaking (extracting system prompt)

**Design rules:**
- Semantic validation against safety policy, not pattern matching
- Self-check input: have the LLM reflect on whether the request is safe
- Topic boundary enforcement: reject queries outside allowed domains
- Maintain multi-turn state to detect attack escalation patterns

## Layer 3: Runtime Guardrails

**Tool:** NeMo Guardrails (dialog rails)
**Threats addressed:**
- Gradual topic drift into unsafe territory
- Multi-turn manipulation (10+ turns of subtle steering)
- Policy-enforced response boundaries (legal, medical, financial disclaimers)
- Session-level attack detection (sustained adversarial behavior)

**Design rules:**
- Track conversation topic vector over turns
- Alert on sustained drift (> 0.5 cosine from starting topic)
- Enforce per-session safety budget (3 strikes = session termination)
- Apply dialog-level retry/recovery patterns before blocking

## Layer 4: Output Guardrails

**Tool:** Guardrails AI + Presidio
**Threats addressed:**
- Toxic/harmful LLM-generated content
- PII leakage (real and hallucinated PII in generated text)
- Malformed structured output (JSON schema violations)
- Hallucinated facts (contradicting retrieved context)
- Code injection in generated code blocks

**Design rules:**
- Validate every output token before user delivery
- Streaming output requires streaming validators with < 50ms buffer
- Cascade: Guardrails AI first, Presidio second (for residual PII)
- Fail-closed: block output if any validator fails
- Never include detected content in error messages

## Threat Coverage Matrix

| Threat | Layer 1 | Layer 2 | Layer 3 | Layer 4 |
|--------|---------|---------|---------|---------|
| Jailbreak | ✓ | ✓ | | |
| Indirect injection | ✓ | | | |
| Semantic evasion | | ✓ | | |
| Multi-turn attack | | ✓ | ✓ | |
| Topic drift | | | ✓ | |
| Toxic output | | | | ✓ |
| PII leakage | | | | ✓ |
| Hallucination | | | | ✓ |
| Code injection | | | | ✓ |
