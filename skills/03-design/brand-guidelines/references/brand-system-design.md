---
author: Sandeep Kumar Penchala
type: reference
domain: brand
version: "1.0"
last_updated: 2026-07-21
---

# Brand System Design

A complete reference for building and governing brand identity systems. Covers brand architecture, visual identity elements, voice and tone, application across surfaces, and governance models.

---

## Brand Architecture

The structural relationship between a parent brand and its sub-brands, products, or services.

### Brand Architecture Models

| Model | Structure | When to Use | Examples |
|-------|-----------|-------------|----------|
| **Branded House** | Master brand dominates; all products carry the master brand name | Cohesive portfolio, strong parent equity, efficiency in marketing spend | Google (Google Maps, Google Drive, Google Docs), FedEx (FedEx Express, FedEx Ground) |
| **House of Brands** | Each product has its own brand identity; parent brand is invisible to consumers | Diverse products targeting different segments, acquisitions with strong standalone equity, risk isolation | P&G (Tide, Pampers, Gillette), Unilever (Dove, Lipton, Ben & Jerry's) |
| **Endorsed** | Sub-brands have their own identity but are visibly linked to the parent | Leverages parent credibility while allowing sub-brand differentiation | Marriott (Courtyard by Marriott, Residence Inn by Marriott), Nestlé (KitKat, Nescafé) |
| **Hybrid** | Mix of the above across the portfolio | Large conglomerates with varied history | Microsoft (Windows, Xbox — branded house; LinkedIn, GitHub — endorsed/house of brands) |

### Decision Framework

Choose your architecture model based on:
1. **Brand equity**: Is the parent brand strong enough to lift sub-brands?
2. **Target audience overlap**: Do products serve the same or different audiences?
3. **Price/quality tiering**: Do products occupy different market positions?
4. **Acquisition strategy**: Are you buying brands with existing equity?
5. **Risk management**: Does one product's failure risk contaminating others?
6. **Marketing budget**: Can you afford to build multiple independent brands?

### Architecture Documentation

For each brand/sub-brand in the system, document:
- Brand name and logo lockup
- Relationship to parent (if any)
- Target audience and positioning
- Visual differentiators (what makes this brand visually distinct)
- Shared elements (what must remain consistent across brands)
- Governance owner (who approves changes to this brand's identity)

---

## Visual Identity Elements

### 1. Logo System

#### Logo Variants

| Variant | Usage | Min Size (Digital) | Min Size (Print) | Clear Space |
|---------|-------|--------------------|--------------------|-------------|
| **Primary logo** (horizontal lockup) | Default. Website header, print materials, social profile | 120px wide | 1 inch wide | Height of the logo mark on all sides |
| **Vertical/stacked lockup** | Square-format spaces: app icons, social avatars, swag | 60px wide | 0.5 inch wide | 50% of logo height |
| **Icon-only / mark** | Favicons, app icons, watermarks, tight spaces | 16px (favicon: 32px) | 0.25 inch | 25% of icon size |
| **Wordmark only** | When icon is redundant, invoices, legal documents | 100px wide | 0.75 inch | 50% of wordmark height |
| **Monochrome** (single color) | Single-color printing, embroidery, engraving | Same as primary | Same as primary | Same as primary |
| **Reversed** (light on dark) | Dark backgrounds, photography overlays | Same as primary | Same as primary | Same as primary |

#### Logo Construction Rules
- **Minimum clear space**: The area around the logo that must remain free of other elements. Defined relative to the logo mark's height or a typographic element (e.g., x-height of the wordmark).
- **Minimum size**: Smallest dimension the logo can appear while remaining legible. Different for digital (pixels) and print (mm/inches).
- **Prohibited treatments**: Stretching, skewing, rotating, adding effects (drop shadow, glow, gradient unless part of the approved system), low-contrast placement, busy backgrounds, unapproved color variations, placing on brand-colored backgrounds without the reversed variant.
- **File formats**: SVG (primary digital format, infinitely scalable), PNG (fallback, at 1×, 2×, 3× resolutions), PDF/EPS (print, vector), Favicon package (ICO, PNG, SVG, with manifest.json and browserconfig.xml).

#### Logo Do/Don't Examples
- ✅ Use the primary logo on white or light backgrounds
- ✅ Use the reversed logo on dark brand-color backgrounds or dark photography
- ✅ Maintain clear space equal to the logo mark's cap height
- ❌ Do not stretch, skew, or distort proportions
- ❌ Do not recolor the logo (use approved monochrome variant instead)
- ❌ Do not place logo on busy or low-contrast backgrounds
- ❌ Do not add drop shadows, glows, or gradients
- ❌ Do not rotate the logo

---

### 2. Color Palette Architecture

#### Palette Structure

```
Level 1: Brand Colors (the core identity)
  └─ Primary: 1–2 colors that define the brand
  └─ Secondary: 1–3 supporting colors that add depth

Level 2: Functional Colors
  └─ Accent: CTAs, highlights, interactive elements
  └─ Semantic: Success, Error, Warning, Info

Level 3: Neutral Colors
  └─ Neutral warm: Text and backgrounds with warmth
  └─ Neutral cool: Text and backgrounds with coolness
  └─ True gray: Pure grayscale

Level 4: Surface & Elevation
  └─ Surface colors for light mode (layered depth)
  └─ Surface colors for dark mode
```

#### Color Swatch Specification

| Token Name | Hex | RGB | HSL | Pantone | CMYK | WCAG Black Text | WCAG White Text |
|-----------|-----|-----|-----|---------|------|-----------------|-----------------|
| `brand-primary-500` | #0066FF | 0,102,255 | 216°,100%,50% | 2728 C | 100,60,0,0 | FAIL (2.7:1) | PASS (4.5:1 — large text only) |
| `brand-primary-900` | #003399 | 0,51,153 | 220°,100%,30% | 2747 C | 100,67,0,40 | FAIL (2.6:1) | PASS (7.9:1) |
| `neutral-100` | #F5F5F5 | 245,245,245 | 0°,0%,96% | Cool Gray 1 C | 0,0,0,4 | PASS (19.1:1) | FAIL (1.1:1) |
| `neutral-900` | #1A1A1A | 26,26,26 | 0°,0%,10% | Black 6 C | 0,0,0,90 | FAIL (1.1:1) | PASS (14.7:1) |

_Each swatch in the brand palette must have a complete row in this table._

#### Accessibility Requirements for Brand Colors
- The primary brand color must have at least one text-safe pairing documented
- The primary CTA color must support white or dark text at 4.5:1 minimum
- The secondary/accent colors must support text at 4.5:1 or be restricted to non-text use only
- All palette entries must be tested against both white (#FFFFFF) and black (#000000) with documented results

---

### 3. Typography System

#### Typeface Selection

| Role | Typeface | Classification | Weights Available | Usage |
|------|----------|---------------|-------------------|-------|
| **Primary (Display/Heading)** | [Brand Typeface Name] | Sans-serif / Serif | 300, 400, 500, 600, 700, 800 | All headings, hero text, large UI labels |
| **Secondary (Body)** | [Brand Typeface Name] | Sans-serif / Serif | 300, 400, 400i, 500, 600, 600i | Body copy, UI text, forms, captions |
| **Mono** | [Brand Typeface Name] | Monospace | 400, 700 | Code blocks, data displays, technical labels |

#### Type Scale

| Token | Font Size | Line Height | Font Weight | Letter Spacing | Usage |
|-------|-----------|-------------|-------------|----------------|-------|
| `display-2xl` | 72px / 4.5rem | 1.1 (79px) | 700 | -0.02em | Hero headlines (marketing pages only) |
| `display-xl` | 60px / 3.75rem | 1.1 (66px) | 700 | -0.02em | Page titles, landing heroes |
| `display-lg` | 48px / 3rem | 1.1 (53px) | 600 | -0.01em | Major section headings |
| `heading-xl` | 36px / 2.25rem | 1.2 (43px) | 600 | -0.01em | H1 — page headings |
| `heading-lg` | 30px / 1.875rem | 1.25 (38px) | 600 | normal | H2 — section headings |
| `heading-md` | 24px / 1.5rem | 1.3 (31px) | 600 | normal | H3 — subsection headings |
| `heading-sm` | 20px / 1.25rem | 1.3 (26px) | 600 | normal | H4 — card headings |
| `heading-xs` | 16px / 1rem | 1.3 (21px) | 600 | normal | H5 — minor headings |
| `body-xl` | 20px / 1.25rem | 1.5 (30px) | 400 | normal | Large body / lead paragraphs |
| `body-lg` | 18px / 1.125rem | 1.6 (29px) | 400 | normal | Enhanced readability body |
| `body-md` | 16px / 1rem | 1.6 (26px) | 400 | normal | Standard body text |
| `body-sm` | 14px / 0.875rem | 1.5 (21px) | 400 | normal | Secondary body, captions, metadata |
| `body-xs` | 12px / 0.75rem | 1.5 (18px) | 400 | normal | Legal, footnotes, fine print |
| `caption` | 12px / 0.75rem | 1.4 (17px) | 500 | 0.02em | Labels, overlines, small UI text |
| `button` | 16px / 1rem | 1 | 600 | 0.01em | Button text, navigation links |
| `code` | 14px / 0.875rem | 1.5 (21px) | 400 | normal | Inline code, code blocks |

#### Type Scale Ratio
The scale uses a **[Major Third / Perfect Fourth / Golden Ratio]** (choose one) ratio starting from 16px body. All sizes are multiples of 4px for pixel-grid alignment.

#### Font Stack (CSS)
```css
--font-family-display: 'Brand Display', system-ui, -apple-system, 'Segoe UI', sans-serif;
--font-family-body: 'Brand Text', system-ui, -apple-system, 'Segoe UI', sans-serif;
--font-family-mono: 'Brand Mono', 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
```

---

### 4. Spacing & Layout System

#### Spacing Scale (4px base unit)

| Token | Value | Usage |
|-------|-------|-------|
| `space-0` | 0px | No spacing |
| `space-1` | 4px | Inline spacing, icon-to-label gap |
| `space-2` | 8px | Tight padding, option group internal gap |
| `space-3` | 12px | Compact padding, form field gap |
| `space-4` | 16px | **Default** padding/margin baseline |
| `space-5` | 20px | Enhanced spacing between related elements |
| `space-6` | 24px | Section internal spacing |
| `space-8` | 32px | Between card sections |
| `space-10` | 40px | Between major page sections |
| `space-12` | 48px | Section vertical padding |
| `space-16` | 64px | Large section padding, hero spacing |
| `space-20` | 80px | Page-level spacing |
| `space-24` | 96px | Extra-large page spacing |

#### Layout Grid

| Breakpoint | Min Width | Max Width | Columns | Gutter | Margin |
|-----------|-----------|-----------|---------|--------|--------|
| **xs** (mobile) | 320px | 767px | 4 | 16px | 16px |
| **sm** (tablet) | 768px | 1023px | 8 | 24px | 24px |
| **md** (desktop) | 1024px | 1439px | 12 | 24px | 32px |
| **lg** (wide) | 1440px | — | 12 | 32px | auto (max-width: 1280px container) |

---

### 5. Iconography

#### Icon Style Specification

| Attribute | Specification |
|-----------|--------------|
| **Style** | Line (outline) / Filled (solid) / Duotone |
| **Grid size** | 24×24px (primary), 16×16px (small), 20×20px (inline) |
| **Stroke width** | 2px (line style) / n/a (filled style) |
| **Corner radius** | 2px (set), 0px (sharp) — pick one for entire set |
| **ViewBox** | 0 0 24 24 (for 24px grid) |
| **Alignment** | Pixel-snapped (no half-pixel values) |
| **Naming convention** | `icon-{category}-{name}-{variant}` e.g., `icon-action-add-filled` |

#### Icon Categories
- **Action**: add, remove, edit, delete, download, upload, share, bookmark, refresh, settings, search, filter, sort
- **Navigation**: arrow-left, arrow-right, arrow-up, arrow-down, chevron-left, chevron-right, chevron-up, chevron-down, home, menu, close, back
- **Communication**: mail, chat, phone, notification, feedback, help, support
- **Object**: user, group, calendar, clock, document, folder, image, file, link, lock, unlock, tag, star, heart, cart, credit-card
- **Status**: check, check-circle, alert, error, info, warning, progress, loading

#### Icon Usage Rules
- Icons MUST always be accompanied by visible text OR an accessible label (`aria-label` on the icon element)
- Decorative icons ONLY use `aria-hidden="true"` — they should never be interactive
- Icon sizes: 16px for inline text, 20px for compact UI, 24px for standard, 32px+ for large UI
- Do not scale icons to non-standard sizes (use the dedicated size variant instead)

---

### 6. Elevation & Shadow System

Elevation creates the perception of layered depth in the interface.

| Token | Elevation (z-index equivalent) | Shadow Values | Usage |
|-------|-------------------------------|---------------|-------|
| `shadow-none` | 0 | `none` | Flat elements, base background |
| `shadow-xs` | 1 | `0 1px 2px rgba(0,0,0,0.05)` | Subtle raised cards, table rows hover |
| `shadow-sm` | 2 | `0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06)` | Cards, inputs (default state) |
| `shadow-md` | 3 | `0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.05)` | Dropdowns, tooltips, elevated cards |
| `shadow-lg` | 4 | `0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.05)` | Modals, dialogs |
| `shadow-xl` | 5 | `0 20px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.05)` | Full-screen overlays, drawers |
| `shadow-2xl` | 6 | `0 25px 50px -12px rgba(0,0,0,0.25)` | Top-level modals, notification overlays |

#### Dark Mode Elevation
In dark mode, shadows are less visible. Use **lightening of the surface color** to denote elevation instead:
```
surface (base): #121212
surface--raised (elevated): #1E1E1E
surface--overlay (higher): #242424
surface--popover (highest): #2C2C2C
```

---

### 7. Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `radius-none` | 0px | Tables, sharp-cornered containers |
| `radius-xs` | 2px | Checkboxes, small badges |
| `radius-sm` | 4px | Input fields, small buttons, tags |
| `radius-md` | 6px | Standard buttons, cards, dropdowns |
| `radius-lg` | 8px | Large cards, modals |
| `radius-xl` | 12px | Hero cards, marketing components |
| `radius-2xl` | 16px | Large modal containers |
| `radius-full` | 9999px | Pills, avatars, circular buttons |

---

### 8. Motion System

#### Motion Principles
1. **Purposeful**: Every animation communicates meaning — state change, spatial relationship, or feedback
2. **Quick**: Durations are short (100–400ms) — animation should never feel like it's delaying the user
3. **Natural**: Use ease-out for entering, ease-in for exiting — respect physics
4. **Accessible**: Respect `prefers-reduced-motion` — all significant motion must have a static fallback
5. **Consistent**: Same type of transition always uses the same duration and easing

#### Duration Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `duration-instant` | 0ms | Instant state changes |
| `duration-fast-1` | 100ms | Micro-interactions (hover, focus, ripple effects) |
| `duration-fast-2` | 150ms | Button press, toggle, checkbox |
| `duration-base` | 200ms | Standard transitions (opacity, color, small transforms) |
| `duration-slow-1` | 300ms | Panel expand/collapse, modal open/close, drawer slide |
| `duration-slow-2` | 400ms | Complex animations, page transitions, hero animations |
| `duration-slow-3` | 500ms | Large-scale transitions, onboarding flows |

#### Easing Curves

| Token | CSS Cubic-Bezier | Usage | Feel |
|-------|-----------------|-------|------|
| `ease-default` | `cubic-bezier(0.4, 0, 0.2, 1)` | Standard transitions | Smooth deceleration |
| `ease-in` | `cubic-bezier(0.4, 0, 1, 1)` | Elements entering/exiting | Acceleration |
| `ease-out` | `cubic-bezier(0, 0, 0.2, 1)` | Elements appearing | Deceleration |
| `ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | Elements moving between positions | Symmetric |
| `ease-emphasized` | `cubic-bezier(0.0, 0, 0.2, 1)` | Emphasis, spring effects | Strong deceleration |
| `ease-overshoot` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Bouncy reveals | Overshoot + settle |

#### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

Design all motion-dependent interactions so they work identically (or with a simple opacity swap) when motion is disabled.

---

## Brand Voice & Tone

### Voice Attributes

The brand voice is consistent across all contexts. Define 4–5 attributes with do/don't examples.

| Attribute | Description | ✅ Do | ❌ Don't |
|-----------|-------------|--------|---------|
| **Clear** | Simple, direct, avoids jargon | "Your file is ready to download." | "The requested digital asset has successfully completed the processing pipeline." |
| **Helpful** | Anticipates user needs, provides context | "We noticed your subscription ends soon. Here's what you'll lose access to." | "Subscription expiring." |
| **Human** | Conversational, warm, not robotic | "Oops! That didn't work. Let's try again." | "Error 500: Internal server exception." |
| **Confident** | Authoritative without arrogance | "We recommend enabling two-factor authentication to protect your account." | "You MUST enable 2FA now." |
| **Inclusive** | Welcoming to all, avoids assumptions | "Welcome back" or username-based greeting | "Hey guys!" or gendered defaults |

### Tone Spectrum

Tone flexes by context. Define the acceptable range per content type.

| Context | Tone | Example |
|---------|------|---------|
| **Product UI** | Clear, helpful, human | Empty state: "Nothing here yet. Create your first project to get started." |
| **Success message** | Celebratory but brief | "All done! Your changes have been saved." |
| **Error message** | Helpful, calm, solution-oriented | "We couldn't process your payment. Check your card details and try again." |
| **Warning** | Direct, proactive | "You have 3 days left in your trial. Add a payment method to keep access." |
| **Marketing landing page** | Confident, aspirational, benefit-focused | "Build faster. Ship smarter. The platform teams trust." |
| **Email notification** | Warm, informative, actionable | "Hi Alex, your report is ready. View it here →" |
| **Help/Support article** | Patient, thorough, step-by-step | "To change your billing address: 1. Go to Settings... 2. Click..." |
| **Release notes** | Enthusiastic, transparent | "🎉 New: Dark mode is here! Plus 12 bug fixes you asked for." |
| **Legal/Terms** | Precise, unambiguous (tone flexibility is limited) | "These terms govern your use of the Service. By using the Service, you agree..." |

### Messaging Pillars

Key themes that all brand communication must reinforce:

1. **[Pillar 1 Name]**: One-sentence description of what this pillar communicates
2. **[Pillar 2 Name]**: One-sentence description
3. **[Pillar 3 Name]**: One-sentence description

Every piece of copy should ladder up to at least one messaging pillar.

### Grammar & Mechanics

| Rule | Decision | Example |
|------|----------|---------|
| Oxford comma | Yes / No | — |
| Date format | Month DD, YYYY (US) or DD Month YYYY (International) | "January 15, 2026" |
| Time format | 12-hour with AM/PM or 24-hour | "2:30 PM" or "14:30" |
| Numbers | Spell out one through nine; numerals for 10+ | "three files", "12 users" |
| Headline case | Title Case for Marketing, Sentence case for UI | "Get Started Today" (marketing), "Create a new project" (UI) |
| Contractions | Yes (conversational) or No (formal) | "You're all set" vs. "You are all set" |
| Pronouns | Gender-neutral (they/them unless individual preference known) | "A user can update their settings" |
| Button text | Verb-first, short (≤ 3 words) | "Save changes", not "Click here to save your changes" |
| Placeholders | Example format in gray: `e.g., name@example.com` | Always include format hint, not just field name |
| "Sign in" vs "Log in" | Pick one; use consistently | "Sign in" recommended (more modern; aligns with SSO terminology) |
| Emoji | Yes (sparingly, for celebratory contexts) or No | "🎉 You're all set!" |

---

## Brand Application

### Digital
- **Web**: Logo in header (primary, top-left or centered). Favicon (icon-only variant). Open Graph image with logo + brand colors.
- **Mobile apps**: App icon (icon-only on brand-color background). Splash screen (logo centered on brand background). System font as fallback.
- **Email**: Logo in header. Brand primary color for buttons. Web-safe fonts for body. Dark mode support for email clients.
- **Social media**: Avatar (icon-only). Header/banner (full logo + brand imagery). Post templates with consistent typography and color use.
- **Presentation decks**: Title slide (logo + brand imagery). Content slides (brand typography, accent color for emphasis, consistent margin). Data slides (brand palette for chart colors).

### Print
- **Business cards**: Logo (primary). Typography: at minimum 8pt for legibility. Color: brand primary + neutral. Bleed: 3mm.
- **Letterhead**: Logo (primary, top). Typography: body font. Margins: generous left margin for filing. Footer: legal info, contact.
- **Brochures/Flyers**: Cover (hero image + logo + headline). Inside (brand typography, generous whitespace, brand color accents).
- **Merchandise**: Apparel (embroidery: monochrome logo; screen printing: full color on light garment, reversed on dark). Drinkware/notebooks (single-color logo, clean placement).

### Environmental
- **Office signage**: Logo (primary, large scale). Wayfinding: brand typography + accent color.
- **Event booths**: Backdrop (large logo + brand pattern). Collateral (consistent with digital + print identity).

---

## Brand Governance

### Roles & Responsibilities

| Role | Responsibility | Authority |
|------|---------------|-----------|
| **Brand Steward** | Owns the brand guidelines. Approves all brand changes. Runs quarterly audits. | Final decision on all brand identity matters |
| **Design Lead** | Maintains design files, templates, and asset library. Reviews brand application in product. | Approves design-level brand use |
| **Marketing Lead** | Ensures campaign materials follow guidelines. Briefs external agencies. | Approves marketing-level brand use |
| **Engineering Lead** | Maintains design tokens in code. Ensures component library matches brand specs. | Approves code-level brand implementation |
| **Content Lead** | Maintains voice and tone guide. Reviews all public-facing copy. | Approves copy-level brand adherence |

### Brand Review & Approval Process

1. **Request**: Team member submits brand asset request with: description, context (where used), deadline, and any constraints
2. **Review**: Brand steward or design lead reviews against guidelines within SLA (e.g., 2 business days)
3. **Feedback**: Approve, approve with changes, or reject with rationale
4. **Iterate**: Requester addresses feedback; re-submit if needed
5. **Finalize**: Asset is approved and added to the brand asset library

### Brand Audit Cadence

| Frequency | Scope | Owner |
|-----------|-------|-------|
| **Weekly** | Spot-check: marketing emails, social posts, new landing pages | Marketing Lead |
| **Monthly** | Product UI: new screens, component changes, design token drift | Design Lead + Engineering Lead |
| **Quarterly** | Full audit: all surfaces (web, mobile, email, print, social, environmental) | Brand Steward |
| **Annually** | Brand health: awareness survey, NPS by brand perception, competitive positioning review | Brand Steward + Leadership |

### Brand Drift Detection Checklist (Quarterly)
- [ ] Are all logos the correct variant for their context?
- [ ] Are brand colors within 5% tolerance of spec (check 10 random screens/pages)?
- [ ] Is typography consistent with the type scale (check 10 random screens/pages)?
- [ ] Are interactive components using the correct spacing and radius tokens?
- [ ] Is the brand voice consistent in error messages, empty states, and notifications?
- [ ] Are design tokens in code matching the latest exported token JSON?
- [ ] Are third-party vendors and agencies using the most recent brand guidelines?
- [ ] Have any new brand elements been added without going through approval?

---

## References

- _Designing Brand Identity_ (5th Ed.) by Alina Wheeler
- _Brand Gap_ by Marty Neumeier
- _Articulating Design Decisions_ by Tom Greever
- Material Design 3 — for token architecture reference
- Style Dictionary by Amazon — for design token infrastructure
- Figma Tokens plugin — for syncing tokens between design and code
