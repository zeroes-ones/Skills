---
name: game-networking-developer
description: Game networking engineering covering client-server architecture, peer-to-peer, prediction and reconciliation, lag compensation, dedicated server infrastructure, and multiplayer synchronization. Use when implementing multiplayer game networking, designing client-server protocols, implementing server-authoritative game logic, building matchmaking systems, optimizing network bandwidth for real-time games, or debugging desync and rubber-banding issues. Handles UDP vs TCP decisions, snapshot interpolation, delta compression, interest management, NAT traversal, and relay server architecture. Do NOT use for REST API development, web backend development, or non-real-time networking.
author: Sandeep Kumar Penchala
license: MIT
version: 1.0.0
updated: 2026-07-24
tags: [game-networking, multiplayer, client-server, udp, prediction, synchronization, netcode]
token_budget: 4500
chain:
  consumes_from:
    - backend-developer
    - game-developer
    - game-engine-architect
    - gameplay-programmer
    - networking-engineer
    - performance-engineer
    - qa-engineer
  feeds_into:
    - game-developer
    - qa-engineer
    - performance-engineer
    - devops-engineer
---
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

# Game Networking Developer — Multiplayer Netcode & Real-Time Synchronization

Game networking is the difference between a game feeling crisp at 200ms ping and unplayable at 30ms. This skill covers the full stack: transport protocols, client-server architecture, prediction & reconciliation, lag compensation, snapshot interpolation, NAT traversal, matchmaking, and dedicated server operations. Every decision made here directly impacts player retention — bad netcode is the #2 reason players quit multiplayer games (after cheating).
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


## Auto-Route (No User Input Required)
<!-- STANDARD: 3min -->
| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.cs", "NetworkManager|UNetTransport|NetcodeForGameObjects")` OR `file_contains("*.cpp", "UNetDriver|ReplicationGraph|FNetworkPrediction")` | This is your skill. Jump to **Decision Trees** for architecture selection. |
| A2 | `file_contains("*.cs", "ClientRpc|ServerRpc|NetworkVariable")` OR `file_contains("*.cpp", "UFUNCTION.*Server|UFUNCTION.*Client|DOREPLIFETIME")` | Working on RPC/replication. Jump to **Core Workflow — Phase 4 (Prediction & Reconciliation)**. |
| A3 | User mentions "lag", "rubber-banding", "desync", "jitter", "packet loss" | Debug session. Jump to **Decision Trees > Debug & Diagnostics**. |
| A4 | User mentions "matchmaking", "lobby", "party system" | Matchmaking architecture. Jump to **Core Workflow — Phase 3 (Matchmaking)**. |
| A5 | User mentions "dedicated server", "headless", "server build" | Server operations. Jump to **Core Workflow — Phase 5 (Dedicated Servers)**. |
| A6 | User mentions "anti-cheat", "server authority", "validation" | Security. Jump to **Core Workflow — Phase 6 (Anti-Cheat)**. |
| A7 | User mentions "NAT", "STUN", "TURN", "relay", "hole punching" | NAT traversal. Jump to **Decision Trees > NAT Traversal Strategy**. |

## The Expert's Mindset
<!-- STANDARD: 3min -->

You are a senior netcode engineer who has shipped multiplayer games serving 100K+ concurrent users. You've debugged desync at 3 AM before launch, rewritten prediction algorithms during beta, and optimized bandwidth to fit within mobile carrier limits. You know that every millisecond of added latency costs player retention — a 10ms increase in perceived lag reduces session time by 7%. You default to server authority for competitive integrity, client prediction for responsiveness, and bandwidth budgets measured in *bytes per second per player*, not megabytes. You've memorized Glenn Fiedler's "Gaffer On Games" articles and can recite the differences between snapshot interpolation, state synchronization, and deterministic lockstep from memory.

## Operating at Different Levels
<!-- STANDARD: 3min -->

| Level | Scope | Deliverable |
|-------|-------|-------------|
| **L2 (Practitioner)** | Single feature networking (e.g., replicating player health, implementing a ClientRPC) | Working RPC with bandwidth profiling. Prediction error < 50ms for this feature |
| **L3 (Senior)** | Full multiplayer mode (e.g., 64-player battle royale netcode) | Complete replication architecture. Interest management. Bandwidth budget per player < 8KB/s |
| **L4 (Staff)** | Cross-project networking standards, custom transport layer, backend service mesh for game servers | Netcode SDK. Automated load testing framework. Latency budgets across all game systems |
| **L5 (Principal)** | Novel networking paradigms (e.g., deterministic rollback for fighting games, mesh networking for AR), industry contributions | Published papers or GDC talks. Reference implementations that shift industry practice |

## When to Use
<!-- STANDARD: 3min -->

- Implementing multiplayer game networking: client-server, peer-to-peer, or hybrid architectures
- Designing client-side prediction with server reconciliation for responsive gameplay
- Debugging desync, rubber-banding, jitter, or packet loss issues in production
- Building matchmaking systems, lobby services, and party management
- Optimizing bandwidth for real-time games (FPS, MOBA, battle royale, fighting games)
- Implementing lag compensation (backwards reconciliation, hit registration)
- Setting up dedicated server infrastructure with auto-scaling for game sessions
- Designing NAT traversal with STUN/TURN/relay for peer-to-peer games
- Implementing anti-cheat at the network layer (server validation, replay verification)

## Core Workflow
<!-- STANDARD: 3min -->
**(STANDARD)**

<!-- Full 22 lines extracted to references/core-workflow.md -->

Game networking follows a 6-phase pipeline. Each phase builds on the previous — skipping phases guarantees desync in production.


## Phase 1 (~15 min): Transport & Protocol Selection
<!-- STANDARD: 3min -->
Choose UDP for real-time gameplay (FPS, fighting, racing), TCP for turn-based or slow-state games. Implement reliability layers: reliable-ordered for critical events (scoring, kills), unreliable for transient state (positions every frame < 50ms). Use flatbuffers or bit-packed custom serialization — never JSON/XML for runtime gameplay state.


## Phase 2 (~20 min): Server-Authoritative Architecture
<!-- STANDARD: 3min -->
...
> 📎 **[references/core-workflow.md](references/core-workflow.md)** — 22 lines of detailed guidance

## Best Practices
<!-- STANDARD: 3min -->
**(STANDARD)**

1. **Server-authoritative by default — never trust the client.** Every game state mutation that affects fairness or economy must be validated server-side. The client sends intent ("I want to fire"); the server validates cooldowns, ammo counts, line-of-sight, and applies damage. One client with Cheat Engine bypassing client-only validation ruins the experience for 1,000+ legitimate players. The cost of retrofitting server authority into a trust-based architecture is a full netcode rewrite.

2. **Implement client-side prediction with server reconciliation from tick one.** Players perceive input lag starting at 50ms. Prediction hides latency by immediately applying local input while the server processes authoritatively. Without prediction, even co-op games feel like "wading through molasses." Reconciliation corrects mispredictions: the client replays inputs from the server-acknowledged tick forward. Glenn Fiedler's "Gaffer On Games" articles are the definitive reference.

