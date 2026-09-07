# Skills Library Comparison

How zeroes-ones/Skills compares to other agent skill libraries.

## Measured Baseline (live)

Data for the zeroes-ones/Skills corpus, refreshed with:
`python3 scripts/benchmark-skills.py --root skills --markdown`
(add `--root <peer> --flat` to score a peer corpus with the same metrics).

<!-- MEASURED-BASELINE:START -->

| Skills (prompts) | 297 |
| Executable-node eligible (Core Workflow + Verification) | 294 |
| Declared `workflow:` contracts | 30 |
| Avg body words (load cost) | 8976 |
| Compiled coverage | 233/297 |
| Avg effective load (compiled tokens) | 3545 |
| Effective load saving vs raw body | 63.4% |
| Portability target declared | 100.0% |
| Golden eval sets covered | 3/3 |
| Routing Top-1 / Top-5 (lexical baseline) | 3/10 (30%) / 6/10 (60%) |

<!-- MEASURED-BASELINE:END -->

### vs. leading skill ecosystems — measured (peer repos fetched 2026-09-07)

Scored with the same harness (`python3 scripts/benchmark-skills.py`); structural rows are only
comparable where corpora share conventions, so the fair headline metrics are count and load cost:

| Metric | zeroes-ones/Skills | anthropics/skills | addyosmani/agent-skills | mattpocock/skills | obra/superpowers |
|--------|--------------------|-------------------|-------------------------|-------------------|------------------|
| Prompts | 297 | 19 | 25 | 37 | 14 |
| Avg body words (load cost) | 8976 | 1969 | 2073 | 638 | 1457 |
| Core Workflow + Verification structure | 294/297 | 0/19 (different anatomy) | 0/25 (different anatomy) | 0/37 (different anatomy) | 0/14 (different anatomy) |
| `workflow:` contracts | 30 | 0 | 0 | 0 | 0 |
| Portability target declared | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Golden eval sets covered | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 |

Routing rows are omitted for peers (their names do not match this library's held-out task set).
Re-run method: `python3 scripts/benchmark-skills.py --root skills --markdown` (ours) and
`--root <peer>/skills --shallow --markdown` for single-level layouts.

### Where each ecosystem leads (qualitative, 2026)

| Dimension | zeroes-ones/Skills | anthropics/skills | superpowers | mattpocock/skills | skills.sh (ecosystem) |
|---|---|---|---|---|---|
| Scale + lifecycle coverage | 297 skills / 37 domains (CEO → governance) | curated ~19 skill archetypes | ~14-skill disciplined methodology | ~37 pragmatic daily skills | registry of many publishers' skills |
| Skill load economy | compiled 65-90% savings + progressive disclosure (body words are raw) | lean bodies | lean bodies, auto-injected session discipline | leanest bodies (638 avg) | CLI-managed installs |
| Quality governance | template/YAML/chain gates, audit, portability across 6 agents | high curation bar | methodology consistency | battle-tested by use | audits + community reputation |
| Distribution / marketplace | GitHub only today | official plugin/marketplace reach | plugin marketplaces + session hooks | skills.sh installer + plugin marketplaces | **the open registry + `skills` CLI** (auto-discovery, leaderboard) |
| Executable workflow layer / evals / self-improvement | **unique** | none | methodology as prose | none | install/update tooling, not content |

See `docs/distribution-best-in-class.md` for the researched incorporation plan (flat index for
registry auto-discovery, marketplace manifests, curated flagship set, methodology plugin,
lockfiles).
| Executable workflow layer (loops/graphs/engine) | **unique** — none of the peers ship an engine + manifests + guardrails | none | pipeline discipline is prose (workflows as plans) | none |
| Evals + telemetry + self-improvement | golden evals, OTel exporter, SLIs, verifier-gated self-improvement | none published | none published | none published |
| Ecosystem/mindshare + marketplace distribution | newer; smaller install base | Anthropic official + huge reach | large reach + plugin marketplaces | large reach (skills.sh / plugin marketplaces) |

Note: "Matt Pocock's Superpowers" historically conflates `mattpocock/skills` with
`obra/superpowers`; measured rows above match each repository by its URL.

## vs. addyosmani/agent-skills

| Dimension | zeroes-ones/Skills | addyosmani/agent-skills |
|-----------|-------------------|------------------------|
| **Skills** | 297 across 37 domains | 24 across ~10 domains |
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
