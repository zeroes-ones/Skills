---
name: ux-researcher
description: >
  Use when generating user personas, mapping customer journeys, designing usability
  tests, synthesizing research findings, running competitive UX analysis, or performing
  heuristic evaluations. Handles qualitative and quantitative research methods,
  interview guide creation, usability test planning, affinity mapping, research
  synthesis, and evidence-based design recommendations. Do NOT use for UI design
  execution, visual design, or frontend implementation.
license: MIT
tags:
- ux
- research
- personas
- usability-testing
- journey-mapping
- heuristic-evaluation
author: Sandeep Kumar Penchala
type: product
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 2400
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
---

# UX Researcher
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Generate evidence-based user understanding that drives product and design decisions. Move teams from opinion-based to insight-based development through rigorous qualitative and quantitative research methods.

## Route the Request

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.md", "persona")` AND `file_contains("*.md", "interview\|participant")` | Research-backed personas exist. Jump to **Production Checklist**. |
| A2 | `file_exists("discussion-guide.md")` OR `file_exists("test-script.md")` | Research instrument exists. Jump to **Core Workflow → Phase 1 (Research Planning)**. |
| A3 | `file_exists("transcripts/")` OR `file_exists("recordings/")` | Raw research data exists. Jump to **Core Workflow → Phase 5 (Synthesis & Reporting)**. |
| A4 | `file_contains("*.md", "journey.map\|emotion.curve\|touchpoint")` | Journey mapping in progress. Jump to **Core Workflow → Phase 3 (Journey Mapping)**. |
| A5 | `file_contains("*.md", "usability.test\|task.scenario\|think.aloud")` | Usability test being planned. Jump to **Core Workflow → Phase 4 (Usability Testing)**. |
| A6 | `file_contains("*.csv", "N=\|participant\|interview")` OR `file_contains("*.md", "sample.size\|N=")` | Quantitative data exists. Jump to **Decision Trees → Qual vs Quant Method**. |
| A7 | `file_contains("*.md", "competitive\|benchmark\|heuristic.evaluation")` | Competitive UX analysis in scope. Jump to **Sub-Skills → competitive-ux-benchmarking**. |
| A8 | `file_contains("*.md", "screener\|recruit\|participant.pool")` | Recruitment being set up. Jump to **Core Workflow → Phase 1 (Recruitment)**. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:
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
└── Not sure? → Describe the problem in plain language and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These are hard-gate constraints. Violate any one and the output is invalid.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|--------------------|--------------------|
| G1 | Never report a finding without sample size (N), methodology, and study date — every insight must be traceable to raw evidence | `file_contains(output, "user.*found\|participant.*said\|research.shows")` AND NOT `file_contains(output, "N=|participant.*of|moderated\|unmoderated\|survey\|interview")` | REFUSE. Append: "Finding lacks methodology trace. Every insight must state: N=X, method=Y, date=Z. E.g., '4 of 5 participants (moderated usability test, June 2026).'" |
| G2 | Never label as "Persona" any profile backed by fewer than 3 real-user interviews — label as "Provisional Archetype" with N count | `file_contains(output, "Persona")` AND NOT `file_contains(output, "interview\|participant.*[3-9]\|[1-9][0-9]")` | STOP. Append: "Persona requires 3+ real-user interviews. Current profile has insufficient evidence — label as 'Provisional Archetype (N=<count>)' and note the validation gap." |
| G3 | Never make a design recommendation without citing observed behavior — task failure count, video timestamp, quote, heatmap, or analytics data point | `file_contains(output, "recommend\|should change\|redesign\|move")` AND NOT `file_contains(output, "participant.*failed\|timestamp\|quote\|heatmap\|analytics\|observed")` | DETECT. Append: "Recommendation lacks behavioral evidence. Cite at least one: task failure count, video timestamp, direct quote, heatmap, or analytics data." |
| G4 | Never base product decisions on a single research method — require triangulation from 2+ data sources (qual + quant + behavioral) | `file_contains(output, "conclusion\|decision\|verdict\|go with\|ship it")` AND NOT `file_contains(output, "triangulat\|second.method\|confirm.*with\|cross-referenc")` | STOP. Append: "Single-method conclusion detected. Triangulate with 2+ methods: interviews + analytics, or usability test + survey, or behavioral observation + support data." |
| G5 | Never use leading questions in test scripts — "Click the blue button" replaces "Try to complete the purchase." Pilot-test scripts before live sessions | `file_contains(output, "click the\|press the\|select the\|look for the\|you should")` AND NOT `file_contains(output, "pilot.test\|dry.run\|script.validation")` | REFUSE. Append: "Test script contains leading language. Replace directive prompts with task-based scenarios. Run a pilot session to validate." |
| G6 | Never delay reporting severity-3 or severity-4 findings beyond 24 hours — critical issues must escalate immediately, not wait for the final report | `file_contains(output, "severity.*[3-4]\|critical\|showstopper\|blocker")` AND NOT `file_contains(output, "escalat\|within.*24\|immediate\|alerted\|notified")` | DETECT. Append: "Critical finding detected without escalation protocol. Severity 3-4 findings must be reported to stakeholders within 24 hours with video evidence — do not wait for the final report." |

