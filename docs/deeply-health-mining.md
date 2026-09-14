# Mining Deeply-Health — Transferable Lessons for This Skill Library

**Source:** `/Users/sp.vm/Documents/Projects/Deeply-Health` — a production health app (iOS, Android, React Native, Next.js, Python/FastAPI backend), ~320k words of docs, ~207k words of native code, 15 ADRs, a live design-token pipeline.

**Method:** 11 parallel deep reads of the highest-value doc clusters (learnings, design system, UI/UX practice, theming/motion, onboarding/parity, ADRs, health-specific, native access control, strategy, mobile architecture, testing/codegen), then mapped against this library's existing skills.

**Purpose:** identify what a real production team learned that our generic skills do *not* teach, and where our skills would actively give wrong advice.

---

## 1. The headline finding

Deeply-Health's own organising statistic is the most transferable thing in it:

> **8 defects found by compilers, 2 more by decoding real data, 1 by reading** — zero of 22 found by careful review.

Every lesson below is downstream of that ratio. Our library currently teaches *review, discipline, and checklists*. The evidence from a team that shipped says the highest-yield verification is **mechanical, executable, and proven to fire** — and that reading is the weakest signal.

This does not invalidate our skills; it relocates their centre of gravity.

---

## 2. The highest-value findings, ranked

### F1 — A gate that reports CLEAN is not evidence it works

The single strongest rule encountered, stated independently in **four** of the eleven source clusters (learnings, design gates, access control, testing). The concrete failure: a stability gate reported clean **while two compilers were failing**, because it compared raw names on both sides and thereby validated a mismatch as consistent. Its first run also produced 28 false positives.

The discipline: every gate ships with **regression tests proving it fires** on injected input and stays **silent** where it should; a 0-error compiler run needs a **negative control**; and a rule whose threshold no longer fires is worse than no rule.

> **Our gap:** `verification-independence-engineer` teaches *who* verifies. Nothing teaches *how to prove a verifier works*. Our own repo is the proof: we shipped a G6 gate that grepped output instead of trusting an exit code, and a G8 that counted headings instead of checking for trees. Both passed for months.

### F2 — Verify the artefact, not the configuration

A green build proves nothing about the bundle. Real instances: a localisation directory declared but never a **target source**, so translations shipped nowhere and the app rendered raw keys — with no warning; an Info.plist key declared in config and silently dropped because only known keys inject; entitlements correct in file *and* setting, but the signature carried an **empty dict**.

