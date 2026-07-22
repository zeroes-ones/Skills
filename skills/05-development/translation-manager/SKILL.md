---
name: translation-manager
description: >-
  Translation management without human translators — translation memory (TM) strategy and maintenance, machine translation (MT) engine selection (DeepL, Google Cloud Translation, Azure Translator, ModernMT), glossary and termbase management, pseudo-localization for pre-flight testing, continuous localization pipeline design (Git-based, API-driven), string extraction and key-based identification (i18next, ICU MessageFormat, Fluent), translation quality automation (placeholder validation, ICU syntax check, length constraints, gender/plural coverage), TMS API integration (Lokalise, Phrase, Crowdin, Transifex), translation memory leveraging and fuzzy match optimization, cost optimization across MT engines, and automated linguist quality assurance (LQA) scoring. Use when setting up a localization pipeline without a human translation team, optimizing MT quality, managing translation memory at scale, or automating localization quality gates in CI/CD.
author: Sandeep Kumar Penchala
type: development
status: stable
version: "1.0.0"
updated: 2027-01-21
tags:
  - translation
  - localization
  - i18n
  - l10n
  - machine-translation
  - tms
token_budget: 3500
output:
  type: "code"
  path_hint: "./"
chain:
  consumes_from:
    - localization-engineer
    - frontend-developer
    - mobile-developer
  feeds_into:
    - localization-engineer
    - qa-engineer
    - ci-cd-builder
---
# Translation Manager

Orchestrate automated translation pipelines — configure machine translation engines, manage translation memory, automate quality checks, and run continuous localization without a human translation team.

## Route the Request
```
What do you need?
├── Set up a new localization pipeline → Jump to "Core Workflow > Phase 1"
├── Choose a machine translation engine → Go to "Decision Trees > MT Engine Selection"
├── Configure translation memory (TM) → Jump to "Core Workflow > Phase 2"
├── Add pseudo-localization for QA → Go to "Best Practices > Pseudolocalization"
├── Automate translation quality checks → Jump to "Core Workflow > Phase 4"
├── Optimize MT costs → Go to "Decision Trees > Cost Optimization"
├── Integrate with a TMS (Lokalise/Phrase/Crowdin) → Jump to "Core Workflow > Phase 3"
└── String extraction from codebase → Go to "Core Workflow > Phase 1"
```

## Ground Rules

- **Never commit machine-translated strings directly to production without validation.** MT output must pass automated quality gates: placeholder integrity, ICU syntax, length constraints, and forbidden character checks. One broken placeholder crashes the entire UI for that locale.
- **Translation memory is your compounding asset.** Every corrected translation goes back into TM. A 60% fuzzy match leveraged across 10,000 strings saves 6,000 translations. Build TM from day one — the ROI compounds with every new locale.
- **Pseudolocalization catches bugs before real translations exist.** Run pseudolocalized builds in CI. If the UI breaks with 2x-length strings, right-to-left rendering, or Unicode characters, it will break with real translations too. Catch it before you pay for translations.
- **String keys are forever; string values are temporary.** Use semantic keys (`checkout.payment.button.confirm`) not English-as-keys (`"Confirm Payment"`). If the English copy changes, the key stays stable. If you use English-as-keys, one marketing copy change forces re-translation of 47 locales.
- **MT quality varies dramatically by language pair and domain.** DeepL is excellent for European language pairs but non-existent for most Asian languages. Google Cloud Translation covers 130+ languages but produces lower quality for nuanced marketing copy. Always benchmark with your actual content, not generic test strings.

## When to Use

- You need to set up a localization pipeline that doesn't depend on human translators
- You are evaluating or switching machine translation engines
- You need to build and maintain translation memory across multiple projects
- You want to automate translation quality validation in CI/CD
- You are optimizing translation costs across locales and MT providers
- You need to integrate a TMS API for automated pull/push workflows
- You are adding pseudo-localization to your QA pipeline

## Decision Trees

### MT Engine Selection
```
What's your primary language pair?
├── European languages (EN↔DE/FR/ES/IT/NL/PL) → DeepL (highest quality)
├── Asian languages (EN↔JA/KO/ZH/TH/VI) → Google Cloud Translation (broadest coverage)
├── Arabic, Hebrew, Farsi (RTL languages) → Google Cloud Translation or Azure Translator
├── Mixed (10+ languages across families) → Google Cloud Translation (130+ languages)
│   └── Supplement with DeepL for European subset if budget allows
└── Domain-specific (medical, legal, financial) → ModernMT (adaptive context-aware)
    └── Or: custom model trained on your TM + glossary on Google AutoML
```

