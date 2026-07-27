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

## Route the Request

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

## Ground Rules

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

| Level | User | Scope | What Changes |
|-------|------|-------|-------------|
| **L1 — Apprentice** | Hobbyist making their first game | Single screen HUD | Learn HUD layout principles: health/stamina/ammo placement, minimap positioning, anchor points. Use engine defaults. |
| **L2 — Solo** | Indie dev shipping on one platform | Full game UI (HUD + menus) | Design for one platform's input (controller OR touch OR mouse). Implement subtitle system. Add basic colorblind toggle. |
| **L3 — Small Team** | 2-10, shipping on 2-3 platforms | Cross-platform UI with input switching | Platform-adaptive layouts: controller grid vs touch radial vs mouse cursor. Hot-swappable input detection. Full accessibility suite. |
| **L4 — Medium** | 10-50, AAA or large indie | Multi-mode UI (exploration, combat, crafting, social) | Context-sensitive HUD that shows/hides based on game state. Custom UI engine optimizations. Localization to 12+ languages (text expansion!). |
| **L5 — Enterprise** | AAA studio, live service game | Persistent UI across seasons, expansions, platforms | UI-as-service: downloadable UI updates without game patches. Analytics-driven HUD optimization (heatmaps of where players look). Competitive accessibility certification. |

## Core Workflow

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

| Trigger | Action | Why |
|---------|--------|-----|
| "I need a HUD" without specifying platform or input method | Ask: "What platform? Controller, touch, or mouse? What resolution do you target?" | UI layout is fundamentally different for each input modality |
| Spec mentions only one colorblind type | Flag: "You've addressed deuteranopia but not protanopia or tritanopia. Test all three." | 8% of males have some form of colorblindness |
| Menu depth exceeds 4 levels from gameplay | Flag: "This menu requires 5+ button presses to return to gameplay. Restructure to ≤4 depth." | Players abandon games with frustrating menus |
| UI text under 24px for critical gameplay info | Flag: "Text at this size is unreadable at TV viewing distance. Bump to 24px minimum." | Console/PC players sit 6-10 feet from display |
| No subtitle system in dialogue-heavy game | Flag: "Add subtitles with speaker labels. 20% of players enable subtitles even without hearing impairment." | Subtitles benefit all players in noisy environments |

## What Good Looks Like

> The HUD is invisible — players absorb information without conscious effort. Health is top-left, ammo bottom-right, minimap top-right. All critical info is readable peripherally at 1080p from 8 feet. The pause menu returns to gameplay in ≤2 button presses. Controller navigation has a visible focus indicator that smoothly animates between elements. Subtitles appear with speaker labels and directional indicators. Three colorblind modes are tested and verified. Every action is remappable with conflict resolution. The HUD renders in under 3ms at 60fps, even with dynamic damage numbers and status effects.

## Error Recovery

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| HUD cropped on some TVs | Fixed pixel layout without safe zone | Add 5% margin on all sides. Use engine's safe zone API. Test on CRT and modern TVs. |
| Controller loses focus in nested menu | Focus manager doesn't remember parent state | Implement focus stack: push on enter, pop on back. Always return to last-focused element in parent. |
| Text unreadable at 4K | Bitmap font at fixed size, not SDF | Switch to SDF (Signed Distance Field) fonts or Distance Field text rendering. |
| Colorblind mode doesn't help | Only hue-shifted colors, no shape/pattern differentiation | Add icon variations, patterns, or text labels alongside color changes. Test with actual colorblind simulation tools. |

## Anti-Hallucination

- [VERIFIED] — Industry-standard game UI pattern (used in multiple shipped AAA titles)
- [COMMON-PRACTICE] — Widely used in indie and AA games
- [INFERRED] — Reasonable extrapolation from game UI principles
- [UNKNOWN] — Requires verification against specific engine or platform capabilities
