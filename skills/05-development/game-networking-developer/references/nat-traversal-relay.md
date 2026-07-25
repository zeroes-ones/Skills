# NAT Traversal & Relay Architecture

> **Reference:** Getting packets through NATs, firewalls, and hostile networks — the plumbing of peer-to-peer multiplayer.

## The NAT Problem

Network Address Translation (NAT) lets multiple devices share one public IP. But it blocks unsolicited inbound packets — exactly what P2P games need. ~90% of home users are behind at least one NAT.

## NAT Types & Traversability

| NAT Type | Behavior | P2P Possible? | STUN Works? |
|---|---|---|---|
| Full Cone | Any external host can send to mapped port once mapped | Yes | Yes |
| Restricted Cone | Only hosts that received outbound packet can send back | Yes | Yes |
| Port Restricted Cone | Only host+port that received outbound can send back | Yes | Yes |
| Symmetric NAT | Different mapping per destination. Port-restricted + destination-restricted | Varies | No — need TURN |
| Carrier-Grade NAT (CGNAT) | ISP-level NAT. 100.64.0.0/10. Often symmetric | Rarely | TURN required |

### NAT Behavior Matrix

```
                     Full Cone │ Restricted │ Port-Rest. │ Symmetric
Full Cone               ✓          ✓            ✓            ✓
Restricted Cone          ✓          ✓            ✓            ~
Port-Restricted Cone     ✓          ✓            ✓            ✗
Symmetric NAT            ✓          ~            ✗            ✗

~ = Possible with port prediction
```

## STUN (Session Traversal Utilities for NAT)

STUN servers tell clients their public IP:port mapping.

### STUN Flow

```
Client A                        STUN Server                    Client B
    │                                │                              │
    │── Binding Request ────────────▶│                              │
    │◀── Binding Response ───────────│                              │
    │    (Your public IP:Port)       │                              │
    │                                │                              │
    │──(exchange addresses via       │                              │
    │    matchmaking/signaling)──────│──────────────────────────────│
    │                                │                              │
    │── UDP packet ────────────────────────────────────────────────▶│
    │◀─ UDP packet ─────────────────────────────────────────────────│
```

### STUN Binding Request (Simplified)

```cpp
struct StunBindingRequest {
    uint16_t type = 0x0001;          // Binding Request
    uint16_t length;
    uint32_t magic_cookie = 0x2112A442;
    uint8_t  transaction_id[12];     // Random
};
```

**Limitation:** STUN fails for symmetric NAT because the mapping is destination-specific. The port STUN sees isn't the port Peer B will see.

## TURN (Traversal Using Relays around NAT)

When direct P2P fails, relay all traffic through a TURN server.

### TURN Flow

```
Client A ──────▶ TURN Server ──────▶ Client B
   │                  │                   │
   │  (Allocate)      │                   │
   │◀─────────────────│                   │
   │  (relay address)  │                   │
   │                  │                   │
   │  Send(indication,│                   │
   │   data, peer=B)  │                   │
   │─────────────────▶│                   │
   │                  │  Data(indication) │
   │                  │──────────────────▶│
```

### TURN Allocation

```
Client → TURN: Allocate Request
TURN → Client: Allocate Success Response
               { RELAY-ADDRESS: 203.0.113.5:52000,
                 LIFETIME: 600 seconds }

Client → TURN: CreatePermission { peer: Client B's address }
TURN → Client: CreatePermission Success

Client → TURN: Send Indication { peer: B, data: game_packet }
TURN → Client B: Data Indication { peer: A, data: game_packet }
```

### TURN Costs

| Concurrent Connections | Bandwidth/Conn | Monthly Cost (AWS) | Monthly Cost (Self-Hosted) |
|---|---|---|---|
| 1,000 | 50 KB/s | ~$3,000 | ~$500 |
| 10,000 | 50 KB/s | ~$30,000 | ~$3,000 |
| 100,000 | 50 KB/s | ~$300,000 | ~$25,000 |

**Mitigation:**
1. Only use TURN as fallback (5-15% of connections typically need it).
2. Use UDP TURN (not TCP) — bidirectional streams double cost.
3. Geographic TURN placement: 1 TURN cluster per region.
4. Aggressive allocation timeout: release relay after 60s idle.

## ICE (Interactive Connectivity Establishment)

ICE combines STUN + TURN with a priority system to find the best path.

### ICE Candidate Types

```
Priority (highest → lowest):
1. Host candidate: Direct local IP:port (same LAN)
2. Server Reflexive (srflx): STUN-discovered public mapping
3. Relay candidate: TURN relay address

P2P attempt order:
  1. Try host-to-host (LAN)
  2. Try srflx-to-srflx (STUN)
  3. Try srflx-to-relay (partial TURN)
  4. Fall back to relay-to-relay (full TURN)
```

### ICE Candidate Gathering

```cpp
struct IceCandidate {
    std::string foundation;   // Unique per physical interface
    uint32_t    priority;     // Computed priority
    std::string transport;    // "udp" or "tcp"
    std::string ip;
    uint16_t    port;
    std::string type;         // "host", "srflx", "relay"
};

uint32_t ComputePriority(int type_pref, int local_pref, int component_id) {
    // Type preference: host=126, srflx=100, relay=0
    return (type_pref << 24) | (local_pref << 8) | (256 - component_id);
}
```

