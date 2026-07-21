---
name: brand-guidelines
description: Brand architecture, identity system design, logo system, color palette with accessibility validation, typography hierarchy, iconography, imagery, motion design, brand-in-product expression, and brand governance.
author: Sandeep Kumar Penchala
type: design
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - brand-guidelines
token_budget: 4000
output:
  type: "code"
  path_hint: "./"
---
# Brand Guidelines

Design, document, and enforce a comprehensive brand identity system. This skill covers the full brand design lifecycle: brand architecture and strategy, logo systems with clear space and minimum size rules, color palette creation with accessibility validation, typographic hierarchy, iconography standards, imagery and illustration direction, motion design tokens, brand expression within digital product UI, and governance processes for brand consistency at scale.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Creating a brand identity system for a new company, product, or sub-brand
- Auditing and evolving an existing brand for consistency and accessibility
- Designing a logo system: primary, secondary, icon-only, wordmark, responsive variants
- Building a color palette with semantic colors, dark mode, and WCAG accessibility validation
- Defining typography hierarchy with usage rules: display, heading, body, caption, overline
- Establishing iconography, illustration, and imagery standards
- Creating motion design tokens: timing scales, easing curves, animation principles
- Integrating brand expression into product UI without compromising usability
- Setting up brand governance: review processes, asset distribution, violation handling

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Brand Architecture Model
```
                     ┌──────────────────────────┐
                     │ START: Brand architecture│
                     │ model?                   │
                     └───────────┬──────────────┘
                                 │
              ┌──────────────────▼──────────────────┐
              │ Are the sub-brands/products         │
              │ stronger than the parent brand?     │
              └────┬────────────────────┬───────────┘
                   │ YES                │ NO
                   ▼                    ▼
        ┌──────────────────┐  ┌──────────────────────┐
        │ House of Brands: │  │ Do products share    │
        │ Independent      │  │ the same brand       │
        │ identities (P&G, │  │ promise and audience?│
        │ Unilever).       │  └──┬───────────────┬───┘
        └──────────────────┘     │ YES           │ NO
                                 ▼               ▼
                          ┌────────────┐  ┌──────────────┐
                          │ Branded    │  │ Endorsed or  │
                          │ House:     │  │ Hybrid:      │
                          │ One master │  │ Parent brand │
                          │ brand      │  │ endorsement  │
                          │ (Google,   │  │ (Nest by     │
                          │ Apple)     │  │ Google)      │
                          └────────────┘  └──────────────┘
```
**When Branded House:** Single strong master brand. Products are features/verticals of one promise. Marketing efficiency through unified awareness.  
**When House of Brands:** Acquired companies with existing equity. Targeting different audiences with conflicting brand promises. Risk isolation between brands.

### Logo System Complexity
```
                     ┌──────────────────────────────┐
                     │ START: Logo variants needed? │
                     └─────────────┬────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Logo needs to work in favicon (16×16),  │
              │ app icon (1024×1024), and billboard?   │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ Full system:     │    │ Single use-case?     │
        │ Primary + Icon-  │    │ Primary + Stacked   │
        │ only + Wordmark  │    │ variant only.       │
        │ + Responsive     │    │ Skip responsive.    │
        │ variants.        │    └──────────────────────┘
        └──────────────────┘
```
**When full system needed:** Multi-platform product (web, iOS, Android, print). Logo appears at extreme sizes. Brand used by external partners.  
**When minimal suffices:** Single-context use (web only). Logo always appears at predictable sizes. Internal or B2B tool with limited brand exposure.

### Color Palette Scope
```
                     ┌──────────────────────────────┐
                     │ START: Palette complexity?   │
                     └─────────────┬────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Product has dark mode, data             │
              │ visualization, or multiple themes?      │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ Full token       │    │ Core palette:        │
        │ system: primary, │    │ Primary, secondary,  │
        │ secondary,       │    │ neutral, semantic    │
        │ neutral, semantic│    │ (error, success,     │
        │ + dark variants  │    │ warning). 12–20      │
        │ + chart palette. │    │ colors total.        │
        │ 30–50 tokens.    │    └──────────────────────┘
        └──────────────────┘
```
**When full token system:** Product UI with light/dark mode. Analytics dashboards with charts. White-label or multi-tenant theming requirements.  
**When core palette:** Marketing site + simple app. Light mode only. No data visualization beyond status indicators. Fast time to launch.

