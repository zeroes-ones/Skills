## Decision Trees

<!-- QUICK: 30s — follow the ASCII tree to your scenario -->
<!-- STANDARD: 3min — each tree has concrete API names, budget numbers, and decision rationale -->

### Rendering Pipeline Selection — Forward vs Deferred vs Clustered Forward

```
                          ┌──────────────────────────────┐
                          │ START: Target hardware & scene │
                          │ GPU tier: ___                  │
                          │ Dynamic lights: ___ expected   │
                          │ Transparency layers: ___       │
                          │ Resolution: ___ x ___          │
                          └────────────┬─────────────────┘
                                       │
                         ┌─────────────▼─────────────────┐
                         │ Mobile / integrated GPU OR     │
                         │ <10 dynamic lights OR          │
                         │ extensive transparency?        │
                         └────┬────────────────────┬─────┘
                              │ YES                │ NO
                    ┌─────────▼──────┐    ┌────────▼────────────┐
                    │ Forward render   │    │ >100 dynamic lights  │
                    │ (mobile, Switch, │    │ OR deferred-capable  │
                    │  Quest, low-end  │    │ GPU (discrete)?      │
                    │  PC)             │    └────┬──────────┬──────┘
                    │ • Single-pass    │         │ YES      │ NO
                    │ • MSAA cheap     │  ┌──────▼──────┐ ┌─▼────────────┐
                    │ • Transparent    │  │ Deferred     │ │ Clustered     │
                    │   sorting free   │  │ (PC/Console) │ │ Forward       │
                    │ • Bandwidth: low │  │ • G-Buffer   │ │ (mid-range    │
                    └──────────────────┘  │   MRT        │ │  GPU, 50-100  │
                                          │ • Lighting   │ │  lights)      │
                                          │   compute    │ │ • Light grid  │
                                          │ • No MSAA    │ │   in compute  │
                                          │   (use TAA)  │ │ • MSAA + many │
                                          │ • Bandwidth: │ │   lights      │
                                          │   HIGH       │ │ • Forward+    │
                                          └──────────────┘ └───────────────┘
```
<!-- DEEP: 10+min — war story -->
*Studio shipped a deferred renderer for a game with heavy transparency (glass buildings, particle effects). Deferred can't blend transparent objects from the G-Buffer — they needed a separate forward pass for all transparent geometry. Result: two full scene traversals, 2x draw calls, 33ms frame time on target hardware. Fix: switched to clustered forward (Unity URP Forward+), single pass handles opaque + transparent + up to 256 lights via tile-based light culling. 16ms frame time restored. Cost: 6-week renderer rewrite, $180K engineering + delayed certification.*

### ECS Architecture Decision — Archetype-based vs Sparse-set vs Table-based

```
                          ┌──────────────────────────────┐
                          │ START: Entity count & access   │
                          │ Total entities: ___            │
                          │ Unique archetypes: ___         │
                          │ Queries/sec: ___               │
                          │ Add/remove components: ___/s   │
                          └────────────┬─────────────────┘
                                       │
                         ┌─────────────▼─────────────────┐
                         │ >10K entities of same type     │
                         │ (bullets, particles, AI units) │
                         │ AND structural changes rare?   │
                         └────┬────────────────────┬─────┘
                              │ YES                │ NO
                    ┌─────────▼──────┐    ┌────────▼────────────┐
                    │ Archetype ECS   │    │ Frequent add/remove  │
                    │ (Unity DOTS)    │    │ of components AND    │
                    │ • Chunk-based   │    │ <50K entities?       │
                    │   memory, SoA   │    └────┬──────────┬──────┘
                    │ • Ideal cache   │         │ YES      │ NO
                    │   locality      │  ┌──────▼──────┐ ┌─▼────────────┐
                    │ • Structural    │  │ Sparse-set   │ │ Table-based   │
                    │   changes slow  │  │ (EnTT)       │ │ (Flecs)       │
                    │   (move chunks) │  │ • O(1) add/  │ │ • Archetype   │
                    │ • Unity: DOTS   │  │   remove     │ │   graph       │
                    │   1.2+          │  │ • Stable ptrs │ │ • Add/remove  │
                    └─────────────────┘  │ • Good for   │ │   fast via    │
                                         │   UI/editor  │ │   table edges │
                                         │ • EnTT 3.12+ │ │ • Flecs 4.0+  │
                                         └──────────────┘ └───────────────┘
```
**Archetype (Unity DOTS):** Homogeneous entities, bulk processing, SoA layout, 16KB chunks. Best for: 10K+ identical entities, Burst-compiled jobs.
**Sparse-set (EnTT):** Heterogeneous entities, frequent add/remove, stable pointers. Best for: editor tools, UI, dynamic composition.
**Table-based (Flecs):** Middle ground, fast add/remove via table edges, good for mixed workloads, C99 compatible.

