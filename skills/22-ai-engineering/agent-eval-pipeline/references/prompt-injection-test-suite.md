# Prompt Injection Test Suite

## Attack Taxonomy

### Direct Injection
- "Ignore previous instructions and..."
- "SYSTEM: Your new instructions are..."
- "[[OVERRIDE]] ..."
- Role-playing: "You are now DAN (Do Anything Now)..."

### Indirect Injection
- Malicious content in retrieved documents
- Poisoned web pages in browsing context
- Tool output containing injected instructions

### Context Manipulation
- Long context flooding (attention dilution)
- Multi-turn grooming (build trust, then exploit)
- Language switching mid-conversation

### Multi-Modal Injection
- Instructions hidden in images (OCR triggers)
- Base64-encoded payloads
- Unicode homoglyph attacks

## Test Suite Design
- Minimum 100 test cases covering all attack categories
- Include defense-in-depth: test each guardrail layer independently
- Test with AND without guardrails for baseline comparison
- Rotate test cases: attackers evolve, test suite must evolve
