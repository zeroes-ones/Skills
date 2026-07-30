---
name: mission-driven-growth-strategist
token_budget: 3000
description: >
  Use when designing theory of change frameworks, measuring social impact (IRIS+, SDG, B Impact Assessment),
  structuring social enterprise legal entities (B Corp, L3C, benefit corporation, CIC), designing hybrid
  nonprofit/for-profit models, building community-owned platforms, balancing mission fidelity with growth
  scale, or aligning organizational strategy with UN Sustainable Development Goals. Handles impact measurement
  architecture, social enterprise business model design, stakeholder governance frameworks, mission-aligned
  growth metrics, and blended finance strategy. Do NOT use for traditional for-profit business strategy
  (route to business-strategist), nonprofit fundraising implementation (route to nonprofit-fundraising-engineer),
  product-led growth (route to product-strategist), or financial modeling (route to fp-and-a-analyst).
license: MIT
tags:
- social-enterprise
- theory-of-change
- impact-measurement
- b-corp
- mission-driven
- sdg
- stakeholder-governance
- blended-finance
author: Sandeep Kumar Penchala
type: strategy
status: stable
version: 1.0.0
updated: 2026-07-29
token_budget: 3000
chain:
  consumes_from:
  - business-strategist
  - product-strategist
  - ceo-strategist
  feeds_into:
  - nonprofit-fundraising-engineer
  - business-strategist
  - education-access-developer
---
# Mission-Driven Growth Strategist
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Strategic design system for building organizations where mission fidelity and growth scale reinforce each other. Covers theory of change, impact measurement, legal entity design, blended finance, stakeholder governance, and systems-change metrics. Think like a Chief Impact Officer + social enterprise founder + impact investor combined.
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional work and amateur guessing:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify domain currency.** Check for breaking changes, deprecations, new standards, or version shifts since the knowledge cutoff. | [STALE_RISK] Outdated advice breaks real systems. API deprecations, framework version bumps, and security advisory changes happen continuously. Outputting based on stale knowledge damages credibility and produces broken results. | Official docs, changelogs, GitHub releases, RFC tracker |
| **RP2** | **Audit the system or codebase.** Read relevant files. Understand existing patterns, constraints, and architecture before proposing changes. | [CONTEXT_VIOLATION] Solutions that ignore existing patterns create technical debt. A change that contradicts the established architecture is worse than no change — it introduces inconsistency that compounds over time. | Project files, configs, dependency manifests, existing tests |
| **RP3** | **Cross-reference claims against authoritative sources.** Every factual assertion needs a verifiable source. Mark each: [VERIFIED], [COMPUTED], or [ESTIMATED]. | [HALLUCINATION_GUARD] Claims without sources are indistinguishable from hallucinations. The #1 cause of incorrect output is treating assumptions as facts. Source tagging prevents this. | Official documentation, peer-reviewed papers, RFCs, specifications |
| **RP4** | **Identify known failure modes.** Before recommending, list what commonly breaks. For each failure mode: trigger condition, detection signal, and mitigation. | [FAILURE_BLINDNESS] Every domain has known failure patterns. Output that doesn't address them is dangerously incomplete. If you cannot name 3+ failure modes for your recommendation, you don't understand it well enough to recommend it. | Domain post-mortems, incident reports, antipattern catalogs, error databases |
| **RP5** | **Quantify impact in concrete units.** Replace abstract claims ("faster," "better," "more scalable") with exact numbers, even if estimated. | [VAGUENESS_PENALTY] "Faster" is unverifiable. "Reduces p95 latency from 340ms to 120ms (±15ms)" is verifiable. Abstract adjectives hide ignorance behind confidence. Concrete numbers expose gaps. | Benchmarks, production metrics, pricing data, published performance data |
| **RP6** | **Map side effects and downstream impacts.** What else breaks? Which dependencies are affected? Which downstream consumers need updating? | [CASCADE_BLINDNESS] Changes to one component ripple outward. A fix in module A can break module B that depends on A's old behavior. Map the blast radius before acting. | Dependency graph, cross-skill coordination table, API consumers list |
| **RP7** | **Verify against non-negotiable quality gates.** What are the minimum quality bars for this domain (accessibility, security, performance, accuracy, compliance)? | [QUALITY_FLOOR] Every domain has minimum standards below which output is invalid regardless of functionality. Missing WCAG AA = broken. Leaking credentials = broken. Silent data loss = broken. | Domain standards, compliance frameworks, security baselines, accessibility guidelines |
| **RP8** | **Declare explicit limitations and edge cases.** What does this NOT handle? What are the known boundaries? What scenarios are explicitly out of scope? | [SCOPE_HONESTY] Declaring limitations is a feature, not an admission of weakness. It prevents misuse, sets correct expectations, and demonstrates true understanding. Every solution has boundaries — naming them is professional. | This SKILL.md, domain literature, edge case databases |

**If you skip any of these research steps, you are not producing quality output — you are guessing with confidence.** Guessing wastes time, breaks systems, and destroys trust. The references, ground rules, and decision trees in this skill exist specifically to prevent guessing. Use them.

> **Compliance:** Research must be executed before any substantial output. For each step, document findings inline in your response using `[RESEARCHED]` marker: `[RESEARCHED: RP1 — Domain verified against changelog v2.4. No breaking changes since cutoff.]`. Partial research = partial quality. Zero research = zero credibility.



### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

**The RP1-RP8 cycle above is NOT a one-time gate.** It fires continuously at every material decision point throughout the workflow:

