# Cross-Platform Strategy

<!-- STANDARD: 3min -- native vs. adaptive vs. shared, and framework caveats -->

> **Verification note.** Framework capabilities and rendering defaults change between versions.
> Confirm a framework's current platform-fidelity behaviour against its documentation for the
> installed version.

## The three strategies

| Strategy | What is shared | Fidelity | Cost | Choose when |
|---|---|---|---|---|
| **Native per platform** | Domain layer, data, content | Highest | Highest | Platform capability is the product (widgets, watch, TV, spatial, deep system integration) |
| **Adaptive, one codebase** | Logic + content; UI expressed per platform | High | High | The UI must feel native to be accepted (consumer apps, platform review) |
| **Shared UI, custom language** | Logic + content + UI | Lowest fidelity to platform | Lowest | Internal tools, single-storefront apps, brand-led experiences |

The mistake is choosing the third and *describing* it as the first. A shared UI is a legitimate
business decision; presenting it as platform conformance is not (R3).

## Choosing

```text
Does the product's value depend on platform-specific capability?
├── Yes → NATIVE PER PLATFORM
└── No ↓
    Must the UI feel native to be accepted (storefront, consumers, platform review)?
    ├── Yes → ADAPTIVE
    │   ├── Does the framework render native controls per platform?
    │   │   ├── Yes → use them; fork navigation/gestures per platform
    │   │   └── No  → adopt platform component libraries, or take the shared-UI trade
    │   └── Must navigation differ per platform?
    │       ├── Yes → implement per platform (do NOT unify)
    │       └── No  → share the navigation model
    └── No → SHARED UI (record the trade explicitly)
Finally, in every branch:
  per-platform accessibility, text sizing and motion MUST still be honoured (R6)
```

## The shared / native boundary

This is the boundary that decides whether an adaptive app feels native. Get it wrong in either
direction and the strategy fails: too much shared and the app feels foreign; too much forked and
the maintenance cost consumes the benefit.

### Share

- Domain model, business logic, validation
- Data, networking, persistence
- Content and copy (with length, not convention, as the constraint)
- Information architecture (the *what*, not the *how*)
- Brand identity: colour, imagery, voice, illustration
- Analytics, feature flags, experimentation plumbing

### Fork

| Concern | Why it cannot be shared |
|---|---|
| Navigation model | Back affordance and peer structure are learned per platform |
| Gestures | The gesture vocabulary differs per platform, and conflicts are silent |
| Control behaviour | Hit-target and feedback expectations differ |
| Input handling | Pointer, keyboard, remote, gaze each have their own conventions |
| Motion | Timing, easing and reduced-motion behaviour differ |
| System integration | Permissions, share, widgets, intents are platform APIs |
| Accessibility | Each platform has its own accessibility tree and expectations |
| Typography expression | System text styles carry the user's size setting (see `typography-designer`) |

The table is the practical answer to "how much can we share?" — share everything above the
interaction layer, fork the interaction layer itself.

## Framework caveats

### Flutter

| Property | Consequence |
|---|---|
| Self-drawn widgets by default | The default widget set is *not* a platform convention; shipping it to a platform-targeted app is a recorded trade |
| Platform-adaptive widgets available | Use them for controls where fidelity matters |
| Navigation must be handled per platform | The framework's navigator does not adopt per-platform back conventions automatically |
| Semantics bridge | Verify the platform accessibility tree, not the framework's debug view |

### React Native

| Property | Consequence |
|---|---|
| Renders native primitives | Closer to native fidelity by default |
| Platform-specific files/conditionals | Navigation and gestures still need per-platform handling |
| Native modules available | Reach for them where a convention has no framework equivalent |
| Third-party component sets | Many are shared-UI in disguise; check platform fidelity before adopting |

### Kotlin Multiplatform

| Property | Consequence |
|---|---|
| Two viable routes | Shared Compose UI, or native UI per platform with shared logic |
| Shared Compose UI | Same trade as Flutter: a custom UI, not platform conformance |
| Native UI per platform | Platform conventions come free; this is the high-fidelity route |
| Logic sharing | Excellent; the domain layer sharing is the framework's strength |

### .NET MAUI

| Property | Consequence |
|---|---|
| XAML controls map to native handlers | Good but incomplete fidelity |
| Handler customisation | Available where the mapping is insufficient |
| Verify navigation and gestures | The mapping does not always adopt platform navigation conventions |

## The fidelity audit

Before claiming an adaptive app is platform-native, verify on the real device:

| Check | Method |
|---|---|
| Back behaves per platform | Perform the platform's back gesture from several depths |
| Navigation structure matches | Compare peer/detail structure to the platform convention |
| Controls behave natively | Exercise selection, toggles, pickers, text entry |
| Gestures carry the expected meaning | Swipe on a row; long-press; pinch |
| Focus/input works | Complete the primary task without touch |
| Text sizing honoured | Raise the platform text size to its maximum |
| Accessibility tree populated | Use the platform's inspector and screen reader |
| System affordances are system's | Trigger a permission, share and selection |

Any failure is either a defect or a deviation — there is no third category. Record deviations
(R3), fix defects.

## The cross-platform checklist

- [ ] Strategy chosen (native / adaptive / shared) and recorded per surface
- [ ] Shared/native boundary explicit, not emergent
- [ ] Navigation forked per platform where the platforms differ
- [ ] Gestures fork per platform; conflicts identified
- [ ] Framework's default widgets assessed against platform conventions
- [ ] Accessibility tree verified on each platform, not in the framework debug view
- [ ] Text sizing honoured on each platform at the maximum setting
- [ ] System affordances are the system's
- [ ] Fidelity audit run on real devices for each platform
- [ ] Any shared-UI trade recorded as a trade, with its cost
