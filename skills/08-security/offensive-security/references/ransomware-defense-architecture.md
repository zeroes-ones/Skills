# Ransomware Defense Architecture

## Overview

Ransomware is the most financially damaging cyber threat, with average ransom payments exceeding $800K in 2024 (up from $400K in 2023) and total incident costs averaging $5.1M (IBM/Ponemon 2024). This reference covers backup architecture, identity hardening, EDR deployment validation, deception technology, and RRA scoring methodology.

## 3-2-1 Backup Rule with Modern Augmentations

### The Classic 3-2-1 Rule
- **3 copies** of data: primary production copy + 2 backups.
- **2 different media types:** disk + tape, disk + cloud, or two different storage systems.
- **1 off-site copy:** geographically separated from primary and other backups.

### The Modern 3-2-1-1-0 Rule (Ransomware-Hardened)
- **3 copies** of data (unchanged).
- **2 different media types** (unchanged).
- **1 off-site copy** (unchanged).
- **1 immutable or air-gapped copy:** Object lock (S3), WORM (Write Once Read Many) storage, append-only ZFS snapshots, offline tape. This is the single most important defense: ransomware cannot encrypt data it cannot modify. Immutability must include retention periods that cannot be shortened even by the root/administrator account.
- **0 errors:** Backup verification with automated restore testing. Unverified backups are not backups -- they are hopes stored on disk. Schedule quarterly full restoration drills. Measure Recovery Time Objective (RTO) and Recovery Point Objective (RPO). If RTO > 72 hours for critical systems, the backup architecture is insufficient.

### Backup Account Isolation
- Backup infrastructure credentials must be in a separate Active Directory forest or at minimum a separate domain with no trust.
- Backup admin accounts must use dedicated Privileged Access Workstations (PAW).
- Backup deletion/modification requires multi-person approval (break-glass procedure).
- Backup system alerts on: mass deletion, configuration changes, retention policy modifications, credential changes.

## LAPS (Local Administrator Password Solution)

LAPS is a Microsoft solution that manages local Administrator account passwords on domain-joined computers. It is free, built into Windows, and the single highest-ROI security control for preventing lateral movement.

- **Password uniqueness:** Every local Administrator account must have a unique, complex password.
- **Password rotation:** Rotate passwords every 30 days by default, configurable per organizational policy.
- **Access control:** Only authorized personnel (help desk, SOC, IT) can read LAPS passwords. All access is logged in Event ID 4662 with the requesting user identity.
- **Integration:** LAPS integrates with Microsoft Intune for cloud-managed devices and Active Directory for on-premises.

## EDR Deployment Validation

An EDR product that is installed but not properly configured is security theater. Validate:
- **Coverage:** 100% of servers and workstations. Use the EDR console's coverage dashboard. Any gap is a blind spot.
- **Block mode:** Is the EDR in protect/block mode or monitor-only? Monitor-only detects but does not prevent -- ransomware encrypts before SOC responds. Block mode must be enabled.
- **Exclusions:** Review exclusion list. Common over-exclusions: entire C:\ drive, all .exe in a directory, process name-based exclusions. Every exclusion bypasses EDR.
- **Testing:** Run Atomic Red Team tests for common ransomware techniques (T1486: Data Encrypted for Impact, T1490: Inhibit System Recovery, T1562.001: Disable or Modify Tools). Verify EDR detects AND blocks.
