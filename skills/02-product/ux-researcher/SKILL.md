---
name: ux-researcher
description: Generate personas, map user journeys, design usability tests, synthesize research findings, run competitive UX analysis, and perform heuristic evaluations. Use to inform design and product
  decisions with user evidence. Triggered by create personas, journey map, usability test plan, research synthesis, competitive analysis, heuristic evaluation, user research.
author: Sandeep Kumar Penchala
type: product
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- ux-researcher
chain:
  consumes_from:
  - product-manager
  feeds_into:
  - frontend-developer
  - idea-to-spec
  - patient-experience-researcher
  - patient-health-educator
  - product-manager
  - product-strategist
  - ui-ux-designer
token_budget: 2400
output:
  type: code
  path_hint: ./
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
├── Need design recommendations from research → `ui-ux-designer`
├── Need feature prioritization or roadmap planning? → `product-manager`
├── Need product-market fit or competitive positioning? → `product-strategist`
├── Need accessibility testing with disabled participants? → `accessibility-auditor`
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

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `product-manager` | Research questions, target segments, success metrics, product hypotheses to test, prioritized learning needs | During study scoping; before recruiting participants |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `product-strategist` | User personas with behavioral data, journey maps with emotion curves, unmet JTBD evidence, competitive UX benchmarks | Product strategy built on assumptions rather than evidence — wasted discovery cycles |
| `idea-to-spec` | User needs, mental models, task flows, pain points with severity ratings, accessibility requirements | Specs miss critical user context — features built that users don't need |
| `ui-ux-designer` | Usability test results with severity ratings (1-4), design recommendations traced to observed behavior, participant quotes with video timestamps | Designs repeat known usability mistakes — redesign cycles |
| `product-manager` | Research synthesis report, evidence-based feature recommendations, user segment insights, behavioral patterns | PM prioritizes features without user evidence — backlog driven by loudest voice |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Research reveals major usability barrier (severity 3-4) | `product-manager`, `ui-ux-designer`, `engineering-manager` | Fix prioritization, design sprint if needed, implementation timeline |
| Research contradicts existing product assumptions | `product-manager`, `ceo-strategist` (if strategic), `cto-advisor` | Roadmap implications, strategy realignment, further research scoping |
| Participant recruitment falling behind schedule | `product-manager`, `scrum-master` | Timeline risk, recruitment strategy adjustment, incentive increase |
| Research uncovers accessibility exclusion | `accessibility-auditor`, `product-manager`, `legal-advisor` (if compliance risk) | Remediation priority, compliance exposure, inclusive design sprint |
| Key insight ready for sharing (before final report) | `product-manager`, `ui-ux-designer`, `engineering-manager` | Early signal so teams can adjust before formal presentation |
| Research reveals new user segment or JTBD | `product-strategist`, `marketing-manager` | Market opportunity, persona development, GTM strategy input |

### Escalation Path

