## Implementation Reference Patterns

### LlamaGuard 3 Custom Policy Example

Replace Meta's default 14-category taxonomy with domain-specific hazards:

```python
CUSTOM_SAFETY_POLICY = """
S1: Medical Misinformation
    - Promoting unproven treatments or cures
    - Discouraging evidence-based medical care
    - Recommending harmful alternative remedies
S2: Financial Misconduct
    - Pump-and-dump stock schemes
    - Unauthorized investment advice
    - Cryptocurrency fraud instructions
S3: Legal Misrepresentation
    - Unauthorized legal counsel
    - Court document forgery instructions
    - Impersonating legal professionals
S4: Code Injection & Exploitation
    - SQL injection payload generation
    - XSS attack vector construction
    - Malware development instructions
S5: Self-Harm & Suicide Content
    - Methods or encouragement of self-harm
    - Suicide instructions or glorification
    - Eating disorder promotion
"""

# Deploy with custom policy
result = classify_safety(conversation, custom_policy=CUSTOM_SAFETY_POLICY)
```

### Streaming Output Validation Pattern

For real-time streaming applications, buffered validation with safety cutoff:

```python
import asyncio

class StreamingSafetyBuffer:
    """Buffer streaming tokens, validate chunks, cut off if unsafe."""

    def __init__(self, check_interval_ms: int = 50, max_buffer_chars: int = 200):
        self.buffer = ""
        self.check_interval = check_interval_ms / 1000
        self.max_chars = max_buffer_chars
        self.safe = True

    async def process_stream(self, token_stream):
        """Stream tokens to user while validating in background."""
        async for token in token_stream:
            if not self.safe:
                break  # Safety cutoff — stop streaming

            self.buffer += token
            yield token  # Deliver immediately (sub-50ms buffer)

            if len(self.buffer) >= self.max_chars:
                safety_result = await self.check_safety(self.buffer)
                if not safety_result["safe"]:
                    self.safe = False
                    yield "\n\n[Response interrupted by safety filter.]"
                self.buffer = ""  # Reset buffer

    async def check_safety(self, text: str) -> dict:
        """Async safety check without blocking the stream."""
        return await asyncio.to_thread(output_guardrail, text)
```

### Multi-Turn Attack Detection Pattern

Crescendo attacks escalate harmfulness across conversation turns. Detect escalation:

```python
class MultiTurnSafetyTracker:
    """Track safety scores across turns to detect gradual escalation."""

    def __init__(self, escalation_threshold: float = 0.3, window: int = 5):
        self.turn_scores = []
        self.threshold = escalation_threshold
        self.window = window

    def record_turn(self, jailbreak_score: float, toxicity_score: float):
        self.turn_scores.append({
            "jailbreak": jailbreak_score,
            "toxicity": toxicity_score
        })

        if len(self.turn_scores) >= self.window:
            recent = self.turn_scores[-self.window:]
            jb_trend = sum(r["jailbreak"] for r in recent) / self.window
            tox_trend = sum(r["toxicity"] for r in recent) / self.window

            if jb_trend - self.turn_scores[0]["jailbreak"] > self.threshold:
                return {"alert": "jailbreak_escalation", "trend": jb_trend}
            if tox_trend - self.turn_scores[0]["toxicity"] > self.threshold:
                return {"alert": "toxicity_escalation", "trend": tox_trend}

        return {"alert": None}

    def should_terminate_session(self) -> bool:
        """Terminate session if safety budget exceeded (3 strikes rule)."""
        strikes = sum(
            1 for s in self.turn_scores
            if s["jailbreak"] > 0.7 or s["toxicity"] > 0.8
        )
        return strikes >= 3
```

### Failover Architecture for Guardrail Unavailability

```python
class GuardrailOrchestrator:
    """Orchestrate guardrail layers with circuit breakers and fallbacks."""

    def __init__(self):
        self.circuit_state = {layer: "closed" for layer in LAYERS}
        self.failure_count = {layer: 0 for layer in LAYERS}
        self.failure_threshold = 5
        self.cooldown_seconds = 30

    async def execute_layer(self, layer: str, fn, *args) -> dict:
        if self.circuit_state[layer] == "open":
            await self.check_cooldown(layer)
            return self.fallback_response(layer)

        try:
            result = await asyncio.wait_for(fn(*args), timeout=0.05)
            self.failure_count[layer] = 0
            return result
        except (asyncio.TimeoutError, Exception) as e:
            self.failure_count[layer] += 1
            if self.failure_count[layer] >= self.failure_threshold:
                self.circuit_state[layer] = "open"
                trigger_alert(f"Guardrail {layer} circuit breaker OPEN")
            return self.fallback_response(layer)

    def fallback_response(self, layer: str) -> dict:
        """Fail-closed for input layers, fail-open+audit for output layers."""
        if layer in ("input", "prompt"):
            return {"allow": False, "flags": ["guardrail_unavailable_fail_closed"]}
        else:
            log_audit_warning(f"Guardrail {layer} bypassed — fail-open")
            return {"allow": True, "flags": ["guardrail_unavailable_fail_open"]}
```

---

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

**Portability:** works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
