# Production Checklist

<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|--------------------|----------|
| S1 | Brand architecture model documented (Branded House / House of Brands / Endorsed / Hybrid) | `grep -l "brand.architecture|branded.house|house.of.brands|endorsed|hybrid" *.md` | N/A — architectural decision requires human judgment |
| S2 | Logo system: primary, stacked, icon-only, wordmark, responsive variants all provided in SVG and PNG at 1x/2x/3x | `find . -name "logo*" \( -name "*.svg" -o -name "*.png" \) \| wc -l \| awk '{if ($1<8) exit 1}'` | Generate missing variants from primary using ImageMagick resize pipeline |
| S3 | Clear space rule defined (equal to icon height) and enforced with visual exclusion zone diagrams | `grep -c "clear.space|exclusion.zone|minimum.size" brand-guidelines.md` | N/A — requires visual diagram generation |
| S4 | Color palette with semantic tokens: primary, secondary, accent, neutral, semantic, dark mode — all exported as JSON | `cat design-tokens.json \| jq '.color \| keys' \| grep -c "primary|secondary|accent|neutral|semantic|dark"` | Generate missing semantic token groups from primitive palette using color mapping rules |
| S5 | All text-on-background color combinations validated for WCAG 2.2 AA (4.5:1 normal, 3:1 large text) | `npx axe-cli --rules color-contrast brand-swatches.html --exit` | Run `contrast-ratio` CLI on each token pair; generate lighter/darker accessible variant for failures |
| S6 | Typography hierarchy: display, h1–h4, body-lg/body/body-sm, caption, overline — with sizes, weights, line-heights, and usage rules | `grep -c "font-size|font-weight|line-height" design-tokens.json` | N/A — typographic scale requires design judgment |
| S7 | Icon set consistent in style, stroke weight (1.5px or 2px), corner radius (2px or 4px), and grid alignment (24×24 base) | `find icons/ -name "*.svg" -exec grep -L "viewBox=\"0 0 24 24\"" {} \; \| wc -l \| awk '{if ($1>0) exit 1}'` | Run SVGO with `--config viewbox-24.json` to standardize viewBox and stroke attributes |
| S8 | Imagery/illustration direction documented with style keywords, composition rules, and 3+ reference examples | `grep -c "illustration|imagery|photography|composition" brand-guidelines.md` | N/A — art direction requires creative brief |
| S9 | Motion tokens defined: durations (instant/fast/base/slow in ms), easings (default/enter/exit), reduced-motion mapping to 0ms | `cat design-tokens.json \| jq '.motion \| keys' \| grep -c "duration|easing|reduced-motion"` | Auto-generate reduced-motion token mappings (all durations → 0ms) in tokens output |
| S10 | Brand governance: review process, violation tiers (1–3), asset distribution portal, versioned guidelines with changelog | `grep -c "governance|violation.tier|review.process|changelog" brand-guidelines.md` | N/A — governance process requires organizational design |