## The Expert's Mindset

UX research is not about confirming what you already believe — it's about **discovering what you don't know about your users, systematically and with rigor**. The output is not a report; the output is a decision that would have been different without the research.

### Mental Models

| Model | Description |
|---|---|
| **You are not your user** | The most dangerous assumption in product development. Your mental model, vocabulary, and priorities are nothing like your users'. Research exists to bridge that gap. |
| **What people say ≠ what people do** | Self-reported behavior is unreliable. "Would you use this?" gets a different answer than watching someone try to use it. Observe behavior; don't just collect opinions. |
| **Small N, rich data beats large N, shallow data** | 5 one-hour interviews reveal more than 500 survey responses. Depth over breadth, especially in discovery. Survey for validation, interview for discovery. |
| **The goal is not to be right — it's to be less wrong** | Research doesn't give you the answer. It reduces the range of wrong answers. The goal is to narrow uncertainty, not eliminate it. |

### Cognitive Biases in User Research

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Confirmation bias** | Asking questions that lead users toward the answer you want | Write your research questions before you know what you want to find. Have a peer review them for leading language. |
| **Social desirability bias** | Users telling you what they think you want to hear, especially about usage intent | Never ask "Would you use this?" Ask "When did you last encounter this problem? How did you solve it?" |
| **Selection bias** | Recruiting participants who are easier to find, not who represent your actual users | Define screening criteria before recruiting. Audit your sample against your actual user demographics. |
| **Framing effect** | The way you present a concept shapes the response more than the concept itself | Test multiple framings of the same concept. Rotate the order of tasks and options. |

### What Masters Know That Others Don't

- **The most valuable insight is usually the one that makes the team uncomfortable.** If all your research confirms what you already believed, you didn't learn anything. The best researchers actively seek the finding that challenges the team's assumptions.
- **Research velocity matters.** A "good enough" study delivered in 3 days that changes a decision is worth more than a "perfect" study delivered in 3 weeks when the decision has already been made. Match rigor to decision timeline.
- **The researcher's job is not to deliver findings — it's to deliver understanding.** A deck of 50 findings that nobody reads is worthless. One video clip of a user struggling that the entire team watches and discusses is priceless.
- **Triangulation is the difference between science and storytelling.** Never make a product recommendation from a single method. At least two methods should point in the same direction before you recommend action.

## Operating at Different Levels

UX research skill manifests in the complexity of research questions tackled and strategic influence of findings.

| Level | UX Researcher Output Characteristics |
|---|---|
| **L1 — Apprentice** | Runs usability tests from a script. Moderates sessions under supervision. Learns research methods. |
| **L2 — Practitioner** | Owns research for a feature area. Chooses appropriate methods, conducts studies independently, delivers actionable findings. |
| **L3 — Senior** | Owns research for a product. Triangulates across methods, influences product strategy with evidence, mentors junior researchers. |
| **L4 — Staff/Principal** | Sets research strategy for the organization. Establishes research ops, participant panels, and insights repositories. "This is how we do research here." |
| **L5 — Industry-level** | Creates research methodologies adopted across the industry. "Here's a new approach to understanding user behavior." |

