# Script Coverage

<!-- DEEP: 5+min -- per-script requirements and how to test coverage -->

## The governing rule

**Coverage is a property of the shipped file, not of the family name.** A family may ship
dozens of files; a subset may drop a block; a version may change its coverage. The only
evidence is a test against the exact file that ships, over the exact characters the content
can produce (R5).

## Why "it looks fine in English" is not coverage

The failure modes are invisible in a Latin-only test:

- Tofu boxes appear only for the locales that were never rendered during development.
- Joined scripts render unjoined when a subset drops presentation forms — the words are
  technically present but illegible.
- CJK text wraps in the wrong places because the full-width punctuation was substituted.
- Thai text becomes one long unbroken run because Thai has no word spaces.

Each of these ships silently to a market the team cannot read.

## Per-script requirements

### Latin, Cyrillic, Greek

| Requirement | Detail |
|---|---|
| Base coverage | ASCII plus the locale's diacritics (Latin-1, Latin Extended-A/B) |
| Punctuation | typographic quotes `“ ” ‘ ’`, dashes `– —`, ellipsis `…`, non-breaking space |
| Shaping | none — each glyph is independent |
| Tracking | safe |
| Watch for | missing typographic punctuation, which silently falls back and looks mismatched |

### Arabic, Persian, Urdu (joined, RTL)

| Requirement | Detail |
|---|---|
| Base coverage | the Arabic block plus presentation forms the shaper needs |
| Shaping | **contextual** — initial, medial, final and isolated forms |
| Diacritics | harakat for Arabic; often omitted in UI but must not tofu |
| Direction | RTL; set `dir` and use logical properties |
| Tracking | **never** — `letter-spacing` breaks the joins |
| Watch for | a subset that keeps base codepoints but drops presentation forms, producing unjoined text |

### Hebrew (RTL, non-joined)

| Requirement | Detail |
|---|---|
| Base coverage | Hebrew block plus Hebrew presentation forms |
| Shaping | minimal — Hebrew does not join |
| Direction | RTL |
| Tracking | technically safe, but do not apply it — it reads as a defect |
| Watch for | mixed Hebrew/Latin runs reversing incorrectly without proper bidi isolation |

### Devanagari, Bengali, Tamil, and other Indic scripts

| Requirement | Detail |
|---|---|
| Base coverage | consonants, independent vowels, **matras**, virama/halant |
| Shaping | **complex** — conjuncts form from multiple codepoints; reordering occurs |
| Tracking | **never** — it breaks conjuncts and separates matras from their base |
| Line breaking | space-based, but matras affect visible bounds |
| Watch for | missing conjunct forms producing stacked or separated glyphs; nominal size too small |

### Thai (no word spaces)

| Requirement | Detail |
|---|---|
| Base coverage | Thai block plus tone marks and vowel signs |
| Shaping | marks above and below the base; vertical metrics matter |
| Line breaking | **no spaces** — breaking requires a dictionary; the browser does it, but test it |
| Tracking | do not apply |
| Watch for | a single unbroken line; a dictionary-based `line-break` that is not enabled |

### CJK — Chinese, Japanese, Korean

| Requirement | Detail |
|---|---|
| Base coverage | kana (JP), hangul (KR), the required Han repertoire (varies by locale) |
| Punctuation | **full-width** forms; ideographic space U+3000; CJK brackets |
| Line breaking | `line-break: strict` / `word-break` affects kinsoku (no-break) rules |
| Tracking | do not apply generally; small `letter-spacing` is sometimes used deliberately for CJK display type |
| Vertical metrics | glyphs fill the em box; more leading is needed |
| Watch for | Han unification issues (the same codepoint rendering in a different regional style); missing full-width punctuation substituting Latin forms |

## Testing coverage

### 1. Derive the required character set from content, not mockups