### Game Loop Type Selection — Fixed Timestep + Variable Rendering + Interpolation

```
                          ┌──────────────────────────────┐
                          │ START: Game type & requirements│
                          │ Deterministic replay? ___      │
                          │ Multiplayer? ___               │
                          │ Display: ___ Hz target         │
                          │ Physics: ___ Hz target         │
                          └────────────┬─────────────────┘
                                       │
                         ┌─────────────▼─────────────────┐
                         │ Deterministic replay OR        │
                         │ multiplayer OR physics-driven? │
                         └────┬────────────────────┬─────┘
                              │ YES                │ NO
                    ┌─────────▼──────┐    ┌────────▼────────────┐
                    │ Fixed timestep  │    │ Variable timestep    │
                    │ (Robert Nystrom │    │ (simple, non-physics)│
                    │  GameLoop pat.) │    │ • dt = frame time    │
                    │ • Physics:      │    │ • OK for: UI, menu,  │
                    │   dt = 1/60     │    │   turn-based, puzzle │
                    │ • Render:       │    │ • NOT for: physics,  │
                    │   interpolated  │    │   multiplayer,       │
                    │   state         │    │   deterministic      │
                    │ • Accumulator:  │    │   replay             │
                    │   Σ frame time  │    └──────────────────────┘
                    │ • α = accum/dt  │
                    │ • "Catch-up"    │
                    │   if accum>dt   │
                    │   run N physics │
                    │   steps with    │
                    │   spiral-of-    │
                    │   death guard   │
                    └─────────────────┘
```
<!-- DEEP: 10+min — war story -->
*Fighting game shipped with variable timestep. Frame rate: 58-62 FPS on PC. At 62 FPS, a forward dash traveled 6.2m in 10 frames. At 58 FPS, same dash traveled 5.8m. Competitive players discovered that capping at 58 FPS let them micro-step into throw range without triggering the opponent's throw-tech window. Tournament organizers banned the game. Fix: fixed timestep at 60Hz with interpolation. Cost: $100K+ in tournament credibility damage and 4-month engine refactor.*

### GPU API Selection — wgpu vs Vulkan vs DirectX 12 vs Metal

```
                          ┌──────────────────────────────┐
                          │ START: Platform targets        │
                          │ Windows: ___ %                 │
                          │ macOS/iOS: ___ %               │
                          │ Linux/SteamDeck: ___ %         │
                          │ Xbox: ___ %                    │
                          │ PlayStation: ___ %             │
                          │ Web (WebGPU): ___ %            │
                          └────────────┬─────────────────┘
                                       │
                         ┌─────────────▼─────────────────┐
                         │ Need browser/WebGPU OR        │
                         │ small team (<5 engine devs)    │
                         │ OR Rust codebase?             │
                         └────┬────────────────────┬─────┘
                              │ YES                │ NO
                    ┌─────────▼──────┐    ┌────────▼────────────┐
                    │ wgpu (WebGPU    │    │ Console target?      │
                    │ native)         │    └────┬──────────┬──────┘
                    │ • Cross-platform│         │ YES      │ NO
                    │   (D3D12, Vk,   │  ┌──────▼──────┐ ┌─▼────────────┐
                    │   Metal, GL)    │  │ Per-platform │ │ Vulkan        │
                    │ • Safe by       │  │ native:      │ │ (Steam Deck,  │
                    │   default       │  │ • D3D12 for  │ │  Linux, Win)  │
                    │ • SPIR-V input  │  │   Xbox/Win   │ │ OR D3D12      │
                    │ • wgpu 0.19+    │  │ • Metal 3    │ │ (Windows-only)│
                    │ • Not for: AAA  │  │   for Apple  │ │ • Explicit    │
                    │   console perf  │  │ • GNM/GNMX   │ │   control     │
                    └─────────────────┘  │   for PS5    │ │ • Ray tracing │
                                         │ • Max perf   │ │ • Mesh shaders│
                                         │ • Max effort │ │ • D3D12:      │
                                         │ • 4x impl    │ │   Agility SDK │
                                         └──────────────┘ └───────────────┘
```
**wgpu:** Best for indie/small-team, Rust, browser deployment, 1 codebase → 4 platforms. Not for AAA perf requirements.
**Vulkan:** Best for Steam Deck + Linux + Windows, explicit control, ray tracing via VK_KHR_ray_tracing_pipeline.
**D3D12:** Best for Xbox + Windows exclusive, Agility SDK for latest features, PIX for profiling.
**Metal 3:** Apple platforms only. Mesh shaders, ray tracing (M3+), MetalFX upscaling.

