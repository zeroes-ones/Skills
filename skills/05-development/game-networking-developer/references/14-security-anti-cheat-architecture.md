## 14. Security & Anti-Cheat Architecture

### Server-Authoritative Validation

Every client-submitted value must be validated:

```cpp
bool ValidateMovement(Vector3 from, Vector3 to, float delta_time) {
    float distance = length(to - from);
    float max_distance = PLAYER_MAX_SPEED * delta_time * 1.1f; // 10% tolerance
    return distance <= max_distance;
}

bool ValidateDamage(float damage, uint32_t weapon_id, float range) {
    auto& weapon = WeaponDatabase[weapon_id];
    if (damage > weapon.max_damage) return false;    // Damage hack
    if (range > weapon.effective_range * 1.2f) return false; // Range hack
    return true;
}
```

### Common Attack Vectors & Defenses

| Attack | Method | Defense |
|---|---|---|
| Speedhack | Inject faster movement values | Server-side velocity cap per tick |
| Aimbot | Auto-aim at nearest enemy | Server-side raycast validates aim angle |
| Wallhack | Read enemy positions from memory | Interest management — never send occluded entity data |
| Packet injection | Spoof fire/damage packets | Authenticate packets with per-session key |
| Lag switch | Artificially delay own packets | Server-side timeout at 5s; kick at 15s no packets |
| DDoS game server | Flood server with garbage UDP | Rate limit per-IP; authenticate before heavy processing |

### DoS/DDoS Protection

- **Game server port:** Only accept packets from authenticated, match-assigned clients. Drop all others in kernel space (eBPF/XDP filter).
- **Relay service:** Use Steam SDR or cloud DDoS protection (AWS Shield, Cloudflare Spectrum).
- **Rate limiting:** Max 200 packets/second per client. Drop excess silently.
