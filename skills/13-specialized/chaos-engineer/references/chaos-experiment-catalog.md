# Chaos Experiment Catalog

> 31 ready-to-use chaos experiment definitions covering infrastructure, network, application, security, and state failure modes.

---

## 1. Single Pod Termination

| Field | Value |
|-------|-------|
| **Name** | `checkout-pod-kill-single` |
| **Category** | Infrastructure |
| **Hypothesis** | When one checkout-service pod is terminated, the load balancer detects the failure, routes traffic to remaining pods, and no customer requests fail. P99 latency may increase up to 100ms during the 5-second rebalancing window. |
| **Steady State Metrics** | P99 latency < 300ms, error rate < 0.1%, pod count = target (3), request success rate = 100% |
| **Method** | `kubectl delete pod -l app=checkout-service --now=true` (Chaos Mesh: `PodChaos` with action `pod-kill`, target=1 pod) |
| **Blast Radius** | 1 pod in checkout-service, single namespace, single AZ |
| **Duration** | 5 minutes (pod will be restarted by ReplicaSet) |
| **Abort Conditions** | Error rate > 1%, P99 latency > 1s for >30s, any 5xx returned to customers |
| **Rollback** | Automatic — ReplicaSet recreates pod. Manual: `kubectl scale deployment checkout-service --replicas=3` |
| **Expected Outcome** | **Success**: Pod terminates, new pod appears within 10s, zero failed requests, latency spike <100ms. **Failure**: Requests fail with 5xx, latency spikes >1s, pod count stays below target, load balancer doesn't detect pod removal. |

---

## 2. 50% Pod Termination

| Field | Value |
|-------|-------|
| **Name** | `checkout-pod-kill-50pct` |
| **Category** | Infrastructure |
| **Hypothesis** | When 50% of checkout-service pods are terminated simultaneously, remaining pods handle traffic with P99 latency <500ms, error rate <0.5%, and no complete request failures occur. |
| **Steady State Metrics** | P99 latency < 300ms, error rate < 0.1%, pod count = running replicas (target: 6), per-pod CPU < 80% |
| **Method** | `kubectl delete pod -l app=checkout-service --field-selector=status.phase=Running --max=3` (Chaos Mesh: `PodChaos` selector with mode=`fixed-percent`, value=50) |
| **Blast Radius** | 3 of 6 pods, checkout-service only, single AZ. Run during low-traffic window only. |
| **Duration** | 10 minutes |
| **Abort Conditions** | Error rate > 2%, P99 latency > 2s for >30s, any P0 alert fires |
| **Rollback** | Scale deployment to restore: `kubectl scale deployment checkout-service --replicas=6`. Verify health endpoint returns 200. |
| **Expected Outcome** | **Success**: New pods spin up within 15s, latency P99 stays <500ms during rebalance, error rate <0.5%, throughput returns to baseline within 60s. **Failure**: Requests fail, circuit breakers don't open, pods can't restart due to resource constraints, latency spike >2s. |

---

## 3. Rolling Pod Termination

| Field | Value |
|-------|-------|
| **Name** | `checkout-pod-kill-rolling` |
| **Category** | Infrastructure |
| **Hypothesis** | When checkout-service pods are terminated one at a time every 10 seconds, the system maintains steady state throughout the rolling termination cycle with no request failures. |
| **Steady State Metrics** | P99 latency < 400ms, error rate < 0.1%, minimum 2 healthy pods at all times |
| **Method** | Chaos Mesh `PodChaos` with action `pod-kill`, mode=`fixed`, value=3, duration=30s between pods. Or script: `for pod in $(kubectl get pod -l app=checkout-service -o name); do kubectl delete $pod --wait=false && sleep 10; done` |
| **Blast Radius** | All pods in checkout-service (one at a time), single namespace |
| **Duration** | Duration = (pod count * interval) + 2 minutes observation. Typically 5-8 minutes. |
| **Abort Conditions** | Two consecutive terminated pods fail to restart, error rate > 0.5% for >15s, P99 latency > 1s |
| **Rollback** | Abort script, scale deployment: `kubectl scale deployment checkout-service --replicas=3` |
| **Expected Outcome** | **Success**: Each pod termination results in <10 requests lost, new pod replaces killed pod within timeout, no cascading failures. **Failure**: Requests fail during transition, autoscaler doesn't keep up, pods fail readiness probes. |

---

## 4. Single Node Failure

| Field | Value |
|-------|-------|
| **Name** | `node-failure-single` |
| **Category** | Infrastructure |
| **Hypothesis** | When a single worker node fails, all pods running on that node are rescheduled to other nodes within 5 minutes, and service-level SLOs are maintained during rescheduling. |
| **Steady State Metrics** | Node count = N, all nodes Healthy, pod distribution balanced across nodes, P99 latency < 300ms |
| **Method** | AWS FIS: `aws:ec2:terminate-instances` on a single instance in the node group. Gremlin: `Shutdown` attack on host. LitmusChaos: `node-kill` experiment. Chaos Mesh: `PodChaos` with node selector. |
| **Blast Radius** | 1 k8s worker node (not control plane). Avoid nodes running critical system components (monitoring, ingress controllers). |
| **Duration** | 15 minutes (includes node replacement by ASG) |
| **Abort Conditions** | Any service reports error rate > 1%, capacity drops below 2x current load requirement, any P0 alert fires |
| **Rollback** | ASG replaces the instance automatically. Manual: cordon other nodes temporarily. If experiment must be stopped: no rollback needed — node is truly gone but ASG replaces it. |
| **Expected Outcome** | **Success**: Node terminates, pods appear on remaining nodes within 5 min, no request failures, P99 latency spike <200ms. **Failure**: Pods stuck in Pending (insufficient capacity), long recovery time, services degrade. |

---

## 5. AZ Failure Simulation

