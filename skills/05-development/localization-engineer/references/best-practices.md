# Best Practices

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
