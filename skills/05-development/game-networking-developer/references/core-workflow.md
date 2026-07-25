## Core Workflow

Game networking follows a 6-phase pipeline. Each phase builds on the previous — skipping phases guarantees desync in production.

### Phase 1 (~15 min): Transport & Protocol Selection
Choose UDP for real-time gameplay (FPS, fighting, racing), TCP for turn-based or slow-state games. Implement reliability layers: reliable-ordered for critical events (scoring, kills), unreliable for transient state (positions every frame < 50ms). Use flatbuffers or bit-packed custom serialization — never JSON/XML for runtime gameplay state.

### Phase 2 (~20 min): Server-Authoritative Architecture
Server is the source of truth for all gameplay state. Clients send inputs only. Server processes inputs, updates simulation, sends snapshots. Never trust client-reported state (position, health, inventory). Implement server-side validation for every client action.

### Phase 3 (~20 min): Client-Side Prediction & Reconciliation
Predict local player movement immediately (don't wait for server ack). Store unacknowledged inputs in a circular buffer. When server state arrives, reconcile: re-simulate from last acknowledged state with stored inputs. If prediction error > threshold, snap to server position (with interpolation to prevent popping).

### Phase 4 (~25 min): Lag Compensation & Hit Registration
For shooter hit detection: rewind server state to what the shooter saw at their ping time. Use a ring buffer of recent world states (configurable history, typically 500ms). Validate shot against rewound state. Apply damage to current state. Handle high-ping edge cases: cap compensation window at 200ms.

### Phase 5 (~20 min): Interest Management & Bandwidth
Only send entities relevant to each player. Spatial: grid-based or distance-based relevance. Prioritize: critical entities at high frequency, distant at low frequency. Budget: aim for < 8KB/s per player for competitive games. Implement delta compression — only send changed properties.

### Phase 6 (~25 min): Testing, Profiling & Anti-Cheat
Simulate network conditions: 0-300ms latency, 0-10% packet loss, jitter 0-50ms. Profile bandwidth per-player with real gameplay sessions. Implement server-side replay validation. Detect impossible actions (speed hacks, teleport hacks) via server-side simulation comparison.
