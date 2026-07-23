# Sub-Skills

<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `brand-architecture` | Defining master brand, sub-brand, endorsed, or house-of-brands structure for new products or acquisitions | Branded House vs House of Brands vs Endorsed vs Hybrid — selection criteria and migration planning |
| `logo-system` | Designing primary, stacked, icon-only, wordmark, and responsive logo variants with clear space rules | Grid construction, minimum size thresholds, exclusion zones, monochrome/inverse variants, favicon to billboard |
| `color-palette` | Creating semantic color tokens: primary, secondary, accent, neutral, semantic, dark mode variants | HCT/HSLuv perceptual color spaces, WCAG 2.2 AA contrast validation (4.5:1 / 3:1), color blindness simulation |
| `typography-hierarchy` | Defining display, heading, body, caption, and overline type scales with usage rules | Font pairing, fluid type scales, line-height and letter-spacing tokens, performance (font loading strategy) |
| `iconography` | Establishing icon set: style (filled/outlined/duotone), grid (24×24), stroke weight, corner radius | Icon contribution guidelines, naming conventions, SVG optimization, accessibility labeling |
| `motion-design` | Creating motion tokens: duration scale, easing curves, animation principles, reduced-motion respect | `prefers-reduced-motion` query, entrance/exit/hover/attention animation categories, performance budget (no layout thrashing) |
| `brand-in-product` | Expressing brand within UI components: buttons, cards, navigation, empty states, loading states | Brand expression without compromising usability — color isn't the sole affordance, motion isn't distracting |
| `brand-governance` | Establishing review processes, asset distribution portal, violation tiers, and versioned guidelines | Self-serve brand portal, PR-based review for digital assets, violation severity (tier 1–3), changelog |


### War Story 1 — The Brand That Looked Like 5 Different Companies
**Symptom:** A startup grew from 10 to 80 people across 3 products. The marketing site used one blue, the app used another, the email templates used a third. Customer research revealed that 40% of users didn't realize the email and the app were from the same company.
**Root cause:** No centralized brand guidelines. Each team chose colors, fonts, and spacing independently. The brand "system" was a Figma file that nobody updated and nobody referenced. There was no brand governance — just chaos.
**Fix:** Created a single source of truth: design tokens in a JSON file consumed by both Figma (via Tokens Studio) and code (via Style Dictionary). Established a brand review process: any new asset must reference design tokens, not hardcoded values.
**Lesson:** Brand consistency doesn't happen by accident. If brand guidelines exist only in a PDF that nobody reads, they might as well not exist. Tokenize everything and embed brand rules into the tools teams already use.

### War Story 2 — The Design System That Collected Dust
**Symptom:** A company invested 6 months building a comprehensive design system with 50+ components. One year later, only 20% of the components were used in production. Engineers preferred building their own because the design system components were hard to customize and broke on edge cases.
**Root cause:** The design system was built by designers in Figma without engineering input. Components had no functional specs, no API documentation, and didn't cover edge states (loading, error, empty). Engineers found them unreliable and built alternatives.
**Fix:** Rebuilt the design system as an engineering-design partnership: designers own the visual spec, engineers own the implementation. Every component ships with a complete API reference, state coverage, and unit tests. Adoption is measured quarterly.
**Lesson:** A design system without engineering buy-in is a design portfolio, not a tool. Co-ownership with engineering ensures components are actually usable in production.

### War Story 3 — The Logo That Looked Great at 200px but Broke at 16px
**Symptom:** A brand team designed a beautiful logo with intricate line work and a 4-color gradient. It looked stunning on the website. But in the browser tab, the favicon was an illegible blur. In mobile navigation headers, the logo was unrecognizable. The app icon was a mess.
**Root cause:** The logo was designed at one scale (200px+ for desktop) with no responsive variants. No icon-only version was created. No minimum-size rules were defined. Engineers had to create their own simplified versions — each different.
**Fix:** Designed a complete logo system: primary (full logo, horizontal and stacked), icon-only (simplified mark at 32px), favicon (16px), and responsive variants per breakpoint. Defined minimum sizes and clear space rules for each variant.
**Lesson:** A logo that only works at one size isn't a logo system — it's a single asset. Design every logo variant from favicon to billboard before launch. Engineers will create their own (worse) versions if you don't.
