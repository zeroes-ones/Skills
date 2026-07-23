# Core Workflow — Full Implementation

<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Brand Architecture & Strategy

#### 1.1 Brand Architecture Models

| Model | Description | When to Use | Example |
|-------|-------------|-------------|---------|
| **Branded House** | One master brand, all products share identity | Strong single brand, cohesive experience | Google (everything is Google), Apple |
| **House of Brands** | Independent brands under a parent company | Diverse products, different audiences | P&G (Tide, Pampers, Gillette), Unilever |
| **Endorsed** | Sub-brands with own identity + parent endorsement | Related but distinct products | Marriott (Courtyard by Marriott, Residence Inn by Marriott) |
| **Hybrid** | Mix of endorsed and independent | Complex portfolios | Microsoft (Windows, Xbox, LinkedIn — each distinct) |

Decision framework:
```
┌─ Single audience, single promise? ───────► Branded House
│
├─ Multiple distinct audiences, different promises? ──► House of Brands
│
└─ Related products, shared trust? ───────► Endorsed Brand Architecture
```


**What good looks like:** Brand guidelines document that a designer outside your company can pick up and produce an on-brand screen within an hour. Design token file (JSON/TS/CSS custom properties) matches the guidelines byte-for-byte — they're the same truth, not two documents that contradict each other. Every component pattern has examples of correct use, incorrect use, and edge cases.
#### 1.2 Brand Strategy Foundation

Before designing, document:

1. **Brand Promise:** What does the brand commit to delivering? One sentence.
   - *Example: "Stripe makes payments infrastructure invisible — so businesses can focus on building."*

2. **Brand Personality:** 3-5 adjectives describing the brand as a person.
   - *Example: "Stripe is: technical, precise, trustworthy, empowering, global."*

3. **Target Audience:** 2-3 primary audience personas with needs and context.

4. **Competitive Landscape:** 3-5 competitors. How does this brand differentiate visually and verbally?

5. **Brand Voice:** Tone attributes for copy and content.
   - *Example: "Stripe is: clear over clever, direct over decorative, helpful over hype."*

### Phase 2 (~30 min): Logo System

#### 2.1 Logo Variants

Every brand needs a logo system, not just one logo. Define all variants:

| Variant | Description | Primary Use |
|---------|-------------|-------------|
| **Primary / Horizontal** | Full logo (icon + wordmark, horizontal layout) | Website header, marketing, default usage |
| **Stacked / Vertical** | Full logo (icon above wordmark) | Square spaces, social media avatars, app icons |
| **Icon-only / Mark** | Icon/symbol without wordmark | App icons, favicons, social media avatars, watermarks |
| **Wordmark** | Text only without icon | Footer, legal, co-branded spaces |
| **Responsive / Compact** | Simplified for small sizes | Mobile headers, browser tabs (< 32px), email signatures |

#### 2.2 Clear Space & Minimum Size

```
Clear Space Rule:
┌─────────────────────────────────────────┐
│                                         │
│    ┌──────────────────────────┐         │
│    │                          │         │
│    │        LOGO HERE         │  ← x    │
│    │                          │         │
│    └──────────────────────────┘         │
│    ←────── x ──────►                    │
│                                         │
│  x = height of the logo mark/icon       │
│  Minimum clear space on ALL sides = x   │
└─────────────────────────────────────────┘
```

**Clear space:** Equal to the height of the icon/mark on all four sides. Nothing enters this zone (text, other logos, UI elements, image edges).

**Minimum sizes:**
- Primary logo: Min 120px wide (digital), 40mm wide (print).
- Icon-only mark: Min 32px (digital), 16px for favicon.
- Wordmark: Min 100px wide for legibility.

#### 2.3 Logo Usage Rules

```
✅ DO:
- Use provided artwork files — never recreate or modify.
- Maintain aspect ratio — never stretch or squash.
- Use on backgrounds with sufficient contrast.

❌ DON'T:
- Recolor the logo (except approved monochrome variants).
- Apply effects: drop shadows, gradients, outlines, rotation.
- Place on busy backgrounds where legibility is compromised.
- Use low-resolution or unapproved file formats.
- Recreate the logo from memory — always use source files.
```

