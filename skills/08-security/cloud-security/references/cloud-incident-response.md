# Cloud Incident Response & Forensics

Reference for cloud-specific incident response procedures, forensic evidence collection, and containment strategies across AWS, Azure, and GCP.

---

## Incident Response Lifecycle (Cloud-Specific)

```
Detection → Containment (15min) → Evidence Collection → Eradication → Recovery → Post-Incident
```

Cloud-specific considerations at each phase:

### Detection Sources

| Source | AWS | Azure | GCP |
|--------|-----|-------|-----|
| API activity anomalies | CloudTrail Insights | Activity Log anomalies | Audit Logs anomalies |
| Threat detection | GuardDuty | Microsoft Defender for Cloud | Security Command Center (Event Threat Detection) |
| Compromised credentials | IAM Access Analyzer, CloudTrail ConsoleLogin | Azure AD Identity Protection (risky sign-ins, impossible travel) | Security Command Center (IAM anomalous activity) |
| Cryptomining detection | GuardDuty (CryptoCurrency:B! finding), CloudWatch billing alarm | Defender for Cloud (cryptomining alert) | Event Threat Detection (cryptomining) |
| Data exfiltration | GuardDuty (Exfiltration:S3 finding), Macie (anomalous data access) | Defender for Cloud (unusual data transfer), Sentinel UEBA | Security Command Center, VPC Flow Logs analysis |
| Malware | GuardDuty (Malware:EC2 finding), Inspector | Defender for Cloud (malware detection), Defender for Endpoint | Event Threat Detection (malware) |

## Containment (First 15 Minutes)

### 1. IAM Key/Credential Rotation
```bash
# AWS: Deactivate immediately (don't delete — preserve for forensics)
aws iam update-access-key --access-key-id AKIAXXXXXXXXXXXXXXXX --status Inactive --user-name compromised-user

# Azure: Remove application permission, reset service principal credential
az ad app permission admin-consent --id <app-id>  # Revoke delegated permissions
az ad sp credential reset --id <sp-id>            # Reset client secret

# GCP: Disable service account key
gcloud iam service-accounts keys disable KEY_ID --iam-account=SA_NAME@PROJECT.iam.gserviceaccount.com
```

### 2. Instance/Resource Isolation
```bash
# AWS: Apply isolation security group (deny all inbound + outbound)
SG_ID=$(aws ec2 create-security-group --group-name isolate-$(date +%s) \
  --description "INCIDENT RESPONSE — Total isolation" --vpc-id vpc-xxx --query 'GroupId')
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol -1 --cidr 0.0.0.0/0  # Empty list = deny all
aws ec2 modify-instance-attribute --instance-id i-xxx --groups $SG_ID

# Remove from auto-scaling group (prevent termination + replacement)
aws autoscaling detach-instances --instance-ids i-xxx --auto-scaling-group-name my-asg \
  --should-decrement-desired-capacity

# Azure: Apply NSG with DenyAll rule
az network nic update --resource-group RG --name nic-name \
  --network-security-group isolate-nsg
az network public-ip update --resource-group RG --name pip-name --disassociate

# GCP: Apply firewall rule, remove external IP
gcloud compute instances delete-access-config i-xxx --access-config-name "External NAT"
gcloud compute firewall-rules create isolate-i-xxx --direction=INGRESS --action=DENY \
  --target-tags=compromised --priority=0
```

### 3. S3 Bucket Isolation & Legal Hold
```bash
# Apply restrictive bucket policy (deny all, preserve evidence)
aws s3api put-bucket-policy --bucket compromised-bucket --policy '{
  "Statement": [{
    "Effect": "Deny",
    "Principal": "*",
    "Action": "s3:*",
    "Resource": ["arn:aws:s3:::compromised-bucket", "arn:aws:s3:::compromised-bucket/*"]
  }]
}'

# Apply legal hold (immutable until removed — compliance/legal requirement)
aws s3api put-object-lock-configuration --bucket compromised-bucket \
  --object-lock-configuration '{ "ObjectLockEnabled": "Enabled", "Rule": { "DefaultRetention": { "Mode": "GOVERNANCE", "Years": 7 }}}'
```

## Forensic Evidence Collection

### Volatile Evidence (Preserve Immediately)
```bash
# EC2 memory dump (requires SSM agent)
aws ssm send-command --instance-ids i-xxx \
  --document-name AWS-RunShellScript \
  --parameters '{"commands":["sudo dd if=/dev/mem of=/tmp/mem.dump bs=1M && aws s3 cp /tmp/mem.dump s3://forensics-bucket/mem-i-xxx-$(date +%s).dump"]}'

# EBS snapshot (preserve disk state)
aws ec2 create-snapshot --volume-id vol-xxx --description "IR snapshot — compromised instance i-xxx"

# Database snapshot
aws rds create-db-snapshot --db-instance-identifier compromised-db \
  --db-snapshot-identifier ir-compromised-db-$(date +%Y%m%d-%H%M%S)
```

### Logs to Preserve
- **CloudTrail**: `aws cloudtrail lookup-events --lookup-attributes AttributeKey=Username,AttributeValue=compromised-user --start-time $(date -d '7 days ago' +%s)`
- **VPC Flow Logs**: Query CloudWatch Logs Insights for compromised instance ENI ID
- **GuardDuty findings**: `aws guardduty list-findings --detector-id <id> --finding-criteria Criterion={service.archived={Eq=["false"]}}`
- **S3 access logs**: Download from logging bucket for compromised bucket
- **SSH/RDP session logs** (if using Session Manager/Bastion): Export from CloudWatch

## Post-Incident Activities

### 1. Root Cause Analysis
- How did the attacker gain initial access? (credentials leak, misconfigured resource, unpatched CVE, phishing)
- What was the blast radius? (IAM Access Analyzer: What could the compromised role access?)
- What data was accessed or exfiltrated? (S3 access logs, CloudTrail S3 data events, Macie findings)
- What was the dwell time? (Time between initial access and detection)
- Could this have been detected earlier? (Missing GuardDuty? No CloudTrail Insights? No billing alarm?)

### 2. Prevent Recurrence
- Immediate: Fix the root cause (enable MFA, delete long-lived keys, patch CVE, fix bucket policy)
- Short-term: Enable additional detection controls (GuardDuty in all regions, CloudTrail Insights, VPC Flow Logs)
- Medium-term: Security architecture changes (SCPs to prevent, permission boundaries, automated remediation)
- Long-term: Tabletop exercises, incident response playbook updates, team training

### 3. Blast Radius Reduction
- If a single compromised role could access 50%+ of resources: redesign IAM with permission boundaries and SCPs
- If a single security group spans multiple tiers: split into per-tier security groups
- If lateral movement was easy: implement NetworkPolicy (K8s) or security group referencing (EC2)

## Incident Response Automation

Pre-build runbooks as AWS Systems Manager Documents / Azure Automation Runbooks:
- **IsolateEC2Instance**: Apply deny-all security group, detach from ASG, snapshot EBS
- **RotateCompromisedCredentials**: Identify all keys for user, deactivate, rotate in Secrets Manager
- **EnableForensicsLogging**: Enable VPC Flow Logs, CloudTrail Insights, DNS query logging, S3 data events
- **S3BucketLockdown**: Apply deny-all bucket policy, enable legal hold, export access logs

Automation reduces the 15-minute containment window to 2-3 minutes. Every minute counts during a cloud incident — attackers can provision thousands of dollars in compute resources in under 5 minutes.
