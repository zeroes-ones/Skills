# Production Checklist

<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | Scope brief approved by product owner and tech lead with written sign-off | `grep -rn "approved\|sign.off\|reviewed.by" spec.md` → must find > 0 approval indicators with names | Template: `templates/spec.md` — requires approval section with name + date |
| **[S2]** | Non-goals explicitly documented and agreed upon — "Out of Scope" section present and reviewed | `grep -c "Out of Scope\|Non.Goals\|Not.Building" spec.md` → must be > 0 | Spec template enforces "Out of Scope" section before requirements |
| **[S3]** | Entity state machines cover all lifecycle transitions including rollback paths | `grep -c "state.machine\|lifecycle\|transition\|rollback\|status.*→" spec.md` → must find state definitions for all entities | Template: `templates/state-machine.md` — state diagram + transition table |
| **[S4]** | API contract includes error schemas for every 4xx and 5xx response | `npx @redocly/cli lint openapi.yaml` → must return 0; `grep -c "4[0-9][0-9]\|5[0-9][0-9]" openapi.yaml` → must find error response schemas | CI: `redocly lint openapi.yaml` in `.github/workflows/spec-lint.yml` |
| **[S5]** | Pagination, sorting, and filtering patterns are consistent with existing APIs | `grep -rn "pagination\|sort\|filter\|limit\|offset\|cursor" openapi.yaml` → must find consistent patterns matching existing API conventions | Lint rule: `scripts/check-api-consistency.sh` — flags pagination/sort parameters that differ from standard |
| **[S6]** | Every screen has defined loading, empty, error, and permission-denied states | `grep -c "Loading\|Empty\|Error\|Permission.Denied\|Edge.Case" spec.md` → must have ≥ 1 per screen/flow defined | Spec template: `templates/spec.md` — state matrix required per screen |
| **[S7]** | Story map ordered by dependency and value-to-effort ratio | `grep -rn "story.map\|user.story.*order\|dependency.*order" spec.md` → must find dependency graph or ordered story list | Template: `templates/story-map.md` — dependency matrix + value/effort scoring |
| **[S8]** | Each user story has at least 3 acceptance criteria in Given/When/Then format | `grep -c "GIVEN.*WHEN.*THEN" spec.md` → must be ≥ 3× (number of user stories) | Spec template enforces min 3 GIVEN/WHEN/THEN per story |
| **[S9]** | Open questions have assigned owners and due dates — no orphan questions | `grep -rn "question\|TBD\|TODO\|open" spec.md \| grep -v "owner\|assigned\|due" -A 2` → must find 0 questions without owner/date | Question tracker: `scripts/question-audit.sh` — flags open questions without owner or past due date |
| **[S10]** | Spec versioned and distributed for async review before any planning meeting | `grep -c "version\|changelog\|review.window\|review.period" spec.md` → must find version + 48h review window | Spec template auto-inserts version table and review deadline; `scripts/spec-review-reminder.sh` alerts at deadline |