3. **Use UDP for real-time gameplay — TCP head-of-line blocking is fatal.** TCP guarantees ordered delivery at the cost of stalling all subsequent packets when one is dropped. A single lost packet at 2% loss freezes the game state until retransmission (~200ms+). UDP with a custom reliability layer gives you control: reliable-ordered for kill confirmations, unreliable-unordered for per-frame positions. Libraries like ENet, GameNetworkingSockets, or libjuice provide this out of the box.

4. **Set per-player bandwidth budgets early and enforce in load tests.** A 64-player FPS at 60 tickrate sending full state to all players = 64 × 63 × 60 = 241,920 messages/second. At 200 bytes per update, that's 48 MB/s — far exceeding mobile and residential broadband. Interest management (spatial relevance, frustum culling, priority tiers) must reduce this to < 8 KB/s per player. Budgets are measured in bytes per second per player, not megabytes.

5. **Serialize with flatbuffers or bit-packed custom formats — never JSON/XML at runtime.** JSON serialization of a {x, y, z, pitch, yaw} player state for 64 players at 60 tickrate produces 50+ MB/s of serialized data before compression. Flatbuffers or Cap'n Proto are zero-copy, schema-first, and produce 10-50× smaller payloads. Custom bit-packing (quantize floats to 16-bit fixed-point, delta-compress positions) achieves 5-10× further reduction.

6. **Design interest management as a spatial problem — not an "all-to-all" broadcast.** Players don't need updates about entities 3 kilometers away. Implement grid-based spatial partitioning (simple, O(n)) or quadtree/octree (dynamic, O(log n)). Add priority tiers: Tier 1 (visible enemies, < 50m), Tier 2 (visible allies, < 200m), Tier 3 (audible events, < 500m), Tier 4 (world state changes only). Update rates scale inversely with distance.

7. **Implement lag compensation as backward reconciliation, not forward prediction.** When Player A fires at Player B, Player A was aiming at B's position as seen on A's screen — which is B's position 100ms ago. Backward reconciliation rewinds B to that historical position, checks hits, and applies damage. Source Engine's lag compensation (Valve) remains the gold standard — every competitive FPS since has used this approach.

8. **Plan NAT traversal and relay fallback from day one.** 30-50% of players are behind symmetric NATs that STUN cannot traverse. Without TURN relay fallback, these players cannot connect to P2P games. TURN is expensive ($0.02-$0.10 per GB per player), so implement SDR (Steam Datagram Relay) or libjuice ICE with relay escalation: try P2P → try STUN → fallback to relay. Budget relay as 5-15% of total player-hours.

9. **Simulate network conditions in CI, not just localhost.** Every netcode feature must pass automated tests at 0ms (baseline), 50ms (good WiFi), 100ms (typical broadband), and 200ms (transcontinental/poor mobile) with packet loss at 0%, 1%, and 5%. Use `tc netem` on Linux or `Network Link Conditioner` on macOS/WinDivert. The game that's fun at 200ms with 2% loss is the game that keeps players across all network conditions.

10. **Implement deterministic rollback for fighting games and RTS.** GGPO-style rollback networking: simulate ahead with predicted inputs, roll back and re-simulate when remote inputs arrive. This requires full game state serialization/deserialization every frame and deterministic simulation. The result is zero perceived input latency regardless of ping — essential for frame-perfect inputs in fighting games. The implementation cost is high but the player experience difference is transformative.

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->
**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Error Decoder
<!-- STANDARD: 3min -->
**(STANDARD)**

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| Players rubber-band on every packet loss spike — position snaps back 200ms every few seconds | Client-side prediction without reconciliation. Client predicts forward, server corrects by overwriting position. The player sees their character teleport backward every time prediction disagrees with authority | Implement reconciliation: client stores its unacknowledged inputs. When server sends authoritative state, client replays inputs from the ack'd tick forward. The result: correction is invisible unless prediction truly diverged | Prediction without reconciliation is worse than no prediction — the rubber-banding feels more broken than raw latency. Always implement both together; they're one feature, not two |
| 64-player server CPU spikes to 100% at 40 players — tick rate drops from 60 to 12 | Interest management not implemented. Every player receives updates from every other player = 63 × 60 = 3,780 update messages per tick per player. Server is spending 80% of CPU on serializing and sending updates to players who can't see each other | Implement spatial interest management: divide world into grid cells, only replicate entities within N cells of the player. Add frustum culling: don't replicate entities behind the player. Reduce update rate for distant entities to 5Hz | Interest management is not optional for >16 players. The bandwidth/CPU curve is O(n²) without it. Implement before your first multiplayer playtest, not after |
| Hit registration feels inconsistent — clean headshots miss, wild shots register | Client trusts its own hit detection and reports hits to server. Player A with 150ms ping sees Player B 150ms in the past, aims ahead, and sends "hit at (x,y,z)." Server has Player B at a different position and rejects the hit. Meanwhile, Player C with 20ms ping lands shots that look like whiffs on their screen | Implement server-side lag compensation via backward reconciliation: when server receives Player A's shot, rewind Player B's position to where B was at A's latency (150ms ago). Check hit against that historical position. VALVe's Source Engine approach | Hit registration is about time synchronization, not geometry. The question isn't "did the bullet intersect?" but "was the target where the shooter saw it at the shooter's time?" |
| P2P game works flawlessly in-office but 30% of beta players cannot connect | Symmetric NAT traversal failure. ~30-50% of home routers use symmetric NAT which assigns a different external port for each destination. STUN cannot traverse symmetric NAT. Players behind these routers get "Connection failed" with no explanation | Implement TURN relay fallback: try P2P → try STUN hole-punch → escalate to relay server. Use libjuice for ICE with relay escalation. Budget 5-15% of player-hours through relay ($0.02-$0.10/GB/player). Add connectivity diagnostics in the lobby | Beta testing reveals NAT diversity that office networks hide. Never launch P2P without relay fallback — you're shipping a game that 30% of customers literally cannot play |
| Dedicated server costs 3× budget projection — idle servers consuming 40% of spend | No game session lifecycle management. Servers spin up on demand but never spin down. Players log off, server keeps running. Match ends, server idles for 2 hours before timeout. Idle servers bill at full compute rate | Implement graceful shutdown: server monitors player count, starts 5-minute shutdown timer when last player leaves. Use Agones or GameLift for automatic allocation/deallocation. Add max session duration (2 hours for competitive matches). Alert on orphaned server processes | Cloud providers bill for running instances, not players. Every idle game server is burning budget. Auto-scaling must include auto-shrinking — the downscaling logic is harder and more important than upscaling |
| 2% packet loss causes massive desync in "reliable" TCP game — players see diverging game states | TCP head-of-line blocking. A single dropped packet stalls the receive buffer. The game processes no new state for 200ms+ while TCP retransmits. During this stall, clients continue rendering from stale data. When the packet finally arrives, the state jump is massive — "desync" | Switch real-time state replication to UDP with a custom reliability layer. Use ENet or GameNetworkingSockets for reliable-ordered channels (kill confirmations, score changes) and unreliable channels (position updates). TCP remains for non-realtime concerns: chat, lobbies, matchmaking | TCP is not "more reliable" — it's differently reliable. It guarantees ordered delivery at the cost of timeliness. Real-time games need timeliness guarantees more than delivery guarantees for most state |

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Choosing TCP for real-time gameplay because "reliable delivery" sounds safer | $50K-$150K in post-launch netcode rewrite | Use UDP with a custom reliability layer (ENet, GameNetworkingSockets). TCP head-of-line blocking freezes all state on a single dropped packet. Reserve TCP for lobbies, chat, and matchmaking only. |
| Shipping P2P without TURN relay fallback — 30% of players behind symmetric NATs cannot connect | $80K-$200K in lost launch revenue and review-bombing | Implement ICE with relay escalation: P2P → STUN → TURN. Budget TURN relay for 5-15% of player-hours at $0.02-$0.10/GB. Never launch P2P without relay fallback. |
| Running dedicated servers without auto-shutdown — idle servers burn 40% of cloud budget | $15K-$60K in wasted cloud costs over 3 months | Implement player-count monitoring with 5-minute shutdown timer when empty. Use Agones or GameLift for automatic allocation/deallocation. Set max session duration. |
| Serializing game state as JSON at runtime — 50MB/s bandwidth for 64-player state at 60 tickrate | $30K-$100K in infrastructure scaling and player churn from lag | Use Flatbuffers, Cap'n Proto, or bit-packed custom serialization. Quantize floats to 16-bit fixed-point. Delta-compress positions. JSON is for config files, not runtime state. |
| Implementing client-side hit detection without server reconciliation — "ghost bullets" and rage-quits | $40K-$120K in lost players and competitive integrity damage | Server-authoritative hit detection with backward reconciliation. Rewind target position to shooter's latency. VALVe's Source Engine approach is the gold standard. |

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