### Typography Hierarchy Depth
```
                     ┌──────────────────────────────┐
                     │ START: Type scale depth?     │
                     └─────────────┬────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Product has long-form content,          │
              │ documentation, or articles?             │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ Full scale:      │    │ Compact scale:       │
        │ Display, H1–H4,  │    │ H1–H3, Body,        │
        │ Body Large, Body,│    │ Caption, Overline.   │
        │ Body Small,      │    │ 6–8 sizes. UI-       │
        │ Caption, Overline│    │ focused.             │
        │ + Blockquote.    │    └──────────────────────┘
        │ 10–14 sizes.     │
        └──────────────────┘
```
**When full scale:** Blog, documentation, marketing site with long-form reading. Multiple content types (articles, case studies, legal). Readability-critical.  
**When compact scale:** Dashboard, admin panel, B2B tool. Primarily UI components. Short text mostly. Consistency over typographic expression.

### Governance Model
```
                     ┌──────────────────────────────┐
                     │ START: Governance approach?  │
                     └─────────────┬────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Brand assets used by external partners, │
              │ agencies, or > 10 internal creators?    │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ Full governance: │    │ Light governance:    │
        │ Self-serve portal│    │ Shared Figma +       │
        │ + review process │    │ design token repo.   │
        │ + asset CDN +    │    │ PR-based review.     │
        │ violation tiers. │    └──────────────────────┘
        └──────────────────┘
```
**When full governance:** Co-branding with partners. Multiple agencies creating assets. Brand used in 20+ countries. Enterprise with legal/compliance requirements.  
**When light governance:** Single design team. Assets consumed only by internal engineering. No external co-branding. Brand changes < quarterly.

## Core Workflow
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


**What good looks like:** Brand guidelines document covering logo usage, color palette (with accessibility contrast ratios), typography scale, tone of voice, and example applications. Design token file (JSON/TS) matches the guidelines exactly. Component library follows every rule in the guidelines.

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
## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Brand guidelines are useless if nobody uses them. Coordination with design, engineering, and marketing ensures the brand is applied consistently — not just in Figma, but in production code, marketing materials, and partner content.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **UI/UX Designer** | Component design, design system creation, product UI | Design tokens (colors, spacing, typography, motion), component theming, dark mode variants |
| **Frontend Developer** | Design token implementation, component library, CSS architecture | Token export format (JSON, CSS custom properties), naming conventions, breakpoints, implementation constraints |
| **Marketing Lead** | Campaign assets, website, social media, events | Brand assets (logos, fonts, colors), templates, tone of voice, usage guidelines |
| **Accessibility Auditor** | Color palette validation, typography review, motion compliance | Contrast ratios, font size minimums, prefers-reduced-motion, focus indicators |
| **Documentation Engineer** | Brand docs site, design system documentation | Brand story, visual examples, usage guides, changelog format |
| **Content Designer / Tech Writer** | Tone of voice, messaging, content style guide | Brand voice attributes, messaging frameworks, terminology guidelines |
| **Growth Engineer** | Landing pages, email templates, A/B test variants | Brand-compliant templates, asset optimization, performance constraints |
| **Sales / Partnerships** | Sales decks, co-branded materials, partner kits | Approved assets, co-branding rules, logo usage, partner templates |
| **Product Manager** | Feature branding, product naming, in-product messaging | Naming conventions, brand hierarchy, tone consistency, visual alignment |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Rebrand or major brand refresh | All functional leads, Marketing, CEO | Coordinated rollout across all touchpoints, asset migration, external communications |
| Design token breaking change | UI/UX Designer, Frontend Lead | Component regression risk, migration plan, deprecation timeline |
| New sub-brand or product brand created | Product Manager, Marketing, Sales | Brand architecture update, naming guidelines, visual system extension |
| Brand violation in production (logo, color, typography) | Frontend Lead, Product Manager, Marketing | Fix prioritization, root cause (missing token, hardcoded value), prevention |
| Accessibility issue found in brand elements | Accessibility Auditor, UI/UX Designer | Contrast adjustment, typography change, motion compliance fix |
| Brand asset request from external partner | Legal, Partnerships, Marketing | Usage approval, co-branding rules, license terms |
| Brand guideline version published | All consumers (via changelog + notification) | What changed, what's deprecated, migration guide, effective date |

