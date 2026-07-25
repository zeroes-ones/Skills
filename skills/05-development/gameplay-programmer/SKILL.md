---
name: gameplay-programmer
description: Gameplay systems programming with C++, C#, Unity, Unreal Engine, and custom engines. Use when designing gameplay mechanics, implementing combat systems, building AI behaviors, creating animation state machines, integrating physics for gameplay, designing player controllers, or prototyping game features. Handles gameplay architecture patterns (ECS, component-based, data-driven design), game loop integration, input handling, camera systems, and gameplay performance optimization. Do NOT use for rendering pipeline engineering, engine architecture, networking infrastructure, or art/asset pipeline.
author: Sandeep Kumar Penchala
license: MIT
version: 1.0.0
updated: 2026-07-24
tags: [gameplay, game-development, unity, unreal, cpp, csharp, game-design]
token_budget: 4500
chain:
  consumes_from:
    - game-developer
    - game-engine-architect
    - backend-developer
    - performance-engineer
  feeds_into:
    - game-developer
    - game-networking-developer
    - qa-engineer
---

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

# Gameplay Programmer — Real-Time Interactive Game Logic

Build production gameplay systems — spanning Unity (C#), Unreal Engine (C++/Blueprints), and custom engines — with deep expertise across the full game development lifecycle. Covers game loop architecture, entity-component-system (ECS) patterns, physics integration, input handling, camera systems, AI behavior trees, multiplayer state synchronization, animation state machines, procedural generation, and performance optimization to stable 60/120fps.

## Route the Request

### Auto-Route (No User Input Required)
| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("*.unity")` OR `file_exists("*.uproject")` OR `file_contains("*.cs", "MonoBehaviour|GameObject|Transform")` OR `file_contains("*.cpp", "AActor|UObject|FString")` | This is your skill. Jump to **Core Workflow — Phase 1**. |
| A2 | `file_contains("*.cs", "FixedUpdate|Time.deltaTime|Physics.Raycast")` OR `file_contains("*.cpp", "TickComponent|DeltaTime|LineTrace")` | Jump to **Decision Trees — Physics & Frame Rate Strategy**. |
| A3 | `file_contains("*.cs", "NetworkBehaviour|Command|ClientRpc")` OR `file_contains("*.cpp", "Replicated|RPC|NetMulticast")` | Jump to **Decision Trees — Multiplayer Sync Model**. |
| A4 | `file_contains("*.cs", "NavMeshAgent|BehaviorTree|StateMachine")` OR `file_contains("*.cpp", "AIController|Blackboard|BTService")` | Jump to **references/ai-behavior-systems.md**. |
| A5 | `file_contains("*.cs", "Animator|AnimationClip|BlendTree")` OR `file_contains("*.cpp", "AnimInstance|AnimBlueprint|Montage")` | Jump to **references/animation-state-machines.md**. |
| A6 | Frame drops or performance issues reported → Jump to **Decision Trees — Performance Budget**. |
| A7 | `file_contains("*.cs", "PerlinNoise|Procedural|Random.seed")` OR `file_contains("*.cpp", "FMath::Perlin|FProcMesh|Seed")` | Jump to **references/procedural-generation.md**. |
| A8 | Unknown — describe your gameplay mechanic → I'll route you. |

```
What are you trying to do?
├── Build a player controller (3rd person, FPS, top-down) → Core Workflow Phase 2
├── Implement combat/damage system → Core Workflow Phase 3
├── Set up multiplayer networking (authoritative server) → Decision Trees — Multiplayer Sync Model
├── Create AI behaviors (patrol, chase, attack, flee) → references/ai-behavior-systems.md
├── Optimize frame rate (target 60/120fps stable) → Decision Trees — Performance Budget
├── Design ECS architecture for 10K+ entities → Decision Trees — ECS vs GameObject
├── Implement save/load system → Core Workflow Phase 6
├── Need input system for cross-platform → references/input-handling-systems.md
├── Need game design guidance → Invoke game-developer skill instead
├── Need engine architecture → Invoke game-engine-architect skill instead
├── Need networking infrastructure → Invoke game-networking-developer skill instead
└── Don't know where to start? → Describe your game genre and target platform and I'll route you
```

Do not read the entire skill. Follow the route above.

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| **R1** | **NEVER run game logic in `Update()` that belongs in `FixedUpdate()`.** Physics calculations, Rigidbody manipulation, and collision-dependent logic in `Update()` cause framerate-dependent behavior — a jump that works at 60fps sends the player flying at 144fps. | Trigger: generated code uses `Rigidbody.AddForce()` or `Physics.Raycast()` inside `Update()` instead of `FixedUpdate()` | STOP. Move all physics code to `FixedUpdate()`. Cache non-physics state (input, animations) read from `Update()` in member variables, consumed by `FixedUpdate()`. Rule: `Update()` for input/graphics, `FixedUpdate()` for physics. |
| **R2** | **REFUSE to allocate memory in the game loop (Update/FixedUpdate/Tick).** Every `new`, `Instantiate()`, `GetComponent<>()`, LINQ expression, or `std::vector` resize inside the game loop allocates heap memory. GC spikes on Mono/IL2CPP cause 50-200ms frame hitches — players feel it as "stutter." | Trigger: generated code contains `new`, `Instantiate()`, `GetComponent<T>()`, `Find()`, `.ToArray()`, `.Where()` inside `Update()`/`FixedUpdate()`/`Tick()` | STOP. Pre-allocate in `Awake()`/`Start()`/`BeginPlay()`. Use object pools for bullets, particles, enemies. Cache component references in `Awake()`. Replace LINQ with for-loops. Rule: zero allocations after scene load. |
| **R3** | **REFUSE to use `GameObject.Find()` or `FindObjectOfType<T>()` in production code.** These scan the entire hierarchy — O(n) per call, 5-50ms on a scene with 10K objects. Calling them every frame crashes frame budget. | Trigger: generated code contains `GameObject.Find(` or `FindObjectOfType<` anywhere outside `Awake()` | STOP. Wire references via Inspector (`[SerializeField] private`), dependency injection, or service locator initialized once. `FindObjectOfType` allowed ONLY in `Awake()` for singleton initialization (once). |
| **R4** | **DETECT and WARN when multiplayer code uses client-authoritative state for gameplay decisions.** Movement speed, health, score, inventory — if the client can set these, hackers will. Every multiplayer game shipped with client-authoritative state has been ruined by cheaters within 48 hours of launch. | Trigger: generated code has `[Command]` without server validation OR `[SyncVar]` writable by client OR `Replicated` property with client setter | WARN: "This is client-authoritative. Every competitive multiplayer game that shipped client-authoritative state was destroyed by cheaters within 2 days. Server must validate ALL gameplay state changes. Client is a dumb terminal that sends inputs — server runs the simulation." |
| **R5** | **NEVER assume a consistent frame rate.** Frame rate varies by hardware, thermal throttling, background processes, and platform (Quest 2 at 72fps vs PC at 144fps). Code that assumes 60fps breaks at 30fps (slow-mo) and 144fps (hyperspeed). | Trigger: generated code multiplies by constant (e.g., `speed * 0.016f`) instead of `Time.deltaTime` (Unity) or `DeltaTimeSeconds` (Unreal) | STOP. Every movement, rotation, timer, and lerp must multiply by delta time. Use `Time.deltaTime` (Unity) or `GetWorld()->GetDeltaSeconds()` (Unreal). FixedUpdate uses `Time.fixedDeltaTime`. |
| **R6** | **REFUSE to leave debug code in production builds.** `Debug.Log()`, `GEngine->AddOnScreenDebugMessage()`, `print()`, and `DrawDebugLine()` in production cost 0.5-2ms per call — 10 calls per frame = 20ms at 60fps = frame drop. | Trigger: generated code contains `Debug.Log(` or `print(` or `DrawDebug` without `#if UNITY_EDITOR` / `#if WITH_EDITOR` guard | STOP. Wrap in `#if UNITY_EDITOR` (Unity) or `#if WITH_EDITOR` (Unreal). Use conditional compilation so debug code is stripped from builds. For runtime debugging, use a debug manager with runtime toggle. |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

Competent gameplay programmers make features that work on their dev machine. Masters make features that hold 60fps on a 5-year-old console, never desync in multiplayer, and survive 100K entities without frame drops. The shift: stop coding for the demo video and start coding for the player who paid $70 and expects zero bugs.

**Cognitive biases that kill games:**
| Bias | How It Manifests | Antidote |
|------|-----------------|----------|
| **Dev-machine myopia** | Testing on an RTX 4090 + i9-14900K with 64GB RAM, then shipping to players on GTX 1060. "It runs fine for me" = 1-star Steam reviews. | Profile on minimum-spec hardware weekly. Set a performance budget: 16.6ms at 60fps (or 8.3ms at 120fps). Profile daily, not monthly. |
| **Network-neglect syndrome** | Building all gameplay as single-player, planning to "add multiplayer later." Retrofitting multiplayer doubles development time and introduces 200+ edge cases (latency compensation, state reconciliation, authoritative server migration). | If the game is multiplayer, build multiplayer from day 1. Run client-server with simulated latency (100ms) during development. |
| **Object-pool denial** | Using `Instantiate()`/`Destroy()` for bullets, particles, and enemies because "the profiler shows it's fine now." 100 simultaneous explosions = 100 GC allocations = 200ms frame hitch when the GC runs. | Object-pool every frequently-spawned GameObject. Bullets, particles, audio sources, UI elements. One pool per prefab, pre-warm to peak capacity. |

## Operating at Different Levels

| Level | Gameplay Programmer Output |
|-------|--------------------------|
| **L1 — Junior** | Implements features following existing patterns. Player controller from template, basic AI patrol. Works in single-player context. |
| **L2 — Mid** | Implements complex gameplay systems independently. Combat with damage types, status effects, hit reactions. Performance-conscious (object pooling, no per-frame allocations). Handles basic multiplayer (NetworkBehaviour, RPCs). |
| **L3 — Senior** | Architects gameplay systems for entire game. ECS vs GameObject tradeoffs. Authoritative server with prediction + reconciliation. Behavior tree architecture for 50+ AI types. Performance budgets enforced in CI. |
| **L4 — Lead** | Defines gameplay architecture across multiple titles. Custom netcode decisions. Engine-level optimizations (Jobs/Burst, compute shaders). Mentors team on performance patterns. Cross-discipline with design, art, audio. |
| **L5 — Principal** | Industry-defining gameplay systems. Ships technology used by dozens of studios. Invents new gameplay paradigms. "This netcode architecture became the studio standard for the next 5 years." |

## When to Use

- Building player controllers: first-person, third-person, top-down, vehicle, flight
- Implementing combat systems: hit detection, damage calculation, status effects, buffs/debuffs, elemental systems
- Designing AI behavior: finite state machines, behavior trees, utility AI, GOAP, navmesh navigation
- Setting up multiplayer: authoritative server, client-side prediction, state reconciliation, lag compensation
- Optimizing performance: object pooling, LOD systems, occlusion culling, Jobs/Burst, ECS
- Creating animation systems: state machines, blend trees, IK, procedural animation, root motion
- Building save/load: serialization, checkpoint systems, persistent world state
- Implementing procedural generation: level generation, loot tables, enemy placement, terrain

## Decision Trees

### ECS vs GameObject Architecture
```
START: Entity count in your scene?
|
├── Under 500 active entities?
│   └── GameObject/MonoBehaviour. ECS overhead not justified.
│       Standard Unity workflow. Pool frequently spawned objects.
│
├── 500-5,000 active entities?
│   ├── Most entities unique behavior? → GameObject + Jobs for parallel work
│   └── Many entities share behavior (bullets, particles, units)? → Hybrid: GameObject rendering, Jobs for logic
│
├── 5,000-50,000 active entities?
│   └── ECS (Unity DOTS or custom). GameObject overhead (Transform, 5+ components each) kills frame budget.
│       Entities.ForEach with Burst compilation. IComponentData only — no managed types.
│
└── 50,000+ active entities?
    └── Pure ECS mandatory. Jobs + Burst. No GameObject bridge. Custom rendering via DrawMeshInstancedIndirect.
```

### Multiplayer Sync Model
```
START: Competitive or cooperative?
|
├── Competitive (PvP)?
│   ├── Fast-paced FPS? → Authoritative server + client prediction + reconciliation. Server rewinds time for hit validation.
│   ├── MOBA/RTS? → Lockstep deterministic simulation. Send inputs, not state. Must be fully deterministic.
│   └── Turn-based? → Server authoritative. Client sends action, server validates, broadcasts result. Simplest to secure.
│
├── Cooperative (PvE)?
│   ├── Host listenserver? → Host authoritative. Low latency for host, normal for clients. Host migration for host disconnect.
│   ├── Dedicated server? → Server authoritative. Highest security, consistent latency. Required for cross-play.
│   └── Peer-to-peer? → Only for 2-4 player casual co-op. No competitive integrity. Easy to cheat.
│
└── Single-player with optional co-op?
    └── Client authoritative with server backup. Player hosts their own game. Friend joins as client. Trust the host.
```

### Physics & Frame Rate Strategy
```
START: What needs physics?
|
├── Character movement + jumping?
│   └── CharacterController (Unity) or CharacterMovementComponent (Unreal). NOT Rigidbody for player movement.
│       Rigidbody-based player controllers feel floaty and framerate-dependent. Use kinematic controller + custom gravity.
│
├── Ragdolls, explosions, debris, vehicles?
│   └── Rigidbody (Unity) or PhysicsBody (Unreal). Use FixedUpdate for forces. Interpolate for smooth rendering.
│
├── 100+ physics objects interacting?
│   └── Unity DOTS Physics or Unreal Chaos Physics. Standard PhysX/Nvidia Physics bottlenecked by single-threaded solver.
│
└── No physics needed (puzzle, card game, visual novel)?
    └── Skip physics entirely. Use custom lightweight collision (AABB, sphere checks). Physics engine is 2-5ms overhead you don't need.
```

### AI Architecture
```
START: AI complexity level?
|
├── Simple (guard patrols, enemy chases player)?
│   └── Finite State Machine (FSM). 3-8 states. Easy to debug, predictable. Enum-based states with switch/case transitions.
│
├── Medium (enemy takes cover, flanks, retreats when wounded)?
│   └── Behavior Tree. Composable tasks. Designers can modify without code. Unreal Behavior Tree or Unity Behavior (package).
│       Parallel nodes for simultaneous behaviors (shoot + move). Decorators for conditions (has ammo? player visible?).
│
├── Complex (dynamic tactics, learns player patterns, coordinates squad)?
│   └── Utility AI + GOAP (Goal-Oriented Action Planning). AI scores possible actions, picks highest utility. Emergent behavior.
│       Alyssa (Halo Infinite), F.E.A.R. AI. Each action has weight curves based on world state. Very hard to debug — log everything.
│
└── Massive (100+ AI with crowd behavior, flocking, formations)?
    └── ECS-based AI. Avoid GameObject overhead per AI. Flocking = 3 simple rules per entity parallelized via Jobs. Formations = leader-follower with local avoidance.
```

### Performance Budget Allocation
```
60fps = 16.6ms total frame budget. Allocate:
├── Rendering (GPU): 8-10ms (60% of budget)
├── Gameplay logic (CPU): 3-5ms (25%)
├── Physics: 1-2ms (10%)
├── AI: 1-2ms (10%)
└── Audio, UI, other: 1ms (5%)

120fps = 8.3ms. Cut all budgets by half.
Rule: gameplay code must NEVER exceed 3ms at 60fps. If it does, profile and slice.
```

## Core Workflow

### Phase 1 (~20 min): Project Setup & Game Loop Architecture
1. **Engine selection**: Unity (C#, best for mobile/indie/2D/3D), Unreal (C++/Blueprints, best for AAA/3D/FPS/photoreal), Godot (GDScript/C#, best for 2D/small team/open source)
2. **Game loop**: `Update()` → input collection → gameplay logic → `FixedUpdate()` → physics step → LateUpdate → rendering. Never mix physics and rendering logic.
3. **Scene architecture**: Bootstrap scene (persistent) → managers (GameManager, AudioManager, PoolManager) → level scenes (additive loaded)
4. **Singleton pattern**: `MonoBehaviour` singletons ONLY for managers. All other objects injected or referenced via Inspector. Rule: max 5 singletons per project.

### Phase 2 (~25 min): Player Controller & Input
- **Input System**: Unity Input System Package (event-driven, rebindable, multi-device) or Unreal Enhanced Input. Never use legacy `Input.GetKey()`.
- **Controller architecture**: Input → Input Handler → Command → Controller → Movement/Abilities. Decouple input from action.
- **Camera**: Cinemachine (Unity) or SpringArmComponent (Unreal). Collision detection, camera shake, FOV changes. Never parent camera directly to player — use virtual camera with damping.

### Phase 3 (~30 min): Combat & Damage Systems
- **Hit detection**: Raycast (hitscan), sphere cast (melee AOE), projectile (physics-based). Pick based on weapon type.
- **Damage pipeline**: Attacker → DamageData (amount, type, source, penetration) → Receiver.Armor.Reduce() → Health.Apply(). Each step is testable independently.
- **Status effects**: Buff/Debuff as components with duration, tick rate, stack behavior. ScriptableObject for data, MonoBehaviour for runtime.

### Phase 4 (~30 min): Multiplayer Implementation
- **Client-Server model**: Server runs gameplay simulation. Client sends inputs, receives state. Client predicts locally for responsiveness.
- **State sync**: SyncVars (Unity NGO/Mirror) or Replicated properties (Unreal). Only sync what changed, only to relevant clients.
- **RPCs**: ServerRpc (client→server, validated), ClientRpc (server→clients, broadcast or targeted). Never trust ClientRpc parameters — validate on server.

### Phase 5 (~25 min): Animation Integration
- **State machine**: Idle → Walk → Run → Jump → Fall → Land. Blend trees for direction + speed. Animation events for footstep sounds, hit frames, weapon trails.
- **Procedural animation**: IK for foot placement on uneven terrain, look-at for head tracking, weapon sway. Reduces animation asset count by 60%.

### Phase 6 (~20 min): Save/Load & Persistence
- **Save architecture**: GameState → serialized to JSON/binary → compressed → written to disk. Always write to temp file, rename atomically — prevents corruption on crash mid-save.
- **What to save**: Player position (checkpoint), inventory, quest progress, world state (opened doors, killed enemies, collected items). NEVER save: visual effects, transient audio, temporary decals.

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `game-developer` | Game design document, mechanic specs, balance curves, progression systems | Before implementing any gameplay mechanic |
| `game-engine-architect` | Engine selection, rendering pipeline architecture, memory budget, threading model | Before choosing ECS vs GameObject, Jobs vs main thread |
| `game-networking-developer` | Netcode architecture, transport layer, matchmaking, relay servers | Before implementing multiplayer gameplay |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `qa-engineer` | Playable build, performance baseline (frame rate, memory), multiplayer test configuration | QA can't test without playable gameplay |
| `performance-engineer` | Profiler captures, CPU/GPU frame breakdowns, object allocation traces | Performance work is blind without gameplay profiling data |

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "I'll optimize after all gameplay features are done — premature optimization is evil." | Gameplay architecture determines performance ceiling. Object pools, ECS choice, and authoritative server model must be decided before 10K lines of MonoBehaviour code exist. Retrofitting pools into 200 files is a rewrite, not a refactor. Cost: 4-8 weeks. |
| "Multiplayer can wait until the single-player demo is approved." | Every gameplay system built single-player (player controller, combat, AI, inventory) must be rewritten for authoritative server. Input → Command pattern, state serialization, and prediction are incompatible with direct state mutation. Day-1 multiplayer costs 20% overhead; retroactive multiplayer costs 100%. |
| "The profiler shows 58fps — close enough to 60, we'll ship." | 58fps means 1 dropped frame every 0.5 seconds. Players perceive it as "jank." App Store and Google Play feature only 60fps-stable games. Console certification (Sony, Microsoft) REQUIRES stable frame rate — 0 dropped frames in certification test run. |
| "We don't need object pooling — modern GC is fast." | Unity Mono GC collects 1MB in ~2ms. A bullet hell game spawning 200 bullets/second with `Instantiate`/`Destroy` generates 40KB garbage per bullet = 8MB/second. GC runs every 2 seconds = 15ms hitches. Players call it "stutter," reviewers call it "poorly optimized." |
| "The AI behavior tree works in the test level — ship it." | Test levels have clean navmeshes, no dynamic obstacles, 3 enemies. Production levels have 20 enemies, destructible cover, dynamic navmesh obstacles, and 16ms frame budget. AI that takes 2ms in test takes 14ms in production — leaves 2ms for everything else. Profile on production levels, not test levels. |

## Gotchas

- **FixedUpdate at wrong timestep — game plays in slow-mo or hyperspeed on different hardware.** Unity's `Time.fixedDeltaTime` defaults to 0.02 (50Hz). If your `FixedUpdate()` relies on this without multiplying forces by `Time.fixedDeltaTime`, physics behaves differently at 50Hz vs 30Hz vs 100Hz. A character that jumps correctly at 50Hz may barely leave the ground at 30Hz (mobile thermal throttling). **$20K-$80K in post-launch patches, negative reviews citing "floaty controls," and lost featuring on app stores for inconsistent physics behavior.** Test physics at fixedDeltaTime = 0.033 (30Hz), 0.02 (50Hz), 0.013 (75Hz).

- **`GameObject.Find()` in `Update()` — frame drops from 60fps to 3fps on level restart.** A developer adds `GameObject.Find("Player")` to reconnect references after scene reload. In a scene with 15K objects, `Find()` scans the entire hierarchy taking 8-25ms. Called every frame = permanent 3fps. **$5K-$15K in wasted profiling and debugging, with developers searching for "memory leaks" that don't exist.** Solution: Cache all references in `Awake()`. If you must find dynamically, use `FindWithTag()` (indexed by engine) or maintain a manager with a registration dictionary.

- **IL2CPP stripping removes event functions used via reflection — game silently breaks on iOS.** Unity's IL2CPP strips unused code. If your `MonoBehaviour` uses `StartCoroutine()` with a method name string or `SendMessage()`, the target method is stripped from the build. The game works in Editor (Mono JIT) and silently fails on device. **$30K-$100K in App Store rejection, emergency patches with 48-hour review wait, and lost launch momentum.** Solution: Add `[Preserve]` attribute or a `link.xml` file to prevent stripping. Never use `SendMessage()` — use direct method calls or C# events.

- **Uncapped deltaTime in replays — game diverges after 20 seconds.** Deterministic replays require fixed timestep simulation. If your replay system captures inputs and replays them using `Update()` (variable deltaTime), floating point divergence causes the replay to drift within seconds. Characters walk through walls, bullets miss, the replay is garbage. **$50K-$200K for competitive games — esports replays are the primary anti-cheat evidence; broken replays mean unbannable cheaters.** Solution: Record at fixed timestep. All gameplay logic in `FixedUpdate()` with deterministic math (no `float` random without seeded RNG). Verify replay determinism via checksum comparison at key frames.

- **`[SerializeField]` references break silently when prefab is nested — null reference in production.** A nested prefab's serialized reference to a sibling component survives in the top-level prefab but becomes null when the nested prefab is instantiated in a different context (prefab variant, addressable asset). The game ships with `NullReferenceException` in production logs, which players don't see but causes invisible failures (AI doesn't patrol, doors don't open). **$10K-$40K in "can't reproduce" bug reports, negative reviews, and support tickets for broken quests.** Solution: Use `GetComponentInChildren<T>()` or `GetComponentInParent<T>()` for references within the same prefab hierarchy. Serialized references only for cross-prefab (scene-level) connections.

- **Animator.SetTrigger() called but animation doesn't play — state machine transition condition blocks it.** The Animator state machine only processes triggers when in a state that has a transition listening for that trigger. If the character is in the "Death" state and you call `SetTrigger("Jump")`, the trigger is consumed but no transition exists = the jump never plays and the trigger is permanently consumed. **$5K-$20K in animation bugs reported as "character frozen," "unresponsive controls."** Solution: Use `Animator.ResetTrigger()` before setting. Verify transition exists from current state. For critical animations (hit reaction, death), use `Animator.Play()` to force state change bypassing transitions.

- **Multiplayer: `NetworkTransform` smooths position with default interpolation — players visually overshoot corners.** Default network interpolation smooths from old state to new state over 100ms. When a player stops moving, the interpolation continues for 100ms — the character model slides past the stopping point and snaps back. Players perceive this as "lag" even at 20ms ping. **$15K-$50K in multiplayer beta feedback: 'netcode is broken,' 'rubber-banding,' 'unplayable.'** Solution: Use `NetworkTransform` with rigidbody-based interpolation mode. Tune `Interpolate` to 0.1-0.2 for snappy response. Implement client prediction for player-owned objects — the local player should never see interpolation lag.

## What Good Looks Like

> The game runs at a locked 60fps (16.6ms) on minimum-spec hardware with 500 active entities, zero per-frame allocations after scene load, and no GC spikes. Player input feels instantaneous (<100ms from button press to visual response). Multiplayer is authoritative — the server validates every gameplay action, clients predict locally with <50ms reconciliation error. AI enemies navigate dynamic environments without getting stuck, and their behavior scales from 3 to 100 entities without algorithmic complexity explosion. Save/load is atomic — corrupted saves don't exist because writes are never in-place. The profiler shows gameplay CPU at <3ms, leaving 13ms for rendering, physics, and future features.

## Deliberate Practice

1. **60fps from scratch**: Build a bullet hell with 1,000 bullets on screen at 60fps on a mid-range device. Must use object pooling, DOTS/ECS, and zero per-frame allocations. Profile and document every allocation found and removed.
2. **Authoritative server from day 1**: Implement a simple competitive game (Pong or a racing game) with authoritative server, client prediction, and reconciliation. Measure reconciliation error. Must feel responsive at 100ms simulated latency.
3. **AI crowd**: Implement 100 AI agents navigating a dynamic city with obstacles appearing mid-game. Must maintain 60fps. Use ECS, flow fields, or hierarchical pathfinding. Agents must never get stuck.


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

### How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "gameplay-programmer",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }
   ```
3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.

### State Log Schema

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |

### Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## Production Checklist

- [ ] **[S1]** Player controller: input decoupled from action; works at 30/60/120/144fps with consistent feel
- [ ] **[S2]** Zero per-frame allocations after scene load (confirmed with Unity Profiler Deep Profile)
- [ ] **[S3]** Object pools for: bullets, particles, enemies, UI elements. Pre-warmed to peak capacity.
- [ ] **[S4]** Multiplayer: server authoritative for all gameplay state. Client prediction + reconciliation for player movement.
- [ ] **[S5]** AI: behavior trees/FSM documented with state diagrams. All transitions tested. No AI stuck in geometry.
- [ ] **[S6]** Animation: state machine complete. All transitions have exit time or condition. Blend trees for direction + speed.
- [ ] **[S7]** Save system: atomic writes (temp file → rename). Save version number for backward compatibility. Corruption detection via checksum.
- [ ] **[S8]** Performance: 60fps stable on minimum-spec hardware. Profiler shows gameplay CPU <3ms, physics <2ms, AI <2ms.
- [ ] **[S9]** No `GameObject.Find()`, `SendMessage()`, or `FindObjectOfType<T>()` in production code outside `Awake()`.
- [ ] **[S10]** IL2CPP stripping: `link.xml` configured. All reflection-used types preserved. Tested on device build, not just Editor.

## Proactive Triggers

| Trigger | Action | Rationale |
|---|---|---|
| `GameObject.Find()` or `SendMessage()` found in PR | Block merge — flag as performance anti-pattern | These methods scan entire scene hierarchy; single call costs 0.5-10ms on production scenes |
| Frame rate drops below target in profiler capture | Investigate update loop, physics tick, GC allocation. Check `Time.deltaTime` variance >2ms | Players perceive inconsistency before they see low average FPS — spikes cause "micro-stutter" that drives negative reviews |
| Player reports "lag" or "rubber-banding" in multiplayer | Verify client prediction error threshold. Check if reconciliation snapshots exceed 3-frame window | Desync beyond 50ms is felt by players; beyond 100ms causes rage-quits. Prediction must converge within 3 physics ticks |
| New animation added without state machine diagram | Require state diagram showing all transitions, conditions, and exit times before review | Animation bugs (snapping, stuck states, wrong blends) are the #1 visual bug category — state diagrams prevent 80% of them |
| `Awake()` or `Start()` growing beyond 20 lines | Refactor into separate initialization phases with explicit ordering | Unity's script execution order is non-deterministic by default; bloated Awake/Start creates Heisenbugs that only reproduce on certain machines |
| Save file version mismatch after update | Run migration path; never silently fail. Alert player if save cannot be migrated | Corrupted saves cause players to abandon games — a single corrupted 60-hour save file generates more negative reviews than any other bug |

## References

- [references/ai-behavior-systems.md](references/ai-behavior-systems.md) — Behavior trees, utility AI, GOAP, navmesh, crowd simulation
- [references/animation-state-machines.md](references/animation-state-machines.md) — Blend trees, IK, root motion, animation events, procedural animation
- [references/input-handling-systems.md](references/input-handling-systems.md) — Unity Input System, Unreal Enhanced Input, rebinding, multi-device, input buffering
- [references/multiplayer-sync-patterns.md](references/multiplayer-sync-patterns.md) — Client prediction, state reconciliation, lag compensation, interest management
- [references/object-pooling-patterns.md](references/object-pooling-patterns.md) — Generic pool, pre-warming, addressable-based pooling, pool debugging
- [references/physics-best-practices.md](references/physics-best-practices.md) — FixedUpdate timing, interpolation, collision matrix, physics material tuning
- [references/performance-profiling.md](references/performance-profiling.md) — Unity Profiler, Unreal Insights, RenderDoc, frame budgeting, IL2CPP optimization
- [references/combat-systems-design.md](references/combat-systems-design.md) — Damage pipeline, hit detection (hitscan/projectile/AOE), status effects, buff/debuff architecture
- [Unity DOTS Documentation](https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/index.html)
- [Unity Netcode for GameObjects](https://docs-multiplayer.unity3d.com/netcode/current/about/)
- [Unreal Engine Gameplay Framework](https://docs.unrealengine.com/5.5/en-US/gameplay-framework-in-unreal-engine/)
- [GDC Vault — Overwatch Gameplay Architecture](https://www.gdcvault.com/play/1024003/)
- [Game Programming Patterns by Robert Nystrom](https://gameprogrammingpatterns.com/)
