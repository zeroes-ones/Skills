# Accessibility Auditor - WCAG 2.2 Checklist

Complete WCAG 2.2 Level AA checklist with test methods and code examples.

---

## How to Use

- **Level A:** Minimum — must satisfy, basic accessibility
- **Level AA:** Should satisfy — addresses biggest barriers (legal standard: ADA, Section 508, EN 301 549)
- **Level AAA:** May satisfy — highest standard

This checklist covers **Level A & AA** (all 50 success criteria in WCAG 2.2).

**Test Methods:**
- 🔍 Visual inspection
- ⌨ Keyboard test
- 🖥 Screen reader (VoiceOver/NVDA/JAWS)
- 📐 Automated tool (axe-core, Lighthouse, WAVE)
- 💻 Code review

---

## Principle 1: Perceivable

### 1.1 Text Alternatives

| SC | Level | Criterion | Test Method | Pass Criteria |
|----|-------|-----------|-------------|---------------|
| 1.1.1 | A | Non-text content has text alternative | 🔍🖥 | Images have alt text; decorative images have `alt=""`; CAPTCHAs have alternatives |

**Code Examples:**
```html
<!-- PASS: Meaningful alt text -->
<img src="chart.png" alt="Q4 revenue: $2.3M, up 12% from Q3">

<!-- PASS: Decorative image -->
<img src="divider.png" alt="">

<!-- FAIL: No alt text -->
<img src="chart.png">

<!-- FAIL: Alt text describes appearance, not content -->
<img src="chart.png" alt="Blue bar chart">
```

### 1.2 Time-Based Media

| SC | Level | Criterion | Test Method | Pass Criteria |
|----|-------|-----------|-------------|---------------|
| 1.2.1 | A | Audio-only/video-only: alternative | 🔍 | Transcript for audio; descriptive transcript or audio description for video |
| 1.2.2 | A | Captions (prerecorded) | 🔍 | All pre-recorded video with audio has synchronized captions |
| 1.2.3 | A | Audio description or media alternative | 🔍 | Video content also available as text or audio description |
| 1.2.4 | AA | Captions (live) | 🔍 | Live video streams have captions |
| 1.2.5 | AA | Audio description (prerecorded) | 🔍 | Audio description for all pre-recorded video |

```html
<!-- PASS: Captions via <track> -->
<video controls>
  <source src="tutorial.mp4" type="video/mp4">
  <track src="captions.vtt" kind="captions" srclang="en" label="English">
</video>

<!-- PASS: Transcript adjacent to media -->
<video controls src="interview.mp4"></video>
<details>
  <summary>Transcript</summary>
  <p>Interviewer: Welcome. Guest: Thank you...</p>
</details>
```

### 1.3 Adaptable

| SC | Level | Criterion | Test Method | Pass Criteria |
|----|-------|-----------|-------------|---------------|
| 1.3.1 | A | Info and relationships | 📐💻 | Semantic HTML: headings `<h1>`-`<h6>`, lists `<ul>/<ol>`, tables `<th>` with scope |
| 1.3.2 | A | Meaningful sequence | 🔍 | Reading order matches visual order; no CSS `position: absolute` reversing order |
| 1.3.3 | A | Sensory characteristics | 💻 | No instructions relying solely on "click the red button" or "see right sidebar" |
| 1.3.4 | AA | Orientation | 🔍📐 | Content works in both portrait and landscape; no forced orientation |
| 1.3.5 | AA | Identify input purpose | 💻 | Form inputs have `autocomplete` attribute per WCAG 2.2 Input Purposes |

```html
<!-- PASS: Semantic structure -->
<h1>Annual Report</h1>
<h2>Financial Summary</h2>
<h3>Revenue</h3>
<table>
  <thead><tr><th scope="col">Quarter</th><th scope="col">Revenue</th></tr></thead>
  <tbody><tr><td>Q1</td><td>$1.2M</td></tr></tbody>
</table>

<!-- PASS: Autocomplete for common fields -->
<input type="text" name="email" autocomplete="email">
<input type="text" name="name" autocomplete="name">
<input type="text" name="country" autocomplete="country-name">

<!-- FAIL: Sensory-only instructions -->
<p>Click the green button on the right to continue.</p>
<!-- FIX: <p>Click <strong>Continue</strong> to proceed.</p> -->
```

