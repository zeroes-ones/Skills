# Dedicated Server Infrastructure

> **Reference:** Deploying, scaling, and operating game server fleets — from bare metal to Kubernetes.

## Server Binary Design

### Headless Mode

A dedicated server is your game executable without rendering, audio, or UI:

```cpp
int main(int argc, char* argv[]) {
    // Parse command-line arguments
    ServerConfig config = ParseServerArgs(argc, argv);
    // --map de_dust2 --max_players 10 --tickrate 64 --port 27015
    // --gamemode competitive --region us-east

    // Initialize only server subsystems
    NetworkManager::Init(config.port, config.max_players);
    PhysicsEngine::Init(config.tickrate);
    GameModeManager::Init(config.gamemode);
    // -- NO renderer init, NO audio init, NO input init --

    // Load map
    World::LoadMap(config.map);

    // Main loop
    while (running) {
        auto frame_start = now();

        NetworkManager::ReceivePackets();      // Collect client input
        GameModeManager::ProcessGameLogic();   // Rules, scoring, events
        PhysicsEngine::Step(config.tickrate);  // Physics simulation
        World::UpdateEntities();               // Entity lifecycle
        NetworkManager::SendSnapshots();       // Broadcast state to all clients

        // Frame rate control
        auto frame_time = now() - frame_start;
        auto target_frame = 1.0 / config.tickrate;
        if (frame_time < target_frame) {
            sleep(target_frame - frame_time);
        }
    }

    NetworkManager::Shutdown();
    return 0;
}
```

### Build Configuration

```bash
# Dedicated server build (Linux, no graphics)
cmake .. \
    -DBUILD_DEDICATED_SERVER=ON \
    -DBUILD_CLIENT=OFF \
    -DUSE_VULKAN=OFF \
    -DUSE_OPENGL=OFF \
    -DUSE_AUDIO=OFF \
    -DCMAKE_BUILD_TYPE=Release \
    -DENABLE_LTO=ON

# Result: single ~20-80MB binary with minimal dependencies
```

## Docker Containerization

### Minimal Dockerfile

```dockerfile
FROM ubuntu:22.04 AS builder

RUN apt-get update && apt-get install -y \
    build-essential cmake libssl-dev zlib1g-dev

COPY . /src
WORKDIR /src
RUN cmake -DBUILD_DEDICATED_SERVER=ON -DCMAKE_BUILD_TYPE=Release . && make -j$(nproc)

FROM ubuntu:22.04 AS runtime

RUN apt-get update && apt-get install -y \
    libssl3 libstdc++6 ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /src/gameserver /app/gameserver
COPY maps/ /app/maps/
COPY config/ /app/config/

RUN useradd -m -u 1000 gameserver
USER gameserver:gameserver

EXPOSE 27015/udp 27015/tcp

ENTRYPOINT ["/app/gameserver"]
CMD ["--map", "default", "--max_players", "10"]
```

### Docker Compose (Local Dev)

```yaml
version: "3.8"
services:
  gameserver-1:
    build: .
    ports:
      - "27015:27015/udp"
      - "27015:27015/tcp"
    environment:
      - SERVER_NAME=Dev Server 1
      - MAX_PLAYERS=10
      - TICKRATE=64
      - MAP=de_dust2
    volumes:
      - ./demos:/app/demos
    restart: unless-stopped
    logging:
      driver: json-file
      options:
        max-size: "50m"
        max-file: "3"
```

## Orchestration with Agones (Kubernetes)

Agones is the industry standard for game server orchestration on Kubernetes:

### GameServer Resource

```yaml
apiVersion: agones.dev/v1
kind: GameServer
metadata:
  name: game-server-example
spec:
  ports:
    - name: game-udp
      portPolicy: Dynamic
      containerPort: 7654
      protocol: UDP
  health:
    initialDelaySeconds: 10
    periodSeconds: 5
    failureThreshold: 3
  template:
    spec:
      containers:
        - name: gameserver
          image: registry.example.com/game-server:1.2.3
          resources:
            requests:
              cpu: "2"
              memory: "2Gi"
            limits:
              cpu: "4"
              memory: "4Gi"
          env:
            - name: GAME_PORT
              valueFrom:
                fieldRef:
                  fieldPath: status.ports[0].port
```

