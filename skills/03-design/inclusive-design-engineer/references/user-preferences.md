# User Preferences

<!-- STANDARD: 3min -- reduced motion, contrast, colour scheme and text scaling -->

## Why preferences are requirements

The user's system preferences are how they tell every interface how to behave for them. Honouring
them is not a courtesy; it is the mechanism by which a user with a vestibular disorder, a
photosensitivity, or a low-vision condition uses the product at all.

There are four that matter most for inclusive implementation. Each has a media query for the web and
an equivalent system setting for native platforms.

## Reduced motion

```css
@media (prefers-reduced-motion: reduce) {
  /* Substitute, do not delete */
  .panel   { transition: none; transform: none; }      /* no travel */
  .fade-in { transition: opacity 120ms linear; }       /* opacity generally acceptable */
  .spinner { animation: none; }                        /* keep the status text instead */
}
```

| Requirement | Detail |
|---|---|
| Honour the preference | Replace motion with an instant or opacity change |
| Do not remove necessary feedback | The in-flight state and status text remain; only the travel goes |
| Avoid large-field motion regardless | Parallax, full-screen slides, and camera movement |
| Provide a non-motion equivalent | A progress bar that does not animate still communicates |

**The two errors:** ignoring the preference entirely (the common defect), and taking it as licence to
remove all feedback so the interface becomes unusable in a different way. The correct response is
substitution, and this is why AR-01-style rigour applies: state what the substitution is.

## Increased contrast

```css
@media (prefers-contrast: more) {
  :root {
    --text-secondary: var(--text-primary);      /* collapse the secondary tone */
    --border-subtle: var(--border-strong);
    --focus-ring: 3px;                           /* thicker indicator */
  }
}
```

| Requirement | Detail |
|---|---|
| Increase text and border contrast | Collapse subtle tones toward the primary |
| Strengthen boundaries | Input borders, dividers, control outlines become visible |
| Strengthen the focus indicator | Thicker, or higher-contrast |
| Do not rely on brand colour | The preference may override the palette entirely |

This preference is used by people for whom the standard palette is not legible. Brand fidelity
yields to it.

## Colour scheme

```css
:root { color-scheme: light dark; }                  /* opt in to the user's choice */

@media (prefers-color-scheme: dark) { /* dark tokens */ }
@media (prefers-color-scheme: light) { /* light tokens */ }
```

| Requirement | Detail |
|---|---|
| Respect the preference by default | Do not force a theme without a user-facing choice |
| Verify contrast in **both** themes | The dark theme is where focus rings and secondary text fail |
| Handle elevation in dark mode | Higher surfaces are lighter, not shadowed |
| Keep the user's explicit choice | An in-app override should persist and win over the system preference |

The most common defect here is a focus ring designed for light surfaces becoming invisible in dark
mode. Verify the indicator per theme (see contrast-and-colour.md).

## Text scaling

| Platform | Mechanism |
|---|---|
| Web | The user's root font size, plus browser zoom |
| Native | The platform's text-size setting, which scales text styles |

| Requirement | Detail |
|---|---|
| Text sizes are relative | So the user's preference has an effect (see `typography-designer`) |
| Layout survives the maximum scale | No clipping, no overlap, no truncation of essential text |
| Reflow rather than scroll | At high zoom, content reflows to one dimension |
| Spacing preferences honoured | If the user overrides spacing, nothing is lost |

A component that breaks at the largest text size is a component that breaks for the users who need
the largest text size, which is precisely the audience the setting exists for.

## Other preferences worth honouring

| Preference | Why |
|---|---|
| Forced colours / high contrast mode | The user's palette wins; do not fight it with fixed colours |
| Transparency reduction | Reduce translucency; provide opaque surfaces |
| Animations from the OS (native) | The platform-level equivalent of reduced motion |
| Bold text (native) | The platform's heavier-weight preference |

## Implementation rules

1. **Query the preference, do not guess it.** Use the media query or the platform API; never infer
   from another signal.
2. **Substitute, do not strip.** Every preference has a correct non-degrading response.
3. **Verify each preference as a distinct test case.** A preference that was never enabled is a
   preference that does not work.
4. **Keep the preference orthogonal to the feature.** Reduced motion changes *how* something is
   presented, not *whether* it works.
5. **Re-verify after a theme or palette change.** Preferences interact with tokens.

## The preference test matrix

```text
For each of: reduced motion / increased contrast / dark theme / light theme /
             maximum text size / forced colours
  1. Enable the preference.
  2. Complete the primary task.
  3. Confirm: nothing is lost, nothing is clipped, everything remains perceivable.
  4. Confirm necessary feedback survives (especially with reduced motion).
  5. Record the combination tested.
```

Six preferences, five minutes each, and they catch the defects that only appear for the users who
set them — which is exactly the group a default-configuration test never reaches.

## The preferences checklist

- [ ] Reduced motion honoured, substituting an instant or opacity change (CR11)
- [ ] Necessary feedback survives reduced motion
- [ ] Increased contrast honoured; subtle tones and borders strengthen
- [ ] Colour scheme respected; contrast verified in both themes
- [ ] Focus indicators verified per theme
- [ ] Text scaling honoured to the platform's maximum without loss
- [ ] Forced-colours / high-contrast mode not defeated by fixed colours
- [ ] Each preference is a distinct, recorded test case
- [ ] Preferences are orthogonal: they change presentation, not function
- [ ] Re-verified after any palette or theme change