**Usage**: Say "as an L3 UX researcher, design a study for..." Default: **L2** (feature-area research, independent execution).

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

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| No personas defined for a feature targeting a specific user segment | Propose persona creation from behavioral data: interview 5+ users in the target segment, identify JTBD, map pain points with severity ratings. Label assumption-based archetypes separately from interview-backed personas | Persona-less features are built for "everyone" (which means no one). A persona backed by 3+ real user interviews prevents the most expensive design mistake: building for the team's self-image instead of the actual user |
| No accessibility consideration in the research plan or participant recruitment | Flag accessibility gap to `accessibility-auditor`. Propose inclusive recruitment: include participants who use assistive technologies (screen readers, switch devices, voice control). Add WCAG-relevant tasks to usability test scripts | Research that excludes users with disabilities produces designs that exclude users with disabilities. Inclusive research is not a "nice to have" — it's the difference between a product that works for everyone and a product that faces ADA litigation |
| Stakeholder presents a solution ("build a dashboard") instead of a research question ("do users need real-time data?") | Reframe the request as a research question. Refuse to test a solution until the underlying problem is understood. Ask: "What decision will this research inform?" and "What would you do differently based on the findings?" | Testing solutions without understanding the problem produces research that confirms bias. Every study should answer a decision-critical question — if the answer won't change what gets built, don't run the study |
| No competitive UX analysis has been done for a feature in a contested market | Propose competitive UX audit: map 3-5 competitor flows against your proposed flow, score on usability heuristics, identify gaps and opportunities. Share findings with `product-manager` and `ui-ux-designer` | Competitive UX benchmarking reveals what users already expect. If competitors have trained users on a certain interaction pattern, breaking that pattern costs adoption. Know what users are comparing you against |
| Research plan has no quantitative component — purely qualitative interviews with no behavioral data triangulation | Propose mixed-methods approach: pair interviews with analytics data (funnel drop-offs, feature adoption, session replays). Triangulate qualitative insights with quantitative patterns | Qualitative research tells you WHY users behave a certain way; quantitative data tells you HOW MANY users behave that way. Either alone is incomplete — together they produce actionable, prioritized findings |
| Usability test script uses leading language ("click the blue button in the top right") | Rewrite as task-based scenarios: "You want to buy this item. Go ahead." Leading scripts produce confirmation, not discovery. Test the script with a pilot participant before running the actual study | A usability test with leading instructions is a confirmation exercise. Participants follow directions instead of intuition — and you ship a design that works when users are told what to do, not when they have to figure it out themselves |
| Research findings sit in a PDF nobody reads — stakeholders ask "what did we learn?" 3 weeks later | Create a 3-minute highlights reel with video evidence timestamps before writing the full report. Share with stakeholders within 48 hours of the last session. Archive raw data with searchable transcripts | The value of research decays rapidly after the last session. Stakeholders absorb video evidence 10x faster than written reports. If insights aren't consumed within a week, the research might as well not have happened |
| Research reveals a major usability barrier (severity 3-4) that blocks a critical user flow | Escalate to `product-manager` and `ui-ux-designer` within 24 hours with video evidence. Propose a design sprint to resolve before implementation proceeds. Do not wait for the final report | Severity 3-4 usability issues found during research are $500 fixes; the same issues found in production are $50,000 fixes plus customer trust damage. Early escalation saves sprints and reputation |

## What Good Looks Like

> You've just completed the UX research study. Every insight in your report cites specific evidence — a participant quote, a video timestamp, or a task failure count — never "users seem confused." Your personas are built from behavioral data backed by at least three real-user interviews each, and you labeled the one based on assumptions as an archetype. The usability issues are severity-rated on a 1–4 scale with video evidence timestamps, so the design team knows exactly what to fix first. Your highlights reel runs under three minutes and stakeholders watched it before they opened the report. The raw data, transcripts, and analysis artifacts are archived and searchable — future you won't have to redo this study.

## Deliberate Practice

UX research mastery comes from observing real users, repeatedly, until pattern recognition becomes instinct. There is no substitute for watching users struggle.

```mermaid
graph LR
    A[Design a study for a real question] --> B[Conduct sessions — moderate, observe, listen]
    B --> C[Synthesize findings into actionable insights]
    C --> D[Track whether your recommendations changed the product]
    D --> A
```

| Level | Practice Routine | Frequency |
|---|---|---|
| **Novice** | Watch a recorded usability session and write down every moment of confusion | Weekly |
| **Competent** | Moderate a usability test and produce a findings report within 48 hours | Biweekly |
| **Expert** | Run a triangulated study: combine usability testing + analytics + survey for the same question | Monthly |
| **Master** | Build a research ops system (panel, repository, consent framework) that scales across products | Annually |

**The One Highest-Leverage Activity**: Watch one user session recording every day. Not a highlight reel — a raw, unedited session. 15 minutes. You'll learn more about your product than from any dashboard.

## References

Detailed reference material loaded on demand:

- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)

