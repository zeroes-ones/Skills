# Skills Library Comparison

How zeroes-ones/Skills compares to other agent skill libraries.

## Measured Baseline (live)

Data for the zeroes-ones/Skills corpus, refreshed with:
`python3 scripts/benchmark-skills.py --root skills --markdown`
(add `--root <peer> --flat` to score a peer corpus with the same metrics).

<!-- MEASURED-BASELINE:START -->

| Skills (prompts) | 303 |
| Executable-node eligible (Core Workflow + Verification) | 300 |
| Declared `workflow:` contracts | 30 |
| Avg body words (load cost) | 8870 |
| Compiled coverage | 303/303 |
| Avg effective load (compiled tokens) | 1247 |
| Effective load saving vs raw body | 85.9% |
| Portability target declared | 100.0% |
| Golden eval sets covered | 3/3 |
| Routing Top-1 / Top-5 (lexical baseline) | 5/10 (50%) / 6/10 (60%) |

<!-- MEASURED-BASELINE:END -->

### vs. leading skill ecosystems — measured (peer repos fetched 2026-09-07)

Scored with the same harness (`python3 scripts/benchmark-skills.py`); structural rows are only
comparable where corpora share conventions, so the fair headline metrics are count and load cost:

| Metric | zeroes-ones/Skills | anthropics/skills | addyosmani/agent-skills | mattpocock/skills | obra/superpowers |
|--------|--------------------|-------------------|-------------------------|-------------------|------------------|
| Prompts | 298 | 19 | 25 | 37 | 14 |
| Avg body words (load cost) | 8960 | 1969 | 2073 | 638 | 1457 |
| Core Workflow + Verification structure | 295/298 | 0/19 (different anatomy) | 0/25 (different anatomy) | 0/37 (different anatomy) | 0/14 (different anatomy) |
| `workflow:` contracts | 30 | 0 | 0 | 0 | 0 |
| Portability target declared | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Golden eval sets covered | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 |