### Connectivity Checks

ICE performs STUN binding requests over candidate pairs (4-way handshake) to verify reachability:

```
Check 1: A:srflx → B:srflx → SUCCESS (both non-symmetric NATs)
Check 2: A:srflx → B:relay → SUCCESS (B behind symmetric NAT)
Check 3: A:relay → B:srflx → SUCCESS (A behind symmetric NAT)
```

## Game-Specific NAT Traversal Libraries

| Library | Protocol | Features | Platforms |
|---|---|---|---|
| Steam Datagram Relay (SDR) | UDP + encryption | STUN + relay built-in, DDoS protection, QoS | Windows, Linux, macOS |
| libjuice (WebRTC-lite) | UDP/ICE | Lightweight ICE, no SDP parsing | All |
| ENet | UDP | Reliability layers, no NAT traversal built-in | All |
| GameNetworkingSockets (Valve) | UDP | SDR-like, open source | Windows, Linux, macOS |
| Photon Realtime | UDP/TCP/WebRTC | Managed relay, no STUN needed | All |

## Relay Server Architecture

### Steam Datagram Relay (SDR) Model

```
              ┌──────────┐
              │  SDR POP │  (Point of Presence)
              │ US-West  │
              └────┬─────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───▼───┐    ┌────▼────┐    ┌───▼───┐
│Client │    │  SDR    │    │Client │
│  A    │    │  Relay  │    │  B    │
└───────┘    └─────────┘    └───────┘

SDR handles:
- NAT traversal (STUN-like)
- Relay fallback (TURN-like)
- DDoS protection (authenticated packets)
- Route optimization (nearest POP selected)
```

### Self-Hosted Relay Architecture

```
                    ┌─────────────┐
                    │  Matchmaker │
                    │  (chooses   │
                    │   relay)    │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────▼─────┐    ┌────▼─────┐    ┌─────▼─────┐
    │  Relay    │    │  Relay   │    │  Relay    │
    │  us-east  │    │ eu-west  │    │ ap-seoul  │
    └─────┬─────┘    └────┬─────┘    └─────┬─────┘
          │               │               │
    ┌─────▼─────┐   ┌────▼─────┐   ┌─────▼─────┐
    │ Game Srv  │   │ Game Srv │   │ Game Srv  │
    └───────────┘   └──────────┘   └───────────┘

Relay = lightweight packet forwarder, no simulation
```

### Relay Packet Forwarding Performance

```
Single relay instance (c5.xlarge, 4 vCPU):
  - Max packets/sec: ~500,000
  - Max concurrent sessions: ~10,000
  - Latency added: <1ms (in-region), 3-5ms (cross-region)
  - Bandwidth: 1 Gbps (~125 MB/s)
```

## UDP Hole Punching (Direct P2P)

For non-symmetric NATs, UDP hole punching works without relay:

```
1. A sends UDP → B (creates NAT mapping on A's side)
     → B's NAT drops packet (no inbound mapping yet)
2. B sends UDP → A (creates NAT mapping on B's side)
     → A's NAT now has mapping from step 1 → packet reaches A!
3. A sends UDP → B again → B's NAT mapping from step 2 → packet reaches B!
4. Connection established
```

**Success rate:** ~82% for home NATs, ~50% for corporate/enterprise NATs.

## Common Pitfalls

1. **Assuming STUN always works** — ~8-15% of connections need TURN relay. Always implement relay fallback.
2. **ICE timeout too short** — Mobile/WiFi can take 3-5 seconds for candidate gathering. Minimum 10s timeout.
3. **Not refreshing NAT bindings** — Most NATs expire UDP mappings in 30-120 seconds. Send keepalives every 15 seconds.
4. **IPv4-only thinking** — IPv6 eliminates NAT. Always prefer IPv6 when available (direct P2P).
5. **Relay bandwidth costs unmonitored** — One 100-player game on relay = $0.50/hour. Budget and cap.

## Keepalive Strategy

```cpp
void SendKeepalives() {
    static const float KEEPALIVE_INTERVAL = 15.0f;  // Seconds
    static const float NAT_TIMEOUT_MIN = 30.0f;      // Conservative minimum

    if (time_since_last_send > KEEPALIVE_INTERVAL) {
        for (auto& peer : connected_peers) {
            if (peer.is_idle) {
                SendSmallPacket(peer, PACKET_KEEPALIVE);
                // 4 bytes: type(1) + padding(3) — enough to refresh NAT
            }
        }
    }
}
```

## References

- RFC 5389: Session Traversal Utilities for NAT (STUN)
- RFC 5766: Traversal Using Relays around NAT (TURN)
- RFC 8445: Interactive Connectivity Establishment (ICE)
- Steam Datagram Relay documentation — Valve
- libjuice: github.com/paullouisageneau/libjuice
- GameNetworkingSockets: github.com/ValveSoftware/GameNetworkingSockets
