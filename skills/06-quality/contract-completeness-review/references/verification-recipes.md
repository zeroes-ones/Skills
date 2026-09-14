# Verification Recipes

The eight checks from the skill's Verification section, as runnable procedures. Each states what it
proves and what it cannot see.

## 1. Inventory

**Proves:** every shared contract is on the list.

```bash
# Contracts with more than one implementation or consumer
grep -rn --include='*.kt' --include='*.swift' --include='*.ts' --include='*.py' \
  -E '^\s*(public\s+)?(interface|protocol|trait|abstract class)\s+\w+' src/ \
  | sed -E 's/.*(interface|protocol|trait|abstract class)\s+([A-Za-z0-9_]+).*/\2/' \
  | sort -u
```

For each name, count implementations: `grep -rn ": <Name>" --include='*.kt'` (Kotlin), `": <Name>"`
on a type declaration (Swift), `"implements <Name>"` (TS/Java). One implementation means the bypass
grid records `N/A`; two or more makes it mandatory.

**Cannot see:** a contract expressed as a message schema, an OpenAPI component, an event payload, or
a generated interface. Add those sources by hand.

## 2. Operation set derived from behaviour

**Proves:** the required set came from behaviour, not from the interface. This is a manual step and
cannot be automated; the check is procedural.

```
Sources to enumerate:
  [ ] every call site of the contract's members
  [ ] every screen, job, or flow that reads the datum the contract describes
  [ ] every persisted field backing that datum
  [ ] every user-visible state transition (create, edit, delete, sign out)
  [ ] every error or recovery path that must change the datum

Mark each operation [VERIFIED] (a call site or a flow you read)
                 or [ESTIMATED] (an assumption about behaviour you could not reach)
```

An inventory with no `[ESTIMATED]` entries on a codebase you did not fully search is a sign the
inventory was read off the interface instead.

## 3. Writer check

**Proves:** every read has a named writer on the same seam.

```bash
# Reads without writes, by naming convention
for accessor in has is get current state status; do
  grep -rn --include='*.kt' --include='*.swift' -E "fun (${accessor}[A-Z]\w*)\(|func (${accessor}[A-Z]\w*)\(" src/ \
    | grep -v 'Test\|Mock\|Fake'
done
```

For each read found, name its writer by hand and record the seam. The mechanical part is the
enumeration; the finding is the naming.

**Cannot see:** a reader whose writer exists but is never called (a frozen initialiser), which is why
step 2 lists state transitions.

## 4. Symmetry check

**Proves:** the contract can express a complete lifecycle.

For each contract, list its members and place each against the lifecycle table in
`writer-reader-audit.md`: create, read, update, delete, observe. Any operation with no member is a
finding.

```
contract: SessionStore
  create   → MISSING                    ← finding
  read     → hasSession()
  update   → MISSING (folded into create)
  delete   → clear()
  observe  → n/a
```

## 5. Bypass map

**Proves:** where the contract is actually load-bearing.

```bash
# Direct access to the thing the contract abstracts, per implementation
grep -rn --include='*.kt' -E 'EncryptedSharedPreferences|getSharedPreferences|SQLiteDatabase|OkHttpClient' android/ \
  | grep -v 'SessionStore\|Test'
grep -rn --include='*.swift' -E 'SecItemAdd|SecItemCopyMatching|UserDefaults|URLSession' ios/ \
  | grep -v 'SessionStore\|Tests'
```

Each hit is a candidate `BYPASS` cell. Confirm by reading whether the operation the contract also
exposes is performed there.

| | iOS | Android | Fake |
|---|---|---|---|
| create | | | |
| read | | | |
| delete | | | |

A blank cell is an unfinished audit. `N/A (one implementation)` is a valid entry; blank is not.

## 6. Evidence check

**Proves:** at least one assertion derives from behaviour, and the round trip is capable of failing.

```bash
git diff --stat -- '**/*Mock*' '**/*Fake*' '**/*Stub*'   # count of fakes touched by the change
```

Zero fakes touched means the contract change was cosmetic. Then run the removal check from
`round-trip-assertions.md`: remove the operation, confirm the assertion fails, restore it.

**Cannot see:** whether the assertion is placed where every implementation runs it. Check the
placement separately — port-level or shared-domain, not adapter-local.

## 7. Reachability

**Proves:** every declared member is exercised, or is deliberately not.

```bash
# Call sites per member, excluding declaration and test sites
for m in hasSession clear save; do
  n=$(grep -rn --include='*.kt' --include='*.swift' "\.$m(" src/ | grep -v Test | wc -l | tr -d ' ')
  echo "$m: $n call site(s)"
done
```

Zero is a finding until classified: **superseded** (remove), **external contract** (keep, name the
consumer), or **generated-unapplied** (defect — add the call site).

## 8. Reverse direction

**Proves:** the conformance check is bidirectional.

```
1. Add an operation to the implementation only (not to the declaration).
2. Run the conformance check.
3. Green → the reverse direction is a no-op. That is the finding.
4. Remove the addition.
```

Do this once per conformance check, not once per project — a check that was bidirectional last year
can acquire a no-op branch in a refactor, exactly as the source instance did.

## Composite runner

`scripts/verify-skill.sh` in this skill directory echoes all eight checks as a checklist. It is a
harness for the reviewer, not an automated gate: six of the eight need a human to decide what the
system must be able to do, and a script that pretends otherwise would manufacture the confidence
this skill exists to remove.