| Field | Value |
|-------|-------|
| **Name** | `az-failure-us-east-1a` |
| **Category** | Infrastructure |
| **Hypothesis** | When us-east-1a becomes unavailable, all traffic is routed to us-east-1b and us-east-1c within 60 seconds, P99 latency stays below 1s during failover, and no requests are lost. |
| **Steady State Metrics** | Traffic distributed across 3 AZs, P99 latency < 300ms, error rate < 0.1%, per-AZ pod count balanced |
| **Method** | Block all traffic to/from the AZ using a Network ACL. AWS FIS: `aws:network:disrupt-connectivity` for a subnet. Or terminate all EC2 instances in the AZ. Gremlin: `Blackhole` traffic to the AZ's CIDR range. |
| **Blast Radius** | Single AZ (us-east-1a). All services in that AZ affected. Must have at least 2 remaining AZs with sufficient capacity. |
| **Duration** | 15 minutes |
| **Abort Conditions** | Remaining AZs cannot handle traffic (latency > 3s, error rate > 5%), any service enters degraded mode with customer impact, multi-service dependency chain breaks |
| **Rollback** | Restore Network ACL, allow traffic, or re-create instances in ASG. Verification: all AZs show healthy endpoints. |
| **Expected Outcome** | **Success**: Traffic shifts to remaining AZs in <60s, no complete request failures, P99 latency <1s during shift, services in remaining AZs handle full load. **Failure**: Insufficient capacity in remaining AZs, cross-AZ dependency causes cascade, DNS failover doesn't trigger, load balancer health checks fail on remaining AZs. |

---

## 6. Network Latency (50ms)

| Field | Value |
|-------|-------|
| **Name** | `network-latency-50ms-orders-to-payment` |
| **Category** | Network |
| **Hypothesis** | When 50ms of latency is added to calls from orders-service to payment-service, orders-service P99 latency increases by no more than 50ms and no orders fail. No timeouts triggered. |
| **Steady State Metrics** | orders-service → payment-service latency: P50 < 20ms, P99 < 100ms. orders-service error rate < 0.1% |
| **Method** | Chaos Mesh: `NetworkChaos` with delay=50ms, direction=`from`, targets with label `app=orders-service`, sources with label `app=payment-service`. `tc qdisc add dev eth0 root netem delay 50ms` on specific pod. |
| **Blast Radius** | Traffic from orders-service to payment-service only. Other service calls not affected. |
| **Duration** | 5 minutes |
| **Abort Conditions** | payment-service error rate increases, downstream services show cascading latency, orders timeout and fail |
| **Rollback** | Chaos Mesh auto-rollback on experiment end. Manual: `tc qdisc del dev eth0 root netem` |
| **Expected Outcome** | **Success**: Added latency is visible in p50/p99 metrics, no timeouts, no errors, service meets its latency SLO. **Failure**: Timeouts occur (if configured too low), errors increase, retry storms cascade. |

---

## 7. Network Latency (200ms)

| Field | Value |
|-------|-------|
| **Name** | `network-latency-200ms-orders-to-payment` |
| **Category** | Network |
| **Hypothesis** | When 200ms of latency is added to calls from orders-service to payment-service, orders-service P99 latency stays below 1s, the circuit breaker does NOT trip (within normal latency variance), and no orders fail. |
| **Steady State Metrics** | orders-service P99 latency < 500ms, payment-service timeout errors = 0, circuit breaker state = CLOSED |
| **Method** | Chaos Mesh `NetworkChaos` delay=200ms, jitter=50ms, correlation=50. Gremlin `Network Latency` attack. |
| **Blast Radius** | orders-service → payment-service only. |
| **Duration** | 5 minutes |
| **Abort Conditions** | Circuit breaker opens, error rate > 1%, P99 latency > 2s |
| **Rollback** | Remove latency injection. Verify payment-service response times return to baseline. |
| **Expected Outcome** | **Success**: Latency P99 increases by ~200ms but stays <1s, no errors, circuit breaker stays closed (latency within tolerance). **Failure**: Timeout exceeded, circuit breaker trips, errors increase. |

---

## 8. Network Latency (500ms)

| Field | Value |
|-------|-------|
| **Name** | `network-latency-500ms-orders-to-payment` |
| **Category** | Network |
| **Hypothesis** | When 500ms of latency is added to calls from orders-service to payment-service, the circuit breaker opens within 30 seconds, fast-fail responses are returned, and orders-service health is maintained. |
| **Steady State Metrics** | orders-service P50 latency < 50ms, circuit breaker CLOSED, error rate < 0.1% |
| **Method** | Chaos Mesh `NetworkChaos` delay=500ms, jitter=100ms. Verify system response: does circuit breaker detect the latency as failure? |
| **Blast Radius** | orders-service → payment-service path only. |
| **Duration** | 5 minutes (must be long enough for circuit breaker to open and potentially half-open) |
| **Abort Conditions** | Circuit breaker does not open within expected time, cascading failures to other services, error rate > 5% |
| **Rollback** | Stop latency. Circuit breaker should transition HALF_OPEN → CLOSED automatically. |
| **Expected Outcome** | **Success**: Circuit breaker opens within 30s of sustained latency, fast-fail responses returned (no waiting), orders-service stays healthy, after latency stops breaker transitions to half-open then closed. **Failure**: Circuit breaker doesn't open, requests queue waiting for timeout, orders-service thread pool exhausts, cascading failure. |

---

## 9. Network Latency (2000ms)

| Field | Value |
|-------|-------|
| **Name** | `network-latency-2000ms-orders-to-payment` |
| **Category** | Network |
| **Hypothesis** | When 2000ms latency is added to orders-service → payment-service calls, the circuit breaker opens, fast-fail responses are returned within 10ms, and orders-service maintains its own latency SLO. |
| **Steady State Metrics** | orders-service P99 latency < 500ms, circuit breaker CLOSED, active thread count < 50, error rate < 0.1% |
| **Method** | Chaos Mesh `NetworkChaos` delay=2000ms, correlation=100 (constant delay). Wait for circuit breaker to open. |
| **Blast Radius** | orders-service → payment-service. |
| **Duration** | 5 minutes |
| **Abort Conditions** | orders-service thread pool exhaustion, cascading failures, latency spike beyond 5s |
| **Rollback** | Stop latency injection immediately. Monitor circuit breaker recovery. |
| **Expected Outcome** | **Success**: Circuit breaker opens, requests fail fast (~10ms), orders-service healthy, thread pool stays unsaturated. **Failure**: Thread pool exhausted (retries + timeouts overwhelm), orders-service goes down, cascade to upstream services. |

---

## 10. Packet Loss (1%)