Routing rows are omitted for peers (their names do not match this library's held-out task set).
Re-run method: `python3 scripts/benchmark-skills.py --root skills --markdown` (ours) and
`--root <peer>/skills --shallow --markdown` for single-level layouts.

### Where each ecosystem leads (qualitative, 2026)

| Dimension | zeroes-ones/Skills | anthropics/skills | obra/superpowers | mattpocock/skills | skills.sh (ecosystem) |
|---|---|---|---|---|---|
| Scale + lifecycle coverage | 298 skills / 37 domains (CEO → governance) | curated ~19 skill archetypes | ~14-skill disciplined methodology | ~37 pragmatic daily skills | registry of many publishers' skills |
| Skill load economy | compiled 65-90% savings + progressive disclosure (body words are raw) | lean bodies | lean bodies, auto-injected session discipline | leanest bodies (638 avg) | CLI-managed installs |
| Quality governance | template/YAML/chain gates, audit, portability across 6 agents | high curation bar | methodology consistency | battle-tested by use | audits + community reputation |
| Distribution / marketplace | GitHub only today | official plugin/marketplace reach | plugin marketplaces + session hooks | skills.sh installer + plugin marketplaces | **the open registry + `skills` CLI** (auto-discovery, leaderboard) |
| Executable workflow layer / evals / self-improvement | **unique** | none | methodology as prose | none | install/update tooling, not content |

See `docs/distribution-best-in-class.md` for the researched incorporation plan (flat index for
registry auto-discovery, marketplace manifests, curated flagship set, methodology plugin,
lockfiles).

> **Column naming.** "Superpowers" alone is ambiguous: `obra/superpowers` (Jesse Vincent) is an
> autonomous spec → plan → subagent-execute → review methodology; `mattpocock/skills` (Matt Pocock)
> is a composable engineering toolkit centered on requirement grilling (`grill → spec → tickets →
> TDD → code review`). They are separate repositories with different owners and philosophies; this
> comparison tracks each under its own URL.

### vs. andrej-karpathy-skills (a note on scope)

`forrestchang/andrej-karpathy-skills` — the viral ~70-line `CLAUDE.md` distilling Karpathy's four
behavioral rules (think before coding, simplicity first, surgical changes, goal-driven execution) —
is **not a skills library and is excluded from the measured table**. It is a single per-project
configuration file constraining agent behavior, not a corpus of scoped, loadable skills; there is no
`SKILL.md` anatomy, routing, progressive disclosure, or per-skill verification to score. Its category
(closest to a global ground-rules block) is complementary: those four rules could serve as a
project-level `CLAUDE.md` overlay on top of any of the libraries above.

## vs. addyosmani/agent-skills

| Dimension | zeroes-ones/Skills | addyosmani/agent-skills |
|-----------|-------------------|------------------------|
| **Skills** | 298 across 37 domains | 24 across ~10 domains |
| **Scope** | Full company lifecycle (CEO → governance) | Engineering workflow (Define → Ship) |
| **Quality system** | 10/10 rating with 12+ required sections per skill | 6 standard sections per skill |
| **Chain/dependency** | 1,576 symmetric edges, bidirectional graph | Cross-references by name only |
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
| **Tiered activation** | --solo (8 skills), --grow (18), --full (298) | All-or-nothing |
| **Format standardization** | Agent-agnostic YAML frontmatter with portability target | Agent-agnostic YAML frontmatter |

**Bottom line:** zeroes-ones/Skills covers the full company lifecycle with deeper quality standards. addyosmani/agent-skills is an excellent engineering-focused library that pioneers persona architecture, hooks, and evals — all now absorbed into this library.

## vs. mattpocock/skills (Matt Pocock)

> History note: "Matt Pocock's Superpowers" conflates two separate projects. This section compares
> `mattpocock/skills` (Matt Pocock); `obra/superpowers` (Jesse Vincent) is scored in the measured
> table above. See the qualitative table note on column naming.

| Dimension | zeroes-ones/Skills | mattpocock/skills |
|-----------|-------------------|-------------|
| **Skills** | 298 (measured) | ~37 (measured) |
| **Focus** | Full lifecycle | TypeScript/JavaScript engineering workflow |
| **Architecture** | Structured skills with chain system + progressive disclosure | Composable slash commands, user-invoked vs model-invoked split |
| **Workflow** | Per-domain Core Workflow + Verification in every skill | grill → spec → vertical-slice tickets → TDD at seams → two-axis code review |
| **Domain coverage** | 37 domains | Primarily frontend/TypeScript |
| **Enterprise readiness** | Tiered activation, compliance skills | Dev-focused |
| **Cross-skill coordination** | 1,576 symmetric edges | Dependency-declared tickets, not cross-skill links |

**Bottom line:** mattpocock/skills is a disciplined, battle-tested engineering toolkit that
centers on grilling requirements before coding. zeroes-ones/Skills covers roles it doesn't address:
CEO, CTO, product, design, security, devops, data, legal, finance, healthcare, and more.

## What Makes This Library Unique

1. **Full lifecycle**: From CEO vision through architecture, development, security, compliance, operations, and governance — all coordinated via symmetric chain edges
2. **10/10 quality**: Every skill passes 12 governance gates including anti-hallucination guardrails, dollar-quantified gotchas, and progressive disclosure
3. **Scale-aware**: Solo → Small → Medium → Enterprise depth in every skill. Tiered activation matches skills to project maturity
4. **Industry-agnostic**: Universal frameworks with industry specifics in `references/` — works for healthcare, fintech, gaming, government, open source
5. **Persona architecture**: Role-based agent personas with tool restrictions, orchestration rules, and parallel fan-out patterns
6. **Infrastructure**: 5-category linting, 13-gate pre-commit hook, 43+ eval scenarios, command parity validation, hook system
7. **2,000+ sub-skills**: Progressive depth — start with parent skill overview, drill into sub-skills for domain-specific patterns