#### 2.4 File Formats & Delivery

| Format | Use | Notes |
|--------|-----|-------|
| `.svg` | Web, digital products | Primary format. Scalable, lightweight. Ensure text is outlined or fonts are embedded. |
| `.png` (transparent) | Presentations, email signatures, Office docs | Provide at 1x, 2x, 3x (72dpi). |
| `.eps` / `.ai` | Print, merchandise, vendor use | Vector source files. CMYK color space option. |
| `.ico` | Favicon | Multi-size .ico (16, 32, 48px). |
| `.pdf` | Print proofing | Press-ready, CMYK, embedded fonts. |

---
### Phase 3 (~20 min): Color Palette

#### 3.1 Palette Architecture

Build a systematic palette — not arbitrary color picking:

```
Palette Structure:

Primary           → Brand-defining color(s). Used in logo, key CTAs, headers.
Secondary         → Complementary colors. Cards, illustrations, data viz.
Accent            → High-emphasis highlights. Sales badges, focus states.
Neutral           → Gray scale for UI: backgrounds, borders, text.
Semantic          → Functional meaning colors:
  Success (green) → Confirmation, completion, positive metrics
  Warning (amber) → Caution, pending, attention needed
  Error (red)     → Destruction, critical alerts, validation errors
  Info (blue)     → Neutral information, tips, status updates
```

#### 3.2 Color Token Naming Convention

**Wrong:** `blue-500`, `#2563EB`, `primary`
**Right:** Semantic tokens that convey intent.

```
// Design tokens — NOT what the color IS, but what it MEANS
--color-background-primary
--color-background-secondary
--color-background-brand
--color-text-primary
--color-text-secondary
--color-text-link
--color-text-on-brand
--color-border-default
--color-border-focus
--color-icon-primary
--color-icon-secondary
--color-surface-success
--color-text-success
--color-surface-error
--color-text-error
```

#### 3.3 Accessibility Validation

Every color pairing must pass WCAG 2.2 AA contrast ratios:

| Text Size | AA Minimum | AAA Minimum |
|-----------|------------|--------------|
| Normal text (< 18pt / 24px) | 4.5:1 | 7:1 |
| Large text (≥ 18pt bold / 24px) | 3:1 | 4.5:1 |
| UI components (borders, icons) | 3:1 | N/A |

**Validation workflow:**
1. Check all text-on-background combinations.
2. Check all icon-on-background combinations.
3. Check focus indicators against adjacent backgrounds.
4. Check disabled states — they're exempt from contrast requirements but must be supplemented with non-color cues (reduced opacity + icon + text change).
5. Check link text against body text (links must be differentiable by more than color — underline or icon).

**Tooling:**
```css
/* Tailwind plugin — valid color palette checker */
/* Use https://colorbox.io/ or Leonardo for accessible color generation */
/* Validate with: https://webaim.org/resources/contrastchecker/ */
```

#### 3.4 Dark Mode Palette

Dark mode is NOT simply inverting colors. Key principles:

```
Light Mode              →    Dark Mode
─────────────────────────────────────────────
White background        →    Dark gray (#121212 or #1E1E1E)
Dark text (#1A1A1A)     →    Light text (#E5E5E5) — NOT pure white (#FFFFFF) — reduces eye strain
Gray-100 (#F3F4F6)      →    Gray-900 (#111827)
Gray-900 (#111827)      →    Gray-100 (#F3F4F6)
Brand color             →    Desaturated + lightened by 10-15% — saturated colors vibrate on dark backgrounds
Shadows                 →    Shadows don't work on dark. Use borders or elevated surface colors instead.

// Dark mode surface elevation (lighter = higher)
--surface-ground: #121212       // Base background
--surface-elevated: #1E1E1E     // Cards, modals
--surface-overlay: #2C2C2C      // Dropdowns, tooltips
--surface-highlight: #383838    // Hover states
```

---
### Phase 4 (~15 min): Typography Hierarchy

#### 4.1 Type Scale

