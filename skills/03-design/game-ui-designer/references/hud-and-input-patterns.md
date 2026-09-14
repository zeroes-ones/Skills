# HUD and Input Patterns

A game HUD is read at speed, under load, often at distance. Legibility beats beauty.

## Readability rules

| Concern | Requirement |
|---|---|
| Contrast | Survives the busiest scene, not just a menu mock |
| Safe area | Nothing critical inside the title-safe margin of any target aspect |
| Scale | Legible at the smallest supported resolution and the largest display distance |
| Redundancy | Never encode critical state in one channel — pair colour with shape, icon, or position |
| Motion | Animate state change, not decoration; motion draws the eye away from the play area |

## Input

- Map to the physical layout of the controller, not an abstract list.
- Support remapping; never hard-code one scheme.
- Show the prompt for the input device actually in use, and switch when it changes.

## Failure modes

- **Contrast that fails mid-combat.** The HUD is legible on a static screenshot and invisible during play.
- **Colour-only state.** Team, threat, or rarity communicated by hue alone.
- **Critical UI outside safe area.** Clipped on a target aspect ratio.
- **Subtitle truncation.** Long lines cut off with no wrap or scroll.
- **No remap.** A player whose layout differs cannot play.
- **Prompt shows keyboard while a controller is connected.** The player is told the wrong button.
