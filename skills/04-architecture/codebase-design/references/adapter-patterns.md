# Adapter Patterns

## Pattern Catalog

### Translation Adapter
**When:** Module A and Module B use different data formats, protocols, or conventions.
**What:** Adapter converts A's format to B's expected format.
**Example:** A produces XML but B expects JSON. Adapter handles marshaling.
**Interface cost:** Low — typically 1-3 methods for format conversion.

### Facade
**When:** B is a complex subsystem with 10+ entry points, but A only needs 2-3 operations.
**What:** Facade exposes a simplified interface over B's complexity.
**Example:** Full email library (SMTP, MIME, attachments, retry) — Facade exposes `send(to, subject, body)`.
**Interface cost:** Very low — 1-5 methods covering the common case.

### Anti-Corruption Layer (ACL)
**When:** B is an external system, legacy code, or third-party dependency whose interface could change.
**What:** ACL translates between A's domain model and B's external model, insulating A from B's changes.
**Example:** Vendor payment API. ACL maps internal `Payment` domain object to vendor's v1 and v2 API formats.
**Interface cost:** Medium — worth it for the isolation benefit.

### Bridge
**When:** A needs to work with multiple implementations of the same abstract behavior.
**What:** Bridge defines an interface that multiple implementations satisfy. A depends on the interface, not any concrete implementation.
**Example:** Storage abstraction — S3, local FS, in-memory. Bridge defines `store()`, `retrieve()`, each backend implements.
**Interface cost:** Low — the abstraction reduces total interface surface.

## Selection Decision Matrix

| Criterion | Translation | Facade | ACL | Bridge |
|-----------|-------------|--------|-----|--------|
| Format mismatch | ✅ | ❌ | ✅ | ❌ |
| Simplify subsystem | ❌ | ✅ | ❌ | ❌ |
| External dependency | ❌ | ❌ | ✅ | ❌ |
| Multiple backends | ❌ | ❌ | ❌ | ✅ |
| Interface minimization | Medium | High | Medium | High |