### 1.4 Distinguishable

| SC | Level | Criterion | Test Method | Pass Criteria |
|----|-------|-----------|-------------|---------------|
| 1.4.1 | A | Use of color | 🔍📐 | Color not sole means of conveying info; error states use icon + text |
| 1.4.2 | A | Audio control | 🔍 | Auto-playing audio >3s has pause/stop/mute; or is independently controllable |
| 1.4.3 | AA | Contrast (minimum) | 📐 | Text: 4.5:1; large text (≥18pt or 14pt bold): 3:1 |
| 1.4.4 | AA | Resize text | 🔍 | Text resizes to 200% without content/function loss (no fixed px heights) |
| 1.4.5 | AA | Images of text | 🔍 | No images of text (except logos, or where essential) |
| 1.4.10 | AA | Reflow | 🔍 | Content reflows to 320px width (CSS pixels) without horizontal scrolling |
| 1.4.11 | AA | Non-text contrast | 📐 | UI components and graphics: 3:1 against adjacent colors |
| 1.4.12 | AA | Text spacing | 🔍 | Content works with: line-height 1.5, paragraph spacing 2× font, letter-spacing 0.12×, word-spacing 0.16× |
| 1.4.13 | AA | Content on hover/focus | 🔍 | Hover/focus content: dismissible (Esc), hoverable (persistent), persists until dismissed |

```css
/* PASS: 4.5:1 text contrast and 3:1 non-text contrast */
.text-body {
  color: #333333; /* 12.6:1 on white */
  background-color: #ffffff;
}
.button {
  background-color: #2563EB; /* 5.9:1 on white */
  color: #ffffff;
  border: 2px solid #1D4ED8;
}

/* FAIL: Light gray text on white */
.text-subtle {
  color: #CCCCCC; /* 1.6:1 — FAIL */
  background: #FFFFFF;
}
/* FIX: color: #767676; /+ 4.54:1 +/ */

/* PASS: Reflow — use relative units, max-width */
.container {
  max-width: 80rem; /* 1280px equivalent — no horizontal scroll at 320px */
  padding: 1rem;
}
img {
  max-width: 100%;
  height: auto;
}
```

---

## Principle 2: Operable

### 2.1 Keyboard Accessible

| SC | Level | Criterion | Test Method | Pass Criteria |
|----|-------|-----------|-------------|---------------|
| 2.1.1 | A | Keyboard | ⌨ | All functionality operable via keyboard (no mouse-only handlers) |
| 2.1.2 | A | No keyboard trap | ⌨ | Focus never trapped in element without exit |
| 2.1.4 | A | Character key shortcuts | ⌨💻 | Single-char shortcuts: remappable, turn-off-able, or only active on focus |

```html
<!-- PASS: Interactive element reachable by keyboard -->
<button onclick="submitForm()">Submit</button>
<a href="/profile">Profile</a>
<div role="button" tabindex="0" onkeydown="if(event.key==='Enter') activate()">Click me</div>

<!-- FAIL: Div without tabindex or keyboard handler -->
<div onclick="doSomething()">Click me</div>
<!-- FIX: Use <button> or add role="button" tabindex="0" + onkeydown -->
```

### 2.2 Enough Time

| SC | Level | Criterion | Test Method | Pass Criteria |
|----|-------|-----------|-------------|---------------|
| 2.2.1 | A | Timing adjustable | 🔍 | Time limits: turn off, adjust to 10×, or extend (except real-time or >20h) |
| 2.2.2 | A | Pause, stop, hide | 🔍 | Auto-moving/updating content: pause, stop, or hide mechanism |

### 2.3 Seizures and Physical Reactions

| SC | Level | Criterion | Test Method | Pass Criteria |
|----|-------|-----------|-------------|---------------|
| 2.3.1 | A | Three flashes or below threshold | 📐 | No content flashes >3× per second |
| 2.3.2 | A (WCAG 2.2 new) | Focus appearance | 🔍📐 | Focus indicator: ≥2px thick, contrast ≥3:1 against adjacent colors, minimum area of focus indicator perimeter |

