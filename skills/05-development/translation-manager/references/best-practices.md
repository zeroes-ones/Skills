# Best Practices

<!-- STANDARD: 3min -->

1. **Pseudolocalize before translating.** Prefix with [^^^] and suffix with [vvv] to detect truncated strings. Double the string length using Unicode lookalikes (ä for a, é for e). This catches 80% of i18n bugs before you pay a single translation cost.
2. **Use glossary/termbase for brand and technical terms.** `npm install` should NEVER be translated. Brand names, API method names, and technical terms must be locked in the glossary with `translate: false`.
3. **TM leverage should be measured and reported.** Track: % of strings auto-translated from TM, % from MT, % requiring human post-editing. Goal: > 70% TM leverage across locales.
4. **Continuous localization, not batch.** Push new source strings on every merge to main. Pull translations daily. Batching creates a localization bottleneck where 2 weeks of translations block a release.
5. **Plural forms are not optional.** ICU MessageFormat supports all CLDR plural forms (zero, one, two, few, many, other). Arabic has 6 forms, Russian has 4, English has 2. Never assume singular/plural is enough.
6. **String context matters more than the string itself.** A TM entry for "Post" could mean blog post, mail post, or after something. Always include context metadata: file path, component name, and a developer comment.
7. **MT post-editing cost should drive engine selection.** If DeepL costs $25/1M chars but requires 10% post-editing, and Google costs $20/1M chars but requires 25% post-editing, DeepL is cheaper when post-editing costs $100/hour.
8. **Screen reader strings need separate handling.** `aria-label` strings are consumed by screen readers, not visually rendered. They have no length constraints but require high accuracy — prioritize TM+human review over raw MT for accessibility strings.
