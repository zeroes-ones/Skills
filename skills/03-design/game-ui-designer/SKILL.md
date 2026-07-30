---
name: game-ui-designer
description: >
  Use when designing user interfaces for games — HUD layouts, menu systems,
  diegetic/non-diegetic UI patterns, controller and gamepad input mapping,
  cross-platform game UI (console, PC, mobile), accessibility for game interfaces
  (subtitles, colorblind modes, remappable controls), and performance-constrained
  UI rendering at 60fps+. Handles game-specific interaction patterns that standard
  UI/UX skills don't cover. Do NOT use for game design (mechanics, systems, narrative),
  game engine selection, or non-game application UI.
license: MIT
allowed-tools: Read Grep Glob
tags:
  - gaming
  - game-ui
  - hud
  - game-ux
  - accessibility
  - controller
  - cross-platform
author: Sandeep Kumar Penchala
type: design
status: stable
version: 1.0.0
updated: 2026-07-26
token_budget: 3200
chain:
  consumes_from:
    - ui-ux-designer
    - accessibility-auditor
  feeds_into:
    - game-developer
    - frontend-developer
    - mobile-developer
---
# Game UI Designer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

Design user interfaces for games — an entirely different discipline from application UI. Game UI is part of the experience, not a tool to accomplish a task. It must communicate state instantly, never break immersion, and work across fundamentally different input devices (controller, touch, mouse/keyboard).
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

### Auto-Route

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.unity", "Canvas")` OR `file_contains("*.unity", "uGUI")` | Unity UI project. Jump to **Core Workflow → Phase 2 (Implementation)**. |
| A2 | `file_exists("*.umap")` OR `file_exists("*.uasset")` | Unreal Engine project. Jump to **references/unreal-umg-patterns.md**. |
| A3 | `file_exists("*.tscn")` AND `file_contains("*.tscn", "Control")` | Godot project. Jump to **references/godot-ui-patterns.md**. |
| A4 | `file_contains("*.css", "game-ui|hud|menu")` | Web game UI. Jump to **Core Workflow → Phase 2 → Web Game UI**. |

### Intent Route

```
What are you designing?
├── HUD (health bars, minimaps, ammo counters, quest trackers) → Core Workflow → HUD Design
├── Menu system (main menu, pause, settings, inventory) → Core Workflow → Menu Design
├── Diegetic UI (in-world screens, holograms, spatial displays) → Core Workflow → Diegetic UI
├── Controller-first UI (gamepad navigation, console menus) → Core Workflow → Input & Navigation
├── Accessibility for a game (subtitles, colorblind, controls) → Core Workflow → Accessibility
├── Not sure what UI paradigm fits my game → Describe the game genre, camera perspective, and platform
└── Need general UI/UX design → ui-ux-designer
```

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|--------------------|--------------------|
| G1 | Never design game UI at a fixed resolution — it must scale from 720p handheld to 4K displays | `file_contains(spec, "1920x1080")` AND NOT `file_contains(spec, "scale|anchor|canvas.scaler|safe.zone")` | REFUSE. "Resolution-dependent UI will break on different screens. Define anchor points, safe zones, and scale modes." |
| G2 | Never design controller navigation without a visual focus indicator — players must always see what's selected | `file_contains(spec, "controller|gamepad|d-pad")` AND NOT `file_contains(spec, "focus.indicator|highlight|selection.visual")` | REFUSE. "Controller navigation requires a visible focus indicator at all times. Specify highlight state and transition animation." |
| G3 | Never use text smaller than 24px equivalent for critical gameplay information (health, ammo, time) | `file_contains(spec, "font.*size.*[0-9]")` AND `file_contains(spec, "health|ammo|timer|crosshair")` | DETECT. "Critical gameplay text must be legible at a glance. Minimum 24px at 1080p reference resolution." |
| G4 | Never design a menu that requires more than 3 button presses to return to gameplay | `file_contains(spec, "menu|settings|inventory")` AND NOT `file_contains(spec, "depth|back.press|quick.return")` | STOP. "Menu navigation must return to gameplay in ≤3 presses (pause → resume, or settings → back → resume)." |
| G5 | Never ship game UI without subtitles, colorblind support, and remappable controls | `file_contains(spec, "game|release")` AND NOT `file_contains(spec, "subtitle|colorblind|remap|accessibility")` | REFUSE. "Games ship to millions of players. Accessibility is non-optional: subtitles (with speaker labels), colorblind modes (3 types), and fully remappable controls." |
| G6 | Never specify game telemetry, analytics, or crash reporting that captures player PII without explicit consent and redaction | `file_contains(spec, "telemetry|analytics|crash.report|track.event")` AND NOT `file_contains(spec, "consent|redact|sanitize|PII|GDPR|COPPA|anonymize")` | REFUSE. "Game telemetry must never capture PII without consent. Specify: opt-in consent flow with clear language, PII redaction pipeline (names, emails, IP addresses, device IDs), COPPA compliance if targeting under-13 audience, GDPR right-to-deletion design. Crash reporters must strip screen contents and user input. Analytics must use anonymous session tokens." |
| G7 | Never specify a HUD animation without its frame budget impact, haptic pairing, and reduced-motion fallback — game UI animations compete with the render budget | `file_contains(spec, "animate|pulse|shake|flash|fade|spring|tween")` AND NOT `file_contains(spec, "frame.budget|ms.budget|haptic|prefers-reduced-motion|accessibility")` | REFUSE. "Game UI animations cost frame time and must be budgeted: (1) UI animation budget ≤1ms per frame at target FPS — the rest belongs to rendering/physics/AI, (2) every animation must specify: duration (ms), easing, trigger, haptic pairing (light/medium/heavy per platform SDK), and reduced-motion alternative (instant or fade), (3) health pulse must pair with controller rumble, (4) damage flash must never exceed 3 flashes/second — seizure safety threshold, (5) diegetic animations (in-world holograms, screens) share the 3D render budget — more expensive than canvas overlay." |