### Escalation Path

```
Brand integrity at risk (unauthorized sub-brand, major public misuse, trademark violation)
  └── Brand Lead + Legal + Marketing Lead + CEO. Cease-and-desist if external. Fix within 24 hours if internal.

Design system conflict (brand token change breaks 10+ components)
  └── UI/UX Designer + Frontend Lead + Brand Lead. Impact assessment, migration plan, staged rollout.

Minor brand drift (wrong shade, inconsistent spacing, outdated logo in one location)
  └── Direct fix by team that owns the asset. Brand Lead informed. No escalation needed.
```

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Tokenize everything:** Colors, spacing, typography, motion — every design decision becomes a named token in a single source of truth (design-tokens.json).
- **Test at extremes:** Your color palette works on white. Does it work on brand-colored backgrounds? In dark mode? At 400% zoom? With color blindness simulation?
- **Design for non-designers:** Templates for presentations, documents, social media. If marketers don't have a template, they'll invent their own (wrong) brand.
- **Show, don't just tell:** Every guideline needs a visual example. ✅ Do this / ❌ Not this. Words without images will be misinterpreted.
- **Brand evolves, guidelines don't drift:** 90% of the brand is stable. The 10% that changes (new illustration style, new social template) is added without removing the old — archive old, mark as deprecated.
- **Accessibility IS brand:** An inaccessible brand is a broken brand. Contrast, legible typography, motion respect — these are brand quality measures, not compliance burdens.

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Brand = a logo + 2-3 colors + 1 font. No guidelines document. "Brand identity" lives in your head and the app itself.
- **What to skip**: Brand guidelines document. Design tokens. Brand architecture model. Motion guidelines. Icon sets. Brand governance process.
- **Coordination**: You design everything. Consistency is natural.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Simple brand guidelines (1-page PDF or Figma file). Logo variants (primary, icon-only). Color palette (4-6 colors). Typography (1-2 fonts with hierarchy). Basic do/don't examples. Assets shared via Google Drive or Figma.
- **What to skip**: Full brand architecture model. Design tokens. Motion guidelines beyond "keep it simple." Illustration system. Brand governance committee.
- **Coordination**: Designer owns brand. New assets reviewed by designer before use. Quarterly brand audit (30 min).

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Comprehensive brand guidelines portal. Full brand architecture model. Design tokens (colors, typography, spacing, elevation). Semantic color tokens (primary, semantic, neutral). Dark mode palette. Icon set with consistent style. Illustration direction. Motion tokens. Brand governance with review process. Asset distribution portal (Figma library + CDN).
- **What to skip**: Multi-brand architecture (unless acquired). Brand valuation study. Global brand compliance audits.
- **Coordination**: Brand designer reviews all public-facing assets. Monthly brand council. Quarterly brand refresh consideration.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Multi-brand architecture (Branded House / House of Brands). Design token pipeline (Figma → Style Dictionary → code). Global brand compliance. Brand valuation tracking. Brand guidelines for 10+ markets/languages. Co-branding and partnership guidelines. M&A brand integration playbook. Brand governance committee with cross-functional membership. Legal trademark management.
- **What's full production**: Brand center of excellence. Annual brand audit. Brand training for all marketers and designers. Brand compliance scoring. Automated design token distribution.
- **Coordination**: Monthly brand council. Quarterly brand compliance review. Annual brand strategy offsite. Legal review for trademark use.

