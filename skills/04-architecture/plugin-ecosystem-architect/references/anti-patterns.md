# Anti-Patterns

<!-- STANDARD: 3min -- the extension-platform anti-pattern catalogue with detection heuristics -->

## 1. The retrofitted boundary

**Symptom:** extensibility was added after the core shipped; every internal change breaks integrations.
**Cause:** the boundary was designed after the internal design hardened (R1).
**Detection:** do extension points reference internal types, or well-formed abstractions?

**Fix:** replace exposed internals with abstractions; move the rest behind an experimental tier.

## 2. The undeclared contract

**Symptom:** a release breaks many integrations at once, publicly.
**Cause:** no stability tiers and no version-negotiation rule (R2).
**Detection:** is there a published tier table, and does every extension declare a target range?

**Fix:** tiers, a declaration, defined mismatch behaviour, and a deprecation window.

## 3. The unenforced capability

**Symptom:** an extension does something the documentation says it cannot.
**Cause:** capabilities declared but not checked at a chokepoint (R3).
**Detection:** trace a privileged operation from the extension to the primitive. Does anything refuse?

**Fix:** one enforcement chokepoint, default deny, a typed refusal, and an audit log.

## 4. The omnibus capability

**Symptom:** every extension requests the same broad permission; users click through.
**Cause:** capabilities designed for the platform's convenience, not for consent.
**Detection:** read the consent screen as a user. Can they make a meaningful choice?

**Fix:** intent-named, independently grantable capabilities.

## 5. The trusted-all-partner model

**Symptom:** third-party code runs in-process with host authority.
**Cause:** the trust model assumed today's partners are tomorrow's partners (R5).
**Detection:** can an extension reach a raw primitive at all?

**Fix:** a named isolation mechanism per class; state the trust boundary explicitly.

## 6. The missing removal path

**Symptom:** a malicious or broken extension cannot be removed at scale.
**Cause:** no disable, rollback or revocation state (R4).
**Detection:** walk the lifecycle. Can you disable it? Roll it back? Revoke it?

**Fix:** disable, rollback and revoke as first-class states, with offline behaviour defined.

## 7. Silent capability expansion

**Symptom:** an update gains capabilities the user never agreed to.
**Cause:** expansion treated as an update, not as a new consent.
**Detection:** does an update that adds a capability require re-consent?

**Fix:** expansion is a consent event; declining keeps the old version or grants.

## 8. Unload-and-reload lifecycle

**Symptom:** every extension update requires a host restart.
**Cause:** the lifecycle assumed unload works (see `library-linkage-architect`).
**Detection:** does the design mention unloading as the update mechanism?

**Fix:** version and load alongside; accept bounded resident versions.

## 9. Unsigned distribution

**Symptom:** a compromised or substituted update cannot be distinguished from a legitimate one.
**Cause:** no signing, or verification treated as a warning.
**Detection:** is every artefact signed, and does the host refuse unverified ones?

**Fix:** sign everything, verify before executing, support key rotation.

## 10. The un-actionable error

**Symptom:** developers cannot diagnose a load failure; support volume is high.
**Cause:** errors name the symptom, not the cause or the fix.
**Detection:** read the host's error strings. Do they say what to do?

**Fix:** cause, next action, and a link to the specific fix (see `developer-experience.md`).

## 11. The empty first hour

**Symptom:** the platform launches; few extensions appear.
**Cause:** no scaffold, no local host, no test harness (R6).
**Detection:** time a real developer from start to a working extension.

**Fix:** scaffold, local host, test harness, one-command packaging.

## 12. The silently degraded extension

**Symptom:** an extension behaves inconsistently across versions, with no explanation.
**Cause:** degradation without telling the extension or the user.
**Detection:** when a capability is unavailable, does anything say so?

**Fix:** degrade honestly — disable the feature, tell the user, tell the extension.

## 13. The moved boundary

**Symptom:** the platform ships a feature that a successful partner's extension provided.
**Cause:** the platform-versus-partner boundary was never published, or was not honoured.
**Detection:** is there a written line, and did the roadmap respect it?

**Fix:** publish the boundary; honour it. The cost of a single violation is the whole ecosystem's trust.

## 14. Internal types as extension points

**Symptom:** the platform cannot refactor without breaking extensions.
**Cause:** convenience — the internal type was already there.
**Detection:** do any published extension points reference host-internal structures?

**Fix:** opaque handles and intent-level operations.

## 15. No DX enforcement of the real constraints

**Symptom:** extensions work locally and fail at install.
**Cause:** local development granted all capabilities, so the model was never exercised.
**Detection:** does local development enforce the capability set?

**Fix:** enforce locally; the developer discovers the model before publishing.

## Detection sweep

```bash
SRC="${1:-src}"

echo "== extension manifest: does it declare identity, version and target range? =="
find . -iname '*manifest*.json' -not -path '*/node_modules/*' 2>/dev/null | head -5 | while IFS= read -r f; do
  echo "--- $f"; grep -oE '"(id|version|targets|capabilities)"' "$f" 2>/dev/null | sort -u
done

echo "== stability tiers published? =="
find . -iname '*stability*' -o -iname '*compat*matrix*' 2>/dev/null | head || echo "  NONE"

echo "== capability enforcement chokepoint (look for the check, not the declaration) =="
grep -rnE 'hasCapability|checkCapability|requireCapability|capability.*granted' "$SRC" 2>/dev/null | head || echo "  NONE — capabilities may be declared but unenforced"

echo "== isolation mechanism =="
grep -rnE 'wasm|isolate|Sandbox|child_process|spawn|Worker|subprocess' "$SRC" 2>/dev/null | head -5 || echo "  NONE — likely in-process"

echo "== lifecycle: disable / revoke / rollback =="
grep -rniE 'disable|revoke|rollback|uninstall|remove' "$SRC" 2>/dev/null | wc -l | xargs echo "  lifecycle references:"

echo "== signing / verification =="
grep -rniE 'signature|verify|publicKey|checksum' "$SRC" 2>/dev/null | head -5 || echo "  NONE — unsigned distribution"

echo "== DX: scaffold / template / local dev =="
find . -iname '*template*' -path '*plugin*' -o -iname '*scaffold*' 2>/dev/null | head || echo "  NONE — no scaffold"

echo "== actionable errors =="
grep -rnE '"[^"]*(could not load|failed to load|incompatible)[^"]*"' "$SRC" 2>/dev/null | head -3
```

Interpretation: **no enforcement chokepoint** with **declared capabilities** is the highest-severity
finding in this sweep — it is a control that does not exist. **No signing** means the distribution model
cannot be trusted. **No scaffold** predicts an ecosystem that never forms.
