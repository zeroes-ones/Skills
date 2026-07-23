# Scale Depth

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
