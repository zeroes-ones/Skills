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
    - backend-developer
    - game-developer
    - game-engine-architect
    - performance-engineer
    - qa-engineer
  feeds_into:
    - game-developer
    - game-networking-developer
    - qa-engineer
---
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

# Gameplay Programmer — Real-Time Interactive Game Logic

Build production gameplay systems — spanning Unity (C#), Unreal Engine (C++/Blueprints), and custom engines — with deep expertise across the full game development lifecycle. Covers game loop architecture, entity-component-system (ECS) patterns, physics integration, input handling, camera systems, AI behavior trees, multiplayer state synchronization, animation state machines, procedural generation, and performance optimization to stable 60/120fps.
<!-- QUICK: 30s -->
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional work and amateur guessing:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify domain currency.** Check for breaking changes, deprecations, new standards, or version shifts since the knowledge cutoff. | [STALE_RISK] Outdated advice breaks real systems. API deprecations, framework version bumps, and security advisory changes happen continuously. Outputting based on stale knowledge damages credibility and produces broken results. | Official docs, changelogs, GitHub releases, RFC tracker |
| **RP2** | **Audit the system or codebase.** Read relevant files. Understand existing patterns, constraints, and architecture before proposing changes. | [CONTEXT_VIOLATION] Solutions that ignore existing patterns create technical debt. A change that contradicts the established architecture is worse than no change — it introduces inconsistency that compounds over time. | Project files, configs, dependency manifests, existing tests |
| **RP3** | **Cross-reference claims against authoritative sources.** Every factual assertion needs a verifiable source. Mark each: [VERIFIED], [COMPUTED], or [ESTIMATED]. | [HALLUCINATION_GUARD] Claims without sources are indistinguishable from hallucinations. The #1 cause of incorrect output is treating assumptions as facts. Source tagging prevents this. | Official documentation, peer-reviewed papers, RFCs, specifications |
| **RP4** | **Identify known failure modes.** Before recommending, list what commonly breaks. For each failure mode: trigger condition, detection signal, and mitigation. | [FAILURE_BLINDNESS] Every domain has known failure patterns. Output that doesn't address them is dangerously incomplete. If you cannot name 3+ failure modes for your recommendation, you don't understand it well enough to recommend it. | Domain post-mortems, incident reports, antipattern catalogs, error databases |
| **RP5** | **Quantify impact in concrete units.** Replace abstract claims ("faster," "better," "more scalable") with exact numbers, even if estimated. | [VAGUENESS_PENALTY] "Faster" is unverifiable. "Reduces p95 latency from 340ms to 120ms (±15ms)" is verifiable. Abstract adjectives hide ignorance behind confidence. Concrete numbers expose gaps. | Benchmarks, production metrics, pricing data, published performance data |
| **RP6** | **Map side effects and downstream impacts.** What else breaks? Which dependencies are affected? Which downstream consumers need updating? | [CASCADE_BLINDNESS] Changes to one component ripple outward. A fix in module A can break module B that depends on A's old behavior. Map the blast radius before acting. | Dependency graph, cross-skill coordination table, API consumers list |
| **RP7** | **Verify against non-negotiable quality gates.** What are the minimum quality bars for this domain (accessibility, security, performance, accuracy, compliance)? | [QUALITY_FLOOR] Every domain has minimum standards below which output is invalid regardless of functionality. Missing WCAG AA = broken. Leaking credentials = broken. Silent data loss = broken. | Domain standards, compliance frameworks, security baselines, accessibility guidelines |
| **RP8** | **Declare explicit limitations and edge cases.** What does this NOT handle? What are the known boundaries? What scenarios are explicitly out of scope? | [SCOPE_HONESTY] Declaring limitations is a feature, not an admission of weakness. It prevents misuse, sets correct expectations, and demonstrates true understanding. Every solution has boundaries — naming them is professional. | This SKILL.md, domain literature, edge case databases |

**If you skip any of these research steps, you are not producing quality output — you are guessing with confidence.** Guessing wastes time, breaks systems, and destroys trust. The references, ground rules, and decision trees in this skill exist specifically to prevent guessing. Use them.

> **Compliance:** Research must be executed before any substantial output. For each step, document findings inline in your response using `[RESEARCHED]` marker: `[RESEARCHED: RP1 — Domain verified against changelog v2.4. No breaking changes since cutoff.]`. Partial research = partial quality. Zero research = zero credibility.



### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

**The RP1-RP8 cycle above is NOT a one-time gate.** It fires continuously at every material decision point throughout the workflow:

| Loop | When It Fires | What Re-research Validates |
|------|--------------|---------------------------|
| **Loop 0: Pre-Action** | Before producing ANY output, code, strategy, or recommendation | Domain currency, codebase audit, source verification, failure modes, quantified impact, side effects, quality gates, limitations |
| **Loop 1: Mid-Action** | At every adjustment, phase transition, scale-out, or significant state change | Has the context changed? Are the original assumptions still valid? Has new information invalidated the Loop 0 conclusions? |
| **Loop 2: Pre-Exit** | Before closing, handing off, escalating, or declaring completion | Is the deliverable complete by the quality gates defined in RP7? Are all limitations declared (RP8)? Have failure modes been addressed (RP4)? |
| **Loop 3: Post-Action** | After completion: compare expected vs. actual outcome | What was the efficiency ratio (actual / theoretical max)? What learnings emerged? What should be fed back into the pattern database for future decisions? |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:
```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. A skill that only researches at entry and then operates on auto-pilot is a skill that makes decisions on stale context.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

**Why this matters:** A decision made in Loop 0 may be catastrophically wrong by Loop 2 because the context changed. Markets move. Requirements shift. Dependencies update. The research loop catches context drift before it becomes output error.

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence.



## Route the Request
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| **R1** | **NEVER run game logic in `Update()` that belongs in `FixedUpdate()`.** Physics calculations, Rigidbody manipulation, and collision-dependent logic in `Update()` cause framerate-dependent behavior — a jump that works at 60fps sends the player flying at 144fps. | Trigger: generated code uses `Rigidbody.AddForce()` or `Physics.Raycast()` inside `Update()` instead of `FixedUpdate()` | STOP. Move all physics code to `FixedUpdate()`. Cache non-physics state (input, animations) read from `Update()` in member variables, consumed by `FixedUpdate()`. Rule: `Update()` for input/graphics, `FixedUpdate()` for physics. |
| **R2** | **REFUSE to allocate memory in the game loop (Update/FixedUpdate/Tick).** Every `new`, `Instantiate()`, `GetComponent<>()`, LINQ expression, or `std::vector` resize inside the game loop allocates heap memory. GC spikes on Mono/IL2CPP cause 50-200ms frame hitches — players feel it as "stutter." | Trigger: generated code contains `new`, `Instantiate()`, `GetComponent<T>()`, `Find()`, `.ToArray()`, `.Where()` inside `Update()`/`FixedUpdate()`/`Tick()` | STOP. Pre-allocate in `Awake()`/`Start()`/`BeginPlay()`. Use object pools for bullets, particles, enemies. Cache component references in `Awake()`. Replace LINQ with for-loops. Rule: zero allocations after scene load. |
| **R3** | **REFUSE to use `GameObject.Find()` or `FindObjectOfType<T>()` in production code.** These scan the entire hierarchy — O(n) per call, 5-50ms on a scene with 10K objects. Calling them every frame crashes frame budget. | Trigger: generated code contains `GameObject.Find(` or `FindObjectOfType<` anywhere outside `Awake()` | STOP. Wire references via Inspector (`[SerializeField] private`), dependency injection, or service locator initialized once. `FindObjectOfType` allowed ONLY in `Awake()` for singleton initialization (once). |
| **R4** | **DETECT and WARN when multiplayer code uses client-authoritative state for gameplay decisions.** Movement speed, health, score, inventory — if the client can set these, hackers will. Every multiplayer game shipped with client-authoritative state has been ruined by cheaters within 48 hours of launch. | Trigger: generated code has `[Command]` without server validation OR `[SyncVar]` writable by client OR `Replicated` property with client setter | WARN: "This is client-authoritative. Every competitive multiplayer game that shipped client-authoritative state was destroyed by cheaters within 2 days. Server must validate ALL gameplay state changes. Client is a dumb terminal that sends inputs — server runs the simulation." |
| **R5** | **NEVER assume a consistent frame rate.** Frame rate varies by hardware, thermal throttling, background processes, and platform (Quest 2 at 72fps vs PC at 144fps). Code that assumes 60fps breaks at 30fps (slow-mo) and 144fps (hyperspeed). | Trigger: generated code multiplies by constant (e.g., `speed * 0.016f`) instead of `Time.deltaTime` (Unity) or `DeltaTimeSeconds` (Unreal) | STOP. Every movement, rotation, timer, and lerp must multiply by delta time. Use `Time.deltaTime` (Unity) or `GetWorld()->GetDeltaSeconds()` (Unreal). FixedUpdate uses `Time.fixedDeltaTime`. |
| **R6** | **REFUSE to leave debug code in production builds.** `Debug.Log()`, `GEngine->AddOnScreenDebugMessage()`, `print()`, and `DrawDebugLine()` in production cost 0.5-2ms per call — 10 calls per frame = 20ms at 60fps = frame drop. | Trigger: generated code contains `Debug.Log(` or `print(` or `DrawDebug` without `#if UNITY_EDITOR` / `#if WITH_EDITOR` guard | STOP. Wrap in `#if UNITY_EDITOR` (Unity) or `#if WITH_EDITOR` (Unreal). Use conditional compilation so debug code is stripped from builds. For runtime debugging, use a debug manager with runtime toggle. |
| **R7** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R8** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset
<!-- STANDARD: 3min -->

Competent gameplay programmers make features that work on their dev machine. Masters make features that hold 60fps on a 5-year-old console, never desync in multiplayer, and survive 100K entities without frame drops. The shift: stop coding for the demo video and start coding for the player who paid $70 and expects zero bugs.

**Cognitive biases that kill games:**
| Bias | How It Manifests | Antidote |
|------|-----------------|----------|
| **Dev-machine myopia** | Testing on an RTX 4090 + i9-14900K with 64GB RAM, then shipping to players on GTX 1060. "It runs fine for me" = 1-star Steam reviews. | Profile on minimum-spec hardware weekly. Set a performance budget: 16.6ms at 60fps (or 8.3ms at 120fps). Profile daily, not monthly. |
| **Network-neglect syndrome** | Building all gameplay as single-player, planning to "add multiplayer later." Retrofitting multiplayer doubles development time and introduces 200+ edge cases (latency compensation, state reconciliation, authoritative server migration). | If the game is multiplayer, build multiplayer from day 1. Run client-server with simulated latency (100ms) during development. |
| **Object-pool denial** | Using `Instantiate()`/`Destroy()` for bullets, particles, and enemies because "the profiler shows it's fine now." 100 simultaneous explosions = 100 GC allocations = 200ms frame hitch when the GC runs. | Object-pool every frequently-spawned GameObject. Bullets, particles, audio sources, UI elements. One pool per prefab, pre-warm to peak capacity. |

## Operating at Different Levels
<!-- STANDARD: 3min -->

| Level | Gameplay Programmer Output |
|-------|--------------------------|
| **L1 — Junior** | Implements features following existing patterns. Player controller from template, basic AI patrol. Works in single-player context. |
| **L2 — Mid** | Implements complex gameplay systems independently. Combat with damage types, status effects, hit reactions. Performance-conscious (object pooling, no per-frame allocations). Handles basic multiplayer (NetworkBehaviour, RPCs). |
| **L3 — Senior** | Architects gameplay systems for entire game. ECS vs GameObject tradeoffs. Authoritative server with prediction + reconciliation. Behavior tree architecture for 50+ AI types. Performance budgets enforced in CI. |
| **L4 — Lead** | Defines gameplay architecture across multiple titles. Custom netcode decisions. Engine-level optimizations (Jobs/Burst, compute shaders). Mentors team on performance patterns. Cross-discipline with design, art, audio. |
| **L5 — Principal** | Industry-defining gameplay systems. Ships technology used by dozens of studios. Invents new gameplay paradigms. "This netcode architecture became the studio standard for the next 5 years." |

### Solo / Small / Medium / Enterprise

| Scale | Challenge | Solution |
|---|---|---|
| **Solo dev** | All gameplay systems, alone | Unity with Asset Store for non-core systems; simplify feature scope; focus on 1-2 tightly coupled mechanics that create depth |
| **Small team (2-10)** | Merge conflicts on core gameplay scripts | Modular system boundaries; each system owner has clear interface contracts; weekly gameplay integration playtests |
| **Medium (10-50)** | Multiplayer introduces exponential complexity | Dedicated netcode engineer; server-authoritative from day 1; client prediction + reconciliation tested in CI with 100ms simulated latency |
| **Enterprise (50+)** | Cross-studio consistency; engine modifications | Shared gameplay framework with code review gates; ECS architecture mandatory for 500+ entity scenes; custom engine branch with contribution guidelines |

**Transition Triggers:** When 3+ gameplay systems interact → system boundary docs with interface contracts. When multiplayer is announced → dedicated netcode engineer, not an afterthought. When entity count exceeds 500 per scene → ECS migration. When team exceeds 10 → per-system owners and weekly gameplay integration tests.

## When to Use
<!-- STANDARD: 3min -->

- Building player controllers: first-person, third-person, top-down, vehicle, flight
- Implementing combat systems: hit detection, damage calculation, status effects, buffs/debuffs, elemental systems
- Designing AI behavior: finite state machines, behavior trees, utility AI, GOAP, navmesh navigation
- Setting up multiplayer: authoritative server, client-side prediction, state reconciliation, lag compensation
- Optimizing performance: object pooling, LOD systems, occlusion culling, Jobs/Burst, ECS
- Creating animation systems: state machines, blend trees, IK, procedural animation, root motion
- Building save/load: serialization, checkpoint systems, persistent world state
- Implementing procedural generation: level generation, loot tables, enemy placement, terrain

## Decision Trees **(QUICK)**
<!-- STANDARD: 3min -->

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

## Core Workflow **(STANDARD)**
<!-- STANDARD: 3min -->

### Phase 1 (~20 min): Project Setup & Game Loop Architecture
1. **Engine selection**: Unity (C#, best for mobile/indie/2D/3D), Unreal (C++/Blueprints, best for AAA/3D/FPS/photoreal), Godot (GDScript/C#, best for 2D/small team/open source)
2. **Game loop**: `Update()` → input collection → gameplay logic → `FixedUpdate()` → physics step → LateUpdate → rendering. Never mix physics and rendering logic.
3. **Scene architecture**: Bootstrap scene (persistent) → managers (GameManager, AudioManager, PoolManager) → level scenes (additive loaded)
4. **Singleton pattern**: `MonoBehaviour` singletons ONLY for managers. All other objects injected or referenced via Inspector. Rule: max 5 singletons per project.
  Complete when: Engine is selected, game loop scaffold runs at target frame rate, and a persistent bootstrap scene loads a test level additively.

### Phase 2 (~25 min): Player Controller & Input
- **Input System**: Unity Input System Package (event-driven, rebindable, multi-device) or Unreal Enhanced Input. Never use legacy `Input.GetKey()`.
- **Controller architecture**: Input → Input Handler → Command → Controller → Movement/Abilities. Decouple input from action.
- **Camera**: Cinemachine (Unity) or SpringArmComponent (Unreal). Collision detection, camera shake, FOV changes. Never parent camera directly to player — use virtual camera with damping.
  Complete when: Input → Command → Controller pipeline works with at least one rebindable action, and the camera follows the player with collision detection.

### Phase 3 (~30 min): Combat & Damage Systems
- **Hit detection**: Raycast (hitscan), sphere cast (melee AOE), projectile (physics-based). Pick based on weapon type.
- **Damage pipeline**: Attacker → DamageData (amount, type, source, penetration) → Receiver.Armor.Reduce() → Health.Apply(). Each step is testable independently.
- **Status effects**: Buff/Debuff as components with duration, tick rate, stack behavior. ScriptableObject for data, MonoBehaviour for runtime.
  Complete when: A damage event flows through the full pipeline — from attacker to receiver health bar — with armor reduction applied and at least one status effect ticking.

### Phase 4 (~30 min): Multiplayer Implementation
- **Client-Server model**: Server runs gameplay simulation. Client sends inputs, receives state. Client predicts locally for responsiveness.
- **State sync**: SyncVars (Unity NGO/Mirror) or Replicated properties (Unreal). Only sync what changed, only to relevant clients.
- **RPCs**: ServerRpc (client→server, validated), ClientRpc (server→clients, broadcast or targeted). Never trust ClientRpc parameters — validate on server.
  Complete when: Two clients connect to a server, player movement replicates with <50ms reconciliation error at 100ms simulated latency, and a ServerRpc executes with server-side validation.

### Phase 5 (~25 min): Animation Integration
- **State machine**: Idle → Walk → Run → Jump → Fall → Land. Blend trees for direction + speed. Animation events for footstep sounds, hit frames, weapon trails.
- **Procedural animation**: IK for foot placement on uneven terrain, look-at for head tracking, weapon sway. Reduces animation asset count by 60%.
  Complete when: Idle→Walk→Run blend tree transitions by speed, jump/fall states trigger correctly, and at least one animation event fires a gameplay callback (footstep, hit frame).

### Phase 6 (~20 min): Save/Load & Persistence
- **Save architecture**: GameState → serialized to JSON/binary → compressed → written to disk. Always write to temp file, rename atomically — prevents corruption on crash mid-save.
- **What to save**: Player position (checkpoint), inventory, quest progress, world state (opened doors, killed enemies, collected items). NEVER save: visual effects, transient audio, temporary decals.
  Complete when: Save writes atomically (temp file → rename), loads with version header validation, and survives a crash mid-save with zero corruption. Load from save restores all game state.
  Complete when: All tests pass — unit, integration, and E2E with > 80% coverage on new code.
  Complete when: Accessibility audit passes — WCAG 2.1 AA compliance with automated and manual checks.

## Best Practices
<!-- STANDARD: 3min -->

1. **Input → Command → Controller architecture decouples input from action** — Unity Input System or Unreal Enhanced Input maps raw input to semantic commands (`Jump`, `Shoot`, `Interact`). Controllers consume commands, never raw key codes. This enables rebindable controls and multiplayer replay from input logs.
2. **Behavior trees over finite state machines for AI with 10+ states** — Behavior trees compose reusable sub-trees (patrol, investigate, attack, flee). For Unity, use `BehaviorDesigner` or built-in `BehaviorTree` in Unity Muse; for Unreal, native `UBehaviorTree` with `UBTDecorator` and `UBTTaskNode`. State machines become unmaintainable spaghetti beyond ~15 states.
3. **Animation state machine with blend trees for direction + speed** — `Idle → Walk → Run` transitions by `Speed` parameter. Blend tree maps `MoveDirection` to strafe/walk forward/backward. For Unreal, use `BlendSpace1D`/`2D`. Never use raw animation clips with hard cuts — instant transitions look robotic.
4. **Server-authoritative with client prediction and reconciliation** — Server validates every `ServerRpc`, runs game logic, and broadcasts state. Client predicts movement locally, reconciles position on `ClientRpc` state update. Unity Netcode for GameObjects: `NetworkTransform` with `Interpolate = false` on owner, `true` on proxies; for Unreal: `bReplicateMovement = true` on `ACharacter`.
5. **Hit detection: raycast for hitscan, sphere cast for melee AOE, physics projectile for grenades/rockets** — Raycast weapons fire instantly and register on the frame of the trigger pull. Projectile weapons use `Rigidbody` with continuous collision detection (`CollisionDetectionMode.ContinuousDynamic`). Never use `OnTriggerEnter` without proper layer mask filtering.
6. **Object pooling for bullets, particles, enemies, UI elements with pre-warmed capacity** — `ObjectPool<T>` generic with `Get()` → reset state → use → `Release()`. For Unity: `PoolManager` Singleton with per-type pools. For Unreal: `UActorComponent` pools managed via `UWorld` subsystem. A bullet-hell game spawns 200 projectiles/second — without pooling, GC runs every 2 seconds.
7. **Save architecture: atomic writes with version header and corruption detection** — Serialize `GameState` → JSON/binary → compress → write to temp file → fsync → rename over target. Include `saveVersion` in the header; every update ships a migration from `saveVersion-1`. SHA256 checksum at end of file detects corruption on load. Never write directly to the save file — a crash mid-write destroys the save.
8. **Fixed timestep for physics and gameplay logic; variable deltaTime only for visual interpolation** — All gameplay code in `FixedUpdate()` (Unity) or tick callback (Unreal). Use `Time.deltaTime` (Unity) / `GetWorld()->GetDeltaSeconds()` (Unreal) ONLY for camera smoothing, particle effects, and UI animations. Physics behavior at 30Hz vs 120Hz must be identical.
9. **`link.xml` for IL2CPP stripping preservation in Unity** — Add `[Preserve]` attribute to all types used via reflection (`StartCoroutine("MethodName")`, `SendMessage()`, custom serialization). Create `link.xml` in Assets root with `<assembly fullname="Assembly-CSharp"><type fullname="*" preserve="all"/></assembly>` for critical assemblies. Test on device, not Editor.
10. **Network prediction error under 50ms at 100ms simulated latency** — Measure reconciliation error: `|clientPredictedPosition - serverAuthoritativePosition|`. Must converge within 3 physics ticks. If error exceeds threshold, increase update rate or reduce extrapolation duration. Players feel lag at >50ms reconciliation error, rage-quit at >100ms.

## Error Recovery **(STANDARD)**
<!-- STANDARD: 3min -->

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Using `Instantiate`/`Destroy` for bullets without object pooling — GC runs every 2 seconds at 200 projectiles/second, 15ms hitches | $20K-$80K in post-launch optimization patches and "poorly optimized" reviews | Pre-warm `ObjectPool<T>` with `Get()` → reset → `Release()`. Pool bullets, particles, enemies, and UI elements. A bullet-hell game without pooling is unshippable on console. |
| Building single-player, then retrofitting multiplayer — every gameplay system must be rewritten for authoritative server | $50K-$200K in near-complete rewrite (100% overhead vs 20% if done from day one) | Input → Command pattern, server-authoritative validation, and state serialization from day one. Day-1 multiplayer costs 20% overhead; retroactive multiplayer costs 100%. |
| Not multiplying forces by `Time.fixedDeltaTime` in `FixedUpdate()` — physics behave differently at 50Hz vs 30Hz (thermal throttling) | $20K-$80K in post-launch patches, "floaty controls" reviews, and lost featuring | Test physics at `fixedDeltaTime = 0.033` (30Hz), `0.02` (50Hz), `0.013` (75Hz). Character behavior must be identical. Console certification REQUIRES stable frame rate — 0 dropped frames in certification run. |
| AI tested only on clean test levels (3 enemies, no dynamic obstacles) — 20 enemies with destructible cover on production levels takes 14ms, leaving 2ms for everything else | $15K-$50K in AI rewrite weeks before ship | Profile AI on production levels with full enemy counts, dynamic navmesh obstacles, and destructible cover. Test-level AI performance is fantasy data. Production is the only benchmark that matters. |
| Saving directly to the save file instead of atomic write-then-rename — crash mid-save corrupts the file, user loses 40+ hours of progress | $30K-$100K in support burden and review-bombing from save corruption | Write to temp file → fsync → rename over target. Include `saveVersion` header for migration. SHA256 checksum detects corruption on load. Atomic saves prevent the most rage-inducing bug in gaming. |

## Verification Guardrails
<!-- STANDARD: 3min -->

Run these checks before declaring work complete. ALL must pass.

| # | Guardrail | Check |
|---|-----------|-------|
| V1 | Output matches specification | Compare generated output against the requirements stated at the start. Every explicit requirement must have a corresponding deliverable. |
| V2 | No broken references or links | All file references must resolve. Run `grep -oP '\]\([^)]+\)' [output] | while read link; do [ -f "$link" ] || echo "BROKEN: $link"; done`. |
| V3 | All validations pass where applicable | Run any existing test suite or verification script. `bash scripts/validate-skills.sh` if in this repository. |
| V4 | No placeholder or TODO content remains | `grep -ri 'TODO\|FIXME\|PLACEHOLDER' [output]` must return empty. |
| V5 | Error states handled | Verify error paths produce clear messages, not silent failures or stack traces. |
| V6 | Edge cases considered | Empty input, max/min values, concurrent access, boundary conditions handled or documented as out-of-scope. |
| V7 | Performance within budget | If constraints specified, verify compliance. If not, verify no unbounded loops or quadratic blowup. |
| V8 | Anti-patterns from Gotchas section avoided | Re-read Gotchas section. Verify none of the listed anti-patterns appear in the output. |

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `game-developer` | Game design document, mechanic specs, balance curves, progression systems | Before implementing any gameplay mechanic |
| `game-engine-architect` | Engine selection, rendering pipeline architecture, memory budget, threading model | Before choosing ECS vs GameObject, Jobs vs main thread |
| `game-networking-developer` | Netcode architecture, transport layer, matchmaking, relay servers | Before implementing multiplayer gameplay |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `qa-engineer` | Playable build, performance baseline (frame rate, memory), multiplayer test configuration | QA can't test without playable gameplay |
| `performance-engineer` | Profiler captures, CPU/GPU frame breakdowns, object allocation traces | Performance work is blind without gameplay profiling data |

## Verification
<!-- STANDARD: 3min -->

1. **[Build/compile verification]** — Verify the implementation compiles and runs without errors by executing the project build command and confirming exit code 0
2. **[Test suite pass]** — Verify all unit, integration, and end-to-end tests pass by running the test suite and confirming zero failures
3. **[Edge case handling]** — Verify edge cases (empty state, error state, boundary conditions, concurrent access, interrupted operations) are handled with graceful degradation rather than crashes

**Pass criteria:** All checks pass before delivering output.

## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "I'll optimize after all gameplay features are done — premature optimization is evil." | Gameplay architecture determines performance ceiling. Object pools, ECS choice, and authoritative server model must be decided before 10K lines of MonoBehaviour code exist. Retrofitting pools into 200 files is a rewrite, not a refactor. Cost: 4-8 weeks. |
| "Multiplayer can wait until the single-player demo is approved." | Every gameplay system built single-player (player controller, combat, AI, inventory) must be rewritten for authoritative server. Input → Command pattern, state serialization, and prediction are incompatible with direct state mutation. Day-1 multiplayer costs 20% overhead; retroactive multiplayer costs 100%. |
| "The profiler shows 58fps — close enough to 60, we'll ship." | 58fps means 1 dropped frame every 0.5 seconds. Players perceive it as "jank." App Store and Google Play feature only 60fps-stable games. Console certification (Sony, Microsoft) REQUIRES stable frame rate — 0 dropped frames in certification test run. |
| "We don't need object pooling — modern GC is fast." | Unity Mono GC collects 1MB in ~2ms. A bullet hell game spawning 200 bullets/second with `Instantiate`/`Destroy` generates 40KB garbage per bullet = 8MB/second. GC runs every 2 seconds = 15ms hitches. Players call it "stutter," reviewers call it "poorly optimized." |
| "The AI behavior tree works in the test level — ship it." | Test levels have clean navmeshes, no dynamic obstacles, 3 enemies. Production levels have 20 enemies, destructible cover, dynamic navmesh obstacles, and 16ms frame budget. AI that takes 2ms in test takes 14ms in production — leaves 2ms for everything else. Profile on production levels, not test levels. |

## Anti-Patterns
<!-- STANDARD: 3min -->

- **FixedUpdate at wrong timestep — game plays in slow-mo or hyperspeed on different hardware.** Unity's `Time.fixedDeltaTime` defaults to 0.02 (50Hz). If your `FixedUpdate()` relies on this without multiplying forces by `Time.fixedDeltaTime`, physics behaves differently at 50Hz vs 30Hz vs 100Hz. A character that jumps correctly at 50Hz may barely leave the ground at 30Hz (mobile thermal throttling). **$20K-$80K in post-launch patches, negative reviews citing "floaty controls," and lost featuring on app stores for inconsistent physics behavior.** Test physics at fixedDeltaTime = 0.033 (30Hz), 0.02 (50Hz), 0.013 (75Hz).

- **`GameObject.Find()` in `Update()` — frame drops from 60fps to 3fps on level restart.** A developer adds `GameObject.Find("Player")` to reconnect references after scene reload. In a scene with 15K objects, `Find()` scans the entire hierarchy taking 8-25ms. Called every frame = permanent 3fps. **$5K-$15K in wasted profiling and debugging, with developers searching for "memory leaks" that don't exist.** Solution: Cache all references in `Awake()`. If you must find dynamically, use `FindWithTag()` (indexed by engine) or maintain a manager with a registration dictionary.

- **IL2CPP stripping removes event functions used via reflection — game silently breaks on iOS.** Unity's IL2CPP strips unused code. If your `MonoBehaviour` uses `StartCoroutine()` with a method name string or `SendMessage()`, the target method is stripped from the build. The game works in Editor (Mono JIT) and silently fails on device. **$30K-$100K in App Store rejection, emergency patches with 48-hour review wait, and lost launch momentum.** Solution: Add `[Preserve]` attribute or a `link.xml` file to prevent stripping. Never use `SendMessage()` — use direct method calls or C# events.

- **Uncapped deltaTime in replays — game diverges after 20 seconds.** Deterministic replays require fixed timestep simulation. If your replay system captures inputs and replays them using `Update()` (variable deltaTime), floating point divergence causes the replay to drift within seconds. Characters walk through walls, bullets miss, the replay is garbage. **$50K-$200K for competitive games — esports replays are the primary anti-cheat evidence; broken replays mean unbannable cheaters.** Solution: Record at fixed timestep. All gameplay logic in `FixedUpdate()` with deterministic math (no `float` random without seeded RNG). Verify replay determinism via checksum comparison at key frames.

- **`[SerializeField]` references break silently when prefab is nested — null reference in production.** A nested prefab's serialized reference to a sibling component survives in the top-level prefab but becomes null when the nested prefab is instantiated in a different context (prefab variant, addressable asset). The game ships with `NullReferenceException` in production logs, which players don't see but causes invisible failures (AI doesn't patrol, doors don't open). **$10K-$40K in "can't reproduce" bug reports, negative reviews, and support tickets for broken quests.** Solution: Use `GetComponentInChildren<T>()` or `GetComponentInParent<T>()` for references within the same prefab hierarchy. Serialized references only for cross-prefab (scene-level) connections.

- **Animator.SetTrigger() called but animation doesn't play — state machine transition condition blocks it.** The Animator state machine only processes triggers when in a state that has a transition listening for that trigger. If the character is in the "Death" state and you call `SetTrigger("Jump")`, the trigger is consumed but no transition exists = the jump never plays and the trigger is permanently consumed. **$5K-$20K in animation bugs reported as "character frozen," "unresponsive controls."** Solution: Use `Animator.ResetTrigger()` before setting. Verify transition exists from current state. For critical animations (hit reaction, death), use `Animator.Play()` to force state change bypassing transitions.

- **Multiplayer: `NetworkTransform` smooths position with default interpolation — players visually overshoot corners.** Default network interpolation smooths from old state to new state over 100ms. When a player stops moving, the interpolation continues for 100ms — the character model slides past the stopping point and snaps back. Players perceive this as "lag" even at 20ms ping. **$15K-$50K in multiplayer beta feedback: 'netcode is broken,' 'rubber-banding,' 'unplayable.'** Solution: Use `NetworkTransform` with rigidbody-based interpolation mode. Tune `Interpolate` to 0.1-0.2 for snappy response. Implement client prediction for player-owned objects — the local player should never see interpolation lag.

## What Good Looks Like
<!-- STANDARD: 3min -->

> The game runs at a locked 60fps (16.6ms) on minimum-spec hardware with 500 active entities, zero per-frame allocations after scene load, and no GC spikes. Player input feels instantaneous (<100ms from button press to visual response). Multiplayer is authoritative — the server validates every gameplay action, clients predict locally with <50ms reconciliation error. AI enemies navigate dynamic environments without getting stuck, and their behavior scales from 3 to 100 entities without algorithmic complexity explosion. Save/load is atomic — corrupted saves don't exist because writes are never in-place. The profiler shows gameplay CPU at <3ms, leaving 13ms for rendering, physics, and future features.

## Deliberate Practice
<!-- STANDARD: 3min -->

1. **60fps from scratch**: Build a bullet hell with 1,000 bullets on screen at 60fps on a mid-range device. Must use object pooling, DOTS/ECS, and zero per-frame allocations. Profile and document every allocation found and removed.
2. **Authoritative server from day 1**: Implement a simple competitive game (Pong or a racing game) with authoritative server, client prediction, and reconciliation. Measure reconciliation error. Must feel responsive at 100ms simulated latency.
3. **AI crowd**: Implement 100 AI agents navigating a dynamic city with obstacles appearing mid-game. Must maintain 60fps. Use ECS, flow fields, or hierarchical pathfinding. Agents must never get stuck.

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## Error Decoder — War Stories from the Trenches
<!-- STANDARD: 3min -->

**(STANDARD)**

When gameplay code goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Animation event fires on wrong frame during transition — character punches air instead of hitting, damage numbers appear before contact | Animation event is placed on the outgoing animation clip. During a blend/transition, both old and new animations fire events. The old animation's "Hit" event fires simultaneously with the new animation's "Idle" frame | Place animation events only on the target animation clip, not on transitions. For critical events (damage, effects), use state-machine behaviors with `OnStateEnter`/`OnStateExit` instead of clip events. Verify event timing with `Animator.frameCount` debugging in Editor | Animation events fire based on normalized time, not visual state. During a 0.3s crossfade, both animations are "playing" and both fire events. State-machine behaviors are more reliable than clip events for gameplay-critical moments |
| NavMesh agent stuck walking into a wall — NPC runs in place, players report "brain-dead AI" | NavMesh destination is inside a non-walkable area or behind a dynamic obstacle. `SetDestination()` succeeds (returns true) but the agent never reaches the point. It raycasts to a position it can never arrive at | Check `NavMesh.SamplePosition(destination, out hit, 2.0f, NavMesh.AllAreas)` before setting destination. Use `NavMeshPath` validation: `NavMesh.CalculatePath()` and check `path.status == NavMeshPathStatus.PathComplete`. Set `agent.autoRepath = true` for dynamic obstacles | `SetDestination()` returning true only means the point was accepted — not that it's reachable. NavMesh agents will happily pathfind to unreachable destinations and walk into walls forever |
| Object pool returns an already-active object — enemy spawns with half health, wrong position, carrying the previous instance's state | Pool "returns" an object to the pool but doesn't reset its state. The next `Get()` call gives the caller an object that still has velocity, health, and target from its previous life. It teleports to the caller's position but retains the old velocity — flies off screen | Reset ALL mutable state when returning to pool: `OnReturnToPool()` method that zeros velocity, resets health to max, clears target, resets animator to default state. Enforce via interface: `IPoolable { void OnGet(); void OnReturn(); }`. Add a debug check: if poolable is active, log error and don't return | Object pooling is not just allocation avoidance — it's lifecycle management. A pooled object that isn't fully reset carries its previous life's state. The bug is silent because the object "looks right" at spawn — it only misbehaves 2 frames later |
| Save file loaded on wrong game version — all NPCs spawn at world origin, quest flags are scrambled, inventory is empty | Save file lacks a version header. The new game build interprets old save data with new field offsets. An `int` that used to be `health` is now read as `mana` because the serialization format changed | Include a semantic version in the first 4 bytes of every save file. On load, check version: if different, run migration: `if (saveVersion < 2) MigrateV1ToV2(data)`. Never change the binary layout of existing fields — only append. Keep all migration functions forever | Save file compatibility is a promise to every player who's ever saved your game. One field reorder corrupts every save ever made. Version headers and append-only schemas are non-negotiable |
| Player input feels "floaty" or "laggy" — streamers blame the game, not their setup. Reviewers say controls are "unresponsive" | Input is processed in `Update()` but character movement is in `FixedUpdate()`. At 144 FPS, `Update` runs 2-3 times per `FixedUpdate`. Input from the first two `Update` calls is overwritten by the third before `FixedUpdate` reads it | Buffer input: accumulate input in `Update()`, consume and clear in `FixedUpdate()`. Use `InputSystem` with `InputAction.started/performed/canceled` callbacks. For immediate-response actions (jump, dash), process in `Update()` and apply visual feedback immediately — let `FixedUpdate` handle physics | Input polling is lossy by default. If `Update` runs 3 times per `FixedUpdate` and you overwrite the input variable each time, 2 out of 3 player inputs are silently dropped. Input buffering costs one `List<InputFrame>` and eliminates "my input was eaten" |
| Physics objects jitter or vibrate on slopes — character slides down a 1° incline, camera shakes uncontrollably | `Rigidbody` position is being set directly in `Update()` instead of through forces. The physics engine applies gravity → moves the body down slope → your code teleports it back up → physics pushes it down again. 60Hz tug-of-war creates visible vibration | Use `Rigidbody.AddForce()` or `Rigidbody.MovePosition()` instead of `transform.position =`. Set `Rigidbody.interpolation = Interpolate` for smooth visual output. For character controllers, use `CharacterController.Move()` or configure `PhysicsMaterial` with appropriate static/dynamic friction | Directly setting transform.position on a Rigidbody is fighting the physics engine. Every frame, you teleport the object to where you think it should be, and the physics engine instantly corrects you. Use forces, not teleportation |

## Production Checklist **(DEEP)**
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

| Trigger | Action | Rationale |
|---|---|---|
| `GameObject.Find()` or `SendMessage()` found in PR | Block merge — flag as performance anti-pattern | These methods scan entire scene hierarchy; single call costs 0.5-10ms on production scenes |
| Frame rate drops below target in profiler capture | Investigate update loop, physics tick, GC allocation. Check `Time.deltaTime` variance >2ms | Players perceive inconsistency before they see low average FPS — spikes cause "micro-stutter" that drives negative reviews |
| Player reports "lag" or "rubber-banding" in multiplayer | Verify client prediction error threshold. Check if reconciliation snapshots exceed 3-frame window | Desync beyond 50ms is felt by players; beyond 100ms causes rage-quits. Prediction must converge within 3 physics ticks |
| New animation added without state machine diagram | Require state diagram showing all transitions, conditions, and exit times before review | Animation bugs (snapping, stuck states, wrong blends) are the #1 visual bug category — state diagrams prevent 80% of them |
| `Awake()` or `Start()` growing beyond 20 lines | Refactor into separate initialization phases with explicit ordering | Unity's script execution order is non-deterministic by default; bloated Awake/Start creates Heisenbugs that only reproduce on certain machines |
| Save file version mismatch after update | Run migration path; never silently fail. Alert player if save cannot be migrated | Corrupted saves cause players to abandon games — a single corrupted 60-hour save file generates more negative reviews than any other bug |

## References
<!-- STANDARD: 3min -->

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