```python
import glob, json, re
chars = set()
for f in glob.glob("locales/**/*.json", recursive=True):
    data = json.load(open(f, encoding="utf-8"))
    # strip ICU placeholder syntax so only literal text remains
    chars |= set(re.sub(r"\{[^}]*\}", "", json.dumps(data, ensure_ascii=False)))
# add punctuation and digits the UI produces outside catalogues
chars |= set("0123456789.,-_/()[]{}%$€£¥…–—“”‘’\u00a0")
open("/tmp/required-chars.txt", "w", encoding="utf-8").write("".join(sorted(chars)))
print(len(chars), "distinct characters required")
```

**Include user-generated content paths.** Names, addresses, notes and free-text fields can
contain any character the locale's keyboard produces. If the product accepts input in a
script, that script is required, whether or not the mockups show it.

### 2. Test each shipped file

```python
from fontTools.ttLib import TTFont
import glob
required = set(open("/tmp/required-chars.txt", encoding="utf-8").read())
for path in sorted(glob.glob("public/fonts/*.woff2")):
    f = TTFont(path)
    covered = {chr(cp) for table in f["cmap"].tables for cp in table.cmap}
    missing = sorted(required - covered)
    status = "OK" if not missing else "MISSING " + "".join(missing)
    print(f"{path:48s} {status}")
```

### 3. Test shaping for joined and complex scripts

Coverage of codepoints is necessary but not sufficient. Rendering must be checked:

- Render a sentence with words that join on both sides (`السلام`, `سلامت`), in a browser and
  on the target device.
- Render a Devanagari conjunct (for example क्ष, त्र) and confirm the conjunct forms rather
  than stacking.
- Confirm no `letter-spacing` is inherited from a parent rule (the most common cause of
  broken joins — it is usually a global `*` selector).

```css
/* A global tracking rule is the usual culprit — it silently breaks every joined script */
* { letter-spacing: -0.01em; }              /* ❌ breaks Arabic, Indic */

:lang(ar), :lang(fa), :lang(ur), :lang(hi),
:lang(bn), :lang(ta), :lang(th) { letter-spacing: normal; }   /* ✅ minimum safeguard */
```

Better: do not apply tracking globally at all. Apply it to the specific display roles that
benefit (R5).

### 4. Test line breaking where it is non-trivial

| Script | Test |
|---|---|
| Thai | a long Thai paragraph must break at word boundaries, not overflow the container |
| CJK | a line must not begin with a closing bracket or end with an opening one (kinsoku) |
| Arabic | mixed Arabic/Latin runs must not reorder incorrectly |

## Coverage strategies when a face falls short

| Situation | Strategy |
|---|---|
| Face lacks the script entirely | Add a per-script family in the fallback chain, ordered before the generic |
| Face covers the script but lacks some marks | Extend the chain for the mark-bearing subset; verify the join points |
| Coverage exists but style clashes | Choose a harmonised family for that script rather than accepting a mismatch |
| Latin-only brand face required for headings | Use the brand face for the Latin portions only and a companion for other scripts, declared explicitly |
| A single face must cover everything | Accept a larger payload, subset by block, and load non-Latin blocks only when used |

## The fallback chain, ordered

```css
:root {
  --font-sans:
    "Inter var",            /* the chosen face */
    "Inter Fallback",       /* metric-matched (R1) */
    "Noto Sans Arabic",     /* script coverage, joined */
    "Noto Sans Devanagari", /* script coverage, conjuncts */
    "Noto Sans Thai",       /* script coverage, no word spaces */
    "Noto Sans CJK JP",     /* CJK */
    system-ui,              /* the platform face */
    sans-serif;             /* the ultimate generic */
}
```

Each entry in the chain is a decision, not padding. Entries 1 and 2 are about *design*;
entries 3–6 are about *coverage*; entries 7–8 are the last resort. Document which entry exists
for which script — an undocumented chain is one refactor away from being deleted.

## Recording the result

For each locale, record in the State Log:

| Field | Example |
|---|---|
| Locale | `ar-SA` |
| Required characters | 312 distinct codepoints |
| File tested | `noto-arabic.woff2`, version recorded |
| Codepoint coverage | 100% |
| Shaping verified | yes, on device X, date Y |
| Tracking applied | none |
| Residual risk | harakat coverage untested on the user-input path |
