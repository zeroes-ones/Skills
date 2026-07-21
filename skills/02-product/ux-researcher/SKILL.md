---
name: ux-researcher
description: "Generate personas, map user journeys, design usability tests, synthesize research findings, run competitive UX analysis, and perform heuristic evaluations. Use to inform design and product decisions with user evidence. Triggered by create personas, journey map, usability test plan, research synthesis, competitive analysis, heuristic evaluation, user research."
author: Sandeep Kumar Penchala
type: product
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - ux-researcher
token_budget: 2400
output:
  type: "code"
  path_hint: "./"
---
# UX Researcher

Generate evidence-based user understanding that drives product and design decisions. Move teams from opinion-based to insight-based development through rigorous qualitative and quantitative research methods.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Understand users (personas, journey maps, mental models) → Jump to "Core Workflow" — Phase 2 & 3
├── Test usability of a design or prototype → Jump to "Core Workflow" — Phase 4 (Usability Testing)
├── Run a survey or gather quantitative feedback → Go to "Decision Trees" — choose qual vs quant method
├── Perform competitive UX audit or benchmarking → Jump to "Sub-Skills" — competitive-ux-benchmarking
├── Synthesize scattered research into a findings report → Jump to "Core Workflow" — Phase 5 (Synthesis & Reporting)
├── Need design recommendations from research → Invoke ui-ux-designer skill instead
└── Not sure? → Describe the problem in plain language and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never report findings without sample size and methodology.** Every insight must state: how many participants, what method, and when the study was conducted. Do: "4 of 5 participants (moderated usability test, June 2026) failed to locate the settings menu." Don't: "Users can't find settings."
- **Persona details must come from research, not assumptions.** Personas without at least 3 real-user interviews are archetypes, not personas — label them accordingly. Do: "Based on 8 interviews with oncology nurses..." Don't: "Our primary persona is Busy Brenda, a working mom."
- **Don't recommend without testing.** Design recommendations must trace to observed behavior (task failure, quote, heatmap, analytics). Do: "Recommend repositioning the CTA because 4/5 participants scrolled past it (video timestamps: 3:12, 5:47, 8:03, 11:22)." Don't: "The CTA should be more prominent."
- **Always triangulate findings across methods.** Never make a product decision based on one research method alone — confirm with at least two data sources.
- **Admit what you don't know.** If recruitment is incomplete, sample size is below threshold, or a demographic segment is missing, say so and tell the user to run additional studies or consult the analytics team.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- A product lacks validated personas and the team builds for themselves
- You need to understand the end-to-end user journey across touchpoints
- Before a major redesign — baseline usability with a heuristic evaluation
- Competitor products have features you're considering — benchmark their UX
- User feedback is scattered across support tickets, interviews, and analytics — needs synthesis
- A feature is high-risk and needs moderated usability testing before launch

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Research Method Selection

```
What stage of the product lifecycle?
├── Discovery (exploring problem space) → Semi-structured interviews + diary studies
│     Goal: Understand mental models, pain points, unmet needs
├── Design (validating solutions) → Moderated usability tests + concept testing
│     Goal: Find interaction flaws, validate design direction
├── Development (refining implementation) → Unmoderated usability tests + A/B tests
│     Goal: Statistical confidence, comparative analysis
└── Post-launch (optimizing) → Surveys + analytics + support ticket analysis
      Goal: Measure satisfaction, identify friction, prioritize fixes

Sample size decision?
├── Qualitative (interviews, moderated tests) → 5 participants per segment
│     Rationale: 5 users uncover ~85% of usability issues (Nielsen)
├── Quantitative (surveys, unmoderated tests) → 30+ participants per segment
└── Mixed methods → 5-8 qual + 30-50 quant. Triangulate findings.
```


**What good looks like:** Research plan with falsifiable hypotheses. 5+ user interviews completed with transcripts and recordings. Findings synthesized into 3-5 key insights with direct quotes. Recommendations linked to specific design decisions.

### When NOT to Do Formal Research

