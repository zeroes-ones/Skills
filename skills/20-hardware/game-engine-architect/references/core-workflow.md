## Core Workflow

<!-- QUICK: 30s — scan phase titles to understand the process -->
<!-- STANDARD: 3min — each phase has explicit Do/Verify/Recover steps -->
<!-- DEEP: 10+min -->

### Phase 1 (~8 hours): Rendering Pipeline Architecture & PBR Setup
1. **Do:** Select pipeline per the Rendering Pipeline decision tree. Configure G-Buffer layout for deferred (Albedo RGB + Normal RG + Roughness/Metalness B + Depth 24) or forward pass with depth prepass for clustered.
2. **Do:** Implement PBR shading with Cook-Torrance BRDF: `F = F0 + (1-F0) * pow(1-NdotH, 5)`, `D = α² / (π * (NdotH² * (α²-1) + 1)²)`, `G = G_SchlickGGX(NdotV) * G_SchlickGGX(NdotL)`. Use roughness-metalness workflow with IBL from pre-filtered environment map.
3. **Do:** Set up shader compilation pipeline: Vulkan pipeline cache serialized to disk, Unity ShaderVariantCollection with warm-up scene, Unreal PSO cache with `r.ShaderPipelineCache.Enabled=1`.
4. **Verify:** Profile with RenderDoc: G-Buffer bandwidth < 64 bytes/pixel for deferred. Shader compile hitches < 1ms after warm-up. PBR validation: compare against Disney BRDF Explorer reference images.
5. **Recover:** G-Buffer too wide → drop specular color, reconstruct from roughness/metallic. Shader compile hitches persist → ship pre-compiled pipeline cache file with game build.

### Phase 2 (~6 hours): C++ Game Loop Implementation with Fixed Timestep
1. **Do:** Implement the canonical fixed timestep loop (Robert Nystrom pattern):
```cpp
double previous = getCurrentTime();
double lag = 0.0;
const double MS_PER_UPDATE = 16.6667; // 60Hz physics

while (running) {
    double current = getCurrentTime();
    double elapsed = current - previous;
    previous = current;
    lag += elapsed;

    // Fixed timestep physics: catch up if lagged
    while (lag >= MS_PER_UPDATE) {
        processInput();        // Sample inputs at step start
        fixedUpdate(MS_PER_UPDATE / 1000.0);
        lag -= MS_PER_UPDATE;
    }

    // Render with interpolation: α = lag / MS_PER_UPDATE
    double alpha = lag / MS_PER_UPDATE;
    render(alpha);
}
```
2. **Do:** Implement spiral-of-death guard: `const int MAX_FRAMES_TO_CATCHUP = 5;` in the while loop. On Xbox Series X at 120Hz, you have 8.33ms per frame — if physics takes >8.33ms, clamp catch-up to prevent snowball.
3. **Do:** Input sampling: snapshot at beginning of each fixed update step, not per-render frame. Use double-buffered input state read atomically.
4. **Verify:** Render at 30Hz, physics at 60Hz → visual smoothness via interpolation. Render at 144Hz, physics at 60Hz → no duplicated physics frames visible.
5. **Recover:** Spiral of death → increase physics tick rate (120Hz) or decrease physics cost. Drop physics fidelity before dropping frames.

### Phase 3 (~10 hours): Unreal Engine 5 Architecture Configuration
1. **Do:** Nanite configuration: set `r.Nanite 1`, `r.Nanite.MaxPixelsPerEdge 1` (quality), `r.Nanite.ViewMeshLODBias.Enable 0`. Fallback mesh target: <1% of triangles for masked/translucent materials. Virtual shadow maps: `r.Shadow.Virtual.Enable 1`.
2. **Do:** Lumen global illumination: `r.Lumen.DiffuseIndirect.Allow 1`, `r.Lumen.Reflections.Allow 1`. Surface cache: `r.Lumen.ScreenProbeGather.SpatialFilter 1`. For 60 FPS console: `r.Lumen.ScreenProbeGather.TracingOctahedronResolution 8` (half-res).
3. **Do:** Gameplay Ability System: `UGameplayAbility` subclass per ability, `FGameplayAttribute` for stats (Health, Mana, Stamina), `FGameplayTag` for state (Stunned, Invulnerable, Rooted). Use `UGameplayEffect` with `FGameplayModifierInfo` for buffs/debuffs. Attribute replication via `FGameplayAttributeData` with `OnRep`.
4. **Verify:** Nanite: `r.Nanite.Visualize.Overdraw 1` — overdraw < 8x on target GPU. Lumen: `r.Lumen.Visualize.Traces 1`. GAS: ability tag blocking verified (stun prevents cast).
5. **Recover:** Nanite overdraw > 8x → enable fallback mesh for high-density foliage. Lumen ghosting → enable `r.Lumen.Reflections.HistoryWeight 0.9`. GAS attribute desync → check `AActor::GetReplicatedServerLastTransformUpdateTimeStamp`.

### Phase 4 (~5 hours): Unity DOTS/ECS Optimization
1. **Do:** Entity archetype design: group by shared write access pattern — entities that all need `Translation` + `Rotation` updated together belong in same archetype. Use `IJobEntity` for simple iteration, `IJobChunk` for manual chunk iteration with `ArchetypeChunkComponentType`.
2. **Do:** Burst compilation: `[BurstCompile(FloatPrecision.Low, FloatMode.Fast)]` for physics, `OptimizeFor = OptimizeFor.Performance`. Avoid managed objects in Burst — use `FixedString64Bytes`, `BlobAssetReference<T>`, `NativeHashMap`.
3. **Do:** Memory layout: `ComponentType.ChunkComponent` for shared read-only data. `EntityCommandBuffer` for structural changes (create/destroy entities, add/remove components) — never inside `IJobEntity`/`IJobChunk`.
4. **Verify:** Unity Profiler: Burst jobs show as "Burst" in timeline. `SystemAPI.Query<T>()` zero managed allocations. Job `Schedule()` latency < 0.1ms. Chunk utilization > 80% (no sparse chunks).
5. **Recover:** Structural change in job → `EntityCommandBuffer` pattern. Managed leak → `NativeArray.Dispose()` audit with `LeakDetectionMode = NativeLeakDetectionMode.Enabled`.

### Phase 5 (~4 hours): Multiplayer Netcode Implementation
1. **Do:** Client-side prediction: client runs same simulation code as server, predicts local player `+N` ticks ahead. Input buffer: `InputCommand inputs[MAX_INPUT_HISTORY]` indexed by tick number. Send input with tick number, not frame number.
2. **Do:** Server reconciliation: server processes input for tick T, broadcasts authoritative state for tick T. Client receives state for tick T, compares with predicted state at same tick. If `|predicted_position - server_position| > threshold`, rewind state to tick T, replay all inputs from T to current, re-predict.
3. **Do:** Snapshot interpolation: server sends state snapshots at tickrate (e.g., 64Hz). Client buffers 2-3 snapshots, renders interpolated state between tick `N` and `N+1` at `N + interp_delay` ticks. Jitter buffer: adaptive size based on network jitter measurement.
4. **Verify:** Client prediction: 0ms input latency visually, no "swimming" feel. Reconciliation: teleport correction < 1cm for <100ms ping. Interpolation: no stutter with ±30ms jitter.
5. **Recover:** Prediction overshoot (>10cm at 50ms ping) → reduce prediction time window or add velocity damping. Interpolation starvation → increase `interp_delay` by one tick.