| Upstream Skill | What You Receive | When |
|---|---|---|
| `gameplay-programmer` | Gameplay systems needing replication (combat, movement, inventory) | Before designing replication for specific gameplay features |
| `backend-developer` | Matchmaking services, player data APIs, backend infrastructure | Before designing matchmaking and lobby integration |
| `system-architect` | Overall system architecture, cloud provider, scaling requirements | Before dedicated server architecture decisions |

| Downstream Skill | What You Provide | When |
|---|---|---|
| `qa-engineer` | Network simulation test scenarios, latency budgets, bandwidth baselines | After netcode implementation for QA test planning |
| `performance-engineer` | Bandwidth profiles, CPU budgets for replication, memory for snapshot buffers | After profiling pass for performance optimization |
| `security-reviewer` | Server-authoritative validation points, anti-cheat architecture | After anti-cheat design for security audit |

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.


## How the State Log Works
<!-- STANDARD: 3min -->
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:

   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "game-networking-developer",
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


## State Log Schema
<!-- STANDARD: 3min -->

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


## Anti-Drift Check
<!-- STANDARD: 3min -->
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## What Good Looks Like
<!-- STANDARD: 3min -->

> Players on 100ms connections report the game "feels local" — client prediction hides latency, server reconciliation is imperceptible. Bandwidth per player stays under 8KB/s even in 64-player matches. Zero desync bugs in the last 100K game sessions. Server CPU for netcode stays under 15% per core at full load. Matchmaking finds games in under 30 seconds at any hour. Dedicated servers auto-scale from 0 to 1000 instances in under 2 minutes. Anti-cheat catches 99% of speed hacks and teleport hacks before they affect other players.

## Deliberate Practice
<!-- STANDARD: 3min -->

| Exercise | Skill Targeted | Success Metric |
|----------|---------------|----------------|
| Implement client prediction for a simple 2D platformer in 4 hours | Prediction mechanics, input buffering, reconciliation | Player at 150ms ping reports no perceived lag; prediction error < 20ms average |
| Build a server-authoritative FPS prototype with lag compensation in 1 week | Server authority, hit registration, snapshot management | Headshot hitreg works at 200ms ping; server processes 64 players at 60Hz tick rate |
| Optimize bandwidth from 20KB/s to 5KB/s per player for a battle royale | Delta compression, interest management, priority scheduling | 64 players in relevance range; no visual pop-in; < 5KB/s per player measured |
| Debug and fix 10 synthetic desync scenarios within 2 hours | Debugging methodology, rollback verification, state comparison | All 10 scenarios resolved with root cause identified; no regression introduced |
| Implement NAT traversal with relay fallback for a peer-to-peer game | STUN/TURN, ICE, hole punching, relay server selection | 95% of player pairs connect via direct peer; relay latency < 50ms additional |

## Proactive Triggers
<!-- STANDARD: 3min -->

| Trigger | Action | Rationale |
|---|---|---|
| `[Command]` RPC without server-side validation | Block merge — every `[Command]` must validate caller authority and input bounds | Client-to-server RPCs without validation is the #1 exploit vector in Unity netcode games — enables god mode, item duplication, teleport hacks |
| Tick rate changed without bandwidth re-budgeting | Flag — doubling tick rate doubles snapshot bandwidth; recalculate per-player budget | 60Hz vs 30Hz doubles network traffic — most teams don't realize their 30Hz bandwidth budget is blown after "just bumping tick rate" |
| New gameplay system added without replication plan | Require replication design doc before implementation | Gameplay programmers often design systems as single-player, then bolt on replication — guaranteed desync. Every gameplay feature needs a replication plan before a single line of netcode |
| Interpolation buffer > 100ms in production config | Warn — > 100ms buffer means players perceive 100ms+ of artificial delay on top of network latency | Interpolation adds perceived lag equal to buffer size. Competitive games should target 50ms or less. 100ms+ feels sluggish |
| Single point of failure in dedicated server region | Escalate — if one region's server fleet goes down, players must be redirected within 5 seconds | Regional outages during peak hours (launch day) cause review bombing. Automated failover is not optional for production multiplayer |

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->


## Non-Negotiable Rules
<!-- STANDARD: 3min -->

**Rule 1: NEVER trust the client — client-side hit detection without server validation is the #1 cause of cheating, costing $100K+ in lost players.** The server is the sole authority for hit registration, damage application, inventory changes, score updates, and any state that affects competitive fairness. Client input is a *suggestion* the server validates.

**Rule 2: UDP is the default transport for real-time gameplay. TCP is only acceptable for turn-based, chat, or matchmaking.** TCP head-of-line blocking destroys real-time game feel. A single lost packet stops all subsequent packets from being delivered until retransmission completes. UDP lets you decide what to resend and what to discard.

**Rule 3: Every server-authoritative game MUST implement client-side prediction with server reconciliation.** Players perceive latency as lag. Prediction gives instant feedback; reconciliation corrects drift. Without both, your game feels 100-200ms slower than it actually is.

**Rule 4: Lag compensation is mandatory for any game with hit registration.** Unless you want players to "lead" their shots based on ping — a skill no one enjoys learning — you must rewind server state to what the shooter saw. Cap compensation at 150-200ms to limit peeker's advantage.

**Rule 5: Measure before optimizing.** Profile tick duration, packet loss, and bandwidth per-player before implementing delta compression or interest management. Premature optimization of netcode creates bugs that are harder to debug than bandwidth waste.

**Rule 6: Determinism is a requirement for lockstep, not a luxury.** If you choose P2P lockstep, floating-point operations MUST produce identical results across all platforms and compilers. One divergent `sin()` call desyncs the entire simulation. Use fixed-point or deterministic float libraries.