## The Expert's Mindset
<!-- STANDARD: 3min -->

Game UI is not a tool — it's a **diegetic or semi-diegetic extension of the game world**. Players should feel the UI belongs in the game's universe, not overlaid on top of it. The best game UI is the one the player never notices.

### Mental Models

| Model | Description |
|---|---|
| **Diegesis spectrum** | Every UI element falls on a spectrum: diegetic (exists in game world — wall-mounted screens, holograms), non-diegetic (floating HUD — health bars, minimaps), spatial (UI embedded in 3D space), meta (fourth-wall-breaking — narrator UI). Choose intentionally. |
| **Peripheral readability** | Players read HUD elements with their peripheral vision. Size, contrast, and animation must work when the player isn't looking directly at the element. |
| **Input modality defines layout** | A controller menu (radial, grid, list with d-pad) is completely different from a mouse menu (cursor, click, drag) which is different from touch (direct manipulation, swipe). Design for the primary input first. |
| **Diegetic UI costs performance** | In-world UI (holograms, screens) renders as part of the 3D scene and costs draw calls, overdraw, and GPU time. Non-diegetic UI (canvas overlay) is cheaper but less immersive. |

### Cognitive Biases in Game UI

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Fidelity trap** | Making the HUD too visually complex because "it looks cool" | Test HUD readability with a 5-second glance test. If the player can't read their health in <500ms, it fails. |
| **PC-first myopia** | Designing for mouse precision and forgetting controller or touch | Every menu must be navigable with a d-pad. Every button must have a controller focus state. |
| **Over-information** | Showing everything "just in case" — cluttering the periphery | For every HUD element, ask: "Does the player need this RIGHT NOW, or can it appear contextually?" |
| **Aesthetic-usability in games** | A beautiful, minimalist HUD that doesn't communicate critical state | Form follows function. A health bar must communicate health; looking good is secondary. |

### What Masters Know

- **The HUD is a contract with the player.** If you show a health bar, the player trusts that number. If damage is inconsistent with the display, you've broken the contract.
- **Animation is information, not decoration.** A health bar that pulses when critical or flashes on hit is communicating. Animation without information is motion sickness.
- **Audio cues replace visual UI.** Footstep sounds, heartbeat on low health, ammo-click on empty — audio is UI. Design the soundscape as part of the interface.

**HUD animation catalog (by gameplay function):**

| Function | Animation | Duration | Haptic | Reduced Motion | Frame Cost |
|---|---|---|---|---|---|
| Low health (<25%) | Red vignette pulse + health bar pulse | Pulse 1Hz, continuous | Heavy rumble (controller) / long vibration (mobile) | Static red vignette + "LOW HEALTH" text | ~0.3ms (color overlay) |
| Take damage | Screen edge red flash + health bar shake | 150ms | Medium impact | Instant health bar decrement — no flash | ~0.2ms (flash) + ~0.1ms (shake transform) |
| Critical hit landed | Yellow/gold flash + damage number pop | 100ms flash, 400ms number | Light tap | Static gold damage number | ~0.2ms (flash) + ~0.3ms (text animation) |
| Ability cooldown | Radial wipe + number countdown | Real-time (matches cooldown) | None (already info-dense) | Static number + filled/unfilled ratio bar | ~0.4ms (radial shader) |
| Buff applied | Icon glow + slide-in from edge | 200ms ease-out | Light tap | Static icon with "+BUFF" text | ~0.2ms (glow) + ~0.1ms (slide) |
| Buff expiring (last 3s) | Icon pulse + transparency fade | 500ms fade-out | Light warning pulse | Static icon with countdown number | ~0.3ms (pulse + fade) |
| Kill confirmed | Kill feed slide-in + score pop | 300ms ease-out-back | Medium celebration | Static kill feed entry (no animation) | ~0.3ms (slide) + ~0.2ms (score pop) |
| Objective updated | Banner slide-down + hold + slide-up | 500ms in, 2s hold, 300ms out | None | Static banner (no animation) | ~0.3ms (slide) |
| Ammo low (<20%) | Ammo counter yellow → red + gentle pulse | Pulse 0.5Hz | None | Static red ammo number | ~0.1ms (color shift) |
| Menu open/close | Scale + fade (from center) | 200ms ease-out (open), 150ms ease-in (close) | Light tap on open | Instant show/hide | ~0.5ms (scale + fade) |

