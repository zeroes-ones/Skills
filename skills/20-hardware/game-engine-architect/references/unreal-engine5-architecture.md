# Unreal Engine 5 Architecture

## Nanite Virtualized Geometry
- **Console variables:** `r.Nanite 1`, `r.Nanite.MaxPixelsPerEdge 1`, `r.Nanite.ViewMeshLODBias.Enable 0`
- **Meshlet:** 128 triangles per meshlet, BVH over meshlets
- **Software rasterization:** 2x2 pixel quads. Falls back to hardware raster for small triangles
- **Overdraw profiling:** `r.Nanite.Visualize.Overdraw 1` — target <8x on mid-range GPU
- **Fallback:** `r.Nanite.FallbackPercentTriangle` for masked/translucent materials

## Lumen Global Illumination
- **Enable:** `r.Lumen.DiffuseIndirect.Allow 1`, `r.Lumen.Reflections.Allow 1`
- **Surface Cache:** Card-based scene representation, updated incrementally
- **Ray tracing:** `r.Lumen.HardwareRayTracing 1` for hardware RT override
- **60 FPS console:** Reduce `r.Lumen.ScreenProbeGather.TracingOctahedronResolution` to 8

## Gameplay Ability System (GAS)
- **Ability:** `UGameplayAbility` subclass. Override `ActivateAbility()`, `CanActivateAbility()`
- **Attribute:** `FGameplayAttributeData` with `ATTRIBUTE_ACCESSORS` macro, `ReplicatedUsing = OnRep`
- **Effect:** `UGameplayEffect` with `FGameplayModifierInfo` for buffs/debuffs
- **Tags:** `FGameplayTag` for state (Stunned, Invulnerable, Rooted), ability blocking via `ActivationBlockedTags`

## Mass Entity (Crowd Simulation)
- **Fragments:** Component data per entity (similar to Unity DOTS)
- **Processors:** `UMassProcessor` per system, scheduled via `UMassProcessingPhaseManager`
- **Configuration:** `FMassEntityConfig` with trait-based composition