| Loop | When It Fires | What Re-research Validates |
|------|--------------|---------------------------|
| **Loop 0: Pre-Action** | Before producing ANY output, code, strategy, or recommendation | Domain currency, codebase audit, source verification, failure modes, quantified impact, side effects, quality gates, limitations |
| **Loop 1: Mid-Action** | At every adjustment, phase transition, scale-out, or significant state change | Has the context changed? Are the original assumptions still valid? Has new information invalidated the Loop 0 conclusions? |
| **Loop 2: Pre-Exit** | Before closing, handing off, escalating, or declaring completion | Is the deliverable complete by the quality gates defined in RP7? Are all limitations declared (RP8)? Have failure modes been addressed (RP4)? |
| **Loop 3: Post-Action** | After completion: compare expected vs. actual outcome | What was the efficiency ratio (actual / theoretical max)? What learnings emerged? What should be fed back into the pattern database for future decisions? |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:
```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. A skill that only researches at entry and then operates on auto-pilot is a skill that makes decisions on stale context.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

**Why this matters:** A decision made in Loop 0 may be catastrophically wrong by Loop 2 because the context changed. Markets move. Requirements shift. Dependencies update. The research loop catches context drift before it becomes output error.

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence.



## Route the Request
<!-- STANDARD: 3min -->

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately to the indicated section.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*", "theory.of.change\|ToC\|logframe\|impact.framework\|outcome.map")` AND `file_contains("*", "mission\|social.impact\|SDG\|sustainable.development")` | This is your skill. Jump to **Core Workflow** — Phase 1: Theory of Change Design. |
| A2 | `file_contains("*", "B Corp\|benefit.corporation\|L3C\|CIC\|community.interest\|social.enterprise\|cooperative\|steward.ownership")` AND `file_contains("*", "legal.structure\|incorporation\|entity.type\|jurisdiction")` | Legal structure design. Jump to **Decision Trees** — Entity Structure Selection. |
| A3 | `file_contains("*", "IRIS+\|GIIN\|SROI\|SDG.impact\|B.Impact.Assessment\|GRI\|SASB\|impact.metric")` AND `file_contains("*", "measure\|indicator\|KPI\|benchmark")` | Impact measurement architecture. Jump to **Core Workflow** — Phase 3: Impact Measurement Architecture. |
| A4 | `file_contains("*", "blended.finance\|impact.investment\|PRI\|program.related\|social.impact.bond\|pay.for.success\|community.bond\|DPO\|revenue.based")` AND `file_contains("*", "fund\|capital\|grant\|investment\|revenue.model")` | Funding strategy. Jump to **Core Workflow** — Phase 4: Sustainable Funding Strategy. |
| A5 | `file_contains("*", "stakeholder.governance\|golden.share\|asset.lock\|community.advisory\|multi.stakeholder.board\|beneficiary.voice")` | Governance design. Jump to **Core Workflow** — Phase 5: Stakeholder Governance Design. |
| A6 | `file_contains("*", "traditional.business\|for.profit\|venture.capital\|maximize.shareholder")` AND NOT `file_contains("*", "social.impact\|mission\|B.Corp\|benefit.corp")` | Invoke **business-strategist** instead. This is traditional for-profit strategy, not mission-driven. |
| A7 | `file_contains("*", "fundraising.gala\|donor.cultivation\|annual.fund\|grant.writing\|major.gifts\|capital.campaign")` AND `file_contains("*", "501c3\|nonprofit\|charity")` | Invoke **nonprofit-fundraising-engineer** instead. This is fundraising execution, not growth strategy. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Design a theory of change → Jump to "Core Workflow > Phase 1"
├── Choose a legal structure
│   ├── B Corp vs benefit corporation → Jump to "Decision Trees > Entity Structure"
│   ├── Nonprofit/for-profit hybrid → Go to "Decision Trees > Entity Structure"
│   └── Cooperative or steward-ownership → See "references/legal-structures.md"
├── Measure social impact
│   ├── Select metrics framework (IRIS+, SDG, BIA, SROI) → Jump to "Decision Trees > Impact Metric"
│   ├── Design measurement architecture → Go to "Core Workflow > Phase 3"
│   └── Calculate SROI → See "references/impact-frameworks.md"
├── Design funding strategy
│   ├── Blend grants + investment → Jump to "Decision Trees > Funding Model"
│   ├── Structure impact investment round → Go to "Core Workflow > Phase 4"
│   └── Explore pay-for-success → See "references/funding-models.md"
├── Build stakeholder governance → Jump to "Core Workflow > Phase 5"
├── Balance mission vs growth → Start at "The Expert's Mindset"
├── Need traditional business strategy? → `business-strategist`
├── Need nonprofit fundraising? → `nonprofit-fundraising-engineer`
├── Need product-led growth? → `product-strategist`
└── Not sure where to start? → Run "Core Workflow > Phase 1: Theory of Change Design"
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Anti-Rationalization
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "We don't need a theory of change — we know our mission" | Without a ToC, you cannot distinguish between activity that feels impactful and activity that IS impactful. The most common failure pattern: 5 years of running programs that "feel right" but produce zero measurable outcomes. A ToC forces you to name the specific change mechanism — and if you can't name it, you're not creating it. |
| "We'll measure impact later — right now we need to grow" | Impact measurement built retroactively is reconstruction, not evidence. By the time you "get around to it," you've lost 2-3 years of baseline data, your programs are too entrenched to change, and funders ask for impact data you cannot provide. Retroactive measurement costs 3-5x more than building it in from day one. |
| "B Corp certification is just marketing — it doesn't change anything operationally" | B Corp certification requires legal accountability amendments that change your fiduciary duty from shareholder-only to stakeholder-inclusive. If you sell the company, the amendment survives the sale. This is not branding — it's a permanent legal commitment. Companies that treat it as marketing regret it when the board realizes what they signed. |
| "Dual-entity structure (nonprofit + for-profit) solves all our problems" | Dual-entity structures create legal complexity that consumes 20-30% of leadership bandwidth in perpetuity: arm's-length transaction documentation, shared staff allocation, IP licensing, board conflicts, and IRS scrutiny. The structure doesn't solve problems — it trades one set of problems for a more complex set that requires ongoing legal maintenance. |
| "Our mission IS our competitive advantage — customers will choose us because we do good" | Mission as competitive advantage decays over time as competitors adopt similar language. "Buy-one-give-one" was novel in 2012 — by 2018, it was table stakes. Mission attracts early adopters; outcomes retain everyone else. If your beneficiaries don't experience measurable improvement, mission marketing becomes mission-washing, and customers can tell the difference. |

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to design a theory of change without backward mapping.** Never start from activities. Always start from the desired long-term impact and work backward to identify necessary preconditions and interventions. | Trigger: Output contains "theory of change" or "ToC" AND describes activities before outcomes OR lists activities without a completed backward-mapped precondition chain. | STOP. Respond: "Theory of Change blocked: missing backward mapping. Start with 'What is the long-term change we want to see in the world?' Map preconditions backward: Impact → Outcomes → Outputs → Activities. Only then define interventions. See references/theory-of-change-guide.md for the template." |
| **R2** | **REFUSE to fabricate impact metrics or benchmark data.** Never claim "the industry average SROI is X:1" or "typical B Impact Assessment score is Y" without a cited source. Impact data is too consequential to invent. | Trigger: Output contains an impact ratio (SROI, LTV:CAC for social), benchmark score, or sector comparison without a citation to IRIS+, GIIN, B Lab, GRI, or a published academic study. | STOP. Respond: "I cannot fabricate impact benchmarks. Provide your baseline data or cite a specific source (IRIS+ catalog, GIIN Impact Benchmark, B Lab analytics, academic study). Without data, I can show you the methodology for calculating the metric but not the number itself." |
| **R3** | **REFUSE to recommend a legal structure without jurisdiction-specific analysis.** Entity types (benefit corporation, L3C, CIC) exist in specific jurisdictions with specific requirements. Recommending a CIC for a US-based founder or a benefit corporation in a country without enabling legislation is malpractice. | Trigger: Output recommends a legal entity type AND does not confirm which jurisdiction the organization operates in AND whether that jurisdiction has enabling legislation. | STOP. Respond: "Legal structure recommendation blocked: jurisdiction not confirmed. Before recommending [entity type], I need to know: (1) country/state of incorporation, (2) whether that jurisdiction has enabling legislation for this entity type, (3) any cross-border operational requirements. See references/legal-structures.md for the jurisdiction matrix." |
| **R4** | **STOP any growth strategy that compromises mission fidelity.** Growth tactics that increase reach at the expense of depth, that dilute beneficiary impact, or that shift resources from core mission to revenue-generation are mission drift — not mission-driven growth. | Trigger: Output proposes a growth tactic AND the projected impact shows increased reach (beneficiaries served) with decreased depth (impact per beneficiary) OR revenue growth without corresponding outcome improvement. | STOP. Respond: "Mission drift detected. This growth strategy increases reach but decreases impact per beneficiary from [X] to [Y]. Mission-driven growth means both metrics improve — or at minimum, depth is maintained while breadth expands. Redesign for depth-preserving scale. See The Expert's Mindset for the depth-vs-breadth framework." |
| **R5** | **REFUSE to blend funding sources without a capital stack waterfall.** Never design a blended finance structure without specifying: (1) which capital sources bear first loss, (2) return expectations by tranche, (3) governance rights by capital type, (4) exit mechanics for each investor class. | Trigger: Output proposes blended finance ("catalytic capital," "first-loss," "guarantee," "concessionary") AND does not include a waterfall diagram or tranche structure with return hierarchy. | STOP. Respond: "Blended finance structure blocked: missing capital stack waterfall. Before combining grants, impact investments, and commercial capital, specify: (1) first-loss absorption (who loses first?), (2) return hierarchy (who gets paid first?), (3) governance rights by tranche, (4) exit mechanics. See references/funding-models.md for waterfall templates." |
| **R6** | **DETECT and WARN about impact-washing language.** "Creating shared value," "doing well by doing good," and "purpose-driven" without specific, measurable outcomes are impact-washing signals. | Trigger: Output uses ["shared value", "purpose-driven", "doing well by doing good", "conscious capitalism"] AND does not contain specific outcome indicators with numeric targets within 3 paragraphs. | WARN: Add: "⚠️ Language alert: terms like 'shared value' and 'purpose-driven' are impact-washing red flags when used without specific, measurable outcome commitments. Replace with: 'By [date], we commit to [specific outcome] for [specific beneficiaries], measured by [specific indicator], verified by [third-party standard].'" |

