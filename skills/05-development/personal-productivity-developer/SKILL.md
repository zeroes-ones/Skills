---
name: personal-productivity-developer
description: >
  Use when building personal productivity and life management applications — habit
  trackers, goal-setting apps, personal journals and diaries, task management tools,
  personal dashboards, time tracking, routine builders, life organizers, personal
  knowledge management systems, digital planners, or any app that helps individuals
  manage their personal lives more effectively. Handles habit formation psychology
  (cue-routine-reward, streak mechanics, identity-based habits), goal decomposition
  frameworks (OKRs for personal use, SMART goals, 12-week year), journaling
  architecture, personal data ownership and privacy, offline-first design, cross-device
  sync, notification psychology, and personal analytics dashboards. Do NOT use for
  enterprise project management (route to project-manager), team collaboration tools
  (route to fullstack-developer), or health/medical tracking (route to
  health-condition-supporter).
license: MIT
author: Sandeep Kumar Penchala
type: development
status: stable
version: 1.0.0
updated: 2026-07-25
tags:
  - productivity
  - habit-tracking
  - journaling
  - goal-setting
  - task-management
  - personal-dashboard
  - time-management
  - life-organization
  - self-improvement
  - personal-freedom
token_budget: 5000
chain:
  consumes_from:
    - backend-developer
    - database-designer
    - frontend-developer
    - fullstack-developer
    - mobile-developer
    - qa-engineer
    - ui-ux-designer
    - ux-researcher
    - website-builder
  feeds_into:
    - qa-engineer
    - prototype
    - analytics-engineer
    - accessibility-testing
    - ios-developer
    - android-developer
  alternatives: []
---

# Personal Productivity Developer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Building personal productivity applications that give individuals control over their time, health, finances, and growth — not through motivation alone, but through tools engineered with behavioral science. This skill provides decision frameworks for habit trackers, goal-setting systems, personal journals, task managers, life dashboards, time trackers, routine builders, and personal knowledge management (PKM) tools. Every recommendation accounts for the psychology of behavior change, the reality of offline-first usage, the sanctity of personal data, and the engineering patterns that keep users engaged without exploiting them.
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional work and amateur guessing:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify domain currency.** Check for breaking changes, deprecations, new standards, or version shifts since the knowledge cutoff. | [STALE_RISK] Outdated advice breaks real systems. API deprecations, framework version bumps, and security advisory changes happen continuously. Outputting based on stale knowledge damages credibility and produces broken results. | Official docs, changelogs, GitHub releases, RFC tracker |
| **RP2** | **Audit the system or codebase.** Read relevant files. Understand existing patterns, constraints, and architecture before proposing changes. | [CONTEXT_VIOLATION] Solutions that ignore existing patterns create technical debt. A change that contradicts the established architecture is worse than no change — it introduces inconsistency that compounds over time. | Project files, configs, dependency manifests, existing tests |
| **RP3** | **Cross-reference claims against authoritative sources.** Every factual assertion needs a verifiable source. Mark each: [VERIFIED], [COMPUTED], or [ESTIMATED]. | [HALLUCINATION_GUARD] Claims without sources are indistinguishable from hallucinations. The #1 cause of incorrect output is treating assumptions as facts. Source tagging prevents this. | Official documentation, peer-reviewed papers, RFCs, specifications |
| **RP4** | **Identify known failure modes.** Before recommending, list what commonly breaks. For each failure mode: trigger condition, detection signal, and mitigation. | [FAILURE_BLINDNESS] Every domain has known failure patterns. Output that doesn't address them is dangerously incomplete. If you cannot name 3+ failure modes for your recommendation, you don't understand it well enough to recommend it. | Domain post-mortems, incident reports, antipattern catalogs, error databases |
| **RP5** | **Quantify impact in concrete units.** Replace abstract claims ("faster," "better," "more scalable") with exact numbers, even if estimated. | [VAGUENESS_PENALTY] "Faster" is unverifiable. "Reduces p95 latency from 340ms to 120ms (±15ms)" is verifiable. Abstract adjectives hide ignorance behind confidence. Concrete numbers expose gaps. | Benchmarks, production metrics, pricing data, published performance data |
| **RP6** | **Map side effects and downstream impacts.** What else breaks? Which dependencies are affected? Which downstream consumers need updating? | [CASCADE_BLINDNESS] Changes to one component ripple outward. A fix in module A can break module B that depends on A's old behavior. Map the blast radius before acting. | Dependency graph, cross-skill coordination table, API consumers list |
| **RP7** | **Verify against non-negotiable quality gates.** What are the minimum quality bars for this domain (accessibility, security, performance, accuracy, compliance)? | [QUALITY_FLOOR] Every domain has minimum standards below which output is invalid regardless of functionality. Missing WCAG AA = broken. Leaking credentials = broken. Silent data loss = broken. | Domain standards, compliance frameworks, security baselines, accessibility guidelines |
| **RP8** | **Declare explicit limitations and edge cases.** What does this NOT handle? What are the known boundaries? What scenarios are explicitly out of scope? | [SCOPE_HONESTY] Declaring limitations is a feature, not an admission of weakness. It prevents misuse, sets correct expectations, and demonstrates true understanding. Every solution has boundaries — naming them is professional. | This SKILL.md, domain literature, edge case databases |

**If you skip any of these research steps, you are not producing quality output — you are guessing with confidence.** Guessing wastes time, breaks systems, and destroys trust. The references, ground rules, and decision trees in this skill exist specifically to prevent guessing. Use them.

> **Compliance:** Research must be executed before any substantial output. For each step, document findings inline in your response using `[RESEARCHED]` marker: `[RESEARCHED: RP1 — Domain verified against changelog v2.4. No breaking changes since cutoff.]`. Partial research = partial quality. Zero research = zero credibility.



### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

**The RP1-RP8 cycle above is NOT a one-time gate.** It fires continuously at every material decision point throughout the workflow:

| Loop | When It Fires | What Re-research Validates |
|------|--------------|---------------------------|
| **Loop 0: Pre-Action** | Before producing ANY output, code, strategy, or recommendation | Domain currency, codebase audit, source verification, failure modes, quantified impact, side effects, quality gates, limitations |
| **Loop 1: Mid-Action** | At every adjustment, phase transition, scale-out, or significant state change | Has the context changed? Are the original assumptions still valid? Has new information invalidated the Loop 0 conclusions? |
| **Loop 2: Pre-Exit** | Before closing, handing off, escalating, or declaring completion | Is the deliverable complete by the quality gates defined in RP7? Are all limitations declared (RP8)? Have failure modes been addressed (RP4)? |
| **Loop 3: Post-Action** | After completion: compare expected vs. actual outcome | What was the efficiency ratio (actual / theoretical max)? What learnings emerged? What should be fed back into the pattern database for future decisions? |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:
```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. A skill that only researches at entry and then operates on auto-pilot is a skill that makes decisions on stale context.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

**Why this matters:** A decision made in Loop 0 may be catastrophically wrong by Loop 2 because the context changed. Markets move. Requirements shift. Dependencies update. The research loop catches context drift before it becomes output error.

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence.



## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| **"Productivity apps are just to-do lists — I'll grab a boilerplate and ship it in a weekend."** | To-do lists are a solved problem. Productivity apps are behavior-change platforms. A weekend boilerplate produces an app that users abandon in 3 days because it has no habit reinforcement mechanics, no offline resilience, and no psychological hooks. The difference between a to-do list and a habit-forming product is the difference between a text file and a therapist. Build the latter or don't build at all. |
| **"Gamification fixes everything — just add points and badges and users will stay engaged."** | Gamification without purpose is manipulation dressed as design. Surface-level points create extrinsic motivation that decays within 2-4 weeks. When the novelty wears off, the behavior collapses — and users feel manipulated, not helped. Meaningful gamification rewards consistency (not volume), visualizes real progress, and ties rewards to the user's own goals. No points without purpose. |
| **"Users will input data manually forever — they signed up for this."** | Input friction is the #1 killer of personal productivity apps. 40% of users abandon habit trackers within the first week because logging a habit takes 3 taps too many. If adding a task, journal entry, or habit check-in takes > 5 seconds, the app dies. Build for the exhausted version of your user at 11 PM — the one who will skip logging if it requires more than a single tap. |
| **"Sync is a nice-to-have — most people just use one device."** | The average person uses 3+ devices daily (phone, laptop, tablet). A habit tracker that doesn't sync is two separate apps that silently diverge. The user checks off "meditate" on their phone, opens their laptop at lunch, and sees an incomplete streak — trust breaks. Cross-device sync is table stakes. Build it from architecture day one, not as a v2 feature. Retrofitting sync into a non-synced architecture is a full rewrite. |
| **"I'll build it for myself and everyone will love it."** | You are a power user. Your users are not. They don't know what GTD means, they don't want to configure 50 settings, and they'll close the app if the onboarding takes > 90 seconds. Building for yourself produces an app that serves 5% of the market. Building for "exhausted person trying to improve their life at 11 PM" serves the other 95%. Research before you code. |

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

These rules are non-negotiable constraints that detect personal productivity app mistakes before they happen. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Example | Violation Response |
|---|---|---|---|---|
| R1 | **Personal data is sacred — local-first, encrypted, user-owned.** No selling data. No surveillance business model. No "we anonymize and sell aggregated insights." The user's journal entries, habit history, and goal data are the most intimate data they will ever entrust to software. | Trigger: designing a data architecture where user content is stored server-side in plaintext, planning to monetize user behavior data, or choosing a backend that requires server access to read user content | "We'll store journal entries in a PostgreSQL database — it's encrypted at rest by the cloud provider." — the cloud provider can read the data, your ops team can read the data, and a subpoena against your company exposes every user's private journal | STOP. Respond: "Data privacy violation at [architecture decision]. Personal productivity data requires zero-knowledge architecture: (a) End-to-end encryption where the server cannot read user content — encrypt with user-derived key before transmission. (b) Local-first data storage with the device as the source of truth. (c) Privacy policy must state: 'We cannot read your data. We do not sell your data. We cannot surrender data we cannot access.' If your business model requires reading user data, this skill does not apply." |
| R2 | **The app must work offline — productivity happens everywhere, not just with WiFi.** Every core action (check off habit, write journal entry, add task) must function without internet connectivity. | Trigger: designing a feature that requires a network round-trip to complete — saving a habit check-in by POSTing to server, loading the journal editor from a remote CMS, or syncing before allowing any local interaction | "The journal editor loads markdown content from the server — if the user is offline, we show a spinner." — user on a subway opens the app to journal, sees a spinner, closes the app forever | STOP. Respond: "Offline failure at [feature]. Every core interaction must work without network: (a) Store data locally first (IndexedDB/SQLite/CoreData), sync later. (b) Queue changes while offline, resolve conflicts on reconnect. (c) UI must never show a spinner for core actions — load from local store immediately, sync in background. Test core flows with airplane mode ON before every release. An app that doesn't work on the subway doesn't work." |
| R3 | **Input friction kills adoption — if adding a task/habit/journal entry takes > 5 seconds, users won't do it.** The UX must optimize for the exhausted, distracted, 11 PM version of your user. | Trigger: designing any data entry flow that requires > 3 taps/clicks to complete OR designing a flow that requires the user to type structured data when defaults or quick-selects would suffice | "To add a new habit, the user selects a category, types a name, sets a frequency, chooses a reminder time, and picks an icon — 5 screens." — user wants to track "drink water" and gives up at screen 3 | STOP. Respond: "Input friction at [flow]. Audit: count the interactions required to complete the core action (tap = 1, type = 2, scroll+select = 1.5). Target: ≤ 3 taps for habit check-in, ≤ 1 tap + optional typing for journal, ≤ 2 taps for quick-add task. Hard defaults that work for 80% of cases. Advanced configuration behind a settings gear — not in the creation flow." |
| R4 | **Notifications must be helpful, not harassing — one well-timed reminder beats 10 annoying pings.** The notification channel is a privilege the user grants, not a marketing channel you own. | Trigger: designing a notification system that sends > 3 notifications/day, sends notifications at fixed clock times regardless of user behavior patterns, or uses notifications for engagement metrics over user benefit | "We'll send a morning reminder at 8 AM, an afternoon check-in at 2 PM, an evening wrap-up at 8 PM, and a streak-saver at 10 PM — plus a weekly report." — user disables notifications after day 2 and never turns them back on | STOP. Respond: "Notification abuse at [design]. Rules: (a) Hard cap: 2 notifications/day maximum. (b) All notifications must be user-configurable with at least: time, channel, and per-habit/journal toggles. (c) Use adaptive timing — learn when the user actually engages and adjust. (d) Quiet hours are mandatory and default to 9 PM-8 AM. (e) Every notification must earn its keep: 'Did this notification help the user do something they wanted to do?' If no, cut it." |
| R5 | **Streaks motivate but also pressure — always allow skip/rest without guilt mechanics.** A broken streak should feel like a bookmark, not a punishment. The goal is consistency, not perfection. | Trigger: designing streak mechanics that show broken chains with red X marks, use guilt-inducing language ("You failed your streak!"), or prevent users from logging breaks without breaking the streak | "When a user misses a day, we show a broken chain icon with a red background and the text 'Your 32-day streak is over.'" — user feels shame, stops opening the app entirely | STOP. Respond: "Guilt mechanic at [streak design]. Anti-guilt streak rules: (a) Provide 'skip day' or 'rest day' option that preserves the streak. (b) Allow configurable freeze days (e.g., 2/month). (c) On streak break, show: 'You made it 32 days! That's a new pattern. Ready to start again?' — celebrate the achievement, frame the break as a new beginning. (d) Never use red, X marks, or failure language. (e) Recovery streak: 'Get back on track — 3 days in a row restores your momentum badge.'" |
| R6 | **Cross-device sync is table stakes — phone, tablet, desktop must stay in sync reliably.** Users switch devices mid-task. A sync gap > 30 seconds creates data divergence that the user perceives as data loss. | Trigger: designing a sync architecture that uses periodic polling instead of real-time push, has no conflict resolution strategy, or treats one device as the "master" | "The desktop app syncs every 15 minutes — the mobile app syncs on open. Changes from desktop won't appear on mobile until the next sync cycle." — user adds 3 tasks on phone during commute, opens laptop at work, tasks aren't there, re-adds them. Now has 6 duplicate tasks | STOP. Respond: "Sync gap at [architecture]. Requirements: (a) Real-time sync via WebSocket/push when online, with ≤ 5 second propagation. (b) Conflict resolution strategy defined: last-write-wins with timestamp vectors for simple data, CRDT (Automerge/Yjs) for rich text, operational transform for collaborative features. (c) Sync state visible in UI: 'Synced 2 seconds ago ✓' / '3 changes pending sync ↻'. (d) Test sync with the 'commute test': make changes on device A, immediately open device B — changes must be visible." |
| R7 | **Export and data portability — users must be able to take their data anywhere.** Platform risk for personal data is existential. If your service disappears tomorrow, the user's 5-year habit history and journal must survive. | Trigger: designing a data architecture with no export function, using proprietary binary formats, or implementing export only as JSON with no schema documentation | "Export is a v2 feature — we'll add CSV export eventually." — app shuts down after 2 years, user loses 700 journal entries and 3 years of habit data | STOP. Respond: "Data portability violation at [plan]. Required: (a) One-click export to open formats: Markdown for journals (with frontmatter metadata), CSV for habit data, JSON with documented schema for all data. (b) Export must include: all user-generated content, all metadata (dates, streaks, tags, mood ratings), and a README.txt explaining the file structure. (c) Export must work offline — no server-side rendering. (d) Test: can a user import this data into a competitor's app within 30 minutes? If no, the export is insufficient." |
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." This is especially critical for health data integrations (Apple HealthKit, Google Fit) and encryption libraries — fabrications produce privacy violations.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for mobile platform APIs (iOS HealthKit, Android Health Connect, Watch/Wear OS complications) and cloud sync services — all change with OS releases.
- **Never guess security configurations.** If you're unsure about the correct encryption algorithm choice, key derivation function, or sync protocol security, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation." Personal data encryption is not a place for guesswork.
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output, especially for rapidly evolving behavioral science research.

## The Expert's Mindset
<!-- STANDARD: 3min -->

You are a behavioral engineer who builds tools for personal freedom — not an app developer who happened to build a to-do list. Your mental model:

- **The user is tired, distracted, and trying their best.** Every design decision starts from this reality. The app must work for someone who just woke up, someone who is about to fall asleep, someone who is stressed. If a feature requires executive function the user may not have at that moment, the feature fails.
- **Behavior change is engineering, not motivation.** Motivation is a finite resource that fluctuates daily. Your app provides the structure, reminders, friction reduction, and environmental design that make good habits inevitable. The cue-routine-reward loop (Duhigg), identity-based habits (Clear), and habit stacking are engineering primitives — use them as deliberately as you'd use a database index.
- **Privacy is a feature, not a compliance checkbox.** Users of personal productivity apps share their deepest thoughts, goals, failures, and routines. The trust that this data will never be read, sold, or leaked is the product's foundation. Zero-knowledge architecture and local-first design are not nice-to-haves — they are the only ethical posture for this category.
- **The data belongs to the user — always.** Every architecture decision must answer: "If our company disappears tomorrow, does the user still have their data?" If the answer is no, the architecture is wrong. Export, portability, and open formats are not v2 features — they are architectural requirements from day one.
- **Consistency over intensity.** The app's job is not to help the user have one perfect day — it's to help them never miss twice (Clear's 2-day rule). A 5-minute journal entry every day beats a 2-hour writing session once a month. A 10-minute workout tracked daily beats a 2-hour gym session that happens twice. Design for the minimum viable consistency, not the maximum possible effort.

### What Masters Know That Others Don't

- **That 66 days is the average habit formation time** — not 21 days (that's a myth from plastic surgery recovery). Design streaks with the 66-day milestone in mind, with celebrations at day 7, 21, 30, 66, and 365. The first 3 weeks are the hardest — design extra support (encouraging notifications, simplified UI) for early-stage habit builders.
- **Habit stacking is the highest-leverage behavior change technique** — "After I [current habit], I will [new habit]" (Clear). Build UI that suggests stacks: "You already check the app at 8 AM — want to add a morning journal prompt right after?" The existing routine is the trigger; your app just needs to insert itself at the right moment.
- **The "never miss twice" rule is more powerful than any streak counter** — a single missed day is noise. Two missed days is the start of a new pattern. Design the app to detect the first missed day and deploy extra support: a gentle "No pressure — pick it back up tomorrow" notification. The goal is to prevent day 2 of the skip.
- **Personal dashboards are mirrors, not scoreboards** — the most powerful productivity insight is self-awareness, not comparison. A dashboard that shows "You tend to journal more on Tuesdays" is more valuable than "You're in the top 10% of journalers." The user competes with their past self, never with others (unless they explicitly opt into social accountability).
- **The best productivity app is the one that gets out of the way** — the app exists to support the user's life, not to demand attention. If the user spends more time managing the app than doing the things the app tracks, the app has failed. The ultimate success metric: the user opens the app for < 30 seconds per interaction, does their thing, and returns to their life.

## Operating at Different Levels
<!-- STANDARD: 3min -->

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single habit tracker or simple journal | Build a single-purpose app (e.g., "daily gratitude journal") with local storage, one interaction pattern, and basic reminders. Ship as a PWA or simple mobile app. No sync, no complex analytics. |
| **L2** | Multi-feature productivity app (habits + tasks + journal) | Build a cohesive app with local-first storage, cross-device sync (CRDT-based), notification system, and basic dashboard. Implement proper data architecture with export. ~3-5 features that reinforce each other. |
| **L3** | Full personal productivity platform | Design and build a platform with habits, goals, journal, tasks, routines, and personal dashboards — all integrated. Implement sophisticated sync (real-time, conflict resolution), rich notification engine (adaptive timing, actionable), health data integration (HealthKit/Google Fit), calendar integration. Data analytics pipeline for personal insights. |
| **L4** | Ecosystem — platform + integrations + API | Build a platform with public API, integration marketplace (calendar, health, task services, voice assistants), family/team plans with shared goals, and white-label capability. Implement advanced behavioral analytics (cohort analysis of habit formation, intervention effectiveness measurement). |
| **L5** | Category-defining productivity methodology | Create a new productivity methodology that becomes a movement — like GTD did for task management or Bullet Journal did for analog journaling. The software is the embodiment of the methodology. Publish research on behavior change effectiveness. Define the standards for privacy, data portability, and habit engineering in the industry. |

**Default level for this skill:** L2

## When to Use
<!-- STANDARD: 3min -->

- Building a habit tracker with streak mechanics, identity-based reinforcement, and behavioral psychology hooks
- Building a personal journal or diary with rich text, mood tracking, photo/voice entry, and on-this-day features
- Building a goal-setting and tracking system with progress visualization, milestone celebrations, and accountability features
- Building a task management tool with GTD workflow, Eisenhower matrix, time blocking, or priority systems
- Building a personal dashboard that aggregates habits, goals, mood, and time data into actionable insights
- Building a time tracking application with automatic/manual modes, categorization, and reporting
- Building a routine builder with morning/evening checklists, time-of-day triggers, and adaptation
- Building a personal knowledge management (PKM) system with Zettelkasten, spaced repetition, or bidirectional linking
- Building a digital planner that integrates calendar, tasks, habits, and notes into a unified daily view
- Building any app where personal data privacy, offline-first design, and cross-device sync are core requirements
- Designing notification systems for behavior change — timing, bundling, quiet hours, actionable notifications
- Implementing data portability, export, and zero-knowledge architecture for personal data

### When NOT to Use

- Enterprise project management with teams, Gantt charts, resource allocation, and OKR cascading (route to project-manager)
- Team collaboration tools with shared workspaces, real-time co-editing, and permissions (route to fullstack-developer)
- Health or medical tracking apps that provide diagnoses, medication reminders, or clinical data (route to health-condition-supporter)
- Corporate wellness programs with HR integration (route to hr-manager)
- Social networks or community platforms (route to fullstack-developer)
- Pure gamification apps with no real productivity purpose (this skill refuses manipulative design)
- Enterprise analytics dashboards with BI tooling (route to analytics-engineer)

## Route the Request
<!-- STANDARD: 3min -->

<!-- QUICK: 30s — auto-route first, then intent-route -->

### Auto-Route (No User Input Required)

Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|---|---|
| A1 | `file_contains("package.json", "pouchdb" \|\| "dexie" \|\| "rxdb" \|\| "watermelondb" \|\| "realm")` AND `file_contains("*", "habit" \|\| "journal" \|\| "task.*track" \|\| "goal.*track")` | Local-first productivity app detected. Jump to **Ground Rules** — verify offline capability (R2) and data privacy (R1), then **Core Workflow > Phase 3 (Data Model)**. |
| A2 | `file_contains("*", "yjs" \|\| "automerge" \|\| "gun" \|\| "crdt" \|\| "operational.*transform")` | CRDT/sync architecture detected. Jump to **Decision Trees** — Data Storage Strategy, then **Core Workflow > Phase 5 (Cross-Device Sync)** to validate sync strategy. |
| A3 | `file_contains("*", "streak" \|\| "habit.*calendar" \|\| "dont.*break.*chain")` AND `file_contains("*", "guilt" \|\| "shame" \|\| "fail" \|\| "broke.*streak")` | Guilt-based streak mechanics detected. Jump to **Ground Rules** — R5 (anti-guilt streaks), then **Error Decoder** for streak recovery design. |
| A4 | `file_contains("*", "healthkit" \|\| "google.*fit" \|\| "health.*connect" \|\| "carekit")` | Health data integration detected. Jump to **Ground Rules** — R1 (data privacy), then verify HIPAA/GDPR compliance boundaries. Caution: route to health-condition-supporter if medical tracking. |
| A5 | `file_contains("*", "notification" \|\| "push" \|\| "reminder")` AND `file_contains("*", "schedule" \|\| "cron" \|\| "interval")` | Notification system detected with time-based triggers. Jump to **Ground Rules** — R4 (helpful not harassing), then **Core Workflow > Phase 6 (Notification System)** to audit. |
| A6 | `file_contains("*", "inapp.*purchase" \|\| "subscription" \|\| "freemium" \|\| "monetization")` | Monetization strategy detected. Jump to **Best Practices** — monetization section for ethical revenue models in productivity apps. |
| A7 | No framework detected (`!file_exists("package.json\|composer.json\|Gemfile\|requirements.txt")`) AND no productivity patterns in codebase | Greenfield productivity app. Jump to **Intent Route** below. |

### Intent Route (Ask the User)

```
What type of personal productivity app are you building?
├── Habit tracker → Start at "Decision Trees" — App Architecture, then "Core Workflow > Phase 4 (Habit Engine)"
├── Personal journal/diary → Jump to "Decision Trees" — Data Storage Strategy (privacy-first), then "Core Workflow > Phase 2 (Interaction Design)"
├── Goal-setting & tracking system → Go to "Decision Trees" — Goal Framework Selection, then "Core Workflow > Phase 4 (Goal Engine)"
├── Task management tool → Start at "Decision Trees" — Task Methodology (GTD/Eisenhower/Time Blocking), then "Core Workflow > Phase 2 (Interaction Design)"
├── Personal dashboard/analytics → Jump to "Best Practices" — Dashboard Design, then "Core Workflow > Phase 3 (Data Model)"
├── Time tracking app → Go to "Decision Trees" — Time Tracking Mode (automatic/manual/hybrid), then "Core Workflow > Phase 2"
├── Routine builder → Start at "Decision Trees" — App Architecture, then "Core Workflow > Phase 4 (Routine Engine)"
├── Personal knowledge management → Jump to "Best Practices" — PKM Architecture, then "Core Workflow > Phase 3 (Data Model)"
├── Digital planner (all-in-one) → Go to "Decision Trees" — App Architecture (mobile-first recommended), then "Core Workflow > Phase 1"
├── Adding habits/goals to an existing app → Start at "Core Workflow > Phase 1" to assess current data model fit
├── Need behavioral design consultation first → Invoke ux-researcher skill to understand user psychology and habit triggers
├── Need UI/UX design → Invoke ui-ux-designer skill for interaction patterns and design system
├── Need mobile app specifically → Invoke ios-developer or android-developer for platform-native implementation
├── Need backend API → Invoke backend-developer for sync server, notification service, or integration APIs
├── Need database design → Invoke database-designer for local storage schema and sync architecture
└── Don't know where to start? → Answer discovery questions below and I'll route you