### Fleet (Warm Pool) Configuration

```yaml
apiVersion: agones.dev/v1
kind: Fleet
metadata:
  name: warm-pool-us-east
spec:
  replicas: 50  # Always keep 50 ready
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
  template:
    spec:
      ports:
        - name: game-udp
          portPolicy: Dynamic
          containerPort: 7654
          protocol: UDP
      health:
        initialDelaySeconds: 15
        periodSeconds: 5
      template:
        spec:
          containers:
            - name: gameserver
              image: registry.example.com/game-server:1.2.3
              resources:
                requests:
                  cpu: "2"
                  memory: "2Gi"
```

### Autoscaler

```yaml
apiVersion: autoscaling.agones.dev/v1
kind: FleetAutoscaler
metadata:
  name: fleet-autoscaler-us-east
spec:
  fleetName: warm-pool-us-east
  policy:
    type: Buffer
    buffer:
      bufferSize: 10        # Always keep 10 ready
      minReplicas: 5
      maxReplicas: 200
```

## AWS GameLift (Managed Alternative)

### Fleet Configuration

```json
{
  "Name": "competitive-us-east",
  "Description": "US East fleet for competitive matches",
  "BuildId": "build-abc123",
  "ServerProcesses": [
    {
      "LaunchPath": "/app/gameserver",
      "Parameters": "--mode dedicated",
      "ConcurrentExecutions": 4
    }
  ],
  "EC2InboundPermissions": [
    {
      "FromPort": 27015,
      "ToPort": 27030,
      "IpRange": "0.0.0.0/0",
      "Protocol": "UDP"
    }
  ],
  "InstanceType": "c5.2xlarge",
  "RuntimeConfiguration": {
    "GameSessionActivationTimeoutSeconds": 300
  }
}
```

### GameLift vs Agones Comparison

| Feature | Agones | GameLift |
|---|---|---|
| Platform | Kubernetes (any cloud/on-prem) | AWS only |
| Pricing Model | Infrastructure cost only | Per-instance + GameLift fee |
| Warm pool | Manual Fleet config | Built-in |
| Matchmaking | External (FlexMatch or custom) | Integrated FlexMatch |
| Latency-based placement | Manual | Built-in |
| DDoS protection | Manual (cloud-specific) | AWS Shield |
| Portability | Full (runs anywhere K8s runs) | AWS-locked |
| Best for | Custom control, multi-cloud | Quick start, AWS-native shops |

## Performance Tuning

### CPU Pinning for High Tick Rate (128t+)

```yaml
spec:
  containers:
    - name: gameserver
      resources:
        requests:
          cpu: "4"
          memory: "4Gi"
        limits:
          cpu: "4"  # Guaranteed QoS — CPU pinning
          memory: "4Gi"
      env:
        - name: OMP_NUM_THREADS
          value: "4"
        - name: GOMAXPROCS
          value: "4"
```

### Network Tuning

```bash
# On host / privileged init container:
# Increase UDP buffer sizes
sysctl -w net.core.rmem_max=26214400
sysctl -w net.core.wmem_max=26214400
sysctl -w net.core.rmem_default=26214400
sysctl -w net.core.wmem_default=26214400

# Increase connection tracking table
sysctl -w net.netfilter.nf_conntrack_max=1048576

# Disable UDP checksum offloading (can cause issues with some NICs)
ethtool -K eth0 tx-udp_tnl-segmentation off
```

### Tick Rate CPU Budget

```
Tick Rate   │ Max Players │ CPU Budget/Tick │ Required CPU
────────────┼─────────────┼────────────────┼─────────────
30          │ 64          │ 33ms            │ 2 vCPU
60          │ 10          │ 16ms            │ 2 vCPU
60          │ 64          │ 16ms            │ 4 vCPU
128         │ 10          │ 7.8ms           │ 4 vCPU
128         │ 64          │ 7.8ms           │ 8 vCPU
```

