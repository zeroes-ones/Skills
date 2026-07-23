# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You design screens in Figma but can't explain how the layout resolves at 320px, 768px, 1440px, and 2560px without opening the file | You ship a component spec and 6 months later, the production implementation still exactly matches — no design drift, no engineer improvisation, no "we changed it because the spec didn't cover this edge case" | Engineers invite you to their sprint planning because your specs prevent rework — the team estimates 30% fewer "design clarification" spikes since you started writing specs their way |
| You hand off a Figma file and say "let me know if you have questions" | You hand off a package containing design tokens JSON, interaction specs, responsive behavior tables, accessibility annotations, and a recorded walkthrough — engineers implement 90%+ on first pass without follow-up questions | You define the design system that 50+ engineers use daily and you can trace a 40% reduction in design-to-code time to specific, measurable improvements you made in the handoff pipeline |
| You design a component's default state beautifully but discover the loading, error, and empty states during QA — or worse, in production | Every component spec you ship includes: default, hover, focus, active, disabled, loading, empty, error, and overflow states — with accessibility annotations and interaction timing for each | A junior designer you mentored for 3 months ships their first independent component spec and you have zero substantive feedback — your standards are internalized and reproducible by others |

**The Litmus Test:** Can you take a raw PRD for a feature you've never seen, produce a complete component spec (all states, responsive layout, accessibility annotations, interaction timing, design tokens) in under 4 hours, and have an engineer implement it without asking a single clarification question?