Define a type scale with specific usage rules. Use a modular scale (1.25, 1.333, or 1.5 ratio).

```
Role        | Size/Line    | Weight | Usage
────────────┼──────────────┼────────┼──────────────────────────
Display     | 48/56–64/72  | 700    | Marketing hero, landing pages. ONE per page.
H1          | 36/44        | 600    | Page titles, section heroes
H2          | 28/36        | 600    | Card headers, subsection titles
H3          | 22/30        | 600    | Widget headers, feature titles
H4          | 18/26        | 600    | In-card subheaders
Body Lg     | 18/28        | 400    | Lead paragraphs, introductory text
Body        | 16/24        | 400    | Primary reading text
Body Sm     | 14/20        | 400    | Secondary text, metadata, captions
Caption     | 12/16        | 400    | Timestamps, legal, footnotes
Overline    | 12/16        | 600    | Section labels, category tags (uppercase + letter-spacing: 0.05em)
```

#### 4.2 Font Selection Rules

```
Display font (optional): For marketing headlines, hero, brand moments.
  - Max 1 display font. Never use for body text.
  - Must pair well with body font.

Body font: For all reading text, UI, forms, navigation.
  - Max 1 body font family.
  - Must have: Regular (400), Medium (500), SemiBold (600), Bold (700).
  - Must have: true italics (not faux/synthesized).

Monospace font: For code, data, technical content.
  - 1 monospace family. Use for inline code, code blocks, data tables.

Total: Maximum 2 font families per brand (display + body, or body + mono).
      3 only if monospace is functionally required.

Web font loading strategy:
  - Subset to needed characters (Latin + target languages).
  - Use font-display: swap (text visible during load).
  - Preload critical font files with <link rel="preload" as="font">.
  - Self-host fonts — avoid Google Fonts CDN (GDPR, performance).
```

#### 4.3 Usage Rules

```
✅ DO:
- Use the type scale — never custom font sizes outside it.
- Limit line length to 45-75 characters for body text.
- Use at most 3 levels of heading nesting (h2 → h3 → h4).

❌ DON'T:
- Use display font for body text.
- Use bold for emphasis — use Medium (500) for inline emphasis; reserve Bold for headings.
- Use underline for non-link text (confuses users).
- Use all-caps for sentences — only for overlines, labels, buttons (max 3 words).
```

---
### Phase 5 (~25 min): Iconography

#### 5.1 Style Direction

| Style | Characteristics | Best For |
|-------|----------------|----------|
| **Outline / Line** | Thin stroke (1.5-2px), open shapes, modern | SaaS products, dashboards, developer tools |
| **Filled / Solid** | Heavy visual weight, good at small sizes | Mobile apps, consumer products, tactile UIs |
| **Duotone** | Two-color, depth via overlays | Marketing, feature illustrations |
| **Glyph / Minimal** | Simple shapes, maximum clarity | Navigation, toolbars, System UIs |

#### 5.2 Sizing & Grid

```
Icon grid: 24×24px base grid with 2px padding (content area: 20×20px)

Sizes:
  sm (16×16)   → Tight spaces: inline with text, table cells
  md (24×24)   → Default: buttons, navigation, form fields
  lg (32×32)   → Feature icons, empty states
  xl (48×48)   → Hero icons, marketing spots

Stroke weight:
  Outline icons: 1.5px–2px stroke at 24px.
  Scale stroke proportionally at other sizes.

Design rules:
  □ All icons from a set share consistent stroke weight.
  □ Corners: rounded (2px radius) or sharp (0px) — pick ONE.
  □ Line endings: round cap or square cap — pick ONE.
  □ Perspective: flat (2D) or isometric — pick ONE.
  □ Every icon has a unique, unambiguous meaning.
  □ Icons at ≤ 16px may need simplified versions.
```

#### 5.3 Icon Accessibility

