# Sub-Skills

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