- One-day design tweak? → Skip. Ship and monitor analytics.
- "Should we change this button color?" → A/B test. No research needed.
- You have < 10 users? → Talk to all of them directly. Formal methods add no value.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Research Planning
Define the research objective in one sentence. Identify the key research questions (3–5 max). Choose the method: moderated usability test for interaction flow, unmoderated for volume/statistical significance, semi-structured interview for mental models, diary study for longitudinal behavior, survey for attitudes/preferences. Recruit participants: 5 per persona segment for qualitative, 30+ per segment for quantitative. Draft a discussion guide or test script with timestamps. Prepare consent forms, recording setups, and note-taking templates (split observer and facilitator roles).

### Phase 2 (~30 min): Persona Generation
Build personas from behavioral data, not demographics. For each persona: name, archetype label, primary goal, core tasks (3–5), pain points, current tools/workarounds, context of use (environment, device, time pressure), and a representative quote. Map each persona to a Jobs-to-be-Done (JTBD): "When [situation], I want to [motivation], so I can [outcome]." Create an empathy map for the top 2 personas: Says, Thinks, Does, Feels. Validate personas with at least 3 real users matching the profile before distributing.

### Phase 3 (~20 min): Journey Mapping
Map the end-to-end experience across time, channel, and emotional state. For each step in the journey: user action, touchpoint/channel, emotion (high/low), pain points, and opportunities. Identify the "moments of truth" — steps where satisfaction or abandonment is determined. Overlay the frontstage (user-visible) and backstage (system/internal) actions per step. Annotate with quantitative data where available: drop-off rates, time-on-step, support ticket volume per step.

### Phase 4 (~15 min): Usability Testing
Create task scenarios that are realistic, specific, and avoid leading language. For each task: define the success criteria (completion rate, time-on-task, error count), the maximum acceptable error rate, and the benchmark. Run a dry-run with one participant before the actual sessions. During testing: think-aloud protocol, minimal intervention, note severity of each observed issue (1 = cosmetic, 2 = minor, 3 = major blocker, 4 = catastrophic). Debrief after each session while memory is fresh. Aggregate findings in a rainbow spreadsheet: row per participant, column per issue, color-coded by severity.

### Phase 5 (~25 min): Synthesis & Reporting
Cluster observations into themes using affinity diagramming. For each theme: state the insight, the evidence (quotes, clips, metrics), the severity/impact, and a design recommendation. Structure the final report as: Executive Summary, Methodology, Key Insights (top 3), Detailed Findings (by theme), Recommendations (prioritized), Appendix (raw data, session recordings, recruitment screener). Socialize findings with a highlights reel (3 minutes max) before the written report — stakeholders consume video faster than documents.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
UX research findings are useless if they don't change what gets built. Coordination ensures insights flow from research into design, product, and engineering — not into a PDF that nobody reads.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Product Strategist / Product Manager** | Study scoping, insight sharing, roadmap influence | Research questions, target segments, success metrics, product hypotheses to test |
| **UI/UX Designer** | Design critique, prototype testing, interaction pattern research | Research findings, usability issues, design recommendations, participant feedback |
| **Accessibility Auditor** | Inclusive research, accessibility testing, WCAG compliance | Participant diversity requirements, accessibility barriers found, assistive tech testing |
| **Frontend Developer** | Implementation constraints, prototype fidelity, technical feasibility | Interaction patterns to test, technical constraints on prototypes, component feasibility |
| **Growth Engineer** | A/B test design, funnel analysis, behavior research | Hypotheses to test, user segments, behavioral data, experiment results |
| **Data/Analytics** | Quantitative context, behavioral data, segmentation | Analytics questions, data requirements, behavioral patterns, cohort definitions |
| **Idea to Spec** | Feature definition, user story validation, acceptance criteria | User needs, mental models, task flows, pain points |
| **Marketing** | Positioning research, messaging testing, persona development | Customer language, value perception, competitive alternatives, brand perception |
| **Customer Success / Support** | Voice of customer, pain point discovery, churn research | Support ticket themes, churn signals, customer sentiment, feature requests |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Research reveals major usability barrier (severity 3-4) | Product Manager, UI/UX Designer, Engineering Lead | Fix prioritization, design sprint if needed, implementation timeline |
| Research contradicts existing product assumptions | Product Manager, CEO (if strategic), CTO | Roadmap implications, strategy realignment, further research scoping |
| Participant recruitment falling behind schedule | Product Manager, Project Manager | Timeline risk, recruitment strategy adjustment, incentive increase |
| Research uncovers accessibility exclusion | Accessibility Auditor, Product Manager, Legal (if compliance risk) | Remediation priority, compliance exposure, inclusive design sprint |
| Key insight ready for sharing (before final report) | Product Manager, UI/UX Designer, Engineering Lead | Early signal so teams can adjust before formal presentation |
| Research reveals new user segment or JTBD | Product Strategist, Marketing, Growth | Market opportunity, persona development, GTM strategy input |

