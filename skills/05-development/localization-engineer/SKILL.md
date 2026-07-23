---
name: localization-engineer
description: 'i18n/l10n architecture, translation pipelines, RTL layout, locale-aware formatting (dates/numbers/currencies), Unicode/BIDI, pseudo-localization, continuous localization in CI/CD, TMS integration
  (Lokalise/Phrase/Crowdin), and locale detection. Trigger: i18n, l10n, internationalization, localization, translation, RTL, multilingual, locale, globalization, g11n, language support, cultural adaptation.
  Works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI.'
author: Sandeep Kumar Penchala
type: development
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- localization-engineer
token_budget: 4000
output:
  type: code
  path_hint: ./
chain:
  consumes_from:
  - frontend-developer
  - mobile-developer
  - translation-manager
  - ux-writer
  feeds_into:
  - frontend-developer
  - mobile-developer
  - qa-engineer
  - translation-manager
---
# Localization / i18n-L10n Engineer

Design and implement end-to-end internationalization (i18n) and localization (l10n) systems. This skill covers message extraction, translation pipeline architecture, locale-aware formatting, RTL layout, pseudo-localization testing, and continuous localization integrated into CI/CD. Every decision balances developer ergonomics, translator workflow, and end-user experience across languages and cultures.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Set up i18n from scratch → Start at "Decision Trees > New Project"
├── Extract hardcoded strings for translation → Jump to "Core Workflow > Phase 1 (Message Extraction)"
├── Integrate a TMS (Lokalise/Phrase/Crowdin) → Go to "Core Workflow > Phase 2 (Translation Pipeline)"
├── Implement RTL layout support → Jump to "Core Workflow > Phase 3 (RTL Layout)"
├── Format dates, numbers, currencies per locale → Go to "references/icu-messageformat-guide.md"
├── Set up pseudolocalization testing in CI → Jump to "Core Workflow > Phase 4 (Pseudolocalization)"
├── Design locale detection (URL/subdomain/Accept-Language) → Go to "Decision Trees > Locale Detection Strategy"
├── Need string translation management → Invoke translation-manager skill instead
├── Need frontend i18n integration → Invoke frontend-developer skill instead
├── Need mobile i18n integration → Invoke mobile-developer skill instead
├── Need QA for locale testing → Invoke qa-engineer skill instead
├── Need accessibility in multiple languages → Invoke accessibility-testing skill instead
└── Don't know where to start? → Describe your app, target languages, and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never hardcode strings.** Every user-visible string goes into a translation file. Do not embed text in JSX/TSX/Swift/Kotlin — use translation keys with fallbacks.
- **Always test with pseudolocalization before translations.** Run pseudo-localized builds to catch hardcoded strings, layout breakage, and truncation before translators invest time. Do not wait for real translations to find i18n bugs.
- **Dates, numbers, and currencies are locale-specific.** Never use `new Date().toLocaleString()` without specifying the locale. Formats, first-day-of-week, digit grouping, and currency symbols all vary. Do not assume `en-US` formatting.
- **Always design for text expansion.** English is compact — German and Arabic can be 30-50% longer. UI layouts must accommodate expansion without breaking.
- **Admit what you don't know.** If you don't know the target locales, RTL requirements, or TMS integration details, say so and ask before designing the pipeline.

## When to Use

