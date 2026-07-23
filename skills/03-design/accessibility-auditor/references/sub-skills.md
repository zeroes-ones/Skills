# Sub-Skills

<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `wcag-conformance` | Selecting WCAG 2.2 conformance target (A, AA, AAA) based on legal obligations and user needs | 87 success criteria across 13 guidelines, 4 principles (Perceivable, Operable, Understandable, Robust) |
| `automated-a11y-testing` | Setting up axe-core, Lighthouse, pa11y in CI with quality gates | ~30% of WCAG criteria machine-testable; integrate in PR pipeline, fail on violations |
| `screen-reader-testing` | Manual testing with VoiceOver (macOS/iOS), NVDA (Windows), JAWS (Windows), TalkBack (Android) | ~70% of WCAG criteria require human judgment; test reading order, landmark navigation, live regions |
| `keyboard-audit` | Verifying all interactive elements are keyboard-operable with visible focus indicators | Tab order, focus trapping in modals, skip links, no keyboard traps, focus management on SPA navigation |
| `semantic-html-audit` | Auditing landmark regions, heading hierarchy, form labeling, table structure | `<main>`, `<nav>`, `<aside>`, heading levels without skips, `<label>` with `for`, `<th scope>`, ARIA fallback |
| `form-accessibility` | Labels, error messages, instructions, `aria-describedby`, `aria-invalid`, required fields | Error announcement on submit, error recovery path, sufficient color contrast for error state indicators |
| `time-based-media` | Captions, transcripts, audio descriptions for video and audio content | WCAG 1.2.x criteria; captions (1.2.2 AA), audio description (1.2.5 AA), sign language (1.2.6 AAA) |
| `legal-compliance` | ADA Title III, Section 508, EN 301 549, AODA — which applies and what's the exposure | Jurisdiction analysis, demand letter response, VPAT/ACR preparation, structured negotiation strategy |


### War Story 1 — The Lawsuit That Started With a Missing Alt Tag
**Symptom:** An e-commerce company received a demand letter from a plaintiffs' firm alleging their entire checkout flow was inaccessible to blind users. The lawsuit named 47 specific WCAG violations. Settlement cost: $85K plus court-ordered remediation.
**Root cause:** The team had run automated Lighthouse audits that scored 92 — they thought they were fine. But automated tools miss ~70% of accessibility issues. Missing alt text on 200 product images, no focus indicators on checkout buttons, and a modal that trapped keyboard users without escape — none caught by automation.
**Fix:** Implemented a three-layer accessibility process: (1) automated audits in CI on every PR (axe-core, minimum zero violations), (2) manual keyboard-only testing by QA on every release, (3) quarterly screen reader audits with VoiceOver and NVDA.
**Lesson:** An automated accessibility score above 90 does not mean your product is accessible. Manual testing catches the issues that matter most to real users — and that plaintiffs' lawyers look for first.

### War Story 2 — The Modal Nobody Could Close
**Symptom:** A marketing site launched a newsletter signup modal that appeared on first visit. Keyboard users could not close it — the close button was reachable only by mouse. Users on screen readers were trapped in the modal with no way out. Over 400 support tickets in 72 hours.
**Root cause:** The modal was built with a `<div>` instead of a proper dialog role, the close button was a `<span>` with an onclick handler (no keyboard accessibility), and focus was not trapped or restored. No accessibility review was done before launch.
**Fix:** Rebuilt the modal using the ARIA dialog pattern with focus trapping, Escape key handler, and focus restoration on close. Added modal accessibility to the design system's mandatory checklist.
**Lesson:** Modals are the most accessibility-failed pattern on the web. Every modal must be tested with keyboard-only navigation before it ships. A $50 fix pre-launch costs $5,000 in support tickets post-launch.

### War Story 3 — The Color Palette That Looked Great to the Designer
**Symptom:** A fintech app launched with a beautiful, on-brand color palette. Within a week, users with low vision flooded customer support: "I can't read the buttons" and "The text blends into the background." The color contrast ratios were 2.8:1 and 3.2:1 — well below WCAG AA minimum of 4.5:1.
**Root cause:** The designer chose colors based on brand aesthetics and visual appeal, not contrast ratios. No color combinations were validated against WCAG standards before handoff. The Figma file was handed off with no contrast annotations.
**Fix:** Mandated color contrast validation at the design stage: no Figma frame leaves the design phase without all text/background combinations passing WCAG 2.2 AA. The brand palette was adjusted to include accessible variants while preserving brand identity.
**Lesson:** Accessibility IS brand. An inaccessible color palette isn't a compliance problem — it's a broken brand promise. Validate contrast before handing off, not after users complain.
