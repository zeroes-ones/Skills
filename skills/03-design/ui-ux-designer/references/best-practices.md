# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- Name design tokens semantically from day one — renaming is exponentially expensive later.
- Every component variant should be expressed as prop combinations, not separate Figma frames.
- Design for the 99th percentile of content length, not the ideal — stress-test with long strings and edge content.
- Always specify the focused and disabled states before the hover state — they affect accessibility the most.
- Use `prefers-reduced-motion` as a design constraint; animations that can't gracefully degrade shouldn't exist.
- Version the design system — tag releases and maintain a migration guide for breaking changes.
- Involve an engineer in component design reviews before finalizing specs — feasibility checks prevent redesigns.
