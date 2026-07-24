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

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---:|
| "We talked to 2 users and the pattern is crystal clear" | N=2 is not research — it's anecdote with a slide deck. Two participants agreeing is the most dangerous pattern in UX: it feels like confirmation but it's coincidence. 3+ interviews minimum for personas; below that, label it "Provisional Archetype." |
| "The usability test was conclusive — one method is enough" | Single-method conclusions are the #1 source of research-driven product mistakes. Users say one thing in interviews, do another in usability tests, and something else entirely in analytics. Triangulate with 2+ methods, or admit you're guessing with extra steps. |
| "Just tell me what to change — I'll review the evidence later" | Design recommendations without cited behavioral evidence (task failures, timestamps, direct quotes) are indistinguishable from personal opinion. Your "obvious fix" is someone else's subjective preference until you anchor it in observed behavior. |
| "We'll include the critical finding in the final report in 2 weeks" | Severity 3-4 findings that wait 2 weeks for a report cycle have already shipped to production. Critical usability blockers demand 24-hour escalation with video evidence. Every hour of delay is another user hitting the blocker — and another chance they never come back. |
| ""Try clicking the blue button" is a perfectly clear test task" | That's not a test task — it's a leading instruction that handed the user the answer. You just proved users can follow directions. Task-based scenarios reveal behavior; directive prompts reveal obedience. Your test proved nothing. |

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
| R6 | **DETECT and WARN when research questions are framed to confirm existing beliefs rather than test them.** "How do users like our new dashboard?" assumes users like it. The research is designed to find confirming evidence, not truth. Confirmation bias in research questions produces "validated" features that fail in market. | Trigger: research questions containing "like," "prefer," or "satisfied" without neutral alternatives (e.g., "How do users interact with the dashboard? Where do they struggle?") | WARN. Reframe all questions neutrally: "What do users do?" not "Do users like?" "Where do users struggle?" not "How satisfied are users with the flow?" Research design should be equally capable of discovering you're wrong as confirming you're right. |
| R7 | **REFUSE to generalize findings from 5 participants to an entire user population without acknowledging the limitations.** 5 users is valid for usability testing (Jakob Nielsen: 5 users find 85% of problems). It is NOT valid for: preference testing ("80% of users prefer blue" — with N=5, that's 4 users), behavioral frequency claims, or prioritizing features across user segments. Using 5-person findings to justify roadmap decisions is statistically indefensible. | Trigger: presenting percentages or "X% of users" claims from studies with N < 30 | STOP. Language correction: "3 of 5 participants struggled with the checkout flow" NOT "60% of users struggle." "Participants mentioned wanting faster search" NOT "Most users want faster search." Small-N research identifies problems and generates hypotheses — it does NOT measure prevalence. |

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
| **Recency bias** | Giving disproportionate weight to the last participant's feedback because it's freshest in memory | Take structured notes during every session. Review all sessions before synthesizing. Use affinity diagramming to surface patterns across the full dataset, not just the most memorable sessions. |
| **Observer-expectancy effect** | Subtly cueing participants toward expected behaviors through body language, tone, or follow-up questions | Pilot-test scripts with a colleague who matches the target persona. Record sessions and have a second researcher review for unintentional leading. Use unmoderated methods when observer bias risk is high. |
| **Survivorship bias** | Only studying users who stayed — missing the insights from users who churned, abandoned onboarding, or never signed up | Proactively recruit lapsed users and churned customers. Exit surveys and cancellation flows are goldmines. Every churned user carries an insight about your product that active users can't provide. |

## Research Operations

### Participant Recruitment & Session Management

| Activity | Standard | Anti-Pattern |
|---|---|---|
| **Screener design** | Behavioral screening questions: "When did you last [behavior]?" not "Are you familiar with [concept]?" Include disqualifying criteria before qualifying criteria to reduce gaming. | "Have you used a project management tool?" — 100% say yes. Meaningless. |
| **Incentives** | $75-150/hr for consumer, $150-300/hr for professional/enterprise. Pay within 48 hours of session. Incentive is for time, not for positive feedback. | Gift card raffle. "Exposure." Free month of the product. |
| **No-show rate** | Over-recruit by 30%. For 5 participants, schedule 7. Confirm 48 hours and 2 hours before. Have backup slots. | Assuming all 5 will show. They won't. |
| **Session recording** | Always get written consent. Record screen + audio + face (for emotion/confusion detection). Timestamp key moments during the session. | "We'll record if that's okay?" (asked after they've already started and feel awkward saying no). |
| **Observer management** | Max 3 observers per session. Observers join a dedicated Slack channel for real-time notes. No observers speak during the session. Debrief observers immediately after: "What surprised you?" | 8 stakeholders in the observation room. Someone asks "Can you try clicking the other button?" The session is now ruined. |
| **Participant data privacy** | Anonymize all data within 24 hours. Store raw recordings in access-controlled system. Delete recordings per legal/consent timeline. Never share identifiable data in public presentations. | Participant's full name and company in the slide deck. Recording stored in personal Google Drive. |

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

### Research Cadence Decision

```
How often should you run formal research?
├── Pre-product (0 users, exploring problem space) → 2-4 discovery interviews per week
│     Continuous discovery. Every week you don't talk to a user, you're building on assumptions.
│     Output: running list of validated problems, prioritized by pain severity and frequency.
├── Early product (10-100 users, finding PMF) → Biweekly usability tests + monthly synthesis
│     Test every significant feature before it ships. 5 users per round, 2-week turnaround.
│     Output: usability score per feature, prioritized fix list, design recommendations.
├── Growth stage (1K-100K users, scaling) → Monthly moderated tests + quarterly survey + continuous analytics
│     Moderated for deep issues, survey for attitudes, analytics for behavior at scale.
│     Output: quarterly UX health report with trend lines and ROI of research-driven changes.
├── Mature product (100K+ users, optimizing) → Continuous unmoderated testing + quarterly moderated deep-dives
│     Unmoderated platform (UserTesting, Maze) for volume testing of incremental changes.
│     Quarterly moderated studies for strategic questions: "Should we enter this new market?"
│     Output: monthly UX metrics dashboard, quarterly strategic research report.
└── Crisis mode (churn spike, NPS crash, competitor threat) → Flash research sprint
      Recruit 5 users within 48 hours. Run 5 one-hour moderated sessions in 3 days.
      Synthesize and present findings within 1 week of the trigger event.
      Output: top 3 issues causing churn, ranked by severity with video evidence.
```

### Synthesis & Deliverable Format

```
How should you communicate research findings to maximize impact?
├── Urgent finding (blocking release, P0 usability issue) → Slack + 1-page async memo
│   ├── Format: Finding, user impact, recommended action, effort estimate
│   ├── Deliver within 24 hours. Do NOT wait for the full report.
│   ├── Follow-up: brief sync with PM to confirm understanding and action
│   └── Anti-pattern: "This will be in the final report in 2 weeks" — the release ships in 1 week
├── Standard usability study (5-8 participants, evaluative) → Top 3 Actions memo + video clips
│   ├── Page 1: Top 3 Actions (finding → impact → recommendation → effort)
│   ├── Page 2-5: Findings organized by severity, each with a 30-60 second video clip
│   ├── Video clips > quotes > heatmaps > statistics (for usability: show, don't tell)
│   ├── Appendix: full session recordings, moderator guide, participant demographics
│   └── Deliver within 3 business days of last session. Stakeholder readout: 30 min max.
├── Foundational/generative research (12-20 participants, longitudinal) → Full report + workshop
│   ├── Deliverable 1: Executive summary (1 page) — key insights, opportunities, risks
│   ├── Deliverable 2: Detailed findings organized by theme with evidence (quotes, behavioral data)
│   ├── Deliverable 3: Opportunity map — 2x2 of impact vs effort for top 10 opportunities
│   ├── Deliverable 4: 2-hour stakeholder workshop to prioritize opportunities into roadmap
│   └── Timeline: deliver within 2 weeks of last session. If it takes 4 weeks, scope was too broad.
└── Continuous/discovery research (ongoing, lightweight) → Living insights repository
    ├── Format: searchable database (Notion, Dovetail, Condens) organized by topic and user segment
    ├── New insights added weekly. Stale insights flagged and re-validated after 6 months.
    ├── Each insight: source, confidence level (single observation → pattern across studies → statistical significance)
    └── Stakeholders self-serve from the repository. Researcher role shifts from "report writer" to "insight curator."
```

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

### BEFORE (Novice) → AFTER (World-Class)

**Research Rigor:**
- **BEFORE:** "We interviewed 3 users and they all liked it. Let's ship!" No recording. No transcript. No systematic analysis. Findings based on the interviewer's memory of what was said. Three months later: "Why is nobody using this feature we 'validated'?"
- **AFTER:** 5+ moderated sessions per round. Every session recorded, transcribed, and timestamped. Findings synthesized via affinity diagramming. Each insight states: sample size (N=X), methodology, date, and direct evidence (video timestamp + quote). Recommendations traceable to specific observed behaviors. Triangulation from 2+ methods (interview + analytics, or usability test + survey).

**Stakeholder Impact:**
- **BEFORE:** 40-slide research report presented at all-hands. Filed in Google Drive. Never referenced again. Stakeholders 3 weeks later: "What did we learn from that research again?" $15K study, $0 ROI.
- **AFTER:** 3-minute highlights reel with video evidence shared within 48 hours of last session. Key insights embedded in Jira tickets with severity ratings. Research findings tracked as "research debt" in the same backlog as feature work. Quarterly metric: % of product decisions informed by user evidence (target > 80%).

**Persona Quality:**
- **BEFORE:** "Sarah, 34, marketing manager, 2 kids, drives a Honda." Demographic fiction based on stereotypes. Nobody on the team can use this to make a design decision — what does "2 kids" tell you about how Sarah uses your SaaS product?
- **AFTER:** Behavioral persona: "The Batch Processor — runs reports at end of month, needs bulk operations, frustrated by single-item actions, current workaround is exporting to Excel." Includes: primary JTBD, core tasks (3-5), pain points with severity, current tools/workarounds, context of use, representative quote from real interview. Backed by 3+ real-user interviews.

**Stakeholder Engagement Through the Research Process:**
- **BEFORE:** Researcher operates in a silo. PM writes a research brief, researcher disappears for 3 weeks, then surfaces with a 40-slide deck at a readout meeting. Stakeholders see the findings for the first time at the presentation. Questions derail the meeting because stakeholders weren't primed. PM says "this doesn't answer what I needed" because the scope drifted without mid-course correction. Researcher feels their work was undervalued. Nobody changed what they were building.
- **AFTER:** Researcher embeds with the product team throughout the study. Kickoff workshop aligns on research questions and decisions-to-be-made (not just things-to-learn). Mid-study checkpoint at 50% data collection: "Here's what we're hearing so far — does this change what you want us to probe deeper on?" Raw session notes shared within 24 hours of each session. Stakeholders invited to observe at least 1 live session (no substitutes — watching a user struggle in real time is the single most effective way to build empathy). Findings workshop (not readout): stakeholders rank insights by impact, assign owners to each recommendation, and commit to decisions before leaving the room. Researcher's success metric: number of product decisions that changed because of the research — not number of reports produced.

> Every insight in your report cites specific evidence — a participant quote, a video timestamp, or a task failure count — never "users seem confused."

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.

## Deliberate Practice

UX research mastery comes from observing real users, repeatedly, until pattern recognition becomes instinct. There is no substitute for watching users struggle.

| Level | Practice Routine | Frequency |
|---|---|---|
| **Novice** | Watch a recorded usability session and write down every moment of confusion | Weekly |
| **Competent** | Moderate a usability test and produce a findings report within 48 hours | Biweekly |
| **Expert** | Run a triangulated study: combine usability testing + analytics + survey for the same question | Monthly |
| **Master** | Build a research ops system (panel, repository, consent framework) that scales across products | Annually |

**The One Highest-Leverage Activity:** Watch one user session recording every day. Not a highlight reel — a raw, unedited session. 15 minutes. You'll learn more about your product than from any dashboard. Do this for 30 days and you'll have more user empathy than 90% of product teams.

## Gotchas

- **Recruiting the wrong participants wastes the entire study budget.** Testing a developer tool with non-technical participants, or an enterprise SaaS with students, produces data that looks real but points in wrong directions. A study with 8 wrong participants costs $5K-$15K in incentives, facilitation time, and analysis — with $0 in valid insights. Even worse: acting on those wrong insights can send $100K+ in engineering in the wrong direction. **Total cost: $5K-$15K per wasted study; $50K-$150K if acted upon.** Define screening criteria with behavioral triggers (e.g., "has deployed to production in the last 30 days") and screen every participant before scheduling.
- **Confirmation bias turns research into validation theater.** When you frame questions to hear what you want ("You'd prefer a simpler dashboard, right?"), you get agreement — not truth. Teams then spend $50K-$300K building features that validated their assumptions instead of testing them. **Total cost: $50K-$300K building validated wrong assumptions.** Use neutral, open-ended questions ("Walk me through the last time you used a dashboard. What worked? What didn't?") and pre-register your hypotheses before data collection so you can distinguish learning from confirmation.
- **Sample sizes that are too small produce misleading confidence.** Testing a critical workflow with 3 participants who all succeed doesn't mean the design works — it means you haven't tested enough. With 3 users, you can only detect problems affecting >65% of users. A "validated" feature that fails for 40% of users in production triggers $20K-$100K in emergency fixes. **Total cost: $3K-$10K per misleading insight; $20K-$100K in downstream rework.** Calculate your required sample size upfront based on the problem prevalence you need to detect — don't default to 5 users for every study.
- **Research that sits in a slide deck costs $10K-$50K per study in zero ROI.** A 3-week research project produces a 40-slide report presented at an all-hands, then filed in Google Drive and never referenced again. The $15K study delivered $0 in product improvement because findings weren't actionable or weren't integrated into the team's workflow. **Total cost: $10K-$50K per un-actioned study.** Every finding must include a specific recommendation, a priority, and an owner — and be tracked in the same backlog as feature work. Research readouts without assigned action items are entertainment.
- **Testing with internal employees instead of actual target users.** "We'll just validate with the sales team — they talk to customers every day." Internal employees have domain expertise, product familiarity, and organizational incentives that real users don't. A checkout flow that 8/8 employees complete flawlessly might fail for 6/10 real customers because employees unconsciously compensate for confusing UI patterns that real users get stuck on. The $8K-$12K saved by skipping external recruitment gets spent 10x over when the feature ships broken and triggers an emergency redesign sprint. **Total cost: $30K-$100K in rework from false-positive internal validation that masks real usability failures.** Recruit external participants who match your target persona with behavioral screening criteria — internal dogfooding is a supplement, never a substitute for research with actual customers.
- **Recruiting your own product's power users for usability testing.** Power users have built mental models and workarounds that novices don't. They forgive confusing UX because they know "that's just how it works." Testing with power users produces falsely positive results — they breeze through flows that frustrate and lose 60% of new users. The product team hears "users found it intuitive" and ships a design that alienates new users. **Total cost: $50K-$200K in lost new-user acquisition spend wasted on a leaky onboarding funnel — plus 6-12 months of churn before the problem is identified.** Fix: Segment research participants by experience level. Every usability study should include minimum 50% first-time users of the feature/product. If you must use existing users, screen for those who've used the product less than 3 times in the last 90 days.
- **Presenting raw research findings without prioritized, actionable recommendations.** A 40-page research report with 87 findings is a firehose. The PM reads 3 pages, gets overwhelmed, files it. The research had no impact. Three months later, the PM makes the same mistake the research identified because nobody turned findings into decisions. **Total cost: $30K-$80K per research study that produces zero product impact (researcher salary + participant incentives + stakeholder time in readouts).** Fix: Every research deliverable includes a "Top 3 Actions" executive summary on page 1. Format: "Finding → Impact (quantified if possible) → Recommended Action → Effort (S/M/L)." The PM should be able to make a decision after reading page 1. The rest of the report is evidence and methodology — important, but not required for action.
- **Conducting research on a prototype so polished it looks like production.** Users are reluctant to criticize a "finished" product. They'll say "it's fine" to avoid hurting feelings, even when the design has fundamental problems. The research becomes a validation exercise rather than a discovery tool. Meanwhile, real usability issues go undetected because the prototype's visual polish suppressed honest feedback. **Total cost: $40K-$120K in development cost for a feature that launched with undetected usability problems — requiring expensive post-launch rework and causing user churn.** Fix: Match fidelity to research goals. Generative/discovery research: paper sketches, wireframes, low-fidelity (users feel comfortable critiquing). Evaluative/usability testing: medium-fidelity prototypes, grayscale, no custom illustrations (looks "in progress"). Validation: high-fidelity is appropriate — you're testing polish, not concept.
- **Usability test with 5 users** (Nielsen Norman Group heuristic) — 5 users find ~85% of usability problems IF the problems affect >30% of users. Rare problems (affecting 5% of users) need 50+ participants to surface. 5 users is for formative testing, not for making statistical claims about prevalence.
- **Confirmation bias in interview questions** — "Would you say the navigation is confusing?" primes the participant. They say yes because you suggested it. The unbiased version: "Tell me about your experience finding the settings page." Let them surface the problem (or not surface it) organically.
- **Persona creation from demographic stereotypes** — "Sarah, 34, marketing manager, 2 kids" tells you WHO she is, not WHAT she needs or HOW she behaves. Behavioral personas ("the batch processor," "the real-time monitor") based on observed usage patterns are actionable; demographic personas are fiction.
- **A/B test that reaches significance at 7 days** — you stop it and declare the variant winner. But if you had run it for 14 days, the effect reversed (novelty effect wore off). Always pre-register test duration AND sample size. Peeking and stopping early inflates false positive rate to ~30%.
- **"Users said they wanted X"** — what users SAY in interviews and what they DO in a live product correlate at ~0.3 (weak). Users said they wanted folders in Google Inbox; they actually needed search and archiving. Observe behavior; don't just ask for wishlists.

## Verification

- [ ] Research plan: objectives, methodology, participant criteria, and sample size documented BEFORE data collection
- [ ] Interview guide: questions are open-ended, non-leading, and pilot-tested with 1-2 participants
- [ ] Data saturation: analysis shows thematic saturation (no new themes emerging in last 20% of sessions)
- [ ] Findings report: themes supported by multiple participant quotes, recommendations traceable to specific findings
- [ ] Bias documented: researcher positionality, recruitment channels, and methodological limitations stated
- [ ] Share-out: findings presented to stakeholders, decisions documented, follow-up research planned for open questions

## Research Tools Quick Reference

| Tool | Best For | Pricing Model |
|---|---|---|
| **UserTesting / UserZoom** | Unmoderated usability testing at scale, panel recruitment | Per-seat license + per-session |
| **Maze** | Prototype testing, first-click tests, design surveys | Freemium → per-seat |
| **Dovetail / Condens** | Research repository, transcription, tagging, insight management | Per-seat |
| **Lookback / Zoom** | Moderated session recording with timestamped notes | Per-seat / freemium |
| **Optimal Workshop** | Card sorting, tree testing, first-click testing | Per-study or subscription |
| **Hotjar / FullStory** | Session replay, heatmaps, feedback widgets | Freemium → per-session |

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