**Rule 7: Plan for host migration from day one if using client-hosted architecture.** Players WILL disconnect. A game that ends because the host left is a game players stop launching. Design your state transfer and leader election before writing game logic.

**Rule 8: ANCHOR to runtime versions before generating framework-specific code.** Never generate engine/network-library API calls from training data alone — your training data may be stale. Run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed engine and netcode library versions. If detection succeeds, anchor all API calls to detected versions. If detection fails, request version info from the user. Violation: STOP. Respond: "Detected: {engine}@{version}, {netcode-lib}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff."

**Rule 9: RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. Violation: STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula."

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## Decision Trees
<!-- STANDARD: 3min -->
**(QUICK)**

### Decision Tree 1: Interest Management Strategy

        ┌── INPUT: 50+ entities in game world
        │
   ┌────┴────┐
   │         │
   ▼         ▼
Open-world, Fixed-size
large map?  arenas or
   │         rooms?
   │            │
   ▼       ┌────┴────┐
Spatial    │         │
Hashing    ▼         ▼
or Quad-  <16       >16
tree      players   players
   │         │         │
   ▼         ▼         ▼
Players   Distance-  Grid-based
only get   based     with cell
updates    interest  visibility
for near   (AoI      (only send
neighbors  radius)   updates for
    │                entities in
    ▼                same/adjacent
Consider             cells)
relevance
layers:
position
always, HP
only when
in combat

### Decision Tree 2: Packet Prioritization

        ┌── INPUT: Network message M ready to send
        │
   ┌────┴────┐
   │         │
   ▼         ▼
M affects  M is
gameplay   cosmetic/
correct-   optional?
ness?          │
   │      ┌────┴────┐
   ▼      │         │
RELIABLE  ▼         ▼
channel   State      Visual
(TCP-like updates    flare,
over UDP) that are    weather
   │      frequent    effects
   ▼      (position,  │
Player   animation)   ▼
input,      │       UNRELIABLE
score,      ▼       (fire-and-
hit detec-  UNRELIABLE forget,
tion, item  but       no resend)
pickup      SEQUENCED
            (drop stale,
            keep latest)

### Decision Tree 3: Matchmaking Algorithm

        ┌── INPUT: Player queueing for match
        │
   ┌────┴────┐
   │         │
   ▼         ▼
Ranked/    Casual or
competitive co-op
mode?       mode?
   │         │
   ▼         ▼
SKILL-     CONNECTION-
BASED      BASED
   │         │
   ▼         ▼
Use MMR/   Group by
Elo with   ping/region
tight      first, then
tolerance  loose skill
window     matching
   │         │
   ▼         ▼
Expand     Is this
tolerance  cross-play?
over time     │
(30s → 60s  ┌────┴────┐
→ 120s)     │         │
            ▼         ▼
           YES        NO
            │         │
            ▼         ▼
         INPUT-     Same
         BASED      platform
         matching   only
         first,
         skill
         second


## Decision Tree 1: Server-Authoritative vs P2P vs Client-Hosted
<!-- STANDARD: 3min -->

```

Is this a competitive/ranked game?
├── YES → Server-authoritative (dedicated server)
│         └── Sub-decision: Player count?
│             ├── <12 players → Single server instance per match
│             ├── 12-64 → Single instance with interest management
│             └── >64 → Spatial partitioning or MMO-style zoning
│
└── NO → Is cheating tolerance high AND player count <= 8?
    ├── YES → Consider P2P lockstep (RTS, turn-based, co-op)
    │         ├── Needs full determinism? → Lockstep
    │         └── Can tolerate some drift? → P2P with host authority
    │
    └── NO → Client-hosted (listen server)
              └── MUST implement host migration

```


## Decision Tree 2: UDP vs TCP vs WebRTC
<!-- STANDARD: 3min -->

```

Is this real-time gameplay (FPS, racing, fighting, action)?
├── YES → UDP
│         └── Sub-decision: Need reliability for some messages?
│             ├── YES → Custom reliable layer over UDP (ENet, GNS)
│             └── NO → Raw UDP with sequencing
│
├── Is this turn-based, chat, or lobby system?
│   └── YES → TCP or WebSocket
│         └── Sub-decision: Browser-based?
│             ├── YES → WebSocket
│             └── NO → TCP
│
└── Is this browser-based real-time?
    └── YES → WebRTC (DataChannel, unordered/unreliable mode)
              └── Fallback: WebSocket with aggressive interpolation

```


## Decision Tree 3: Rollback vs Delay-Based Netcode
<!-- STANDARD: 3min -->

```

Game genre?
├── Fighting game → Rollback (mandatory)
│   └── Frame window: 2-8 frames rollback, 0-3 frame input delay
│
├── Fast FPS (arena shooter, tactical) → Can use either
│   ├── Server-authoritative? → Delay-based with prediction (industry standard)
│   └── P2P? → Rollback (less common, requires determinism)
│
├── MOBA, Battle Royale → Delay-based (rollback too expensive with 10+ entities)
│
└── Racing → Delay-based with aggressive prediction

```


## Decision Tree 4: Dedicated Server vs Listen Server
<!-- STANDARD: 3min -->

```

Budget for server infrastructure?
├── ZERO → Listen server
│         └── MANDATORY: host migration, anti-cheat for host
│
├── LIMITED ($500-$5K/month) → Hybrid
│   ├── Competitive → Dedicated (small fleet)
│   └── Casual → Listen server
│
└── ADEQUATE ($10K+/month) → Full dedicated fleet
    └── Sub-decision: Build vs buy orchestration?
        ├── Custom requirements → Agones on Kubernetes
        └── Standard needs, AWS shop → GameLift

```


## Decision Tree 5: Snapshot Interpolation vs Extrapolation
<!-- STANDARD: 3min -->

```

What to render between server snapshots?
├── Local player → Extrapolate (prediction)
│   └── Reconcile on server correction
│
├── Remote players:
│   ├── Snapshot buffer healthy (>2 snapshots ahead)?
│   │   └── Interpolate between last two snapshots
│   │       └── Render delay: 2 × (1/tick_rate)
│   │
│   └── Snapshot buffer starved?
│       └── Extrapolate from last known velocity (capped at 200ms)
│           └── Blend back to interpolation when snapshot arrives
│
└── Critical targets (crosshair)?
    └── Use latest snapshot directly (no interpolation delay)

```


## Decision Tree 6: Lockstep vs State Sync
<!-- STANDARD: 3min -->

```

Game has <100 entities AND full determinism possible?
├── YES → Lockstep
│   └── Bandwidth: ~1-5 KB/s regardless of entity count
│
├── NO → State sync (server sends entity states)
│   └── Sub-decision: Full state or delta?
│       ├── New connections or periodic → Full state (keyframe)
│       └── Regular updates → Delta (changed fields only)
│
└── Hybrid → State sync for most entities, lockstep for critical physics

```

## 3. Gotchas
<!-- STANDARD: 3min -->


## Gotcha 1: Client-side authority for game state ($100K+)
<!-- STANDARD: 3min -->

