---
author: Sandeep Kumar Penchala
type: reference
domain: user-research
version: "1.0"
last_updated: 2026-07-21
parent_skill: ux-researcher
---

# UX Research Methods Guide

> **Author:** Sandeep Kumar Penchala

A practical reference for selecting, executing, and synthesizing UX research methods. Covers method selection by question type, usability test scripts, interview guides, survey design, synthesis frameworks, and research repository structure. Use alongside the UX Researcher skill's study design and analysis workflows.

---

## 1. Method Selection by Question Type

### Generative Research (Explore problems, discover needs)
| Method | Best for | Participants | Time | Output |
|--------|----------|-------------|------|--------|
| **User interview** | Deep understanding of behaviors, motivations, pain points | 5–12 per segment | 30–60 min each | Themes, personas, journey maps |
| **Field study / contextual inquiry** | Observing users in their real environment | 4–8 sessions | 1–3 hrs each | Workflow maps, environmental constraints |
| **Diary study** | Understanding behavior over time (habits, frequency) | 10–20 | 1–4 weeks | Behavior patterns, trigger points |
| **Card sorting** | Information architecture — how users group concepts | 15–30 | 20–30 min each | Dendrograms, IA structure |

### Evaluative Research (Test solutions, find usability issues)
| Method | Best for | Participants | Time | Output |
|--------|----------|-------------|------|--------|
| **Usability test (moderated)** | Finding *why* users struggle with a flow | 5 per segment | 45–60 min each | Usability issues ranked by severity |
| **Usability test (unmoderated)** | Quick validation of simple flows | 20–50 | 15–20 min each | Completion rates, click paths |
| **A/B test** | Comparing two live versions with real users | 1K+ | Days to weeks | Statistical winner by metric |
| **Heuristic evaluation** | Expert review against usability principles | 1–3 evaluators | 2–4 hrs each | Severity-rated issues list |
| **First-click test** | Is navigation intuitive? | 50+ | 5 min each | % correct first click per task |

### Quantitative Research (Measure, benchmark, segment)
| Method | Best for | Participants | Time | Output |
|--------|----------|-------------|------|--------|
| **Survey** | Attitudes, satisfaction, feature preferences at scale | 100–1K+ | 5–10 min each | Statistical distributions, segments |
| **Analytics review** | Actual behavior at scale (what users do, not say) | All users | Ongoing | Funnels, cohorts, retention curves |
| **A/B test** | Causal impact of a specific change | 1K+ per variant | 1–4 weeks | Lift + confidence interval |
| **Tree test** | Validate IA without visual design influence | 50+ | 10 min each | Task success rate, directness |

---

## 2. Usability Test Script Template

```
┌─────────────────────────────────────────────────────────┐
│              USABILITY TEST SCRIPT                       │
│  Study: [Name] | Date: [ ] | Moderator: [ ]             │
└─────────────────────────────────────────────────────────┘

SECTION 1: INTRODUCTION (5 min)
─────────────────────────────────
"Hi [Name], thanks for joining. I'm [Name] from [Company].
We're testing [product/feature] — not testing YOU.
There are no wrong answers. Please think out loud as you go.
With your permission, I'll record this session.
Do you have any questions before we begin?"

→ Start recording.
→ Ask participant to share screen (if remote).

SECTION 2: WARM-UP (3 min)
─────────────────────────────────
"Tell me a little about yourself."
- What's your role?
- How do you currently [do the task this product addresses]?
- What tools do you use for that?

SECTION 3: TASKS (30–40 min)
─────────────────────────────────
[For each task, read the scenario aloud. Do NOT explain the UI.]

TASK 1: [Scenario]
Scenario: "Imagine you [realistic context]..."
Success criteria: [What does completion look like?]
Follow-up probes:
  - "What are you looking at right now?"
  - "What do you expect to happen when you click that?"
  - "Is this what you expected to see?"

TASK 2: [Scenario]
...
TASK 3: [Scenario]
...

SECTION 4: DEBRIEF (5–10 min)
─────────────────────────────────
- "On a scale of 1–7, how easy was this to use?"
- "What was the hardest part?"
- "If you could change one thing, what would it be?"
- "Is there anything else you'd like to share?"

→ Stop recording.
→ Thank participant. Process incentive.
```