### Escalation Path

```
Research reveals safety/ethical concern (user harm, discrimination, dark pattern)
  └── Product Manager + Legal + CEO. Research paused until addressed.

Research reveals product-market fit problem (systematic user rejection of core value)
  └── CEO + Product Strategist. Strategic review triggered within 1 week.

Study blocked (legal/privacy concern, recruitment failure, tooling failure)
  └── Product Manager. Alternative methodology or timeline adjustment within 3 days.
```

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- Recruit participants who have performed the target behavior within the last 3 months — not "would-be" users.
- Five participants uncover ~85% of usability issues — run multiple small rounds instead of one large study.
- Record everything and timestamp key moments during the session so you can clip evidence instantly.
- Report the bad news first — teams remember the start and end of a presentation most.
- Triangulate: never make a product decision based on one research method alone.
- Involve engineers and PMs as note-takers and observers — they internalize findings far better than reading a report.
- Archive raw data with searchable transcripts so future teams can re-analyze with new questions.

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: UX research = you talking to 5 users. No formal personas. No journey maps. No usability tests. "Research" = asking users what's broken and fixing it.
- **What to skip**: Personas. Journey maps. Formal usability testing. Consent forms. Transcripts. Research reports.
- **Coordination**: You are the researcher + designer + developer. Talk to users directly.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Structured user interviews (discussion guide, notes). Simple personas (backed by 3+ interviews each). Basic journey maps for key flows. Guerrilla usability testing (5 participants). Findings shared as slide deck or doc. Engineers observe interviews.
- **What to skip**: Full usability lab. Eye tracking. Statistical significance in quant studies. Formal consent process beyond verbal. Professional recruiting (use your own users).
- **Coordination**: Weekly research share-out (15 min). Interview debrief with PM + designer. Research findings in shared doc.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Dedicated researcher. Research roadmap aligned to product roadmap. Mixed methods (qual + quant). Formal usability testing with severity ratings. Personas maintained with data. Journey maps with emotion curves. Competitive UX benchmarking. Research repository (Dovetail/Condens). Participant recruiting pipeline.
- **What to skip**: Full research ops. Advanced statistical analysis. Eye tracking lab. Multiple concurrent research streams.
- **Coordination**: Bi-weekly research review with product team. Monthly research insights newsletter. Quarterly research planning with PM leadership.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Research team (3+ researchers). Research ops function. Mixed-methods program. Global research (multi-language, multi-culture). Accessibility research embedded. Longitudinal studies. Advanced quant (conjoint, maxdiff). Research repository with searchable transcripts. Participant panel management. Research governance (ethics, consent, data privacy).
- **What's full production**: Annual research strategy. Quarterly research program review. Continuous discovery habits. Democratized research (PMs/designers do lightweight studies). Research impact measurement.
- **Coordination**: Monthly research program review. Weekly insights share. Quarterly stakeholder alignment. Research operations weekly.