The check is a command against the built artefact (`plutil -p`, list `.lproj` dirs, compare the APK's resource table against source).

> **Our gap:** `shipping-and-launch` and `verification-before-completion` both stop at "tests pass / build succeeds." Neither teaches "inspect the shipped artefact for the thing you configured."

### F3 — The verification ladder, with a "does NOT catch" column

Four rungs, and you cannot skip: **written → compiles → decodes real data → `--check` in CI.** The value is the *negative* column — each rung's blind spot is explicit.

Concrete payoff: two bugs that compiled cleanly (a nullable union widened to opaque; a `$ref` dereferenced too early) drove opaque wrapper occurrences from 131 → 51, reclaiming real types on ~80 fields. **Only decoding a captured live response finds these.** And the fixture must be captured from the live API — *"a hand-written sample encodes the same assumptions as the generator."*

> **Our gap:** we teach "add a test." We do not teach that compiling is rung 2 of 4, nor that a mock fixture proves nothing about the real wire format.

### F4 — An interface that cannot express an operation cannot be tested for it

`SessionStore` declared `hasSession` and `clear` but **no `save`**. Android implemented the port faithfully and never persisted a session. Nothing caught it: both compilers, **214 green tests** (the fakes mirrored the omission), all five gates, two green builds — iOS passed only because it **bypassed the port entirely**.

The transferable question: **"who WRITES this?"** — ask it of any state something else depends on reading.

> **Our gap:** this is a genuinely missing diagnostic. It is not code review, not testing, not architecture. It is *contract-completeness review*, and no skill in 324 owns it.

### F5 — Parity is not "both build"; it is "both checked for the thing that differs"

When a platform supplies a default, the **other** platform is where you look. `enableEdgeToEdge()` is mandatory at API 35, so every Android screen must opt in to the safe area while SwiftUI applies it unless a view opts out — same code, defect on one side, both builds green, *"a CTA under the navigation bar is unreachable."* Same shape twice more.

> **Our gap:** `mobile-developer` and `platform-hig-architect` discuss platform differences conceptually. Neither teaches the *probe*: "which platform gets this by default, and what does the other one have to remember?"

### F6 — A design doc that is hand-written will lie; generate it

The clearest cautionary tale in the corpus. `tokens.json` + generated `tokens.md` are live and correct. `accessibility.md`, `components.md`, `screens.md` are hand-written, four months stale, and **document a red brand that was never shipped** — while the app renders amber. A team mining those files naively would learn an abandoned palette.

The fix was not discipline; it was making `tokens.json` the source and generating the human doc from it, with CI failing on drift.

> **Our gap:** every one of our 324 skills is a hand-written doc. We now have three gates against drift *within* a skill (duplication, domain, templates) but none against a skill's claims drifting from reality.

### F7 — Three token tiers, and the middle tier is mandatory because the bottom tier compiles

Primitive (`charcoal`) → semantic role (`background`/`onBackground`) → component role (`buttonLabel`). The failure: on iOS the raw ramp is exposed as `Color.deeplyCharcoal`, which **compiles, renders correctly on a dark device, and is unreadable in light mode.** The literal-detection linter looked for hex literals, not wrong-but-real tokens. Nothing caught it; the reviewer's phone was dark.

The fix: `check-theme-compliance.py` reads palette keys **from the generated token file** so it cannot drift from the compiler's view — and was shown failing on a reintroduced violation.

> **Our gap:** we have no design-system skill at all. `ui-ux-designer` covers component spec and handoff; nothing owns token architecture across platforms.

### F8 — Separate the target you document from the floor you enforce

The project documents ≥90% critical / ≥80% general coverage. CI enforces **35/35/10**. The real lever is elsewhere: Codecov **patch** coverage at 80% (changed lines must be covered) with a **1%** project-drop tripwire.

The rationale is the transferable part: a high absolute number invites assertion-free tests; a low tripwire plus a high patch bar gets the behaviour you want.

> **Our gap:** we have no testing-strategy skill that distinguishes documented targets from enforced floors — and our own repo has the same split undocumented.

### F9 — Coverage percentage is not the quality signal; a named test per named behaviour is

`check-testability.py` **explicitly refuses** to enforce coverage, refuses tests for pure presentation, and demands: every view model has a test, every domain use case has a test. Its stated reason: *"A number can be satisfied by assertion-free tests; a named test for a named behaviour cannot."*

Paired artefact: a **behaviour-named test table** — `Test | The defect it guards` — 8 rows, each cross-referenced to the shipped bug it would have caught.

> **Our gap:** `tdd-guide` and `qa-engineer` discuss coverage targets. Neither teaches "name the test after the defect it guards."

### F10 — Commit generated code, and replace the lost freshness guarantee with a drift gate

This **inverts** the standard advice. The reasoning is explicit: committing gives a reviewable diff, an offline build, and no generator-version dependency in CI — *then* add `--check` that regenerates in memory, compares, and exits non-zero on any diff.

Also: *"if a generator writes into the repo, that file belongs in the repo. **Untracked-and-unused is the worst of both**."*

> **Our gap:** nothing in our library addresses generated-artefact discipline, and this is a case where the textbook advice is wrong for a common setup.

### F11 — A one-way consistency check is a silent rot vector

`spec-gap-check.py` is bidirectional, and names the exact failure: the reverse direction *"used to be a deliberate no-op, which is how the spec silently fell to 41 documented paths while the API served 114."*

> **Our gap:** our own `emit-*-check.py` gates are freshness checks (one direction). We do not check that every skill is *reachable* by the corpus that claims to reference it.

### F12 — Rules can each be locally correct and jointly contradictory

The most generalisable idea found. A scope had **no legal spelling**: `ios/DeeplyDomain` + `internal` failed a rule requiring explicitness *and* a rule banning redundancy. The encoded invariant: *"every scope must have a legal spelling in every tree."*

Also: *"a gate that cries wolf gets ignored, and an ignored gate is worse than no gate."* Their design gate policed every raw colour and reported 80 violations, mostly legitimate scrims — resolved by two tiers (strict inside the design system, duplication-only elsewhere) rather than one noisy rule.

> **Our gap:** we have never checked whether our own rules can contradict. Our `--delta` grandfathering and our 12-vs-22 section mismatch were exactly this class of defect.

### F13 — Stop fixing, start ruling out layers

A stuck spinner consumed three fixes (two genuine but irrelevant) before someone waited past the transport's own timeout and got **no error at all** — *"a request that never starts cannot fail"* — which ruled out networking in one step. The document notes the evidence *"was available the whole time."*

> **Our gap:** `debugging-and-error-recovery` teaches triage but not the **layer-elimination** move: find the observation that eliminates a whole layer, rather than fixing the next plausible cause.

### F14 — Retention loops have a mortality order, and cold-start is existential

*"The order matters more than the features: cold-start and 'less alone' before insight, insight before the two-sided network."* And critically: **a member who sees an empty feed never returns** — so recruit 20–50 founding members per pod *before opening*, with the target metric being **time-to-first-meaningful-connection < 48h**, not signups.

> **Our gap:** `community-operations-manager` measures time-to-first-*response* (<1h), a weaker metric. `marketplace-platform-builder` has the seeding instinct scoped only to marketplaces.

### F15 — Never paywall the retention engine

The highest-value insight feature (doctor-visit prep) must be **free**, because gating it *"pays for retention with churn."* This **contradicts** the standard freemium playbook, which identifies the highest-WTP feature and gates it. The project additionally prohibits ads outright, with a stated reason: *"your attention is the product"* kills the trust that is the wedge.

> **Our gap:** `saas-monetization-strategist` teaches conversion-trigger gating and would recommend gating exactly the wrong feature.

### F16 — Treat the cacheable prefix as a frozen build artefact

A **5-character edit** to the always-loaded context file turns a `$0.0141` request into `$0.0216` — **25× on the prefix portion**. Measured: a frozen prefix saves ~35% of input cost, ~$270/year at 100 req/day. Enforcement is mechanical: `git diff` against HEAD must be empty.

Paired with a **saturation ladder** with per-layer token budgets and an explicit **15%/10% buffer row**, and a **NEVER-compact list** — six security invariants that must survive every eviction.

> **Our gap:** `token-efficiency` says "verify the prefix diff is empty, hit-rate ≥60%." It does not quantify the cost of an edit, nor frame prefix edits as review-gated events, nor require a named do-not-drop list.

### F17 — Validate lossy compression with constraint probes, not topic coverage

Extract every named constant, version, and threshold from the source (25 of them), then check each survives compression. Report `kept/N` against a ≥90% gate. The project scored 25/25 at 51% byte reduction.

> **Our gap:** we set the same ≥90% gate in `token-efficiency` but specify no probe method. Pulling named values out and checking each is the actionable technique.

### F18 — Compaction is a quality optimisation, not a cost optimisation

Reactive compaction at 95% is treated as a **defect**: *"the summarizer runs on a nearly-full context, produces lower-quality output, and the agent already suffered 15 turns of diluted attention."* The goal is staying in the optimal attention band (30–55% of window).

> **Our gap:** our framing is cost-first. This inverts the priority correctly.

### F19 — Capability gating is derived on the client, enforced on the server

A real hole: a lupus-only (email-verified) user could POST bleed logs, because the endpoint checked verification and ownership but not capability. **Presentation metadata is not authorization.** The fix adds `require_capability(...)` to every tracker endpoint, plus a 403 test.

Companion rule: **separate capabilities from data models.** Two conditions shared one model, so sickle-cell vaso-occlusive crises were stored as "bleeds" with the wrong fields. The bug is invisible until someone asks *"is this the same event?"*

> **Our gap:** `iam-architect` and `secure-api-design` teach authorization models. Neither teaches the specific audit: "enumerate every endpoint, and ask which capability it requires — separately from what the client chose to render."

### F20 — An honest assessment names what it has NOT verified

The project's self-assessment has an explicit **unverified section**, uses **"Not built yet" rather than a mock** so the gap is visible, and reports *"P0 gates closed: 0 of 85"* without softening.

> **Our gap:** our `*-benchmark.md` docs model this for the library, but no skill teaches it as a product practice.

---

## 3. Where our skills would give actively wrong advice

| Our skill | What it teaches | What the evidence says |
|---|---|---|
| `saas-monetization-strategist` | Gate the highest-converting feature | Gate nothing that drives retention; the most compelling feature must be free |
| `tdd-guide`, `qa-engineer` | Aim for a coverage target | Coverage invites assertion-free tests; gate *patch* coverage high and absolute low, and require named tests per behaviour |
| `marketplace-platform-builder` | Seed supply before demand | Right, but needs the *quota* (20–50 per pod) and the metric change (time-to-first-*connection*) |
| `community-operations-manager` | Time-to-first-response <1h | First response ≠ first meaningful connection; target <48h to connection |
| `ui-ux-excellence`, `ui-ux-designer` | Use tokens; keep docs in sync | The raw primitive **is** a compilable token; you need a *role-level* gate reading from the generated source |
| `token-efficiency` | Keep the prefix stable (advisory) | Quantify the edit (25× on prefix), make prefix edits review-gated, add a NEVER-compact list |
| `context-engineering` | Compact when the window fills | Reactive compaction at 95% is a defect; compact proactively at 70% |
| `mobile-developer` | Handle platform differences | Parity means *both checked for the thing that differs*, not both building |
| `verification-before-completion` | Verify the work | Verify the **artefact** (inspect the bundle), and prove the verifier fires |
| `on-device-ai-engineer` | Tier by device capability | Tier by **user share**, and make the fallback the existing product, not a degraded stub |
| — | *(no design-system skill exists)* | Token tiers, cross-platform role mapping, parity gates, monotonic type-scale checks |

---

## 4. Concrete upgrades this enables

Ranked by leverage. Each names the artefact to reproduce.

### U1 — New skill: `verifier-design` (or extend `verification-independence-engineer`)
The highest-value gap. Teaches: proving a gate fires (fire-case + silent-case tests, mutation testing, negative controls), the "clean is not evidence" rule, joint-rule contradiction checking, and gate severity calibration.
**Artefacts to reproduce:** the fire/silent regression-test pattern; the exhaustive *(scope × modifier)* matrix; the tiered-severity allowance.

### U2 — New skill: `design-system-architect`
We have none, and this is the richest cluster. Teaches: three token tiers with the role vocabulary bridging platforms, monotonic cross-platform type mapping with a rank assertion, size-vs-spacing axis separation, per-platform floor tokens declared rather than unified, role-level theming gates reading from the generated source, and every exemption carrying a reason.
**Artefacts to reproduce:** the component-spec template (Purpose · Anatomy · Variants · Sizes · States table · Accessibility with literal announced strings · Props · Edge cases); the contrast/role pairing table; the accent-derivation parameter table; the gate-script skeleton (what shipped broken → what it checks → what it deliberately does NOT check, with reasons → vocabulary read from generated source → fail loud if unreadable).

### U3 — New skill: `generated-artefact-discipline`
Teaches the codegen doctrine: generate the edges, hand-write the core with a load-bearing mapper; commit generated code when the generator carries a network/version dependency, then add `--check`; exclude generated trees from formatting so the drift gate stays authoritative; bidirectional consistency checks; and the rule that generating is not the same as generating *compiling* code.
**Artefacts to reproduce:** the source-of-truth → derived → verify-command table; the "what is verified / what is not" report table.

### U4 — New skill: `contract-completeness-review`
From F4. The single cheapest high-value diagnostic found: ask *"who WRITES this?"* of every piece of state; check every interface can express its operations; check whether one platform bypasses a shared contract.
**Artefact:** the defect table with a **"Found by"** column — which is what makes the discovery-ratio argument visible.

### U5 — New skill: `token-budget-discipline` (extends `token-efficiency`)
Per-layer budget table with buffer row, the 70/85/95 saturation ladder, the NEVER-compact enumerated list, the constraint-probe retention scorecard, prefix-edit-as-review-event, and measured prefix economics.
**Artefacts:** the ladder; the per-layer budget; the probe scorecard.

### U6 — Enrichments to existing skills (smaller, targeted)
| Skill | Add |
|---|---|
| `debugging-and-error-recovery` | Layer-elimination move: find the observation that rules out a whole layer |
| `qa-engineer` | Documented-target vs enforced-floor split; patch-vs-absolute coverage |
| `tdd-guide` | Behaviour-named tests cross-referenced to the defect they guard |
| `mobile-developer` | The parity probe ("which platform gets this by default?") |
| `frontend-developer` | "Suites passing is not evidence the UI is correct"; need a browser verdict |
| `saas-monetization-strategist` | The never-paywall-the-retention-engine rule |
| `community-operations-manager` | Seeding quota + time-to-first-connection metric |
| `healthcare-ui-designer` | Role-paired contrast (compute against the actual partner, not the page background); the medical-ID override block |
| `regulatory-specialist` | Capability-derived-on-client / enforced-on-server; capability ≠ data model |
| `ui-ux-excellence` | Severity-delta discipline; evidence tagging `[VERIFIED]` vs `[verify-in-browser]` |

### U7 — Add a gate class to our own tooling
The repo-level analogue of F1: every script in `scripts/` that is a *gate* should have a fire-case and silent-case test. We currently verify gate *plumbing* (they exit 0) but never that they would exit 1 on a real violation. We proved two of our own gates had never fired correctly.

---

## 5. What is NOT transferable

Recorded so it is not mined again:

* **Environment specifics** — JDK 26 vs 17, SwiftPM sandbox flags, a Kotlin daemon `FileSystemException`, an absent iOS SDK. Machine-specific. The one generalisable technique: when an environment restriction bites, **probe each construct individually** to find exactly which are affected.
* **Project business state** — the per-app gap list, roadmap contents, the 12–18 month phase plan, "P0 gates closed: 0 of 85".
* **The stale design docs' content** — `accessibility.md`, `components.md`, `screens.md` document a red brand that never shipped. Their *format* is valuable; their *values* are wrong.
* **Three internal inconsistencies** worth not copying: the project's own docs disagree on coverage numbers, on the destructive-action pattern (confirm dialog vs 5-second undo, authored the same day), and its CI runs the strongest design gates only in a bypassable pre-push hook.

---

## 6. The one-sentence takeaway

Deeply-Health's transferable core is not its palette, its stack, or its domain — it is a **verification culture**: gates that are proven to fire, artefacts inspected rather than assumed, contracts checked for completeness rather than consistency, and every exemption declared with a reason. Our library teaches discipline; this teaches *falsification*. That is the upgrade.
