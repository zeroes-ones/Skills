# Source Hierarchy Guide

## Trust Levels and Escalation Paths

```
TRUST SPECTRUM
═══════════════════════════════════════════════════════════════
  Level 1  [     TRUSTED     ]  Official docs & API references
  Level 2  [     TRUSTED     ]  Official blog & release notes
  Level 3  [    VERIFIED     ]  Web standards (MDN, W3C, WHATWG)
  Level 4  [    VERIFIED     ]  Browser/engine compat (caniuse, node.green)
  Level 5  [    CAUTION      ]  Source code — accurate but expensive
  ─────────────────────────────────────────────────────────
  Level 0  [    REJECTED     ]  LLM output, forums, blog posts, SO
═══════════════════════════════════════════════════════════════
```

## Level 1: Official Documentation

**Characteristics:** Hosted on the framework's primary domain. Versioned. Maintained by framework authors. Usually at `docs.{project}.com` or `{project}.dev/docs`.

**Examples:** react.dev/reference, docs.stripe.com/api, prisma.io/docs/orm, nextjs.org/docs, pkg.go.dev/{module}

**When to trust:** Always — but only for the version explicitly stated on the page. Cross-reference the version selector or URL prefix.

**Red flags:** No version indicator, "last updated" >6 months with a newer release available, broken links to referenced API pages.

## Level 2: Official Blog & Release Notes

**Characteristics:** Maintainer-authored announcements. GitHub Releases pages. Changelogs in the repo.

**Examples:** blog.rust-lang.org, github.com/facebook/react/releases, nodejs.org/en/blog/release

**When to trust:** For behavioral changes, deprecations, new features. Do NOT trust for exact API signatures — always verify against Level 1.

## Level 3: Web Standards

**Characteristics:** MDN Web Docs, W3C specifications, WHATWG living standards. Browser-vendor reviewed.

**Examples:** developer.mozilla.org, w3.org/TR, html.spec.whatwg.org, tc39.es/ecma262

**When to trust:** For browser APIs, CSS, HTML, and ECMAScript. Cross-reference with Level 4 for actual implementation status.

## Level 4: Compatibility Data

**Characteristics:** Automated compatibility tables. Reflects what actually ships, not what's specified.

**Examples:** caniuse.com, node.green, browser-compat-data (MDN's @mdn/browser-compat-data)

**When to trust:** For "does this work in target X?" questions. Use to validate Level 3 assumptions against reality.

## Level 5: Source Code

**Characteristics:** The definitive ground truth. But expensive to verify and easy to misinterpret.

**When to reach for it:** When Levels 1-4 are contradictory, silent, or outdated. Always pin to a specific git tag or commit SHA.

**⚠️ CAUTION:** Source code can contain internal/unexported behavior not part of the public API. Don't rely on it without checking for `@internal`, `@private`, or `_` prefix conventions.

## Escalation Path

```
Level 1 missing/ambiguous → Level 2 (release notes may clarify)
Levels 1-2 insufficient   → Level 3-4 (standards + compat)
Levels 1-4 contradictory   → Level 5 (source code at git tag)
Levels 1-5 all insufficient → File issue; document gap with ⚠️ DOC-GAP
```