**Frame budget allocation for game UI animations:**
- At 60fps (16.67ms total): UI animation budget = **≤1.5ms** — the rest belongs to rendering (8ms), physics/AI (5ms), network (1ms), margin (1.17ms)
- At 30fps (33.33ms total): UI animation budget = **≤3ms**
- **Enforce in engine**: profile UI layer separately. If UI > budget, reduce: particle count, animation complexity, or canvas redraw area
- **Diegetic UI warning**: in-world UI animations (holograms, screens, spatial markers) render in the 3D pass — they share the RENDERING budget (8ms), not the UI budget. Diegetic animations are 3-5x more expensive than canvas overlay equivalents.

## Operating at Different Levels
<!-- STANDARD: 3min -->

| Level | User | Scope | What Changes |
|-------|------|-------|-------------|
| **L1 — Apprentice** | Hobbyist making their first game | Single screen HUD | Learn HUD layout principles: health/stamina/ammo placement, minimap positioning, anchor points. Use engine defaults. |
| **L2 — Solo** | Indie dev shipping on one platform | Full game UI (HUD + menus) | Design for one platform's input (controller OR touch OR mouse). Implement subtitle system. Add basic colorblind toggle. |
| **L3 — Small Team** | 2-10, shipping on 2-3 platforms | Cross-platform UI with input switching | Platform-adaptive layouts: controller grid vs touch radial vs mouse cursor. Hot-swappable input detection. Full accessibility suite. |
| **L4 — Medium** | 10-50, AAA or large indie | Multi-mode UI (exploration, combat, crafting, social) | Context-sensitive HUD that shows/hides based on game state. Custom UI engine optimizations. Localization to 12+ languages (text expansion!). |
| **L5 — Enterprise** | AAA studio, live service game | Persistent UI across seasons, expansions, platforms | UI-as-service: downloadable UI updates without game patches. Analytics-driven HUD optimization (heatmaps of where players look). Competitive accessibility certification. |

## Decision Trees
<!-- STANDARD: 3min -->

### Decision Tree 1: UI Diegesis Selection

        ┌── INPUT: What is the player's primary activity?
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
[Immersion]       [Information]       [Mixed]
Exploration,      Strategy,           RPG inventory
narrative,        competitive,        on character,
horror            simulation          menu for crafting
   │                 │                  │
   ▼                 ▼                  ▼
Diegetic UI:      Non-Diegetic:      Hybrid: spatial
in-world HUD,     screen-space       elements in-world
no overlays,      overlays,          + overlay for
character-as-     mini-map,          complex data
indicator         health bars        (Spatial UI)

### Decision Tree 2: Input Method & Platform Targeting

        ┌── INPUT: Target platforms?
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
[Console/PC]      [Mobile/Touch]     [Cross-Platform]
Controller or     Tap and swipe      All platforms
mouse+keyboard    primary            must work
   │                 │                  │
   ▼                 ▼                  ▼
Grid navigation,  Large touch        Hot-swappable
focus management, targets (≥48px),   input detection,
button prompts    radial menus,      adaptive layouts
show controller   swipe gestures     per platform

### Decision Tree 3: HUD Element Prioritization

        ┌── INPUT: What game state is active?
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
[Exploration]     [Combat]           [Safe Zone]
Open world,       Active fighting,   Town, menu,
puzzle solving    boss encounter     inventory
   │                 │                  │
   ▼                 ▼                  ▼
Minimal: compass, Expanded: health,  Full: all stats,
objective text,   abilities bar,     gear compare,
interaction       cooldowns, target  crafting grid,
prompt only       health, ammo       quest tracker

## Core Workflow
<!-- STANDARD: 3min -->

### Phase 1: Define the UI Paradigm (10 min)

