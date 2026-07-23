# Core Workflow — Full Implementation

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