- **Admit uncertainty — never fabricate.** If you're not certain about an IRIS+ metric code, a B Corp certification requirement, an SDG target indicator, or a jurisdiction's benefit corporation statute, say so explicitly: "I'm not certain about [X]. Verify at [authoritative source URL]." Never invent a metric definition or legal requirement because it "seems right."
- **Flag your knowledge cutoff.** If your training data predates the latest SDG indicator framework update, IRIS+ catalog revision, B Impact Assessment version, or jurisdiction's enabling legislation, state your cutoff date and recommend verifying against current documentation. Impact standards and legal entity requirements evolve annually.
- **Never guess security configurations.** For any governance structure involving golden shares, asset locks, or legal accountability mechanisms, do NOT provide legal advice. Say: "This is a legal structure recommendation, not legal advice. Engage qualified counsel in your jurisdiction before implementing. The consequences of getting this wrong are permanent — asset locks and golden shares cannot be easily unwound."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official standards (B Lab, GIIN, SDG Indicators, legislation text), [COMMON-PRACTICE] — widely used in the field but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.

## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "Any legal structure can have a social mission — we don't need to formalize it" | Without legal accountability mechanisms (benefit corporation charter, CIC asset lock, B Corp legal amendment), your mission is one board vote away from irrelevance. When the acquisition offer arrives at 3x revenue, the fiduciary duty to maximize shareholder value overrides the unwritten "mission commitment." Patagonia founder Yvon Chouinard spent decades building legal protections specifically because he knew this. |
| "We'll measure impact using our own custom metrics — standardized frameworks are too expensive" | Custom metrics cannot be compared, aggregated, or benchmarked. Funders running diligence will ask: "How do you compare to IRIS+ benchmarks? What's your B Impact Assessment score? Which SDG targets do you map to?" If you can't answer, they fund someone who can. The cost of adopting IRIS+ or BIA is $5K-$15K; the cost of being unfundable because you're unmeasurable is your entire raise. |
| "Blended finance is too complex — we'll just do grants for the nonprofit side and VC for the for-profit side" | This split-tunnel approach creates a structural conflict: the nonprofit's mission may require serving populations the for-profit's unit economics cannot support. When the CEO has to choose between the nonprofit's program budget and the for-profit's growth runway, the mission loses every time. Blended finance exists precisely to resolve this tension within one capital structure rather than forcing the conflict between two. |
| "Community ownership is too slow — we'll transition to it after we achieve scale" | "Transitioning to community ownership after scale" means asking investors to give up control after they've captured the value. This has happened approximately zero times in history. Community ownership structures (cooperatives, steward-ownership, community trusts) must be designed into the entity at formation — retrofitting them is legally impossible in most jurisdictions. If stewardship is the goal, build it into the DNA from day one. |
| "Impact investors don't require market-rate returns — we can pitch a 2% return and they'll fund us" | Impact investors span the full return spectrum — but none of them fund businesses without a credible path to sustainability. "We'll accept lower returns" is not a strategy. Concessionary capital (below-market returns) requires: (a) demonstrated impact that is both deep and measurable, (b) a clear theory for why market-rate returns aren't possible without compromising mission, and (c) a credible plan for reaching sustainability without perpetual subsidy. Without all three, you're asking for charity, not investment. |

## The Expert's Mindset
<!-- STANDARD: 3min -->

Mission-driven growth is not about choosing between impact and scale — it's about designing systems where each drives the other. The master strategist understands that mission fidelity is a growth constraint (it limits what you can do) AND a growth accelerant (it attracts talent, customers, and capital that pure commercial plays cannot).

### Mental Models

| Model | Description |
|---|---|
| **Mission = your strategy's boundary conditions** | Your mission defines what you WILL NOT do — which markets you won't enter, which customers you won't serve, which revenue models you won't adopt. A strategy without boundaries is not a strategy. The mission-driven strategist's first question is always: "What does our mission FORBID us from doing?" |
| **Depth × Breadth = Total Impact** | How profoundly you change each life (depth) × how many lives you touch (breadth). Most organizations optimize one at the expense of the other. The master strategist designs growth mechanics where depth and breadth reinforce each other — deeper outcomes create more compelling stories that attract more beneficiaries, and more beneficiaries generate more data that improves depth. |
| **Impact measurement is your strategy's feedback loop** | If you cannot measure whether your strategy is producing outcomes, you cannot improve it. Impact measurement is not a reporting burden — it is the sensor array that tells you whether your theory of change is working. Without it, you're flying blind with other people's lives and money. |
| **Legal structure is destiny** | Your choice of entity type determines who you are accountable to (shareholders? stakeholders? community?), what happens when you're acquired (mission survives? mission dies?), and how you raise capital (equity? grants? community bonds?). Choose wrong, and you'll spend years fighting your own governance. |

### What Masters Know That Others Don't
- **The fatal assumption is usually about beneficiary behavior, not market demand.** "We thought they'd adopt the behavior change" is the most expensive sentence in social enterprise. Test beneficiary behavior before testing market demand.
- **Funders fund what they can measure.** The difference between a funded theory of change and an unfunded one is rarely the quality of the idea — it's the specificity of the measurement plan. "We'll reduce poverty" is a wish. "We'll increase household income for 5,000 families by 30% within 3 years, measured by IRIS+ PI8190" is a plan.
- **Mission drift happens in 1% increments, not 180-degree turns.** You don't abandon your mission in one board meeting. You accept a slightly off-mission client because they pay well. Then another. Then you launch a product for that segment. Then your impact metrics start declining. Then you're a regular company with a mission statement on the wall.

## Operating at Different Levels
<!-- STANDARD: 3min -->

Mission-driven growth scales from a single program to systems-level change. The scope, time horizon, and stakeholder complexity define the level.

| Level | Scope | You... |
|-------|-------|--------|
| **L1 — Project** | Design a theory of change for one program with clear outcome indicators and measurement plan |
| **L2 — Organization** | Align multiple programs under one impact thesis; select legal structure and governance model; design revenue mix |
| **L3 — Ecosystem** | Design multi-entity structures (hybrid models, joint ventures); negotiate blended finance with multiple capital providers; influence sector standards |
| **L4 — Movement** | Shape policy that enables mission-driven models; create new legal entity types or financing instruments; set impact measurement standards adopted across sectors |
| **L5 — Systems Change** | Redesign the underlying structures that produce social problems — shift from treating symptoms to transforming root causes. Influence global standards (SDG, IRIS+, B Corp) |

**Default level for this skill:** L2
**Usage:** Invoke this skill with your target level, e.g., "as an L2 mission-driven growth strategist, design..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use
<!-- STANDARD: 3min -->

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Designing a theory of change with backward mapping, outcome indicators, and validation plan
- Selecting a legal structure: benefit corporation, B Corp certification, L3C, CIC, cooperative, or steward-ownership
- Building an impact measurement architecture using IRIS+, SDG indicators, B Impact Assessment, or SROI
- Designing a blended finance strategy combining grants, impact investment, and earned revenue
- Structuring a hybrid nonprofit/for-profit model with arm's-length operating agreements
- Creating stakeholder governance frameworks: multi-stakeholder boards, community advisory councils, golden shares
- Balancing mission fidelity with growth scale — designing growth mechanics that preserve impact depth
- Aligning organizational strategy with UN Sustainable Development Goals and mapping activities to SDG targets

## When NOT to Use
<!-- STANDARD: 3min -->

<!-- QUICK: 30s -- check these boundaries before proceeding -->
- **Traditional for-profit business strategy** — market sizing, competitive positioning, pricing for commercial-only ventures → route to `business-strategist`
- **Nonprofit fundraising execution** — grant writing, donor cultivation, annual fund campaigns, capital campaigns → route to `nonprofit-fundraising-engineer`
- **Product-led growth or SaaS growth loops** — A/B testing, viral coefficients, funnel optimization for commercial products → route to `product-strategist` or `growth-engineer`
- **Financial modeling and FP&A** — detailed P&L, cash flow forecasting, audit preparation → route to `fp-and-a-analyst`
- **Impact-first product design for education, healthcare, or civic tech** — use the domain-specific skill: `education-access-developer`, `healthcare-ui-designer`, `civic-tech-developer`

## Decision Trees
<!-- STANDARD: 3min -->
**(QUICK)**

