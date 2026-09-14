# Templating and Fidelity

## Why templates

Appearance must live in one place. Code that styles each run by hand diverges from the brand the
moment the brand changes, and nobody notices until a customer does.

## Template patterns

| Format | Mechanism | Notes |
|---|---|---|
| `.docx` | `docxtpl` `{{ placeholder }}` | Author the template in Word; keep styles in the template |
| `.xlsx` | Named ranges + a template sheet | Never positional references; insert rows freely |
| `.pptx` | Slide layouts + placeholders | Position via layout, not absolute coordinates |
| `.pdf` | A reportlab frame layout or an HTML/CSS stylesheet | Keep the layout definition separate from the data |

## Fidelity checklist for any conversion

Run this every time a file changes format.

1. **Page/slide count** — compare source and output; explain every difference.
2. **Fonts** — confirm the intended faces survived; substitutions are silent.
3. **Table widths and borders** — the most common visible regression.
4. **Images** — resolution and placement.
5. **Formulas and pivots** — do they still recalculate?
6. **Macros** — usually lost; state it explicitly.
7. **Tracked changes and comments** — preserved, or explicitly resolved?
8. **Metadata** — author, title; strip anything sensitive before external send.
9. **Links and bookmarks** — internal references often break.
10. **Accessibility structure** — heading levels and alt text matter if the output is published.

## Reporting rule

State what survived and what was lost. Never present a converted file as equivalent to its source
without having checked.