| Field | Value |
|-------|-------|
| **Name** | `packet-loss-1pct-orders-to-payment` |
| **Category** | Network |
| **Hypothesis** | When 1% packet loss is introduced between orders-service and payment-service, TCP retransmission handles the loss, latency increases slightly but no requests fail. |
| **Steady State Metrics** | orders-service → payment-service P99 latency < 200ms, error rate = 0%, TCP retransmit rate < 0.5% |
| **Method** | Chaos Mesh `NetworkChaos` loss=1%, correlation=50. `tc qdisc add dev eth0 root netem loss 1%`. |
| **Blast Radius** | Network path from orders-service to payment-service only. |
| **Duration** | 5 minutes |
| **Abort Conditions** | Error rate > 0.5%, P99 latency > 1s, TCP retransmit rate > 5% |
| **Rollback** | Remove netem loss. |
| **Expected Outcome** | **Success**: TCP retransmits lost packets, latency increases minimally (<50ms), no application-level errors. **Failure**: Application errors increase, retries timeout, connection pool exhausts from slow connections. |

---

## 11. Packet Loss (5%)

| Field | Value |
|-------|-------|
| **Name** | `packet-loss-5pct-orders-to-payment` |
| **Category** | Network |
| **Hypothesis** | When 5% packet loss is introduced, TCP handles it with retransmission, latency increases but stays within P99 < 1s, and no requests fail. Connection pool may need tuning. |
| **Steady State Metrics** | P99 latency < 500ms (baseline), error rate < 0.1%, active connections < max pool |
| **Method** | `tc qdisc add dev eth0 root netem loss 5% 25%` (5% loss with 25% correlation). |
| **Blast Radius** | Single network path. |
| **Duration** | 5 minutes |
| **Abort Conditions** | Error rate > 2%, connection pool exhaustion, upstream timeouts |
| **Rollback** | `tc qdisc del dev eth0 root netem` |
| **Expected Outcome** | **Success**: TCP handles loss gracefully, latency increases but stays within limits, no application errors. **Failure**: Connection pool exhaustion (slow connections accumulate), retry storms, timeouts. |

---

## 12. Packet Loss (10%)

| Field | Value |
|-------|-------|
| **Name** | `packet-loss-10pct-orders-to-payment` |
| **Category** | Network |
| **Hypothesis** | When 10% packet loss is introduced, the system should degrade gracefully. Circuit breaker may open to protect orders-service. No cascading failures. |
| **Steady State Metrics** | All services healthy, no cascading failures, error rate < 5% (expected increase) |
| **Method** | `tc qdisc add dev eth0 root netem loss 10% 50%` |
| **Blast Radius** | orders-service → payment-service. |
| **Duration** | 5 minutes |
| **Abort Conditions** | Cascading failure to upstream services, orders-service unhealthy, crash loops |
| **Rollback** | Remove loss. |
| **Expected Outcome** | **Success**: Circuit breaker may open, fast-fail returned, no cascading failures. **Failure**: Connection pool exhausts, orders-service backs up, upstream services time out waiting for orders-service. |

---

## 13. Network Partition (Service to Database)

| Field | Value |
|-------|-------|
| **Name** | `network-partition-db-isolation` |
| **Category** | Network |
| **Hypothesis** | When orders-service is isolated from its primary database, the service returns a degraded-mode response (cached data or error message) instead of hanging or crashing. |
| **Steady State Metrics** | orders-service health endpoint = 200, connection pool active = 5, error rate < 0.1% |
| **Method** | Chaos Mesh `NetworkChaos` action=partition, direction=both, target with selector `app=orders-service`. Blackhole all traffic from orders-service to database IP/port. |
| **Blast Radius** | orders-service isolated from its database. Other services not affected. Cache service still reachable. |
| **Duration** | 5 minutes |
| **Abort Conditions** | orders-service crash loop, HTTP 503 from ingress, database not actually isolated (should not affect other services) |
| **Rollback** | Remove partition, verify database connectivity, verify orders-service recovers, verify data consistency. |
| **Expected Outcome** | **Success**: orders-service returns cached data or graceful error, connection pool reaps dead connections, health endpoint returns 200 (degraded). **Failure**: orders-service crashes, connection pool exhausts without reaping, gateway times out, upstream services degrade waiting for orders-service. |

---

## 14. DNS Failure (Drop All Queries)

| Field | Value |
|-------|-------|
| **Name** | `dns-failure-drop-queries` |
| **Category** | Network |
| **Hypothesis** | When DNS resolution fails completely, services with cached DNS entries continue to function for TTL duration, and services query DNS return a cached-or-default response or graceful error. |
| **Steady State Metrics** | DNS query success rate = 100%, service discovery works, external API calls succeed |
| **Method** | Chaos Mesh `DNSChaos` with action=error, patterns=`*`, or block UDP port 53 via iptables. Gremlin: `DNS Blackhole` attack. |
| **Blast Radius** | All DNS queries from targeted service(s). |
| **Duration** | 5 minutes |
| **Abort Conditions** | Service discovery breaks, new pods can't register, traffic routing fails, cascading failures |
| **Rollback** | Unblock DNS, verify resolution works, flush DNS cache. |
| **Expected Outcome** | **Success**: Services with DNS cache continue to operate, new connections fail gracefully, health checks catch DNS issue. **Failure**: All services lose ability to make external calls, service discovery for new pods fails, cascading failure. |

---

## 15. Slow DNS Resolution

| Field | Value |
|-------|-------|
| **Name** | `dns-failure-slow-resolution` |
| **Category** | Network |
| **Hypothesis** | When DNS resolution takes 5 seconds per query, services with DNS cache are unaffected for cached entries, and DNS timeouts are handled gracefully. |
| **Steady State Metrics** | DNS resolution time < 50ms, external API latency P99 < 500ms |
| **Method** | `iptables -A OUTPUT -p udp --dport 53 -m statistic --mode random --probability 0.5 -j DROP` combined with delayed upstream DNS. Or Chaos Mesh `DNSChaos` with pattern matching. |
| **Blast Radius** | Single service or namespace. |
| **Duration** | 5 minutes |
| **Abort Conditions** | Connections stall, thread pool exhaust, downstream services degrade |
| **Rollback** | Remove iptables rule, verify DNS resolution speed. |
| **Expected Outcome** | **Success**: Cached DNS entries serve requests, DNS timeouts handled gracefully, service log shows "DNS resolution timeout" warnings. **Failure**: Thread pool exhausts waiting for DNS, connections stall, services become unresponsive. |

---

## 16. CPU Stress (80%)

