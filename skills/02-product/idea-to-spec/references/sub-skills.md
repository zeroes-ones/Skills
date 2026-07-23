# Sub-Skills

<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `prd-writing` | Feature definition, stakeholder alignment | Phase 2 — scope brief, success metrics, non-goals |
| `domain-modeling` | Entity design, data relationships, state machines | Phase 2 — ERD, data dictionary, cardinalities |
| `api-contract-design` | Endpoint definition, error schemas, pagination | Phase 3 — OpenAPI 3.1 spec, idempotency |
| `screen-inventory` | Screen enumeration, state mapping, interaction design | Phase 4 — loading/empty/error/edge states |
| `story-mapping` | Work breakdown, sequencing, dependency ordering | Phase 5 — user stories, acceptance criteria |
| `rfc-process` | Cross-team spec review, async approval | `product-manager` — stakeholder alignment |
| `accessibility-requirements` | WCAG integration into screen specs | `accessibility-auditor` — heading hierarchy, focus management |


### War Story 1 — The 30-Page Spec That Collided With Reality
**Symptom:** A PM wrote a comprehensive 30-page spec for a new billing system, covering 12 API endpoints, 5 screens, and 3 integration touchpoints. Engineering started building and discovered 8 unhandled edge cases in the first week. The spec was rewritten 3 times during the sprint.
**Root cause:** The spec was written in isolation with no engineering review, no API contract validation, and no state-machine modeling for the billing entity. Edge cases (prorated refunds, mid-cycle plan changes, failed payment recovery) were assumed to be "standard" — but the existing system handled each one differently.
**Fix:** Adopted a "spec roughening" process: write a 5-page scope brief first, review with engineering async for 48 hours, THEN expand to full spec. Include entity state machines and API response schemas before writing user stories.
**Lesson:** A spec written without engineering input is a hypothesis, not a specification. Get engineering eyes on the scope brief before expanding. State machines and API contracts catch more edge cases than prose ever will.

### War Story 2 — The API That Looked Great on Paper
**Symptom:** A team designed a RESTful API for a content management system with beautiful resource hierarchy: `/organizations/{id}/projects/{id}/documents/{id}/versions/{id}`. The frontend team needed to render a document list — 4 nested API calls to get all documents across all projects. Page load time: 8 seconds.
**Root cause:** The API was designed around the data model, not the UI consumption patterns. The spec perfectly modeled the domain but ignored the primary query pattern: "show me all my recent documents."
**Fix:** Added denormalized read endpoints (`GET /documents?sort=updated_at`) and specified response schemas that matched screen data requirements. API contract review now includes a "top 3 UI queries" validation before approval.
**Lesson:** API design must serve both the domain model AND the UI consumption model. If the spec's API contract doesn't support the screen inventory's primary query, the spec is incomplete.

### War Story 3 — The Empty State That Wasn't Designed
**Symptom:** A spec for a team dashboard described the main view in full detail: charts, filters, data tables. What it didn't describe: what the dashboard looked like before the user had any data. The engineering team built a blank white page. Users thought the app was broken.
**Root cause:** The spec only defined the happy path. The loading state, empty state, error state, and permission-denied state were all left as "standard" — but there was no standard defined for any of them.
**Fix:** Made a "states-first" rule: every screen spec must define loading, empty, error, and permission-denied states before the happy path is described. Added a mandatory checklist to the spec template.
**Lesson:** The happy path is the smallest part of the spec. Loading, empty, error, and edge-case states are where the real design complexity lives. Define them first — they're the states users actually see.


### Error Decoder
<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Stakeholder rejects spec | Spec solves wrong problem or misses context | Run "Five Whys" with stakeholder before writing. Confirm problem statement in writing before solution. | A spec that solves the wrong problem is worse than no spec. Validate the problem before proposing the solution — every hour spent on problem definition saves days of rework. |
| Dev estimates don't match spec | Spec has hidden complexity, missing edge cases | Every screen needs loading/empty/error/edge states defined. Ambiguity → estimate buffer. | Every unstated edge case becomes a 2x multiplier on estimates. Loading, empty, error, and edge states are not optional — they are the difference between a spec and a wish. |
| Users don't use the feature | Built what was asked, not what was needed | Outcome-based specs: "increase X by Y%" not "build Z". User research before writing. | Building what was asked is not the same as building what is needed. Outcome-driven specs force you to ask: will this change user behavior? If "I hope so" is the answer, go back to research. |
| Scope creep during build | Spec didn't define explicit non-goals | "Out of scope" section is non-negotiable. Refer back when scope tries to expand. | Non-goals are the most important section of a spec. Without them, every feature request sounds reasonable in isolation. Define what you are NOT doing — and defend it. |
| No adoption after launch | Success metric not validated before building | Define success metric before writing first user story. Validate with prototype before building. | A success metric defined after launch is not a goal — it is a rationalization. Define "what good looks like" in measurable terms before writing a single user story. |
| Cross-team dependency blocks delivery | Spec assumed dependencies would be available | Map all dependencies with owners and dates in the spec. Flag red dependencies to PM weekly. | A dependency with no named owner and no deadline is not a dependency — it is a hope. Every external dependency needs a DRI and a check-in date embedded in the spec. |
| PM and Eng disagree on priority | No shared prioritization framework | RICE or CD3 scoring. Written framework removes opinion-based priority fights. | Priority arguments exhaust teams because they are personal. A written scoring framework removes the person from the argument and lets data decide. |