## Monitoring & Metrics

### Key Metrics to Track

```cpp
struct ServerMetrics {
    // Tick performance
    float tick_duration_ms;
    float tick_duration_p99_ms;
    int   ticks_missed;           // >0 = overload

    // Network
    int   packets_received_per_tick;
    int   packets_sent_per_tick;
    float bytes_sent_per_second;
    float bytes_received_per_second;
    float packet_loss_percentage; // Per-client

    // Players
    int   connected_players;
    int   max_players;
    float avg_ping_ms;
    float p99_ping_ms;

    // Memory
    size_t ram_used_mb;
    size_t ram_limit_mb;

    // Game state
    int   entity_count;
    int   active_physics_bodies;
};
```

### Observability Stack

```
Game Server → Prometheus metrics endpoint /metrics
            → Structured logs → Fluentd/Fluent Bit → Elasticsearch/Loki
            → Tick traces → Jaeger/Zipkin (OpenTelemetry)
```

### Prometheus Metrics Example

```cpp
// In-game metrics
static prometheus::Gauge tick_duration{"gameserver_tick_duration_ms",
    "Server tick duration in milliseconds"};
static prometheus::Gauge player_count{"gameserver_player_count",
    "Number of connected players"};
static prometheus::Counter packets_sent{"gameserver_packets_sent_total",
    "Total packets sent"};
static prometheus::Histogram ping_histogram{"gameserver_ping_ms",
    "Client ping distribution", {10, 20, 30, 50, 80, 100, 150, 200}};
```

## Graceful Shutdown

```cpp
void InitiateShutdown(const std::string& reason) {
    server_state = SHUTTING_DOWN;
    LogInfo("Server shutting down: {}", reason);

    // 1. Notify all clients
    BroadcastPacket(PacketType::SERVER_SHUTDOWN, {
        {"reason", reason},
        {"estimated_time", 30} // seconds until termination
    });

    // 2. Stop accepting new connections
    matchmaker.UnregisterServer(server_id);

    // 3. Wait for clients to disconnect or timeout
    auto deadline = now() + std::chrono::seconds(30);
    while (connected_players > 0 && now() < deadline) {
        NetworkManager::ProcessDisconnects();
        sleep(1);
    }

    // 4. Save match data
    SaveMatchResults();
    SaveReplayFile();

    // 5. Cleanup
    NetworkManager::Shutdown();
    MetricsReporter::FinalFlush();
}
```

## Cost Optimization

### Instance Right-Sizing

```
Game Type        │ Players/Inst │ Instance    │ Cost/Hour │ Cost/PlayerHr
─────────────────┼──────────────┼─────────────┼───────────┼──────────────
FPS 5v5          │ 1 match      │ c5.xlarge   │ $0.17     │ $0.017
FPS 5v5          │ 4 matches    │ c5.4xlarge  │ $0.68     │ $0.017
Battle Royale    │ 1 match      │ c5.4xlarge  │ $0.68     │ $0.007
Minecraft-like   │ 1 server     │ c5a.xlarge  │ $0.13     │ $0.003
MOBA 5v5         │ 2 matches    │ c5.2xlarge  │ $0.34     │ $0.017

Strategy: Pack multiple matches per instance when CPU allows.
```

### Spot/Preemptible Instances

- Use spot instances for casual/unranked modes (60-90% cost savings).
- Never use spot for ranked matches (risk of mid-game termination).
- Implement graceful spot termination handling (2-minute warning via instance metadata).

## References

- Agones: agones.dev / github.com/googleforgames/agones
- AWS GameLift documentation: docs.aws.amazon.com/gamelift
- "Running Dedicated Game Servers on Kubernetes" — Google Cloud blog
- "Scaling Game Servers with Agones" — GDC 2019, Mark Mandel (Google)
- Unreal Engine: Dedicated Server compilation guide
- Unity: Dedicated Server build guide