1. **Identify the game genre** — FPS, RPG, RTS, fighting, racing, puzzle, platformer, sports, simulation
2. **Choose UI approach per game state:**
   - **Exploration/World**: Minimal HUD — health, compass, interaction prompt
   - **Combat**: Expanded HUD — health, abilities, cooldowns, target info, damage numbers
   - **Menu/Pause**: Full UI — settings, inventory, map, quests, crafting, character
   - **Cinematic**: No UI — or subtitle-only
3. **Decide diegesis:** Diegetic (immersion-first) vs Non-diegetic (clarity-first) vs Hybrid

### Phase 2: HUD Layout Design (15 min)

**Anchor zones (1080p reference):**

| Zone | Position | Best For |
|------|----------|----------|
| Top-Left | Safe for all platforms | Health, player name, status effects |
| Top-Center | Watch for platform UI (notch, clock) | Compass, objective text, score |
| Top-Right | Safe for all platforms | Minimap, ammo, currency |
| Bottom-Left | May overlap virtual controls on mobile | Chat, event log, quest tracker |
| Bottom-Center | Never overlap on mobile (home indicator) | Crosshair (center), ability bar |
| Bottom-Right | Safe for most platforms | Ammo, equipment, quick slots |

**Safe zone:** Keep critical UI within 90% of screen (5% margin on all sides) for TV overscan and platform chrome.

**HUD element hierarchy by priority:**
1. Health/player state (always visible, top-left or bottom-center)
2. Crosshair/aiming reticle (center, always visible in gameplay)
3. Ammo/resources (top-right or bottom-right)
4. Minimap/compass (top-right or corner)
5. Abilities/cooldowns (bottom-center or bottom-right)
6. Objectives/quests (top-right or side panel, hideable)
7. Chat/social (bottom-left, hideable)

### Phase 3: Menu System Design (10 min)

**Menu hierarchy depth rule:** No menu path deeper than 4 levels from gameplay.

```
Gameplay
├── Pause Menu (1 press)
│   ├── Resume (1 press)
│   ├── Settings (2 presses)
│   │   ├── Graphics (3 presses)
│   │   ├── Audio (3 presses)
│   │   ├── Controls (3 presses) → Rebind (4 presses)
│   │   └── Accessibility (3 presses)
│   ├── Save/Load (2 presses)
│   └── Quit to Main Menu (2 presses + confirm)
└── Inventory (1 press if quick-access)
    ├── Item Detail (2 presses)
    ├── Equip/Use (3 presses)
    └── Craft (3 presses)
```

### Phase 4: Input & Navigation (10 min)

**Controller navigation patterns:**
- **Grid layout**: D-pad moves in 2D grid. Bumper tabs for sections. Best for inventories, settings.
- **List layout**: D-pad up/down navigates. Left/right changes value. Best for settings, dialogue.
- **Radial menu**: Right stick selects direction. Release to confirm. Best for quick actions, weapon wheels.
- **Focus wrapping**: When on last item, next input wraps to first. Essential for fast navigation.

**Input glyph system:**
- Show platform-specific button icons (Xbox A vs PS ✕ vs Switch B vs keyboard E)
- Detect controller type at runtime; never show wrong glyphs
- Color-code by platform: Xbox green A, PS pink ✕, Switch red B

### Phase 5: Performance Budget (5 min)

**UI render budget (per frame):**
- **60fps target**: UI must complete within 2-3ms (of 16.67ms frame budget)
- **Canvas rebuilds**: Dirty-rect only. Never redraw entire HUD when only ammo changed.
- **Text mesh generation**: Cache. Do not regenerate text every frame.
- **Atlas packing**: All UI textures in one atlas. One draw call for entire HUD.
- **Resolution-independent**: Use Distance Field fonts or SDF-based rendering for sharp text at any scale.

## HUD Patterns by Genre
<!-- STANDARD: 3min -->

| Genre | Key HUD Elements | Special Considerations |
|-------|-----------------|----------------------|
| **FPS** | Crosshair, health, ammo, minimap, kill feed | Peripheral clarity critical. Ammo must be readable without looking away from crosshair. |
| **RPG** | Health/mana bars, ability hotbar, quest tracker, minimap, party frames | Information-dense. Collapsible panels. Ability cooldowns must be obvious peripherally. |
| **RTS** | Minimap (dominant), selection panel, command card, resource counters, unit groups | Information overload is the biggest risk. Floating health bars on units. Minimap is the most-used element. |
| **Fighting** | Health bars (both players), timer, combo counter, super meter | Symmetric layout. Large, centered health bars. Timer always visible. Minimal HUD — let the fight be the focus. |
| **Racing** | Speedometer, position, lap counter, minimap/track outline, RPM gauge | Speed must update smoothly (interpolated, not polling). Rear-view mirror or proximity arrows. Minimal HUD — immersion-first. |
| **Platformer** | Lives, coins/collectibles, timer, level progress | Simple HUD. Lives iconography (not text). Timer only if relevant. World-map progress between levels. |
| **Sports** | Score, timer/clock, player names, stamina, minimap | Broadcast-style presentation. Scoreboard takes visual priority. Player indicators must be distinguishable at distance. |
| **Puzzle** | Move counter, hint button, level number, objective | Minimal HUD. Puzzle is the interface. HUD exists only for meta-progress. |
| **Simulation** | Needs bars, notifications, speed controls, resource counters | Management UI resembles productivity software. Panels, tabs, tooltips. Keyboard shortcuts for power users. |
| **Battle Royale** | Health/shield, minimap, kill feed, player count, safe zone timer, inventory | Information-dense but must not obscure combat. Inventory quick-swap. Map ping system. Death recap. |

