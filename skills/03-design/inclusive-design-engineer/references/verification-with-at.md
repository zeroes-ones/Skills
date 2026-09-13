# Verification with Assistive Technology

<!-- DEEP: 5+min -- the verification protocol per AT, platform and browser -->

## Why the protocol exists

**R2 is the rule that makes remediation real.** Assistive-technology behaviour differs by AT, by
platform and by browser — the same markup can announce differently in each combination. A fix
asserted from documentation is a hypothesis; a fix observed in a named combination is evidence.

This file is the protocol that turns a fix into evidence.

## The combinations that matter

You do not need every combination. You need a small set that covers the platforms you ship to, and
you must record which one you used.

| Platform | Screen reader | Browser | Covers |
|---|---|---|---|
| macOS | VoiceOver | Safari | The Apple-native path |
| macOS | VoiceOver | Chrome | Chromium on the Apple platform |
| Windows | NVDA | Firefox | The most-used Windows combination |
| Windows | NVDA | Chrome | The dominant browser on Windows |
| Windows | JAWS | Chrome | A widely deployed commercial AT |
| iOS | VoiceOver (touch) | Safari | The mobile touch path |
| Android | TalkBack | Chrome | The Android path |

**The minimum defensible set** for a web product: one desktop combination per OS you ship to, plus
one mobile combination. For a native app: the platform's own screen reader on each platform.

The point is not exhaustiveness — it is that the combination is *named* and the result *recorded*,
so the verification can be reproduced and its limits understood.

## The verification protocol

```text
For each fixed component:
  1. Name the AT + platform + browser being used. Write it down BEFORE testing.
  2. Navigate to the component using only the keyboard (pointer disabled).
  3. Record the announcement verbatim: role, name, state, and any description.
  4. Operate the component fully: every key in its contract, every state change.
  5. Confirm the accessible name matches the visible label.
  6. Confirm every state change is announced (or deliberately not).
  7. Open any overlay it controls: focus in, contained, restored.
  8. Tab away and confirm the component does not trap focus.
  9. Record the outcome: PASS, FAIL (with the observed behaviour), or UNVERIFIED.
 10. If UNVERIFIED (the combination was unavailable), SAY SO. Do not imply success.
```

Step 10 is not a formality. An honest "unverified" is recoverable; a false "verified" becomes a
finding in the next audit and erodes trust in the whole process.

## What to record

| Field | Example |
|---|---|
| Component | `Dialog` |
| AT / platform / browser | VoiceOver, macOS 15, Safari |
| Name announced | "Delete project, dialog" |
| State announced | modal, title read on open |
| Keyboard contract | Tab cycles inside; Escape closes; focus returned to "Delete project" button |
| Result | PASS |
| Notes | Background not read while open (verified by attempting to read the page behind) |
| Unverified | NVDA on Windows not tested — no environment available |

The `Unverified` field is what makes the record honest.

## Verification is not testing for regressions

Two different activities, often conflated:

| Activity | Purpose | Owner |
|---|---|---|
| **AT verification** | Confirm the fix works for a real user of that AT | This skill (Phase 5) |
| **Regression guard** | Confirm the fix does not silently break again | This skill (Phase 6) and `accessibility-testing` |

Verification happens once per fix, manually, with the AT. The guard runs continuously, automatically,
and asserts the accessible *outcome* (a name, a role, a state, a focus position) rather than a pixel.

Both are required. Verification without a guard means the fix decays; a guard without verification
means the assertions may be guarding the wrong thing.

## What can be verified without assistive technology

Some properties are checkable mechanically, and these should be checked first to avoid wasting AT
time on the obvious:

| Property | How |
|---|---|
| Accessible name present | The platform's accessibility inspector |
| Role and state | The inspector's tree |
| Focus order and focus visibility | A keyboard walkthrough, with the pointer disabled |
| Keyboard operability | Complete the task with the keyboard only |
| Focus containment and restoration | Tab through an overlay and close it |
| Contrast ratios | The computation (see contrast-and-colour.md) |
| Text scaling | Set the root size / platform text size to maximum |
| Reduced motion | Enable the preference and observe |

The inspector shows *what* the AT will be told; the AT shows *how* the user experiences it. Both are
useful, and the inspector first makes the AT session much shorter.

**The cross-platform trap:** a framework's own semantics view may map only partially to the
platform's accessibility tree. A green result in the framework's debug view with an empty platform
tree is a real and common failure. Always confirm on the platform's own inspector.

## The accessibility tree check

```text
1. Open the platform's accessibility inspector.
2. Confirm the tree contains the elements you expect, with the right roles.
3. Confirm names are populated (not empty, not the raw text of an icon).
4. Confirm states are present (expanded, selected, checked, invalid).
5. Confirm the reading order matches the visual order.
6. Confirm nothing focusable is absent from the tree (the aria-hidden defect).
```

Step 6 catches the worst class of defect: an element reachable by keyboard but invisible to AT, so a
keyboard user lands on an unnamed, roleless element.

## Recording template

```markdown
### Verification — <component> — <date>

| Field | Value |
|---|---|
| AT | <VoiceOver / NVDA / JAWS / TalkBack> |
| Platform | <OS + version> |
| Browser | <browser + version> |
| Navigated by | keyboard only / AT only / both |
| Announcement | "<verbatim record>" |
| States announced | <list> |
| Keyboard contract observed | <keys and outcomes> |
| Focus in / contained / restored | yes / yes / yes |
| Result | PASS / FAIL / UNVERIFIED |
| Evidence | <recording, screenshot, log> |
| Unverified combinations | <list, or "none"> |
```

## The verification checklist

- [ ] The AT, platform and browser are named before testing begins (CR12)
- [ ] The announcement is recorded verbatim, not summarised
- [ ] Every key in the component's contract was exercised
- [ ] State changes were confirmed announced, or deliberately not
- [ ] Focus entry, containment and restoration were confirmed
- [ ] The accessible name matches the visible label
- [ ] No focusable element is missing from the accessibility tree
- [ ] The verification is recorded with its unverified combinations listed
- [ ] Unverified combinations are reported as unverified, never as passing
- [ ] The platform's own inspector was used, not a framework's semantics view
