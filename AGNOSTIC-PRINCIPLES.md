# Agnostic Principles

> Skills are universal frameworks. They work for healthcare, fintech, gaming, e-commerce, education, infrastructure, government — any domain, any industry, any project type.

## Core Rule: Universal by Default, Specific by Reference

**Every SKILL.md must:**
1. Teach the universal pattern — applicable to ALL domains
2. Use domain-agnostic examples (e.g., "user data" not "patient record", "transaction" not "bank transfer")
3. Keep industry-specific guidance in `references/` — loaded only when needed
4. Never assume a single industry, domain, or project archetype

**Industry specifics belong in:**
- `references/industry-compliance-matrix.md` — regulations by industry
- `references/industry-patterns.md` — domain-specific architecture patterns
- Sub-skill references — domain-specific deep dives

## How to Test for Agnosticism

Read the SKILL.md and ask:
- Would this work for a healthcare startup? ✅/❌
- Would this work for a fintech company? ✅/❌
- Would this work for a gaming studio? ✅/❌
- Would this work for a government agency? ✅/❌
- Would this work for an e-commerce platform? ✅/❌
- Would this work for an open-source library? ✅/❌

If any answer is NO — the skill is too narrow. Fix it.

## Anti-Patterns: Domain Bias

| Anti-Pattern | Fix |
|-------------|-----|
| "Always use PCI DSS" | "Apply industry-specific compliance (see references/industry-compliance-matrix.md)" |
| "For SaaS products..." | "For products with user accounts..." |
| "MySQL is best for e-commerce" | "Relational databases excel when data integrity and ACID transactions are critical" |
| "Use React for dashboards" | "SPA frameworks excel for highly interactive interfaces" |
| "GDPR requires..." (as default) | "Privacy regulations require... (see references for jurisdiction specifics)" |
| "HIPAA mandates..." | "Healthcare compliance mandates... (see references/industry-compliance-matrix.md)" |
| "Fintech needs SOC 2" | "Regulated industries need SOC 2, ISO 27001, or equivalent" |

## Universal Pattern Examples

### BAD (Domain-Specific)
> "When building a SaaS platform, use multi-tenant database architecture with Stripe for payments."

### GOOD (Universal)
> "When multiple customers share infrastructure, isolate data per tenant. Payment processing should use a PCI-compliant provider."

### BAD (Industry-Biased)
> "Healthcare apps must encrypt PHI at rest with AES-256 per HIPAA requirements."

### GOOD (Universal)
> "Sensitive data must be encrypted at rest with AES-256 or stronger. Industry regulations may mandate additional controls — consult references for domain-specific requirements."

## Token-Efficient Agnosticism

The skill teaches the universal pattern in ~300 lines. Industry specifics live in references, loaded on demand. This saves tokens:

```
Agent working on fintech project:
  → Reads SKILL.md (300 lines) — universal database design patterns
  → Reads references/industry-compliance-matrix.md (200 lines) — PCI DSS specifics
  → Total: 500 lines of relevant content

Agent working on gaming project:
  → Reads SKILL.md (300 lines) — universal database design patterns
  → Doesn't need compliance reference
  → Total: 300 lines
```

Without agnostic design:
```
→ Reads SKILL.md (800 lines) — 500 lines of fintech-specific content wasted
```

## Chain-Aware Coordination

Skills are linked via symmetric YAML `chain:` blocks. Coordination is not ad-hoc — it follows the declared dependency graph:

```yaml
chain:
  consumes_from: [api-designer, database-designer]  # Must complete BEFORE this skill
  feeds_into: [frontend-developer, qa-engineer]      # Needs this skill's output NEXT
```

**Principles:**
1. **Chain edges are domain-agnostic** — `backend-developer` feeds into `code-reviewer` whether you're building fintech, healthcare, or gaming
2. **Decision gates are universal** — "Before merging, verify API contract compatibility" applies to all industries
3. **Artifacts are archetype-aware** — The artifact format may vary (FHIR resources vs. REST APIs), but the handoff pattern is the same
4. **Coordinate at decision gates, not continuously** — The chain tells you WHEN to coordinate, not just WHO to talk to
5. **Symmetry is verifiable** — Run `python3 -c "import yaml, glob; ..."` to confirm 0 asymmetries across all 103 skills

## Project Archetype Coverage

Every skill should reference these archetypes in decision trees (not hardcode):

| Archetype | Characteristics | Common Constraints |
|-----------|----------------|-------------------|
| **Web SaaS** | Multi-tenant, web-based, user accounts | Scalability, multi-tenancy, billing |
| **API/Platform** | Developer-facing, programmatic access | Rate limiting, docs, versioning |
| **Mobile App** | Native/hybrid, app store distribution | Offline, push, platform HIG |
| **Data/AI Product** | ML models, analytics, data pipeline | Data quality, pipeline reliability |
| **IoT/Embedded** | Hardware, sensors, edge computing | Bandwidth, power, reliability |
| **Open Source Library** | Community-driven, public repo | Contribution flow, documentation |
| **Internal Tool** | Employee-facing, limited audience | Simplicity, UX not critical |
| **E-commerce** | Transactions, catalog, checkout | Payment compliance, performance |
| **Content Platform** | Publishing, media, SEO | CMS, CDN, editorial workflow |
| **Infrastructure/Tooling** | DevOps, monitoring, CI/CD | Reliability, developer experience |

A skill should provide guidance that ADAPTS to any of these archetypes — not guidance written FOR one archetype.

## Sub-Skills and Industry Depth

When a sub-skill requires industry depth:
- The parent SKILL.md says "For [industry], see `references/[industry]-guide.md`"
- The reference document contains the industry-specific patterns
- The agent loads the reference only for that industry

This way:
- The skill stays clean and universal (~300 lines)
- Each industry reference is deep and specific (~200-500 lines)
- Token usage is optimized — only relevant content loaded