```css
/* PASS: Visible focus ring with 3:1 contrast */
:focus-visible {
  outline: 3px solid #2563EB;
  outline-offset: 2px;
}

/* FAIL: Removed focus outline without replacement */
:focus {
  outline: none;
}
/* FIX: Provide custom visible focus indicator — never remove without replacement */
```

### 2.4 Navigable

| SC | Level | Criterion | Test Method | Pass Criteria |
|----|-------|-----------|-------------|---------------|
| 2.4.1 | A | Bypass blocks | ⌨🖥 | Skip navigation link as first focusable element |
| 2.4.2 | A | Page titled | 🔍 | Unique, descriptive `<title>` per page |
| 2.4.3 | A | Focus order | ⌨ | Focus order matches visual/logical reading order |
| 2.4.4 | A | Link purpose (in context) | 🖥💻 | Link text alone or in context describes purpose; no "click here", "read more" |
| 2.4.5 | AA | Multiple ways | 🔍 | ≥2 ways to find pages (nav, search, sitemap, table of contents) |
| 2.4.6 | AA | Headings and labels | 🔍💻 | Headings describe topic; labels describe field purpose |
| 2.4.7 | AA | Focus visible | ⌨ | Keyboard focus indicator always visible (see 2.3.2 for new enhanced requirement) |

```html
<!-- PASS: Skip link -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- PASS: Descriptive link text -->
<a href="/reports/q4-2023.pdf">Q4 2023 Financial Report (PDF, 2.1 MB)</a>

<!-- FAIL: Ambiguous link-text -->
<a href="/reports/q4.pdf">Click here</a>
```

### 2.5 Input Modalities

| SC | Level | Criterion | Test Method | Pass Criteria |
|----|-------|-----------|-------------|---------------|
| 2.5.1 | A | Pointer gestures | 🔍 | Multi-point/path gestures have single-pointer alternative |
| 2.5.2 | A | Pointer cancellation | 🔍 | Up-event: no down-event activation; can cancel by moving away |
| 2.5.3 | A | Label in name | 🖥💻 | Visible label text matches (or starts with) accessible name |
| 2.5.4 | A | Motion actuation | 🔍 | Motion-operated functions have alternative; can be disabled |
| 2.5.7 | AA (WCAG 2.2 new) | Dragging movements | ⌨ | Dragging actions have single-pointer alternative (e.g., up/down buttons on sortable list) |
| 2.5.8 | AA | Target size (minimum) | 📐 | Pointer targets ≥ 24×24 CSS pixels (except inline links, spacing, user-agent controls) |

```css
/* PASS: Minimum target size 24x24px */
.icon-button {
  width: 44px;
  height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* PASS: Dragging alternative */
.sortable-list {
  /* Mouse: drag to reorder */
}
.sort-button {
  /* Keyboard: press button to move item up/down */
}
```

---

## Principle 3: Understandable

### 3.1 Readable

| SC | Level | Criterion | Test Method | Pass Criteria |
|----|-------|-----------|-------------|---------------|
| 3.1.1 | A | Language of page | 💻 | `<html lang="en">` matches primary language |
| 3.1.2 | AA | Language of parts | 💻 | Language changes marked: `<span lang="fr">Bonjour</span>` |

### 3.2 Predictable

| SC | Level | Criterion | Test Method | Pass Criteria |
|----|-------|-----------|-------------|---------------|
| 3.2.1 | A | On focus | ⌨ | Focusing element doesn't trigger context change (no auto-submit on focus) |
| 3.2.2 | A | On input | ⌨ | Changing setting doesn't auto-trigger context change unless warned |
| 3.2.3 | AA | Consistent navigation | 🔍 | Nav order and relative position same across pages |
| 3.2.4 | AA | Consistent identification | 🔍 | Same function/same label across pages (icon + "Search" always same) |
| 3.2.6 | A (WCAG 2.2 new) | Consistent help | 🔍 | Help mechanisms (contact, chat, FAQ) in consistent relative order |