## Game Accessibility
<!-- STANDARD: 3min -->

### Subtitles & Captions
- **Speaker labels**: Color-coded or named. Critical for off-screen dialogue.
- **Background**: Semi-transparent black bar behind text, not just text stroke.
- **Size options**: Small / Medium / Large (minimum 46 characters per line at medium).
- **Direction indicators**: Arrow or radar for off-screen sound sources.
- **Timing**: Appear 100ms before audio, disappear 200ms after.

### Colorblind Support
Test with all three types: **Protanopia** (red-blind), **Deuteranopia** (green-blind), **Tritanopia** (blue-blind).
- Never convey information by color alone — add icon, pattern, or text.
- Enemy/ally distinction: shapes or icons, not just red vs green.
- Rarity colors: always show text label ("Rare," "Legendary") alongside color.

### Remappable Controls
- Every action must be rebindable.
- Show conflict resolution: "This key is already bound to Jump. Replace?"
- Provide presets: Default, Southpaw, Accessibility, Custom.
- Allow multiple inputs for one action (primary + secondary binding).

### Motor Accessibility
- Toggle vs hold options for aim, crouch, sprint.
- Auto-aim strength slider.
- Button-hold duration settings (long press vs short press).
- Single-stick mode (move + aim on one stick).
- Controller vibration: on/off + intensity slider.

### Cognitive Accessibility
- Tutorial prompts that stay until dismissed (not timed).
- Objective reminders on screen.
- No time-pressure mechanics without toggleable extended timers.
- Simple mode: reduced HUD, fewer mechanics, clearer objectives.

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

| Upstream Skill | What We Need | When |
|---------------|-------------|------|
| `ui-ux-designer` | Design system tokens, component interaction states, color theory | Before designing menus — game menus still follow UI fundamentals |
| `accessibility-auditor` | WCAG 2.2 baseline, assistive tech test patterns | Before shipping — adapt WCAG patterns to game-specific accessibility |

| Downstream Skill | What We Provide | When |
|-----------------|----------------|------|
| `game-developer` | HUD layout specs, menu wireframes, input navigation maps, accessibility requirements | After design complete — developer implements in engine |
| `frontend-developer` | Web game UI patterns, canvas-based HUD specs | For browser-based games |
| `mobile-developer` | Touch-native game UI patterns, gesture-designed controls | For mobile games |

## Proactive Triggers
<!-- STANDARD: 3min -->

| Trigger | Action | Why |
|---------|--------|-----|
| "I need a HUD" without specifying platform or input method | Ask: "What platform? Controller, touch, or mouse? What resolution do you target?" | UI layout is fundamentally different for each input modality |
| Spec mentions only one colorblind type | Flag: "You've addressed deuteranopia but not protanopia or tritanopia. Test all three." | 8% of males have some form of colorblindness |
| Menu depth exceeds 4 levels from gameplay | Flag: "This menu requires 5+ button presses to return to gameplay. Restructure to ≤4 depth." | Players abandon games with frustrating menus |
| UI text under 24px for critical gameplay info | Flag: "Text at this size is unreadable at TV viewing distance. Bump to 24px minimum." | Console/PC players sit 6-10 feet from display |
| No subtitle system in dialogue-heavy game | Flag: "Add subtitles with speaker labels. 20% of players enable subtitles even without hearing impairment." | Subtitles benefit all players in noisy environments |

## What Good Looks Like
<!-- STANDARD: 3min -->

