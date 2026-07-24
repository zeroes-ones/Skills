# Sensitive Data Discovery

## Overview
Automated scanning and classification of sensitive data across all data stores. Continuous discovery — shadow data is the attacker's first target.

## Discovery by Environment
### Structured Data Stores (Databases, Warehouses)
- Column-level scanning: regex patterns + column name heuristics
- Data fingerprinting: hash known PII values → search other stores
- Tools: AWS Macie, Google DLP API, Azure Purview

### Cloud Object Storage (S3, GCS, Azure Blob)
- Priority: buckets with public/authenticated-read ACLs
- Sample-based scanning: first 1MB per file type
- Full scan for flagged buckets: Parquet/ORC/CSV column-level, PDF/Office OCR

### SaaS Applications
- Google Workspace: Drive files, shared drive permissions
- Slack/Teams: messages and file attachments for PII/credentials
- Jira/Confluence: tickets and pages — developers paste credentials
- Salesforce: reports, dashboards, custom objects

## Discovery Cadence
- Known data stores: weekly incremental scan (new columns/tables)
- Cloud object storage: daily for new buckets, weekly full content scan
- SaaS applications: weekly scan — prioritize newly shared/created files

## Post-Discovery Actions
1. Auto-tag with classification label
2. Trigger protection workflow: enable encryption, apply RLS
3. Notify data owner for validation
4. Add to data catalog with classification metadata