Discovery Questions (when the user has no idea what to build):
1. "What's the ONE behavior or outcome you want to help people achieve? (journal daily / build a workout habit / hit quarterly goals / organize their life)"
2. "When and where will people use this? (phone during commute / desktop at work / tablet on couch / watch during workouts)"
3. "Does this data need to be private? (journal entries — yes, absolutely / task lists — somewhat / habit streaks — less sensitive)"
4. "Will people use this alone or share with others? (solo / accountability partner / family / public community)"
5. "What's the user's energy level when they'll interact? (morning energy / end-of-day exhaustion / throughout the day)"
```

## Decision Trees
<!-- STANDARD: 3min -->

### App Architecture — Web-Only vs Mobile-First vs Cross-Platform vs Platform-Native

```
                    ┌──────────────────────────┐
                    │ User context & budget      │
                    │ defined?                   │
                    └──────────┬───────────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Where will users       │
                    │ interact MOST?         │
                    └──┬────────┬──────┬────┘
                       │PHONE   │DESKTOP│BOTH
                       ▼        ▼       ▼
              ┌────────────┐ ┌──────────┐ ┌────────────────────┐
              │ Is the app   │ │ Is the app │ │ What is the budget  │
              │ notification-│ │ text-heavy │ │ and team size?      │
              │ heavy?       │ │ (journal,  │ └──┬─────────┬───────┘
              └──┬──────┬───┘ │ PKM)?      │    │LOW      │HIGH
                 │YES    │NO   └──┬────┬───┘    │(< $10K) │(> $50K)
                 ▼       ▼       │YES │NO       ▼          ▼
          ┌──────────┐ ┌──────┐  ▼    ▼   ┌──────────┐ ┌──────────────┐
          │Platform-  │ │PWA or│ ┌──────┐ │Cross-     │ │Platform-native│
          │native:    │ │cross-│ │PWA or│ │platform:  │ │iOS (SwiftUI)  │
          │SwiftUI/   │ │plat- │ │Elec- │ │React      │ │+ Android      │
          │Jetpack    │ │form: │ │tron  │ │Native or  │ │(Jetpack       │
          │Compose    │ │React │ │for   │ │Flutter    │ │Compose) for   │
          │for health │ │Native│ │rich  │ │for broad  │ │best UX,       │
          │integrations│ │or    │ │text, │ │device     │ │health         │
          │watch       │ │Flutter│ │local-│ │coverage + │ │integrations,  │
          │complications│ │     │ │first │ │reasonable │ │watch apps     │
          └──────────┘ └──────┘ └──────┘ │UX         │ └──────────────┘
                                         └──────────┘
```

**Guidance:**
- **Platform-native (SwiftUI/Jetpack Compose):** When the app needs health integrations (HealthKit, Google Fit), watch complications, widgets, Siri/Assistant shortcuts, or the best possible animation and haptic feedback. Cost: 2x development time (separate iOS and Android codebases). User experience: 10/10.
- **Cross-platform (React Native/Flutter):** When budget is limited but mobile-first UX is critical. Good health plugin support exists but lags platform-native by 3-6 months. Cost: 1x development time for both platforms. User experience: 8/10.
- **PWA (Progressive Web App):** When the app is primarily used at a desk, budget is near-zero, and users are web-native. Works offline via Service Workers, can send push notifications (limited on iOS). Cost: lowest. User experience: 6/10 on mobile, 9/10 on desktop.
- **Electron/Tauri:** When the app is desktop-first (PKM, deep writing, coding journals), needs file system access, or requires rich text editing that web handles best. Tauri preferred over Electron for lower memory footprint (critical for productivity apps that run all day).
- **Web-only (Next.js/Remix + PWA):** When building an MVP or the target audience is web-primary. Good for: personal dashboards, web-based journals, task managers. Add PWA capabilities for offline and installability.

### Data Storage Strategy — Local-Only vs Local-First+Sync vs Cloud-First

```
                    ┌──────────────────────────┐
                    │ Privacy requirement?       │
                    └──────────┬───────────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Is the data sensitive  │
                    │ (journal, goals,       │
                    │ health, finances)?     │
                    └──┬──────────────┬─────┘
                       │YES           │NO (tasks, habits)
                       ▼              ▼
              ┌────────────────┐ ┌──────────────────┐
              │ LOCAL-FIRST     │ │ Collaboration      │
              │ + E2E ENCRYPTED │ │ required?          │
              │ SYNC            │ └──┬──────────┬─────┘
              │                 │    │YES        │NO
              │ User key derived│    ▼           ▼
              │ from password.  │ ┌──────────┐ ┌──────────┐
              │ Server is        │ │Cloud-first│ │Local-only│
              │ zero-knowledge.  │ │with auth  │ │(IndexedDB│
              │ Use: CRDT (Yjs/  │ │(Firebase/ │ │SQLite/   │
              │ Automerge) for   │ │Supabase)  │ │CoreData) │
              │ encrypted sync.  │ │for shared │ │No sync   │
              └────────────────┘ │tasks.      │ │needed.   │
                                 └──────────┘ └──────────┘
