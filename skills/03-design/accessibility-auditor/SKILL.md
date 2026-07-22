---
name: accessibility-auditor
description: WCAG 2.2 compliance auditing across automated and manual testing, screen reader workflows, semantic HTML validation, focus management, accessible forms, legal landscape (ADA, Section 508, EN
  301 549), and remediation prioritization.
author: Sandeep Kumar Penchala
type: design
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- accessibility-auditor
chain:
  consumes_from:
  - accessibility-testing
  - frontend-developer
  - ui-ux-designer
  feeds_into:
  - accessibility-testing
  - frontend-developer
  - legal-advisor
  - qa-engineer
token_budget: 4000
output:
  type: code
  path_hint: ./
---
# Accessibility Auditor

Master the art and science of digital accessibility auditing — from automated scanning to manual assistive-technology testing. This skill covers WCAG 2.2 at all conformance levels, automated testing tools (axe-core, pa11y, Lighthouse), manual testing scripts for screen readers (VoiceOver, NVDA, JAWS), semantic HTML audits, focus management, accessible forms, time-based media, legal compliance frameworks, and remediation prioritization strategies.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── WCAG compliance audit (A, AA, or AAA) → Start at "Decision Trees > Conformance Level Selection"
├── Screen reader testing (VoiceOver, NVDA, JAWS) → Go to "references/accessibility-auditor.md"
├── Semantic HTML review (landmarks, headings, forms) → Jump to "references/accessibility-auditor.md"
├── Legal compliance check (ADA, Section 508, EN 301 549) → Go to "references/accessibility-auditor.md"
├── Remediation planning (prioritize fixes by impact) → Jump to "references/accessibility-auditor.md"
├── Need component specifications or design tokens? → `ui-ux-designer`
├── Need accessible implementation with ARIA patterns? → `frontend-developer`
├── Need legal compliance review (ADA, Section 508)? → `legal-advisor`
├── Need brand color contrast or typography validation? → `brand-guidelines`
└── Don't know where to start? → Run automated audit first, then manual testing
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never claim "fully accessible" — accessibility is a spectrum.** Every product has gaps. Report what was tested, at what level, and what remains untested. Do: "This audit covers 47 of 50 WCAG 2.2 AA criteria; 3 criteria require manual review." Don't: "This site is fully accessible."
- **WCAG level must be specified (A/AA/AAA).** Never say "WCAG compliant" without the level. Do: "Component passes WCAG 2.2 AA." Don't: "Component is WCAG compliant."
- **Automated tools miss ~30% of issues.** Every audit must include manual testing steps for keyboard navigation, screen reader flow, and focus management. Do: "axe-core found 12 issues; manual testing surfaced 4 additional keyboard traps." Don't: "Lighthouse score is 100, so we're good."
- **Always report severity with user impact.** Frame every issue as: what the user experiences, which WCAG criterion it violates, and how to reproduce. Do: "A screen reader user cannot submit the form because the submit button has no accessible name (WCAG 4.1.2)." Don't: "Missing aria-label on button."
- **Admit what you don't know.** If you haven't tested with a specific assistive technology or browser/screen-reader combination, say so and tell the user to test with that combination before claiming coverage.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Auditing a web application for WCAG 2.2 compliance (A, AA, or AAA)
- Setting up automated accessibility testing in CI/CD pipelines
- Performing manual screen reader testing with VoiceOver, NVDA, or JAWS
- Auditing semantic HTML structure, landmark regions, and heading hierarchy
- Testing keyboard navigation, focus management, and focus trapping
- Auditing form accessibility: labels, error handling, instructions
- Preparing an Accessibility Conformance Report (ACR) or VPAT
- Assessing legal risk under ADA Title III, Section 508, or EN 301 549
- Prioritizing accessibility remediation by user impact severity

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Conformance Level Selection
```
                     ┌──────────────────────────────┐
                     │ START: WCAG target level?    │
                     └─────────────┬────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Is this a government, healthcare, or    │
              │ education product?                      │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ WCAG 2.2 AA      │    │ Is this a public-    │
        │ minimum. Section │    │ facing consumer      │
        │ 508 / EN 301 549 │    │ product with >10K   │
        │ likely apply.    │    │ users?               │
        └──────────────────┘    └──┬───────────────┬───┘
                                   │ YES           │ NO
                                   ▼               ▼
                            ┌────────────┐  ┌──────────────┐
                            │ WCAG 2.2 AA│  │ WCAG 2.2 A   │
                            │ for legal  │  │ minimum.     │
                            │ risk       │  │ Internal tool│
                            │ mitigation │  │ or MVP.      │
                            └────────────┘  └──────────────┘
```
**When AA required:** Government, healthcare, education, financial services. Public-facing with > 10K users. Legal department advises or ADA litigation risk exists.  
**When A acceptable:** Internal admin tool used by < 100 known employees. Early-stage MVP with accessibility roadmap. No legal obligation (confirmed by counsel).