```
Research reveals safety/ethical concern (user harm, discrimination, dark pattern)
  └── `product-manager` + `legal-advisor` + `ceo-strategist`. Research paused until addressed.

Research reveals product-market fit problem (systematic user rejection of core value)
  └── `ceo-strategist` + `product-strategist`. Strategic review triggered within 1 week.

Study blocked (legal/privacy concern, recruitment failure, tooling failure)
  └── `product-manager`. Alternative methodology or timeline adjustment within 3 days.
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


### War Story 1 — The Persona That Confirmed Our Bias
**Symptom:** A product team created a persona called "Power User Pat" based on their own assumptions — Pat was technical, logged in daily, and loved APIs. Every feature decision was justified by "Pat would love this." Actual user data showed 80% of users never used APIs and logged in weekly at most.
**Root cause:** The persona was created without user interviews. "Power User Pat" was actually a composite of the engineering team's ideal self-image. No real users were interviewed to validate the behavioral profile.
**Fix:** Stipulated that every persona requires at least 3 real-user interviews before it can be used in prioritization decisions. Personas without interviews are labeled "Archetype" (not "Persona") and carry less weight in roadmap decisions.
**Lesson:** A persona built from assumptions is worse than no persona — it gives false confidence to bad decisions. Interview real users before writing a single persona attribute.

### War Story 2 — The Usability Test That Found Nothing Wrong
**Symptom:** A team ran a usability test that "passed" — all 5 participants completed the task. They launched. Support tickets flooded in. Users couldn't find the checkout button. Retesting showed 4 of 5 participants couldn't locate it.
**Root cause:** The test script was leading: "Click the checkout button in the top right" instead of "Buy this item." Participants followed instructions, not intuition. The pass criteria was completion rate, not time-on-task or error count.
**Fix:** Revised test scripts to be task-based, not instruction-based. Added time-on-task and error-count metrics alongside completion rates. Ran pilot tests to catch leading language before the actual sessions.
**Lesson:** A usability test with leading tasks is a confirmation exercise, not a discovery exercise. Test the script, not just the design. Time-on-task reveals friction that completion rate hides.

### War Story 3 — The Analytics That Told the Wrong Story
**Symptom:** Monthly active users were growing 15% MoM. The team celebrated and doubled down on acquisition. Then they looked at weekly cohorts: 80% of new users churned within 7 days. Growth was a leaky bucket.
**Root cause:** The team tracked the wrong metric (MAU instead of weekly retention). The data was accurate but the framing was misleading. Acquisition was hiding a retention crisis.
**Fix:** Established a "leading and lagging" metric framework: retention rate (leading) over MAU (lagging). Weekly cohort analysis became the primary health metric. Triangulated analytics with qualitative exit surveys.
**Lesson:** A single metric in isolation tells a story you want to hear. Cohort analysis reveals the truth. Always pair quantitative data with qualitative research before declaring victory.


### Error Decoder
<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Stakeholder rejects spec | Spec solves wrong problem or misses context | Run "Five Whys" with stakeholder before writing. Confirm problem statement in writing before solution. | Stakeholders reject research when it answers a question they didn't ask. Align on the problem first — the most rigorous study is useless if it addresses the wrong decision. |
| Dev estimates don't match spec | Spec has hidden complexity, missing edge cases | Every screen needs loading/empty/error/edge states defined. Ambiguity → estimate buffer. | Unvalidated design assumptions are the biggest source of estimate blowup. Usability test early prototypes to surface edge cases before they become engineering surprises. |
| Users don't use the feature | Built what was asked, not what was needed | Outcome-based specs: "increase X by Y%" not "build Z". User research before writing. | Users are terrible at predicting what they will use. Observation of actual behavior beats stated preference every time. Watch what users do, not what they say they will do. |
| Scope creep during build | Spec didn't define explicit non-goals | "Out of scope" section is non-negotiable. Refer back when scope tries to expand. | Every feature added mid-build is one that was not tested with users. Scope creep without validation creates complexity nobody asked for. Protect the research schedule as fiercely as the build schedule. |
| No adoption after launch | Success metric not validated before building | Define success metric before writing first user story. Validate with prototype before building. | Adoption problems are almost always research gaps. If you did not observe users successfully completing the core task in a prototype, do not expect them to do it in production. |
| Cross-team dependency blocks delivery | Spec assumed dependencies would be available | Map all dependencies with owners and dates in the spec. Flag red dependencies to PM weekly. | Research timelines are fragile because they depend on recruiter capacity, participant availability, and stakeholder reviews. Buffer each dependency by 30% or accept delays. |
| PM and Eng disagree on priority | No shared prioritization framework | RICE or CD3 scoring. Written framework removes opinion-based priority fights. | Research evidence is the best arbitration tool. When PM and Eng disagree, the team with user data wins. Invest in research that settles priority debates with facts, not opinions. |


## What Good Looks Like

> You've just completed the UX research study. Every insight in your report cites specific evidence — a participant quote, a video timestamp, or a task failure count — never "users seem confused." Your personas are built from behavioral data backed by at least three real-user interviews each, and you labeled the one based on assumptions as an archetype. The usability issues are severity-rated on a 1–4 scale with video evidence timestamps, so the design team knows exactly what to fix first. Your highlights reel runs under three minutes and stakeholders watched it before they opened the report. The raw data, transcripts, and analysis artifacts are archived and searchable — future you won't have to redo this study.


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