### 3.3 Input Assistance

| SC | Level | Criterion | Test Method | Pass Criteria |
|----|-------|-----------|-------------|---------------|
| 3.3.1 | A | Error identification | 🔍🖥 | Error described in text; error field programmatically identified |
| 3.3.2 | A | Labels or instructions | 🔍💻 | All inputs have visible labels; required fields, expected format indicated |
| 3.3.3 | AA | Error suggestion | 🔍 | Suggestions provided when error detected (e.g., "Date must be MM/DD/YYYY") |
| 3.3.4 | AA | Error prevention (legal, financial, data) | 🔍 | Reversible, checked, or confirmed before final submission |
| 3.3.7 | A (WCAG 2.2 new) | Accessible authentication | 🔍 | No cognitive function test (e.g., "remember password" or password managers not blocked) |
| 3.3.8 | AA (WCAG 2.2 new) | Accessible authentication (minimum) | 🔍 | No cognitive test in any step — alternatives: magic link, WebAuthn, password manager |

```html
<!-- PASS: Error identification -->
<label for="email">Email address</label>
<input id="email" type="email" aria-describedby="email-error" aria-invalid="true">
<span id="email-error" role="alert">Please enter a valid email address (e.g., name@example.com)</span>

<!-- PASS: Confirmation before destructive action -->
<form onsubmit="return confirm('Delete your account? This cannot be undone.')">
  <button type="submit">Delete Account</button>
</form>

<!-- PASS: Accessible authentication — allows password managers -->
<input type="password" name="password" autocomplete="current-password">
<!-- NOT blocked by paste-disabled or copy-paste prevention scripts -->
```

---

## Principle 4: Robust

### 4.1 Compatible

| SC | Level | Criterion | Test Method | Pass Criteria |
|----|-------|-----------|-------------|---------------|
| 4.1.1 | A | Parsing (removed in WCAG 2.2) | 📐 | Obsolete — removed because browsers handle parsing errors |
| 4.1.2 | A | Name, role, value | 🖥💻 | All UI components have accessible name; ARIA roles/values correct; custom widgets expose state |
| 4.1.3 | AA | Status messages | 🖥💻 | Status messages (success, error, progress) announced without focus change — use `role="status"` or `aria-live` |

```html
<!-- PASS: Status message announced without focus change -->
<div role="status" aria-live="polite">
  <!-- Dynamically updated: "Item added to cart" — screen reader announces it -->
</div>

<!-- PASS: Custom widget with correct ARIA -->
<div role="tablist" aria-label="Product info">
  <button role="tab" aria-selected="true" aria-controls="panel-desc" id="tab-desc">Description</button>
  <button role="tab" aria-selected="false" aria-controls="panel-specs" id="tab-specs" tabindex="-1">Specifications</button>
</div>
<div role="tabpanel" id="panel-desc" aria-labelledby="tab-desc">...</div>
```

---

## Automated Testing Commands

```bash
# axe-core CLI — automated WCAG audit (catches ~30-40% of issues)
npx @axe-core/cli https://example.com --tags wcag2a,wcag2aa

# Lighthouse accessibility audit
npx lighthouse https://example.com --only-categories=accessibility --output=json

# pa11y CI — integrate into CI pipeline
npx pa11y https://example.com --standard WCAG2AA

# HTML validation (4.1.1 parsing — though now removed, still good practice)
npx html-validate "**/*.html"
```

## Quick Audit Process

1. **Automated scan** (axe-core, Lighthouse): Catch ~30-40% of issues (contrast, missing alt, ARIA violations)
2. **Keyboard audit**: Tab through entire app; verify focus order, focus visibility, no traps
3. **Screen reader audit** (one desktop + one mobile): Navigate pages; verify content and interactions work
4. **Zoom test**: Browser zoom to 200% and 400%; verify no content loss
5. **Color contrast audit**: Verify all text 4.5:1, UI components 3:1 (use Colour Contrast Analyser tool)
6. **Forms audit**: Submit empty forms, verify errors; verify labels, suggestions, confirmation