### Cost Optimization
```
Translation volume per month?
├── < 10K strings → Pay-as-you-go per-char pricing, focus on quality not cost
├── 10K-100K strings → Negotiate volume discounts, consider annual commitment
├── 100K-1M strings → Multi-engine routing: send high-visibility content to premium MT
│   └── Pattern: marketing pages → DeepL, help docs → Google, UI strings → TM first
└── > 1M strings → Self-host open-source MT (LibreTranslate, OpenNMT) for base layer
    └── Premium MT only for customer-facing content
```

## Core Workflow

### Phase 1: String Extraction & Key Design (~2 hours)
Audit the codebase for hardcoded strings. Implement key-based extraction using the framework's native i18n library: `i18next` (React/Next.js), `vue-i18n` (Vue), `ngx-translate` (Angular), `flutter_localizations` (Flutter), `react-native-i18n` (React Native). Design the key naming convention: `{domain}.{feature}.{component}.{element}`. Example: `checkout.payment.creditcard.cvv_label`. Extract all source strings to a base locale JSON file (typically `en.json`). Verify no hardcoded strings remain using eslint-plugin-i18next or a grep for quote patterns.

### Phase 2: Translation Memory Setup (~1 hour)
Initialize TM from existing translations if available. Configure TM format (TMX is the standard interchange format — every TMS supports it). Set fuzzy match thresholds: ≥80% for auto-population, 60-79% for suggestion, < 60% sent to MT. TM stores: source string, target string, locale, context (file path + key), last modified, and quality score. A 10,000-entry TM with 80% leverage across 5 new locales saves ~40,000 new translations.

### Phase 3: TMS Integration (~3 hours)
Choose TMS: Lokalise (best UX, generous free tier), Phrase (most powerful API, best for developers), Crowdin (best open-source support, GitHub integration), Transifex (enterprise focus). Configure API-based pull/push workflow: source strings pushed from CI on merge to main → TMS auto-translates via configured MT engine → translated strings pulled back to repo as locale JSON files on a schedule or trigger. Implement webhook-based PR creation: when translations are ready in TMS, a PR is automatically created with the new locale files.

### Phase 4: Automated Quality Gates (~2 hours)
Implement pre-commit and CI quality checks for translation files. Placeholder integrity: every `{0}`, `%s`, `{{variable}}` in the source must appear in the translation. ICU MessageFormat validation: parse ICU syntax and verify plural forms and selectors are intact. Length constraint check: flag translations exceeding UI element character limits (button: 30 chars, heading: 60 chars, body: 300 chars). Forbidden character detection: flag translations containing characters outside the target locale's expected character set. LQA scoring: automated score based on placeholder match (30%), length compliance (25%), ICU validity (25%), and termbase consistency (20%). Gate threshold: score ≥ 90 to pass, 80-89 warns, < 80 blocks.

## Best Practices

1. **Pseudolocalize before translating.** Prefix with [^^^] and suffix with [vvv] to detect truncated strings. Double the string length using Unicode lookalikes (ä for a, é for e). This catches 80% of i18n bugs before you pay a single translation cost.
2. **Use glossary/termbase for brand and technical terms.** `npm install` should NEVER be translated. Brand names, API method names, and technical terms must be locked in the glossary with `translate: false`.
3. **TM leverage should be measured and reported.** Track: % of strings auto-translated from TM, % from MT, % requiring human post-editing. Goal: > 70% TM leverage across locales.
4. **Continuous localization, not batch.** Push new source strings on every merge to main. Pull translations daily. Batching creates a localization bottleneck where 2 weeks of translations block a release.
5. **Plural forms are not optional.** ICU MessageFormat supports all CLDR plural forms (zero, one, two, few, many, other). Arabic has 6 forms, Russian has 4, English has 2. Never assume singular/plural is enough.
6. **String context matters more than the string itself.** A TM entry for "Post" could mean blog post, mail post, or after something. Always include context metadata: file path, component name, and a developer comment.
7. **MT post-editing cost should drive engine selection.** If DeepL costs $25/1M chars but requires 10% post-editing, and Google costs $20/1M chars but requires 25% post-editing, DeepL is cheaper when post-editing costs $100/hour.
8. **Screen reader strings need separate handling.** `aria-label` strings are consumed by screen readers, not visually rendered. They have no length constraints but require high accuracy — prioritize TM+human review over raw MT for accessibility strings.

## Error Decoder