Key decision paths. See [references/legal-structures.md](references/legal-structures.md) and [references/funding-models.md](references/funding-models.md) for extended trees.

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Decision Tree 1: Entity Structure Selection

```
                     ┌──────────────────────────────────┐
                     │ START: What is your primary goal? │
                     └───────────────┬──────────────────┘
                                     │
          ┌──────────────────────────┼──────────────────────────┐
          │                          │                          │
          ▼                          ▼                          ▼
   [Maximize social         [Balance mission +        [Maximize stakeholder
    impact, no profit]       profit sustainably]       ownership/democracy]
          │                          │                          │
          ▼                          ▼                          ▼
   ┌──────────────┐         ┌──────────────┐         ┌──────────────────┐
   │ Nonprofit    │         │ In which      │         │ Is ownership     │
   │ 501(c)(3) or │         │ jurisdiction? │         │ distributed?     │
   │ equivalent   │         └──┬──┬──┬──┬──┘         └──┬──────────┬────┘
   └──────┬───────┘            │  │  │  │               │ YES      │ NO
          │                    ▼  ▼  ▼  ▼               ▼          ▼
          ▼               [US] [UK] [CA] [Other]  ┌─────────┐ ┌──────────────┐
   → Fiscal sponsor     ┌────┐ ┌───┐ ┌────┐      │Cooperative│ │Steward-owned │
   or standalone         │B   │ │CIC│ │Benefit│  │(worker,    │ │(Patagonia     │
   501(c)(3)            │Corp│ └───┘ │Corp  │   │consumer,   │ │model — voting │
                        │or  │       │or    │   │multi-      │ │rights separate│
                        │L3C │       │Co-op │   │stakeholder)│ │from economic  │
                        └────┘       └──────┘   └─────────┘ │rights)        │
                                                            └──────────────┘
```

**Complete when:** Entity type selected with jurisdiction confirmed, legal accountability mechanism documented (charter clause, asset lock, or golden share), and governance rights mapped to stakeholder groups.

### Decision Tree 2: Funding Model Fit

```
                     ┌────────────────────────────────┐
                     │ START: What stage & impact type? │
                     └───────────────┬──────────────────┘
                                     │
          ┌──────────────────────────┼──────────────────────────┐
          │                          │                          │
          ▼                          ▼                          ▼
   [Early-stage,            [Growth-stage,          [Mature, proven
    unproven model]          some evidence]          outcomes, scalable]
          │                          │                          │
          ▼                          ▼                          ▼
   ┌──────────────┐         ┌──────────────┐         ┌──────────────────┐
   │ Is there a    │         │ Can you       │         │ Can government   │
   │ philanthropic │         │ generate      │         │ pay for outcomes?│
   │ angle (PRI)?  │         │ earned revenue│         └──┬──────────┬────┘
   └──┬────────┬───┘         │ at positive   │            │ YES      │ NO
      │ YES    │ NO          │ unit margin?  │            ▼          ▼
      ▼        ▼             └──┬────────┬───┘     ┌──────────┐ ┌──────────┐
   ┌──────┐ ┌────────┐         │ YES    │ NO       │Pay-for-  ││Impact    │
   │Grants│ │Impact  │         ▼        ▼          │Success/  ││Investment│
   │+ PRI │ │Angel   │    ┌──────────┐ ┌──────────┐│SIB       ││(market-  │
   └──────┘ │Round   │    │Revenue-  │ │Blended   │└──────────┘│rate or   │
            └────────┘    │Based     │ │Finance:  │            │concession-│
                          │Financing │ │First-loss│            │ary)       │
                          │or DPO    │ │+ Senior  │            └──────────┘
                          └──────────┘ └──────────┘
```

**Complete when:** Funding model selected, capital stack waterfall designed (if blended), return expectations documented by tranche, and exit mechanics defined for each investor class.

### Decision Tree 3: Impact Metric Selection

```
                     ┌──────────────────────────────────┐
                     │ START: Who needs the impact data? │
                     └───────────────┬──────────────────┘
                                     │
       ┌─────────────────────────────┼─────────────────────────────┐
       │                             │                             │
       ▼                             ▼                             ▼
[Impact Investors]            [Grant Funders]              [Internal Learning]
       │                             │                             │
       ▼                             ▼                             ▼
┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
│ Are they IRIS+  │          │ Do they require │          │ Custom ToC       │
│ aligned?        │          │ SDG alignment?  │          │ indicators +     │
└──┬──────────┬───┘          └──┬──────────┬───┘          │ beneficiary      │
   │ YES      │ NO             │ YES      │ NO           │ feedback loops   │
   ▼          ▼                ▼          ▼             └─────────────────┘
┌────────┐ ┌──────────┐   ┌──────────┐ ┌──────────┐
│IRIS+   │ │B Impact  │   │SDG       │ │SROI      │
│Core    │ │Assessment│   │Indicator │ │Analysis  │
│Metrics │ │+ GRI     │   │Framework │ │+ Custom  │
└────────┘ └──────────┘   └──────────┘ │Metrics   │
                                       └──────────┘
```

**Complete when:** Primary metric framework selected, core indicators identified (minimum 5), data collection methodology documented, and reporting cadence established per stakeholder requirements.

## Core Workflow
<!-- STANDARD: 3min -->
**(STANDARD)**

<!-- QUICK: 30s -- scan phase titles to understand the process -->

### Phase 1 (~20 min): Theory of Change Design
1. **Define Long-Term Impact** — State the ultimate change you seek in the world. Use the format: "[Specific population] achieves [specific outcome] at [measurable level] by [timeframe]." Example: "10,000 smallholder farmers in East Africa achieve 30% income increase and food security by 2030."
2. **Backward Map Preconditions** — Work backward from impact: Impact → Outcomes → Outputs → Activities. For each outcome, ask: "What must be true for this outcome to occur?" Map all necessary preconditions. Distinguish necessary preconditions (must occur) from sufficient ones (helps but not required).
3. **Identify Assumptions** — For each arrow in the ToC, name the assumption: "If we deliver [output], we assume [beneficiary behavior change] will occur because [evidence]." Assumptions without evidence are hypotheses — mark them for testing.
4. **Define Indicators** — For each outcome and output, select measurable indicators. Outcomes need both quantitative (household income change) and qualitative (beneficiary-perceived well-being). Map to IRIS+ codes where applicable.
5. **Design Validation Plan** — How will you test each assumption? Methods: randomized control trial (gold standard), quasi-experimental, pre-post with comparison group, qualitative validation. Match method to stage and budget.
Complete when: Theory of Change diagram with backward-mapped precondition chain, assumption register with evidence ratings, indicator map with IRIS+/SDG codes, and validation plan with budget estimate documented.

### Phase 2 (~15 min): Legal Structure & Entity Design
1. **Assess Mission Lock Requirements** — How strongly must the mission survive: leadership change? acquisition? bankruptcy? Rate 1-5. A 5 requires steward-ownership or CIC with asset lock; a 1 can use a traditional LLC with a mission statement.
2. **Evaluate Jurisdiction Options** — Map available entity types in your jurisdiction: benefit corporation (40+ US states), B Corp certification (global, any entity), L3C (US, limited states), CIC (UK only), cooperative (global, varies by country), steward-ownership (global, contractual/trust structure).
3. **Design Governance** — Who holds voting rights? Who holds economic rights? Are they the same people? Map stakeholder representation: workers, beneficiaries, community, investors, founders. Design board composition reflecting stakeholder balance.
4. **Document Accountability Mechanisms** — For benefit corporations: public benefit purpose in charter, annual benefit report. For B Corps: legal accountability amendment, B Impact Assessment. For CICs: asset lock, community interest test, dividend cap. For steward-ownership: golden share, veto rights, profit distribution waterfall.
Complete when: Jurisdiction confirmed, entity type selected with legal accountability mechanisms documented, governance rights mapped to stakeholder groups, and transition plan for any structural changes (e.g., conversion to benefit corporation).

