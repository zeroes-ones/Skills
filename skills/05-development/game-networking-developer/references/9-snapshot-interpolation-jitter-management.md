## 9. Snapshot Interpolation & Jitter Management

**Reference:** [snapshot-interpolation.md](references/snapshot-interpolation.md)

### The Interpolation Buffer

Render remote entities with a deliberate delay to absorb jitter:

```
Render time = server_time - interpolation_delay
            = server_time - (2 × tick_interval)

Example: 60 tick, 16.67ms interval → 33ms render delay
```

### Jitter Buffer Adaptation

```cpp
target_delay = max(target_delay, measured_jitter * 2.0f);
target_delay = clamp(target_delay, 16ms, 150ms);
```

The buffer grows during jitter spikes (WiFi interference, mobile handoff) and slowly shrinks when the network stabilizes.

### Extrapolation Fallback

When snapshots run dry (packet loss):

1. Extrapolate from last known velocity (linear dead reckoning).
2. Cap extrapolation at **200ms maximum**.
3. On snapshot arrival, blend from extrapolated to interpolated over 100ms.
4. After **500ms with no snapshots**, freeze the entity (don't extrapolate into walls).