| Field | Value |
|-------|-------|
| **Name** | `cpu-stress-80pct-inventory` |
| **Category** | Application |
| **Hypothesis** | When inventory-service pods are stressed to 80% CPU, inventory lookup latency P99 stays below 1s and throughput drops by no more than 20%. Autoscaler should detect and scale. |
| **Steady State Metrics** | CPU utilization < 40%, inventory P99 latency < 200ms, throughput 1000 req/s per pod |
| **Method** | Chaos Mesh `StressChaos` with stressors cpu-workers=2, load=80 (percentage). Litmus: `cpu-hog` experiment. Gremlin: `CPU` attack with 80% load. `stress-ng --cpu 2 --cpu-load 80`. |
| **Blast Radius** | 2 inventory-service pods. Non-critical path. |
| **Duration** | 10 minutes (to allow autoscaler to react) |
| **Abort Conditions** | Latency P99 > 3s, error rate > 2%, autoscaler fails to detect, pods get OOM-killed |
| **Rollback** | Stop stress injection. Verify CPU returns to baseline. |
| **Expected Outcome** | **Success**: Latency increases proportionally, no errors, autoscaler adds pods, throughput recovers. **Failure**: Pods become unresponsive, latency spikes, errors increase, autoscaler doesn't trigger. |

---

## 17. CPU Stress (100%)

| Field | Value |
|-------|-------|
| **Name** | `cpu-stress-100pct-inventory` |
| **Category** | Application |
| **Hypothesis** | When inventory-service is stressed to 100% CPU, autoscaler detects CPU saturation, scales up additional pods, and existing pods remain responsive but degraded. |
| **Steady State Metrics** | CPU < 50%, inventory P99 latency < 300ms, error rate < 0.1% |
| **Method** | `stress-ng --cpu $(nproc) --cpu-load 100 --timeout 300s`. Chaos Mesh `StressChaos` with stressors cpu-workers=4, load=100. |
| **Blast Radius** | 2 pods in inventory-service. Ensure other services don't share the same node. |
| **Duration** | 10 minutes |
| **Abort Conditions** | Pod OOM-killed, node becomes unhealthy, other pods on same node affected, error rate > 5% |
| **Rollback** | Stop stress immediately. Node may need pod rescheduling if it became unhealthy. |
| **Expected Outcome** | **Success**: Autoscaler detects CPU > 80% and scales up, latency degrades but no errors, existing pods stay healthy. **Failure**: Node becomes NotReady, pods on same node are evicted, cascading failures from resource contention. |

---

## 18. Memory Exhaustion (90%)

| Field | Value |
|-------|-------|
| **Name** | `memory-stress-90pct-inventory` |
| **Category** | Application |
| **Hypothesis** | When inventory-service pods are stressed to 90% memory, GC pressure increases latency but no OOM kills occur, and autoscaler scales up based on memory utilization. |
| **Steady State Metrics** | Memory < 60%, P99 latency < 300ms, GC pause time < 100ms, no OOM events |
| **Method** | Chaos Mesh `StressChaos` with stressors memory-workers=4, memory-size=90% (of pod memory limit). Gremlin: `Memory` attack. `stress-ng --vm 4 --vm-bytes 90%`. |
| **Blast Radius** | 1-2 inventory-service pods. Verify memory limits set correctly. |
| **Duration** | 10 minutes |
| **Abort Conditions** | OOM kill occurs, pod crashes, latency > 3s, node memory pressure (affects other pods) |
| **Rollback** | Stop stress. Check if any pods were OOM-killed and need restart. |
| **Expected Outcome** | **Success**: Memory usage reaches 90%, GC frequency increases, latency degrades but stays within SLO, no OOM kills, autoscaler reacts. **Failure**: OOM kill, pod crash loop, node memory pressure evicts other pods. |

---

## 19. Memory Exhaustion (95%)

| Field | Value |
|-------|-------|
| **Name** | `memory-stress-95pct-edge` |
| **Category** | Application |
| **Hypothesis** | When memory usage reaches 95% of the pod limit, the application handles memory pressure with increased GC and may begin refusing requests with HTTP 503 (pressure signal) instead of crashing. |
| **Steady State Metrics** | Memory < 70%, GC pause < 200ms, no OOM, HTTP 503 rate < 1% |
| **Method** | Chaos Mesh `StressChaos` stressors memory-workers=4, memory-size=95%. |
| **Blast Radius** | Single pod, single service. Ensure pod has memory limits and no other co-located critical services. |
| **Duration** | 5 minutes |
| **Abort Conditions** | OOM kill, node pressure, cascading pod evictions |
| **Rollback** | Stop stress. If OOM killed, pod will auto-restart. |
| **Expected Outcome** | **Success**: Memory saturates, GC runs continuously, application stays up but heavily degraded, possibly returns 503 to shed load. **Failure**: OOM kill, node pressure, pod crash loop (if memory leak limits are wrong). |

---

## 20. Disk Fill (85%)

| Field | Value |
|-------|-------|
| **Name** | `disk-fill-85pct` |
| **Category** | Application |
| **Hypothesis** | When disk reaches 85% utilization, the application continues to function normally. Alerts for disk usage fire at the configured threshold (80%). |
| **Steady State Metrics** | Disk utilization < 60%, write latency < 10ms, log shipping works, health endpoint = 200 |
| **Method** | `dd if=/dev/zero of=/tmp/fillfile bs=1M count=XXX` to fill to 85%. Gremlin: `Disk Fill` with 85% path=/tmp. LitmusChaos: `disk-fill` with fill-percentage=85. |
| **Blast Radius** | Single pod instance, ephemeral storage only (not persistent volumes if avoidable). |
| **Duration** | 10 minutes |
| **Abort Conditions** | Application crashes, writes fail, log rotation fails, health check fails |
| **Rollback** | `rm /tmp/fillfile`. Verify disk returns below threshold and alert clears. |
| **Expected Outcome** | **Success**: Application continues running, alert fires at 80% threshold, writes succeed, logs rotate correctly. **Failure**: Application crash on write, health check fails, log rotation errors, monitoring gap. |

---

## 21. Disk Fill (95%)

