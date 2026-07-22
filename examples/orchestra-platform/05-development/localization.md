# Internationalization (i18n)

## Framework and Setup

react-i18next 14.1 with i18next 23.11 for React/Next.js integration. Translation files stored as JSON under `public/locales/{lang}/` with namespace splitting: `common.json` (shared UI: buttons, labels, errors), `catalog.json`, `templates.json`, `plugins.json`, `admin.json`, `auth.json`. Configuration in `i18n.ts` enables language detection from the `Accept-Language` header (server), browser `navigator.language` (client), and a user preference stored in the database (highest priority). Fallback language: English (en-US).

## Launch Locales

English (en-US) and German (de-DE) at launch. Translation coverage: 347 unique keys across 6 namespaces. German translations completed by a professional LSP (Acme Translations GmbH) with a technical reviewer who understands platform engineering terminology. Both locales pass the ICU MessageFormat validation — plural forms (`one`, `other`) and interpolation tested for all 347 keys.

## RTL Readiness

Layout uses CSS logical properties throughout (`margin-inline-start` instead of `margin-left`, `padding-inline` instead of `padding-left/right`). Tailwind's `ltr:`, `rtl:` modifiers applied where direction-specific styling is unavoidable (e.g., stepper arrows). Arabic (`ar-SA`) planned for Q1 2027 based on 4 enterprise prospects in UAE and Saudi Arabia. The component library's RTL test suite passes with no layout breakages in the pseudolocalization environment.

## Pseudolocalization Testing

Pseudolocalization runs in CI on every PR using `i18next-pseudo`. All strings are transformed: prefixed with `[Ḁ]`, extended by 40% (stress-testing truncation), and accented. The Cypress component test suite runs against pseudolocalized builds. Current results: **0 truncation issues** detected across all 23 components. The QA pipeline enforces a maximum string length ratio of 1.5x against English for any container with `overflow: hidden`.

## Translator Workflow — Lokalise

Lokalise integration: GitHub Action on push to `main` uploads new/changed keys to Lokalise (auto-tagged with branch name). Translators work in Lokalise's web editor with screenshots and context descriptions for each key. Completed translations trigger a Lokalise webhook that opens a PR with updated JSON files. Review required by at least one internal reviewer per locale before merge.

## Date, Number, and Currency Formatting

All formatting uses the ECMAScript `Intl` API via `Intl.DateTimeFormat`, `Intl.NumberFormat`, and `Intl.RelativeTimeFormat`. No external formatting library dependencies. Date formats follow CLDR locale data: `DD.MM.YYYY` for German, `MM/DD/YYYY` for English US. Currency amounts (billing pages) use `Intl.NumberFormat` with the organization's configured currency (USD default, EUR for EU tenants).