### Observation guide (for note-takers)
During the session, log:
- **Path deviations:** Where did they go off the happy path?
- **Verbatim quotes:** Exact words for frustration, delight, confusion
- **Non-verbal cues:** Hesitation, scrolling up/down repeatedly, sighs, smiles
- **Time on task:** How long did each task take vs expected?

---

## 3. User Interview Guide — 10 Open-Ended Questions

### Interview structure (45–60 min)
```
00:00–05:00   Introduction (same as usability test intro)
05:00–10:00   Context & background
10:00–40:00   Core questions (below)
40:00–45:00   Wrap-up
```

### Core questions (with probing follow-ups)
```
1. "Walk me through a typical [day/week] at work."
   → "What's the first thing you do?"
   → "What takes up most of your time?"

2. "Tell me about the last time you [did the task we care about]."
   → "What triggered you to do that?"
   → "Walk me through it step by step."

3. "What's the hardest part about [task]?"
   → "Why is that hard?"
   → "What have you tried to make it easier?"

4. "What tools or workarounds do you use for this?"
   → "What do you like about [tool]?"
   → "What does it NOT do that you wish it did?"

5. "If you had a magic wand, what would the ideal solution look like?"

6. "Who else is involved when you do [task]?"
   → "What's their role?"
   → "How do you coordinate with them?"

7. "What would happen if you couldn't do [task] at all?"
   → [Probes for severity, workarounds, downstream impact]

8. "Have you ever paid for a solution to this problem?"
   → "How much?"
   → "What made it worth paying for?"

9. "How has [task/need] changed over the last year?"
   → [Probes for trends, growing/shrinking importance]

10. "Is there anything I should have asked but didn't?"
```

### Interview anti-patterns
- ❌ "Would you use a feature that does X?" (hypothetical, biased)
- ❌ "Do you like this design?" (social desirability bias)
- ❌ Leading questions: "Don't you find that frustrating?"
- ✅ "Tell me about a time when…" (behavioral, grounded)
- ✅ "Show me how you…" (demonstration, not description)

---

## 4. Survey Design Principles

### Question types and when to use
```
| Type              | Example                                | Use for                     |
|-------------------|----------------------------------------|-----------------------------|
| Likert scale      | "Rate 1–7: How easy was..."           | Attitudes, satisfaction     |
| Multiple choice   | "Which of these do you use most?"     | Categorical data            |
| Single choice     | "What's your primary role?"           | Segmentation                |
| Ranking           | "Rank these features by importance"   | Prioritization              |
| Open text         | "What's one thing we could improve?"  | Qualitative color, verbatims|
| Semantic diff.    | "Modern [1–7] Outdated"               | Brand perception            |
| Net Promoter      | "How likely to recommend? (0–10)"     | Loyalty, word-of-mouth      |
| MaxDiff           | "Which is MOST/LEAST important?"      | Trade-off analysis          |
```

### Bias avoidance checklist
- [ ] No double-barreled questions ("Is the app fast and easy to use?")
- [ ] No leading questions ("How much do you love our new feature?")
- [ ] Balanced scales (equal positive/negative options, neutral midpoint)
- [ ] Randomize answer order (for non-ordinal choices)
- [ ] Include "Not applicable" option
- [ ] Demographic questions at END, not beginning
- [ ] Attention check: "Select 'Somewhat agree' for this row"

### Sample size calculator (minimums)
```
| Population | ±5% margin | ±3% margin | ±1% margin |
|------------|-----------|-----------|-----------|
| 1,000      | 278       | 516       | 906       |
| 10,000     | 370       | 964       | 4,899     |
| 100,000    | 383       | 1,056     | 8,762     |
| 1,000,000  | 384       | 1,067     | 9,513     |

Confidence: 95%. For qualitative surveys, N ≥ 30 per segment is a practical minimum.
```