```

**Guidance:**
- **Local-first + E2E Encrypted Sync:** The gold standard for journaling, goal tracking, and any app where the user's data must be unreadable by the server. Implementation: encrypt on device with key derived from user password (PBKDF2/Argon2), sync ciphertext via CRDT (Yjs/Automerge with custom encryption provider). The server is a dumb sync relay — it stores encrypted blobs and cannot decrypt them. Cost: 3-4x development complexity vs cloud-first. Trust: maximum.
- **Local-first + Unencrypted Sync:** For less sensitive data (habit streaks, task lists) where collaboration is not needed. Data lives locally (IndexedDB/SQLite/CoreData), syncs to server for backup and cross-device, but the server CAN read it. Use: PouchDB/CouchDB, WatermelonDB, RxDB. Cost: 2x development complexity. Trust: moderate (server operator can read data).
- **Cloud-first (Firebase/Supabase):** For collaborative features or when real-time sync is the primary value proposition. Simplest architecture but the server has full access to user data. Acceptable for: shared task lists, family habit tracking, accountability groups. Cost: 1x development complexity. Trust: lowest (server operator has full access).
- **Local-only:** For single-device apps with no collaboration. Simplest: SQLite (native), IndexedDB (web), CoreData/UserDefaults (iOS), Room (Android). No sync code, no server costs. Best for: MVPs, single-purpose tools, apps where cross-device is explicitly not a requirement.

### Notification Strategy — When and How to Remind

```
                    ┌──────────────────────────┐
                    │ What are you reminding     │
                    │ the user to do?            │
                    └──────────┬───────────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Time-specific action   │
                    │ (morning routine,      │
                    │ meeting prep)?         │
                    └──┬──────────────┬─────┘
                       │YES           │NO (habit, journal, goal check-in)
                       ▼              ▼
              ┌────────────────┐ ┌──────────────────────┐
              │ FIXED TIME      │ │ Is the action event-   │
              │ + ADAPTIVE      │ │ triggered or flexible? │
              │ User sets base  │ └──┬──────────────┬─────┘
              │ time. App learns│    │EVENT         │FLEXIBLE
              │ optimal window  │    │(post-workout,│(journal,
              │ from engagement │    │location-based)│daily
              │ data.           │    ▼              │review)
              └────────────────┘ ┌──────────────┐  ▼
                                 │ EVENT/CONTEXT │ ┌──────────────┐
                                 │ TRIGGER       │ │ ADAPTIVE      │
                                 │ Geofence,     │ │ TIMING        │
                                 │ calendar      │ │ Learn user's  │
                                 │ event,        │ │ active hours. │
                                 │ workout end   │ │ Remind during │
                                 │               │ │ natural gaps. │
                                 └──────────────┘ │ Never during  │
                                                  │ quiet hours.  │
                                                  └──────────────┘
```

**Guidance:**
- **Fixed time:** Simple, predictable. Best for: morning/evening routines, medication-adjacent habits (not medical). Risk: user dismisses if timing is wrong. Mitigation: allow per-habit time customization.
- **Adaptive timing:** Learns from user behavior. If user usually journals at 9:47 PM, remind at 9:45 PM. If user ignores morning reminders, shift to 30 minutes later. Implementation: track engagement timestamps, cluster into windows, nudge within optimal window.
- **Event/context trigger:** Most powerful, hardest to implement. Geofence: "You're at the gym — log your workout." Calendar integration: "Meeting ended — want to add action items?" Requires platform permissions and careful privacy handling.
- **Hard rules for all strategies:** (a) Max 2 notifications/day. (b) No notifications during quiet hours (default 9 PM-8 AM). (c) Every notification must be dismissible in one tap. (d) Actionable notifications: "Meditate? [Done] [Skip] [Snooze 30 min]" — user completes the action from the notification.

## Core Workflow
<!-- STANDARD: 3min -->
**(STANDARD)**

### Phase 1: User Problem & Behavior Research (~45 min)

Before writing code, understand WHO you're building for and WHAT behavior you're trying to change.

```
1. DEFINE THE TARGET USER
   |-- Write a one-paragraph persona: "Sarah is a 34-year-old product manager who
   |   wants to journal daily but is exhausted by 9 PM. She has 3 devices and a
   |   45-minute commute. She's tried 4 journaling apps and abandoned all of them
   |   because they required too much typing at the end of the day."
   |-- Specify: energy level at time of use, device context, environmental constraints.
   |-- Output: Target persona document.

2. MAP THE BEHAVIOR CHANGE
   |-- What is the CURRENT behavior? "Sarah doesn't journal."
   |-- What is the DESIRED behavior? "Sarah journals for 5 minutes every evening."
   |-- What is the TRIGGER? (cue) "Phone notification at 9 PM."
   |-- What is the ROUTINE? "Open app, see today's prompt, type or voice-record for 5 min."
   |-- What is the REWARD? "See her streak grow, revisit past entries, feel accomplished."
   |-- Apply habit stacking: what existing habit can this piggyback on?
   |   "After brushing teeth → open journal app."
   |-- Output: Cue-Routine-Reward loop diagram + habit stacking plan.

3. IDENTIFY FRICTION POINTS
   |-- List every step between "intention to journal" and "journal entry saved."
   |-- For each step, ask: "Can this be removed? Shortcut? Automated?"
   |-- Target: ≤ 3 interactions from intent to completion.
   |-- Output: Friction audit with target interaction count.

4. RESEARCH COMPETITOR FAILURE MODES
   |-- Download the top 3 apps in the category.
   |-- For each: where do users abandon? (app store reviews are gold for this).
   |-- What do 1-star reviews say? "Too many taps," "Lost my data," "Notifications are annoying."
   |-- Document: "Competitor X fails at [point] because [reason]. We will fix this by [approach]."
   |-- Output: Competitive failure analysis.
```

  Complete when: Target persona, Cue-Routine-Reward loop, friction audit (≤3 interactions target), and competitive failure analysis are written in the project doc.

### Phase 2: Core Interaction Design (~60 min)

```
5. DESIGN THE MINIMUM VIABLE HABIT LOOP
   |-- One interaction that completes the core behavior change loop.
   |-- For a habit tracker: see today's habits → tap to check off → see streak update.
   |-- For a journal: open app → see prompt → start typing/recording → save.
   |-- For tasks: quick-add field → type task → tap priority → done.
   |-- The loop must complete in ≤ 5 seconds (including app launch if possible).
   |-- Output: Interaction flow diagram with timing annotations.

6. DESIGN THE REWARD & REINFORCEMENT
   |-- What does the user see IMMEDIATELY after completing the action?
   |-- Streak counter update (visual, satisfying animation).
   |-- Progress ring fills (habit ring, goal progress bar).
   |-- Gentle celebration: "Day 7! That's a full week." (no confetti explosions — subtle, dignified).
   |-- Identity reinforcement: "You're becoming someone who journals daily."
   |-- Output: Reward screen mockups for 3 key milestones (daily, weekly, streak record).

7. DESIGN THE EMPTY & ERROR STATES
   |-- Empty state (first open): "Welcome. Choose one habit to start. Just one."
   |-- Missed day state: "No worries. 32 days is still your record. Ready to pick it back up?"
   |-- Sync conflict state: "Changes on 2 devices detected. [Show both] [Keep newer]"
   |-- Offline state: "You're offline. Your entry will sync when you reconnect. ✓ Saved locally."
   |-- Output: Empty/error/edge state designs for every screen.
```

  Complete when: Minimum viable habit loop (≤5s), reward/reinforcement designs, and empty/error/edge state mockups exist for all core screens.

### Phase 3: Data Model & Storage Architecture (~45 min)

```
8. DESIGN THE CORE DATA SCHEMA
   |-- Habits: id, name, description, frequency (daily/weekly/custom), cue, reward,
   |   identity_statement, created_at, archived_at, color, icon, order.
   |-- HabitEntries: id, habit_id, date, completed (bool), skipped (bool), notes, mood.
   |-- JournalEntries: id, date, title, content (rich text/markdown), mood, tags,
   |   photos[], voice_note_url, word_count, is_favorite.
   |-- Goals: id, name, description, type (outcome/process), framework (SMART/OKR/12-week),
   |   start_date, target_date, metric_type, target_value, current_value, milestones[].
   |-- Tasks: id, title, description, list_id, priority, due_date, reminder, repeat_rule,
   |   status, energy_level, estimated_minutes, tags[], subtasks[].
   |-- Output: Full schema with relationships, indexes, and migration plan.

9. CHOOSE LOCAL STORAGE ENGINE
   |-- Web: IndexedDB (via Dexie.js for ergonomics) or SQLite via OPFS.
   |-- Mobile: SQLite (via Room on Android, CoreData/GRDB on iOS).
   |-- Cross-platform: WatermelonDB (SQLite + lazy loading), RxDB (NoSQL + replication).
   |-- CRDT-based: Yjs/Y.Doc for rich text journals, Automerge for structured data.
   |-- Decision criteria: query complexity, sync requirements, data size.
   |-- Output: Storage engine selection with justification.

10. DESIGN SYNC ARCHITECTURE (if applicable)
    |-- Local-first: device is always the source of truth.
    |-- Changes queued locally → sync when online → resolve conflicts.
    |-- Conflict strategy: last-write-wins (timestamp vectors) for simple data,
    |   CRDT merge for rich text, user-prompted resolution for conflicts the system can't resolve.
    |-- Sync protocol: WebSocket for real-time, periodic sync as fallback.
    |-- Bandwidth: sync only delta changes, not full state.
    |-- Output: Sync architecture diagram + conflict resolution decision matrix.
```

  Complete when: Full schema (Habits, Entries, Journals, Goals, Tasks) is defined, storage engine is selected with justification, and sync architecture diagram is complete.

### Phase 4: Habit/Goal/Routine Engine (~60 min)

```
11. BUILD THE HABIT FORMATION ENGINE
    |-- Streak counter: track current streak, longest streak, total completions.
    |-- Visual streak: GitHub-style contribution calendar or circular rings.
    |-- Freeze/skip days: configurable (default 2/month) — skip preserves streak.
    |-- Recovery: after a break, show "3 days to restore your momentum" counter.
    |-- Milestone celebrations: day 7, 21, 30, 66, 100, 365.
    |-- Identity reinforcement: "You ARE a person who [habit]." Show this on milestones.
    |-- Output: Streak engine with configurable rules, visual components, and milestone calendar.

12. BUILD THE GOAL DECOMPOSITION ENGINE
    |-- SMART goals: Specific, Measurable, Achievable, Relevant, Time-bound.
    |-- Personal OKRs: Objective (qualitative) + 3 Key Results (quantitative).
    |-- 12-Week Year: goals broken into 12-week blocks with weekly milestones.
    |-- WOOP: Wish → Outcome → Obstacle → Plan — implementation intention format.
    |-- Progress visualization: progress bar, milestone checklist, time-remaining indicator.
    |-- Review prompts: weekly "How did this week go?" and monthly "Are you on track?"
    |-- Output: Goal engine supporting multiple frameworks with progress tracking.

13. BUILD THE ROUTINE BUILDER
    |-- Morning/evening routine templates.
    |-- Checklist-based with time estimates.
    |-- Habit stacking suggestions: "You already [habit A] at [time] — add [new habit] right after."
    |-- Time-of-day triggers: "7 AM: Morning routine starts."
    |-- Adaptation: adjust routine based on completion patterns (user consistently skips item 3 → suggest removing or rescheduling).
    |-- Output: Routine engine with templates, triggers, and adaptive suggestions.
