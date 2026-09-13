# Portable Policy

<!-- STANDARD: 3min -- .editorconfig as the intent layer, and what belongs there versus in a tool -->

## Why a portability layer exists

An organisation with Go, TypeScript, Swift and Python cannot have one formatter — each language has its own, and stretching one tool across all of them produces false positives. But it **can** have one *policy*: the same intent about line endings, whitespace and indentation, expressed in a mechanism every major editor and IDE reads.

That mechanism is `.editorconfig`.

## What `.editorconfig` is, and is not

| It is | It is not |
|---|---|
| A portable statement of **intent** | a formatter |
| Read by most editors and IDEs | read by every tool |
| Applied per file type | a substitute for the language's formatter |
| The first line of defence | the authority (CI is) |

**The key limitation:** `.editorconfig` sets editor behaviour (indentation, line endings, whitespace handling). It does not reformat quotes, wrap lines, order imports, or decide any language-specific layout. That is the formatter's job.

So the layers do not overlap: `.editorconfig` prevents the common editor-level churn; the formatter decides everything else.

## A baseline set

```ini
# EditorConfig — consistent editor settings across all contributors
root = true

[*]
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
charset = utf-8
indent_style = space
indent_size = 2

[*.py]
indent_size = 4

[*.go]
indent_style = tab          # gofmt uses tabs; do not fight the formatter

[Makefile]
indent_style = tab          # make requires tabs

[*.md]
trim_trailing_whitespace = false   # two trailing spaces are a hard line break in Markdown
```

Two properties worth noting in that file:

1. **It defers to the formatter where the formatter has a strong opinion.** Go uses tabs; fighting that with `indent_size = 2` produces a config that disagrees with `gofmt` on every save.
2. **It has an exception where the exception is real** — Markdown's trailing-space line break. An exception with a reason is part of a good policy.

## What belongs in `.editorconfig`

| Property | Belongs here | Why |
|---|---|---|
| `end_of_line` | yes | the single most common source of spurious diffs |
| `insert_final_newline` | yes | universal, unambiguous |
| `trim_trailing_whitespace` | yes | universal, with the Markdown exception |
| `charset` | yes | prevents encoding churn |
| `indent_style` / `indent_size` | yes | universal, per language |
| `max_line_length` | **partly** | editors read it; the formatter has the real authority — set both, consistently |

## What does not belong here

| Concern | Where it belongs |
|---|---|
| Quote style, semicolons | the formatter (Prettier, Biome, the language's tool) |
| Line wrapping behaviour | the formatter |
| Import ordering | the formatter or a dedicated import sorter |
| Naming conventions | the linter |
| Complexity thresholds | the linter |
| Anything security-relevant | the linter, and never suppressible |

Putting these in `.editorconfig` produces a config that claims an authority it does not have.

## The alignment rule

Where a concern exists in both layers, they must agree:

```ini
# .editorconfig
[*.{js,ts}]
max_line_length = 100
```

```json
// prettier config — MUST match, or the two disagree on every save
{ "printWidth": 100 }
```

**A mismatch here is a visible defect:** the editor stops at 100, the formatter rewrites to 80, and the developer sees a diff on every save. Set the value once and reference it, or keep the two files adjacent with a comment pointing at the other.

## Precedence and inheritance

| Rule | Detail |
|---|---|
| Nearest file wins for conflicting properties | a nested `.editorconfig` overrides a parent for that subtree |
| `root = true` stops the search upward | set it at the repository root |
| More specific glob wins | `[*.py]` overrides `[*]` for Python files |
| A property not set is not overridden | the parent's or the editor's default applies |

**The practical implication:** in a monorepo, one root `.editorconfig` plus per-package overrides is the pattern. A package that needs a different indentation declares it locally rather than at the root.

## Verifying it is actually applied

A config that nothing reads is documentation. Verify:

```text
1. Open a file of each type in an editor that supports EditorConfig.
2. Confirm the indentation and line endings match the config.
3. Create a file with CRLF and trailing whitespace → the editor fixes it on save.
4. Confirm the language's formatter does not fight it (the two disagree visibly).
5. Check CI: the formatter's check should agree with what the editor produced.
```

Step 4 is the one that finds a misconfigured layer: if the formatter rewrites what the editor just produced, the two are contradicting each other and every save is churn.

## In a monorepo

```
/.editorconfig                 ← root: universal intent, root = true
/packages/web/.editorconfig    ← web-specific overrides (if any)
/packages/ios/.editorconfig    ← Swift specifics
/packages/service/.editorconfig
```

Three rules:

1. **Only override what differs.** A package that repeats the root's values is a maintenance burden and a divergence risk.
2. **Never remove the root file**, even if every package overrides it — the root is what makes the search terminate and what new packages inherit.
3. **Keep overrides to intent, not layout.** A package does not get to redefine what "formatted" means.

## Checklist

- [ ] `.editorconfig` exists at the repository root with `root = true`
- [ ] Every file type present in the repo is covered by a section
- [ ] `end_of_line`, `insert_final_newline`, `trim_trailing_whitespace` and `charset` are set
- [ ] Indentation defers to the language's formatter where the formatter has a strong opinion (Go, Makefile)
- [ ] Real exceptions carry a reason (Markdown trailing whitespace)
- [ ] Values that exist in both layers agree with the formatter's config
- [ ] Monorepo overrides are minimal, and the root still exists
- [ ] It has been verified to apply in an editor, not merely written
