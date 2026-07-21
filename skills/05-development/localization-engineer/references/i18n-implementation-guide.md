# i18n Implementation Guide

> **Author:** Sandeep Kumar Penchala

Comprehensive internationalization (i18n) patterns covering library selection, message extraction, pluralization, formatting, RTL support, translation management, and pseudo-localization. These patterns support the localization-engineer skill's full localization lifecycle.

## i18n Library Comparison

| Library | Framework | Bundle Size | ICU Support | Pluralization | Key Features |
|---------|-----------|------------|-------------|--------------|--------------|
| react-intl (FormatJS) | React | ~15 KB | Full ICU | Built-in | Rich text formatting, date/time via Intl |
| i18next | Framework-agnostic | ~10 KB core | Via plugin | Built-in | Most popular, huge plugin ecosystem, async loading |
| LinguiJS | React | ~3 KB + catalog | Full ICU | Built-in | Compile-time extraction, macros, smallest runtime |
| vue-i18n | Vue | ~8 KB | Partial | Built-in | Vue Composition API, lazy loading, SFC support |
| next-intl | Next.js | ~5 KB | Full ICU | Built-in | Server Components, middleware, async messages |
| svelte-i18n | Svelte | ~3 KB | Via Intl | Via Intl | Svelte stores, lazy loading |

### Decision Matrix

```
Need framework-agnostic + plugin ecosystem? → i18next
React only, want smallest runtime?          → LinguiJS
React, need rich ICU formatting?             → react-intl
Next.js app router (RSC + client)?           → next-intl
Vue ecosystem?                               → vue-i18n
Svelte?                                      → svelte-i18n
```

## Message Extraction Workflow

### LinguiJS Extraction (Recommended for React)

```bash
npm install -D @lingui/cli @lingui/macro
```

```jsonc
// lingui.config.ts
export default {
  locales: ["en", "es", "fr", "ja", "ar"],
  sourceLocale: "en",
  catalogs: [{
    path: "<rootDir>/src/locales/{locale}/messages",
    include: ["src"],
    exclude: ["**/node_modules/**"],
  }],
  format: "po",  // PO format for translator compatibility
};
```

```tsx
// Source code — LinguiJS macro extracts at compile time
import { Trans, msg } from "@lingui/macro";

function Welcome({ name }: { name: string }) {
  return (
    <div>
      <Trans>Hello, <strong>{name}</strong>! Welcome back.</Trans>
      <p>{msg`You have ${count} unread messages.`}</p>
    </div>
  );
}
```

```bash
# Extract messages into PO files
npx lingui extract

# Compile PO → JS for production
npx lingui compile
```

### CI Integration for Stale Detection

```yaml
# .github/workflows/i18n.yml
i18n-check:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - run: npm ci
    - run: npx lingui extract
    - name: Check for stale translations
      run: |
        git diff --exit-code src/locales/ || (echo "Translations out of sync. Run 'lingui extract' locally." && exit 1)
```

## Pluralization Rules (CLDR)

The CLDR defines six plural categories. Not all categories apply to every language.

| Language | zero | one | two | few | many | other |
|----------|------|-----|-----|-----|------|-------|
| English | — | 1 | — | — | — | 0, 2+ |
| Arabic | 0 | 1 | 2 | 3-10 | 11-99 | 100+ |
| Japanese | — | — | — | — | — | all |
| Russian | — | 1, 21, 31... | — | 2-4, 22-24... | — | 0, 5-20... |
| Irish | — | 1 | 2 | 3-6 | 7-10 | 0, 11+ |

### ICU Message Format for Pluralization

```jsonc
// en/messages.json
{
  "item_count": "{count, plural, =0 {No items} one {# item} other {# items}}",
  "order_summary": "{count, plural, =0 {Your cart is empty} one {1 item in your cart} other {# items in your cart}}"
}
```

```tsx
// Usage with react-intl
<FormattedMessage id="item_count" values={{ count: 5 }} />
// Renders: "5 items"
```

## Date, Number, and Currency Formatting

### Intl API (Zero-Dependency)

```typescript
// Date formatting
new Intl.DateTimeFormat('de-DE', { dateStyle: 'full' }).format(new Date());
// → "Montag, 21. Juli 2026"

new Intl.DateTimeFormat('ja-JP', { year: 'numeric', month: 'long', day: 'numeric' }).format(new Date());
// → "2026年7月21日"

// Number formatting
new Intl.NumberFormat('en-US').format(1234567.89);    // → "1,234,567.89"
new Intl.NumberFormat('de-DE').format(1234567.89);    // → "1.234.567,89"
new Intl.NumberFormat('en-IN').format(1234567.89);    // → "12,34,567.89"

// Currency formatting
new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(42.50);
// → "$42.50"
new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(42.50);
// → "42,50 €"

// Relative time
new Intl.RelativeTimeFormat('en', { numeric: 'auto' }).format(-3, 'day');
// → "3 days ago"
new Intl.RelativeTimeFormat('ja', { numeric: 'auto' }).format(1, 'day');
// → "明日"

// List formatting
new Intl.ListFormat('en', { style: 'long', type: 'conjunction' }).format(['Alice', 'Bob', 'Carol']);
// → "Alice, Bob, and Carol"
```

## RTL Layout Guide

### CSS Logical Properties