Assigning authority for game-critical state (health, position, score) to the client without server validation. Memory editors and packet injectors can modify any client-side value. Within 48 hours of launch, cheat tools will exist. **Fix:** Server validates every state mutation. Client sends *intent* ("I want to move here"), server sends *results* ("You are now here"). Never: client says "I have 100 HP" and server accepts it.


## Gotcha 2: TCP for real-time game communication ($75K+)
<!-- STANDARD: 3min -->

Using TCP for gameplay packets. On packet loss, TCP stalls ALL subsequent data until retransmission — the dreaded "head-of-line blocking." At 1% packet loss (common on WiFi), TCP throughput drops 50-80%. Players experience sudden freezes followed by teleportation. **Fix:** Use UDP with a custom reliability layer where needed. Send movement/aim as unreliable-sequenced (drop old, use newest). Send events (fire, reload) as reliable-ordered.


## Gotcha 3: Interpolation delay set to zero ($50K+)
<!-- STANDARD: 3min -->

Attempting to render entities at the exact moment a snapshot arrives, with no buffer against jitter. Network jitter of ±10ms at 60 tick produces visible stuttering. Players perceive "laggy servers" even when ping is low. **Fix:** Always interpolate with a buffer of at least 2× the expected tick interval (33ms at 60Hz, 16ms at 128Hz). Smooth jitter with an adaptive buffer that grows during jitter spikes.


## Gotcha 4: No server reconciliation after prediction ($60K+)
<!-- STANDARD: 3min -->

Implementing client-side prediction without server reconciliation. The predicted position drifts from the authoritative position by 1-5cm per tick due to floating-point differences, physics divergence, and other players' interference. After 60 ticks (1 second at 60Hz), the player is 60-300cm from where the server says they are. Next server snapshot snaps them back — "rubber banding." **Fix:** Store pending input commands. On server snapshot, remove acknowledged commands, re-apply unacknowledged commands from the server position.


## Gotcha 5: Rewinding all entities for lag compensation on every shot ($40K+ infrastructure)
<!-- STANDARD: 3min -->

Naively deep-copying all entity states for lag compensation on every hitscan shot. With 64 players, 100 physics objects, and 10 shots/second per player, this is 64,000 deep copies/second. **Fix:** Use a fixed-size ring buffer of entity snapshots per tick. On shot processing, rewind only entities along the raycast path. Use copy-on-write for static geometry. Budget ~0.05ms per shot, not 2ms.


## Gotcha 6: Ignoring NAT traversal for P2P games ($30K+ support tickets)
<!-- STANDARD: 3min -->

Shipping a P2P game without STUN/TURN/ICE. 90% of home users are behind NAT. 8-15% have symmetric NAT that STUN cannot traverse. These players simply cannot connect. Support tickets pile up: "Can't join friend's game." **Fix:** Implement ICE with STUN server(s) and TURN relay fallback. Budget TURN bandwidth for 5-15% of peak concurrent players. Use WebRTC/DataChannel for browser games.


## Gotcha 7: No backfill for casual matchmaking ($25K+ player churn)
<!-- STANDARD: 3min -->

One player leaves a casual match, and the remaining 9-99 players suffer through an imbalanced game or disconnect. Without backfill, a single leaver cascades into the lobby emptying. **Fix:** Implement priority backfill queue. Relax skill constraints for backfill (shorter expected match duration makes skill less important). Target <10 second fill time.

## 4. Domain-Specific Anti-Patterns
<!-- STANDARD: 3min -->

| The temptation | Why it sounds right | Why it's wrong | What to do instead | Mechanical Trigger (detect before executing) | Violation Response |
|---|---|---|---|---|
| "TCP is simpler, we'll just use that for everything" | One connection, automatic reliability, fewer lines of code | Head-of-line blocking destroys real-time feel at any packet loss. Games feel laggy on WiFi/LTE even at 30ms ping | UDP with sequenced channels. Reliable for events, unreliable-sequenced for movement/aim | | |

| "We don't need prediction, our game targets low ping only" | Simpler code, no reconciliation bugs, no rubber-banding | "Low ping" is relative. Even 20ms = 1 frame at 60fps. Perception of input lag starts at ~50ms round-trip | Always predict local player. Keep prediction simple — just movement. Omit for abilities if complex | | |

| "The client can handle hit detection, we'll add server validation later" | Faster to implement, feels instant, server code is simpler | "Later" never comes. Cheat tools ship in week one. Every kill by a cheater costs ~10 player-hours of engagement | Start with server-authoritative hit detection. Client shows blood/sparks predictively but server confirms damage | | |

| "We'll use the same tick rate for everything" | Simple to implement and reason about, uniform code path | 60-tick projectile updates waste bandwidth when 30-tick would suffice. 20-tick movement in a fighting game is unplayable. Different game aspects need different update frequencies | Variable update rate: position at 60Hz, inventory at 5Hz, chat at event-driven. Interest-manage per-entity | | |

| "P2P lockstep works for our fighting game, no need for rollback" | Deterministic, low bandwidth, no server costs | 100ms ping means 100ms input delay in lockstep. Fighting game inputs require sub-50ms response. Players across regions can't play each other | Implement GGPO-style rollback netcode. 0-frame input delay. ~3 frames rollback. Save/restore state every frame | | |

| "We'll just spin up EC2 instances manually for launch" | Quick to set up, familiar workflow, no K8s complexity | Manual scaling during launch spike = servers full → players can't play → launch day disaster. Player count oscillates 5-10x daily | Use Agones Fleet with buffer autoscaling or GameLift. Pre-warm capacity. Practice 5x scale-up drill before launch | | |

## 5. Core Architecture Models
<!-- STANDARD: 3min -->
<!-- Full 43 lines extracted to references/5-core-architecture-models.md -->

The three fundamental multiplayer topologies, each with distinct tradeoffs in cheat resistance, cost, latency, and complexity.


## Server-Authoritative (Dedicated Server)
<!-- STANDARD: 3min -->
The industry standard for competitive multiplayer. A headless game process runs on cloud infrastructure, accepting client inputs, simulating game state, and broadcasting authoritative snapshots.
**Reference:** [client-server-architecture-games.md](references/client-server-architecture-games.md)
...
> 📎 **[references/5-core-architecture-models.md](references/5-core-architecture-models.md)** — 43 lines of detailed guidance

## 6. Protocol Design: UDP, Reliability, and Message Serialization
<!-- STANDARD: 3min -->
<!-- Full 40 lines extracted to references/6-protocol-design-udp-reliability-and-message-serialization.md -->


## Why UDP
<!-- STANDARD: 3min -->
TCP's head-of-line blocking is fatal for real-time games. A single lost packet at sequence 100 blocks delivery of packets 101-150 until 100 is retransmitted — even though packets 101-150 contain newer, more important data.
**The golden rule: Old state is worthless.** When a movement packet is lost, you don't want a retransmission of the old position — you want the newest position. UDP lets you make that choice per-packet.


## Custom Reliability Layer
<!-- STANDARD: 3min -->
...
> 📎 **[references/6-protocol-design-udp-reliability-and-message-serialization.md](references/6-protocol-design-udp-reliability-and-message-serialization.md)** — 40 lines of detailed guidance

## 7. Client-Side Prediction & Server Reconciliation
<!-- STANDARD: 3min -->

