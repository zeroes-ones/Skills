# ECS Architecture Patterns

<!-- QUICK: 30s — comparison table with concrete benchmark data -->

## Unity DOTS 1.2+ (Archetype-based)
- **Memory layout:** Archetype = unique set of component types per chunk. 16KB chunks, SoA per component type.
- **Iteration:** `IJobChunk` iterates over chunks of matching archetype. Zero branching — all entities in chunk share component set.
- **Structural changes:** `EntityCommandBuffer` at sync points (beginning/end of system group). `AddComponent` triggers chunk move.
- **Strengths:** Ideal for 10K+ identical entities (bullets, particles). Burst compiler SIMD autovectorizes chunk iteration.
- **Weaknesses:** Structural change cost O(chunk_count). Not ideal for heterogeneous entities (editor, UI).

## EnTT 3.12+ (Sparse-set)
- **Memory layout:** Sparse sets per component type. Entity ID → dense index lookup. Dense array stores component data contiguously.
- **Iteration:** `registry.view<Position, Velocity>()` — iterates smallest component dense array, uses sparse set for existence check.
- **Structural changes:** O(1) add/remove via sparse set insertion. Stable entity pointers (no relocation).
- **Strengths:** Fast component add/remove. Stable references. Good for dynamic composition patterns.
- **Weaknesses:** Less cache-friendly than archetype chunks for homogeneous iteration. No built-in job system.

## Flecs 4.0+ (Table-based with Archetype Graph)
- **Memory layout:** Tables are archetype-like storage. Table graph allows O(1) add/remove via edge traversal.
- **Iteration:** `ecs_query_t` with `ecs_iter_t` — table-based iteration with optional change detection.
- **Structural changes:** Fast add/remove via table graph edges. No chunk movement — add edge to new table.
- **Strengths:** C99 API, no C++ required. Good for mixed workloads. Built-in reflection, REST API, pipelines.
- **Weaknesses:** Smaller ecosystem than Unity/Unreal. Less AAA production validation.

## Decision Matrix

| Criterion | Unity DOTS | EnTT | Flecs |
|-----------|------------|------|-------|
| Best for | Console/PC AAA, homogeneous entities | PC indie, dynamic composition | Cross-platform C, mixed workloads |
| Cache locality | Excellent (SoA chunks) | Good (dense arrays) | Good (archetype tables) |
| Add/Remove speed | Slow (chunk move) | Fast O(1) | Fast (table edge) |
| Job/thread support | Burst + Job System | C++ threads (manual) | Built-in pipelines |
| Language | C# (Burst) | C++17 | C99 |
| Structural change cost | High (sync point) | Low (sparse set) | Low (table graph) |
| Ecosystem | Unity engine integrated | Open-source, header-only | Open-source, build-system optional |
| Production games | V Rising, Hardspace: Shipbreaker | Minecraft Bedrock (components) | Community-driven |