| Field | Value |
|-------|-------|
| **Name** | `disk-fill-95pct-critical` |
| **Category** | Application |
| **Hypothesis** | When disk reaches 95% utilization, the application degrades gracefully: read requests succeed, write requests return 503 with a clear error message, health endpoint returns 200 (degraded). |
| **Steady State Metrics** | Disk < 70%, write latency < 20ms, application writes succeed |
| **Method** | `dd if=/dev/zero of=/tmp/fillfile bs=1M count=XXX` to fill to 95%. |
| **Blast Radius** | Single pod, not persistent volume. |
| **Duration** | 10 minutes |
| **Abort Conditions** | Application crash, persistent data loss, unable to recover disk space |
| **Rollback** | Delete fill file: `rm /tmp/fillfile`. Verify writes resume. |
| **Expected Outcome** | **Success**: Read operations succeed, writes fail with 503, app stays up, monitoring detects the issue. **Failure**: Application crashes on write, can't write logs, kernel panic, complete service failure. |

---

## 22. File Descriptor Exhaustion

| Field | Value |
|-------|-------|
| **Name** | `fd-exhaustion-inventory` |
| **Category** | Application |
| **Hypothesis** | When file descriptors are exhausted, the application cannot open new connections or files, returns errors gracefully (HTTP 503), and releases FDs when existing connections close. |
| **Steady State Metrics** | Open FDs < 50% of limit, new connections succeed, error rate < 0.1% |
| **Method** | Launch processes that open and hold FDs: `ulimit -n` within a container, then `for i in $(seq 1 10000); do exec {fd}$i<>/dev/null; done`. Gremlin: `Resource` → `File Descriptor Exhaustion`. |
| **Blast Radius** | Single container. |
| **Duration** | 5 minutes |
| **Abort Conditions** | Service becomes unresponsive, cannot health check (needs FD), crash loop |
| **Rollback** | Kill FD-holding processes. Verify FDs released. Restart container if needed. |
| **Expected Outcome** | **Success**: New connections fail with 503, existing connections/sockets remain open, app stays responsive to health checks (dedicated health endpoint FD not exhausted). **Failure**: App crashes, health check fails, complete unavailability. |

---

## 23. Process Kill (Random)

| Field | Value |
|-------|-------|
| **Name** | `process-kill-random-inventory` |
| **Category** | Application |
| **Hypothesis** | When a random process in inventory-service is killed, the application detects the process crash, restarts it, and continues serving requests. No customer-visible impact. |
| **Steady State Metrics** | Process count = expected (e.g., 1 JVM + 1 sidecar), health endpoint = 200, error rate < 0.1% |
| **Method** | `kill -9 $(ps aux | grep inventory | awk '{print $2}' | shuf -n 1)` inside the container. Gremlin: `Process Kill` with random process. |
| **Blast Radius** | Single container. |
| **Duration** | 5 minutes |
| **Abort Conditions** | Container crash, persistent process failure, dependency chain breakage |
| **Rollback** | If process doesn't auto-restart, restart container: `kubectl rollout restart deployment/inventory-service`. |
| **Expected Outcome** | **Success**: Process restarts immediately (managed by supervisord or container runtime), health check recovers, no request failures. **Failure**: Container dies with killed PID, service unavailable until Kubernetes restarts pod. |

---

## 24. Process Kill (Targeted — Main Application Process)

| Field | Value |
|-------|-------|
| **Name** | `process-kill-main-jvm-inventory` |
| **Category** | Application |
| **Hypothesis** | When the main application process (JVM/node/Python) in inventory-service is killed, the container restarts within the pod restart policy threshold, and requests during the restart window fail gracefully (load balancer retries). |
| **Steady State Metrics** | Main process PID = running, container uptime > 1 hour, startup time < 30s |
| **Method** | `kill -15 $(pidof java)` inside inventory-service container. Or `kubectl exec deploy/inventory-service -- kill 1` (kills PID 1 in container). |
| **Blast Radius** | Single pod, single container. |
| **Duration** | 5 minutes |
| **Abort Conditions** | Pod crash loop, startup takes > 5 minutes, readiness probe fails permanently |
| **Rollback** | Kubernetes restarts the container. If stuck in crash loop: `kubectl rollout undo deployment/inventory-service`. |
| **Expected Outcome** | **Success**: Container restarts within 30s, readiness probe transitions to NotReady then Ready, requests during transition may fail briefly (load balancer handles), pod returns to healthy. **Failure**: Crash loop, readiness probe never passes, startup takes too long, failed requests count is too high. |

---

## 25. Dependency Returning 500s

| Field | Value |
|-------|-------|
| **Name** | `dependency-500-payment-service` |
| **Category** | Application |
| **Hypothesis** | When payment-service returns HTTP 500 for 50% of requests, the circuit breaker in orders-service opens within 60 seconds, subsequent requests fail fast, and orders-service remains healthy. |
| **Steady State Metrics** | orders-service → payment-service error rate < 0.1%, circuit breaker CLOSED, orders-service thread pool active < 20 |
| **Method** | Inject HTTP interceptor/middleware returning 500 for matched pattern. Chaos Mesh `HTTPChaos` with abort=true, percentage=50. Gremlin: `HTTP Fault` → 500. |
| **Blast Radius** | orders-service calls to payment-service only. |
| **Duration** | 10 minutes (long enough for circuit breaker lifecycle: CLOSED → OPEN → HALF_OPEN) |
| **Abort Conditions** | orders-service thread pool exhaustion, cascading failures to upstream services, error rate > 10% across all endpoints |
| **Rollback** | Stop HTTP fault injection. Monitor circuit breaker recovery. |
| **Expected Outcome** | **Success**: Circuit breaker opens within expected time, fast-fail on payment calls, orders-service stays healthy, after fault stops breaker transitions to half-open then closed. **Failure**: No circuit breaker, thread pool exhaustion from queued/timeout requests, orders-service goes down. |

---

## 26. Dependency Timeout

| Field | Value |
|-------|-------|
| **Name** | `dependency-timeout-payment-service` |
| **Category** | Application |
| **Hypothesis** | When payment-service hangs (no response, no error) for all requests, the circuit breaker in orders-service detects the timeout as failure, opens within 60 seconds, and subsequent requests fail fast. |
| **Steady State Metrics** | orders-service → payment-service latency P99 < 200ms, circuit breaker CLOSED, timeout count = 0 |
| **Method** | Inject a delay that exceeds the timeout configured in orders-service (e.g., if timeout=5s, inject 10s delay). Chaos Mesh `HTTPChaos` delay=10s, percentage=100. |
| **Blast Radius** | orders-service calls to payment-service only. |
| **Duration** | 10 minutes |
| **Abort Conditions** | orders-service thread pool exhaustion, connection pool exhaustion, cascading failures |
| **Rollback** | Remove delay injection immediately. |
| **Expected Outcome** | **Success**: Timeout fires within configured window, circuit breaker counts failures and opens, fast-fail activated, orders-service stays healthy. **Failure**: No timeout configured (infinite wait), thread pool exhausts, connection pool exhausts, cascading failure. |

