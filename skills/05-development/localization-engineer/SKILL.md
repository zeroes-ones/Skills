---
name: localization-engineer
description: i18n/l10n architecture, translation pipelines, RTL layout, locale-aware formatting (dates/numbers/currencies), Unicode/BIDI, pseudo-localization, continuous localization in CI/CD, TMS integration (Lokalise/Phrase/Crowdin), and locale detection. Trigger: i18n, l10n, internationalization, localization, translation, RTL, multilingual, locale, globalization, g11n, language support, cultural adaptation. Works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI.
author: Sandeep Kumar Penchala
---

# Localization / i18n-L10n Engineer

Design and implement end-to-end internationalization (i18n) and localization (l10n) systems. This skill covers message extraction, translation pipeline architecture, locale-aware formatting, RTL layout, pseudo-localization testing, and continuous localization integrated into CI/CD. Every decision balances developer ergonomics, translator workflow, and end-user experience across languages and cultures.

## Decision Trees

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
```

## Core Workflow

### Phase 1: i18n Foundation — Externalize & Standardize

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

### Phase 2: Translation Pipeline — Connect Dev to Translator

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

### Phase 3: Locale-Aware Everything — Format, Sort, Display

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

### Phase 4: Testing & Quality Assurance

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

| Coordinate With | When (Trigger) | What Info Flows |
|---|---|---|
| **Frontend Developer** | Component development, CSS architecture | i18n wrapper usage, RTL CSS patterns, locale-aware component API |
| **Backend Developer** | API responses that contain user-facing text | Locale parameter in API, server-side formatting, error message externalization |
| **Fullstack Developer** | SSR i18n, locale routing, cookie handling | Locale detection strategy, SSR-safe i18n initialization, hreflang tags |
| **UI/UX Designer** | RTL mockups, layout with longer text, cultural imagery | RTL-flipped designs, text expansion allowances (30-50%), culturally appropriate icons/imagery |
| **QA Engineer** | Locale testing, visual regression, pseudo-locale QA | Testing matrix (locales × devices × pages), visual diff baseline, pseudo-locale build |
| **Content Strategist** | Marketing copy, tone of voice across locales | Transcreation guidelines (not literal translation), cultural sensitivity review, locale-specific campaigns |
| **DevOps/CI-CD Builder** | Continuous localization pipeline | CI job for push/pull to TMS, deployment of locale files, cache invalidation for new translations |
| **Accessibility Auditor** | Screen reader text, ARIA labels across languages | Translated ARIA attributes, RTL screen reader behavior, language attribute correctness |
| **SEO Specialist** | hreflang implementation, localized SEO | hreflang tag accuracy, localized keyword strategy, duplicate content across locales |
| **Legal Advisor / Compliance Officer** | Language requirements by jurisdiction | Quebec (French mandatory), EU (all official languages), Switzerland (DE/FR/IT), India (22 official languages) |
| **Product Manager** | Locale launch prioritization | Market sizing per locale, translation cost estimates, locale launch calendar |
| **Performance Engineer** | Lazy-loading translations, bundle size impact | Code-split by locale, measure translation bundle size, tree-shake unused translations |

### Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| New locale requested by business | Product Manager, Content Strategist, Legal Advisor | Market sizing, content readiness, legal requirements, translation budget |
| Translation coverage drops below 95% for prod locale | QA Engineer, Product Manager | Release blocker — halt deploy until fixed |
| TMS API integration broken / translations stopped syncing | DevOps, Frontend Lead | Translations frozen; manual fallback needed |
| Pseudo-localization CI job finds new hardcoded strings | Frontend Developer responsible for PR | Fix before merge; i18n regression |
| RTL layout breaks on new feature | Frontend Developer, UI/UX Designer | Visual regression; fix or feature flag before release |
| Legal requirement for a language not yet supported | Legal Advisor, Product Manager | Compliance gap; prioritize or document risk acceptance |
| Translation memory shows 40%+ overlap with existing content | Content Strategist, TMS admin | Reuse existing translations; reduce cost and turnaround |

## Scale Depth

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

## Sub-Skills

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

## Production Checklist

- [ ] All user-facing strings externalized — zero hardcoded strings in the codebase (enforced by CI)
- [ ] ICU MessageFormat used for all strings with variables, plurals, or gender
- [ ] Locale routing functional — URL strategy consistent (subdirectory or subdomain), language switcher works
- [ ] CSS logical properties used throughout (no `margin-left`/`margin-right`/`padding-left`/`padding-right`)
- [ ] Pseudo-localization CI job runs on every PR and blocks merge on failures
- [ ] Translation pipeline: strings push to TMS on merge to main; translations PR created automatically
- [ ] Locale-aware formatting for dates, numbers, currencies, relative time, list formatting, and collation across all target locales
- [ ] Plural rules tested for all target locales (Polish has 4 forms, Arabic has 6 — don't assume English-like rules)
- [ ] RTL layout verified: pseudo-locale screenshots reviewed, `dir="auto"` on UGC containers, BIDI controls for mixed text
- [ ] Translations code-split by locale — only current locale loaded, no 2MB bundle with 40 languages
- [ ] hreflang tags implemented and verified (correct reciprocal links between all locale variants)
- [ ] Translation coverage ≥ 95% for production locales; CI gate blocks release if below threshold
- [ ] Visual diff testing for top 5 locales and top 20 pages — no unexpected layout shifts
- [ ] Translation memory set up and populated — reuse existing translations to reduce cost and ensure consistency
- [ ] Glossary defined and enforced in TMS — brand terms, technical terms, never-translate terms
- [ ] Legal requirements verified: Quebec (French mandatory), EU (right to official language), any jurisdiction-specific rules
- [ ] Accessibility verified: `lang` and `dir` attributes correct on `<html>`, screen reader language switches properly
- [ ] Locale detection respects: user preference → Accept-Language → GeoIP fallback (NEVER GeoIP first)

## References

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
