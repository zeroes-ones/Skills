---
name: translation-manager
description: >
  Use when setting up automated translation pipelines without human translators,
  optimizing machine translation quality, managing translation memory at scale,
  or automating localization quality gates in CI/CD. Handles MT engine selection,
  glossary and termbase management, pseudo-localization, string extraction, translation
  quality automation, and cost optimization across MT engines. Do NOT use for i18n
  architecture design, RTL layout implementation, or manual translation workflows
  requiring human linguists.
author: Sandeep Kumar Penchala
license: MIT
type: development
status: stable
version: 1.1.0
updated: 2026-07-23
tags:
- translation
- localization
- machine-translation
- tms
- glossary
- quality-assurance
- ci-cd
- cost-optimization
token_budget: 3500
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
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Orchestrate automated translation pipelines — configure machine translation engines, manage translation memory, automate quality checks, and run continuous localization without a human translation team.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*", "Lokalise\|Phrase\|Crowdin\|transifex\|POEditor\|Smartling")` OR `file_contains("*", "TMS\|TMX\|translation.*memory\|glossary\|termbase")` | This is your skill. Jump to **Core Workflow** — Phase 3 (TMS Integration). |
| A2 | `file_contains(".github/workflows/*", "lokalise\|phrase\|crowdin\|transifex")` OR `file_contains("package.json", "\"@lokalise\|phrase\|crowdin\"")` | Jump to **Core Workflow** — Phase 4 (CI/CD Pipeline). |
| A3 | `file_contains("*", "DeepL\|Google.*Translate\|Azure.*Translator\|ModernMT\|Amazon.*Translate")` AND `file_contains("*", "API.*key\|glossary\|formality")` | Jump to **Decision Trees** — MT Engine Selection. |
| A4 | `file_contains("*", "pseudo\|en-XA\|en-XB\|pseudolocaliz\|pseudo.*locale")` OR `file_contains("*", "pseudolocale\|mock.*translation\|test.*locale")` | Jump to **Best Practices** — Pseudolocalization. |
| A5 | `file_contains("*", "ICU\|MessageFormat\|plural\|selectordinal\|{count}\|{variable}")` | Jump to **Error Decoder** — ICU validation section. |
| A6 | `file_contains("*", "LQA\|quality.*score\|translation.*quality\|BLEU\|TER\|COMET")` OR `file_contains("*", "linguist.*review\|post.*edit\|review.*threshold")` | Jump to **Core Workflow** — Phase 4 (Quality Gates). |
| A7 | `file_contains("*", "cost.*optimiz\|budget\|spend\|MT.*cost\|pricing")` AND `file_contains("*", "TM.*leverage\|fuzzy.*match\|savings")` | Jump to **Decision Trees** — Cost Optimization. |
| A8 | `file_exists("*.tmx")` OR `file_contains("*", "tmx.*import\|tmx.*export\|translation.*memory.*file")` | Jump to **Core Workflow** — Phase 2 (Translation Memory). |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

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

