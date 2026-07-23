# Core Workflow — Full Implementation

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
