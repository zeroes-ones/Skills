# CSPM vs CNAPP Tools — Evaluation & Comparison

Reference for evaluating and deploying Cloud Security Posture Management (CSPM) and Cloud-Native Application Protection Platform (CNAPP) tools across AWS, Azure, and GCP.

---

## CSPM vs CNAPP: What's the Difference?

| Capability | CSPM | CNAPP |
|-----------|------|-------|
| Misconfiguration scanning | ✅ Core function | ✅ Included |
| Compliance benchmarking (CIS, PCI, HIPAA) | ✅ Core function | ✅ Included |
| Vulnerability management | ❌ Limited | ✅ Agentless + agent-based |
| Runtime threat detection | ❌ No | ✅ Yes (agent-based) |
| IaC scanning | ❌ Separate tool | ✅ Integrated |
| Container/K8s security | ❌ Separate tool | ✅ Integrated |
| Attack path analysis | ❌ No | ✅ Graph-based |
| Data security (DLP, DSPM) | ❌ No | ✅ Some (Wiz, Prisma) |
| Identity security (CIEM) | ❌ No | ✅ Some (Wiz, Orca) |
| Cloud workload protection (CWPP) | ❌ No | ✅ Agent-based runtime |

**Evolution:** CNAPP = CSPM + CWPP + CIEM + IaC scanning + container security + DSPM — unified in a single platform. The industry is consolidating toward CNAPP.

## Tool Comparison Matrix

| Tool | Type | Deployment | Strengths | Weaknesses | Pricing Model |
|------|------|-----------|-----------|------------|---------------|
| **Wiz** | CNAPP | Agentless (API + snapshot) | Attack path analysis, cloud context prioritization, multi-cloud, fast deployment | Newer entrant (founded 2020), premium pricing | % of cloud spend (~1-3%) |
| **Orca** | CNAPP | Agentless (SideScanning) | Reads cloud workload block storage without agent, comprehensive | Limited runtime threat detection (no agent) | % of cloud spend |
| **Prisma Cloud** | CNAPP | Agentless (posture) + Agent (Defender) | Mature (Palo Alto), ML-based anomaly detection, integrated WAAS | Complex deployment, agent lifecycle management, higher TCO | Credits or per-asset |
| **AWS Security Hub** | CSPM | Native API integration | Free (AWS Config costs apply), native AWS integration, automated remediation with EventBridge | AWS-only, limited to AWS services, finding deduplication challenges | Free + AWS Config costs ($0.001/config item) |
| **CrowdStrike Falcon** | CNAPP | Agent-based (Falcon sensor) | Strong runtime threat detection, cloud + endpoint unified, adversary intelligence | Agent overhead, primarily endpoint heritage, cloud posture newer | Per-workload ($5-20/host) |
| **Sysdig** | CNAPP | Agent-based (eBPF) | Deep container/K8s runtime detection, Falco integration, eBPF low overhead | Container/K8s focused, less mature cloud posture | Per-node or per-container |

## Agentless vs Agent-Based: Decision Framework

### When Agentless Wins

- You need 100% coverage in <24 hours
- No permission to deploy agents (PaaS/serverless-heavy, third-party managed)
- Cost-sensitive (no agent lifecycle management overhead)
- Primary concern is posture management (misconfigs, compliance, vulnerabilities)

### When Agent-Based Wins

- You need runtime threat detection (process monitoring, network traffic analysis, in-memory forensics)
- Production workloads where compromise detection matters (C2 communication, cryptomining, ransomware behavior)
- Container/K8s environments (eBPF-based agents like Falco/Tetragon/Sysdig)
- You already have an endpoint agent (CrowdStrike, SentinelOne) and want cloud workload protection

### Recommended Strategy

**Agentless for posture + Agent-based for runtime.** Deploy Wiz/Orca/Security Hub for continuous posture management (covers 100% of resources, always-on compliance). Add Falco/Tetragon/Sysdig/CrowdStrike on production Kubernetes and EC2 workloads for runtime threat detection. This combination gives you breadth (posture) and depth (runtime).

## Vulnerability Prioritization with Cloud Context

Traditional CVSS scoring treats all vulnerabilities equally. Cloud context prioritization adds:

1. **Public exposure**: Is the vulnerable resource internet-facing? (ALB, public IP, public DNS)
2. **IAM privilege**: What permissions does the compromised resource have? (IAM role with `s3:*` vs read-only)
3. **Data sensitivity**: Does the resource have access to PII/PCI/PHI data?
4. **Lateral movement risk**: Does it share a security group/network with sensitive resources?
5. **Exploitability**: Is there a known public exploit? (CISA KEV, EPSS score)

A Critical CVE on an EC2 instance with no public IP, no IAM role, and no sensitive data access may have lower **risk priority** than a High CVE on an instance with an IAM role granting `s3:*` on a PCI data bucket.

## Deployment Decision Tree

```
Starting CSPM/CNAPP evaluation:
|-- Single AWS account, <50 resources → AWS Security Hub + GuardDuty + Inspector (free/native)
|-- AWS-only, 10-100 accounts → Security Hub (aggregator) + Prowler + Config conformance packs
|-- Multi-cloud (AWS + Azure + GCP), 50+ accounts → Wiz, Orca, or Prisma Cloud (CNAPP)
|-- Kubernetes-heavy → Sysdig, Aqua, or CNAPP + Falco (runtime depth)
|-- Budget <$10K/year → ScoutSuite + Prowler + Trivy (open source) + Security Hub aggregation
```