These rules are non-negotiable constraints that detect localization mistakes before they are given. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE MT output committed without automated quality gate validation | Trigger: User proposes committing or deploying machine-translated strings without running placeholder integrity checks, ICU MessageFormat syntax validation, length constraint enforcement, and forbidden character detection | STOP. Respond: "MT output must pass automated quality gates before production. One broken placeholder (`{0}`, `%s`, `{{name}}`) crashes the entire UI for that locale — not just one string. Run checks for: placeholder count matching, ICU syntax validity, length within UI constraints, and forbidden characters. Show me the gate results before proceeding." |
| R2 | DETECT English-as-keys in string identifiers | Trigger: Generated or proposed i18n key uses English display text as the key value (e.g., `"Confirm Payment"`, `"Welcome back, {name}"`) instead of a structured semantic key path | STOP. Respond: "English-as-keys (`\"Confirm Payment\"`) couples the identifier to the current English copy. When marketing rewrites the English text, all 47 locales must re-translate — even though nothing changed in their language. Use semantic keys: `checkout.payment.confirm`. Keys are forever; string values are temporary." |
| R3 | REFUSE skipping pseudolocalization before translation spend | Trigger: User proposes purchasing translations, sending strings to translators, or running MT at scale without first executing pseudolocalized builds in CI | STOP. Respond: "Pseudolocalization catches UI bugs before you pay for translations. If the UI breaks with 2x-length strings, RTL rendering, or Unicode characters in pseudolocale, it will break with real translations. Run a pseudolocalized build in CI, fix every layout issue, then spend on translation." |
| R4 | DETECT missing translation memory strategy at pipeline setup | Trigger: User proposes setting up a translation pipeline without defining TM storage, fuzzy match threshold, pre-translation workflow, or post-editing TM update process | STOP. Respond: "Translation memory is your compounding asset — a 60% fuzzy match leveraged across 10,000 strings saves 6,000 translations. Define the TM strategy before any string leaves the pipeline: storage backend, fuzzy match threshold (≥60%), pre-translation fill from TM, and automatic TM update on post-editing. The ROI compounds with every locale added." |
| R5 | DETECT hardcoded user-facing strings in generated code | Trigger: Generated code contains user-visible text as plain string literals (`"Loading..."`, `"Save changes"`) instead of i18n translation function calls (`t('common.loading')`) | STOP. Respond: "Hardcoded strings found: [specific strings]. Every user-visible string must use the i18n translation function (`t()`). Hardcoded strings cannot be translated without code changes — each one is a bug report waiting to happen when the first non-English locale goes live. Replace with `t()` calls using semantic keys." |
| R6 | DETECT concatenated translatable fragments | Trigger: Generated code concatenates individually-translated fragments to form a sentence (e.g., `t('page') + ' ' + t('of') + ' ' + t('total')`) instead of a parameterized whole-string | STOP. Respond: "Concatenating translated fragments (`t('page') + ' ' + t('of')`) is untranslatable — word order, number agreement, and grammatical gender differ across languages. Use a parameterized whole-string: `t('pagination', { current, total })` producing 'Page 1 of 10' in English, '10ページ中1ページ目' in Japanese. Each locale controls its own sentence structure." |
| R7 | DETECT MT engine selected for unsupported or poor-performing language pair | Trigger: User chooses an MT engine (DeepL, Google Cloud Translation, Azure Translator) for a language pair where that engine has no support or documented poor quality | STOP. Respond: "This MT engine may not support or perform well for [language pair]. DeepL supports ~30 European languages. Google Cloud Translation covers 130+ languages but quality varies significantly by domain. Benchmark with your actual content — marketing copy, error messages, legal text — not generic test strings. Engine quality is language-pair and domain specific." |
| R8 | DETECT and WARN when translation keys are generated programmatically without a naming convention. | Trigger: translations without structured key convention or with auto-generated/auto-incrementing keys | WARN. Keys like `homepage_banner_title_v2_final_3` communicate nothing about context, break when the page is redesigned, and make it impossible to identify stale strings. After 2 years, 40% of your translation keys point to strings that no longer exist in the codebase — you're paying to translate dead text. Institute a structured key convention: `[feature].[component].[element]` — e.g., `checkout.payment.card_number_label`. The key communicates context even without seeing the UI. Run quarterly unused-key audits. Keys with no matching usage in 90 days → deprecated. |
| R9 | REFUSE to accept "the translation is the same length as English" as adequate layout testing. | Trigger: localization QA that only tests English UI with translated strings | STOP. German text is typically 30-35% longer than English. Arabic is right-to-left. Chinese characters are taller. Japanese doesn't use spaces between words. A UI that works perfectly with English strings breaks in 5 predictable ways when localized: text overflow, truncated labels, misaligned RTL layouts, broken concatenation, and missing fonts for CJK characters. Require: (1) pseudo-localization testing in CI (adds 30% length + Unicode accents to every string), (2) RTL layout screenshot comparison for Arabic/Hebrew, (3) CJK font rendering test on at least one device per platform. These catch 80% of i18n bugs before human QA sees a single translated string. |

## The Expert's Mindset

Masters of translation manager don't just build — they build **the right thing, at the right time, with the right trade-offs**. They think in systems, not tasks.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Shiny object syndrome** — chasing new tools without evaluating fit | Before adopting any new tool, write the "why this over the incumbent" justification |
| **Over-engineering** — building for hypothetical scale | Default to simplest solution; add complexity only when the current solution actually breaks |
| **Not-invented-here** — preferring to build rather than compose | Always evaluate 2 existing solutions before building custom |
| **Sunk cost fallacy** — sticking with a technology because you already invested in it | Re-evaluate tech choices every quarter; migration cost vs. staying cost |