| Error | Root Cause | Fix |
|-------|-----------|-----|
| Production bug: entire UI in locale `fr` shows English | Fallback chain misconfigured — locale file missing, fell through to source | Add fallback validation in CI: every supported locale must have a JSON file with > 90% of source keys. `i18next` config: `fallbackLng: false` in production, `fallbackLng: 'en'` only in dev. |
| ICU syntax error: "Expected \"}\" but found \":\"" in production build | MT engine translated the ICU variable name or broke the syntax | Add ICU parse validation in CI. Never send ICU strings to MT — extract variables before translation, re-insert after. Pattern: `t('You have {count} items', { count: 5 })` — translate "You have {} items" as the string, `{count}` is the variable placeholder. |
| TM leverage dropped from 85% to 40% after refactor | Keys changed during code cleanup broke TM matching | Keys are an API contract. If you rename keys, provide a migration map. Better: extract strings by content hash, not developer-chosen key — TM matches on the source string, not the key. |
| MT cost 3x budget in first month | Every CI build triggers re-translation of all strings | Only send new strings to MT. Track hash of source strings — if unchanged, don't re-translate. Use TM hit first, MT only on TM miss. Cache MT results with 30-day TTL. |
| Japanese translations consistently overflow buttons | Character limits defined for Latin script only | Japanese characters are wider. Define limits in pixels/ems, not characters. Or: Japanese max chars = English max chars × 0.6. Test with pseudolocalization at 2x length. |

## Production Checklist

- [ ] [TM1] String extraction script runs in CI — build fails if hardcoded strings detected
- [ ] [TM2] Semantic key convention documented and enforced (eslint-plugin-i18next)
- [ ] [TM3] Translation memory in TMX format with ≥ 5,000 entries per supported locale
- [ ] [TM4] Glossary/termbase configured with brand terms, API names, and technical terms locked
- [ ] [TM5] Pseudolocalization build runs in CI and QA validates before any real translation purchase
- [ ] [TM6] MT engine selected and benchmarked against actual content (not generic test strings)
- [ ] [TM7] TMS API integration: push on merge to main, pull translations daily via automated PR
- [ ] [TM8] Quality gate in CI: placeholder integrity, ICU validation, length constraints, forbidden chars
- [ ] [TM9] LQA score threshold enforced: ≥ 90 pass, 80-89 warn, < 80 block
- [ ] [TM10] Fallback chain validated: every locale file has ≥ 90% of source keys
- [ ] [TM11] TM leverage metrics tracked monthly — target > 70% across all locales
- [ ] [TM12] MT costs tracked per-engine per-locale — alert if cost-per-string exceeds threshold
- [ ] [TM13] Accessibility strings (aria-labels, alt text) flagged for higher quality review
- [ ] [TM14] Plural forms configured for all target locales using CLDR rules

## Cross-Skill Coordination

| Skill | When to Coordinate | What to Share |
|-------|-------------------|--------------|
| **localization-engineer** | i18n architecture, locale detection, RTL layout | String extraction config, TM schema, locale list |
| **frontend-developer** | String extraction from React/Next.js, key implementation | i18next config, namespace strategy, key conventions |
| **mobile-developer** | String extraction from React Native/Flutter, app store localization | Platform-specific locale files, App Store/Play Store metadata |
| **qa-engineer** | Pseudolocalization testing, translation quality gates | LQA score thresholds, test locale builds |
| **ci-cd-builder** | Continuous localization pipeline, automated PRs from TMS | Webhook config, pipeline triggers, quality gate scripts |
| **technical-writer** | Documentation translation, help center localization | Glossary for technical terms, style guide for each locale |
| **seo-specialist** | hreflang tags, localized SEO metadata | Translated meta descriptions, localized URLs |

## What Good Looks Like

**What good looks like:** A developer merges a PR with a new feature. Within 30 minutes, source strings are extracted, pushed to TMS, machine-translated for 12 locales, quality-checked automatically, and a PR opens with translated JSON files. The QA team tests the pseudolocalized build and finds zero layout bugs before any real translation costs are incurred. TM leverage is 78% — new strings reuse existing translations where possible. MT quality scores average 93/100 across all locales. Total human intervention: zero. Total time from code merge to translated build: under 2 hours.

## References

- Translation Memory Best Practices: references/tm-strategy.md
- MT Engine Comparison Matrix: references/mt-engine-comparison.md
- TMS Integration Guide (Lokalise/Phrase/Crowdin): assets/tms-integration-guide.md
- ICU MessageFormat Specification: https://unicode-org.github.io/icu/userguide/format_parse/messages/
- CLDR Plural Rules: https://cldr.unicode.org/index/cldr-spec/plural-rules
- i18next Documentation: https://www.i18next.com/
- Mozilla Fluent Project: https://projectfluent.org/