---

## 27. Dependency Returning Malformed JSON

| Field | Value |
|-------|-------|
| **Name** | `dependency-malformed-response-payment` |
| **Category** | Application |
| **Hypothesis** | When payment-service returns malformed JSON responses, orders-service detects the parse error, returns a graceful error response (not a 500 crash), and continues processing other requests. |
| **Steady State Metrics** | orders-service error rate (JSON parse errors) = 0, orders-service P99 latency < 300ms |
| **Method** | Inject proxy that truncates response body at 50%, or replaces JSON body with `{invalid-json`. Gremlin: `HTTP Fault` → Response modification. Use a service mesh sidecar with Envoy ext_authz or Wasm filter. |
| **Blast Radius** | orders-service responses from payment-service only. |
| **Duration** | 5 minutes |
| **Abort Conditions** | orders-service panics/crashes, error rate > 5%, memory leak (accumulating error state) |
| **Rollback** | Remove response modification, clear any error caches. |
| **Expected Outcome** | **Success**: orders-service logs the parse error, returns a 502 or fallback response, continues processing, no crash or memory leak. **Failure**: orders-service crashes on parse error (unhandled exception), returns 500 for all requests, memory leak from error accumulation. |

---

## 28. Connection Pool Exhaustion

| Field | Value |
|-------|-------|
| **Name** | `connection-pool-exhaustion-payment` |
| **Category** | Application |
| **Hypothesis** | When the connection pool from orders-service to payment-service is exhausted, new connection attempts fail immediately (fail-fast), requests are queued or rejected, and the system degrades gracefully without crashing. |
| **Steady State Metrics** | Connection pool utilization < 50%, active connections < maxPoolSize, queued connections = 0, error rate < 0.1% |
| **Method** | Establish persistent connections to fill the pool: create N slow queries/hanging HTTP connections to payment-service from orders-service until pool is full. Gremlin: `Connection Pool Exhaustion` attack. |
| **Blast Radius** | orders-service → payment-service connection pool only. |
| **Duration** | 5 minutes |
| **Abort Conditions** | orders-service becomes unresponsive, cascading failures, thread pool also exhausts |
| **Rollback** | Close held connections abruptly. Pool should drain and recover. |
| **Expected Outcome** | **Success**: Connection acquisition times out (fast), failure to acquire connection returns 503 gracefully, orders-service stays healthy. **Failure**: Connections block waiting for pool, thread pool exhausts, cascading failure. |

---

## 29. Circuit Breaker Verification Test

| Field | Value |
|-------|-------|
| **Name** | `circuit-breaker-verify-payment` |
| **Category** | Application |
| **Hypothesis** | When payment-service failures exceed the circuit breaker threshold (50% failure over 10s window), the circuit opens within 15s, fast-fail responses are returned within 10ms, and after the fault stops the circuit transitions through HALF_OPEN back to CLOSED. |
| **Steady State Metrics** | Circuit breaker state = CLOSED, requests to payment-service succeed with P50 < 50ms |
| **Method** | Inject 100% failure rate (500 or timeout) to payment-service for 20 seconds, then stop. Observe circuit breaker lifecycle. |
| **Blast Radius** | orders-service → payment-service only. |
| **Duration** | 10 minutes (fault 20s, observe 10 min for recovery) |
| **Abort Conditions** | Circuit breaker fails to open, circuit breaker fails to recover, orders-service goes down |
| **Rollback** | Stop fault injection. Circuit breaker should self-recover. |
| **Expected Outcome** | **Success**: Circuit opens within 15s of sustained failures, fast-fail returns fail responses in <10ms, after fault stops HALF_OPEN trial succeeds → CLOSED. **Failure**: Circuit stays CLOSED (no pattern implemented), opens but never recovers, OPEN state prevents all traffic even after dependency heals. |

---

## 30. Retry Storm Detection Test

| Field | Value |
|-------|-------|
| **Name** | `retry-storm-detection` |
| **Category** | Application |
| **Hypothesis** | When payment-service has transient failures, the retry mechanism with exponential backoff and jitter prevents a retry storm, and no thundering herd effect is observed on the downstream service. |
| **Steady State Metrics** | Retry rate < 1% of total requests, payment-service request rate = orders-service request rate × (1 + retry%) |
| **Method** | Inject 30% intermittent failures (alternate success/failure) to payment-service. Observe retry patterns. A properly implemented retry with backoff should show decelerating retry rates. |
| **Blast Radius** | orders-service → payment-service. |
| **Duration** | 10 minutes |
| **Abort Conditions** | Retry storm (payment-service request rate > 3x normal), payment-service failure cascade |
| **Rollback** | Stop fault injection. |
| **Expected Outcome** | **Success**: Retries happen with exponential backoff + jitter, retry rate stabilizes, no thundering herd. **Failure**: Linear retries without backoff cause retry storm, payment-service request rate spikes, cascading failure. |

---

## 31. Clock Skew (30 Minutes Forward)

| Field | Value |
|-------|-------|
| **Name** | `clock-skew-30min` |
| **Category** | State |
| **Hypothesis** | When system clock is advanced by 30 minutes, JWT tokens with short expiry may be rejected, TTL-based cache entries may expire prematurely, and time-based rate limiters may reset. The application handles these changes without crashing. |
| **Steady State Metrics** | JWT validation: 100% success, cache hit rate: baseline, rate limiter: correct counts, scheduled jobs: normal timing |
| **Method** | Chaos Mesh `TimeChaos` with timeOffset=30m, mode=all. Gremlin: `Time Travel` attack. In container: `date -s "+30 minutes"` (within test container only). |
| **Blast Radius** | Single container/pod. NOT the host clock. |
| **Duration** | 5 minutes |
| **Abort Conditions** | Auth failures > 1%, persistent data corruption, clock skew affects other services (NTP resets) |
| **Rollback** | Stop TimeChaos. NTP should resync clock within minutes. Verify: `date` shows correct time. |
| **Expected Outcome** | **Success**: Time-sensitive operations validate correctly or fail gracefully, cache TTLs update correctly after clock resync, no persistent data corruption. **Failure**: JWT tokens incorrectly accepted/rejected after clock resync, stale data served due to incorrect TTL expiration, rate limiters behave erratically. |