> The HUD is invisible — players absorb information without conscious effort. Health is top-left, ammo bottom-right, minimap top-right. All critical info is readable peripherally at 1080p from 8 feet. The pause menu returns to gameplay in ≤2 button presses. Controller navigation has a visible focus indicator that smoothly animates between elements. Subtitles appear with speaker labels and directional indicators. Three colorblind modes are tested and verified. Every action is remappable with conflict resolution. The HUD renders in under 3ms at 60fps, even with dynamic damage numbers and status effects.

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| HUD cropped on some TVs | Fixed pixel layout without safe zone | Add 5% margin on all sides. Use engine's safe zone API. Test on CRT and modern TVs. |
| Controller loses focus in nested menu | Focus manager doesn't remember parent state | Implement focus stack: push on enter, pop on back. Always return to last-focused element in parent. |
| Text unreadable at 4K | Bitmap font at fixed size, not SDF | Switch to SDF (Signed Distance Field) fonts or Distance Field text rendering. |
| Colorblind mode doesn't help | Only hue-shifted colors, no shape/pattern differentiation | Add icon variations, patterns, or text labels alongside color changes. Test with actual colorblind simulation tools. |

## Best Practices

1. **Do budget every HUD animation in milliseconds per frame** — Game UI competes with rendering, physics, and AI for the frame budget. At 60fps, the total frame is 16.67ms. UI animations must consume ≤ 1ms per frame. A 3ms health-bar pulse at 60fps steals 18% of the render budget, causing frame drops when combined with particle effects or physics calculations. Use a GPU profiler (RenderDoc, Xcode Metal Debugger) to measure UI draw time per frame, not estimated budget.
2. **Prefer diegetic UI for immersion-critical moments and non-diegetic overlay for combat clarity** — In-world holograms and screens immerse players but cost draw calls and overdraw. A canvas overlay HUD is cheaper (1 draw call for the entire UI atlas) but breaks immersion. Rule of thumb: exploration/ambient = diegetic; combat/critical-state = non-diegetic hybrid. Never mix without intent — a diegetic health bar in a fantasy RPG that switches to a floating green bar in combat feels broken.
3. **Always test HUD readability with a 5-second glance test** — Show a player a frozen frame of gameplay for 5 seconds, then ask: "What was your health? Ammo? Objective?" If they cannot answer all three correctly, the HUD hierarchy is wrong. The fidelity trap — making HUD too visually complex because "it looks cool" — is the #1 cause of unreadable game UI. A beautiful HUD the player can't read in combat costs $50,000+ in negative reviews citing "cluttered interface."
4. **Never ship a game without subtitles, colorblind modes (deuteranopia, protanopia, tritanopia), and fully remappable controls** — Games ship to millions of players. 15% of the global population has some form of disability. Shipping without these three accessibility features excludes ~200 million potential players and triggers $100,000-$500,000 in post-launch accessibility remediation plus negative press. CVAA compliance for US-market games requires accessible communication features by law.
5. **Measure menu return-to-gameplay press count** — From any menu node, how many button presses to return to gameplay? Target: ≤ 3 presses from any depth. A settings menu buried 5 levels deep that requires 8 presses to exit means players avoid adjusting settings mid-combat — leading to avoidable deaths and frustration. Test: navigate to deepest menu node, count presses to resume; if > 3, add a "Resume" shortcut on long-press or a dedicated controller button.

## Production Checklist

Before deploying or delivering work from this skill, verify:

| # | Check | Verify |
|---|-------|--------|
| ☐ | HUD layout uses anchor points and safe zones — scales from 720p to 4K without clipping or drift | Test at 720p, 1080p, and 4K resolutions; no HUD element clips, drifts, or becomes unreadable at any resolution |
| ☐ | Every controller-navigable menu has a visible focus indicator that animates smoothly between elements without disappearing | Navigate every menu with D-pad/gamepad; focus indicator must always be visible at every navigation step |
| ☐ | All critical gameplay text (health, ammo, timer, crosshair) is ≥ 24px equivalent at 1080p reference resolution | Measure text at 1080p with layout debugger; any critical metric below 24px triggers Ground Rule G3 |
| ☐ | Every menu returns to gameplay in ≤ 3 button presses from any depth | Count presses from deepest menu node to gameplay; if > 3, add direct resume shortcut or flatten hierarchy |
| ☐ | Subtitles include speaker labels, differentiate ambient vs. dialogue sound, and are legible at 720p and 4K | Verify subtitles with correct speaker attribution at both extremes; background contrast ensures readability over all environment lighting |
| ☐ | Colorblind modes cover deuteranopia, protanopia, and tritanopia with shape/pattern/icon differentiation beyond hue-only changes | Run each mode through a colorblind simulator; critical HUD elements must remain distinguishable without relying solely on color |
| ☐ | HUD render budget ≤ 2ms per frame at target FPS — verified via GPU profiler with all systems active | Profile with RenderDoc/Xcode/PerfDog: UI draw time per frame measured, not estimated; any frame where UI > 2ms must be investigated |
| ☐ | Rollback plan is documented and tested | Verify: can revert to previous HUD/menu build without save-data corruption; accessibility settings persist across rollback; PC/console certification submission checklist includes rollback test results |

## Verification
<!-- STANDARD: 3min -->