### Testing Method Selection
```
                     ┌──────────────────────────────┐
                     │ START: Automated or manual?  │
                     └─────────────┬────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Checking color contrast, heading order, │
              │ ARIA syntax, or alt text presence?      │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ Automated:       │    │ Can a screen reader  │
        │ axe-core,        │    │ user complete the    │
        │ Lighthouse,      │    │ core task?           │
        │ pa11y CI.        │    └──┬───────────────┬───┘
        │ ~30% of issues.  │       │ YES           │ NO
        └──────────────────┘       ▼               ▼
                            ┌────────────┐  ┌──────────────┐
                            │ Manual:    │  │ Manual +     │
                            │ Screen     │  │ Keyboard +   │
                            │ reader test│  │ Focus order  │
                            │ (VoiceOver,│  │ test. Cannot │
                            │ NVDA, JAWS)│  │ automate.    │
                            └────────────┘  └──────────────┘
```
**When automated suffices:** ~30% of WCAG criteria are machine-testable. Color contrast, heading structure, ARIA validity, alt text presence. Run in CI on every PR.  
**When manual required:** ~70% of WCAG criteria need human judgment. Keyboard operability, focus management, meaningful alt text (not just presence), modal focus trapping.

### Remediation Priority
```
                     ┌──────────────────────────────┐
                     │ START: Fix priority?         │
                     └─────────────┬────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Does this issue completely block a user │
              │ from completing a core task?            │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ P0: Critical.    │    │ Affects > 5% of users│
        │ Fix this sprint. │    │ or causes significant│
        │ E.g., login      │    │ friction?            │
        │ button not       │    └──┬───────────────┬───┘
        │ keyboard-        │       │ YES           │ NO
        │ accessible.      │       ▼               ▼
        └──────────────────┘ ┌────────────┐  ┌───────────┐
                             │ P1: Fix    │  │ P2: Fix   │
                             │ within 4   │  │ within 3  │
                             │ weeks.     │  │ months.   │
                             └────────────┘  └───────────┘
```
**When P0 (Critical):** Task-blocking for any disability group. Login, checkout, core navigation not operable. Legal exposure from ADA lawsuit precedent.  
**When P2:** Enhancement-level issue. Workaround exists. Affects WCAG AAA criteria only. Low-traffic page with no critical function.

### Legal Risk Assessment
```
                     ┌──────────────────────────────┐
                     │ START: Legal exposure?       │
                     └─────────────┬────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Product serves US consumers and meets   │
              │ ADA "place of public accommodation"?   │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ HIGH risk. ADA   │    │ EU public sector or  │
        │ Title III applies.│    │ government contract? │
        │ WCAG 2.2 AA is   │    └──┬───────────────┬───┘
        │ de facto standard│       │ YES           │ NO
        │ per DOJ guidance. │      ▼               ▼
        └──────────────────┘ ┌────────────┐  ┌───────────┐
                             │ EN 301 549 │  │ LOW risk. │
                             │ applies.   │  │ Monitor   │
                             │ AA required│  │ regulatory│
                             └────────────┘  │ changes.  │
                                             └───────────┘
```
**When HIGH risk:** US consumer-facing website/app. > 10K monthly visitors. E-commerce, education, healthcare, employment, or financial services.  
**When LOW risk:** Internal tool with < 100 known users. B2B SaaS with enterprise contracts (accessibility negotiated per deal). No US nexus.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): WCAG 2.2 Conformance Target Selection

Choose your target based on audience, legal obligations, and product maturity:

| Level | Description | Best For | Examples of Requirements |
|-------|-------------|----------|--------------------------|
| **A (Minimum)** | Bare-minimum accessibility. Without this, some users **cannot** use the product. | Internal tools, MVPs with accessibility roadmap, low-risk products | Keyboard access (2.1.1), non-text alternatives (1.1.1), no keyboard traps (2.1.2), labels/instructions (3.3.2) |
| **AA (Standard)** | The legal and industry standard. Without this, some users **struggle significantly**. | All public-facing products, e-commerce, SaaS, government-adjacent | Contrast 4.5:1 (1.4.3), reflow to 320px (1.4.10), focus visible (2.4.7), consistent navigation (3.2.3), error suggestions (3.3.3) |
| **AAA (Enhanced)** | Gold standard. Achievable only for specific content types. | Dedicated accessibility products, government portals, medical systems | Contrast 7:1 (1.4.6), sign language (1.2.6), no time limits (2.2.3), pronunciation (3.1.6), context-sensitive help (3.3.5) |

**Decision rule:** Target WCAG 2.2 AA for all public-facing products. AAA is aspirational — pursue for specific criteria where achievable, but don't claim AAA conformance unless ALL criteria are met.

### Phase 2 (~30 min): Automated Testing

#### 2.1 axe-core (The Engine Under Everything)

axe-core powers Lighthouse, Deque's browser extension, pa11y, and most CI tools. Understanding axe directly gives you the most control.