### What Masters Know That Others Don't
- The **failure modes** of every component in their stack — not just the happy path
- When **not** to use their favorite tool (every tool has a misuse zone)
- That **data/model quality decays over time** — monitoring is not optional, it's foundational

### When to Break Your Own Rules
- **Move fast on reversible decisions.** Data format? Hard to change. Dashboard layout? Easy. Know the difference.
- **Skip the abstraction until the third use case.** Two is coincidence, three is a pattern.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single component/module | Implement a well-defined piece following established patterns |
| **L2** | Feature or service | Design and build a complete feature; make tech choices within team conventions |
| **L3** | System or product area | Define architecture for a product area; set team tech standards; mentor L1-L2 |
| **L4** | Multiple systems / platform | Define org-wide architecture patterns; make build-vs-buy decisions; influence industry practice |
| **L5** | Industry / ecosystem | Create new architectural patterns adopted across the industry; redefine what's possible |

**Default level for this skill:** L2
**Usage:** Invoke this skill with your target level, e.g., "as an L3 translation manager, design..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

<!-- STANDARD: 3min -->

- You need to set up a localization pipeline that doesn't depend on human translators
- You are evaluating or switching machine translation engines
- You need to build and maintain translation memory across multiple projects
- You want to automate translation quality validation in CI/CD
- You are optimizing translation costs across locales and MT providers
- You need to integrate a TMS API for automated pull/push workflows
- You are adding pseudo-localization to your QA pipeline
- You need to clean up stale translations and audit TM health
- You are setting up translation memory sharing across multiple teams or products
- You need to benchmark MT engine performance per language pair with domain-specific content
- You are designing a localization budget model with per-locale cost tracking
- You need to detect and purge dead translation keys that no longer map to active code
- You are evaluating whether to build vs. buy a localization automation platform

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

### Glossary & Termbase Strategy

```
Building your first glossary for translation?
├── Single product, 1-3 locales → Manual glossary in TMS (Lokalise/Phrase/Crowdin)
│   ├── Start with top 50 brand/product terms that MUST be consistent
│   ├── Review quarterly with in-market reviewers
│   └── Cost: 2-4 hours initial setup, 1 hour/month maintenance
├── Multi-product, 5-15 locales → Automated glossary with term extraction
│   ├── Extract candidate terms from codebase: grep for capitalized proper nouns, repeated phrases
│   ├── Classify: brand terms (translate: false), product features (approved translation), UI verbs (style guide)
│   ├── Enforce at TMS level: flag or hard-block deviations from approved terms
│   └── Run automated termbase coverage audits quarterly — target > 95% term consistency
├── Enterprise, 20+ locales with regulatory content → Termbase with legal validation
│   ├── Legal-reviewed glossary for compliance terms (privacy policy, terms of service, disclaimers)
│   ├── Per-locale legal review of all glossary entries touching liability, rights, or obligations
│   ├── Version-controlled glossary with change log and approval workflow
│   └── Automated scan for glossary violations in translation PRs — block merge on legal term deviations
└── Starting from zero (no existing glossary) → Minimum viable glossary
    ├── Step 1: Extract top 30 terms from your most-trafficked 5 pages
    ├── Step 2: Get one in-market reviewer to approve translations for top 3 locales
    ├── Step 3: Enforce in CI — flag any translation that diverges from glossary
    └── Step 4: Expand by 10 terms per sprint until all product surfaces are covered

```

### Machine Translation Quality Strategy

```
How should you approach MT for your language portfolio?
├── Tier 1 languages (ES, FR, DE, PT, IT, NL) → MT + light post-editing
│   ├── Neural MT (DeepL, ModernMT) produces publishable quality 80%+ of the time
│   ├── Post-editing: review MT output, fix terminology and tone (not full retranslation)
│   ├── Cost: 30-50% of human translation. Turnaround: 1-2 days for 10K words.
│   └── QA: BLEU score > 40, human sample review of 10% of strings
├── Tier 2 languages (JA, ZH, KO, RU, TH, AR) → MT + full human review
│   ├── MT quality is 60-70% for these pairs — post-editing is closer to retranslation
│   ├── Human review: linguist reviews every string against source and glossary
│   ├── Cost: 60-80% of human translation. Turnaround: 3-5 days for 10K words.
│   └── QA: BLEU > 30, human review of 100% of strings, native speaker QA on UI screenshots
├── Tier 3 languages (FI, HU, VI, TR, PL, CS) → Human-first with MT assistance
│   ├── MT provides a draft, but morphology complexity means human retranslation is necessary
│   ├── Human translator starts from source (not MT output), uses MT as reference only
│   ├── Cost: 90-100% of human translation. Turnaround: 5-7 days for 10K words.
│   └── QA: native speaker review of 100%, in-context screenshot review for top 20% of strings by visibility
└── Enterprise decision: build MT quality dashboard
    ├── Track per-language-pair: BLEU, TER, human adequacy score (1-5), post-editing time per word
    ├── Use data to move languages between tiers as MT improves
    ├── Re-evaluate quarterly: MT quality is improving ~5-10%/year, language tiers are not static
    └── Budget optimization: Tier 1 at scale (50K+ words/year) can fund Tier 3 quality improvements
```