- You are adding i18n support to a new web or mobile application from day one
- You need to extract hardcoded strings from an existing codebase for translation
- You are setting up a translation management system (Lokalise, Phrase, Crowdin) integrated with CI/CD
- You need to implement locale-aware date, number, currency, and plural formatting using ICU MessageFormat
- You are adding support for right-to-left (RTL) languages and need to adapt layouts and styles
- You need to set up pseudo-localization in CI to catch i18n bugs before translators see the strings
- You are designing a locale detection and negotiation strategy (URL path, subdomain, Accept-Language header)
- You need to build a continuous localization pipeline that pushes source strings and pulls translations automatically

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
```
NEW PROJECT — How should we structure i18n from day one?
├── Single-language MVP (<3 months to launch)?
│   └── Externalize all strings into a single `en.json`. Don't integrate a TMS yet.
│       Use a simple i18n lib (react-i18next, vue-i18n, rosetta, go-i18n). Add locale
│       routing when the second language is 2 sprints away — not before.
├── Multi-language from launch?
│   └── ICU MessageFormat from day one. Store translations in locale files (JSON/PO/YAML).
│       Integrate a TMS (Lokalise, Phrase, Crowdin) before the first non-English locale ships.
│       Budget: 2-4 weeks for i18n setup before any feature work on locale #2.
└── Enterprise with 10+ languages at launch?
    └── ICU MessageFormat + CLDR data + dedicated i18n service. Translation memory mandatory.
        Pseudo-localization in CI from sprint 0. Legal review for each locale's requirements.
        Budget: 1 dedicated i18n engineer + TMS admin for first 6 months.

STRING EXTRACTION — Hardcoded strings in a 200K LOC codebase?
├── <500 hardcoded strings → Manual extraction sprint (1-2 devs, 1 week).
├── 500-5000 hardcoded strings → Use i18n lint rules (eslint-plugin-i18n, i18next-scanner)
│   to find and flag. Extract in batches by module. 2-4 weeks.
└── 5000+ hardcoded strings → Build an AST-based extraction pipeline. Run it in CI to
    prevent new hardcoded strings. Gradual migration over 1-3 months. Never block the
    whole team — extract one module, merge, repeat.

TRANSLATION PIPELINE — Push vs Pull?
├── Devs push source strings to TMS?
│   └── CI pipeline extracts strings on every merge to main. Pushes to TMS via API.
│       Translators work in TMS. TMS opens a PR with translated files when ready.
│       Best for: dedicated translation team, frequent string changes, CI/CD-native.
├── Translators pull from repo?
│   └── Source strings committed to repo. Translators clone, translate, open PR.
│       Best for: open source, volunteer translators, no TMS budget.
└── Hybrid?
    └── TMS is source of truth. CI pushes to TMS. TMS pushes translated files as PR.
        But devs can also manually trigger pulls. Best for most teams.

RTL (RIGHT-TO-LEFT) — Should we support Arabic, Hebrew, Farsi, Urdu?
├── Never going to support RTL languages?
│   └── Skip RTL infrastructure entirely. Document this decision.
├── Maybe in the next 12 months?
│   └── Use CSS logical properties (`margin-inline-start`, `padding-inline-end`)
│       instead of physical properties (`margin-left`, `padding-right`) from day one.
│       This costs nothing and makes RTL a 1-day CSS flip later.
│       Use `dir="auto"` on user-generated content containers.
└── Launching an RTL locale within 3 months?
    └── Build an RTL-first component library. Every component must render correctly
        in both LTR and RTL. Pseudo-localize to Arabic-pseudo in CI. Hire a native
        RTL reviewer — automated flipping catches 70%, human review catches the rest.

LOCALE DETECTION — How should we decide which language to show?
├── Single locale per deployment (e.g., `es.example.com`)?
│   └── Subdomain-based routing. Build-time locale selection. No runtime detection.
│       Fastest, simplest. SEO-friendly (separate domains indexed).
├── Accept-Language header?
│   └── Parse `Accept-Language` server-side. Respect the browser's preference.
│       Fall back to a default locale. Always provide a language switcher.
│       SEO: use `hreflang` tags + `rel="alternate"`.
├── GeoIP-based?
│   └── USE ONLY AS A FALLBACK, never as the primary detection method.
│       A Swiss user with browser in French ≠ wants German content.
│       GeoIP is wrong ~30% of the time for language. It's acceptable as a
│       hint for currency or regional defaults, not for language.
└── User preference (saved in account settings)?
    └── Always honor explicit user preference over any automatic detection.
        This is the ultimate source of truth.

**What good looks like:** The app renders correctly in all 10+ target locales including RTL languages (Arabic, Hebrew) without a single text truncation or layout break. String extraction covers 100% of user-facing text — verified by automated scan that compares source strings to translation files. Date, number, currency, and pluralization formatting matches every locale's expectations (d/m/y vs m/d/y, 1.000 vs 1,000). Translation files are complete, reviewed, and shipped in the same deploy as the code — no lag, no missing strings.
## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): i18n Foundation — Externalize & Standardize

1. **Choose i18n library** per stack:
   - **JavaScript/React**: `react-i18next` (most popular), `formatjs` (ICU-first), `next-intl` (Next.js native)
   - **Vue**: `vue-i18n` (official), `@nuxtjs/i18n` for Nuxt
   - **Python**: `Babel` + `gettext`, or `fluent` (Mozilla's Fluent)
   - **Go**: `go-i18n`, `gotext`
   - **Java/Kotlin**: `ResourceBundle` + ICU4J, or `i18nize` for Spring
   - **Swift/Kotlin Multiplatform**: `Moko-resources`, Apple `String Catalogs` (Xcode 15+)
   - **Output**: Library chosen, installed, and configured. Proof-of-concept with 3 translated strings.

2. **Define message format**: Use **ICU MessageFormat** for anything beyond simple key-value.
   ```
   // AVOID: "You have {count} new messages" — breaks in Polish (plural rules differ)
   // USE: "{count, plural, =0 {No messages} one {1 message} few {# messages} many {# messages} other {# messages}}"
   ```
   ICU supports: plurals, select (gender), selectordinal, number/date/time formatting.
   - **Output**: Message format standard documented. Developers trained. Linter rules enforced.

3. **Extract all hardcoded strings**: Run the extraction scanner. Generate the source locale file (`en.json`).
   Verify: zero hardcoded strings remain. Add a CI check that fails on new hardcoded strings.
   - **Output**: Source locale file with all strings externalized. CI guard in place.

4. **Implement locale routing**: URL strategy: subdomain (`en.example.com`), subdirectory (`example.com/en/`), or TLD (`example.es`).
   Subdirectory is the default recommendation — best SEO, simplest infrastructure.
   - **Output**: Locale routing live. Language switcher functional.

### Phase 2 (~30 min): Translation Pipeline — Connect Dev to Translator
<!-- DEEP: 10+min -->

1. **Select and integrate a TMS** (Translation Management System):
   - **Lokalise**: Best UX for translators, strong API, screenshot support. $120+/mo.
   - **Phrase** (formerly PhraseApp): Best for developer workflows, Git sync, ICU-first. $125+/mo.
   - **Crowdin**: Best for open source (free for OSS), large community of volunteer translators. Free-$150/mo.
   - **POEditor**: Cheapest ($20/mo), decent API. Good for small teams.
   - **Custom/CLI-only**: Use `i18next-parser` + `tx` (Transifex CLI) or `crowdin-cli`. Zero UI cost.
   - **Output**: TMS integrated. Strings flow: repo → CI → TMS → translator → TMS → PR → repo.

2. **Set up continuous localization in CI/CD**:
   ```yaml
   # GitHub Actions sketch — push source strings on merge, pull translations nightly
   on:
     push:
       branches: [main]
       paths: ['src/locales/en/**']
   jobs:
     push-to-tms:
       steps:
         - run: crowdin-cli upload sources
     pull-translations:
       # Scheduled: every 6 hours or on demand
       steps:
         - run: crowdin-cli download
         - run: |
             if git diff --quiet; then exit 0; fi
             git checkout -b i18n/translations-$(date +%Y%m%d)
             git commit -am "chore(i18n): pull latest translations"
             gh pr create --title "i18n: translation update" --body "Automated."
   ```
   - **Output**: CI pipeline live. Translations update automatically. Zero manual sync.

3. **Define translation key naming convention**:
   - **Structured by component**: `checkout.payment.ccNumber.label` (recommended — findable, sortable)
   - **Flat with namespace**: `checkout:payment.ccNumber.label`
   - **Avoid**: Generic keys like `label123`, `error_msg_1` (translators can't guess context)
   - **Include context**: Suffix with `_label`, `_placeholder`, `_error`, `_tooltip`, `_aria`
   - **Output**: Naming convention documented. Automated linting for key format.

### Phase 3 (~20 min): Locale-Aware Everything — Format, Sort, Display

1. **Locale-aware formatting**: Never hardcode formats. Always use `Intl` APIs or ICU.
   - **Dates**: `new Intl.DateTimeFormat('de-DE').format(date)` → "21.07.2026" vs US "07/21/2026"
   - **Numbers**: `new Intl.NumberFormat('de-DE').format(1234567.89)` → "1.234.567,89"
   - **Currencies**: `new Intl.NumberFormat('ja-JP', {style: 'currency', currency: 'JPY'}).format(1000)` → "￥1,000"
   - **Units**: `new Intl.NumberFormat('en-US', {style: 'unit', unit: 'celsius'}).format(25)` → "25°C"
   - **Relative time**: `new Intl.RelativeTimeFormat('en', {numeric: 'auto'}).format(-1, 'day')` → "yesterday"
   - **List formatting**: `new Intl.ListFormat('en').format(['Alice', 'Bob', 'Charlie'])` → "Alice, Bob, and Charlie"
   - **Collation (sorting)**: `['ä', 'a', 'z'].sort(new Intl.Collator('de').compare)` → ['a', 'ä', 'z']
   - **Output**: Every displayed value uses locale-aware formatting. Audit passes with zero hardcoded format strings.

2. **Implement pluralization and gender rules**: Use ICU MessageFormat for all dynamic text.
   Polish has 4 plural forms (one, few, many, other). Arabic has 6. English has 2.
   Gender: French, Spanish, Arabic, Hindi require gendered forms. Test every rule.
   - **Output**: Plural and gender rules implemented and tested across all target locales.

3. **Implement RTL layout** (if needed): Use CSS logical properties everywhere.
   ```css
   /* DO: */  margin-inline-start: 1rem;  padding-inline-end: 2rem;
   /* NOT: */ margin-left: 1rem;          padding-right: 2rem;
   /* DO: */  text-align: start;           border-inline-start: 3px solid;
   /* NOT: */ text-align: left;            border-left: 3px solid;
   ```
   Use `dir="auto"` on user-generated content containers. Test with `direction: rtl` override.
   - **Output**: RTL layout verified with pseudo-localization. Visual diff screenshots for Arabic locale.

### Phase 4 (~15 min): Testing & Quality Assurance

1. **Pseudo-localization**: Generate a pseudo-locale that replaces characters with accented/Unicode equivalents
   and lengthens strings by 30-40% (German text averages 30% longer than English). Run in CI on every PR.
   Pseudo-locale catches: hardcoded strings, missing i18n wrappers, layout breaks on long text.
   - **Output**: Pseudo-locale CI job live. Zero i18n regressions merge to main.

2. **Visual diff testing**: Take screenshots of key pages in each locale. Compare pixel-diff with baseline.
   Tools: Percy, Chromatic, Playwright visual comparisons.
   - **Output**: Visual diff CI job for top 5 locales and top 20 pages.

3. **Locale coverage report**: Track % of strings translated per locale. Threshold: 95%+ for production
   locales, 80%+ for beta locales. Block release if primary locale drops below 95%.
   - **Output**: Coverage dashboard. CI gate on coverage threshold.

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `frontend-developer` | i18n wrapper usage, RTL CSS patterns, locale-aware component API, string extraction implementation | Before integrating i18n into components; ensures RTL readiness and proper key usage |
| `mobile-developer` | Platform-specific locale files, App Store/Play Store metadata requirements, mobile formatting constraints | Before implementing mobile i18n; platform conventions differ |
| `translation-manager` | String extraction config, TM schema, locale list, TMS API integration, glossary/termbase | Before setting up translation pipeline; ensures extraction format matches TMS expectations |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `qa-engineer` | Testing matrix (locales × devices × pages), visual diff baseline, pseudo-locale build | QA can't test localization without locale infrastructure |
| `frontend-developer` | i18n library configuration, locale detection, RTL layout patterns, locale-aware component API | Frontend builds hardcoded strings — expensive retrofit |
| `mobile-developer` | Mobile i18n framework setup, platform-specific locale files, offline translation support | Mobile ships single-language app — blocks international markets |

### Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| New locale requested by business | Product Manager, Content Strategist, Legal Advisor | Market sizing, content readiness, legal requirements, translation budget |
| Translation coverage drops below 95% for prod locale | QA Engineer, Product Manager | Release blocker — halt deploy until fixed |
| TMS API integration broken / translations stopped syncing | DevOps, Frontend Lead | Translations frozen; manual fallback needed |
| Pseudo-localization CI job finds new hardcoded strings | Frontend Developer responsible for PR | Fix before merge; i18n regression |
| RTL layout breaks on new feature | Frontend Developer, UI/UX Designer | Visual regression; fix or feature flag before release |
| Legal requirement for a language not yet supported | Legal Advisor, Product Manager | Compliance gap; prioritize or document risk acceptance |

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| New feature with user-facing strings merged without i18n wrapper | Run pseudo-localization CI; flag PR if new hardcoded strings detected | Catches i18n regression before translators see it — CI should block merge, not QA catch later |
| RTL locale (Arabic/Hebrew/Farsi) added to roadmap | Audit CSS for logical properties; run RTL pseudo-locale build; schedule native-speaker QA | RTL is not a CSS flip if you haven't used logical properties — early audit prevents 2-month refactor |
| Translation coverage drops below 95% for a production locale | Halt release; notify QA and Product Manager; escalate to translation-manager | Missing translations in production erode user trust — a half-translated app is worse than English-only |
| Pseudo-localization CI job finds new hardcoded strings in a PR | Reject merge; notify Frontend Developer to externalize strings before re-submit | Fixing hardcoded strings in dev costs minutes; in production it costs an app store review cycle |
| Third-party dependency adds new UI strings without i18n support | Audit dependency's i18n capabilities; wrap with locale-aware component; file upstream issue | Dependencies that render user-facing strings without i18n hooks break your entire locale coverage |
| Legal requirement mandates a language your TMS doesn't yet support | Notify Legal Advisor, translation-manager, Product Manager; assess TMS capabilities vs contract translators | Compliance gap carries regulatory fines — prioritize language support based on legal risk, not market size |
| Visual diff detects RTL layout regression on new page | Reject merge; notify Frontend Developer and UI/UX Designer; fix before release | RTL layout breaks compound — one missed page creates a pattern that cascades across the app |
| Locale file grows beyond 10K keys with no code-splitting | Refactor to lazy-load translations per route; measure bundle size impact per locale | Bundling all locales into the main bundle bloats initial load — users download 40 languages and use 1 |

## Scale Depth
<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-1K users)
- **What changes**: One locale file (`en.json`). No TMS. Translate via JSON diff + Google Translate for initial pass, then hire a freelance translator for polish. Pseudo-locale via a simple Node script. RTL: logical properties only if you plan to add RTL within 6 months; skip otherwise.
- **What's overkill**: TMS integration, continuous localization CI, visual diff testing, translation memory, glossary, dedicated i18n library abstraction layer. ICU MessageFormat (simple key-value is fine for 1-2 languages).
- **Coordination**: You are the i18n engineer. Calendar reminder every sprint to review strings.
- **Cost**: $0-500 (freelance translator for key pages only).
- **Transition trigger**: Second language requested by >5% of users or a paying customer.

### Small Team (2-10 people, 1K-100K users)
- **What changes**: 3-5 locales. TMS integration (Lokalise free tier or Crowdin OSS). ICU MessageFormat for plurals. CI pipeline pushes to TMS on merge. Pseudo-localization as a manual step before release. RTL: CSS logical properties everywhere. Basic locale-aware formatting via `Intl`.
- **What's overkill**: Dedicated i18n service, machine translation API integration, automated visual diff across all locales, translation memory optimization, locale-specific CDN routing.
- **Coordination**: Weekly i18n sync (15 min) with frontend lead. TMS admin = 1 person, 2 hrs/week.
- **Cost**: $0-300/mo (TMS free tier or starter).
- **Transition trigger**: 5+ locales OR translation turnaround time exceeds 1 sprint.

### Medium Team (10-50 people, 100K-1M users)
- **What changes**: 10-20 locales. Full TMS (paid). Continuous localization in CI/CD — strings push on merge, translations PR every 6 hours. Pseudo-localization in CI on every PR. Visual diff for top 5 locales. Translation memory and glossary active. Machine translation for initial pass (DeepL/Google Translate API) with human review. Locale-aware formatting everywhere. RTL: full support with native-speaker QA. Screenshot context in TMS for every string.
- **What's overkill**: Dedicated i18n service/team, on-the-fly machine translation for UGC, locale-specific microservices, programmatic quality scoring for translations.
- **Coordination**: Bi-weekly i18n review (30 min) with frontend, content, and QA. TMS admin = 0.5 FTE. Dedicated i18n champion per team.
- **Cost**: $500-2K/mo (TMS + machine translation API).
- **Transition trigger**: 20+ locales OR translation quality complaints from >2 locales OR legal requirement for a new language family (e.g., CJK, RTL, Cyrillic).

### Enterprise (50+ people, 1M+ users)
- **What changes**: 30-50+ locales. Dedicated i18n engineering team (2-3 engineers). Translation quality scoring with automated checks (spelling, terminology, placeholder integrity, length constraints). In-context editing (translators see strings in the actual UI). Locale-specific CDN routing and edge caching. A/B testing of translations. Machine translation with human post-editing at scale. Custom TMS workflows per locale maturity. Legal compliance automation (automated checks for mandatory language requirements). Locale-specific feature flags. Continuous localization with < 1 hour from string change to translation PR.
- **What's full production**: Dedicated i18n platform team. Translation quality metrics dashboard. Locale-specific performance monitoring. Cultural consulting for imagery and copy. Automated locale coverage gates in CI. Locale-specific A/B testing infrastructure.
- **Coordination**: Weekly i18n ops meeting. Monthly stakeholder review. Quarterly locale strategy review with product, legal, marketing. Dedicated TMS admin (1 FTE).
- **Cost**: $5K-30K+/mo (TMS enterprise + machine translation + team).
- **Transition trigger**: 30+ locales OR regulatory requirement for locale-specific legal content OR revenue from international markets >30% of total.

## What Good Looks Like

> Every user-facing string is externalized, translated, and renders correctly in every supported locale — pseudolocalization catches regressions in CI before translators ever see them. RTL layouts mirror LTR perfectly with CSS logical properties; no layout breaks, no truncated text, no orphaned directional assumptions. Dates, numbers, and currencies format correctly per locale using native `Intl` APIs, and plural and gender rules respect CLDR data. The translation pipeline pushes new strings to translators and pulls reviewed translations back as automated PRs within hours, not weeks. Native speakers review in-context, and quality gates block releases that fall below the translation completeness threshold.

### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | frontend-developer | UI with hardcoded strings, locale-ready component structure |
| **This** | localization-engineer | i18n architecture, translation pipeline, RTL support, locale formatting, pseudolocalization tests |
| **After** | qa-engineer | Validates all locale outputs, tests RTL layouts, verifies pseudo-localization catches issues |

Common chains:
- **Web app localization**: frontend-developer → localization-engineer → qa-engineer — Frontend builds the UI, localization externalizes strings and adds locale support, QA verifies across languages
- **Mobile app globalization**: mobile-developer → localization-engineer → release-manager — Mobile builds platform-specific UI, localization adds multi-language support, release manager coordinates app store localization metadata

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|---|---|---|
| `i18n-architecture` | New project setup or i18n overhaul | Choosing i18n library, message format, locale routing strategy, SSR vs CSR i18n |
| `translation-pipeline` | Connecting dev to translators | TMS selection, CI/CD integration, push/pull strategy, translation memory, glossary |
| `rtl-implementation` | Adding Arabic, Hebrew, Farsi, Urdu | CSS logical properties, component mirroring, BIDI text handling, RTL-specific QA |
| `locale-formatting` | Ensuring correct date/number/currency display | `Intl` APIs, ICU MessageFormat, CLDR data, plural/gender rules, collation |
| `pseudo-localization` | Before every release, in CI | Pseudo-locale generation, CI integration, catching hardcoded strings and overflow |
| `locale-detection` | Determining user language | Accept-Language parsing, GeoIP fallback, user preference, cookie vs URL vs subdomain |
| `continuous-localization` | Automating translation sync | CI/CD pipeline design, TMS API integration, automated PR creation, merge strategies |
| `translation-quality` | Ensuring translations are correct and consistent | Quality scoring, automated checks, glossary enforcement, native speaker review workflows |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Externalize on day one**: Adding i18n to a 200K LOC codebase costs 5-10x more than building it in from the start. Even if you only support English at launch, put every user-facing string in a locale file.
- **ICU MessageFormat for anything with variables**: Key-value `"Hello {name}"` breaks in languages with different word order or gender. ICU handles this. Exceptions: truly static strings (labels, headings with no variables).
- **Pseudo-localize in CI, not just before release**: A CI job that builds with pseudo-locale on every PR catches i18n regressions immediately, not 2 days before launch.
- **CSS logical properties everywhere — always**: `margin-inline-start` instead of `margin-left`. Costs nothing. Makes RTL support a CSS variable flip, not a 2-month refactor. This is the highest-ROI i18n decision you can make.
- **Never use GeoIP as the primary language detector**: A Swiss user with browser set to French shouldn't get German content. Accept-Language header first, user preference second, GeoIP as last-resort fallback.
- **Translate context, not words**: Provide translators with screenshots, descriptions of where the string appears, character limits, and whether it's a button/label/error/tooltip. A string without context is a guaranteed mistranslation.
- **Design for 30-50% text expansion**: German, Finnish, and Dutch text averages 30% longer than English. UI that looks perfect in English will overflow in German. Test with pseudo-locale that lengthens strings.
- **Code-split translations by locale**: Don't bundle all locales into the main bundle. Lazy-load only the current locale. Tree-shake ICU data per locale (`Intl` polyfills are large — load only what's needed).
- **Never concatenate translated strings**: `msg = translate("Page") + " " + pageNumber + " " + translate("of") + " " + totalPages` — this breaks in Japanese (word order), Arabic (RTL), Korean (counters). Use ICU: `"Page {current} of {total}"`.
- **Test with native speakers, not just bilingual colleagues**: A bilingual developer can verify correctness. A native speaker verifies naturalness. These are different quality bars. Budget for native-speaker QA per locale.

## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|---|---|
| Using physical CSS properties (`margin-left`, `padding-right`) throughout the codebase | Use CSS logical properties (`margin-inline-start`, `padding-inline-end`) from day one — makes RTL a CSS variable flip |
| Hardcoding strings in source files because "we only support English right now" | Externalize every user-facing string to locale files on day one — retrofitting in a 200K LOC codebase costs 5-10x more |
| Concatenating translated string fragments: `translate("Page") + " " + n + " " + translate("of")` | Use ICU MessageFormat: `"Page {current} of {total}"` — concatenation breaks in Japanese (word order), Arabic (RTL), Korean (counters) |
| Using GeoIP as the primary language detector | Use Accept-Language header first, user preference second, GeoIP only as last-resort fallback — Swiss users with French browsers shouldn't get German content |
| Shipping machine-translated content to Arabic/Hebrew/Farsi markets without native-speaker review | Budget for native-speaker post-editing — MT engines don't understand honorifics, cultural context, or religious sensitivities |
| Bundling all locale files into the main application bundle | Code-split translations per locale and lazy-load only the current one — tree-shake ICU data per locale to avoid shipping 40 languages of polyfills |
| Treating pseudo-localization as a pre-release manual step | Run pseudo-localization CI on every PR — catches hardcoded strings and overflow immediately, not 2 days before launch |
| Designing UI that fits English text perfectly without expansion buffer | Design for 30-50% text expansion — German, Finnish, and Dutch average 30% longer than English; test with pseudo-locale that lengthens strings |

## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| App store resubmission required to fix a typo — 7-day review delay | Error message text was hardcoded in a native Swift string. Typos/copy changes required a full app release | Extract all user-facing strings to locale files from day one. Use OTA update mechanisms (CodePush/expo-updates) for string-only changes. Add a CI check that fails if `console.log` or hardcoded strings > 5 chars are detected in JSX/SwiftUI/Compose | **Hardcoded strings are a deployment liability.** Every string should be externalized on day zero, even for single-language apps. A typo in production shouldn't require an app store review cycle to fix. When you can't OTA-edit, you're on a 7-day fix cycle for every string error |
| Arabic version of the app was unreadable — text overflowed and overlapped everywhere | The CSS used physical properties (`margin-left`, `padding-right`, `float: left`) exclusively. In RTL mode, all of these reversed incorrectly | Rewrite all CSS to use logical properties: `margin-inline-start`, `padding-inline-end`, `text-align: start`. Add `dir="auto"` to user-generated content. Deploy a pseudo-RTL locale in CI that tests every screen with Arabic text | **CSS logical properties are free insurance against RTL breakage.** Using `margin-inline-start` instead of `margin-left` costs nothing and makes RTL support a CSS variable flip. Without it, adding Arabic later is a 2-month refactor of every component. Write RTL-first, not RTL-later |
| German users saw dates like "06/04/2026" — is that June 4th or April 6th? | Server stored dates in ISO 8601 (correct) but the frontend displayed them using `new Date().toLocaleString()` without specifying a locale — defaulted to en-US format | Use `Intl.DateTimeFormat('de-DE')` explicitly. Send dates as ISO 8601 strings and format client-side per locale. Add locale detection tests that verify date format for each supported locale | **Dates are locale-specific. Always format client-side with the user's locale.** Don't assume en-US date format. Server should send ISO 8601; client should render with `Intl` APIs. A date displayed in the wrong format confuses users and erodes trust in financial/medical apps |
| Polish users saw "1 messages" instead of "1 message" — pluralization wrong | Used simple string interpolation `t('You have {count} messages')` instead of ICU MessageFormat plurals. Polish has 4 plural forms; English has 2 | Convert to ICU MessageFormat: `{count, plural, one {1 message} few {# messages} many {# messages} other {# messages}}`. Add CLDR plural rule verification in CI for all target locales | **English plural rules don't apply to most languages.** Polish has 4 forms, Arabic has 6, Russian has 4. Simple `{count}` interpolation breaks in every Slavic and Semitic language. Always use ICU MessageFormat for any string with a numeric variable. Test pluralization with real native speakers, not just Google Translate |
| Korean users complained the app felt like "machine-translated nonsense" | Machine translation was used without human post-editing. Cultural context was lost: Korean has honorific levels (formal/polite/casual) that MT engines don't handle correctly | Add human post-editing for all customer-facing text in Korean, Japanese, and Arabic. Use TM to catch re-translated strings. Implement LQA scoring with a minimum threshold for cultural sensitivity | **Machine translation without human review can offend users.** MT engines don't understand cultural context, honorifics, or brand voice. Budget for native-speaker post-editing for languages with strong cultural nuances. A translated app that feels "off" is worse than an English-only app |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  All user-facing strings externalized — zero hardcoded strings in the codebase (enforced by CI)
- [ ] **[S2]**  ICU MessageFormat used for all strings with variables, plurals, or gender
- [ ] **[S3]**  Locale routing functional — URL strategy consistent (subdirectory or subdomain), language switcher works
- [ ] **[S4]**  CSS logical properties used throughout (no `margin-left`/`margin-right`/`padding-left`/`padding-right`)
- [ ] **[S5]**  Pseudo-localization CI job runs on every PR and blocks merge on failures
- [ ] **[S6]**  Translation pipeline: strings push to TMS on merge to main; translations PR created automatically
- [ ] **[S7]**  Locale-aware formatting for dates, numbers, currencies, relative time, list formatting, and collation across all target locales
- [ ] **[S8]**  Plural rules tested for all target locales (Polish has 4 forms, Arabic has 6 — don't assume English-like rules)
- [ ] **[S9]**  RTL layout verified: pseudo-locale screenshots reviewed, `dir="auto"` on UGC containers, BIDI controls for mixed text
- [ ] **[S10]**  Translations code-split by locale — only current locale loaded, no 2MB bundle with 40 languages
- [ ] **[S11]**  hreflang tags implemented and verified (correct reciprocal links between all locale variants)
- [ ] **[S12]**  Translation coverage ≥ 95% for production locales; CI gate blocks release if below threshold
- [ ] **[S13]**  Visual diff testing for top 5 locales and top 20 pages — no unexpected layout shifts
- [ ] **[S14]**  Translation memory set up and populated — reuse existing translations to reduce cost and ensure consistency
- [ ] **[S15]**  Glossary defined and enforced in TMS — brand terms, technical terms, never-translate terms
- [ ] **[S16]**  Legal requirements verified: Quebec (French mandatory), EU (right to official language), any jurisdiction-specific rules
- [ ] **[S17]**  Accessibility verified: `lang` and `dir` attributes correct on `<html>`, screen reader language switches properly
- [ ] **[S18]**  Locale detection respects: user preference → Accept-Language → GeoIP fallback (NEVER GeoIP first)

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [ICU MessageFormat Specification](https://unicode-org.github.io/icu/userguide/format_parse/messages/) — Unicode Consortium
- [CLDR — Unicode Common Locale Data Repository](https://cldr.unicode.org/) — Locale-specific formatting data
- [W3C Internationalization Best Practices](https://www.w3.org/International/) — Authoritative i18n reference
- [CSS Logical Properties and Values](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values) — MDN
- [Lokalise API Documentation](https://developers.lokalise.com/) — TMS integration reference
- [Phrase CLI & API](https://developers.phrase.com/) — TMS integration reference
- [Crowdin CLI](https://github.com/crowdin/crowdin-cli) — TMS integration for CI/CD
- [FormatJS / react-intl](https://formatjs.io/) — ICU MessageFormat for React
- [i18next Ecosystem](https://www.i18next.com/) — Most popular JS i18n framework
- [Mozilla Fluent](https://projectfluent.org/) — Advanced i18n system by Mozilla
- [Apple String Catalogs (Xcode 15+)](https://developer.apple.com/documentation/xcode/localizing-and-varying-text-with-a-string-catalog)
- [references/locale-data-matrix.md](references/locale-data-matrix.md) — Locale format cheat sheet
- [references/tms-comparison.md](references/tms-comparison.md) — TMS feature comparison matrix