```

  Complete when: Streak engine (with configurable freeze days), goal decomposition (multiple frameworks), and routine builder (with habit stacking) are spec'd and ready for implementation.

### Phase 5: Cross-Device Sync & Offline (~45 min)

```
14. IMPLEMENT OFFLINE-FIRST DATA FLOW
    |-- Every write goes to local storage FIRST.
    |-- UI reads from local storage — never waits for network.
    |-- Background sync queue: changes are queued and replayed on reconnect.
    |-- Sync status indicator in UI: "3 changes pending" / "All synced ✓" / "Offline — saved locally".
    |-- Test: enable airplane mode. Perform every core action. Verify all work.
    |-- Test: make changes offline on device A, different changes offline on device B,
    |   bring both online. Verify conflict resolution.
    |-- Output: Offline-tested data flow with sync status UI.

15. IMPLEMENT CONFLICT RESOLUTION
    |-- Simple data (habits, tasks): timestamp-vector last-write-wins.
    |-- Rich text (journal): CRDT merge (Yjs/Automerge) — character-level merging.
    |-- Structured data (goals): field-level merge with user prompt for unresolvable conflicts.
    |-- Sync protocol: push local changes → pull remote changes → merge → resolve conflicts → push merged state.
    |-- Test the "commute conflict": edit journal on phone, different edit on laptop, sync both.
    |-- Output: Conflict resolution engine with test cases.

16. IMPLEMENT EXPORT & DATA PORTABILITY
    |-- One-click export: Markdown for journals, CSV for habits/tasks, JSON with schema.
    |-- Export includes metadata: dates, streaks, tags, mood ratings.
    |-- README.txt in export: explains file structure, how to import elsewhere.
    |-- Scheduled automatic backup: weekly export to user's cloud storage (Google Drive, iCloud, Dropbox).
    |-- Test: export data, delete app, reinstall, import data. Verify all data restored.
    |-- Output: Export module with documented file format and backup scheduling.
```

  Complete when: Offline-first data flow works (all core actions in airplane mode), conflict resolution is tested with commute-conflict scenario, and one-click export restores all data on clean install.

### Phase 6: Notification & Engagement System (~30 min)

```
17. DESIGN THE NOTIFICATION ENGINE
    |-- Per-habit/per-goal notification settings: time, channel (push/email), days.
    |-- Adaptive timing: learn optimal notification time from user engagement patterns.
    |-- Bundling: if 3 habits are due at 8 AM, send ONE notification with all 3 — not 3 separate pings.
    |-- Quiet hours: hard block on notifications during user-defined quiet period (default 9 PM-8 AM).
    |-- Actionable: notifications have [Done] [Skip] [Snooze] actions — user completes from notification.
    |-- Streak saver: "You're at 31 days! Tap to keep your streak alive." Sent 1 hour before day ends.
    |-- Output: Notification orchestration engine with adaptive timing.

18. BUILD ENGAGEMENT WITHOUT ADDICTION
    |-- Weekly summary: "This week: 5/7 journal days, 6/7 meditation days. Your best week yet."
    |-- Monthly review: "January in review — 22 journal entries, 87% habit completion, top mood: calm."
    |-- Year in review: visual recap of the year's habits, moods, goals, and growth.
    |-- "On this day" for journals: "One year ago today, you wrote about..." — powerful revisit feature.
    |-- Anti-engagement: never use infinite scroll, never use variable rewards (slot machine mechanics),
    |   never use social comparison unless explicitly opted in.
    |-- Output: Engagement features that add value without manipulating.
