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
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What do you need?
├── Set up a new localization pipeline → Jump to "Core Workflow > Phase 1"
├── Choose a machine translation engine → Go to "Decision Trees > MT Engine Selection"
├── Configure translation memory (TM) → Jump to "Core Workflow > Phase 2"
├── Add pseudo-localization for QA → Go to "Best Practices > Pseudolocalization"
├── Automate translation quality checks → Jump to "Core Workflow > Phase 4"
├── Optimize MT costs → Go to "Decision Trees > Cost Optimization"
├── Integrate with a TMS (Lokalise/Phrase/Crowdin) → Jump to "Core Workflow > Phase 3"
├── Need i18n architecture and pipeline → Invoke localization-engineer skill instead
├── Need frontend string extraction → Invoke frontend-developer skill instead
├── Need mobile string extraction → Invoke mobile-developer skill instead
├── Need QA for translation quality → Invoke qa-engineer skill instead
├── Need CI/CD integration for localization → Invoke ci-cd-builder skill instead
└── String extraction from codebase → Go to "Core Workflow > Phase 1"
```

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

- **Never commit machine-translated strings directly to production without validation.** MT output must pass automated quality gates: placeholder integrity, ICU syntax, length constraints, and forbidden character checks. One broken placeholder crashes the entire UI for that locale.
- **Translation memory is your compounding asset.** Every corrected translation goes back into TM. A 60% fuzzy match leveraged across 10,000 strings saves 6,000 translations. Build TM from day one — the ROI compounds with every new locale.
- **Pseudolocalization catches bugs before real translations exist.** Run pseudolocalized builds in CI. If the UI breaks with 2x-length strings, right-to-left rendering, or Unicode characters, it will break with real translations too. Catch it before you pay for translations.
- **String keys are forever; string values are temporary.** Use semantic keys (`checkout.payment.button.confirm`) not English-as-keys (`"Confirm Payment"`). If the English copy changes, the key stays stable. If you use English-as-keys, one marketing copy change forces re-translation of 47 locales.
- **MT quality varies dramatically by language pair and domain.** DeepL is excellent for European language pairs but non-existent for most Asian languages. Google Cloud Translation covers 130+ languages but produces lower quality for nuanced marketing copy. Always benchmark with your actual content, not generic test strings.

## When to Use
<!-- STANDARD: 3min -->

- You need to set up a localization pipeline that doesn't depend on human translators
- You are evaluating or switching machine translation engines
- You need to build and maintain translation memory across multiple projects
- You want to automate translation quality validation in CI/CD
- You are optimizing translation costs across locales and MT providers
- You need to integrate a TMS API for automated pull/push workflows
- You are adding pseudo-localization to your QA pipeline

## Decision Trees
<!-- STANDARD: 3min -->

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

<!-- DEEP: 10+min -->
## Core Workflow

### Phase 1: String Extraction & Key Design (~2 hours)
Audit the codebase for hardcoded strings. Implement key-based extraction using the framework's native i18n library: `i18next` (React/Next.js), `vue-i18n` (Vue), `ngx-translate` (Angular), `flutter_localizations` (Flutter), `react-native-i18n` (React Native). Design the key naming convention: `{domain}.{feature}.{component}.{element}`. Example: `checkout.payment.creditcard.cvv_label`. Extract all source strings to a base locale JSON file (typically `en.json`). Verify no hardcoded strings remain using eslint-plugin-i18next or a grep for quote patterns.

### Phase 2: Translation Memory Setup (~1 hour)
<!-- DEEP: 10+min -->
Initialize TM from existing translations if available. Configure TM format (TMX is the standard interchange format — every TMS supports it). Set fuzzy match thresholds: ≥80% for auto-population, 60-79% for suggestion, < 60% sent to MT. TM stores: source string, target string, locale, context (file path + key), last modified, and quality score. A 10,000-entry TM with 80% leverage across 5 new locales saves ~40,000 new translations.

### Phase 3: TMS Integration (~3 hours)
Choose TMS: Lokalise (best UX, generous free tier), Phrase (most powerful API, best for developers), Crowdin (best open-source support, GitHub integration), Transifex (enterprise focus). Configure API-based pull/push workflow: source strings pushed from CI on merge to main → TMS auto-translates via configured MT engine → translated strings pulled back to repo as locale JSON files on a schedule or trigger. Implement webhook-based PR creation: when translations are ready in TMS, a PR is automatically created with the new locale files.

### Phase 4: Automated Quality Gates (~2 hours)
<!-- DEEP: 10+min -->
Implement pre-commit and CI quality checks for translation files. Placeholder integrity: every `{0}`, `%s`, `{{variable}}` in the source must appear in the translation. ICU MessageFormat validation: parse ICU syntax and verify plural forms and selectors are intact. Length constraint check: flag translations exceeding UI element character limits (button: 30 chars, heading: 60 chars, body: 300 chars). Forbidden character detection: flag translations containing characters outside the target locale's expected character set. LQA scoring: automated score based on placeholder match (30%), length compliance (25%), ICU validity (25%), and termbase consistency (20%). Gate threshold: score ≥ 90 to pass, 80-89 warns, < 80 blocks.

## Best Practices
<!-- STANDARD: 3min -->

1. **Pseudolocalize before translating.** Prefix with [^^^] and suffix with [vvv] to detect truncated strings. Double the string length using Unicode lookalikes (ä for a, é for e). This catches 80% of i18n bugs before you pay a single translation cost.
2. **Use glossary/termbase for brand and technical terms.** `npm install` should NEVER be translated. Brand names, API method names, and technical terms must be locked in the glossary with `translate: false`.
3. **TM leverage should be measured and reported.** Track: % of strings auto-translated from TM, % from MT, % requiring human post-editing. Goal: > 70% TM leverage across locales.
4. **Continuous localization, not batch.** Push new source strings on every merge to main. Pull translations daily. Batching creates a localization bottleneck where 2 weeks of translations block a release.
5. **Plural forms are not optional.** ICU MessageFormat supports all CLDR plural forms (zero, one, two, few, many, other). Arabic has 6 forms, Russian has 4, English has 2. Never assume singular/plural is enough.
6. **String context matters more than the string itself.** A TM entry for "Post" could mean blog post, mail post, or after something. Always include context metadata: file path, component name, and a developer comment.
7. **MT post-editing cost should drive engine selection.** If DeepL costs $25/1M chars but requires 10% post-editing, and Google costs $20/1M chars but requires 25% post-editing, DeepL is cheaper when post-editing costs $100/hour.
8. **Screen reader strings need separate handling.** `aria-label` strings are consumed by screen readers, not visually rendered. They have no length constraints but require high accuracy — prioritize TM+human review over raw MT for accessibility strings.

## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|---|---|
| Selecting MT engine based on cost-per-character alone, ignoring post-editing cost | Calculate total cost: (MT cost + (post-editing hours × editor rate)). DeepL at $25/1M chars with 10% edit rate is cheaper than Google at $20/1M chars with 25% edit rate |
| Sending ICU MessageFormat strings through MT without stripping variables first | Extract variables like `{count}` before MT, re-insert after translation — ICU syntax is structural code, not translatable content |
| Renaming i18n keys during code refactors without providing a migration map | Use content-hash-based keys (match on source string hash) or provide a key migration map — TM matches on keys, not content |
| Running MT re-translation on all source strings every CI build instead of only changed strings | Hash source strings; only send new/changed strings to MT; cache results — re-translating unchanged strings wastes 60-80% of MT budget |
| Defining UI character limits in character counts for CJK markets | Define limits in pixels/ems — Japanese/Chinese/Korean characters are 1.5-2x wider than Latin script characters |
| Importing acquired company TMX without validating source language codes match your project | Validate source language (`en-US` vs `en-GB`), XML well-formedness, segment count; run dry-run import first |
| Using the same glossary for all locales without cultural sensitivity review | Add cultural sensitivity glossary per locale: terms to never translate literally, religious terms, national references, body parts — especially for Arabic, Hebrew, Farsi |
| Shipping MT-only translations to markets with strong cultural language norms without human post-editing | Budget native-speaker post-editing for customer-facing content in Korean (honorifics), Japanese (politeness levels), Arabic (cultural sensitivity) — MT can offend entire markets |

## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Production UI in `fr` locale shows English everywhere | Fallback chain misconfigured — locale file was missing keys, fell through to source language silently | Add fallback validation in CI: every supported locale must have > 90% of source keys. Set `fallbackLng: false` in production (only `'en'` in dev). Add a locale coverage report to the build output | **Silent fallback hides missing translations.** If a locale file is missing keys, falling back to English should be LOUD (logs, alerts) so it gets fixed. Don't let missing translations hide behind silent fallback to source language |
| Production crash: ICU syntax error in `fr` locale — entire screen blank | MT engine translated the ICU variable `{count}` to `{nombre}` — broke the message syntax | Add ICU parse validation in CI on every locale file. Strip ICU variables before sending to MT, re-insert after translation. Use `Intl.MessageFormat` parser to validate syntax before deploy | **Never send ICU syntax through machine translation.** Variables like `{count}` or `{name}` are structural, not textual — MT engines don't know this. Extract variables before translation, re-insert after. ICU syntax is code, not content |
| TM leverage dropped from 85% to 40% after a code refactor — translation costs tripled | Developer renamed i18n keys during a refactor (`checkout.pay.btn` → `payment.checkout.button`) — TM matches on keys, not content | Use content-hash-based keys (match on source string hash) instead of developer-chosen keys. Or: provide a key migration map when renaming. Never rename keys without updating the TM | **Translation keys are an API contract between devs and translators.** Changing keys without a migration map destroys TM leverage. Content-addressed keys (hash of source string) survive refactors. TM leverage is a financial metric — a drop from 85% to 40% costs real money |
| Monthly MT bill hit $3,200 — budget was $1,000 | CI pipeline pushed ALL source strings to MT on every build, including unchanged strings — re-translated 50,000 strings per week that were already translated | Track hash of source strings — only send new/changed strings to MT. Set up TM-first routing: check TM before MT. Cache MT results with 30-day TTL. Add MT cost alerts at 80% of monthly budget | **Re-translating the same strings is the most expensive CI mistake.** Only send new or changed strings to MT. Hash-based deduplication saves 60-80% of MT costs. Set up cost monitoring before you get the bill — not after |
| Japanese button labels overflow and clip in production — buttons show "... 確認" (truncated) | Character limits were defined in characters, not pixels. English "Confirm" (7 chars) fits in 60px. Japanese "確認する" (4 chars) is 1.5x wider per character | Define UI limits in ems/pixels, not character counts. Use pseudolocalization at 2x string length to catch overflow. For buttons: use `min-width` + `padding` with `text-overflow: ellipsis` as last resort | **Character count limits assume Latin script widths.** Japanese, Chinese, Korean characters are 1.5-2x wider than Latin. Test every UI element with pseudolocalized text at 2x source length. Pixel-based limits, not character-based |
| Aggressive machine translation offended Arabic-speaking users — app was removed from the App Store in UAE | MT engine produced a religiously insensitive phrase in Arabic. No glossary was configured to block cultural-taboo terms | Add a cultural sensitivity glossary: terms to never translate literally (religious terms, national references, body parts). Add human post-editing for Arabic, Hebrew, and Farsi. Implement LQA scoring with cultural sensitivity checks | **Machine translation without cultural context can offend entire markets.** Arabic, Hebrew, and Farsi need native-speaker post-editing for customer-facing content. Never ship MT-only translations to culturally sensitive markets. A glossary of forbidden translations is a minimum requirement — a native speaker reviewer is better |
| Translation key renamed causing ALL locales to silently fall back to English | Developer renamed `settings.notifications.title` to `settings.alerts.heading` without updating locale files — all 12 language files fell through to English | Provide a key migration script when renaming keys. Use content-hash-based keys instead of semantic keys. Add CI check: if any locale has < 90% key coverage compared to source, fail the build. | A rebranding exercise renamed 200+ i18n keys across an entire product. Every non-English locale silently fell back to English for 6 months before anyone noticed. The VP of international had to explain to the board why local market NPS dropped. |
| Regional date formats caused scheduling errors in German locale | `formatDate(date, "MM/dd/yyyy")` was hardcoded instead of using locale-aware formatting. German users saw "03/04/2025" and interpreted it as March 4 instead of April 3. | Never hardcode date/time/number formats. Use `Intl.DateTimeFormat(locale)`. Test every locale-specific format with actual locale data, not just the development locale. | A travel booking app's German users kept booking incorrect dates because `04/03/2025` was parsed as April 3 in code but read as March 4 by users. Support tickets tripled in the German market. |
| Plural form crash in Polish — 20% of users on older Android saw app crash | Polish has 4 plural forms (1, few, many, other). The translation for "many" was missing, causing a runtime crash on older CLDR versions. | Use a plural form library that handles all CLDR plural categories per locale. Test with non-English locales that have complex plural rules (Arabic: 6 forms, Polish: 4 forms, Russian: 4 forms). | Missing plural forms are the #1 cause of Android crashes in Slavic-language locales. The fix for Polish added 3 translations per plural-dependent string. |
| RTL layout broke entirely after translation deployment | Arabic locale was added but CSS didn't support `dir="rtl"`. Entire UI mirrored incorrectly — icons faced wrong direction, text overflowed containers. | Add RTL CSS support before translating to Arabic/Hebrew/Farsi. Use logical CSS properties (`margin-inline-start` instead of `margin-left`). Test RTL layout in CI with pseudolocalization. | A health app's Arabic launch had to be rolled back within 24 hours because the RTL UI clipped all medication dosage labels. The fix took 3 weeks and delayed the Middle East market entry by a quarter. |
| Translation memory corrupted by bulk import of mismatched TMX | Acquired company's TMX file had different source-language codes (`en-US` vs `en-GB`), causing TM to match wrong segments | Validate TMX imports: check source language code matches project configuration, check for XML well-formedness, verify segment count against expected. Run TMX import in dry-run mode first. | Merging TM databases from two companies producing 80K mismatched segments. Translation costs doubled for 6 months before the TM was rebuilt from scratch. Recovery took 3 months of manual cleanup. |

## Production Checklist
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `localization-engineer` | i18n architecture, locale detection, RTL layout, locale-aware formatting, ICU MessageFormat patterns | Before configuring TMS; ensures translation pipeline matches engineering architecture |
| `frontend-developer` | String extraction from React/Next.js, i18next config, namespace strategy, key conventions | Before pushing source strings to TMS; ensures keys follow project conventions |
| `mobile-developer` | Platform-specific locale files, App Store/Play Store metadata, mobile formatting constraints | Before translating mobile strings; platform conventions differ |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `localization-engineer` | TM schema, locale list, TMS API integration, quality gate scripts, translated locale files | i18n pipeline can't auto-sync without TMS configuration |
| `qa-engineer` | LQA score thresholds, test locale builds, pseudolocalization configuration, quality gate results | QA can't validate translations without quality automation |
| `ci-cd-builder` | Webhook config, pipeline triggers, quality gate scripts, automated PR configuration | CI/CD can't automate localization pipeline without integration specs |

### Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| TMS integration broken / translations stopped syncing | localization-engineer, ci-cd-builder | Translations frozen; manual fallback needed |
| Translation coverage drops below 95% | qa-engineer, localization-engineer | Release blocker — halt deploy until fixed |
| MT cost spikes 3x budget | frontend-developer (source owner) | Audit source strings; reduce unnecessary re-translation |
| New locale added to TMS | localization-engineer, qa-engineer | Configure locale detection, test infrastructure, CI pipeline |
| Quality gate blocking: LQA score < 80 | qa-engineer, localization-engineer | Investigate MT engine quality or TM degradation |

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| New locale added to TMS | Notify localization-engineer, qa-engineer, content-strategist; configure locale detection, CI pipeline, QA test plan | New locale without infrastructure creates the illusion of translation readiness — strings are translated but nothing renders |
| MT engine quality drops below threshold for a locale (BLEU score decline > 5%) | Audit recent source strings for ICU syntax leakage; compare MT output against TM baseline; consider engine swap | MT quality degradation compounds silently — by the time users complain, you've shipped bad translations for weeks |
| TM leverage drops below 60% after a code refactor | Audit i18n key changes; restore key migration map; rebuild TM from content hashes | Key renaming without migration is the #1 cause of TM leverage collapse — each renamed key is a new translation cost |
| New vendor/agency onboarded for a locale | Validate TMX import; run LQA calibration session; configure glossary enforcement; review first batch before pipeline integration | New translators bring style inconsistency — calibration prevents 6 months of rework |
| Glossary conflict detected — two translators disagree on a brand term translation | Escalate to Brand/Marketing; lock glossary entry with `translate: false` if needed; notify all translators | Brand term inconsistency across locales fragments brand identity — lock terms before they diverge |
| ICU syntax error in translated locale file passes CI | Strengthen ICU validation in quality gate; strip variables before MT, re-insert after; add pre-deploy syntax check | ICU variables like `{count}` are code, not content — MT engines corrupt them; protect structural syntax |
| Continuous localization pipeline latency exceeds 12 hours | Audit TMS API throughput; check webhook reliability; add pipeline health alert | When translations take >12 hours from merge to PR, developers bypass the pipeline and hardcode strings |
| Accessibility string (aria-label) translated with MT-only, no human post-editing | Flag accessibility strings for TM+human review only; never raw MT for screen reader content | Screen reader users rely on label accuracy — a mistranslated aria-label is a broken interface, not just a bad string |

## Scale Depth: Solo → Small → Medium → Enterprise
<!-- STANDARD: 3min -->

### Solo
Single developer handles translations via crowd-sourced or basic PO files. Focus: getting strings translated at all. Skip: translation memory, QA pipelines, context notes. Coordination: with developers on string freeze timing.

### Small Team
Dedicated translation manager, localization platform (Crowdin/Phrase), 1-3 target languages. Focus: consistent terminology, basic i18n. Coordination: with engineering on ICU message format, with content team on source string quality.

### Medium Team
Translation team (PM + linguists + reviewers), 5-10 languages, CI-embedded l10n pipeline. Focus: translation memory, automated QA, context-rich strings. Coordination: with product on string feature gating, with marketing on market-specific messaging.

### Enterprise
Full l10n program, 20+ languages, machine translation with human review, custom glossaries per locale. Focus: regional compliance, scalable content operations. Coordination: with legal on localized ToS/Privacy, with support on translated knowledge base.

### Transition Triggers
| From → To | Trigger |
|-----------|---------|
| Solo → Small | Second language beyond English; manual string management breaking |
| Small → Medium | Operating in 5+ languages; translation errors causing customer complaints |
| Medium → Enterprise | Regulatory need for certified translations; operating in 20+ locales |

## What Good Looks Like
<!-- STANDARD: 3min -->

**What good looks like:** A developer merges a PR with a new feature. Within 30 minutes, source strings are extracted, pushed to TMS, machine-translated for 12 locales, quality-checked automatically, and a PR opens with translated JSON files. The QA team tests the pseudolocalized build and finds zero layout bugs before any real translation costs are incurred. TM leverage is 78% — new strings reuse existing translations where possible. MT quality scores average 93/100 across all locales. Total human intervention: zero. Total time from code merge to translated build: under 2 hours.

## References
<!-- STANDARD: 3min -->

- Translation Memory Best Practices: references/tm-strategy.md
- MT Engine Comparison Matrix: references/mt-engine-comparison.md
- TMS Integration Guide (Lokalise/Phrase/Crowdin): assets/tms-integration-guide.md
- ICU MessageFormat Specification: https://unicode-org.github.io/icu/userguide/format_parse/messages/
- CLDR Plural Rules: https://cldr.unicode.org/index/cldr-spec/plural-rules
- i18next Documentation: https://www.i18next.com/
- Mozilla Fluent Project: https://projectfluent.org/
