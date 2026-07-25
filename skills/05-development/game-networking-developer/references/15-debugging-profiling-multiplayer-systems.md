## 15. Debugging & Profiling Multiplayer Systems

### Essential Debugging Tools

**Network Simulator:**
```bash
# Linux: simulate 100ms ping, 2% packet loss, ±10ms jitter
sudo tc qdisc add dev eth0 root netem \
    delay 100ms 10ms 25% \
    loss 2% 25%
```

**Built-in Debug Overlay:**
```cpp
// Draw net debug info on screen
DrawText(0, 0, "Ping: %dms", ping_ms);
DrawText(0, 16, "Packet Loss: %.1f%%", packet_loss * 100);
DrawText(0, 32, "Snapshots Buffered: %d", interp_buffer.size());
DrawText(0, 48, "Prediction Error: %.3fm", prediction_error);
DrawText(0, 64, "Bandwidth In: %.1f KB/s", bw_in / 1024.0f);
DrawText(0, 80, "Bandwidth Out: %.1f KB/s", bw_out / 1024.0f);
```

### Common Desync Causes & Diagnosis

| Symptom | Likely Cause | Diagnostic Check |
|---|---|---|
| Rubber-banding | Prediction without reconciliation | Log prediction error per tick |
| Jittery remote players | Too little interpolation delay | Log snapshot inter-arrival variance |
| Entities teleporting | No interpolation at all | Check if Interpolate() is called |
| Shots don't register (server) | Rewind buffer too small | Log rewind target time vs buffer range |
| Shots register late (client) | TCP for fire events | Check channel assignment — fire must be reliable UDP, not TCP |
| Players can't connect | NAT hole punch failure | Log ICE candidate pair results |
| Server CPU spike every 30s | GC pause or large allocation | Profile with perf/perfview; use object pools |

### Profiling Commandments

1. **Profile on the server binary, not the client.** Graphics and input distort profiles.
2. **Use tick-level profiling:** `TickProfiler::Begin("Physics"); ... TickProfiler::End();` — shows per-subsystem cost per tick.
3. **Network bandwidth profiling:** Log bytes per channel, per client. Identify bandwidth hogs.
4. **Simulate realistic conditions:** Wi-Fi packet loss, mobile handoff, high player counts. Don't profile on LAN.
5. **Memory:** Watch for per-tick allocations. All game-server allocations should be pre-allocated or pooled.

### Tick Budget Breakdown (Target: 60t 16ms budget)

```
Network Receive:    0.5ms (3%)
Game Logic:         2.0ms (13%)
Physics:            4.0ms (25%)
Lag Compensation:   1.0ms (6%)
Snapshot Build:     1.5ms (9%)
Network Send:       1.0ms (6%)
Headroom:           6.0ms (38%) ← For spikes, GC, OS scheduling
Total:              16.0ms
```

---
