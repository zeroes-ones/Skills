# Font Licensing

<!-- STANDARD: 3min -- licence families, grants per context, register format -->

## The governing rule

**A licence is a grant for a context, not a property of a file.** The same `.ttf` may be
permitted for a desktop design mockup and forbidden in a shipped mobile binary. Free to
download is not free to embed. This is why R4 gates design work on the licence: discovering
the exclusion mid-project forces a font replacement that invalidates the scale, the metrics
and the fallback work already done.

## The contexts that matter

| Context | What it means | Common exclusion |
|---|---|---|
| Design/mockup | use in Figma or a design tool | usually permitted even by restrictive licences |
| Web embedding (`@font-face`) | the font is served to browsers | **many desktop licences forbid this** |
| App embedding | the font file is bundled in a mobile or desktop binary | often a separate grant, sometimes forbidden |
| Server-side rendering | the font is used to render images, PDFs or SSRs on a server | often scoped out and requires an extended licence |
| E-book / document embedding | the font is embedded in a distributable document | usually a separate grant |
| Redistribution | the file is stored in a public repository or shipped to third parties | frequently forbidden |
| Subsetting / modification | the file is altered (subsetting counts as modification) | some licences forbid modification entirely |
| Self-hosting | the font is served from your origin rather than a CDN | some free licences permit it; check the terms |
| High-traffic web | usage tiers above a threshold | some commercial licences price by monthly pageviews |

## Licence families

### SIL Open Font License (OFL)

The most permissive for product use. Permits use, modification, and redistribution, including
bundling in applications and webfont use, **provided** that:

- the font is not sold on its own;
- derivative fonts are released under the OFL, not under a conflicting licence;
- the Reserved Font Name is not used for a modified version (this is why a subset keeping the
  original name can technically breach the terms — rename subsets that are redistributed);
- the copyright notice and licence text are included with the font.

Practical consequence: OFL is safe for almost every product, but keep the licence text
alongside the binary and rename redistributed subsets.

### Apache License 2.0

Permissive, includes an explicit patent grant. Requires the licence and notices to be
retained. Safe for commercial embedding. Used by some corporate-sponsored families.

### Public domain / CC0 / Unlicense

No conditions. Safe in every context. Rare for quality text faces.

### Commercial / proprietary (per-seat or per-pageview)

A paid grant with scoped terms. The specific traps:

- **Desktop-only** licences are the most common purchase and the most common mistake — they
  cover the design phase and nothing shipped.
- **Pageview tiers** can be exceeded by growth, turning a fixed cost into a liability. Track
  the tier against analytics.
- **App embedding** is usually a distinct licence line item.
- **Server rendering** is frequently excluded; a PDF report generator using the font is
  out of scope on a desktop grant.

### Fonts bundled with a platform or OS

Licensed for use **on that platform**, not for redistribution or use elsewhere. Using a system
font by name (`-apple-system`, `system-ui`) is fine — the platform supplies it. Copying the
system font file into your web bundle is not.

### Web-font services (hosted)

The provider hosts and serves under their terms. Traps: the licence may not permit
self-hosting the file (which blocks offline/PWA use and adds a third-party runtime
dependency); and removing the service later may require repurchasing a self-host licence.

## The decision

```text
Does the product ship in more than one context (web AND app AND server render)?
├── Yes → the licence must cover every context, or use a per-context face
└── No  → the licence must cover the one context it ships in
    Is the face OFL, Apache-2.0, or public domain?
    ├── Yes → permitted; record the attribution obligation and rename any redistributed subset
    └── No (commercial)
        ├── Which grant was purchased — desktop, web, app, server?
        │   ├── Covers the shipping context → permitted; record the pageview tier and renewal
        │   └── Does not cover it → obtain the grant, or eliminate the face (do not proceed)
        └── Is the web use through a hosted service?
            ├── Yes → confirm whether self-hosting is permitted (needed for offline/PWA)
            └── No  → confirm the pageview tier against live analytics
Finally: is attribution required, and is the file redistributed?
└── Yes → include the licence text and rename modified/subset redistributions
```

## The licensing register

Maintain a register as part of the type system. Its absence is why "can we use this?" is
answered differently by two people on the same team.

| Face | File | Licence | Web | App | SSR | Redistribute | Modify/subset | Attribution | Notes |
|---|---|---|---|---|---|---|---|---|---|
| Inter | `inter-var.woff2` | OFL-1.1 | ✅ | ✅ | ✅ | ✅ (rename subset) | ✅ | not required, text included | Reserved Font Name applies to modified versions |
| Source Serif | `source-serif.woff2` | OFL-1.1 | ✅ | ✅ | ✅ | ✅ | ✅ | text included | |
| Acme Display | `acme.woff2` | Commercial, web tier ≤ 1M pv/mo | ✅ | ❌ | ❌ | ❌ | ❌ | per agreement | **cannot ship in app** — use for web only |
| SF Pro | system | Apple platform licence | ❌ | via platform only | ❌ | ❌ | ❌ | n/a | reference by name only; never bundle the file |
| Roboto | system (Android) | Apache-2.0 | ✅ | ✅ | ✅ | ✅ | ✅ | notices retained | bundling optional since the platform provides it |

Every row is a decision someone can audit. A shipping context absent from the register is an
unresolved licence question, and an unresolved question at release is a schedule risk (R4).

## Enforcement

Licences fail at two moments: design time (when the wrong face gets designed in) and release
time (when a binary ships without the grant). Catch both.

**At design time:**
- The register precedes the design. No face enters a mockup without a register row.
- A candidate face with an unknown licence is not a candidate.

**At release time (automate it):**

```bash
# Licence gate — every font binary must appear in the register with a permitted context
set -euo pipefail

REGISTER="design/type-licensing.md"
status=0

while IFS= read -r font; do
    name=$(basename "$font")
    if ! grep -q "$name" "$REGISTER"; then
        echo "FAIL: $name has no licence register entry (R4)"
        status=1
    fi
done < <(find public/fonts assets/fonts -type f \( -name '*.woff2' -o -name '*.ttf' -o -name '*.otf' \) 2>/dev/null)

# Confirm the licence text ships with the fonts
if ! find . -iname 'OFL.txt' -o -iname 'LICENSE*' | grep -qi 'font'; then
    echo "WARN: no font licence text found alongside the binaries"
fi

exit $status
```

**In CI**, run the gate on every pull request that touches a font directory. The failure it
prevents — a release blocked by a legal review days before launch, requiring a font swap that
invalidates the scale and the metric overrides — is far more expensive than the gate.

## Cost of getting this wrong

| Failure | Consequence |
|---|---|
| Desktop-only licence in a shipped app | Forced replacement mid-project; the scale, metrics and fallbacks must be redone |
| Exceeded pageview tier | Retroactive fee or a mid-quarter replacement |
| Subset redistributed under the Reserved Font Name | OFL breach requiring a rename and re-release |
| System font file bundled for web | Platform licence breach; also a legal exposure the team cannot remedy retroactively |
| Unknown licence at release | Release blocked pending legal review; schedule risk with no engineering remedy |

The asymmetry is the argument for R4: the cost of checking is an hour; the cost of not
checking is a replacement project.