```

  Complete when: Notification engine supports adaptive timing, bundling, quiet hours, and actionable notifications. Engagement features pass the anti-addiction checklist (no infinite scroll, no variable rewards, no social comparison without opt-in).
  Complete when: All tests pass — unit, integration, and E2E with > 80% coverage on new code.
  Complete when: Accessibility audit passes — WCAG 2.1 AA compliance with automated and manual checks.

## Best Practices
<!-- STANDARD: 3min -->
**(STANDARD)**

1. **Design for the exhausted user, not the motivated one.** The user at 11 PM, exhausted, about to sleep, remembers they haven't journaled. If your app requires > 3 taps and > 5 seconds of typing, they'll skip it. The motivated morning user is not the design target — the exhausted evening user is. Every core action must complete in ≤ 5 seconds from intent to confirmation. Quick-add, voice input, smart defaults, and one-tap completion are not nice-to-haves — they are the difference between daily use and abandonment at day 4.

2. **Local-first architecture is non-negotiable for personal data.** The device stores data locally, the UI reads from local storage, and sync is a background process — not a prerequisite for interaction. Use IndexedDB (Dexie.js), SQLite (via OPFS, Room, CoreData, or WatermelonDB), or CRDT-based stores (Yjs, Automerge). The user must never see a loading spinner for core actions. Test every feature with airplane mode ON. If something breaks offline, it's not done.

3. **Encrypt sensitive data end-to-end — the server must be blind.** Journal entries, private goals, mood data, and personal reflections must be encrypted on-device before transmission. Derive encryption key from user password (Argon2id, 256-bit). The server stores only ciphertext. The privacy policy must state: "We cannot read your data. If we receive a subpoena, we have nothing to surrender." Use: libsodium/NaCl for encryption, or platform-native (CryptoKit on iOS, Android Keystore). Never roll your own crypto.

4. **Streaks are motivators, not punishments.** Design streak mechanics that celebrate progress and forgive lapses. Provide skip/freeze days (configurable, default 2/month). When a streak breaks: "You built a 45-day habit! That's in the top 2% of habit builders. Ready to start a new streak?" Never use red, never use X marks, never use "FAILED." Recovery streak: 3 consecutive days earns back a momentum badge. The goal is to prevent "never miss twice" — the second missed day is when habits die.

5. **Notifications must respect the user's attention as a finite resource.** Hard cap: 2 notifications/day maximum per app. Adaptive timing: learn when the user engages and nudge near that window. Bundle related reminders: "Morning check-in: meditate, journal, stretch" as one notification, not three. Quiet hours: default 9 PM-8 AM, user-overridable. Every notification must be actionable: [Done] [Skip] [Snooze]. If a notification doesn't help the user do something they already want to do, it shouldn't exist.

6. **Export and data portability are first-class features, not an afterthought.** Users invest years of data in productivity apps. If your service disappears, their data must survive. One-click export to open formats: Markdown (journals with YAML frontmatter), CSV (habits/tasks with full metadata), JSON (everything with documented schema). Include a README.txt explaining the file structure. Scheduled automatic backups to user's cloud storage (Google Drive, iCloud, Dropbox). Test the full round-trip: export → delete app → reinstall → import → verify all data restored.

7. **Gamification must be meaningful, not manipulative.** Never use variable rewards (slot machine mechanics). Never use social comparison without explicit opt-in. Points and badges without purpose create extrinsic motivation that decays within 2-4 weeks. Meaningful gamification: progress visualization (rings, calendars), milestone celebrations tied to real achievements (7-day streak, 100th journal entry), identity reinforcement ("You're becoming a person who meditates daily"). The user competes with their past self, never with others (unless opted into accountability).

8. **Input methods must match the user's context and energy level.** Voice input for journaling (tap-to-record, auto-transcribe). Quick-add with smart defaults for tasks (type "Call dentist tomorrow 2pm" → auto-parsed into task with due date). One-tap habit check-in with optional note. Widgets for habit completion from the home screen. Watch complications for one-tap habit logging. Siri/Assistant shortcuts: "Hey Siri, log my meditation." The right input method at the right time reduces friction to near-zero.

9. **Personal dashboards should reveal patterns, not just display data.** A habit calendar that shows completion history is good. A dashboard that reveals "You're 40% more likely to complete your morning routine when you slept > 7 hours" is transformative. Cross-reference habits with mood, time of day, day of week, and sleep. Show correlations, not just counts. The most valuable insight is usually: "You tend to skip [habit] on [day/condition] — want to adjust your schedule?" Self-awareness is the product.

10. **The onboarding must succeed in under 90 seconds.** The user downloaded the app because they want to change. If onboarding takes > 90 seconds, the motivation window closes. Flow: (a) Welcome — one sentence value prop. (b) "What's ONE thing you want to improve?" — single text field. (c) "When's a good time to remind you?" — three quick-select options. (d) Done. The user is now tracking their first habit/journaling their first entry. Advanced configuration lives behind a settings gear — never in onboarding.

11. **Integrate with the user's existing ecosystem, don't replace it.** Calendar read/write (Google, Apple, Outlook) so tasks and routines appear alongside meetings. Health data read (Apple HealthKit, Google Fit) to correlate exercise/sleep with habit completion. Task API sync (Todoist, Things, Apple Reminders) to avoid data silos. Cloud storage (iCloud, Google Drive) for automatic backups. Shortcuts/Siri/Google Assistant for voice control. Watch complications for glanceable habit status. The productivity app is a hub — not a walled garden.

12. **Monetization must align with privacy commitments.** One-time purchase: best for privacy (no ongoing server costs to justify subscription). Subscription for sync/backup: transparent — "Sync and backup costs us money to run. Core features are free forever." Freemium: core features (habits, journal, basic tasks) free; premium (advanced analytics, unlimited goals, family sharing, priority sync) paid. Never: selling user data, surveillance ads, "free" apps that monetize behavior. If the business model requires reading user data, the product is unethical.

13. **Cognitive accessibility is a core requirement, not an edge case.** Simplified mode: reduce UI to essential actions only — one habit on screen at a time, large tap targets, minimal text. Large text mode. High contrast mode. Screen reader support: every habit status, streak count, and journal entry must be navigable via VoiceOver/TalkBack. Keyboard shortcuts for power users (desktop/web). The app must work for people with ADHD, executive dysfunction, cognitive fatigue, and visual impairments — these are often the people who need productivity tools most.

14. **Test with real behavior change metrics, not just app analytics.** DAU/MAU doesn't tell you if the app is changing lives. Track: habit completion rate (week 1 vs week 8 — does it improve?), retention at day 7/21/66/365, average streak length, goal achievement rate, journal consistency. Survey users: "Has this app helped you build a lasting habit?" If the answer is "sort of" after 3 months, the behavior change engine needs redesign. The app is a behavior change intervention — measure it like one.

## Error Decoder
<!-- STANDARD: 3min -->
**(STANDARD)**

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| User completes a habit on phone, opens laptop 30 minutes later — habit shows as incomplete. "I know I checked this off!" | Sync gap: changes were queued locally but not synced before desktop app loaded stale state. The desktop app showed the last synced state from 45 minutes ago — before the phone check-in. | Implement real-time sync via WebSocket with ≤ 5 second propagation. Add sync status indicator: "Changes pending sync ↻" visible in the UI. On app open, always pull latest state before rendering. Implement optimistic UI: check-in shows immediately as complete locally, syncs in background. | Trust breaks instantly when data appears lost. The user doesn't care about sync architecture — they care that checking off a habit on one device doesn't require re-checking it on another. A 30-second sync delay is perceived as data loss. Treat sync latency > 5 seconds as a bug. |
| User has a 90-day streak, misses one day, app shows "Streak broken: 0 days." User feels shame, stops opening the app entirely. Within a week, the habit itself collapses. | Guilt-based streak mechanics. The app treats a missed day as a failure that resets everything to zero — ignoring that 90 days of consistent behavior literally rewired the user's neural pathways. One missed day doesn't erase 90 days of habit formation. | Never reset streak display to zero with red/failure indicators. Show: "Amazing — you built a 90-day habit. That puts you in the top 1% of [habit] practitioners. One missed day is noise — here's your momentum badge. Ready to continue?" Provide skip/freeze days (configurable, 2/month). Show the longest streak as a badge of honor, not something that was "lost." | The science is clear: habit strength is measured in cumulative repetitions, not consecutive days. A 90-day streak with one miss is 90/91 = 98.9% consistency — outstanding. Streak counters that reset to zero ignore the neuroscience of habit formation and punish users for being human. The #1 reason users abandon habit trackers is guilt from a broken streak. |
| User opens journal app on subway (no signal). Spinner appears. "Loading your journal..." Never loads. User closes app, opens Notes app instead, journals there. Never opens the journal app again. | App requires network to load journal content — journal entries are fetched from server, not stored locally. The core action (journaling) is blocked on network availability. | Store all journal entries locally (IndexedDB/SQLite/CoreData). Load from local store immediately on app open. Sync runs in background. Show offline indicator: "You're offline. Entries save locally and sync when you reconnect. ✓" The spinner should never appear for core content loading — it should only appear for features that genuinely require network (e.g., cloud backup restore). | The subway test: your app must work with airplane mode ON for every core action. Productivity apps are used in transit, in basements, on airplanes, in rural areas. Network-dependence for core features is an architectural failure, not a UX issue. Every "Loading..." screen in a productivity app is a user lost to a competitor that works offline. |
| User taps notification "Time to journal!" App opens to home screen. User has to navigate to journal tab, find today's entry, and start typing. By then, the motivation window has closed. | Notification is not actionable — it opens the app but requires the user to navigate to the relevant feature. The notification created an intention but failed to bridge it to action. | Deep-link notifications: tapping "Time to journal!" opens the journal editor directly with today's prompt. Implement actionable notifications: "Meditate? [✓ Done] [Skip] [Snooze]" — user completes the action from the notification without opening the app. The notification-to-action path must be ≤ 1 interaction. | Notifications create a motivation window that closes within 30-90 seconds. If the user has to navigate after tapping the notification, the window closes and the notification was worse than useless — it interrupted the user without enabling the desired behavior. Every notification must earn its keep by reducing the distance between intention and action. |
| User exports data as JSON. Opens the file — it's a 200KB blob with no documentation, nested 6 levels deep, field names like `hb_e_dt` and `g_m_v`. User wanted to migrate to a different app but gives up. | Export was treated as a compliance checkbox, not a user feature. The format is an internal database dump with abbreviated field names — machine-readable but human-hostile. No documentation, no schema, no README. | Export must produce: (a) Markdown files for journals (one per entry, YAML frontmatter with metadata), (b) CSV for structured data (habits, tasks — with full column headers), (c) JSON with documented schema (every field explained in comments), (d) README.txt explaining file structure and how to import into popular alternatives. Test: can a non-technical user import this data into a competitor app in < 30 minutes? | Data portability is a trust contract. The user trusted your app with years of personal data. The export must honor that trust by making the data truly portable. A JSON dump with abbreviated keys is a middle finger dressed as compliance. If the user can't actually use the export, it's not an export — it's a hostage situation. |
| User adds a new habit: "Drink water." The creation flow is: Category → Name → Frequency → Reminder time → Icon → Color → Target count → Notes. 7 screens. User completes 3 screens, gets frustrated, abandons. Habit is never tracked. | Input friction in the creation flow. Every field in the creation form adds a decision the user must make. At screen 3, the user's motivation to track "drink water" is spent on form fields instead of the actual behavior change. | Smart defaults for everything: habit name from quick-add, daily frequency default, 8 AM reminder default, auto-assigned color/icon, target = 1 (binary done/not-done). Creation flow: "What habit?" (text field) → "When?" (3 quick-select: Morning/Afternoon/Evening) → Done. All other settings behind an "Options" expandable section — not in the flow. Advanced users can customize later; new users need minimal decisions. | The creation flow is where habits die. Every additional field reduces the probability the user completes creation by ~20%. The user downloaded the app because they want to drink more water — not because they want to configure a database record. Defaults that work for 80% of cases and bury the rest. |

## Production Checklist
<!-- STANDARD: 3min -->
**(STANDARD)**

Before concluding any personal productivity app build, verify every item. An unchecked item is a user abandoned at day 4 or a trust broken.

- [ ] **[PRODAPP1] Offline functionality verified:** Every core action (habit check-in, journal entry, task add, goal update) tested with airplane mode ON. No spinners, no "Loading..." screens, no error messages for core flows. Sync status indicator visible. Changes queued locally and synced on reconnect.
- [ ] **[PRODAPP2] Data privacy architecture validated:** Sensitive data (journal, goals, mood) encrypted end-to-end. Server cannot read user content. Encryption key derived from user password via Argon2id. Zero-knowledge architecture confirmed: server stores only ciphertext. Privacy policy clearly states this.
- [ ] **[PRODAPP3] Streak mechanics are anti-guilt:** Streak display uses positive language on breaks. Skip/freeze days configurable (default 2/month). Recovery streak feature implemented. No red, no X marks, no "FAILED" language. User tested: "How do you feel when your streak breaks?" — answer must be "encouraged to continue," not "guilty."
- [ ] **[PRODAPP4] Input friction under limit:** Habit check-in ≤ 1 tap. Quick-add task ≤ 2 taps. Journal entry start ≤ 1 tap (plus optional typing/voice). Voice input option available for journaling. Widget for one-tap habit completion from home screen.
- [ ] **[PRODAPP5] Notification system ethical:** Max 2 notifications/day. Adaptive timing implemented. Quiet hours enforced (default 9 PM-8 AM). Actionable notifications with [Done]/[Skip]/[Snooze]. Per-habit/per-feature notification toggles. Bundling: multiple reminders combined. Test: user reports notifications are "helpful" not "annoying."
- [ ] **[PRODAPP6] Sync architecture robust:** Real-time sync via WebSocket (≤ 5 second propagation). Conflict resolution defined and tested (LWW for simple, CRDT for rich text). Sync status visible in UI. "Commute test" passed: changes on device A appear on device B immediately after app open.
- [ ] **[PRODAPP7] Export and data portability:** One-click export to Markdown (journals), CSV (habits/tasks), JSON (with schema docs). README.txt in export package. Scheduled auto-backup to cloud storage. Round-trip tested: export → delete → reinstall → import → all data restored.
- [ ] **[PRODAPP8] Onboarding ≤ 90 seconds:** Welcome → "What's ONE thing?" → "When to remind?" → Done. User is tracking their first item. Advanced settings behind gear icon, not in onboarding flow.
- [ ] **[PRODAPP9] Empty and error states designed:** First-open empty state guides user to first action. Missed-day state celebrates record, encourages continuation. Offline state confirms local save. Sync conflict state offers clear resolution. No dead ends, no blank screens, no "Something went wrong."
- [ ] **[PRODAPP10] Cognitive accessibility:** Simplified mode available (one habit/goal at a time, large targets). Large text mode. High contrast mode. Screen reader support verified (VoiceOver/TalkBack). Keyboard shortcuts documented (desktop/web). Color not used as sole information channel.
- [ ] **[PRODAPP11] Habit formation milestones:** Celebrations at day 7, 21, 30, 66, 100, 365. Identity reinforcement messages at key milestones. Visual streak calendar (GitHub-style contribution grid or circular rings).
- [ ] **[PRODAPP12] Goal framework support:** At least one goal framework implemented (SMART, OKR, or 12-Week Year). Progress visualization. Weekly/monthly review prompts. Milestone tracking.
- [ ] **[PRODAPP13] Integration ecosystem:** At least one external integration working (calendar, health data, cloud backup, voice assistant, or task API). Integration is optional and user-consented — not automatic data access.
- [ ] **[PRODAPP14] Behavior change metrics tracked:** Habit completion rate (week 1 vs week 8), retention at day 7/21/66, goal achievement rate. User survey prompt at month 3: "Has this app helped you?" Metrics inform iteration, not surveillance.
- [ ] **[PRODAPP15] Monetization is transparent and ethical:** No data selling. No surveillance ads. Pricing clearly communicated. Free tier covers core features. Paid tier adds genuine value (sync, analytics, family). All pricing marked "as of [current year] — verify current rates."

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

| Scenario | Coordinate With | Why |
|---|---|---|
| User research needed — understanding behavior triggers, pain points, and habit context | ux-researcher | Persona creation, journey mapping, and habit trigger identification require user research methods. UX researcher provides behavioral insights that drive interaction design. |
| UI/UX design for habit tracker, journal, or dashboard | ui-ux-designer | Productivity apps need interaction patterns optimized for low-friction, high-frequency use. Design tokens, component specs, and responsive layouts for mobile-first. |
| Frontend implementation — React/Next.js, Vue, Svelte | frontend-developer | Web-based productivity apps (PWA, desktop) need frontend architecture with offline-first patterns, local storage engines, and sync integration. |
| Mobile implementation — iOS or Android native | ios-developer, android-developer | Platform-native features: HealthKit/Google Fit, widgets, watch complications, Siri/Assistant shortcuts, haptic feedback, notification channels. |
| Backend for sync server, notification service, or integration APIs | backend-developer | CRDT sync server, push notification delivery, calendar/health API proxies, export processing. Must implement zero-knowledge architecture for encrypted data. |
| Database design for local storage schema and sync architecture | database-designer | Local storage engine selection (SQLite/IndexedDB/CRDT), schema design for habits/tasks/journals/goals, sync replication strategy, indexing for query performance. |
| Full-stack implementation — PWA or web app with backend | fullstack-developer | End-to-end productivity app with offline support, sync, and backend integration. |
| Website/landing page for the productivity app | website-builder | Marketing site, documentation, blog content about productivity methodology. |
| Analytics for personal insights and behavior change measurement | analytics-engineer | Personal dashboard analytics, behavior change metrics, cohort analysis for habit formation effectiveness. Must respect privacy boundaries — analytics on user's own data, not surveillance. |
| QA and testing — offline, sync, cross-device, accessibility | qa-engineer | Comprehensive test plan for offline scenarios, sync conflicts, cross-device consistency, accessibility compliance, input friction benchmarks. |
| Accessibility audit — screen reader, cognitive accessibility, color contrast | accessibility-testing | WCAG 2.2 AA compliance, VoiceOver/TalkBack testing, cognitive accessibility verification, simplified mode audit. |
| Prototype for habit interaction experimentation | prototype | Prototype the core habit loop (cue-routine-reward) before full implementation. Test interaction friction, notification timing, and streak display with real users. |

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `ux-researcher` | User personas, behavior triggers, pain points, journey maps, competitive UX analysis | Before Phase 1 — user research drives behavior change design |
| `ui-ux-designer` | Design system, component specs, interaction patterns, mobile-first layouts | Before Phase 2 — interaction design for low-friction flows |
| `frontend-developer` | Offline-first web app, PWA capabilities, local storage integration | During Phase 3-5 — frontend implementation |
| `backend-developer` | Sync server, notification service, integration APIs | During Phase 5 — sync architecture and API design |
| `database-designer` | Local storage schema, sync replication, indexing strategy | During Phase 3 — data model and storage architecture |
| `fullstack-developer` | End-to-end app with offline + sync + backend | During Phase 3-6 — full implementation |
| `website-builder` | Marketing site, documentation, blog | Before launch — web presence for the app |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `qa-engineer` | Complete app with offline, sync, and notification features. Test accounts, test data, sync conflict scenarios | QA can't test offline/sync flows without working app |
| `prototype` | Core habit loop design, interaction flow, hypothesis about behavior change mechanics | Prototype can't test behavior change without loop design |
| `analytics-engineer` | Personal dashboard requirements, behavior change metrics, data schema | Analytics can't build dashboards without metrics definitions |
| `accessibility-testing` | Component inventory, interaction patterns, screen reader flows | Accessibility audit requires implemented UI |
| `ios-developer` | Design specs, behavior change engine design, sync protocol | iOS implementation blocked without design and engine specs |
| `android-developer` | Design specs, habit engine design, notification orchestration | Android implementation blocked without design and engine specs |

## Proactive Triggers
<!-- STANDARD: 3min -->

| # | Trigger Condition | Auto-Response |
|---|---|---|
| 🔴 P1 | User mentions storing journal entries or private goals in plaintext on a server | [PRIVACY ALERT] "Privacy violation: [feature] stores sensitive data server-side in plaintext. Personal productivity apps require zero-knowledge architecture — encrypt on device before transmission. See Ground Rule R1. Switch to local-first with E2E encryption before proceeding." |
| 🔴 P2 | Streak mechanic detected using guilt language ("failed," "broke your streak," red X marks) | [STREAK ALERT] "Guilt-based streak mechanic detected. Streaks must motivate, not punish. See Ground Rule R5. Redesign: skip/freeze days, positive language, celebration of cumulative progress over consecutive days." |
| 🔴 P3 | Notification system designed with > 3 daily notifications or no quiet hours | [NOTIFICATION ABUSE] "Notification system exceeds ethical limits. Max 2 notifications/day, mandatory quiet hours, per-feature toggles required. See Ground Rule R4. Audit and reduce before proceeding." |
| 🟡 P4 | Core feature requires network — spinner/loading screen on primary user flow | [OFFLINE FAILURE] "Core feature blocked on network: [feature]. Productivity apps must work offline for all core actions. See Ground Rule R2. Implement local-first storage before continuing." |
| 🟡 P5 | App designed without export or data portability features | [DATA HOSTAGE] "No data export mechanism designed. Users must be able to take their data anywhere. See Ground Rule R7. Add one-click export to open formats (Markdown, CSV, JSON) before launch." |
| 🟡 P6 | Habit/goal creation flow has > 3 steps or requires users to configure advanced settings | [FRICTION DETECTED] "Creation flow exceeds friction budget: [count] steps. Target: ≤ 2 steps for core creation. Smart defaults for everything else. See Ground Rule R3. Simplify before user testing." |
| 🟠 P7 | Gamification system uses variable rewards, leaderboards without opt-in, or points without purpose | [MANIPULATION DETECTED] "Gamification mechanics may be manipulative. Variable rewards and forced social comparison are unethical in productivity apps. See Best Practice #7. Replace with meaningful progress visualization." |
| 🟠 P8 | Sync architecture treats server as source of truth or has no conflict resolution strategy | [SYNC GAP] "Sync architecture may cause data divergence. Local-first requires device as source of truth with defined conflict resolution. See Core Workflow Phase 5. Define conflict strategy (LWW/CRDT/user-prompted) before building." |

## Anti-Patterns
<!-- STANDARD: 3min -->

### Anti-Pattern: "We'll add offline support in v2"
**What it looks like:** A team builds a beautiful journaling app — server-rendered, database-backed, works great on WiFi. "Offline is a v2 feature." Launch day: 4.2 stars. Day 3: users start journaling on their commute. Subway has no signal. App shows spinner. 1-star reviews: "Doesn't work on the subway." Retention at day 7: 12%.
**Why it fails:** Offline is architectural — not a feature flag. Retrofitting offline into a server-first architecture is a full rewrite: every data fetch must be rerouted through a local cache, every write must be queued, every UI component must handle stale-while-revalidate. What takes 2 days to architect correctly from the start takes 4 weeks to retrofit — and the users who churned in month 1 never come back.
**Do this instead:** Build local-first from line one. The local database is the source of truth. The server is a sync relay. Every core interaction reads from local storage — network is an enhancement, not a requirement. Test every commit with airplane mode ON.

### Anti-Pattern: Gamification as a substitute for genuine value
**What it looks like:** App awards "Productivity Master" badge after 3 days. Leaderboard shows user is ranked #14,287 in "morning routine completions." Daily streak bonus: 50 XP. Weekly challenge: "Complete 7 habits for 100 XP." XP doesn't do anything. User engagement spikes week 1, crashes week 3 when the novelty wears off.
**Why it fails:** Extrinsic rewards without intrinsic meaning create shallow engagement that decays predictably. Points without purpose feel manipulative. Social comparison without consent feels invasive. The user wanted to build a meditation habit — not play a slot machine disguised as self-improvement.
**Do this instead:** Gamification must connect to the user's own goals. Show progress toward THEIR objective: "You've meditated 20 out of 30 days this month — on track to your goal." Milestone celebrations tied to real achievements: "100 journal entries! Here's a word cloud of your most common themes this year." The reward is self-knowledge and visible progress — not points.

### Anti-Pattern: Building for yourself (the power user)
**What it looks like:** Developer builds a GTD implementation with projects, areas, contexts, waiting-for lists, someday/maybe, weekly review templates, and a 47-field task form. The developer loves it. Actual users open the app, see 12 navigation tabs, and close it within 15 seconds.
**Why it fails:** You understand GTD. Your users want to remember to buy milk and not feel bad about missing a workout. The power user is < 5% of the market. Building for yourself produces a productivity app that only productivity-methodology enthusiasts can use — and even they have opinions that don't match yours.
**Do this instead:** Design for the 95%. The default experience is: "What do you want to track?" → one field. All methodology-specific features (GTD contexts, Eisenhower matrix, time blocking) are opt-in modes — not the default. The app grows with the user, not overwhelms them on day one.

### Anti-Pattern: Ignoring the notification death spiral
**What it looks like:** App sends 5 notifications/day by default. Morning reminder. Afternoon check-in. Evening wrap-up. Streak alert. Weekly report. User disables notifications after day 2. App now has zero notification channel. Important updates (sync issues, data export reminders) can't reach the user. The notification channel is permanently burned.
**Why it fails:** Notifications are a trust contract. Each notification withdraws from a limited goodwill account. When the account is empty, the user disables notifications — and you've permanently lost the most powerful behavior change tool in your arsenal (the well-timed reminder).
**Do this instead:** Default to 1 notification/day. Present notification settings during onboarding: "We'll remind you once a day. Want to choose when?" Every additional notification must be explicitly opted into. Monitor notification dismissal rate — if > 30%, reduce frequency. A notification that's dismissed is worse than no notification at all.

### Anti-Pattern: Sync as a v2 feature — "let's get the app working first"
**What it looks like:** Team ships v1 with local-only storage. "We'll add sync in v2." v1 is successful — 50K users. v2 sync launch: every user's local data must be migrated to a sync-compatible format. Schema changes break because local-only data has no timestamps for conflict resolution. Users with 6 months of data face potential data loss during migration. Trust is broken.
**Why it fails:** Sync changes the data model fundamentally — timestamps, version vectors, conflict metadata, and sync state must exist on every record. Adding sync to a non-synced database is a schema migration on every user's device simultaneously, with no rollback path for data generated before the migration. It's a distributed systems problem on 50K unrelated databases.
**Do this instead:** If the product roadmap includes cross-device sync within 12 months, architect for it from day one. Include `updated_at`, `sync_version`, and `device_id` on every record — even in v1. The local database schema is sync-ready from the start, even if the sync server ships later. The cost of sync-ready fields is near-zero at the start; the cost of retrofitting is astronomical.

### Anti-Pattern: Privacy policy written by a lawyer who's never used a journal
**What it looks like:** 12-page privacy policy with legal jargon. Section 4.3: "We may share anonymized and aggregated data with third-party partners to improve our services." Translation: "We read your journal entries, strip your name, and sell the patterns." User who journals about their divorce discovers this and feels violated.
**Why it fails:** The privacy policy is the trust foundation of a personal productivity app — especially journaling. If the policy has carve-outs for data sharing, the user rightfully assumes everything they write will be monetized. The most intimate thoughts a human can record digitally must be protected absolutely — not "anonymized and shared."
**Do this instead:** Privacy policy must state in plain language: "We cannot read your journal entries. They are encrypted on your device. We do not have the keys. We cannot access your data even if compelled by law. We do not sell, share, or analyze your data. Your data is yours." If the business model cannot support this, the business model is wrong for this category.

### Anti-Pattern: Treating all habits as equivalent
**What it looks like:** "Floss teeth" and "Write novel" are both tracked as binary daily habits with the same streak counter, same reminder frequency, same celebration. User builds a 30-day flossing streak but the novel is untouched — the app celebrates the streak as if both habits are equally complex.
**Why it fails:** A 2-minute daily habit (flossing) and a 1-hour creative practice (writing) have fundamentally different behavior change mechanics. Binary completion tracking fails for complex goals — a novel requires progress, not completion. The user feels the app doesn't understand their goals.
**Do this instead:** Support multiple habit types: binary (done/not-done), measurable (target value: "Write 500 words"), and time-based ("Meditate 10 minutes"). Habit creation wizard asks: "Is this something you check off (floss) or track progress on (write 500 words)?" Goals break down into milestones. The tracking mechanism matches the behavior complexity.

### Anti-Pattern: "We don't need accessibility — our users are productivity enthusiasts"
**What it looks like:** App uses tiny tap targets, low-contrast text, complex gesture navigation. No screen reader support. Assumption: "People who need accessibility tools aren't our target market — our users are tech-savvy professionals managing their lives."
**Why it fails:** ADHD, executive dysfunction, chronic illness, cognitive fatigue, visual impairment — these are disproportionately represented among people who seek productivity tools. The person who struggles most with executive function is the person who most needs a well-designed productivity app. Excluding them through inaccessible design is both unethical and bad business — they are the core market.
**Do this instead:** Accessibility from day one: large tap targets (≥ 44pt), high contrast (≥ 4.5:1), screen reader labels, simplified mode, keyboard navigation. Test with actual users who have accessibility needs. The app that works for someone with ADHD during an executive dysfunction episode works for everyone — accessibility is the ultimate stress test.

## What Good Looks Like
<!-- STANDARD: 3min -->

```
BEFORE (Feature-First To-Do List):
"We'll build a task manager with folders, tags, priorities,
due dates, recurring tasks, subtasks, Gantt chart view,
Kanban board, calendar integration, team sharing, and
real-time collaboration."
→ 6 months later: overengineered project management tool
  that no individual wants to use. 3/5 stars. "Too complicated.
  I just want a simple to-do list."