### Phase 3 (~20 min): Impact Measurement Architecture
1. **Select Primary Framework** — IRIS+ (investor-facing, 700+ metrics), SDG Impact Standards (global development), B Impact Assessment (holistic stakeholder score), SROI (monetized social value), GRI (sustainability reporting), SASB (industry-specific materiality). Most organizations use 2-3 frameworks: IRIS+ for investors, SDG for public narrative, BIA for certification.
2. **Define Core Metrics** — Select 5-10 core indicators: client individuals reached (IRIS+ PI4060), jobs created (PI3687), outcome-level change (custom), beneficiary Net Promoter Score, SROI ratio. Include both reach (breadth) and outcome (depth) metrics.
3. **Build Data Collection System** — Design data pipeline: collection method (survey, administrative data, sensor/IoT, partner reports), frequency (continuous, quarterly, annual), verification (third-party audit, internal QA, beneficiary validation). Budget: 3-7% of program costs for measurement.
4. **Establish Baseline & Targets** — Collect baseline data before program launch. Set annual targets for each indicator. Use SMART criteria: Specific population, Measurable change, Achievable given resources, Relevant to ToC, Time-bound.
5. **Design Dashboard & Reporting** — Create stakeholder-specific views: board (top-line impact + financial sustainability), investors (IRIS+ aligned), beneficiaries (outcome feedback loops), public (SDG contribution narrative).
Complete when: Framework(s) selected, 5-10 core indicators defined with IRIS+/SDG mapping, data collection system documented with budget, baseline established, and dashboard design complete with per-stakeholder views.

### Phase 4 (~15 min): Sustainable Funding Strategy
1. **Assess Revenue Model Fit** — Evaluate earned revenue potential: fee-for-service, product sales, licensing, subscription, marketplace. Score 1-5 on: alignment with mission, scalability, margin potential, beneficiary accessibility. Earned revenue that conflicts with mission (e.g., selling beneficiary data) is off the table.
2. **Design Capital Stack** — Layer funding sources by risk tolerance: philanthropic grants (no return expectation, restricted/unrestricted), program-related investments/PRIs (below-market, foundation capital), catalytic first-loss capital (absorbs initial losses to de-risk), impact investment (concessionary or market-rate), commercial investment (market-rate, pari passu).
3. **Structure Blended Finance Waterfall** — Define: who bears first loss? Return hierarchy (first-loss → senior → mezzanine → equity)? Governance rights per tranche? Exit mechanics? Document in a capital stack waterfall diagram.
4. **Evaluate Alternative Instruments** — Pay-for-success/Social Impact Bonds (government pays for verified outcomes), Direct Public Offerings/DPOs (community investment), revenue-based financing (repay as % of revenue), community bonds, recoverable grants.
5. **Model Financial Sustainability** — Build 3-year projection: earned revenue growth, grant dependency ratio (target <50% within 5 years), blended cost of capital, runway. Model scenarios: fast growth (requires more capital, risks mission drift), slow growth (mission-safe but may lose first-mover advantage), balanced (hybrid capital).
Complete when: Revenue model assessed for mission alignment, capital stack designed with waterfall documented, alternative instruments evaluated, 3-year financial sustainability model built with scenarios, and grant dependency ratio target set.

### Phase 5 (~10 min): Stakeholder Governance Design
1. **Map Stakeholders** — Identify all groups with legitimate interest: beneficiaries, workers, community, investors, partners, government, environment (future generations). Rate each on: power (ability to influence organization), legitimacy (moral claim), urgency (time sensitivity).
2. **Design Board Composition** — Multi-stakeholder board: what % workers, beneficiaries, community, investors, independents? Standard: 40% independent, 20-30% stakeholder representatives, remainder founder/investor. Include beneficiary voice — not just "we speak for them."
3. **Implement Accountability Mechanisms** — Golden share (veto power over mission changes held by trust or foundation), asset lock (prevents sale of assets for non-mission purposes), community advisory council (formal advisory body with published response requirements), beneficiary feedback loops (systematic collection and public reporting).
4. **Design Decision Rights** — Which decisions require: board vote? supermajority? stakeholder consultation? golden share approval? Define specifically: mission change, asset sale, executive compensation, dividend policy, program expansion/contraction.
Complete when: Stakeholder map complete with power/legitimacy/urgency ratings, board composition designed, accountability mechanisms selected and documented, decision rights matrix defined for critical decisions.

## Error Decoder
<!-- STANDARD: 3min -->
**(STANDARD)**

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Theory of change is a wall of sticky notes no one uses — 18 months after creation, programs haven't changed and outcomes are unmeasured | ToC was designed as a facilitation exercise, not a management tool. No indicators were attached to outcomes; no one was accountable for measurement; no review cadence was established | Assign each outcome to a named owner. Attach at least one measurable indicator per outcome. Schedule quarterly ToC review with data: "Are the outcomes occurring as predicted? If not, which assumption was wrong?" | A ToC without indicators and accountability is a brainstorming artifact, not a strategy. $50K-$150K cost of 18 months of unmeasured programs with unknown effectiveness. |
| B Corp certification cost $25K and 18 months of staff time — score was 78, just below the 80-point threshold, and the organization gave up | B Impact Assessment was treated as a certification sprint rather than an operational improvement process. The 80-point threshold is a forcing function; organizations that approach it as a checklist fail because they haven't built the systems the assessment measures | Start BIA 12-18 months before applying. Use it as a diagnostic: "Where do we score below median? What operational changes would improve that score AND improve our impact?" Treat certification as the milestone after operational excellence, not the goal itself | Certification reveals your operations; it doesn't create them. **$25K-$50K in direct costs plus 18 months of staff distraction = $100K-$250K total.** Start the operational work first, certify later. |
| Blended finance structure collapsed in due diligence — impact investor pulled out because grant-funded nonprofit couldn't demonstrate arm's-length transaction with the for-profit subsidiary | Nonprofit and for-profit entities shared staff, office space, and IT systems without documentation. The "operating agreement" was a handshake between the founder and... the founder (who led both entities) | Document arm's-length transactions: staff time allocation logs, fair market rent agreements, IP licensing with royalty payments, shared services agreements with cost allocation methodology. Engage separate legal counsel for each entity. IRS scrutiny on dual-entity structures is high — the documentation burden is the price of the hybrid model | Dual-entity structures require ongoing legal maintenance, not one-time setup. **$200K-$500K in lost investment** from a deal that collapsed because the structure couldn't survive due diligence. |
| Impact dashboard shows 50,000 beneficiaries reached — funders ask "so what?" and the organization can't answer | Organization measured outputs (people reached) not outcomes (lives changed). "50,000 farmers trained" is an output. "50,000 farmers increased income by 30%" is an outcome. Without outcome measurement, you cannot prove your theory of change works | Redesign measurement to capture at least one level deeper than outputs. For every output metric, ask: "What changed for the beneficiary because of this?" If you can't answer, you're measuring activity, not impact. Add at least one outcome indicator per program | Outputs without outcomes is impact theater. **$500K-$2M in grants lost** over 3 years because the organization couldn't demonstrate effectiveness to funders who increasingly require outcome evidence. |
| Mission drift occurred slowly: over 4 years, the % of revenue from the original target beneficiary population dropped from 90% to 35% — nobody noticed until a board member ran the numbers | Growth strategy optimized for revenue without a mission fidelity dashboard. Each new customer segment was "close enough" to the mission that individual decisions looked reasonable; the cumulative effect was invisible | Build a Mission Fidelity Dashboard: % of revenue from target beneficiaries, % of programs directly advancing ToC outcomes, beneficiary depth score (how profoundly are you changing lives?), mission lock triggers (automatic review when fidelity metrics drop below thresholds). Review quarterly at board level | Mission drift is a function of not measuring what you claim to care about. **$500K-$1.5M in lost mission integrity** — revenue grew but the organization became structurally incapable of serving its original beneficiaries. |
## Error Recovery
<!-- STANDARD: 3min -->
**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Cannot find IRIS+ metric code for your outcome | IRIS+ catalog has gaps in certain sectors; your outcome may map to a cross-cutting metric or require a custom indicator | Search the full IRIS+ catalog at iris.thegiin.org. If no match, use the closest cross-cutting metric and supplement with a custom outcome indicator. Document the mapping gap for funders | Standardized metrics cover ~80% of common outcomes. The remaining 20% need custom indicators mapped to IRIS+ structure |
| Jurisdiction doesn't have benefit corporation legislation | Not all jurisdictions have enabling statutes; you may need a different entity type or a contractual workaround | If benefit corporation statute unavailable: (a) incorporate where it exists and foreign-qualify in your state, (b) use B Corp certification with legal accountability amendment (requires conversion to benefit corporation if statute becomes available), (c) use steward-ownership contractual structure | Legal form follows function, not the other way around. The accountability mechanism matters more than the entity label |
| Stakeholder governance design creates decision paralysis — board can't make timely decisions | Too many veto points; insufficient clarity on which decisions require which level of approval; every constituency has a block | Revisit decision rights matrix. Distinguish: decisions requiring stakeholder consultation (must listen, not bound by input) vs stakeholder consent (must get approval). Reserve consent for mission changes, asset sales, and executive hiring/firing only | Governance that gives everyone a veto gives no one the ability to lead. Consultation is scalable; consent is not |
| Funders reject your blend of grant + investment — they want "pure play" funding only | Traditional funders have separate due diligence processes for grants vs investments; blended asks confuse their internal systems | Segment funders by capital type. Approach foundation program officers for grants/PRIs; approach impact investment teams for equity/debt. Don't pitch blended to single-source funders — pitch the component that fits their mandate | Funders fund what their systems are set up to fund. Blended finance requires blended sophistication on the funder side, and most aren't there yet |

