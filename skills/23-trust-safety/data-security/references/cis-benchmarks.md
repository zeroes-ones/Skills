# CIS Benchmarks — Database Hardening

## Overview
Center for Internet Security (CIS) Benchmarks provide consensus-based configuration standards for securing databases including PostgreSQL, MySQL/MariaDB, Microsoft SQL Server, and Oracle Database.

## Common Database Hardening Controls

### Authentication & Authorization
- Remove default accounts and demo databases
- Enforce password complexity and rotation
- Use certificate-based authentication where available
- Implement least-privilege role-based access

### Network Security
- Bind database to specific interfaces (not 0.0.0.0)
- Require TLS 1.2+ for all connections
- Network-level firewalling (security groups, iptables)
- Disable remote root/dba access

### Audit & Monitoring
- Enable query logging for all sensitive data access
- Log connection attempts (successes and failures)
- Forward logs to centralized SIEM
- Alert on schema changes and privilege escalation

### Encryption
- Enable Transparent Data Encryption (TDE)
- Column-level encryption for PII/PHI/PCI fields
- Encrypt backups with separate keys
- Key management via external KMS

## References
- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks/
- PostgreSQL Benchmark, MySQL Benchmark, SQL Server Benchmark