---

## 5. Research Synthesis Frameworks

### Affinity Mapping (5-step process)
1. **Transcribe:** Write one observation/quote per sticky note (yellow = observation, blue = quote, pink = insight)
2. **Cluster:** Group related notes silently (no talking)
3. **Label:** Name each cluster with a theme (e.g., "Onboarding is confusing")
4. **Prioritize:** Vote on clusters by importance × frequency (each person gets 5 dots)
5. **Synthesize:** Write one insight statement per top cluster: "[User type] needs [need] because [reason]"

### Journey Map Template
```
| Stage      | AWARE    | CONSIDER  | ONBOARD  | USE       | ADVOCATE  |
|------------|----------|-----------|----------|-----------|-----------|
| Actions    | Reads    | Signs up  | Connects | Creates   | Shares    |
|            | blog     | for trial | data     | dashboard | w/ team   |
| Thoughts   | "Can this| "Will it  | "This is | "I need   | "Others   |
|            |  solve?" |  work?"   |  complex"|  more X"  |  should"  |
| Emotions   | 😶       | 🤔        | 😤       | 🙂        | 😍        |
| Touchpoints| Blog,    | Website,  | App,     | App,      | Email,    |
|            | LinkedIn | sales call| docs     | support   | referral  |
| Pain pts   | Hard to  | Pricing   | Setup    | Missing   | No share  |
|            | compare  | unclear   | takes hr | feature Y | button    |
| Opportuni- | Compari- | Trans-    | Guided   | In-app    | Referral  |
| ties       | son page | parent $  | setup     | feedback  | program   |
```

### Persona Creation Template
```markdown
# Persona: [Name]

**Role:** [Job title + industry]
**Company size:** [e.g., 50–200 employees]
**Goals:** [1–2 primary goals they're trying to achieve]
**Frustrations:** [1–2 biggest pain points with current workflow]
**Behaviors:** [Tools they use, frequency, triggers]
**Decision criteria:** [How they evaluate solutions]
**Quote:** "[Verbatim quote that captures their mindset]"

**Day in the life:**
- [Morning routine + tools]
- [Core work activity]
- [Collaboration/communication patterns]
- [End-of-day wrap-up]
```

---

## 6. Research Repository Structure

Organize every study with this folder structure:

```
research/
├── 2026-Q3-onboarding-redesign/
│   ├── 01-study-plan.md          ← Research questions, method, screener, timeline
│   ├── 02-recruitment/
│   │   ├── screener.md           ← Screening questionnaire
│   │   └── participant-list.md   ← Anonymized participant roster
│   ├── 03-raw-data/
│   │   ├── interview-transcripts/
│   │   ├── session-recordings/   ← Links, not files (GDPR-aware)
│   │   └── survey-responses.csv
│   ├── 04-analysis/
│   │   ├── affinity-map.png
│   │   ├── theme-taxonomy.md
│   │   └── journey-map.png
│   ├── 05-findings.md            ← Top findings, severity, evidence
│   ├── 06-recommendations.md     ← Actionable recommendations with priority
│   └── 07-impact.md              ← What changed because of this research?
├── 2026-Q2-search-enhancement/
│   └── ...
└── templates/
    ├── study-plan-template.md
    ├── usability-script-template.md
    ├── interview-guide-template.md
    └── findings-report-template.md
```

### Findings report template (05-findings.md)
```markdown
# [Study Name] — Findings

**Date:** [Range] | **Method:** [e.g., Moderated usability test] | **N:** [Number]

## Executive Summary
[3–4 sentences: what we studied, top insight, key recommendation]

## Findings

### Finding 1: [Headline — the insight, not the observation]
**Severity:** Critical / High / Medium / Low
**Evidence:** "3/5 participants [behavior]..." + [verbatim quote]
**Recommendation:** [What should change]

### Finding 2: [Headline]
...
```

---

See also: UX Researcher skill for study design, recruitment, and insights delivery.