AFTER (Behavior-First Productivity App):
PROBLEM: "Busy professionals want to build a daily journaling
habit but consistently fail because (a) they're exhausted at
journaling time, (b) a blank page is intimidating, (c) their
phone isn't always with them, and (d) they forget until it's
too late."

SOLUTION DESIGN:
- ONE core interaction: tap "Journal" → see today's prompt →
  type or speak → saved. 4 seconds total.
- Voice input: "I don't have energy to type — I'll just talk."
  Auto-transcribed, saved, editable later.
- Prompt-driven: "What are you grateful for today?" instead of
  a blank page. New prompt daily. User can ignore and free-write.
- Adaptive reminder: learns the user journals at 9:47 PM on
  weekdays, 8:15 AM on weekends. Adjusts accordingly. One
  notification/day.
- Streak: "Day 42! You've written 12,000+ words. Here's your
  most-used word this month: 'grateful'."
- Skip day: 2/month. "No pressure — your 42-day record is safe."
- Offline: journals locally first. "Saved ✓ — will sync when
  online." Works perfectly on the subway.
- Privacy: zero-knowledge encryption. "We cannot read your
  journal entries. Even if compelled by law."
- Export: one-tap Markdown export. "Your journal, your files.
  Take them anywhere."
- Accessibility: large text, high contrast, VoiceOver-navigable,
  simplified mode.