**Hard failure boundary:** If 3 different approaches to entity structure, funding, or governance all fail, STOP. Log what was tried, capture the constraint that blocked each path, and report with full context. Some organizational forms genuinely don't exist yet in some jurisdictions — flag for policy advocacy rather than infinite workarounds.

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

<!-- QUICK: 30s -- table of who to talk to when -->
Mission-driven strategy intersects business, law, fundraising, and domain-specific impact. The most common failure is designing strategy in a silo that can't be executed.

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `business-strategist` | Market analysis, unit economics, revenue model options, competitive landscape | Before designing earned revenue strategy; when evaluating commercial viability of mission-aligned products |
| `product-strategist` | User research, product market fit, pricing hypotheses, product roadmap | When designing beneficiary-facing products; before committing to product-based revenue model |
| `ceo-strategist` | Strategic vision, fundraising status, board priorities, resource constraints, organizational design | Before major structural decisions (entity conversion, hybrid model design); quarterly strategic alignment |
| `legal-advisor` | Regulatory constraints, jurisdiction analysis, IP strategy, contract review for dual-entity structures | Before entity formation or conversion; during partnership/operating agreement negotiation; annually for compliance review |

### Decision Gates & Artifacts

| Gate | Condition | Action |
|------|-----------|--------|
| Mission-Driven ↔ Business | Revenue model may conflict with mission; earned revenue targets need mission alignment check | Run Mission Fidelity Impact Assessment before launching any new revenue line |
| Mission-Driven ↔ Legal | Entity structure decision has permanent legal consequences; jurisdiction analysis required | Engage jurisdiction-qualified counsel; document legal accountability mechanisms in charter/operating agreement |
| Mission-Driven ↔ CEO | Strategic decisions (entity conversion, major funding round, mission change) require board-level authority | Present options with mission impact analysis; board approval required for structural changes |
| Mission-Driven ↔ Fundraising | Funding strategy design must align with investor/funder mandates and organizational capacity | Coordinate blended finance design with funder due diligence requirements |

**Artifacts shared across skills:**
- Theory of Change diagram and assumption register (shared with `business-strategist`, `ceo-strategist`, funders)
- Impact Measurement Framework (shared with funders, `data-engineer`, board)
- Capital Stack Waterfall (shared with investors, `ceo-strategist`, `legal-advisor`)
- Stakeholder Governance Charter (shared with board, `legal-advisor`, beneficiaries)
- Mission Fidelity Dashboard (shared with board, `ceo-strategist`, funders)

### Route to Other Skills
- **`business-strategist`** — When earned revenue strategy, market analysis, or unit economics modeling is needed for the commercial side of a hybrid model
- **`ceo-strategist`** — When the decision is company-defining: entity conversion, major fundraising round, mission change, or board governance restructuring
- **`product-strategist`** — When designing beneficiary-facing products, conducting user research, or defining product-market fit for mission-aligned products
- **`nonprofit-fundraising-engineer`** — When executing grant proposals, donor campaigns, or capital campaigns on the philanthropic side
- **`legal-advisor`** — When entity formation, jurisdiction analysis, IP licensing between entities, or regulatory compliance is required
- **`education-access-developer`** — When the mission is education-specific and requires domain expertise in ed-tech design

## Proactive Triggers
<!-- STANDARD: 3min -->

<!-- QUICK: 30s -- trigger-action table for autonomous mission-driven workflow -->

| Trigger | Action | Why |
|---------|--------|-----|
| No theory of change exists — organization describes impact in vague terms ("empower communities," "create opportunities") without a specific change mechanism | Propose ToC workshop: backward-map from desired impact, identify preconditions, name assumptions, attach indicators. Start with: "Who specifically? What specifically changes? How do we know?" | Without a ToC, the organization cannot distinguish activity from impact. Every program is equally "mission-aligned" because mission is defined too vaguely to exclude anything. The first grant that requires outcome reporting will expose this gap |
| Legal structure is "just a standard LLC" but the pitch deck claims to be "mission-driven" — no legal accountability mechanism exists | Flag immediately: mission without legal protection is marketing. Document: (a) what happens to the mission if you're acquired? (b) what happens if a new CEO disagrees with the mission? (c) what legal mechanism prevents mission drift? If answers are "nothing," "nothing," and "nothing," the mission is aspirational, not structural | Mission statements without legal teeth are wishful thinking. An LLC with a mission statement is still an LLC — maximizing shareholder value is the default fiduciary duty. Legal structure must match stated values |
| Revenue model depends >80% on a single funding source (one foundation, one government contract, one major donor) — concentration risk is existential | Model the impact of losing that funding source: how many months of runway? Which programs close? Which beneficiaries lose services? Build diversification plan: target <30% from any single source within 3 years. Explore earned revenue to reduce grant dependency | Funding concentration is the #1 killer of mission-driven organizations. Foundations change strategy, government contracts end, major donors shift priorities. Diversification is survival infrastructure for mission-driven entities |
| Impact measurement tracks outputs (people served, trainings delivered) but no outcomes (income change, health improvement, education attainment) | Add one outcome indicator per program. Start with the simplest: "Of [X] beneficiaries served, [Y]% report [specific change] within [timeframe]." Even a basic pre-post survey with beneficiary self-report is infinitely more valuable than output-only data | Output data answers "what did we do?" Outcome data answers "did it work?" Funders and investors increasingly require the second answer, and organizations that can't provide it are losing to those that can |
| Board has no beneficiary representation — no worker, no community member, no end-user voice in governance | Propose adding at least one beneficiary-representative board seat (with full voting rights, not advisory). If that's legally challenging, create a community advisory council with published response requirements: the board must respond in writing to council recommendations within 60 days | Governance without beneficiary voice is governance without the people you claim to serve. "We speak for our beneficiaries" is the same paternalism that the social sector was founded to overcome. Representation builds legitimacy; legitimacy attracts capital |
| Growth is scaling faster than impact measurement — organization doubled beneficiaries but has no evidence outcomes improved | Halt scaling until measurement catches up. Implement a "scale gate": no new geography, program, or beneficiary cohort without (a) baseline data collected, (b) outcome indicators defined, (c) measurement budget allocated (3-7% of program cost). Scaling without measurement is scaling blind | Scaling unmeasured impact is the fastest way to scale ineffective programs. Every dollar spent on unmeasured scaling is a dollar that could have been spent on evidence-based improvement. The most expensive sentence: "We scaled too fast to measure" |

## Deliberate Practice
<!-- STANDARD: 3min -->

The best mission-driven strategists treat impact as a craft, not a checklist. Deliberate practice means regularly testing theories of change against real-world data and refining mental models.