| # | Complete when... | Verify |
|---|---|---|
| ☐ | Complete when HUD layout uses anchor points and safe zones rather than fixed-pixel positioning, scaling correctly from 720p to 4K | Verify by testing at 720p, 1080p, and 4K resolutions; no HUD element clips, drifts, or becomes unreadable at any resolution |
| ☐ | Complete when every controller-navigable menu has a visible focus indicator that animates between elements with explicit transition timing | Verify by navigating every menu with D-pad/gamepad; focus indicator must always be visible and move smoothly between elements without disappearing |
| ☐ | Complete when all critical gameplay text (health, ammo, timer, crosshair labels) is ≥ 24px equivalent at 1080p reference resolution | Verify by measuring text at 1080p; any critical metric below 24px equivalent triggers Ground Rule G3 violation |
| ☐ | Complete when every menu allows return to gameplay in ≤ 3 button presses from any depth (pause → resume path) | Verify by counting presses from deepest menu node to gameplay; if > 3, add direct resume shortcut or flatten menu hierarchy |
| ☐ | Complete when subtitles include speaker labels, differentiate ambient vs. dialogue sound, and are tested at 720p and 4K for legibility | Verify subtitles render with correct speaker attribution at min/max resolution; background contrast ensures readability over all game environments |
| ☐ | Complete when colorblind modes cover at minimum deuteranopia, protanopia, and tritanopia with shape/pattern/icon differentiation beyond hue-only changes | Verify by running each mode through a colorblind simulator; critical HUD elements must remain distinguishable without relying solely on color |
| ☐ | Complete when all controls are fully remappable with per-platform defaults documented and conflict detection for overlapping bindings | Verify remapping UI allows any action to be rebound; attempt to bind two actions to same input → conflict warning appears |
| ☐ | Complete when every HUD animation specifies: duration (ms), easing curve, haptic pairing per platform SDK, and `prefers-reduced-motion` fallback | Verify animation spec document has all four fields for each animation; missing any field triggers Ground Rule G7 violation |
| ☐ | Complete when damage/flash animations never exceed 3 flashes per second (seizure safety threshold per WCAG 2.3.1) | Verify by counting flash frames in any damage or alert animation sequence; if > 3 flashes per second, reduce frequency or add dimming |
| ☐ | Complete when diegetic UI elements (in-world screens, holograms) render within the 3D scene budget without exceeding the per-frame UI animation allocation of ≤ 1ms | Verify via profiler that diegetic UI rendering + animation costs stay under 1ms/frame at target FPS on minimum-spec hardware |

## When to Use
<!-- STANDARD: 3min -->

| Condition | Use This Skill | Use Instead |
|-----------|---------------|-------------|
| Designing HUD layouts (health bars, minimaps, ammo counters) | ✅ Apply safe zones, anchor points, resolution-independent layout | — |
| Building menu systems (main menu, pause, settings, inventory) | ✅ Controller-first navigation, focus indicators, ≤3 presses to gameplay | — |
| Designing diegetic UI (in-world screens, holograms, spatial displays) | ✅ World-space positioning, 3D render budget integration | — |
| Implementing accessibility for games (subtitles, colorblind, remappable controls) | ✅ 3 colorblind modes, speaker-labeled subtitles, full control remapping | — |
| General game design (mechanics, systems, narrative) | ❌ | `game-developer` |
| Non-game application UI design | ❌ | `ui-ux-designer` |
| Controller input mapping for console games | ✅ D-pad navigation, focus stacks, platform-specific button prompts | — |
| Cross-platform game UI (console, PC, mobile) | ✅ Resolution scaling from 720p to 4K, input switching | — |
| Game telemetry that captures PII without consent | ❌ Route to `security-reviewer` | — |
| Choosing a game engine | ❌ | `game-developer` or game engine documentation |

## Deliberate Practice
<!-- STANDARD: 3min -->