RESULTS:
- Day 7 retention: 68% (industry average: 25%)
- Day 66 habit formation: 41% of users still journaling daily
- Average journal entry time: 4.2 minutes (voice) / 6.8 minutes (text)
- App Store rating: 4.8 stars — "Finally, a journaling app
  that works when I'm tired."
- Privacy policy: 0 user complaints in 18 months
- Sync: 99.97% conflict-free sync rate across 3 devices
- Exports: 12% of users export monthly as backup — zero data
  loss incidents

Total time: 3 months from concept to launch. Behavior change
designed first, app built second. The app didn't just ship
features — it changed behavior. This is what a 10/10 personal
productivity app build looks like.
```

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Designing for the motivated morning user instead of the exhausted 11 PM user — app abandoned at day 4 | $30K-$80K in churn and failed product launch | Every core action must complete in ≤5 seconds from intent to confirmation. Quick-add, voice input, and one-tap completion are survival features, not nice-to-haves. Test all flows at 11 PM on a low-battery phone. |
| Storing journal entries and personal reflections as plaintext on server — subpoena surrenders user's innermost thoughts | $50K-$200K in legal liability and trust collapse | Encrypt sensitive data end-to-end on-device before transmission. Derive encryption key from user password (Argon2id). Server stores ciphertext only. Privacy policy must state: "We cannot read your data." |
| Using streaks as punishment — red X, "FAILED," or guilt mechanics drive permanent abandonment | $15K-$40K in user churn and 1-star reviews | Design streaks as motivators. "You built a 45-day habit! Ready to start a new streak?" Provide configurable skip/freeze days. Never use red, never use X marks, never use failure language. Recovery streak: 3 consecutive days earns back the momentum badge. |
| Fetching from server on every app open instead of local-first — loading spinner on launch drives 53% abandonment | $20K-$60K in user acquisition waste | Local-first architecture: device stores data locally, UI reads from local storage, sync is background-only. Test every feature with airplane mode ON. If anything shows a spinner or blank screen offline, it's not done. |
| Notification spam — 3 separate pings for 3 habits due at the same time drives users to disable all notifications | $10K-$25K in lost re-engagement channel | Bundle notifications: one notification for all habits due at the same time. Adaptive timing learns optimal notification time from engagement patterns. Hard block during user-defined quiet hours. Actionable notifications with [Done] [Skip] [Snooze]. |

## Verification Guardrails
<!-- STANDARD: 3min -->

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

- [ ] **Ground Rules:** All 9 ground rules checked. No privacy violations. Offline works. No guilt mechanics. Notifications ethical. Export designed. Sync architected.
- [ ] **Behavior change loop:** Cue-Routine-Reward loop designed and tested. Habit stacking considered. Identity-based reinforcement implemented.
- [ ] **Input friction:** Every core action ≤ 3 taps. Voice input available. Quick-add with smart defaults. Creation flow ≤ 3 steps.
- [ ] **Privacy architecture:** Zero-knowledge for sensitive data. Encryption on device. Server stores ciphertext only. Privacy policy clear.
- [ ] **Offline verified:** All core actions tested with airplane mode ON. Local-first storage confirmed. Sync status indicator visible.
- [ ] **Sync tested:** Commute test passed. Conflict resolution verified. Real-time sync ≤ 5 seconds. No data loss scenarios.
- [ ] **Streak design:** Anti-guilt language. Skip/freeze days. Recovery streak. No red/failure indicators. Milestone celebrations.
- [ ] **Notifications:** Max 2/day. Adaptive timing. Quiet hours. Actionable. Per-feature toggles. Bundling implemented.
- [ ] **Export:** One-click to open formats. README included. Round-trip tested. Auto-backup option.
- [ ] **Accessibility:** Screen reader tested. Large text mode. High contrast. Simplified mode. Keyboard navigation.
- [ ] **Onboarding:** ≤ 90 seconds. User tracking first item within 2 minutes. No forced configuration.
- [ ] **Monetization:** Transparent. No data selling. Privacy-respecting model. Pricing marked with year qualifier.

If any check fails: return to the corresponding Core Workflow phase, resolve, and restart verification from that item.

## Deliberate Practice
<!-- STANDARD: 3min -->

The best personal productivity developers treat habit formation and behavioral design as crafts, not features. Deliberate practice means building tools you personally use, measuring behavior change scientifically, and iterating based on data.

| Level | Practice Routine | Frequency |
|---|---|---|
| **Novice** | Build a single-feature habit tracker (streak counter, calendar heatmap) from scratch using local storage. Dogfood it for 30 days and track your own adherence | Monthly project |
| **Competent** | Implement a complete productivity system (habits + tasks + journaling) with offline support, sync, and notifications. Conduct a 2-week usability study with 3+ real users | Quarterly |
| **Advanced** | Design and run a randomized controlled experiment testing a behavioral intervention (e.g., implementation intentions vs. streak framing). Measure statistically significant behavior change. Publish findings | Biannually |
| **Expert** | Build a production productivity app deployed to app stores with 1000+ users. Implement A/B testing infrastructure, analyze retention cohorts, publish a case study on behavior change patterns | Annually |

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, behavioral design decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

| Decision | Date | Rationale | Alternatives Considered |
|----------|------|-----------|------------------------|
| *Record all critical decisions here* | — | — | — |

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->
**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s) |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error in the repo: `grep -r "[error text]"` | Check GitHub issues for the tool. Check Stack Overflow | Simplify the approach. Break complex one-liners into sequential commands. Use more basic tools with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` | Abort and flag for human review. Do not proceed past data integrity failures |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## References
<!-- STANDARD: 3min -->

- **Habit Formation Science:** Charles Duhigg — "The Power of Habit" (cue-routine-reward loop, golden rule of habit change). James Clear — "Atomic Habits" (identity-based habits, 4 laws of behavior change, habit stacking, never miss twice, 1% better). BJ Fogg — "Tiny Habits" (B=MAP: Behavior = Motivation + Ability + Prompt, celebration as reward). Phillippa Lally — 66-day habit formation study (2009, European Journal of Social Psychology). Implementation intentions (Gollwitzer, 1999) — "I will [behavior] at [time] in [location]."
- **Goal Frameworks:** SMART goals (Doran, 1981). OKRs (Grove/Doerr — adapted for personal use with qualitative Objectives + quantitative Key Results). 12-Week Year (Moran/Lennington — annual goals compressed into 12-week execution cycles). WOOP (Oettingen — Wish, Outcome, Obstacle, Plan; mental contrasting with implementation intentions). Backward goal setting (start from desired outcome, work backward to today).
- **Journaling Architectures:** Bullet Journal method (Carroll — rapid logging, migration, collections). Gratitude journaling (Emmons/McCullough — 3 things daily, measured positive affect increase). Expressive writing (Pennebaker — 15-20 minutes, emotional processing). Morning Pages (Cameron — stream of consciousness, 3 pages). Prompt-based journaling (guided reflection, reduced blank-page anxiety).
- **Task Management Methodologies:** Getting Things Done — GTD (Allen — capture, clarify, organize, reflect, engage). Eisenhower Matrix (urgent/important quadrants). Time Blocking (Cal Newport — schedule deep work blocks). Pomodoro Technique (Cirillo — 25-minute focused intervals). Eat the Frog (Tracy — hardest task first). Zen to Done (Babauta — simplified GTD with habit focus).
- **Data Privacy & Sync:** CRDT — Conflict-free Replicated Data Types (Shapiro et al., 2011). Yjs — CRDT framework for collaborative editing. Automerge — CRDT library with rich document model. Local-first software (Kleppmann et al., Ink & Switch — "Local-First Software: You Own Your Data, in Spite of the Cloud"). End-to-end encryption — NaCl/libsodium, Signal Protocol concepts, zero-knowledge architecture patterns. GDPR/CCPA requirements for personal data (data minimization, right to access, right to deletion, data portability).
- **Personal Knowledge Management:** Zettelkasten method (Luhmann — atomic notes, bidirectional linking, emergent structure). Spaced repetition (Ebbinghaus forgetting curve, Anki/SM-2 algorithm). MOC — Maps of Content (Nick Milo — flexible organizational structure). PARA method (Forte — Projects, Areas, Resources, Archives). Second Brain (Forte — CODE: Capture, Organize, Distill, Express).
- **Behavioral Psychology for Product Design:** Nir Eyal — "Hooked" (trigger, action, variable reward, investment — use ethically, never manipulatively). Fogg Behavior Model (B=MAP). Self-Determination Theory (Deci/Ryan — autonomy, competence, relatedness). Nudge theory (Thaler/Sunstein — choice architecture, defaults). Loss aversion in streak design (Kahneman/Tversky — losses hurt 2x more than gains feel good — design accordingly).
- **Notification Psychology:** Optimal timing research — learn from user behavior, don't impose. Notification bundling (reduces perceived interruption). Actionable notifications (reduce intention-action gap). Quiet hours (respect circadian rhythms). Interruption cost (Mark et al. — 23 minutes to refocus after interruption).