```html
<!-- Decorative icon (no meaning beyond visual decoration) -->
<svg aria-hidden="true" focusable="false">...</svg>

<!-- Informative icon (conveys meaning, e.g., status indicator) -->
<svg role="img" aria-label="Order confirmed">...</svg>

<!-- Icon-only button -->
<button aria-label="Search">
  <svg aria-hidden="true" focusable="false">...</svg>
</button>

<!-- Icon + text — icon is decorative -->
<button>
  <svg aria-hidden="true" focusable="false">...</svg>
  Search
</button>
```

---
### Phase 6 (~25 min): Imagery

#### 6.1 Photography Direction

```
Style keywords (pick 3-4 for the brand):
  □ Natural light / Studio light / Dramatic shadow
  □ Warm color grade / Cool color grade / Desaturated / Vibrant
  □ Shallow depth-of-field (blurred background) / Deep focus (everything sharp)
  □ Candid / Posed / Abstract / Documentary
  □ People-focused / Product-focused / Environment-focused

Composition rules:
  □ Rule of thirds for hero images.
  □ Subject off-center facing INTO the content.
  □ Consistent aspect ratios: 16:9 (hero), 4:3 (cards), 1:1 (avatars), 3:2 (blog).
```

#### 6.2 Illustration Style

```
Style parameters:
  □ Line art / Flat vector / 3D render / Hand-drawn / Collage
  □ Limited palette (use brand colors) / Full color
  □ Geometric / Organic / Abstract
  □ Humans represented? If so, skin tone range, body diversity, accessibility devices included.

Usage: Empty states, onboarding flows, error pages, feature spot illustrations, hero graphics.
```

#### 6.3 Image Accessibility

```
□ Every <img> has alt text.
  - Informative: "Woman using Stripe Dashboard to review revenue analytics"
  - Decorative: alt="" (empty string — screen readers skip)
□ Complex images/charts have long descriptions (aria-describedby or linked page).
□ No text embedded in images (SVG with real text preferred).
□ SVG illustrations have <title> and <desc> elements.
```

---
### Phase 7 (~25 min): Motion Design

#### 7.1 Motion Tokens

```css
/* Duration tokens */
--motion-duration-instant: 0ms;       /* No animation — color changes, opacity toggle */
--motion-duration-fast: 150ms;        /* Micro-interactions: hover, toggle, tooltip */
--motion-duration-base: 250ms;        /* Standard transitions: open/close, navigation */
--motion-duration-slow: 400ms;        /* Emphasis: page transitions, modal open */
--motion-duration-gentle: 700ms;      /* Atmospheric: background animations, hero */

/* Easing tokens */
--motion-ease-default: cubic-bezier(0.4, 0, 0.2, 1);        /* Standard easing — most common */
--motion-ease-enter: cubic-bezier(0, 0, 0.2, 1);            /* Deceleration — elements appearing */
--motion-ease-exit: cubic-bezier(0.4, 0, 1, 1);             /* Acceleration — elements disappearing */
--motion-ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);    /* Overshoot — celebratory moments */
```

#### 7.2 Animation Principles

```
1. Purposeful — every animation communicates something.
   Bad: Spinning logo loader — decorative, no purpose.
   Good: Progress bar that fills — communicates wait time.

2. Fast — users should never wait for animation.
   Enter: 150-250ms. Exit: 100-200ms. Anything > 400ms feels sluggish.

3. Contextual — animation type matches action.
   Expand/collapse: scale + opacity. Navigate: slide directionally.
   Add to cart: move from trigger to cart icon.

4. Performant — only animate transform and opacity.
   GPU-accelerated: transform, opacity.
   CPU (avoid for animation): width, height, top, left, color, box-shadow.

5. Reduced motion — respect user preference.
   @media (prefers-reduced-motion: reduce) {
     *, *::before, *::after {
       animation-duration: 0.01ms !important;
       transition-duration: 0.01ms !important;
     }
   }
```

#### 6.3 Brand Motion Identity

```
Brand entry: How the brand logo appears on first load.
  - Logo fades in from center (gentle, 400ms).
  - No spinning, bouncing, or dramatic reveals.

Page transitions: Between marketing pages or app views.
  - Fade + subtle upward slide (15px), 250ms.

Micro-interactions: Button hover, toggle state, notification badge.
  - Subtle scale (1.02) on hover, 150ms.
  - Badge: scale from 0 to 1 with slight overshoot (entrance only).

Brand moments: Empty states, success states, error states.
  - Illustration fades in + drifts upward 20px, 400ms.
  - Error: subtle horizontal shake (3px, 2 oscillations, 200ms).
```

