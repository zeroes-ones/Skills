# Generated Documentation

<!-- DEEP: 10+min — source-to-rendering, commit-then-check, drift gates, and unexercised generators -->

## The cautionary case

One project carried two kinds of design document side by side:

| Document | How it was produced | State |
|---|---|---|
| the token document | generated from the machine-readable token source | correct, live |
| the accessibility, component, and screen documents | hand-written | four months stale, and describing a **palette the product never shipped** |

The hand-written documents described a brand colour that had been abandoned before launch. Every app
rendered a different one. A contributor mining those documents would learn an abandoned decision and
implement it faithfully.

Nothing detected this. There is no gate that compares prose to a product, and there cannot be one for
hand-written prose. The fix was not discipline — it was removing the second writable copy.

## The rule

**One machine-readable source. Every human-readable design document is a rendering of it. A drift
check fails when they diverge.**

```text
design/tokens.json          ← the ONLY writable file
   ├── generated platform targets (one per platform language)
   ├── generated human document  ← the design reference
   └── generated runtime constants (derivation parameters, thresholds)
```

## Generated artifacts: commit, then check

The instinct is to gitignore generated output. For this class of artifact the better trade is the
opposite, and the reasoning is explicit:

| Committing gives | Cost |
|---|---|
| a reviewable diff when a token changes | a regeneration step in the workflow |
| an offline build with no generator run | the risk of a stale committed copy |
| no generator-version dependency in CI | |

**The lost freshness guarantee is replaced by a drift gate**, which is strictly more precise than
"it is always regenerated":

```bash
generate --check      # regenerate in memory, compare, exit non-zero on any difference
```

Three properties the drift gate must have:

1. **Idempotent.** Two consecutive generations from the same source produce no diff. If they differ,
   the generator is nondeterministic and the gate will cry wolf.
2. **Proven to fire.** Inject a change into the generated output by hand, run the check, and confirm
   a non-zero exit. A drift check that has never reported drift is decoration.
3. **Excluded from formatting.** Generated trees must be excluded from the repo's formatter, or the
   formatter rewrites them and the drift gate then reports the formatter's edit as drift — after
   which the team learns to ignore the gate.

## The untracked-and-unused failure

The worst arrangement is neither committed nor ignored: a generated file that sits in the working
tree, is imported by nothing, and has never been executed by anything.

A real instance: one generator backend appended raw serialised data with no declarations onto a
language preamble, producing a file that could not parse. It had never been detected because the file
was untracked, imported by nothing, and that backend had only ever been exercised in theory. The
generator's other backends were fine, which is what made the gap invisible.

> `N files written` is not success. A backend that has never been run is not "working", it is
> unexercised.

Two rules follow:

* **Every generated target is either committed and consumed, or gitignored and not shipped.**
  Untracked-and-unused gets no review and no type-check.
* **Run every target after editing the source.** Generating one target proves one target.

## The document's shape

A generated design document carries, in order:

1. **A generator header** naming the source file, its version, and the command to regenerate. This is
   what makes it obvious that hand-editing is wrong.
2. **The philosophy and the hard requirements**, lifted from the source's notes rather than retyped.
   Requirements recorded only in prose drift; requirements recorded in the source travel with it.
3. **The primitive ramp** with a usage note per entry.
4. **The semantic roles with their contrast partners and both appearances** (see `contrast-pairing.md`).
5. **The scales** — type, spacing, radius, size — each separated, each with its usage note.
6. **The role table**, mapping each role to its scale step.
7. **The per-platform target list**, naming the file each platform reads.

Putting the hard requirements in the source's notes is the highest-leverage detail: a requirement
that lives only in a document is advice, and advice loses to a plausible-looking shortcut.

## Verifying the pipeline

| Check | Command shape | What it proves |
|---|---|---|
| Freshness | `generate --check` | the committed output matches the source |
| Idempotence | run `generate` twice | the generator is deterministic |
| Fires on drift | hand-edit the output, run `--check` | the gate reports drift rather than trusting the file |
| Compiles | each platform's compiler on the generated target | the emitted code is valid in its language |
| Consumed | search for a real import of each target | the target is not dead output |
| Drift in the doc | diff the generated document against a fresh run | the human document is a rendering, not a copy |

## Review questions for this section

1. Is there exactly one writable file holding design values?
2. Does every human-readable design document name its generator in a header?
3. Is the generated output committed, gitignored, or untracked-and-unused?
4. Has the drift gate been shown exiting non-zero on an injected change?
5. Is the generated tree excluded from the formatter?
6. Has every generator backend been executed at least once and its output compiled?
