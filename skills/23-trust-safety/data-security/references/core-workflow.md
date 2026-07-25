## Core Workflow

Execute these phases in order. Each phase gates the next.

**Phase 1: Data Discovery & Classification (~30 min)**
1. Run automated sensitive data discovery across all data stores
2. Scan schemas for PII patterns, credential leaks
3. Build classification taxonomy: PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
4. Assign classification labels to every data store and sensitive column
5. Identify data owners and map data flows
6. **Output:** Data classification matrix, data flow diagram, shadow data report

**Phase 2: Protection Design (~60 min)**
1. Select encryption approach per threat model: at rest (AES-256-GCM), in transit (TLS 1.3), in use (app-level)
2. Design DLP rules based on classification tiers
3. Define masking/tokenization strategy for non-production
4. Design key management hierarchy and rotation schedule
5. **Output:** Protection architecture document, DLP rule set, KMS configuration

**Phase 3: Implementation & Hardening (~90 min)**
1. Apply database hardening per CIS Benchmarks
2. Configure DLP policies at each layer
3. Implement column-level encryption for PII/PHI/PCI fields
4. Set up audit logging with structured format
5. Configure SIEM forwarding with real-time alerting
6. **Output:** Hardened configurations, deployed DLP policies, audit log pipeline

**Phase 4: Validation & Testing (~45 min)**
1. Test DLP rules with sample sensitive data
2. Verify encryption at storage layer
3. Validate data masking in non-production
4. Penetration test data access controls
5. Verify audit logs appear in SIEM
6. **Output:** Test results report, gap analysis, remediation tickets

**Phase 5: Monitoring & Response (~30 min)**
1. Configure DLP alerts with severity tiers
2. Set up audit log aggregation
3. Define data breach response playbook
4. Schedule recurring data discovery scans
5. Configure automated compliance reporting
6. **Output:** Alert configurations, incident response runbook, scan schedule