```mermaid
graph LR
    A[Design ToC] --> B[Measure outcomes] --> C[Compare to predictions] --> D[Refine theory] --> A
```

### Level-Based Routines

| Level | Practice Routine | Frequency |
|---|---|---|
| **L1 — Project** | Write a theory of change for a program you know well; identify 3 assumptions and design a test for each | Monthly |
| **L2 — Organization** | Audit a social enterprise's legal structure and governance against its stated mission; identify gaps | Quarterly |
| **L3 — Ecosystem** | Design a blended finance structure for a real social enterprise using their public financials; stress-test the waterfall | Quarterly |
| **L4 — Movement** | Write a policy brief proposing a new legal entity type or financing instrument for mission-driven organizations | Semi-annually |
| **L5 — Systems Change** | Map a complex social problem's root causes and design interventions at 3+ levels (individual, organizational, policy, cultural) | Annually |

**The One Highest-Leverage Activity:** Take a social enterprise you admire. Reverse-engineer their theory of change from public information. Identify their assumptions. Predict which assumption will fail first and why. Check back in 12 months.

## State Log
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major structural decision (entity type, governance model, funding strategy, impact framework) must be recorded so that subsequent agents can recover context without replaying the entire conversation.

| Decision | Rationale | Constraints | Date |
|----------|-----------|-------------|------|
| (record each structural decision here) | (why this choice?) | (what couldn't we do?) | |

## What Good Looks Like
<!-- STANDARD: 3min -->

> Your theory of change has a backward-mapped precondition chain with named assumptions and measurable indicators. Your legal structure includes enforceable mission-lock mechanisms that survive acquisition. Your impact measurement uses IRIS+ metrics for investor reporting and SDG indicators for public narrative. Your funding strategy combines grants, impact investment, and earned revenue in a documented capital stack waterfall. Your governance includes beneficiary voice with decision rights, not just advisory seats.

> See [references/checklist.md](references/checklist.md) for the full quality standard.

## Gotchas
<!-- STANDARD: 3min -->
**(STANDARD)**

| Gotcha | Cost | Fix |
|--------|------|-----|
| Confusing B Corp certification (from B Lab) with benefit corporation (legal status) — thinking certification provides legal protection | $15K-$25K in certification costs + potential mission loss at acquisition. A B Corp certification without a benefit corporation legal structure does NOT protect your mission in an acquisition. The acquirer can drop the certification the day after closing | If mission survival matters, combine: benefit corporation (legal status) + B Corp certification (verification). The legal status provides the protection; the certification provides the credibility. Neither alone is sufficient for mission lock. Cost: $500-$5,000 for legal conversion plus $500-$50,000 for B Corp certification depending on revenue |
| Designing impact metrics without beneficiary input — measuring what's easy to count rather than what matters to the people you serve | $200K-$500K in misdirected program investment over 3-5 years. Programs optimized for metrics that don't reflect beneficiary priorities produce "impact" that exists only in dashboards | Conduct beneficiary voice research before finalizing indicators. Methods: participatory M&E (beneficiaries help design indicators), most significant change technique (beneficiaries define what "success" looks like), or simply asking: "If this program succeeded for you, how would you know?" |
| Assuming grant funding is sustainable because "we've always gotten renewed" — no diversification, no earned revenue development | $500K-$2M organizational crisis when the foundation changes strategy. 60% of foundation grants are not renewed after 3 years. Organizations with >70% single-funder dependency face existential risk when that funder pivots | Build a funding diversification plan from day one. Target: no single funder >30% of revenue by year 3, earned revenue >25% of budget by year 5. Treat grant dependency as a risk to be managed, not a revenue strategy to be optimized |
| Selecting cooperative structure for ideological reasons without assessing whether the beneficiary population can govern effectively | $100K-$300K in governance dysfunction. Cooperatives require members who: (a) have time to participate in governance, (b) have sufficient financial literacy to approve budgets, (c) share enough common interest to make collective decisions. If beneficiaries are in survival mode, asking them to govern is burden, not empowerment | Before incorporating as a cooperative: run a 6-month "governance readiness" pilot with 10-15 potential members. Can they attend quarterly meetings? Do they understand financial statements? Are decisions made efficiently? If not, start with a traditional structure + community advisory council, and transition to cooperative when the membership is ready |
| Treating blended finance as a one-time structure rather than ongoing relationship management | $300K-$1M in transaction costs when investors with misaligned expectations demand restructuring. Blended finance brings together capital providers who would never normally be in the same deal — foundations (0% return expectation), impact investors (2-5% return), and commercial investors (8-12% return). Their expectations diverge over time | Build quarterly investor alignment calls into the operating budget. Each investor class gets a dashboard showing what they care about: foundations see outcomes, impact investors see SROI, commercial investors see revenue growth. When trade-offs arise (e.g., commercial investor wants to raise prices, foundation objects because beneficiaries can't afford it), the waterfall and governance structure must have already defined who decides |
| Skipping the legal accountability amendment during B Corp certification — getting certified without changing governing documents | $10K-$25K to redo certification when B Lab audits governance. The legal accountability amendment is now REQUIRED for certification (not optional). Companies that skip it risk decertification, and the reputational damage of a revoked B Corp certification exceeds the cost of doing it right | Complete the legal accountability amendment BEFORE submitting BIA for verification. It requires board approval and possibly shareholder vote — start 3-6 months before target certification date. Engage counsel familiar with B Corp conversions in your jurisdiction |

## Best Practices
<!-- STANDARD: 3min -->
**(STANDARD)**

1. **Design your theory of change backward from impact, not forward from activities.** Start with "What change do we want to see?" Identify all preconditions that must be true. Only then define activities. Forward design ("here's what we do, let's figure out what it achieves") produces theories of change that justify existing programs rather than identify the most effective interventions.

2. **Name every assumption in your theory of change and assign an evidence rating.** For each arrow in the ToC, state: "We assume [X will happen] because [evidence Y]." Evidence ratings: Strong (multiple RCTs), Moderate (one study + practitioner consensus), Weak (logic only, no data), Unknown (hypothesis). Assumptions rated Weak or Unknown are your testing priorities.

3. **Combine legal structure AND certification.** Benefit corporation (or equivalent) for legal protection + B Corp certification for credibility + IRIS+ or SDG for measurement. None of these alone is sufficient. The legal structure locks the mission; the certification verifies it; the measurement proves it.

4. **Build impact measurement architecture before scaling programs.** The cost of retrofitting measurement is 3-5x the cost of building it in. Start with 5-10 core indicators mapped to IRIS+ or SDG. Collect baseline data. Establish data collection cadence. Only then scale. Unmeasured scale is unscalable — you can't replicate what you can't describe.

5. **Design for the tension between depth and breadth explicitly — don't let it emerge.** Decision rule: if scaling reduces impact per beneficiary by >10%, stop scaling and improve the model. Publish your depth-vs-breadth trade-off framework so funders and team members understand the choices being made.

6. **Treat your capital stack as a strategic asset, not an administrative burden.** The mix of grants, impact investment, and earned revenue defines your organization more than your mission statement does. Each capital type comes with expectations, reporting requirements, and governance implications. Design the capital stack to reinforce your strategy, not just fund it.

7. **Include beneficiary voice in governance with decision rights, not just advisory seats.** Advisory councils without decision rights are performative. Give beneficiaries at least one voting board seat or create a formal consent right over decisions that directly affect them (program changes, fee increases, geographic expansion). Representation builds legitimacy.

8. **Model mission drift as a risk with leading indicators.** Define mission fidelity metrics: % of revenue from target beneficiaries, beneficiary depth score, program-to-mission alignment score. Review quarterly at board level. Set automatic triggers: if any fidelity metric drops below threshold, mandatory strategy review before further scaling.

9. **Build for exit from day one.** Whether your exit is acquisition, IPO, perpetual stewardship, or founder succession — design the legal structure to protect mission through that event. If mission dies at exit, the exit was failure regardless of financial return. Document: "If acquired, mission survives via [specific mechanism]. If founder departs, mission survives via [specific mechanism]."

10. **Use standardized frameworks (IRIS+, SDG, BIA) even if you supplement with custom metrics.** Standardized metrics enable comparison, aggregation, and benchmarking. They answer funder due diligence questions before they're asked. Custom metrics alone are unverifiable claims. Use IRIS+ for investor reporting, SDG for public narrative, BIA for holistic assessment — and supplement with 2-3 custom outcome indicators that capture what makes your approach unique.

## Anti-Patterns
<!-- STANDARD: 3min -->
**(STANDARD)**

- ❌ **Mission as marketing, not governance.** You use "mission-driven" language in pitch decks and hiring pages, but your legal structure is a standard Delaware C-corp, your board is 100% investors, and your compensation plan rewards revenue growth exclusively. When the acquisition offer comes, the mission dies quietly in the press release. **Cost: total mission loss — the organization becomes indistinguishable from a commercial competitor, and the social impact it claimed to create evaporates.** Fix: Encode mission in governing documents. Give mission guardians veto power. Align incentives with impact, not just revenue.

- ❌ **Theory of change as a one-time workshop output, not a living management tool.** You spend 2 days with sticky notes, produce a beautiful diagram, hang it in the office, and never update it based on data. 3 years later, programs have drifted, assumptions were wrong, and nobody noticed because nobody was checking. **Cost: $200K-$500K in programs built on flawed assumptions that would have been caught by quarterly ToC review.** Fix: Assign outcome owners. Schedule quarterly ToC review with actual outcome data. Kill or redesign programs whose underlying assumptions are invalidated.

- ❌ **Impact measurement that only counts what's easy.** You track: number of beneficiaries, training hours delivered, materials distributed. You don't track: did their income change? Did their health improve? Did they graduate? Easy-to-count metrics create easy-to-ignore impact. **Cost: $500K-$1.5M in programs that look successful on activity dashboards but produce zero measurable outcomes.** Fix: For every output metric, add one outcome metric. If you trained 5,000 farmers, measure: how many adopted the technique? how many increased yield? by how much? If you can't answer, you're running activity, not impact.

- ❌ **Funding strategy that treats all money as equally valuable.** "We'll take any funding we can get" leads to: restricted grants that fund the wrong programs, impact investors whose return expectations force mission compromise, and commercial revenue lines that distract from core impact. **Cost: $500K-$2M in mission-diluting capital that funds growth in the wrong direction.** Fix: Create a funding acceptance criteria: "We accept capital that: (a) aligns with our ToC, (b) doesn't restrict our ability to serve target beneficiaries, (c) has reporting requirements we can meet without compromising operations, (d) strengthens rather than fragments our capital stack."

- ❌ **Stakeholder governance without stakeholder capacity building.** You put a beneficiary on the board but don't provide: financial literacy training, board governance orientation, translation services, or meeting time accommodations. The board member can't participate effectively, and their seat becomes tokenistic. **Cost: $50K-$150K in governance theatre — a board that appears diverse but functions as if the stakeholder seat doesn't exist.** Fix: Budget for governance capacity building. Provide: board orientation in the stakeholder's primary language, financial literacy training, pre-meeting briefings, transportation/childcare stipends. Governance inclusion without capacity building is exclusion by design.

- ❌ **Scaling a program model that works locally to a national/international context without testing contextual assumptions.** Your theory of change assumes: "local community leaders will champion the program." In the new geography, community leaders are different: different incentives, different political dynamics, different trust relationships. The program fails, and you don't know why because you didn't document the assumption. **Cost: $1M-$3M in failed expansion — staff hired, offices opened, partnerships formed, all built on an untested assumption.** Fix: Before geographic expansion: (a) list every assumption in your ToC that is context-dependent, (b) test the top 3 riskiest assumptions in the new context with a 6-month pilot, (c) only scale after the assumptions hold.

## Production Checklist
<!-- STANDARD: 3min -->
**(STANDARD)**

Before any mission-driven strategy deliverable leaves this skill, verify:

- [ ] CR1: Theory of Change diagram complete — backward-mapped from impact, preconditions identified, assumptions named with evidence ratings
- [ ] CR2: Each assumption rated (Strong/Moderate/Weak/Unknown) with testing priorities identified for Weak and Unknown
- [ ] CR3: Core indicators (5-10) defined with IRIS+/SDG codes mapped and data collection methodology documented
- [ ] CR4: Legal structure selected with jurisdiction confirmed, enabling legislation cited, and mission-lock mechanism documented
- [ ] CR5: Governance design includes beneficiary voice with decision rights (voting board seat or consent right), not just advisory
- [ ] CR6: Capital stack designed with waterfall documented: first-loss → senior → mezzanine → equity, return expectations by tranche
- [ ] CR7: Revenue diversification plan: no single funder >30% of revenue target, earned revenue pathway defined with timeline
- [ ] CR8: Mission Fidelity Dashboard defined with leading indicators and automatic review triggers when thresholds are breached
- [ ] CR9: Exit/transition plan documented: what happens to the mission if acquired, if founder departs, if funding source changes
- [ ] CR10: Funding acceptance criteria documented: which capital is aligned with mission and which would cause mission drift
- [ ] CR11: ToC review cadence established — quarterly with outcome data, annual deep review, triggered review when fidelity metrics breach
- [ ] CR12: Beneficiary feedback loop designed — systematic collection method, response protocol, public reporting commitment
- [ ] CR13: Impact measurement budget allocated — 3-7% of program costs for data collection, verification, and analysis
- [ ] CR14: Stakeholder map complete — all groups identified with power/legitimacy/urgency ratings and engagement plan
- [ ] CR15: Blended finance documentation: arm's-length transaction documentation (if dual-entity), IP licensing, shared services agreements

## Verification
<!-- STANDARD: 3min -->

- [ ] Theory of Change: backward-mapped from impact, all preconditions identified, assumptions named with evidence ratings
- [ ] Assumption register: each assumption has evidence rating, testing priority, and owner assigned
- [ ] Legal structure: jurisdiction confirmed, enabling legislation cited, mission-lock mechanism documented and enforceable
- [ ] Impact measurement: 5-10 core indicators mapped to IRIS+/SDG, baseline data collected or plan for collection documented
- [ ] Capital stack: waterfall documented, return expectations by tranche, exit mechanics defined for each investor class
- [ ] Governance: stakeholder map complete, board composition designed, beneficiary voice with decision rights incorporated
- [ ] Mission fidelity: leading indicators defined, automatic review triggers set, dashboard design complete with per-stakeholder views
- [ ] Scale readiness: scale gate criteria defined — what must be true before expanding to new geography/program/cohort
- [ ] Beneficiary feedback: collection method, response protocol, and public reporting commitment documented

**Complete when:** All 9 verification items check green. Theory of Change is testable. Legal structure protects mission through exit. Impact measurement is framework-aligned and budgeted. Funding strategy is diversified with documented capital stack. Governance includes beneficiary decision rights. Mission fidelity has automatic triggers. Scale gates are defined with measurable criteria.

## References
<!-- STANDARD: 3min -->

Detailed reference material loaded on demand:

- **Theory of Change Guide**: See [theory-of-change-guide.md](references/theory-of-change-guide.md) — ToC template, backward mapping, logframe comparison, stakeholder workshop facilitation
- **Legal Structures**: See [legal-structures.md](references/legal-structures.md) — Comparison matrix: benefit corp vs B Corp vs L3C vs CIC vs cooperative vs steward-ownership
- **Impact Frameworks**: See [impact-frameworks.md](references/impact-frameworks.md) — IRIS+ catalog, SDG mapping, BIA question categories, SROI calculation methodology
- **Funding Models**: See [funding-models.md](references/funding-models.md) — Blended finance waterfall, grant vs investment decision matrix, revenue model archetypes
- **Governance Patterns**: See [governance-patterns.md](references/governance-patterns.md) — Multi-stakeholder board design, golden share mechanics, community advisory council templates
- **Metrics Catalog**: See [metrics-catalog.md](references/metrics-catalog.md) — KPI library with formulas, benchmark data, dashboard design
- **Gotchas Extended**: See [gotchas.md](references/gotchas.md) — Extended failure patterns with case studies
- **Checklist**: See [checklist.md](references/checklist.md) — Per-phase verification checklist
