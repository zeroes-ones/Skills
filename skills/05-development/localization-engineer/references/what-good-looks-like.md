# What Good Looks Like — Full Quality Standard

Every user-facing string is externalized, translated, and renders correctly in every supported locale — pseudolocalization catches regressions in CI before translators ever see them. RTL layouts mirror LTR perfectly with CSS logical properties; no layout breaks, no truncated text, no orphaned directional assumptions. Dates, numbers, and currencies format correctly per locale using native `Intl` APIs, and plural and gender rules respect CLDR data. The translation pipeline pushes new strings to translators and pulls reviewed translations back as automated PRs within hours, not weeks. Native speakers review in-context, and quality gates block releases that fall below the translation completeness threshold.

> This is the full aspirational quality standard. The compressed version in SKILL.md is optimized for model token budgets.