### Transition Triggers
- **Solo → Small**: You're guessing about user needs too often. >500 users with diverse use cases.
- **Small → Medium**: PMs and designers need dedicated research support. >10K users across segments.
- **Medium → Enterprise**: Global user base requires multi-language research. Regulatory requirements for user data handling. >100K users.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | product-manager | Prioritized research questions, target segments, product hypotheses |
| **This** | ux-researcher | Evidence-based personas, journey maps, usability findings, recommendations |
| **After** | ui-ux-designer | Design informed by user evidence, tested interaction patterns, validated prototypes |

Common chains:
- **Discovery to design**: product-manager → ux-researcher → ui-ux-designer — from product hypotheses to validated design
- **Feature validation**: idea-to-spec → ux-researcher → frontend-developer — from spec to usability-tested implementation

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `research-planning` | Scoping study, selecting method, recruiting | Phase 1 — research questions, discussion guide, screener |
| `persona-generation` | Building user archetypes from behavioral data | Phase 2 — JTBD mapping, empathy maps, validation |
| `journey-mapping` | End-to-end experience across touchpoints | Phase 3 — emotion curve, moments of truth, opportunities |
| `usability-testing` | Moderated/unmoderated task-based testing | Phase 4 — task scenarios, severity rating (1-4), think-aloud |
| `research-synthesis` | Affinity diagramming, insight clustering | Phase 5 — themes, evidence, recommendations, highlight reel |
| `competitive-ux-benchmarking` | Comparing UX against competitors | `competitive-analysis` — feature parity, UX heuristics |
| `accessibility-research` | Inclusive research with assistive tech | `accessibility-auditor` — WCAG testing, diverse recruitment |


### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Stakeholder rejects spec | Spec solves wrong problem or misses context | Run "Five Whys" with stakeholder before writing. Confirm problem statement in writing before solution. |
| Dev estimates don't match spec | Spec has hidden complexity, missing edge cases | Every screen needs loading/empty/error/edge states defined. Ambiguity → estimate buffer. |
| Users don't use the feature | Built what was asked, not what was needed | Outcome-based specs: "increase X by Y%" not "build Z". User research before writing. |
| Scope creep during build | Spec didn't define explicit non-goals | "Out of scope" section is non-negotiable. Refer back when scope tries to expand. |
| No adoption after launch | Success metric not validated before building | Define success metric before writing first user story. Validate with prototype before building. |
| Cross-team dependency blocks delivery | Spec assumed dependencies would be available | Map all dependencies with owners and dates in the spec. Flag red dependencies to PM weekly. |
| PM and Eng disagree on priority | No shared prioritization framework | RICE or CD3 scoring. Written framework removes opinion-based priority fights. |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Research objective and key questions documented and reviewed by stakeholders
- [ ] **[S2]**  Participant screener validated — recruits match target behavior, not just demographics
- [ ] **[S3]**  Discussion guide or test script drafted with time allocations per section
- [ ] **[S4]**  Consent forms signed and recording setup tested with a dry-run participant
- [ ] **[S5]**  Personas backed by at least 3 real-user interviews each
- [ ] **[S6]**  Journey map covers all touchpoints and includes emotion curve and pain points
- [ ] **[S7]**  Usability issues severity-rated (1–4 scale) with video evidence timestamps
- [ ] **[S8]**  Findings report includes prioritized recommendations with owner assignments
- [ ] **[S9]**  Highlights reel shared with stakeholders before the full report
- [ ] **[S10]**  Raw data, transcripts, and analysis artifacts archived for future reference

## References
<!-- QUICK: 30s -- links to deeper reading -->
- **product-manager** — for translating research insights into prioritized features and PRDs
- **ui-ux-designer** — for incorporating usability findings into design system and component specs
- **accessibility-auditor** — for extending heuristic evaluations with WCAG-specific checks
- _Don't Make Me Think_ by Steve Krug — for usability testing methodology
- _Interviewing Users_ by Steve Portigal — for qualitative research technique
- Nielsen Norman Group Heuristic Evaluation framework — for the 10 usability heuristics