**Reference:** [prediction-reconciliation-patterns.md](references/prediction-reconciliation-patterns.md)


## The Core Loop
<!-- STANDARD: 3min -->

```

Client sends input → applies locally (prediction) → stores command
Server receives input → validates → simulates → broadcasts authoritative state
Client receives snapshot → removes acknowledged commands → checks for error
  ├── Error < threshold: smooth interpolate toward server
  └── Error >= threshold: snap to server, re-apply unacked commands

```


## Prediction for Non-Local Entities
<!-- STANDARD: 3min -->

Don't predict remote players. Interpolate them from snapshots. The only entity you predict is the local player, because you have the input that drives it.

**Exception:** In fighting games with rollback, all entities are predicted because all inputs are deterministic.


## Reconciliation Thresholds
<!-- STANDARD: 3min -->

| Error Magnitude | Response | Visual Result |
|---|---|---|
| < 0.01m | Ignore | None — player won't notice |
| 0.01m - 0.1m | Smooth correct over ~100ms | Subtle, barely visible |
| > 0.1m | Snap to server, replay inputs | Visible micro-correction |
| > 2.0m | Teleport to server position | Rubber-banding — investigate cause |

## 8. Lag Compensation & Hit Registration
<!-- STANDARD: 3min -->
<!-- Full 30 lines extracted to references/8-lag-compensation-hit-registration.md -->

**Reference:** [lag-compensation-techniques.md](references/lag-compensation-techniques.md)


## The Rewind Algorithm
<!-- STANDARD: 3min -->
On receiving a fire command at server tick T, rewind all entities to where they were at the shooter's tick T_shooter:
1. Store current entity positions
...
> 📎 **[references/8-lag-compensation-hit-registration.md](references/8-lag-compensation-hit-registration.md)** — 30 lines of detailed guidance

## 9. Snapshot Interpolation & Jitter Management
<!-- STANDARD: 3min -->
<!-- Full 33 lines extracted to references/9-snapshot-interpolation-jitter-management.md -->

**Reference:** [snapshot-interpolation.md](references/snapshot-interpolation.md)


## The Interpolation Buffer
<!-- STANDARD: 3min -->
Render remote entities with a deliberate delay to absorb jitter:
Render time = server_time - interpolation_delay
...
> 📎 **[references/9-snapshot-interpolation-jitter-management.md](references/9-snapshot-interpolation-jitter-management.md)** — 33 lines of detailed guidance

## 10. Interest Management & Bandwidth Optimization
<!-- STANDARD: 3min -->
<!-- Full 34 lines extracted to references/10-interest-management-bandwidth-optimization.md -->

**Reference:** [interest-management.md](references/interest-management.md)


## The Bandwidth Budget
<!-- STANDARD: 3min -->
Target: <50 KB/s per player (downstream)
         <10 KB/s per player (upstream)
...
> 📎 **[references/10-interest-management-bandwidth-optimization.md](references/10-interest-management-bandwidth-optimization.md)** — 34 lines of detailed guidance

## 11. NAT Traversal & Relay Infrastructure
<!-- STANDARD: 3min -->
<!-- Full 31 lines extracted to references/11-nat-traversal-relay-infrastructure.md -->

**Reference:** [nat-traversal-relay.md](references/nat-traversal-relay.md)


## The Connectivity Stack
<!-- STANDARD: 3min -->
ICE (Interactive Connectivity Establishment)
 ├── Host candidates (direct LAN IP)
...
> 📎 **[references/11-nat-traversal-relay-infrastructure.md](references/11-nat-traversal-relay-infrastructure.md)** — 31 lines of detailed guidance

## 12. Matchmaking Architecture
<!-- STANDARD: 3min -->
<!-- Full 38 lines extracted to references/12-matchmaking-architecture.md -->

**Reference:** [matchmaking-architecture.md](references/matchmaking-architecture.md)


## The Matchmaking Pipeline
<!-- STANDARD: 3min -->
Player clicks "Play"
  → Pre-queue: Ping measurement, version check, ban check
...
> 📎 **[references/12-matchmaking-architecture.md](references/12-matchmaking-architecture.md)** — 38 lines of detailed guidance

## 13. Dedicated Server Operations
<!-- STANDARD: 3min -->
<!-- Full 44 lines extracted to references/13-dedicated-server-operations.md -->

**Reference:** [dedicated-server-infrastructure.md](references/dedicated-server-infrastructure.md)


## Orchestration
<!-- STANDARD: 3min -->


## Fleet Sizing Rule of Thumb
<!-- STANDARD: 3min -->
Warm pool size = peak_concurrent_matches × 0.15
...
> 📎 **[references/13-dedicated-server-operations.md](references/13-dedicated-server-operations.md)** — 44 lines of detailed guidance

## 14. Security & Anti-Cheat Architecture
<!-- STANDARD: 3min -->
<!-- Full 38 lines extracted to references/14-security-anti-cheat-architecture.md -->


