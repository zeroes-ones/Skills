# Context Pruning Rules — Per Pipeline Stage

## Pruning Philosophy: "Keep Everything Relevant, Nothing More"

Context pruning is NOT about minimizing token count. It's about maximizing signal-to-noise ratio
for the next agent in the pipeline. Each downstream agent sees only what it needs to make decisions.

## Pipeline Stage Rules

### Stage 1: Business → Architecture (strategy → system-architect)

| Keep | Remove |
|------|--------|
| Non-functional requirements (SLOs, scale targets) | Board meeting notes |
| Regulatory constraints (GDPR, HIPAA, SOC2) | Investor communication style |
| Budget ceilings per service | Market positioning details |
| Integration surface area (external systems) | Competitor analysis |

**Compression:** Summarize business constraints into architectural invariants. One-line each.

### Stage 2: Architecture → Development (system-architect → backend-developer)

| Keep | Remove |
|------|--------|
| ADRs with final decisions only | Architectural debate transcripts |
| API contracts (OpenAPI specs) | Alternative architectures considered |
| Data model schemas | Cost estimation spreadsheets |
| Technology constraints with rationale | Capacity planning models |
| Security boundaries and auth model | Deployment topology diagrams |

**Compression:** Collapse architecture decisions into constraint objects. Replace prose with specs.

### Stage 3: Development → DevOps (backend-developer → devops-engineer)

| Keep | Remove |
|------|--------|
| Runtime dependency manifest | Source code (unless for debugging) |
| Environment variable schema | Unit test files |
| Health check endpoints | Database migration scripts |
| Resource requirements (CPU/memory/disk) | API implementation details |
| Port bindings and protocol | Business logic documentation |

**Compression:** Convert app requirements into infrastructure requirements. Code → config.

### Stage 4: Development → Security (backend-developer → security-engineer)

| Keep | Remove |
|------|--------|
| Authentication/authorization flow | UI component trees |
| Data classification per endpoint | Performance tuning parameters |
| Third-party dependency SBOM | Caching strategy |
| Input validation schemas | Logging format preferences |
| Network exposure surface | Non-security configuration |

**Compression:** Extract security-relevant surface area. Everything else is noise.

## Universal Pruning Rules (ALL stages)

1. **Temporal relevance:** Remove anything >2 pipeline stages old unless explicitly pinned
2. **Decision finality:** Remove rejected alternatives if the decision is irreversible
3. **Audience filter:** If the next agent can't act on it, remove it
4. **Size budget:** If `token_budget_after` > 12,000, re-run pruning with stricter rules
5. **Integrity check:** Never remove constraints marked `non_negotiable: true`
