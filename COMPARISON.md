# Skills Library Comparison

How zeroes-ones/Skills compares to other agent skill libraries.

## vs. addyosmani/agent-skills

| Dimension | zeroes-ones/Skills | addyosmani/agent-skills |
|-----------|-------------------|------------------------|
| **Skills** | 210 across 28 domains | 24 across ~10 domains |
| **Scope** | Full company lifecycle (CEO → governance) | Engineering workflow (Define → Ship) |
| **Quality system** | 10/10 rating with 12+ required sections per skill | 6 standard sections per skill |
| **Chain/dependency** | 1,675 symmetric edges, bidirectional graph | Cross-references by name only |
| **Progressive disclosure** | QUICK/STANDARD/DEEP markers on every section | ~500 line max per skill |
| **Scale depth** | Solo → Small → Medium → Enterprise in every skill | Not structured |
| **Error recovery** | Symptom → Root Cause → Fix → Lesson decoders with dollar-quantified gotchas | Common rationalizations table |
| **Token budget** | Declared per skill, progressive loading | System prompt injection (~1024 char) |
| **Persona architecture** | 4 personas with orchestration rules | 4 personas with orchestration rules |
| **Hook system** | 3 hook types (session-start, simplify-ignore, SDD-cache) | 3 hook types |
| **Command wrappers** | 8 commands × 3 tools (Claude, Gemini, Copilot) | 8 commands × 3 tools |
| **Evals** | 43+ structural scenarios | 3-tier: structural + TF-IDF routing + behavioral |
| **Distribution** | npm CLI + marketplace entries + shell installer | npm CLI (`npx skills`) + marketplace |
| **Unique domains** | Web3, hardware, health-clinical, trust-safety, creative, creator-finance, social-impact, corporate-finance, governance | None beyond engineering |
| **Sub-skill map** | 2,000+ sub-skills with industry variations | None |
| **Skill-levels framework** | L1-L5 competency taxonomy | None |
| **Tiered activation** | --solo (8 skills), --grow (18), --full (210) | All-or-nothing |
| **Format standardization** | Agent-agnostic YAML frontmatter with portability target | Agent-agnostic YAML frontmatter |

**Bottom line:** zeroes-ones/Skills covers the full company lifecycle with deeper quality standards. addyosmani/agent-skills is an excellent engineering-focused library that pioneers persona architecture, hooks, and evals — all now absorbed into this library.

## vs. Matt Pocock's Superpowers

| Dimension | zeroes-ones/Skills | Superpowers |
|-----------|-------------------|-------------|
| **Skills** | 210 | ~20 |
| **Focus** | Full lifecycle | TypeScript/JavaScript development |
| **Architecture** | Structured with chain system | Conversational patterns |
| **Domain coverage** | 28 domains | Primarily frontend/TypeScript |
| **Enterprise readiness** | Tiered activation, compliance skills | Dev-focused |
| **Cross-skill coordination** | 1,675 symmetric edges | Not structured |

**Bottom line:** Superpowers is excellent for TypeScript developers. zeroes-ones/Skills covers roles Superpowers doesn't address: CEO, CTO, product, design, security, devops, data, legal, finance, healthcare, and more.

## What Makes This Library Unique

1. **Full lifecycle**: From CEO vision through architecture, development, security, compliance, operations, and governance — all coordinated via symmetric chain edges
2. **10/10 quality**: Every skill passes 12 governance gates including anti-hallucination guardrails, dollar-quantified gotchas, and progressive disclosure
3. **Scale-aware**: Solo → Small → Medium → Enterprise depth in every skill. Tiered activation matches skills to project maturity
4. **Industry-agnostic**: Universal frameworks with industry specifics in `references/` — works for healthcare, fintech, gaming, government, open source
5. **Persona architecture**: Role-based agent personas with tool restrictions, orchestration rules, and parallel fan-out patterns
6. **Infrastructure**: 5-category linting, 13-gate pre-commit hook, 43+ eval scenarios, command parity validation, hook system
7. **2,000+ sub-skills**: Progressive depth — start with parent skill overview, drill into sub-skills for domain-specific patterns
