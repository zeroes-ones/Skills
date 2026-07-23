# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can build a component but can't explain why INP is 350ms on a real Moto G4 — you blame "React being slow" | You can load a production page in Chrome DevTools, run a Performance trace, identify the specific function causing the longest task, and fix it — INP drops to < 200ms | Your app ships with LCP < 1.5s, CLS < 0.05, and INP < 100ms on a $150 Android device on throttled 3G — and these numbers are verified by CrUX field data, not lab tests |
| You handle loading, success, and error states with if/else chains that miss empty and partial-data states | You model every async data dependency as a discriminated union (`{ status: 'loading' } \| { status: 'success', data: T } \| { status: 'error', error: E }`) and TypeScript enforces that all branches are handled | You define the async state pattern for your org and the teams that adopt it see a 60% reduction in "cannot read property of undefined" production errors in the first quarter |
| You add `aria-label` to a div and consider the component "accessible" — Lighthouse says 100 but a screen reader user can't navigate past your carousel | You can navigate your entire app with only a keyboard, never touching a mouse, and complete every critical flow — including modals, dropdowns, and drag-and-drop interactions | Your app passes an external WCAG 2.2 AA audit by a certified accessibility specialist on first submission with fewer than 3 findings — and you've trained 3 other developers to do the same |

**The Litmus Test:** Build a page with: a server-rendered product grid (50 items with images), a filter sidebar (6 facet groups with counts), and an "add to cart" that updates a header badge — all on Next.js App Router. It must achieve LCP < 1.5s, CLS = 0, and INP < 100ms on a Moto G4 with Slow 3G throttling. If any Core Web Vital is above the threshold, you're not L3 yet.
