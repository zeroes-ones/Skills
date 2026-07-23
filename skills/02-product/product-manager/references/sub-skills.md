# Sub-Skills

<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `problem-discovery` | Stakeholder/user interviews, problem framing | Phase 1 — problem statement, success metrics, cohort segmentation |
| `prd-writing` | Feature definition, requirements documentation | Phase 2 — executive summary, user stories, NFRs, edge cases |
| `rice-prioritization` | Backlog grooming, roadmap decisions | Phase 3 — Reach × Impact × Confidence / Effort scoring |
| `roadmap-communication` | Stakeholder updates, executive reviews | Phase 4 — Now/Next/Later, problem-focused, stakeholder summaries |
| `delivery-partnership` | Sprint execution, unblocking, launch validation | Phase 5 — standups, demos, launch metrics, post-launch retro |
| `okr-setting` | Goal cascading, measurable outcomes | `ceo-strategist` — North Star alignment, KPI definition |
| `competitive-analysis` | Market positioning, feature gap analysis | `business-strategist` — win/loss, feature comparison |


### War Story 1 — The 50-Page PRD Nobody Read
**Symptom:** A PM spent 3 weeks writing a 50-page PRD for a new onboarding flow. Engineering spent 2 days reading it, asked 30 clarifying questions, and built something different from what the PM intended. The feature took 2x longer than estimated.
**Root cause:** The PRD was written in isolation, shared as a "final" document, and assumed the reader would fill in the gaps. No early review cycles, no async comment period, no acceptance criteria in a testable format.
**Fix:** Adopted the "Minimum Viable PRD" approach: 5-page maximum, executive summary first, GIVEN/WHEN/THEN acceptance criteria for every story, async review mandatory before any sync meeting. PRDs became collaboration tools instead of approval artifacts.
**Lesson:** PRD quality isn't measured by page count — it's measured by how few questions engineers need to ask after reading it.

### War Story 2 — The RICE Score That Lied
**Symptom:** A team used RICE scoring religiously. The highest-scored feature had a RICE of 320 — 3x the next candidate. They built it over 2 quarters. It got 50 users in the first month, not the 5,000 they modeled.
**Root cause:** The Reach estimate was based on "all logged-in users will see this" (50K/month) rather than "users who need and will act on this" (200/month). Confidence was set at 80% because "we have analytics" — but the analytics didn't measure intent.
**Fix:** Introduced confidence tiering: 20% (gut), 50% (qualitative data), 80% (quantitative proxy), 100% (proven in market). Any feature with Confidence < 80% required a validation sprint before full build. Punted 60% of the backlog.
**Lesson:** RICE is only as good as its inputs. A feature with RICE 100 at 80% confidence beats RICE 300 at 20% confidence every time. Invest in confidence accuracy.

### War Story 3 — The Ship Date That Was Set Before Engineering Saw the Spec
**Symptom:** The CEO committed a "Q2 launch" date to the board based on the PM's estimate. Engineering saw the PRD in April, estimated 6 months. The PM was blamed for the miss. The launch slipped by 2 quarters.
**Root cause:** The PM estimated without engineering input. The spec was incomplete (no edge cases, no error states, no non-functional requirements). Engineering's real estimate was 4x the PM's guess.
**Fix:** Established a "no dates without engineering review" policy. Roadmap uses Now/Next/Later. PMs can say "we're targeting Q2, pending engineering validation." Built a spec review step: engineering estimates after they've read the full spec, not after a 5-minute pitch.
**Lesson:** Dates set without engineering input are not estimates — they're wishes. Always get engineering's estimate after they've read the full spec.