---

## 32. Clock Skew (24 Hours Forward)

| Field | Value |
|-------|-------|
| **Name** | `clock-skew-24h` |
| **Category** | State |
| **Hypothesis** | When system clock is advanced by 24 hours, all time-sensitive operations (token validation, cache TTL, certificate validation) behave correctly after NTP resync. No persistent side effects. |
| **Steady State Metrics** | Token validation: 100%, cache hit rate returns to baseline within 5 min after skew removal, cert validation: 100% |
| **Method** | Chaos Mesh `TimeChaos` timeOffset=24h. Date-shift in isolated container. |
| **Blast Radius** | Single pod. Must NOT affect database timestamps (use read replica with separate clock). |
| **Duration** | 5 minutes (then NTP resync) |
| **Abort Conditions** | Data corruption, database timestamp inconsistency, cascading time-related failures |
| **Rollback** | Remove time offset. NTP should resync. Verify all time-sensitive operations. |
| **Expected Outcome** | **Success**: After clock resync, all time operations return to normal, cached entries have correct TTLs, no auth failures. **Failure**: Cached data marked as expired causes cache stampede, JWT tokens fail validation, scheduled jobs fire incorrectly, persistent data timestamp corruption. |

---

## 33. Certificate Expiry Simulation

| Field | Value |
|-------|-------|
| **Name** | `certificate-expiry-simulation` |
| **Category** | Security |
| **Hypothesis** | When an internal TLS certificate is expired, the health monitoring system detects the certificate error, clients reject the connection, and the service fails safe (no unencrypted fallback). |
| **Steady State Metrics** | TLS handshake success rate = 100%, certificate expiry days > 30, health check success = 100% |
| **Method** | Replace the service's TLS certificate with an expired one (or self-signed). Use `openssl` to generate expired cert: `openssl x509 -in cert.pem -days -1 -out expired.pem`. Load into service or mount as secret. |
| **Blast Radius** | Single service endpoint. |
| **Duration** | 10 minutes |
| **Abort Conditions** | Service reverts to unencrypted HTTP, data leak, panic/crash loop |
| **Rollback** | Restore valid certificate. Verify TLS handshake succeeds. |
| **Expected Outcome** | **Success**: Clients reject expired certificate with clear error, health checks detect and report the failure, monitoring fires cert expiry alert. **Failure**: Service falls back to unencrypted HTTP, clients accept expired cert (no validation), no alert fires. |

---

## 34. Read Replica Failure

| Field | Value |
|-------|-------|
| **Name** | `read-replica-failure` |
| **Category** | Infrastructure |
| **Hypothesis** | When the database read replica fails, all read traffic is routed to the primary. Primary CPU increases but stays < 80%, and write latency remains within SLO. |
| **Steady State Metrics** | Read traffic: 80% read-replica, 20% primary. Primary CPU < 40%, write P99 latency < 50ms |
| **Method** | Terminate the read replica instance. AWS FIS: `aws:rds:failover-db-instance` or terminate the reader instance. |
| **Blast Radius** | Single read replica. Primary can handle read traffic. |
| **Duration** | 15 minutes |
| **Abort Conditions** | Primary CPU > 80%, write latency > 100ms, connection pool exhaustion, reads fail |
| **Rollback** | Autoscaling should provision new read replica. Manual: re-create read replica from latest snapshot. |
| **Expected Outcome** | **Success**: Reads automatically route to primary, primary handles combined load within limits, new replica provisions and reads redistribute. **Failure**: Connection pool exhausts (read pool vs write pool not separated), primary cannot handle load, reads fail with timeouts. |

---

## 35. Cache Node Failure

| Field | Value |
|-------|-------|
| **Name** | `cache-node-failure-redis` |
| **Category** | Infrastructure |
| **Hypothesis** | When one Redis cache node fails, the application falls back to database for cache misses, database load increases but stays within limits, and no requests fail. |
| **Steady State Metrics** | Cache hit rate > 90%, database query rate = baseline, P99 latency < 300ms |
| **Method** | Kill the Redis pod/node. Chaos Mesh: `PodChaos` with selector `app=redis`. AWS ElastiCache: trigger failover. |
| **Blast Radius** | Single Redis shard/node. |
| **Duration** | 10 minutes |
| **Abort Conditions** | Database overload (query rate > 2x, CPU > 80%), latency > 2s, connection pool exhaustion to database |
| **Rollback** | Redis auto-failover promotes replica. Kill the primary Redis instance. |
| **Expected Outcome** | **Success**: Cache miss rate increases to 100%, database handles the extra load, error rate stays at 0%, latency increases but stays within limits. **Failure**: Database overload, thundering herd (all services query DB simultaneously on cache miss), latency spikes, request failures. |

---

## 36. Message Queue Broker Failure

| Field | Value |
|-------|-------|
| **Name** | `mq-broker-failure-kafka` |
| **Category** | Infrastructure |
| **Hypothesis** | When the Kafka broker fails, producers buffer messages, consumers pause processing, and within 5 minutes of broker recovery, all messages are processed and no data loss occurs. |
| **Steady State Metrics** | Producer send latency < 50ms, consumer lag < 1000 messages, broker health = all green |
| **Method** | Terminate the Kafka broker pod/node. Chaos Mesh: `PodChaos` on Kafka. AWS MSK: trigger broker reboot. |
| **Blast Radius** | Single Kafka broker. Topic replication factor must be > 1. |
| **Duration** | 10 minutes (broker down for 5 min, recovery observation for 5 min) |
| **Abort Conditions** | Data loss (consumer offset mismatch), unrecoverable producer buffer overflow, cascading failures from unprocessed messages |
| **Rollback** | Broker should self-recover if part of a cluster. Manual: `kubectl rollout undo statefulset/kafka`. |
| **Expected Outcome** | **Success**: Producers buffer or retry, consumers rebalance, broker recovers, backlog clears, no data loss. **Failure**: Producer buffer overflow (message loss), consumer rebalance fails, messages lost, consumer lag never recovers. |

---

## 37. Auto-Scaling Max Capacity Reached