### Transition Triggers
- **Solo → Small**: Second designer or external agency needs brand direction. Inconsistent brand in marketing materials.
- **Small → Medium**: Multiple products or sub-brands. Design system needs consistent tokens. >10 people creating branded content.
- **Medium → Enterprise**: International expansion with localization. M&A activity. >50 people creating branded content across markets.


### Cross-skills Integration
The preceding skill in the chain documents output format requirements. The following skill in the chain expects that format. Run them sequentially:
```bash
#[previous-skill] && #[this-skill] && #[next-skill]
```
Document the output contract explicitly so consuming skills know what to expect.

## Sub-Skills
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


### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Design doesn't match brand | Missing design token reference | Define all colors, spacing, typography as tokens before starting any screen. Style guide → component library. |
| Accessibility gap found in audit | Not tested during design phase | Test with axe-core during design, not after. Color contrast and heading hierarchy are non-negotiable from the start. |
| Dev implementation differs from design | No handoff spec beyond mockups | Annotate every element: breakpoints, hover/focus/active states, animation timing, empty states. Zeplin/Figma Dev Mode. |
| Dark mode breaks screens | Only tested in light mode | Design dark mode in parallel. Every screen must support both from day one. |
| Component doesn't scale to content | Designed with one data example | Test components with minimum, maximum, and empty content. Real user data, not Lorem Ipsum. |
| Platform inconsistency (iOS vs Android) | No platform-specific adaptation | iOS uses tab bar (bottom); Android uses navigation bar (top). Design per platform, not pixel-perfect identical. |
| Motion causes dizziness | Uncontrolled animation | Respect `prefers-reduced-motion`. Use `motion-safe`/`motion-reduce` for all animations. |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Brand architecture model documented (Branded House / House of Brands / Endorsed / Hybrid)
- [ ] **[S2]**  Logo system: primary, stacked, icon-only, wordmark, responsive variants all provided in SVG and PNG
- [ ] **[S3]**  Clear space rule defined (equal to icon height) and enforced with visual diagrams
- [ ] **[S4]**  Color palette with semantic tokens documented: primary, secondary, accent, neutral, semantic, dark mode
- [ ] **[S5]**  All text-on-background color combinations validated for WCAG 2.2 AA (4.5:1 normal, 3:1 large text)
- [ ] **[S6]**  Typography hierarchy: display, h1-h4, body-lg/body/body-sm, caption, overline — with sizes, weights, and usage rules
- [ ] **[S7]**  Icon set consistent in style, stroke weight, corner radius, and grid alignment (24×24 base)
- [ ] **[S8]**  Imagery/illustration direction documented with style keywords and composition rules
- [ ] **[S9]**  Motion tokens defined: durations (instant/fast/base/slow), easings (default/enter/exit), reduced-motion respect
- [ ] **[S10]**  Brand governance: review process, violation tiers, asset distribution portal, versioned guidelines

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Design Tokens Format](https://design-tokens.github.io/community-group/format/) — W3C Community Group
- [Stripe Brand Guidelines](https://stripe.com/brand) — Reference implementation of comprehensive brand portal
- [Material Design 3 — Color System](https://m3.material.io/styles/color) — HCT color space for accessibility
- [Leonardo — Accessible Color Generator](https://leonardocolor.io/) — Adobe
- [Contrast — WCAG Contrast Checker](https://usecontrast.com/)
- [Practical Typography](https://practicaltypography.com/) — Matthew Butterick
- [Brand New](https://www.underconsideration.com/brandnew/) — Brand identity reviews
- [The Brand Gap](https://www.amazon.com/Brand-Gap-Revised/dp/0321348109) — Marty Neumeier
- [Atomic Design](https://atomicdesign.bradfrost.com/) — Brad Frost (design systems methodology)