---
### Phase 8 (~30 min): Brand in Product

#### 8.1 Brand Expression vs Usability

The hardest challenge: brand personality must not compromise product usability.

| Element | Brand Expression | Usability Constraint |
|---------|-----------------|---------------------|
| **Color** | Brand primary for CTAs | Must pass 4.5:1 contrast on white AND on dark backgrounds |
| **Typography** | Display font for headers | Never for body text, forms, or navigation — use body font |
| **Iconography** | Brand-specific style | Must be recognizable at 16px; meanings must match platform conventions |
| **Animation** | Brand motion feel | Must complete in < 400ms; must respect `prefers-reduced-motion` |
| **Illustration** | Brand style in empty states | Must not distract from actionable content |

**The rule:** Brand expresses in moments (landing pages, empty states, loading screens, success pages). Brand recedes during tasks (forms, data tables, settings, checkout).

#### 8.2 Component Theming

```css
/* Design tokens bridge brand to product */
--button-primary-bg: var(--color-brand-600);
--button-primary-text: var(--color-text-on-brand);
--button-primary-hover: var(--color-brand-700);
--button-radius: 8px;                    /* Brand expression: rounded vs sharp */

--input-border: var(--color-border-default);
--input-focus-ring: var(--color-brand-500);
--input-radius: 6px;

/* Component density — brand personality */
/* Playful brand → more padding, rounded corners */
/* Professional/technical brand → tighter, slightly sharper */
```

---
### Phase 9 (~20 min): Brand Governance

#### 9.1 Review Process

```
Request Workflow:
1. Requester submits request via brand portal/form.
   - What: Logo, color, font, template
   - Use: Where/how will it be used?
   - Deadline: When is it needed?

2. Brand team reviews within 2 business days.
   Past: → Approve as-is
        → Approve with modifications (provide corrected assets)
        → Reject with explanation and suggested alternative

3. Approved assets delivered via brand portal (CDN link) or shared drive.

4. Asset usage tracked. Follow-up audit at 90 days for external-facing uses.
```

#### 9.2 Violation Handling

```
Tier 1 (Minor): Wrong color shade, incorrect clear space.
  → Email notification with correction. 1 week to fix.

Tier 2 (Moderate): Stretched logo, unapproved color variant, wrong typography.
  → Email + meeting request. 48 hours to fix.

Tier 3 (Severe): Altered logo, offensive use, competitor association.
  → Escalate to legal. Immediate takedown if public.

Repeat violations → Mandatory brand training for team.
```

#### 9.3 Asset Distribution

```
Brand portal structure:
/
├── logos/
│   ├── primary/
│   │   ├── horizontal/
│   │   └── stacked/
│   ├── icon-only/
│   ├── wordmark/
│   └── archive/          (Previous logo versions — do not use)
├── colors/
│   ├── palette-guide.pdf
│   ├── design-tokens.json
│   └── tailwind-config.js
├── typography/
│   ├── font-files/       (Licensed .woff2 files)
│   └── type-scale.pdf
├── iconography/
│   ├── icon-set.svg
│   └── icon-guidelines.pdf
├── templates/
│   ├── presentation.potx
│   ├── document.docx
│   └── email-signature.html
├── photography/
│   └── licensed-library/ (Watermarked previews; full-res on request)
└── brand-guidelines.pdf  (This document — always the latest version)
```

#### 9.4 Version Control

```
Brand guidelines are versioned:
  v2.3 — 2024-09-15 — Added TikTok brand asset, updated color contrast values
  v2.2 — 2024-06-01 — New illustration style approved, deprecated old illustrations
  v2.1 — 2024-03-10 — Added dark mode palette, updated minimum logo size
  v2.0 — 2024-01-05 — Major rebrand: new logo, new color system, new typography

Always reference the latest version. Archive, never delete old versions.
```

---