| Field | Value |
|-------|-------|
| **Name** | `autoscaling-max-capacity` |
| **Category** | Application |
| **Hypothesis** | When traffic spikes cause the service to reach its maximum autoscaling capacity, the service degrades gracefully (latency increase, possibly 503s) rather than crashing. Once traffic drops, the system recovers. |
| **Steady State Metrics** | Pod count = min replicas, CPU < 50%, P99 latency < 300ms |
| **Method** | Generate traffic load exceeding the max scaling capacity using a load testing tool (k6, Locust, wrk) to trigger HPA and push past maxReplicas. |
| **Blast Radius** | Single deployment, target service only. |
| **Duration** | 15 minutes |
| **Abort Conditions** | Cascading failures, upstream services affected, database overload |
| **Rollback** | Stop load test. HPA will scale down as load decreases. |
| **Expected Outcome** | **Success**: Service scales to maxReplicas, latency increases proportionally, errors may increase but service stays up and recovers when load drops. **Failure**: Service crashes at max capacity, load balancer health check fails, cascading failures. |

---

## 38. Thundering Herd on Cache Miss

| Field | Value |
|-------|-------|
| **Name** | `thundering-herd-cache-miss` |
| **Category** | Application |
| **Hypothesis** | When a popular cache key expires, multiple concurrent requests for the same key result in only one request hitting the database (request coalescing), and the database is not overwhelmed. |
| **Steady State Metrics** | Database query rate (per key) = 1 query per cache miss, cache hit rate > 90% |
| **Method** | Expire a popular cache key, then send many concurrent requests for it. Observe if the database sees N queries or 1 query for the same key. |
| **Blast Radius** | Single cache key, single service. |
| **Duration** | 5 minutes |
| **Abort Conditions** | Database overload, query rate spike > 10x |
| **Rollback** | Re-populate cache, key will be re-cached after first successful query. |
| **Expected Outcome** | **Success**: Only one database query per key despite N concurrent requests, other requests wait for first to populate cache, database stays healthy. **Failure**: N requests = N database queries (no coalescing), database overload, cache stampede cascades to other keys. |

---

## 39. Slow Database Query (>5s)

| Field | Value |
|-------|-------|
| **Name** | `slow-db-query-5s` |
| **Category** | Application |
| **Hypothesis** | When a specific database query takes >5 seconds, the application's timeout for that query fires, the connection is returned to the pool, and a fallback or error response is returned. No connection pool exhaustion occurs. |
| **Steady State Metrics** | P99 DB query latency < 200ms, connection pool active < 50%, error rate < 0.1% |
| **Method** | Inject a database query that runs a slow SELECT (e.g., `SELECT pg_sleep(5)` in PostgreSQL, or use `pt-mongodb-query-digest` with injected delay). |
| **Blast Radius** | Single query path to database. |
| **Duration** | 5 minutes |
| **Abort Conditions** | Connection pool exhaustion, database CPU spike, cascading slow queries |
| **Rollback** | Kill the slow query. `SELECT pg_terminate_backend(pid)` or kill injected process. |
| **Expected Outcome** | **Success**: Query timeout fires, connection is released back to pool, error response returned gracefully. **Failure**: Connection pool accumulates waiting connections, pool exhaustion, cascading failures to all database queries. |

---

## 40. Slow Database Query (>30s)

| Field | Value |
|-------|-------|
| **Name** | `slow-db-query-30s` |
| **Category** | Application |
| **Hypothesis** | When a database query takes >30 seconds, the application's long-query guard fires, the query is terminated, the connection is released, and the application returns a 503. No connection pool exhaustion occurs even with repeated slow queries. |
| **Steady State Metrics** | P99 DB query latency < 200ms, max query duration < 10s, no query timeout events |
| **Method** | `SELECT pg_sleep(35)` or equivalent. Run multiple concurrent slow queries up to connection pool limit. |
| **Blast Radius** | Single service, database connection pool. |
| **Duration** | 10 minutes |
| **Abort Conditions** | Connection pool exhaustion, database failure, cascading failures |
| **Rollback** | Terminate all slow queries. Verify connection pool drains and returns to health. |
| **Expected Outcome** | **Success**: Queries are terminated at timeout, connections released, pool stays healthy, service returns 503 for affected requests. **Failure**: Connection pool exhausts completely, all database operations fail, service goes down. |

---

## 41. Rate Limiter Effectiveness Test

| Field | Value |
|-------|-------|
| **Name** | `rate-limiter-effectiveness` |
| **Category** | Application |
| **Hypothesis** | When requests to orders-service exceed the configured rate limit, excess requests are rejected with HTTP 429 (Too Many Requests) and the service remains healthy. No requests beyond the limit reach payment-service. |
| **Steady State Metrics** | Request rate = baseline, 429 responses = 0, payment-service request rate = orders-service request rate |
| **Method** | Generate requests to orders-service at 2x, 5x, and 10x the configured rate limit. Use k6 or wrk with increasing concurrency. |
| **Blast Radius** | Single endpoint, single service. |
| **Duration** | 10 minutes |
| **Abort Conditions** | Payment service gets overloaded (rate limiter not effective), orders-service crashes |
| **Rollback** | Stop load test. Rate limiter counters reset according to configuration. |
| **Expected Outcome** | **Success**: Rate limiter returns 429 for excess requests, payment-service sees only allowed request rate, orders-service stays healthy. **Failure**: Rate limiter doesn't trigger (misconfiguration), all requests forwarded to payment-service, no 429 returned. |

---

## 42. Graceful Shutdown Test

| Field | Value |
|-------|-------|
| **Name** | `graceful-shutdown-orders-service` |
| **Category** | Application |
| **Hypothesis** | When a pod is gracefully shut down (SIGTERM), the application catches the signal, stops accepting new requests, completes in-flight requests within the termination grace period, and then exits cleanly. |
| **Steady State Metrics** | Request count during shutdown: 0 failed, 0 dropped. Termination delay: < 30s |
| **Method** | `kubectl delete pod -l app=orders-service --grace-period=30` while sending continuous traffic. Observe request counts during shutdown. |
| **Blast Radius** | Single pod. |
| **Duration** | 5 minutes |
| **Abort Conditions** | Any request fails during shutdown, preStop hook hangs, process doesn't respond to SIGTERM (force kill after grace period) |
| **Rollback** | Pod is terminated and recreated by ReplicaSet. |
| **Expected Outcome** | **Success**: Pod catches SIGTERM, de-registers from load balancer, completes in-flight requests, exits cleanly. **Failure**: SIGKILL after grace period (in-flight requests lost), load balancer still sends traffic during shutdown, processes don't handle SIGTERM. |