```css
/* BAD — physical directions break in RTL */
.sidebar { margin-left: 16px; padding-right: 8px; border-left: 1px solid #ccc; }
.icon { float: left; }
.arrow { transform: rotate(-90deg); }

/* GOOD — logical properties adapt to writing direction */
.sidebar { margin-inline-start: 16px; padding-inline-end: 8px; border-inline-start: 1px solid #ccc; }
.icon { float: inline-start; }
.arrow { transform: rotate(90deg); } /* Arrow direction stays consistent */

/* Direction-aware shorthand reference:
   margin-inline-start  = margin-left (LTR) / margin-right (RTL)
   padding-inline-end   = padding-right (LTR) / padding-left (RTL)
   inset-inline-start   = left (LTR) / right (RTL)
   text-align: start    = left (LTR) / right (RTL)
*/
```

### RTL Mixin / Utility

```scss
// SCSS RTL mixin
$dir: ltr !default;

@mixin rtl {
  @if $dir == rtl {
    html[dir="rtl"] & { @content; }
  }
}

.card {
  margin-left: 20px;
  @include rtl { margin-left: 0; margin-right: 20px; }
}
```

### Tailwind RTL

```html
<!-- Tailwind logical properties (v3.3+) -->
<div class="ms-4 pe-2 border-s">RTL-aware sidebar</div>
<!-- ms-4 = margin-inline-start, pe-2 = padding-inline-end, border-s = border-inline-start -->

<!-- Direction-specific overrides using variant -->
<div class="ltr:ml-4 rtl:mr-4">Physical override when needed</div>
```

## Translation Management

### TMS Integration

| Platform | Key Features | CLI | API | Price Model |
|----------|-------------|-----|-----|-------------|
| Lokalise | Screenshots, in-context editor, OTA updates | ✅ | ✅ | Per-seat + keys |
| Crowdin | GitHub/GitLab integration, MT engines | ✅ | ✅ | Per-seat |
| Phrase (Strings) | Developer-first, API-heavy, branching | ✅ | ✅ | Per-seat |
| POEditor | Simpler, affordable | ✅ | ✅ | Per-project |
| Tolgee | Open-source, in-context editing SDK | ✅ | ✅ | Self-hosted free |

### Developer Workflow

```
1. Developer extracts new/changed strings → PO/JSON files
2. Push to TMS via CLI: `npx lokalise2 file upload --file src/locales/en/messages.po`
3. Translators work in TMS (in-context, screenshots, MT suggestions)
4. Pull translations via CI: `npx lokalise2 file download --format json`
5. Compile to production format, deploy
6. Rinse and repeat each sprint
```

## Locale Detection Priority

```
Order of precedence (first match wins):
  1. URL path        /fr/dashboard      ← Best for SEO, shareable
  2. Cookie          locale=fr          ← Persistent user preference
  3. User setting    account.locale     ← Authenticated user preference
  4. Accept-Language  fr,en;q=0.9       ← Browser preference (fallback)
  5. Default          en                ← Hardcoded fallback
```

```typescript
// Middleware for locale detection (Next.js App Router)
import { match } from '@formatjs/intl-localematcher';
import Negotiator from 'negotiator';

const locales = ['en', 'es', 'fr', 'ja', 'ar'];
const defaultLocale = 'en';

function getLocale(request: NextRequest): string {
  const headers = { 'accept-language': request.headers.get('accept-language') || '' };
  const languages = new Negotiator({ headers }).languages();
  return match(languages, locales, defaultLocale);
}
```

## Pseudo-Localization

Test localization readiness without real translations. Use box-drawing characters to detect overflow and hard-coded strings.

```typescript
// Pseudo-localization transformation
function pseudoLocalize(text: string): string {
  const map: Record<string, string> = {
    'a': 'àáâãäå', 'e': 'èéêë', 'i': 'ìíîï', 'o': 'òóôõö', 'u': 'ùúûü',
    'A': 'ÀÁÂÃÄÅ', 'E': 'ÈÉÊË', 'I': 'ÌÍÎÏ', 'O': 'ÒÓÔÕÖ', 'U': 'ÙÚÛÜ',
  };
  let result = '';
  for (const char of text) {
    const options = map[char];
    result += options ? options[Math.floor(Math.random() * options.length)] : char;
  }
  // Add prefix/suffix for expansion testing (~30% longer for some locales)
  return `「${result}」`;
}

// Usage: pseudoLocalize("Submit") → "「Sùbmìt」"
```

### Pseudo-Localization Checklist

- [ ] All UI strings come from translation files (no hard-coded English)
- [ ] No layout breaks with 30-50% text expansion
- [ ] RTL mirroring works (CSS logical properties used throughout)
- [ ] Date/time/currency formats use Intl, not manual formatting
- [ ] Plural forms work — test with 0, 1, 2, 5, 21 items
- [ ] Concatenation never used (`"Hello " + name` — always use parameterized messages)

## ICU Message Format Reference

```
# Simple argument
Hello, {name}!

# Plural
{count, plural, =0 {No messages} one {# message} other {# messages}}

# Select (gender, enum)
{gender, select, male {He} female {She} other {They}} sent you a message.

# Number formatting
{price, number, ::currency/USD ::minimumFractionDigits/2}

# Date formatting
{date, date, ::yyyyMMdd}

# Rich text (FormatJS)
You have <bold>{count} new messages</bold> in your <link>inbox</link>.
```

This i18n guide implements the localization-engineer skill's core workflow: extract, translate, format, and validate — ensuring every user sees a native-quality experience regardless of locale.
