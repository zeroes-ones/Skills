## 13. Dedicated Server Operations

**Reference:** [dedicated-server-infrastructure.md](references/dedicated-server-infrastructure.md)

### Orchestration

| Platform | Best For | Learning Curve | Cost |
|---|---|---|---|
| Agones + K8s | Custom control, multi-cloud, scale | High | Infrastructure only |
| AWS GameLift | Quick start, AWS-native, managed | Low | Infrastructure + GameLift fee |
| PlayFab Multiplayer | Azure ecosystem, managed | Low | Per-minute |
| Bare metal | 128+ tick servers, maximum perf | Medium | Instance cost, manual ops |

### Fleet Sizing Rule of Thumb

```
Warm pool size = peak_concurrent_matches × 0.15
               + headroom_for_spike

Example: 10,000 CCU, 10 players/match = 1,000 matches
Warm pool: 1,000 × 0.15 = 150 servers always ready
Scale-up time: <60 seconds for additional 200 servers
```

### Performance Budgets

| Tick Rate | Max Players | Tick Budget | CPU Required |
|---|---|---|---|
| 30 | 64 | 33ms | 2 vCPU |
| 60 | 10 | 16ms | 2 vCPU |
| 60 | 64 | 16ms | 4 vCPU |
| 128 | 10 | 7.8ms | 4 vCPU |
| 128 | 64 | 7.8ms | 8 vCPU (or bare metal) |

### Graceful Shutdown

```
1. Unregister from matchmaker (stop receiving new players)
2. Notify clients: "Server closing in 30s"
3. Allow 30s for client disconnect or match completion
4. Save match results and replay
5. Terminate process
```