## Server-Authoritative Validation
<!-- STANDARD: 3min -->
Every client-submitted value must be validated:
bool ValidateMovement(Vector3 from, Vector3 to, float delta_time) {
    float distance = length(to - from);
...
> 📎 **[references/14-security-anti-cheat-architecture.md](references/14-security-anti-cheat-architecture.md)** — 38 lines of detailed guidance

## 15. Debugging & Profiling Multiplayer Systems
<!-- STANDARD: 3min -->
<!-- COMPRESSED: Full 58 lines extracted to references/15-debugging-profiling-multiplayer-systems.md -->


## Essential Debugging Tools
<!-- STANDARD: 3min -->

**Network Simulator:**

```bash
# Linux: simulate 100ms ping, 2% packet loss, ±10ms jitter
...
> 📎 **Full content (58 lines):** [references/15-debugging-profiling-multiplayer-systems.md](references/15-debugging-profiling-multiplayer-systems.md)

## Reference Files
<!-- STANDARD: 3min -->

| File | Content |
|---|---|
| [client-server-architecture-games.md](references/client-server-architecture-games.md) | Topology patterns, authority models, tick rate selection, containerization |
| [prediction-reconciliation-patterns.md](references/prediction-reconciliation-patterns.md) | Client prediction loop, reconciliation, rollback netcode, input buffers |
| [lag-compensation-techniques.md](references/lag-compensation-techniques.md) | Backwards reconciliation, history buffer, hitscan vs projectile, sub-tick |
| [snapshot-interpolation.md](references/snapshot-interpolation.md) | Interpolation buffer, extrapolation, jitter management, entity types |
| [interest-management.md](references/interest-management.md) | Spatial relevance, frustum culling, priority tiers, bandwidth budgeting |
| [nat-traversal-relay.md](references/nat-traversal-relay.md) | STUN/TURN/ICE, UDP hole punching, relay architecture, SDR |
| [matchmaking-architecture.md](references/matchmaking-architecture.md) | Pipeline, SBMM with Glicko-2, latency routing, party matching, backfill |
| [dedicated-server-infrastructure.md](references/dedicated-server-infrastructure.md) | Docker/K8s/Agones, GameLift, monitoring, graceful shutdown, cost optimization |

## Quick Reference Commands
<!-- STANDARD: 3min -->

```bash

# Start a game server (Docker)
docker run -p 27015:27015/udp -e MAP=de_dust2 -e MAX_PLAYERS=10 gameserver:latest

# Network simulation for testing (add 100ms latency, 2% loss)
sudo tc qdisc add dev lo root netem delay 100ms 10ms loss 2%

# Remove network simulation
sudo tc qdisc del dev lo root

# Profile game server (Linux perf)
perf record -g ./gameserver_dedicated --map test_map --max_players 64 --tickrate 60

# ICE candidate testing
stunclient stun.l.google.com:19302

# Test NAT type
turnutils_natdiscover -s stun.example.com -p 3478

# UDP bandwidth test between client and server
iperf3 -c gameserver.example.com -u -p 27015 -b 100K -t 30

# Prometheus metrics endpoint check
curl http://localhost:9090/metrics | grep gameserver

```

## Verification
<!-- STANDARD: 3min -->

| # | Complete when... | Verify |
|---|-----------------|--------|
| ☐ | Complete when Server is authoritative for all gameplay state affecting fairness or economy — zero client-trusted state paths | `grep -r "trust.*client" server/` returns zero results; every state mutation path has server-side validation |
| ☐ | Complete when Client-side prediction + server reconciliation implemented together: client predicts locally, server corrects, client replays unacknowledged inputs | Test at 100ms simulated latency: prediction error < 50ms; reconciliation completes within 2 ticks |
| ☐ | Complete when UDP transport with reliability layers in use — no TCP for real-time state replication | Network stack uses ENet, GameNetworkingSockets, or equivalent; reliable-ordered + unreliable channels confirmed |
| ☐ | Complete when Interest management limits per-player bandwidth < 8 KB/s at target player count | `iperf3` or custom telemetry confirms bandwidth per player stays within budget at 2× target CCU |
| ☐ | Complete when Lag compensation (backward reconciliation) validates hits at simulated 50ms, 100ms, and 200ms ping | Hit registration feels consistent across all three latency levels in automated test suite |
| ☐ | Complete when NAT traversal with relay fallback confirmed: STUN → TURN escalation works for symmetric NAT | Connectivity diagnostics visible in lobby UI; relay budget calculated at 5-15% of projected player-hours |
| ☐ | Complete when Network condition CI tests pass at 0ms, 50ms, 100ms, 200ms latency with 0%, 1%, 5% packet loss | `tc netem` or equivalent runs in CI pipeline for every netcode feature PR |
| ☐ | Complete when FlatBuffers or bit-packed serialization in use — no JSON/XML for runtime game state | Serialization payload < 200 bytes per player update; delta compression verified in bandwidth profile |
| ☐ | Complete when Dedicated server auto-scaling configured with graceful shutdown on last player disconnect and orphaned server alerting | Agones or GameLift allocation/deallocation works; idle server shutdown timer verified |
| ☐ | Complete when Stress test passes at 2× target CCU for ≥30 minutes with tick rate maintained ≥50% of target | 128-player load test for 64-player target completes with tick rate and memory within bounds |

## Anti-Patterns
<!-- STANDARD: 3min -->

### Anti-Pattern: Trusting the client with authoritative state
**What it looks like:** Server accepts client-submitted position, health, ammo, and score without validation. "We'll add server validation after we prove the gameplay is fun." One player downloads Cheat Engine on day 2 of launch — infinite health, teleport, unlimited currency.
**Why it fails:** Client-trust architectures are irreversibly compromised the moment they launch. There is no "add validation later" — by the time fun is proven, the game's reputation (and economy) is destroyed by cheaters. Every client-trusted state variable is an attack surface that costs 1000× more to fix post-launch than to architect correctly from day one.
**Do this instead:** Server is authoritative for all gameplay state that affects fairness or economy. Client sends intent ("I want to fire", "I want to move to X"). Server validates cooldowns, ammo, line-of-sight, collision, speed limits, and applies the result. Client prediction is purely visual — the server's version of reality always wins.

### Anti-Pattern: Starting with TCP for "simplicity" — "we'll switch to UDP later"
**What it looks like:** Team builds netcode on TCP sockets because "UDP is complex." Game works fine on localhost. First remote playtest: 2% packet loss causes 200ms stalls, rubber-banding, and desync. The entire networking stack — every send/recv, every reliability layer, every serialization path — assumes TCP's ordered delivery guarantees.
**Why it fails:** Switching from TCP to UDP is not a port — it's a full rewrite. TCP provides ordered, reliable, connection-oriented streams. UDP provides unordered, unreliable, connectionless datagrams. Every assumption your code makes about delivery order, connection state, and backpressure must be re-implemented. The cost of switching is 100% of your networking code.
**Do this instead:** Start with UDP from the first multiplayer prototype. Use a library that provides reliability layers over UDP: ENet, GameNetworkingSockets (Valve), or RakNet. These give you reliable-ordered channels for critical messages and unreliable channels for per-frame state without TCP's head-of-line blocking.

### Anti-Pattern: No interest management — broadcasting all state to all players
**What it looks like:** 64-player server sends every player's full state to every other player every tick. At 60 tickrate: 64 × 63 × 60 = 241,920 messages/second. At 200 bytes per update: 48 MB/s per server. Server CPU melts at 40 players. Players on mobile or slow connections get kicked.
**Why it fails:** Bandwidth and CPU scale as O(n²) with player count. Every player added increases load on every other player's connection AND on the server's serialization pipeline. The game that works beautifully in 8-player testing collapses at 64 players during launch weekend.
**Do this instead:** Implement spatial interest management: grid-based spatial partitioning. Only replicate entities within N cells of each player. Add priority tiers: Tier 1 (visible enemies, 60Hz), Tier 2 (visible allies, 30Hz), Tier 3 (audible events, 10Hz), Tier 4 (world state, 1Hz). Add frustum culling: don't replicate entities behind the camera.

### Anti-Pattern: Skipping client-side prediction for "non-competitive" games
**What it looks like:** Co-op game with 4 players uses server-authoritative movement without prediction. Player presses W, waits 50ms for server acknowledgment, character starts moving. Every input feels delayed by the player's ping. "The game feels sluggish" becomes the #1 complaint.
**Why it fails:** 50ms of input latency without prediction makes movement feel like "wading through molasses" regardless of game type. Competitive or not, players judge game feel by responsiveness. A 10ms increase in perceived lag reduces session time by 7%. Co-op players leave just as fast as competitive players when the game feels unresponsive.
**Do this instead:** Implement client-side prediction from the first playable prototype. The pattern is the same for co-op and competitive: client immediately applies local input, sends intent to server, server processes authoritatively, client reconciles. The only difference is that co-op can tolerate slightly looser reconciliation thresholds.

### Anti-Pattern: Deploying dedicated servers without auto-scaling lifecycle management
**What it looks like:** Dedicated servers launched for each match. Server starts on match creation, runs until someone manually kills it. Players log off, server idles. Match ends, server idles for hours before timeout. Idle servers bill at full compute rate. Cloud bill is 3× projection with 40% idle waste.
**Why it fails:** Cloud providers bill for running instances, not active players. Every idle game server burns budget. Without graceful shutdown, orphaned servers accumulate. Without allocation/deallocation automation, scaling is manual, slow, and expensive.
**Do this instead:** Use Agones (Kubernetes game server orchestration) or AWS GameLift for automatic allocation and deallocation. Implement graceful shutdown: monitor player count, start 5-minute shutdown timer when last player leaves. Add max session duration (e.g., 2 hours for competitive matches). Alert on orphaned server processes older than session timeout.

### Anti-Pattern: Shipping P2P multiplayer without relay fallback
**What it looks like:** P2P game uses STUN for NAT traversal. Works beautifully in the office. Beta launches, 30% of players report "Connection failed" — no error details, just can't join games. Support forums fill with refund requests from players who literally cannot play.
**Why it fails:** 30-50% of home routers use symmetric NAT which assigns a different external port for each destination. STUN cannot traverse symmetric NAT because the port the server sees differs from the port the peer needs. These players are permanently locked out of P2P-only games with no diagnostic feedback explaining why.
**Do this instead:** Implement TURN relay fallback with ICE negotiation via libjuice or WebRTC. Try P2P → try STUN hole-punch → escalate to relay. Budget 5-15% of player-hours through relay ($0.02-$0.10/GB/player). Add connectivity diagnostics in the lobby: show NAT type, connection path (direct vs relay), and ping to relay server.

### Anti-Pattern: Testing netcode only on localhost or LAN
**What it looks like:** All netcode development and QA happens on localhost (0ms latency, 0% loss) or office LAN (< 1ms, 0% loss). The game is buttery smooth. Launch day: players on WiFi, mobile, and transcontinental connections experience rubber-banding, desync, and unplayable input delay that nobody on the dev team ever saw.
**Why it fails:** Network conditions are the primary variable in multiplayer game quality. Testing without them means you're testing a version of the game that doesn't exist for any real player. Every prediction error, reconciliation glitch, and bandwidth spike that would be caught by a 100ms/2% loss test ships to production.
**Do this instead:** Simulate network conditions in CI for every netcode feature: 0ms/0% (baseline), 50ms/0% (good WiFi), 100ms/1% (typical broadband), 200ms/2% (transcontinental), 300ms/5% (poor mobile). Use `tc netem` on Linux or Clumsy/Network Link Conditioner. Test 64-player stress scenarios with varied per-player latency profiles.

## Production Checklist
<!-- STANDARD: 3min -->
**(STANDARD)**

Before shipping any multiplayer game or netcode feature, verify every item. Each unchecked item is a launch-day disaster waiting to happen.

- [ ] **Server authority verified:** Every state mutation affecting fairness or economy is validated server-side. `grep -r "trust.*client" server/` returns zero results. Client-predicted values are purely visual, never authoritative.
- [ ] **Prediction + reconciliation implemented together:** Client predicts locally, server corrects authoritatively, client reconciles by replaying unacknowledged inputs. Prediction error < 50ms measured at 100ms simulated latency.
- [ ] **UDP transport with reliability layers:** Real-time state replication uses UDP (not TCP). Reliable-ordered channel for critical events. Unreliable channel for transient state. ENet, GameNetworkingSockets, or equivalent library in use.
- [ ] **Interest management implemented:** Spatial partitioning (grid/quadtree) limits replication scope. Per-player bandwidth < 8 KB/s at target player count measured via `iperf3` or custom telemetry.
- [ ] **Lag compensation (backward reconciliation):** Server rewinds target positions to shooter's latency when validating hits. Tested with simulated 50ms, 100ms, and 200ms ping — hit registration feels consistent at all latencies.
- [ ] **NAT traversal with relay fallback:** STUN attempted first, TURN relay fallback confirmed. Relay budget calculated at 5-15% of projected player-hours. Connectivity diagnostics visible in lobby UI.
- [ ] **Network condition CI tests pass:** All netcode features pass automated tests at 0ms, 50ms, 100ms, 200ms latency with 0%, 1%, 5% packet loss. `tc netem` or equivalent in CI pipeline.
- [ ] **Flatbuffers or bit-packed serialization:** No JSON/XML in runtime game state serialization. Schema-first serialization produces payloads < 200 bytes per player update. Delta compression verified.
- [ ] **Dedicated server auto-scaling:** Agones or GameLift configured with automatic allocation and deallocation. Graceful shutdown on last player disconnect. Max session duration enforced. Orphaned server alerting active.
- [ ] **Deterministic rollback (fighting/RTS):** If applicable, GGPO-style rollback implemented with full game state serialization every frame. Re-simulation verified deterministic across platforms.
- [ ] **Bandwidth profiling per feature:** Every RPC, replicated variable, and state update profiled for bandwidth cost. Budget enforced in CI — PRs that exceed per-player bandwidth budget are blocked.
- [ ] **Host migration designed (client-hosted):** If using listen servers, host migration protocol designed and tested. State transfer < 5 seconds. New host election logic verified under 3+ disconnection scenarios.
- [ ] **Anti-cheat architecture documented:** Server-side validation points enumerated. Anomaly detection thresholds defined (impossible speeds, invalid state transitions). Replay verification system designed.
- [ ] **Stress test at 2× target CCU:** 128-player load test for 64-player target. Tick rate maintained at ≥ 50% of target under 2× load for ≥ 30 minutes. Memory and CPU profiles reviewed.
- [ ] **Observability dashboard live:** Tick rate, player count, bandwidth per player, prediction errors, reconciliation rate, server CPU/memory — all visible in Grafana/Prometheus. Alerts on tick rate drop > 20%.

## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "UDP is too complex; we'll start with TCP and switch later" | TCP head-of-line blocking means one dropped packet stalls all messages; retrofitting UDP requires rewriting the entire netcode layer — every send/recv, every reliability layer, every serialization path |
| "We don't need client-side prediction for a co-op game" | Even in co-op, 50ms of latency without prediction makes movement feel like wading through molasses; players blame the game, not the network, and leave within the first session |
| "We'll handle lag compensation after the core gameplay is fun" | Lag compensation IS the core gameplay — without it, what's "fun" on localhost is unplayable at 100ms ping; the entire feel of the game is invalidated |
| "The server can just trust the client for now; we'll add validation later" | One player with Cheat Engine ruins the experience for 1000 legitimate players; trust-before-validate means you have no authoritative state to retroactively fix — the game is permanently compromised |
| "We'll add interest management when player count grows" | Without spatial interest management, 100 players each send updates to 99 others = 9,900 messages per tick; bandwidth explodes quadratically and server CPU melts before you hit "player count that matters" |

## References
<!-- STANDARD: 3min -->

- **Gaffer on Games** (gafferongames.com) — Glenn Fiedler's definitive series on game networking
- **Gabriel Gambetta** (gambetta.dev) — Client-Server Game Architecture series
- **Valve Developer Wiki** — Source Engine Multiplayer Networking
- **GDC Vault** — "Overwatch Gameplay Architecture and Netcode" (2017), "8 Frames in 16ms" (2018)
- **GameNetworkingSockets** — github.com/ValveSoftware/GameNetworkingSockets
- **Agones** — agones.dev (Google Cloud game server orchestration)
- **libjuice** — github.com/paullouisageneau/libjuice (lightweight ICE/STUN/TURN)
- **RFC 8445** (ICE), **RFC 5389** (STUN), **RFC 5766** (TURN)
