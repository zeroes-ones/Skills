# Lifecycle

<!-- STANDARD: 3min -- discovery, install, replace, disable, rollback, remove, and data handling -->

## Why lifecycle is a ground rule

R4 exists because a platform that cannot disable and remove an extension has **no response to
third-party harm**. The first malicious extension, the first badly broken update, the first
supply-chain compromise — each requires a removal path, and if none exists the only remedy is removing
the feature.

## The seven states

| State | Who initiates | Requirement |
|---|---|---|
| **Discover** | user | the extension is findable, with its capabilities and publisher visible |
| **Install** | user | capabilities are consented to before it activates |
| **Enable / disable** | user or platform | a non-destructive way to stop an extension working |
| **Update** | user, publisher, or platform | with the capability-expansion consent rule |
| **Rollback** | user or platform | return to a known-good version |
| **Revoke** | platform | force-disable across installs (abuse response) |
| **Remove** | user | with defined data handling |

## Replace: the mechanism matters

How an updated extension takes effect is a design decision with real consequences.

| Mechanism | Effect | Fit |
|---|---|---|
| Reload the host | simplest; every user restarts | rare-update hosts, desktop apps at quit |
| **Load the new version alongside** | the new version serves new work; the old stays resident | **preferred** for always-on hosts |
| Unload and reload | what everyone wants and cannot rely on | do not design on this |

**Why unload-and-reload is not dependable:** a shared object is unloaded only when its reference count
reaches zero and nothing else references it — registered callbacks, thread-local storage and destructors
all prevent it, and reload does not guarantee re-initialisation. *(Source: `dlopen(3)`, Linux
man-pages.)* The full mechanism belongs to `library-linkage-architect`; the design consequence belongs
here: **version and load alongside, accept bounded resident versions.**

## The capability-expansion rule

```text
Update adds capabilities the user has not granted →
├── Do NOT grant them silently
├── Present the expansion as a change to the user
│   ├── Accept → the new capabilities are granted, the extension updates
│   └── Decline → the extension keeps its OLD grants and the OLD version, or
│                 updates without the new capability (degraded), per design
└── Record the decision
```

**Silent expansion is the single most trust-destroying lifecycle behaviour.** An update that gains file
access without telling the user is indistinguishable from an attack.

## Rollback

Required for remediation. Without it, a bad release from a competent publisher is permanent for every
user who took it.

| Requirement | Why |
|---|---|
| A user can pin a version | stops an unwanted update |
| A user can return to a previous version | recovers from a bad release |
| The platform can force a rollback | recovers at scale |
| The previous version is retained or re-fetchable | otherwise a rollback is a re-install |
| Data written by the newer version is handled | a rollback must not corrupt or lose it |

The last row is the one teams miss: a rollback that leaves data in a newer schema can be worse than the
bad release.

## Revocation

The platform-level version of disable, and the only mechanism that works at scale.

| Element | Detail |
|---|---|
| **Trigger** | a security finding, an abuse report, a publisher compromise, a policy violation |
| **Mechanism** | a signed revocation list the host checks, or a server-side kill signal |
| **Effect** | the extension is force-disabled, with a user-visible explanation |
| **Offline behaviour** | define it — an unreachable revocation list must not silently disable everything, nor silently fail open |
| **Appeal** | a publisher needs a path to contest, or the mechanism is a liability |
| **Communication** | users must understand why something stopped working |

**The offline case is the subtle one.** A host that cannot reach the revocation list must decide: fail
open (keep running), fail closed (disable), or honour a cached list with a staleness bound. Each is
defensible; leaving it undefined is not.

## Removal, and what happens to data

| Data | Options | The rule |
|---|---|---|
| Extension's configuration | delete, or retain for re-install | state which |
| User content the extension created | preserve; it is the user's | never delete the user's data on uninstall without explicit consent |
| Credentials the extension stored | revoke or delete | removing an extension should revoke its access |
| Host-side state attributed to it | clean up | otherwise removal leaves debris |

**Removal must revoke access.** An uninstalled extension that still holds an API token or an OAuth
grant has not been removed in any meaningful sense.

## Failure containment in the lifecycle

| Failure | Containment |
|---|---|
| Extension fails at load | host continues; the failure is surfaced for that extension only |
| Extension fails during use | disable that extension, keep the host running, tell the user |
| Extension update fails | keep the previous version working |
| Extension exhausts resources | per-extension limits, and disable on breach |
| Host update breaks an extension | the version-negotiation outcome (see `stability-contract.md`) |

## User-visible states

The user should always be able to tell what is installed, what it can do, and what state it is in:

```text
My Extensions
├── My Extension 2.1.0        [publisher]  Active     Can: see your content, connect to the internet
├── Another Extension 1.4.0   [publisher]  Disabled   Can: see your settings
└── Broken Extension 0.9.0    [publisher]  Failed     Could not load (incompatible with this version)
```

The `Failed` state with a reason is what makes support tractable.

## Checklist

- [ ] Every extension state is reachable: discover, install, disable, update, rollback, revoke, remove
- [ ] Capability expansion requires consent, never silent granting (R4-adjacent)
- [ ] Replacement uses versioned loads, not unload-and-reload
- [ ] Rollback exists, including handling of data written by the newer version
- [ ] Revocation exists, with defined offline behaviour and a publisher appeal path
- [ ] Removal revokes credentials and tokens, and states what happens to configuration
- [ ] User content is never destroyed on uninstall without explicit consent
- [ ] Every lifecycle failure has a containment story
- [ ] The user can see each extension's state, version and capabilities
- [ ] Every lifecycle step has been exercised end to end in a rehearsal (Phase 9)