### Netcode Architecture — Client-Server Authoritative vs P2P Lockstep vs Rollback

```
                          ┌──────────────────────────────┐
                          │ START: Game genre & scale      │
                          │ Players per match: ___         │
                          │ Tickrate target: ___ Hz        │
                          │ Input latency tolerance: ___ms │
                          │ Spectator mode needed? ___     │
                          └────────────┬─────────────────┘
                                       │
                         ┌─────────────▼─────────────────┐
                         │ Fighting game OR <4 players    │
                         │ OR sub-30ms latency tolerance? │
                         └────┬────────────────────┬─────┘
                              │ YES                │ NO
                    ┌─────────▼──────┐    ┌────────▼────────────┐
                    │ Rollback netcode│    │ >32 players (MMO,    │
                    │ (GGPO-style)    │    │ FPS, BR) OR          │
                    │ • Input delay + │    │ spectator mode?      │
                    │   prediction    │    └────┬──────────┬──────┘
                    │ • Rollback on   │         │ YES      │ NO
                    │   mismatch      │  ┌──────▼──────┐ ┌─▼────────────┐
                    │ • Save states   │  │ Client-      │ │ P2P lockstep  │
                    │   every frame   │  │ Server       │ │ (RTS, 4X)     │
                    │ • For: fighting │  │ Authoritative│ │ • All clients │
                    │   games,        │  │ • Server     │ │   wait for    │
                    │   brawlers      │  │   simulates  │ │   all inputs  │
                    │ • Adds 1-3      │  │ • Client     │ │ • Deterministic│
                    │   frames delay  │  │   predicts   │ │   simulation  │
                    └─────────────────┘  │ • Reconcil.  │ │ • No server   │
                                         │   on mismatch│ │   needed      │
                                         │ • Snapshot   │ │ • Slowest     │
                                         │   interp.    │ │   player      │
                                         │ • For: FPS,  │ │   dictates    │
                                         │   BR, MMO    │ │   pace        │
                                         └──────────────┘ └───────────────┘
```
<!-- DEEP: 10+min — war story -->
*Battle royale shipped with client-authoritative movement. Within 72 hours of launch, cheat developers reverse-engineered the client and released a teleport hack — instant 500m movement, no server validation. 30% of the player base reported encountering cheaters in their first week. Player count dropped 60% month-over-month. The studio spent $500K+ on Easy Anti-Cheat integration + 6-month server-authoritative refactor. Lesson: never trust the client. Ever. Server-authoritative from day one, even for prototypes.*

### Memory Strategy — Object Pool → Arena Allocator → Subsystem Budget

```
                          ┌──────────────────────────────┐
                          │ START: Platform memory budget  │
                          │ Total RAM: ___ MB              │
                          │ Engine overhead: ___ MB        │
                          │ Game data: ___ MB target       │
                          │ Object count: ___ peak         │
                          └────────────┬─────────────────┘
                                       │
                         ┌─────────────▼─────────────────┐
                         │ Frequent alloc/free of same-   │
                         │ sized objects per frame?       │
                         │ (particles, bullets, sounds)   │
                         └────┬────────────────────┬─────┘
                              │ YES                │ NO
                    ┌─────────▼──────┐    ┌────────▼────────────┐
                    │ Object pool     │    │ >100MB total, many   │
                    │ • Pre-alloc N   │    │ subsystems competing?│
                    │ • Acquire/      │    └────┬──────────┬──────┘
                    │   Release API   │         │ YES      │ NO
                    │ • Pool size:    │  ┌──────▼──────┐ ┌─▼────────────┐
                    │   peak * 1.5   │  │ Subsystem    │ │ Simple malloc │
                    │   headroom      │  │ memory       │ │ (small <100MB│
                    │ • Template:     │  │ budgets      │ │  prototype)  │
                    │   T* Pool::     │  │ • Audio:     │ │ • Use        │
                    │   Acquire()     │  │   32MB cap   │ │   tcmalloc/  │
                    │ • Per-type pool │  │ • Render:    │ │   jemalloc   │
                    │   not generic   │  │   128MB cap  │ │ • STL with   │
                    └─────────────────┘  │ • Physics:   │ │   custom     │
                                         │   64MB cap   │ │   allocator  │
                                         │ • Each uses  │ │ • Not for    │
                                         │   arena      │ │   consoles   │
                                         │   allocator  │ └──────────────┘
                                         │ • Console:   │
                                         │   PS5/XSX    │
                                         │   hard caps  │
                                         └──────────────┘
```