1. **Audit a AAA game's HUD.** Launch your favorite game. Screenshot the HUD during combat, exploration, and menus. Map every element: position, size in pixels, color choice, animation timing. How many elements are visible at once? Which ones are diegetic vs non-diegetic? What would you change for accessibility?
2. **Design the same menu for 3 input methods.** Create a settings menu mockup that works with (a) controller/D-pad with focus indicator, (b) mouse with hover states, (c) touch with tap targets ≥44pt. How does the layout change per input? Where does the focus indicator start?
3. **Build an accessible subtitle system.** Design subtitles for a dialogue-heavy cutscene. Include: speaker labels with colors, directional indicators for off-screen speakers, differentiation between dialogue and ambient sound, and three font size options. Test legibility at 720p on a TV 8 feet away.
4. **Optimize a HUD for frame budget.** Given a HUD with health bar, ammo counter, minimap, 3 status effects, and damage numbers, calculate the render cost at 60fps. Which elements can be batched? Which need real-time updates vs polling? Target ≤1ms per frame for all UI rendering.
5. **Design colorblind-safe critical indicators.** Take a combat HUD where low health is shown by a red flash. Redesign so the alert works for deuteranopia, protanopia, and tritanopia using: shape change (pulsing border), icon overlay, audio cue, and haptic feedback.

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| HUD designed at fixed 1920×1080 resolution without safe zones — UI cropped or unreadable on 720p handhelds and 4K TVs | $50K-$200K in post-launch rework when console certification fails due to safe zone violations; $100K-$500K in refunds from users who can't read critical HUD elements | Use anchor points + safe zones (5% margin). Test at 720p, 1080p, and 4K. No element clips or becomes <24px at any resolution |
| Controller navigation without visible focus indicator — player doesn't know what's selected | $30K-$100K in UX rework; negative reviews citing "broken menu navigation" | Visible focus indicator on every navigable element. Animated transition between elements. Focus stack remembers last position when returning from sub-menu |
| No colorblind modes shipped — 8% of male players cannot distinguish critical gameplay information | $50K-$250K in accessibility complaints and potential CVAA regulatory action; lost sales from accessibility-conscious market ($50B+ spending power) | Minimum 3 colorblind modes (deuteranopia, protanopia, tritanopia). Shape/pattern/icon differentiation beyond hue-only changes. Test with colorblind simulation tools |
| Critical gameplay text below 24px equivalent — unreadable at TV viewing distance (6-10 feet) | $20K-$80K in post-launch patch costs; refund requests from TV players who can't read ammo/health | Minimum 24px equivalent at 1080p reference resolution. Test at 8-foot viewing distance on a 42" TV. Use SDF (Signed Distance Field) fonts for crisp scaling |
| Menu requires 5+ button presses to return to gameplay — players abandon game in frustration | $100K-$500K in lost player retention; 40% of players who get lost in menus never return | Maximum 3 presses to gameplay from any menu depth. Add "Resume" as first option in pause menu. Flatten menu hierarchies |
| HUD animations exceeding frame budget — UI rendering causes frame drops below 60fps | $50K-$200K in optimization rework; negative reviews citing "laggy" game feel; certification failure on performance-sensitive platforms | UI animation budget ≤1ms per frame. Batch draw calls. Use atlasing for HUD textures. Profile on minimum-spec target hardware |
| Subtitle system missing speaker labels and directional cues — deaf/hard-of-hearing players lose narrative context | $30K-$100K in accessibility compliance fixes; potential legal exposure under CVAA game accessibility requirements | Speaker labels with consistent colors. Directional indicators for off-screen speakers. Differentiate dialogue vs ambient sound. Test with subtitle-only playthrough |
| No remappable controls — players with motor impairments or non-standard controllers cannot play | $20K-$80K in accessibility complaints; platform store rejection on accessibility grounds | Full control remapping UI. Per-platform default presets. Conflict detection for overlapping bindings. Save/load custom control schemes |

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Decision | Status | Timestamp |
|----------|--------|-----------|
| (none yet) | — | — |

## References
<!-- STANDARD: 3min -->

- [Game Accessibility Guidelines](https://gameaccessibilityguidelines.com/) — Comprehensive game accessibility standards
- [WCAG 2.3.1 Seizure Threshold](https://www.w3.org/TR/WCAG22/#three-flashes-or-below-threshold) — No more than 3 flashes per second
- `references/hud-design-patterns.md` — Health bars, minimaps, ammo counters, quest trackers
- `references/menu-system-design.md` — Pause menus, settings, inventory, save/load patterns
- `references/diegetic-ui-patterns.md` — In-world screens, holograms, spatial UI in 3D
- `references/controller-navigation.md` — D-pad focus, focus stacks, platform button prompts
- `references/game-accessibility.md` — Subtitles, colorblind modes, remappable controls, motor accessibility
- `references/unreal-umg-patterns.md` — Unreal Engine UMG widget patterns
- `references/godot-ui-patterns.md` — Godot Control node patterns
- `references/cross-platform-scaling.md` — Resolution independence, safe zones, DPI scaling

## Anti-Hallucination
<!-- STANDARD: 3min -->

- Admit uncertainty. If you cannot determine the correct approach, ask — do not guess.
- Flag your knowledge cutoff. If this project uses tools or patterns you have not seen, state your assumptions.
- Never guess security. If work touches auth, payments, or PII, route to security-reviewer.
- [VERIFIED] — Industry-standard game UI pattern (used in multiple shipped AAA titles)
- [COMMON-PRACTICE] — Widely used in indie and AA games
- [INFERRED] — Reasonable extrapolation from game UI principles
- [UNKNOWN] — Requires verification against specific engine or platform capabilities