**Browser Extension (quick audits):**
- Install [axe DevTools](https://www.deque.com/axe/devtools/) (Chrome/Firefox).
- Run "Scan all of my page" for a complete page audit.
- Use "Intelligent Guided Tests" for components requiring manual verification (axe can detect a color contrast issue but needs human judgment for complex gradients or images).

**CI Integration with Playwright:**
```typescript
// e2e/accessibility.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const PAGES_TO_AUDIT = ['/', '/login', '/dashboard', '/products', '/checkout'];

for (const path of PAGES_TO_AUDIT) {
  test(`a11y audit: ${path}`, async ({ page }) => {
    await page.goto(path);

    // Wait for page to stabilize
    await page.waitForLoadState('networkidle');

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .exclude('#google-recaptcha') // Exclude third-party components you can't fix
      .exclude('.third-party-chat-widget')
      .analyze();

    // Attach results to test report
    await test.info().attach('a11y-results', {
      body: JSON.stringify(results.violations, null, 2),
      contentType: 'application/json',
    });

    expect(results.violations).toEqual([]);
  });
}
```


**What good looks like:** Audit report with WCAG 2.2 AA violations ranked by severity (Critical/High/Medium/Low). Each finding contains: the failing element, the exact WCAG criteria violated, a code-level fix (not a principle — a specific change), and a screenshot showing the problem. Zero critical or high violations at launch. Screen reader navigation test passes on iOS VoiceOver and Android TalkBack.

**CI Quality Gate:**
```yaml
# .github/workflows/a11y.yml
name: Accessibility Audit
on: [pull_request]
jobs:
  a11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: npx playwright test e2e/accessibility.spec.ts
      - name: Report
        if: failure()
        run: echo "Accessibility violations found — see test artifacts"
```

#### 2.2 Lighthouse (Integrated Score)

```bash
# CLI audit with specific categories
npx lighthouse https://example.com \
  --only-categories=accessibility \
  --chrome-flags="--headless" \
  --output=json,html \
  --output-path=./reports/lighthouse-a11y

# CI: enforce minimum score
npx lighthouse https://example.com \
  --only-categories=accessibility \
  --chrome-flags="--headless" \
  --budget-path=./lighthouse-budget.json
```

`lighthouse-budget.json`:
```json
{
  "accessibility": 95
}
```

#### 2.3 False Positive Handling

axe-core has excellent precision but flags things that need human review:

| Common False Positive | Why It's Flagged | How to Resolve |
|-----------------------|-----------------|----------------|
| Color contrast on disabled buttons | axe checks disabled elements | Ensure disabled state is supplemented with opacity change, or exclude via `.exclude()` or `aria-disabled` |
| `aria-label` on interactive elements | Can override visible text | Ensure `aria-label` starts with visible text for voice control users |
| Landmarks on single-page app shell | Multiple `<nav>` elements | Give each `<nav>` a unique `aria-label` |
| Heading order in component-based pages | Dynamic content insertion | Always check rendered DOM, not component source. Use heading-level props or `aria-level`. |

**Rule of thumb:** Investigate every violation. If it's genuinely not a problem, document why in an accessibility exceptions log.

### Phase 3 (~20 min): Manual Testing

Automated testing catches ~30% of accessibility issues. The remaining 70% require human judgment.

#### 3.1 Keyboard-Only Navigation Test Script

**Equipment:** Unplug your mouse. Use only Tab, Shift+Tab, Enter, Space, Arrow keys, Escape.

**Script per page/component:**

```
1. TAB through every interactive element from top to bottom.
   □ Is a visible focus indicator present on EVERY element? (WCAG 2.4.7)
   □ Is the focus order logical? (Follows visual reading order: L→R, top→bottom)
   □ Can I reach ALL functionality? (Menus, dropdowns, modals, tooltips, tabs)

2. TAB + SHIFT reverse through elements.
   □ Does reverse order match forward order in reverse?

3. ENTER / SPACE on every button and link.
   □ ENTER activates links and buttons.
   □ SPACE activates buttons and toggles checkboxes.

4. ARROW KEYS for composite components.
   □ Tab panels: Left/Right arrows switch tabs.
   □ Menus: Up/Down arrows navigate items.
   □ Sliders: Left/Right or Up/Down adjust values.
   □ Date pickers: Arrow keys navigate calendar grid.

5. ESCAPE closes modals, dropdowns, popups.
   □ Does focus return to the triggering element? (WCAG 2.4.3)

6. SKIP LINK: Tab from page load. Is "Skip to main content" the first focusable element?
   □ Is it visible on focus? (Not display:none; use visually-hidden + visible-on-focus)
   □ Does it navigate past navigation to main content?
```

#### 3.2 Screen Reader Test Scripts

| Screen Reader | OS | Activation | Key Commands |
|---------------|-----|-----------|--------------|
| **VoiceOver** | macOS/iOS | Cmd+F5 (Mac) / Triple-click side button (iOS) | VO+Left/Right: navigate. VO+Space: activate. VO+U: rotor (landmarks, headings, links). |
| **NVDA** | Windows (free) | Ctrl+Alt+N | Down Arrow: next element. H: next heading. K: next link. Insert+F7: elements list. |
| **JAWS** | Windows (paid, enterprise standard) | Desktop shortcut | Tab: next focusable. H: next heading. Insert+F6: heading list. Insert+F7: links list. |

**VoiceOver Test Script (macOS):**

```
1. Activate VoiceOver (Cmd+F5).

2. Page structure scan:
   □ Open Rotor (VO+U). Navigate with Left/Right arrows through:
     - Landmarks: Can I identify banner, navigation, main, complementary, contentinfo?
     - Headings: Is there a logical hierarchy? Are there gaps (h1 → h3)?
     - Links: Are link texts descriptive without context? (No "click here", "read more")

3. Navigate sequentially (VO+Right Arrow):
   □ Is every element announced with its name, role, and state?
     Example: "Products, button, expanded" or "Email address, edit text, required"
   □ Are images announced with meaningful alt text or marked decorative?
   □ Are form errors announced? (Use aria-live="polite" region)

4. Interactive elements (VO+Space to activate):
   □ Buttons: Does VO announce the action that will occur?
   □ Toggles: Does VO announce state changes? "Muted, button, selected"
   □ Dynamic content: Does VO announce new content? Use aria-live for toasts/alerts.

5. Forms (interact with form fields):
   □ Does each field have an associated label read on focus?
   □ Are required fields announced?
   □ On validation error, are error messages announced?
```

**NVDA Test Script (Windows):**

```
1. Start NVDA (Ctrl+Alt+N).

2. Elements list (Insert+F7):
   □ Links: Are all link texts unique and descriptive?
   □ Headings: Is the hierarchy correct?
   □ Landmarks: Are all regions properly labeled?

3. Browse mode navigation (H, K, B, F keys):
   □ H: Cycle headings — correct level announcement?
   □ K: Cycle links — descriptive names?
   □ B: Cycle buttons — clear purpose announced?
   □ F: Cycle form fields — labels read?

4. Focus mode (interacting with form fields):
   □ Tab through fields — labels announced?
   □ Submit form — errors announced in browse mode?
```

#### 3.3 Zoom and Magnification Testing

```
1. Browser zoom: Ctrl/Cmd + Plus to 200%.
   □ All content visible? No horizontal scrolling required?
   □ No content overlapping, truncation, or cutoff?
   □ Interactive elements remain clickable?

2. Text-only zoom: Firefox → View → Zoom → Zoom Text Only. Zoom to 200%.
   □ Text reflows within viewport? (WCAG 1.4.4)
   □ Line height and letter spacing remain readable?

3. Mobile viewport: 320px width (CSS pixels).
   □ No horizontal scrolling? (WCAG 1.4.10)
   □ Touch targets ≥ 24×24 CSS pixels? (WCAG 2.5.8, AA)
   □ Spacing between touch targets sufficient?
```

#### 3.4 Color Blindness Simulation

```bash
# Chrome DevTools: Rendering tab → Emulate vision deficiencies
# Test with:
# - Protanopia (red-blind) — 1% of males
# - Deuteranopia (green-blind) — 1% of males
# - Tritanopia (blue-blind) — rare
# - Achromatopsia (no color) — rare

# Check: Do color-coded indicators have non-color differentiators?
# Bad: "Red items are overdue, green are on-time"
# Good: "Red items (⚠ overdue) and green items (✓ on-time)"
```

### Phase 4 (~15 min): Semantic HTML Audit

#### 4.1 Landmark Region Audit

Every page must have these ARIA landmarks (or equivalent HTML5 elements):

| Landmark | HTML5 Element | Required? | Purpose |
|----------|--------------|-----------|---------|
| `banner` | `<header>` (when child of `<body>`) | Yes | Site-wide header (logo, nav, search) |
| `navigation` | `<nav>` | Yes | Primary navigation block(s) |
| `main` | `<main>` | Yes | Primary content — exactly ONE per page |
| `complementary` | `<aside>` | If applicable | Supporting content (sidebar, related links) |
| `contentinfo` | `<footer>` (when child of `<body>`) | Yes | Site-wide footer |
| `form` | `<form aria-label="...">` | If applicable | Search form needs a label to distinguish from other forms |
| `region` | `<section aria-label="...">` | If applicable | Distinct page sections need labels |

**Landmark checklist:**
```
□ Exactly one <main> element.
□ Every <nav> has a unique aria-label (e.g., "Main", "Breadcrumb", "Footer").
□ <header> and <footer> are direct children of <body> (not nested in sections).
□ All content is inside a landmark region (no orphaned content outside landmarks).
□ Search form is in a <search> landmark or <form role="search"> with label.
```

#### 4.2 Heading Hierarchy Audit

```
□ Exactly one <h1> per page — matches page title or primary purpose.
□ No heading level skips (h1 → h3 without h2 is an error).
□ Headings are used structurally, not for visual styling.
  Bad: <h2 class="text-2xl font-bold"> — using heading for large text.
  Good: <h2>Products</h2><p class="text-2xl font-bold">Marketing tagline</p>
□ Heading text describes the content that follows.
□ Visual heading hierarchy matches semantic hierarchy.
```

**Quick check:** Open browser DevTools, run:
```javascript
// Extract heading outline
[...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => ({
  level: h.tagName,
  text: h.textContent.trim().substring(0, 80),
}));
```

#### 4.3 Table Structure

```
□ <table> only for tabular data (never for layout).
□ <caption> describes the table's purpose.
□ <thead>, <tbody>, <tfoot> for structure.
□ <th scope="col|row"> for all headers.
□ Complex tables: headers + id association for multi-level headers.
□ Responsive tables: consider cards at mobile or horizontal scroll with instructions.
```

---
### Phase 5 (~25 min): Focus Management Deep Dive

#### 5.1 Focus Order

Tab order must follow DOM order. Avoid `tabindex` > 0 (creates a parallel tab order that's confusing).

```html
<!-- Bad: tabindex > 0 creates non-sequential focus -->
<button tabindex="1">First</button>  <!-- Shown first visually -->
<button tabindex="3">Third</button> <!-- Shown third visually -->
<button tabindex="2">Second</button> <!-- Tab order: First → Second → Third — confusing! -->

<!-- Good: Natural DOM order (no tabindex, or tabindex="0" only) -->
<button>First</button>
<button>Second</button>
<button>Third</button>
```

**Valid `tabindex` values:**
| Value | Meaning | Usage |
|-------|---------|-------|
| `0` | Element in natural tab order | Make non-interactive elements (div, span, custom components) keyboard-focusable |
| `-1` | Removable from tab order but programmatically focusable | Modal containers, elements focusable via `element.focus()` |
| `> 0` | **ANTI-PATTERN** — creates separate tab order | Never use. Restructure DOM instead. |

#### 5.2 Focus Indicators

```css
/* Good: visible, high-contrast focus indicator */
*:focus-visible {
  outline: 3px solid #2563EB;
  outline-offset: 2px;
  border-radius: 4px;
}

/* Never do this: */
*:focus {
  outline: none; /* WCAG 2.4.7 violation — unless you provide a custom one */
}

/* If removing default outline, you MUST provide a custom one: */
button:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px #2563EB; /* Custom focus ring — at least 3px */
}
```

#### 5.3 Focus Trapping (Modals)

```typescript
// Focus trap for modals — simplified pattern
function Modal({ isOpen, onClose, children }) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      previousFocusRef.current = document.activeElement as HTMLElement;

      // Focus the modal
      const firstFocusable = modalRef.current?.querySelector<HTMLElement>(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      firstFocusable?.focus();

      const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === 'Escape') {
          onClose();
          return;
        }
        if (e.key !== 'Tab') return;

        const focusableElements = modalRef.current?.querySelectorAll<HTMLElement>(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        if (!focusableElements || focusableElements.length === 0) return;

        const first = focusableElements[0];
        const last = focusableElements[focusableElements.length - 1];

        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      };

      document.addEventListener('keydown', handleKeyDown);
      return () => {
        document.removeEventListener('keydown', handleKeyDown);
        previousFocusRef.current?.focus(); // Restore focus on close
      };
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div role="dialog" aria-modal="true" aria-labelledby="modal-title" ref={modalRef}>
      <h2 id="modal-title">Modal Title</h2>
      {children}
    </div>
  );
}
```

#### 5.4 Skip Links

```html
<!-- Visually hidden until focused -->
<a href="#main-content" class="skip-link">
  Skip to main content
</a>

<style>
.skip-link {
  position: absolute;
  top: -100%;
  left: 0;
  padding: 8px 16px;
  background: #2563EB;
  color: white;
  z-index: 10000;
}
.skip-link:focus {
  top: 0;
}
</style>
```

---
### Phase 6 (~25 min): Accessible Forms

#### 6.1 Labeling

```html
<!-- Explicit label — always preferred -->
<label for="email">Email address</label>
<input type="email" id="email" required aria-describedby="email-hint email-error" />
<p id="email-hint">We'll never share your email.</p>
<p id="email-error" role="alert" class="hidden">Please enter a valid email.</p>

<!-- Implicit label (wrapping) — acceptable but less robust -->
<label>Email address <input type="email" /></label>

<!-- aria-label for inputs without visible label (search icon buttons) -->
<input type="search" aria-label="Search products" />

<!-- aria-labelledby for complex labeling -->
<span id="card-label">Credit Card Number</span>
<span id="card-hint">16 digits on the front of your card</span>
<input type="text" aria-labelledby="card-label card-hint" />
```

#### 6.2 Error Handling

```html
<!-- Before: No error association -->
<input type="email" id="email" />
<span class="error">Invalid email</span>

<!-- After: Error associated, announced -->
<input type="email" id="email" aria-describedby="email-error" aria-invalid="true" />
<span id="email-error" role="alert">Please enter a valid email address (e.g., name@example.com)</span>
```

**Error handling checklist:**
```
□ Error messages associated via aria-describedby.
□ aria-invalid="true" on fields with errors.
□ Error summary at top of form linking to each error field.
□ Errors use role="alert" for screen reader announcement.
□ Inline errors appear on blur AND on submit.
□ Error text describes how to fix the problem, not just "Invalid input."
```

#### 6.3 Required Field Indication

```html
<!-- Don't rely on color alone -->
<input type="text" id="name" required aria-required="true" />
<label for="name">
  Full name
  <span aria-hidden="true" class="text-red-500">*</span>
  <span class="sr-only">(required)</span>
</label>

<!-- Or indicate optional fields instead (less visual noise) -->
<label for="middle-name">
  Middle name
  <span class="text-gray-500">(optional)</span>
</label>
```

---
### Phase 7 (~25 min): Time-Based Media

| Media Type | Level A | Level AA | Level AAA |
|------------|---------|----------|-----------|
| **Pre-recorded audio** | Transcript (1.2.1) | Transcript (1.2.1) | Transcript + sign language (1.2.6) |
| **Pre-recorded video (no audio)** | Text or audio alternative (1.2.1) | Text or audio alternative (1.2.1) | Text alternative (1.2.8) |
| **Pre-recorded video with audio** | Captions (1.2.2) + transcript or audio description (1.2.3) | Captions + audio description (1.2.5) | Captions + extended audio description + transcript + sign language (1.2.6, 1.2.7, 1.2.8) |
| **Live audio** | Captions (1.2.4) | Captions (1.2.4) | Sign language (not required in 2.2) |
| **Live video with audio** | Captions (1.2.4) | Captions (1.2.4) | Extended audio description (not required in 2.2) |

**Caption best practices:**
- SRT/WebVTT format with accurate timing.
- Speaker identification for multiple speakers.
- Sound effects described: `[door slams]`, `[phone ringing]`.
- Captions synchronized within 100ms of audio.

---
### Phase 8 (~30 min): Accessibility Statement

Every public product needs an accessibility statement. Template:

```markdown
# Accessibility Statement

[Organization Name] is committed to digital accessibility. We aim to conform to
WCAG 2.2 Level AA.

## Conformance Status
This website is [fully / partially / not] conformant with WCAG 2.2 Level AA.
[Partially conformant means some parts do not fully conform.]

## Known Limitations
| Issue | WCAG Criterion | Impact | Timeline |
|-------|---------------|--------|----------|
| Third-party chat widget has contrast issues | 1.4.3 | Customers using keyboard navigation cannot read chat messages | Q2 2025 (vendor ETA) |
| PDF documents created before 2023 are not tagged | 1.3.1 | Screen reader users cannot navigate older PDFs | Archived — contact for alternative format |

## Feedback
We welcome your feedback. Please contact us:
- Email: accessibility@example.com
- Phone: (555) 123-4567
- Response time: 2 business days

## Preparation
This statement was prepared on [Date]. It was last reviewed on [Date].
```

---
### Phase 9 (~20 min): Legal Landscape

| Law/Standard | Jurisdiction | Applies To | Key Requirement |
|-------------|-------------|------------|-----------------|
| **ADA Title III** | USA | Places of public accommodation (websites, apps considered places) | "Reasonable accommodation" — courts have consistently interpreted this as WCAG 2.1 AA |
| **Section 508** | USA | Federal agencies and contractors | WCAG 2.0 AA (refreshed to 2.1 in 2028) + ICT requirements |
| **EN 301 549** | EU | Public sector bodies, increasingly private sector via EAA | WCAG 2.1 AA — harmonized European standard |
| **European Accessibility Act (EAA)** | EU | Products and services sold in EU (effective June 2025) | WCAG 2.1 AA for e-commerce, banking, transport, e-books, ATMs |
| **AODA** | Ontario, Canada | Public & private sector orgs with 50+ employees | WCAG 2.0 AA (moving to 2.1) |

**Risk assessment factors:**
- **High risk:** E-commerce, banking, healthcare, education, government. These sectors see the most lawsuits.
- **Medium risk:** B2B SaaS, media/publishing, real estate.
- **Lower risk:** Internal tools, developer tools, early-stage startups (though this is changing).

---
### Phase 10: Remediation Prioritization

Use severity-based triage — prioritize by user impact, not by WCAG level:

| Severity | Description | Example | Response |
|----------|-------------|---------|----------|
| **Blocker** | User literally **cannot** complete a core task | Checkout button not keyboard-accessible | Fix immediately — same sprint |
| **Critical** | User can complete task but with **extreme difficulty** or **no alternative** | CAPTCHA without audio alternative | Fix within 2 weeks |
| **Major** | User can complete task with **significant friction** | Missing form error association, requiring guessing which field errored | Fix within 1 month |
| **Minor** | **Annoying** but workaround exists | Heading level skipped, causing confusing navigation | Fix within 3 months |
| **Cosmetic** | Best practice, minimal user impact | Missing `lang` attribute on a single quoted phrase | Backlog — fix opportunistically |

**Blocker → Critical → Major → Minor → Cosmetic.** Fix in that order, regardless of WCAG level. A Level A issue that blocks users is more urgent than a Level AA issue that's cosmetic.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Accessibility is not a QA gate at the end — it's a design constraint from day one. Coordination with design, engineering, and legal ensures accessibility is built in, not bolted on.

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `ui-ux-designer` | Component specs with interaction states, design tokens (color, spacing, typography), Figma frames with focus order annotations | During design review; before component handoff to engineering |
| `frontend-developer` | Implemented components with ARIA patterns, semantic HTML structure, keyboard navigation behavior, live region updates | During code audit; before PR merge for accessibility-critical features |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `frontend-developer` | WCAG violation report with code-level fix guidance, ARIA pattern recommendations, semantic HTML corrections, focus management remediation | Inaccessible code ships to production — legal exposure and user exclusion |
| `qa-engineer` | Accessibility test cases, axe-core/Lighthouse CI integration config, screen reader test scripts, severity classification rubric | Accessibility regressions go undetected — bugs accumulate |
| `legal-advisor` | WCAG conformance status report, VPAT/ACR draft, known issues register, remediation timeline, legal exposure assessment | Compliance deadline missed — ADA/508 demand letters or lawsuits |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Blocker-level accessibility issue found in production | `product-manager`, `frontend-developer`, `legal-advisor` | Hotfix prioritization, legal exposure assessment, customer communication if warranted |
| ADA/508 demand letter or lawsuit received | `legal-advisor`, `ceo-strategist`, `product-manager`, `cto-advisor` | Immediate legal response, remediation acceleration, PR strategy |
| Design system component fails WCAG AA | `ui-ux-designer`, `frontend-developer` | Component redesign, downstream impact assessment, fix timeline |
| Accessibility score drops below CI threshold | `frontend-developer`, `qa-engineer`, `product-manager` | Build blocked, root cause identification, fix assignment |
| New feature ships without accessibility review | `product-manager`, `frontend-developer`, `legal-advisor` (if regulated) | Retroactive audit, remediation ticket, process improvement |
| VPAT/ACR requested by enterprise customer | `legal-advisor`, `product-manager` | Conformance documentation, known issues disclosure, remediation commitments |

### Escalation Path

```
Legal/regulatory risk (lawsuit filed, demand letter, DOJ investigation)
  └── `legal-advisor` + `ceo-strategist` + `product-manager` + `cto-advisor`. External counsel engaged. All-hands remediation.

Systemic accessibility failure (core user journey completely inaccessible)
  └── `product-manager` + `cto-advisor` + `ui-ux-designer`. Remediation sprint. Feature flagged or rolled back.

Design system violation (shared component fails audit, affects all products)
  └── `ui-ux-designer` + `frontend-developer`. Fix component, propagate to all consumers.
```

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Test with real users:** Automated tools and manual scripts are proxies. Real users with disabilities find issues you'll never catch. Test with at least 3 users with different disabilities.
- **Shift left:** Catch accessibility issues in design (color contrast, focus order, heading structure) before code is written.
- **Design system integration:** Build accessible components once. A button with correct focus, label, and role in the design system benefits every page.
- **Don't override semantics:** `<div onclick>` is not a button. Use `<button>`. `<span class="h2">` is not a heading. Use `<h2>`.
- **ARIA is a last resort:** If you can use native HTML, use it. ARIA adds roles/states/properties but not behavior — you must implement keyboard interaction yourself.
- **`aria-label` must start with visible text:** Voice control users say "Click [visible text]" — if the accessible name differs from visible text, voice commands fail.

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Accessibility = use semantic HTML and check contrast. Run Lighthouse once before launch. No formal WCAG audit. No screen reader testing. Fix the obvious stuff.
- **What to skip**: Full WCAG audit. Screen reader testing. Keyboard-only testing. VPAT/ACR. Accessibility statement. Automated a11y in CI.
- **Coordination**: You test your own work. No coordination needed.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Lighthouse in CI (≥90 score gate). Manual keyboard testing on critical flows. Screen reader spot-check (VoiceOver + NVDA). Semantic HTML audit. Basic accessibility statement. Color contrast checked in design tool.
- **What to skip**: Full WCAG 2.2 AA audit. Professional accessibility audit. VPAT. Automated a11y beyond Lighthouse + axe-core. Accessibility specialist hire.
- **Coordination**: Designer checks contrast. Developer runs Lighthouse in PR. QA does keyboard pass on release. Monthly a11y check-in (15 min).

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: WCAG 2.2 AA conformance target with compliance roadmap. axe-core in CI with quality gates. Manual keyboard + screen reader testing per release. Accessibility champion on each team. VPAT/ACR for enterprise sales. Accessibility statement published. Design system with baked-in accessibility.
- **What to skip**: Full-time accessibility specialist (champions model works). WCAG AAA (target AA). Professional audit every release (annual is enough).
- **Coordination**: Accessibility champions bi-weekly sync. Quarterly accessibility review with PM leadership. VPAT updated per major release.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Dedicated accessibility team (1-3 specialists). Full WCAG 2.2 AA conformance across all products. Professional accessibility audit annually. Accessibility embedded in design system components. VPAT/ACR maintained for all products. Accessibility in procurement review. Legal review of accessibility risk. User testing with people with disabilities.
- **What's full production**: Accessibility program office. Continuous monitoring (axe-core + manual). Training program for all engineers and designers. Accessibility in definition of done. Procurement accessibility requirements.
- **Coordination**: Monthly accessibility program review. Quarterly executive accessibility report. Annual professional audit. Accessibility team weekly with product teams.

### Transition Triggers
- **Solo → Small**: First accessibility complaint or enterprise customer asking about VPAT.
- **Small → Medium**: Enterprise deals require WCAG conformance. Legal risk from accessibility lawsuits. >10K users.
- **Medium → Enterprise**: Multiple products requiring accessibility governance. Regulatory mandate (Section 508, EN 301 549). >100K users.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | ui-ux-designer | Component specs, interaction patterns, design tokens |
| **This** | accessibility-auditor | WCAG audit report, remediation priorities, VPAT/ACR |
| **After** | frontend-developer | Accessible implementation with ARIA, keyboard nav, semantic HTML |

Common chains:
- **Design to compliance**: ui-ux-designer → accessibility-auditor → frontend-developer — from visual design to accessible code
- **Risk assessment**: qa-engineer → accessibility-auditor → legal-advisor — from bug reports to legal risk evaluation



### Design-to-Code Handoff Chain
```bash
# Figma → Design tokens → Component → Implementation → Verify
/ui-ux-designer && /frontend-developer && /qa-engineer
# Every Figma frame has: spacing token, color token, typography token, breakpoint annotation.
# Frontend devs should never guess measurements — if it's not in the handoff, it doesn't exist.

# Brand → Design system → Component library → App
/brand-guidelines && /ui-ux-designer && /frontend-developer
# Brand tokens feed into the design system. Design system tokens are the single source of truth.
# No hardcoded colors or spacing values — every pixel comes from a named token.

# Accessibility → Design → Development → Audit
/accessibility-auditor && /ui-ux-designer && /frontend-developer
# Accessibility requirements are annotated on every Figma frame before handoff.
# Color contrast, heading hierarchy, focus management, and touch targets are non-negotiable.
# Auditor verifies post-implementation — not post-launch.
```

## What Good Looks Like

> Every interactive element on the page is reachable via keyboard, announced correctly by screen readers, and perceivable at 200% zoom without content loss or horizontal scrolling. Color contrast ratios meet or exceed WCAG 2.2 AA across all states — hover, focus, active, disabled, and error — with dark mode validated separately. Semantic landmarks and a logical heading hierarchy give assistive technology users a clear mental model of the page structure in under 10 seconds. Automated axe-core checks run in CI and pass with zero violations, while manual audits confirm that complex widgets like modals, carousels, and autocompletes follow ARIA authoring practices to the letter. The VP of Legal confirms the product meets ADA Title III, Section 508, and EN 301 549 obligations without a single remediation sprint.

## Sub-Skills
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


### Error Decoder
<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Design doesn't match brand | Missing design token reference | Define all colors, spacing, typography as tokens before starting any screen. Style guide → component library. | Brand consistency is a systems problem, not an oversight problem. Design tokens are the source of truth — without them, every screen is a one-off that drifts from the brand. |
| Accessibility gap found in audit | Not tested during design phase | Test with axe-core during design, not after. Color contrast and heading hierarchy are non-negotiable from the start. | Accessibility is not a QA step — it is a design constraint. Catching a contrast violation in design takes 5 seconds; fixing it post-launch takes a sprint. |
| Dev implementation differs from design | No handoff spec beyond mockups | Annotate every element: breakpoints, hover/focus/active states, animation timing, empty states. Zeplin/Figma Dev Mode. | Every unannotated element in a handoff will be interpreted differently by the developer. The cost of specifying an interaction state is measured in seconds; the cost of rebuilding it is measured in days. |
| Dark mode breaks screens | Only tested in light mode | Design dark mode in parallel. Every screen must support both from day one. | Dark mode is not a theme — it is a second design system. Designing it after the fact is a full redesign, not a toggle flip. Build both color schemas into your token system from day one. |
| Component doesn't scale to content | Designed with one data example | Test components with minimum, maximum, and empty content. Real user data, not Lorem Ipsum. | A component tested with one data example works once. Test with real extremes — short names, long text, zero results — to build components that survive production data. |
| Platform inconsistency (iOS vs Android) | No platform-specific adaptation | iOS uses tab bar (bottom); Android uses navigation bar (top). Design per platform, not pixel-perfect identical. | Platform conventions exist because users expect them. Pixel-perfect cross-platform consistency creates a worse experience than following each platform's native patterns. Design for the platform, not for screenshots. |
| Motion causes dizziness | Uncontrolled animation | Respect `prefers-reduced-motion`. Use `motion-safe`/`motion-reduce` for all animations. | Animation is not decoration — it is an accessibility risk. Every transition should be questioned: does it serve a purpose, or does it just look cool? `prefers-reduced-motion` is not optional. |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  WCAG 2.2 AA conformance target defined and communicated
- [ ] **[S2]**  Automated testing (axe-core + Lighthouse) in CI pipeline with quality gates (≥ 95 Lighthouse a11y score)
- [ ] **[S3]**  Manual keyboard testing completed on all critical user flows
- [ ] **[S4]**  Screen reader testing completed: VoiceOver (macOS) + NVDA (Windows) on core flows
- [ ] **[S5]**  Semantic HTML audit: single `<main>`, named `<nav>` elements, heading hierarchy without skips
- [ ] **[S6]**  All interactive elements have visible focus indicators (no `outline: none` without custom indicator)
- [ ] **[S7]**  Focus trapping implemented in all modals, drawers, and dialogs
- [ ] **[S8]**  All form inputs have associated labels; errors linked via `aria-describedby`; `aria-invalid` on error
- [ ] **[S9]**  Color is never the sole differentiator for information (supplement with icons, text, or patterns)
- [ ] **[S10]**  Accessibility statement published with conformance claims, known limitations, and contact info

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [WCAG 2.2 Specification](https://www.w3.org/TR/WCAG22/)
- [axe-core Documentation](https://github.com/dequelabs/axe-core)
- [WebAIM Screen Reader Survey](https://webaim.org/projects/screenreadersurvey9/)
- [WAI-ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [The A11y Project](https://www.a11yproject.com/)
- [Inclusive Components](https://inclusive-components.design/) — Heydon Pickering
- [Accessibility for Everyone](https://abookapart.com/products/accessibility-for-everyone) — Laura Kalbag
- [Section 508](https://www.section508.gov/)
- [EN 301 549](https://www.etsi.org/human-factors-accessibility/en-301-549-v3-the-harmonized-european-standard-for-ict-accessibility)