### Translation Memory Maintenance & Cleanup

```
TM health degrading — where to start?
├── High duplicate rate (> 15% of TM entries are duplicates) → Deduplication run
│   ├── Identify exact duplicates (same source, same target, same locale) → keep newest
│   ├── Identify near-duplicates (same source, slightly different targets) → flag for review
│   ├── Automated dedup with `tmx-cleaner` or TMS built-in tools
│   └── Schedule: monthly for active TMs, quarterly for stable ones
├── Stale entries > 2 years without a match → Archive
│   ├── Entries unused for 24+ months likely correspond to removed/changed features
│   ├── Archive (don't delete) — move to `tm-archive` database
│   ├── Before archiving, cross-reference against active i18n keys in codebase
│   └── Stale TM bloats match queries and increases API costs — trim quarterly
├── TM leverage dropping quarter-over-quarter → Key migration gap
│   ├── Compare current i18n keys against TM keys — identify renamed keys
│   ├── Build a key migration map: old_key → new_key
│   ├── Apply migration to TM entries so translations survive refactors
│   └── Root cause: developers renaming keys without updating TM — add CI check
├── Inconsistent quality scores across TM entries → Quality tier labeling
│   ├── Tag TM entries with quality tier: `approved` (human-reviewed), `mt-unreviewed`, `legacy` (pre-TM era)
│   ├── Prefer `approved` entries for auto-population; `mt-unreviewed` for suggestions only
│   ├── Run periodic quality audit: sample 5% of `approved` entries for accuracy
│   └── Downgrade or flag entries with low BLEU scores against fresh human translations
└── No TM for a new product → Bootstrap from scratch
    ├── Step 1: Extract all existing translations from codebase locale files
    ├── Step 2: Normalize to TMX format, tag with source context (file + key path)
    ├── Step 3: Run MT pre-translation for initial fill (tag as `mt-unreviewed`)
    ├── Step 4: First 1,000 post-edited strings → promote to `approved`
    └── Goal: reach 60%+ TM leverage within 3 months of pipeline launch
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
| Dead translation keys detected (> 10% of TM entries reference keys not in codebase) | Run dead-key audit: grep all TM source keys against current codebase; archive unmatched entries; update TM | You're paying to store and serve translations for features that don't exist — dead keys bloat API payloads and slow match queries |
| Single MT engine used for all content types (marketing, legal, UI, help docs) | Classify content by domain; benchmark engine quality per domain; route accordingly | Marketing copy needs brand voice (DeepL); legal text needs precision (custom model); help docs need low cost (Google) — one engine can't optimize all three |
| TMX file size exceeds 100MB | Partition TM by project/domain; switch to database-backed TM storage (not flat TMX files); implement incremental sync instead of full export/import | Giant TMX files corrupt silently, timeout during import, and make every pipeline run a bottleneck — partition before it breaks |
| No per-locale cost tracking — budget is a single line item | Implement cost tagging: tag every MT API call with locale, content type, and project; build per-locale cost dashboard | You can't optimize what you don't measure — per-locale costs typically vary 5-10x, and the expensive locales aren't necessarily the high-ROI ones |
| Pseudolocalization passes but real locale screenshots show layout breaks | Add locale-specific length ratio checks: German (1.35x English), Arabic (1.1x + RTL), Japanese (0.8x + vertical height); requre screenshot diffs for top 3 non-English locales | Pseudo-loc shows the worst case but not every case — German word compounding creates overflow patterns that generic pseudo-loc padding doesn't catch |

## What Good Looks Like

### BEFORE (Novice) → AFTER (World-Class)

**Pipeline Maturity:**
- **BEFORE:** Developer manually copies English JSON to `fr.json`, Google Translates each string one at a time, commits without quality checks. French launch reveals: 4 broken placeholders (crashed UI), 2 buttons that overflow their containers (40% text expansion unhandled), and "Save" translated differently on 3 different pages.
- **AFTER:** Developer merges PR with English strings. CI extracts source strings, pushes to TMS, machine-translates for 12 locales with glossary enforcement, runs automated quality gates (placeholder integrity, ICU syntax, length constraints, forbidden characters), and opens a PR with translated JSON files — all within 30 minutes. Pseudolocalization CI gate caught the layout issues before translators touched a single string. TM leverage at 78%. Total human intervention: zero.

**Glossary Discipline:**
- **BEFORE:** "Dashboard" rendered as "tableau de bord" (web), "panneau de contrôle" (mobile), "tableau de commande" (marketing). Users can't search for the feature across platforms. Support documentation references terms that don't match any product label.
- **AFTER:** Centralized glossary in TMS with `translate: false` for brand names, approved translations for all product terms, and automated enforcement. Termbase coverage audit shows 97% consistency across all 15 locales. Support teams reference the same glossary — user-facing terms match across every surface.

**Quality Gates:**
- **BEFORE:** Translation quality assessed by "spot-checking 3 random strings" before release. QA passes because the strings are linguistically correct — but nobody tested them IN the UI. German buttons overflow. Arabic form validation errors render before field labels.
- **AFTER:** Automated quality gates in CI: placeholder count matching (30% weight), ICU syntax validity (25%), length compliance per UI element (25%), glossary/termbase consistency (20%). Gate threshold: score ≥ 90 to pass, 80-89 warns, &lt; 80 blocks. Functional QA signs off in 2 non-English locales before release. Pseudolocalization runs in CI on every PR.

**Continuous Localization Pipeline:**
- **BEFORE:** Translations are a release bottleneck. Developers finish features, then wait 2 weeks for human translators. The "translation freeze" blocks the entire release train. Emergency hotfixes can't include translations because the pipeline takes days. Marketing launches in English-only while translated pages lag by 3-4 weeks — international users get a second-class experience.
- **AFTER:** Git-based continuous localization pipeline: merge to main triggers source string extraction → push to TMS → MT auto-translate with glossary enforcement → automated quality gates → PR with translated locale files opened automatically. Pipeline latency is under 2 hours from code merge to translated strings ready for review. Developers never wait on translations. Hotfixes include translations because the pipeline is fast enough. All 12 locales ship simultaneously with English — no more "English first, translations later" releases.

**Cost Awareness:**
- **BEFORE:** Translation budget is a single line item — "Localization: $15K/month." Nobody knows which locales cost the most, which content types drive spending, or what the ROI per locale is. The budget gets cut by 20% during belt-tightening and the team freezes 3 locales arbitrarily. MT engines are chosen by developer preference, not cost-quality trade-off analysis.
- **AFTER:** Per-locale cost dashboard: dollars per word by engine, post-editing cost by language tier, TM leverage savings (dollars saved by fuzzy matches), and cost per 1,000 active users per locale. Glossaries reduced re-translation costs by 22% through term consistency. MT routing saves $8K/month by sending help docs to a cheaper engine. Budget conversations start with data: "We spend $0.12/user in Germany and $0.08/user in Spain — both are below the $0.20/user threshold. Here's what cutting Japanese would actually save vs. cost in user churn."

**What good looks like:** A developer merges a PR with a new feature. Within 30 minutes, source strings are extracted, pushed to TMS, machine-translated for 12 locales, quality-checked automatically, and a PR opens with translated JSON files. The QA team tests the pseudolocalized build and finds zero layout bugs before any real translation costs are incurred. TM leverage is 78% — new strings reuse existing translations where possible. MT quality scores average 93/100 across all locales. Total human intervention: zero. Total time from code merge to translated build: under 2 hours.

## Deliberate Practice

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Set up a localization pipeline from scratch for a sample React app: i18next extraction, TMS connection (Lokalise free tier), MT auto-translate for 3 locales, quality gates, CI integration. Time yourself — target under 4 hours end-to-end. | Monthly |
| **Competent** | Take a production app's locale files and run a full quality audit: placeholder integrity, ICU syntax, length constraints, glossary consistency, forbidden characters. Find and fix every violation. Compare your findings against the existing QA process — what did it miss? | Quarterly |
| **Expert** | Design a multi-engine MT routing system: classify content type (marketing/legal/UI/help-docs), route to optimal MT engine per language pair per content type, measure BLEU/COMET scores per route, optimize for cost vs quality trade-off. Build a cost model showing savings vs single-engine approach. | Quarterly |
| **Master** | Build a translation quality monitoring dashboard: per-locale quality scores over time, MT engine performance trends, TM leverage rates, cost-per-locale trends, pipeline latency metrics. Set up automated alerts for quality regressions and cost anomalies. Document the ROI of each quality gate in dollars saved. | Annually |

**The One Highest-Leverage Activity:** Every quarter, run a pseudolocalized build of your entire product and walk through every screen. Count the layout breaks. If the number isn't decreasing quarter-over-quarter, your localization pipeline has a feedback gap.

## Gotchas

- **Machine translation without human review for legal content.** Running contracts, terms of service, privacy policies, or regulatory documents through MT engines (DeepL, Google Translate) without qualified human post-editing. A single mistranslated clause — "shall" becoming "may," "indemnify" becoming "hold harmless" with different legal meaning — creates binding obligations the company never intended. In regulated industries, this triggers compliance violations, lawsuits, and contract nullification. **Total cost: $50,000-$500,000 in liability from mistranslated legal documents, regulatory fines, and contract disputes.** Fix: Legal and compliance content must go through certified human translation with legal-domain expertise; never MT-only for binding documents; maintain a legal glossary with approved translations for all domain terms.
- **Translation memory not leveraged.** Every new project starts from scratch: translators re-translate "Submit," "Cancel," "Sign up" across 12 languages for every feature release. At $0.15-$0.25 per word, re-translating 50,000 words of repetitive UI strings across 12 locales costs $90,000-$150,000 annually that a properly maintained TM would eliminate. The TM exists but wasn't shared across teams, wasn't updated, or wasn't connected to the translation pipeline. **Total cost: $30,000-$150,000 per year in duplicate translation costs.** Fix: Centralize TM in your TMS (Lokalise, Phrase, Crowdin); enforce TM lookup as the first step before any new translation; set up automated TM maintenance (deduplication, stale entry pruning); share TM across all product teams.
- **Translation memory (TM) fuzzy match thresholds** — setting `fuzzy_match_threshold: 75%` captures "Hello World" → "Hello World!" (1 char difference = ~90% match) but also "Delete account" → "Delete comment" (same fuzzy score, completely different meaning). High fuzzy thresholds produce comically wrong translations that QA misses.
- **Machine translation post-editing distance (HTR)** — if post-editors change < 10% of MT output, you're overpaying for MT+human vs human-only. If they change > 40%, the MT engine is wrong for your domain and training a custom model is cheaper than paying for heavy post-editing.
- **ICU MessageFormat plural rules**: `{count, plural, one {# item} other {# items}}` — the `=0` case is NOT covered by `zero`. `zero` is for languages with a zero CLDR form (Arabic, Latvian). English uses `other` for zero. Missing `=0 {No items}` means English speakers see "0 items" instead of "No items."
- **Pseudolocalization** with `en-XA` or `en-XB` BCP47 tags — if your UI doesn't handle 30% text expansion (English → German) or RTL layout, pseudo-localization reveals it before translators waste time. But pseudo must run in CI, not locally. One developer running pseudo-loc finds only their bugs, not integration bugs.
- **String extraction from concatenation**: `t('views.') + viewName + t('.title')` — this produces 3 separate translation calls for ONE logical string. The concatenated result can't be in TM, can't benefit from context, and produces grammatically broken sentences in languages with different word order (Japanese, Korean, Turkish).
- **No glossary or termbase enforcement across projects.** Translators render "dashboard" as "tableau de bord" in the web app, "panneau de contrôle" in the mobile app, and "tableau de commande" in marketing — all correct French but inconsistent. Users searching for "tableau de bord" can't find the feature on mobile, brand terminology fractures across surfaces, and support documentation references terms that don't match any actual product label. **Total cost: $10,000-$30,000 per year in terminology inconsistency remediation, customer confusion driving support escalations, and diminished trust in localization quality across international markets.** Fix: Build and maintain a centralized glossary/termbase with approved translations for every product and brand term; enforce glossary compliance at the TMS level — flag or hard-block translations that deviate from approved terms; run automated termbase coverage audits quarterly and before each release.
- **Translation quality measured only by linguistic review without functional UI testing.** LQA scores rate translations as linguistically correct, but nobody tests whether the translated strings actually render and function in the application UI. A German button label grows 40% longer and breaks a flex layout constraint. An Arabic translation reverses the order of form validation messages — the error appears before the field label. QA passes (strings are correct), but the localized product is broken. **Total cost: $15,000-$50,000 in post-localization UI bug fixes per release, missed international launch dates, and hotfix deployments for translation-induced functional breakage.** Fix: Integrate localization testing into the QA pipeline — run automated screenshot comparisons in every target locale; require functional QA sign-off in at least 2 non-English locales before release; use pseudo-localization as a CI gate to catch layout issues before translators ever touch the strings.
- **Using different MT engines per project with no consistency management.** The mobile team uses DeepL for German, the web team uses Google Cloud Translation for German, and marketing sends German copy to a human translator. The same English product term gets three different German translations across platforms because each engine has different training data, style biases, and terminology defaults. The product voice becomes fragmented — users notice and trust erodes. **Total cost: $5,000-$20,000 per year in inconsistency fixes, brand voice dilution across platforms, and user trust erosion from seeing different translations for identical features.** Fix: Standardize on one MT engine per language pair across the organization; when multiple engines are unavoidable, run all output through the shared glossary/termbase for post-processing consistency; maintain a per-language style guide with approved terminology for every product surface; feed MT post-editing corrections back into the engine's custom glossary to improve future output.
- **Concatenating translated strings to form sentences.** "You have" + itemCount + "items" works in English but breaks in languages with grammatical gender, dual/plural forms, and different word orders. In Arabic: "لديك 3 عناصر" (you have 3 items) — but the word for "items" changes form. In Russian: different plural forms for 1, 2-4, and 5+. "You have 21 items" is singular in Russian grammar. String concatenation produces grammatically-incorrect output in 70%+ of non-English languages. **Total cost: $15K-$50K per incident — emergency retranslation, hotfix release, brand damage in localized markets.** Fix: Always use ICU MessageFormat with plural rules: `{count, plural, =0 {You have no items} =1 {You have 1 item} other {You have # items}}`. Never concatenate translated fragments.
- **Translating UI strings before the design is finalized.** Every design change after translation starts invalidates translations. A button label expands from "Save" to "Save Changes" — now 32 languages need retranslation. A new error state adds 3 strings. The backlog of "minor copy changes" accumulates across sprints until the translation debt is larger than the initial translation investment. **Total cost: $8K-$20K per release for re-translation of changed strings, plus $5K-$15K in delayed release costs.** Fix: Freeze UI copy 2 weeks before translation starts. Any changes post-freeze go into a "next release" translation batch. Use a string freeze checklist signed by PM, design, and content. Tag strings that can still change vs locked strings in your TMS.
- **Assuming machine translation quality is consistent across language pairs.** MT quality varies dramatically by language pair. English→Spanish (DeepL): near-human quality. English→Korean (Google Translate): requires significant post-editing. English→Finnish (any MT): high error rate due to complex morphology. Using the same MT engine and post-editing budget for all languages wastes money on easy pairs and underfunds hard ones. **Total cost: $10K-$30K/year in either overpaying for unnecessary human review on easy pairs OR shipping poor quality in hard pairs (resulting in user churn in those markets).** Fix: Segment languages into MT quality tiers: Tier 1 (ES, FR, DE, PT — light post-editing), Tier 2 (JA, ZH, KO, RU — full human review required), Tier 3 (FI, HU, AR, VI — MT + mandatory native-speaking reviewer). Budget post-editing proportionally.

## Verification

- [ ] Run `i18next-parser` or equivalent to extract new strings — zero untranslated keys
- [ ] Run pseudo-localization in CI: verify no layout breaks from 30% text expansion
- [ ] Check TM leveraging: fuzzy match rate for new strings against TM > 60%
- [ ] Validate ICU syntax in all resource files with `icu-validator` — zero parse errors
- [ ] Run MT quality threshold: BLEU score for MT output > 30 before skipping human review (or domain-specific threshold)
- [ ] Verify `=0`, `=1`, and `other` plural cases render correctly for English + top 3 locales

## References

Detailed reference material loaded on demand:

- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Negative Constraints**: See [negative-constraints.md](references/negative-constraints.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)

