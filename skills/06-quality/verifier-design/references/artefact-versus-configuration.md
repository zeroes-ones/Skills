# Artefact Versus Configuration — verify the bundle, not the settings

> The most common shape of a silent miss in the source corpus: **declared in configuration, absent
> from the artefact, zero build signal.** No warning, no failed test, no linter finding.

---

## The pattern

```
DECLARED                        WHERE                    ABSENT FROM
-----------------------------   ----------------------   -------------------------
A resources directory as a      project configuration    the app bundle
  target source
A custom Info.plist key         project configuration    the built Info.plist
An entitlements file + setting  both, correctly          the signature (empty dict)
A privacy manifest              the source tree          the bundle; and the
                                                          repository "treats it as done"
A debug signing certificate     the build config         the certificate the OAuth
                                                          client was registered against
```

Every row has the same property: **the configuration is correct and the behaviour is absent.** The
check that settles each one reads the built output:

| Question | Command shape |
|----------|---------------|
| Is the resource directory in the bundle? | List the built package's `.lproj` directories |
| Did the custom plist key reach the bundle? | `plutil -p` on the built app's `Info.plist` |
| What does the signature actually carry? | `codesign -d --entitlements :-` on the built app |
| Is the privacy manifest inside the bundle? | Inspect the built package's contents, not the source tree |
| What package name will the SDK see? | Grep the **merged** manifest |
| What certificate signed the artefact? | `apksigner verify --print-certs` on the built APK |

---

## Why this class is invisible

Each available signal is silent for its own reason, and the reasons do not overlap:

| Signal | Why it stayed silent |
|--------|---------------------|
| The compiler | Nothing is malformed. The key is declared, the source is valid, every reference resolves |
| The test suite | No test asserted the property; a test would have to read the bundle, and tests usually read the code |
| The linter | The config file is well-formed and passes its schema |
| The reviewer | The reviewer reads the config, sees the setting, and confirms it — the config *is* correct |
| The build | Succeeds. A silently dropped key is not a build error |

The reviewer is the important row. Reading the configuration confirms the declaration, which is
exactly the thing that is not in doubt. **The doubt is in the injection step, and only the output
can speak to it.**

### The specific mechanisms worth knowing

| Mechanism | What happens |
|-----------|-------------|
| A build setting that injects **only known keys** | `INFOPLIST_KEY_<custom>` is silently dropped for a key the toolchain does not already know. Declared in config, build succeeds, key absent. |
| A resources directory not registered as a **target source** | The files exist, the directory is declared in the project file, nothing bundles them. The app resolves every key and renders raw key text — which is worse than a literal, because it looks finished |
| An entitlement granted by a **profile, not a plist** | A correct `.entitlements` file plus a correct `CODE_SIGN_ENTITLEMENTS` can still sign with an empty dict. And the simulator does not enforce entitlements, so it hides the gap until a device |
| A debug-only **package suffix** | `applicationIdSuffix = ".debug"` distinguishes builds and silently invalidates every OAuth/push/deep-link registration, all of which are keyed on the exact package name |

---

## Stale versus wrong

The follow-on trap: **an artefact is a cache.** Reading it too early confirms a fix that has not
taken effect.

Two instances from the same corpus:

1. After changing an application ID, the merged manifest still reported the old package name until
   the intermediates directory was cleared. Reading it before clearing would have "confirmed" a fix
   that had not happened.
2. A device showed "not configured" for an OAuth client while the client ID was present in the dex
   and the code was correct — the **installed APK predated the source edits**.

From outside, "the artefact is wrong" and "the artefact is stale" are indistinguishable. The
discriminator is a **count of something only the current source names**:

```
Source contains 25 entries of the auth.errors.* family.
Built APK contains 24.

→ An artefact that cannot render a value the current source names is not the current source.
```

That single comparison separates the two diagnoses in one step, and it is cheaper than any amount
of reading the code.

### Generalisation

> A generated artefact is a cache. Anything that changes the file set invalidates it — including a
> generator that now emits a different **number** of files.

The concrete case: after a generator began emitting 138 files where it had emitted one, the project
file still listed the deleted monolith and none of its replacements. The configuration was right;
the generated artefact was stale.

---

## What to check instead

A procedure that replaces "was the configuration correct?" with "did the value arrive?":

```
For each property the shipped artefact must have:

  1. NAME the property in the form the runtime sees it
       not "the API base URL is configured" but "Info.plist carries APIBaseURL"

  2. NAME the command that reads it from the SHIPPED artefact
       plutil -p, a bundle listing, a resource table dump, a signature dump

  3. CONFIRM the artefact is current
       a count of something only the current source names, or a timestamp you trust

  4. RUN the command and record the output
       the output, not the fact that the command ran

  5. Make step 4 a gate when the property is load-bearing
       a check that reads the artefact becomes the signal that was missing
```

Step 3 is the one that is easy to skip and expensive to omit. Step 5 is what converts a one-time
discovery into coverage.

---

## The three failure directions

| Direction | Example | Signal |
|-----------|---------|--------|
| **Declared but absent** | A custom plist key silently dropped; a localisation source never bundled | None until the artefact is inspected |
| **Present but ineffective** | Entitlements in file and setting, empty in the signature; a dependency in the lockfile but not in the compiled output | None until the artefact is inspected |
| **Present, effective, wrong value** | The signed artefact carries a different certificate than the one registered upstream; the merged manifest reports a suffixed package | An opaque upstream error that names neither side |

The third direction is worth its own note: a third-party console error like
`[28444] Developer console is not set up correctly` names nothing. Two independent things cause it —
package name and signing certificate — and **neither is readable from the configuration.** Both are
readable from the artefact. When an upstream error names nothing, the response is to read every
artefact property the upstream service validates and compare each against its registration.

A related rule: **match the tool to the input.** `keytool -printcert -jarfile` answers "Not a signed
jar file" for an APK; `apksigner verify --print-certs` is the tool that reads it. A tool that cannot
read the input does not report a fact about it — it reports a fact about the tool.

---

## Anti-patterns

| ❌ | ✅ |
|----|----|
| "The key is in the config, so it ships" | Run the command that reads the built bundle and record its output |
| "The build succeeded, so the resource is bundled" | List the bundle's contents; a green build says nothing about inclusion |
| "The signature is correct because the entitlements file is" | `codesign -d --entitlements :-` on the built app |
| "The manifest says our package is X" | The **merged** manifest — that is the one the platform and the SDK read |
| Reading a build intermediate without clearing it first | Clear, rebuild, then read; stale and wrong look identical otherwise |
| Trusting a lockfile as proof of a shipped dependency | Inspect the compiled output for the symbol; the lockfile proves resolution only |
| Using a jar/zip tool on an APK or a bundle | Use the platform's own verification tool |
