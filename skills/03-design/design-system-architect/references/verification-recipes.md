# Verification Recipes

<!-- STANDARD: 3min — the eight verification checks as runnable procedures -->

Each recipe states the check, the command shape, the pass condition, and the failure it exists to
catch. Names are illustrative; substitute the project's own generator, gate, and target paths.

## 1. Tier check

**Check.** Every token sits in exactly one tier, and no screen reads a primitive.

```bash
# the generated artifact is the vocabulary source; a script's own list is the defect
python3 scripts/check-theme-compliance.py
python3 scripts/check-theme-compliance.py --list     # every scanned file, to prove the scope is real
```

**Pass.** Zero findings, and the `--list` output covers every screen (a gate with an empty scope
reports clean).

**Catches.** A screen reading a primitive swatch — invisible in the author's own appearance setting.

## 2. Role check

**Check.** Every control names one role across every platform.

```bash
python3 scripts/check-design-parity.py
python3 scripts/check-design-parity.py --strict      # warnings become errors
```

**Pass.** Zero role-vocabulary findings; every call site names a role in one of the platform's
accepted spellings.

**Catches.** A call site spelling a raw scale member or a vendor slot, which is how the two platforms
diverged silently.

## 3. Rank check

**Check.** The platform mapping is monotonic in rendered size, and the assertion fires on an
inversion.

```bash
# 1. generate from the source; the generator asserts the rank and refuses an inversion
generate --tokens
# 2. inject the inversion: swap two adjacent steps' mapped styles in the source
# 3. re-run — MUST exit non-zero and name both steps and both rendered sizes
# 4. restore — MUST exit zero
generate --tokens
```

**Pass.** The injected inversion is refused with a message naming both steps; the restored source
generates cleanly.

**Catches.** A larger brand step landing on a smaller rendered size — the inverted ladder that
compilers do not see.

## 4. Axis check

**Check.** No component dimension reads a spacing token and no gap reads a size token.

```bash
# a size token whose value equals a spacing token deserves an explicit look
python3 - <<'PY'
import json
t = json.load(open('design/tokens.json'))
sizes = {v['px'] for v in t['size']['scale'].values()}
spacing = {v['px'] for v in t['spacing']['scale'].values()}
for v in sorted(sizes & spacing):
    print(f"coincident value {v}: confirm the size token is named for what it sizes, not the gap it matches")
PY
```

**Pass.** Every coincident value carries a size token whose name states what it sizes.

**Catches.** A control size coupled to the page rhythm, which resizes silently on the next retune.

## 5. Pairing check

**Check.** Every text or icon role names the role it is painted on, and that pair meets the floor.

```bash
python3 scripts/check-contrast-pairs.py             # or the generated pairing table
```

**Pass.** Every role with a text or icon consumer has a named partner, and each pair meets the
declared floor in **both** appearances.

**Catches.** An `on` role measured against the page background — a real number for a pair that never
renders.

## 6. Floor check

**Check.** Each platform minimum is its own token, naming its guideline.

```bash
grep -n 'tapTarget\|hitTarget\|minTouch' design/tokens.json
# every entry should name a platform and the guideline it satisfies
```

**Pass.** One token per platform where the published minimums differ, each with its source stated in
the token's usage note.

**Catches.** A single floor token applied to platforms whose specified minimums differ.

## 7. Provenance check

**Check.** Every human-readable design document is generated, and drift fails.

```bash
head -3 design/tokens.md                 # the generator header must be present
generate --check                          # exit non-zero on any difference
# prove it fires
printf '\n<!-- deliberate drift -->\n' >> design/tokens.md
generate --check                          # MUST exit non-zero
git checkout design/tokens.md
generate --check                          # MUST exit zero
```

**Pass.** The header names the source; the check is idempotent; the injected drift is reported.

**Catches.** A hand-written document restating values the source no longer holds.

## 8. Gate check

**Check.** Every conformance gate has been shown exiting non-zero on an injected violation and
naming file:line, then silent when restored.

```bash
# per gate, per rule class
sed -i '' 's/<roleBackground>/<rawPrimitive>/' <screen>
python3 scripts/check-theme-compliance.py     # MUST exit 1 and name file:line
git checkout <screen>
python3 scripts/check-theme-compliance.py     # MUST exit 0
```

**Pass.** Both runs behave as stated, for **every** rule class — including the classes added most
recently.

**Catches.** A gate whose clean report proves nothing, and an exemption list that has quietly grown
to cover the violations.

## The full pass condition

All eight checks pass before a token system is called done. Where one cannot be run — no generator
harness, no per-platform resolution possible — say so explicitly rather than recording a pass. An
unverified check reported as passing is the exact failure this skill's rules exist to prevent.
