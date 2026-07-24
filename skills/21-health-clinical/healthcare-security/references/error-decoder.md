# Healthcare Security Error Decoder

Common healthcare security error patterns, their root causes, and resolutions.

## E1: "S3 bucket policy allows unencrypted uploads containing PHI"

**Symptom:** Infrastructure-as-code deploys S3 bucket for PHI without
`aws:kms` or `AES256` server-side encryption requirement in bucket policy.
**Root cause:** Default S3 bucket policy does not enforce encryption.
Bucket accepts unencrypted PUT requests, and PHI gets stored in plaintext.
**Resolution:** Add bucket policy condition denying `s3:x-amz-server-side-encryption`
not present: `"Condition": {"StringNotEquals": {"s3:x-amz-server-side-encryption":
["aws:kms", "AES256"]}}`. Enable default encryption with KMS CMK. Verify
with `aws s3api put-object --bucket $BUCKET --key test.txt --body test.txt`
— must fail with `AccessDenied` when no encryption header provided.

## E2: "RDS instance has storage_encrypted = false"

**Symptom:** Terraform/CloudFormation deploys RDS with `storage_encrypted`
unset or `false`. PHI stored in plaintext on EBS volumes. **Root cause:**
Encryption flag is opt-in, not default. **Resolution:** Set
`storage_encrypted = true` and `kms_key_id = aws_kms_key.phikey.arn` in
resource definition. Note: enabling encryption post-creation requires
snapshot-restore migration. Prefer enabling at launch.

## E3: "PHI detected in CloudWatch log group"

**Symptom:** `grep -E '[0-9]{3}-[0-9]{2}-[0-9]{4}'` returns matches in
CloudWatch Logs. SSN/MRN/DOB patterns present in application logs.
**Root cause:** Unstructured logging — `console.log(patient)` dumps entire
patient object. **Resolution:** (1) Deploy PHI redaction middleware that
replaces SSN/MRN with `[REDACTED]` before log emission. (2) Implement
structured logging with a PHI-whitelist for audit tables only. (3) Add
pre-commit/pre-push hooks scanning for identifier patterns. (4) Purge
affected log groups — note: this itself may be a reportable breach if
500+ individuals affected and logs were accessible.

## E4: "Database connection uses sslmode=disable"

**Symptom:** Connection string: `postgresql://user:pass@host/db?sslmode=disable`.
PHI transmitted in plaintext between application and database. **Root cause:**
Convenience during development — sslmode is opt-in. **Resolution:** Use
`sslmode=verify-full` in all environments. Enforce server-side: PostgreSQL
`pg_hba.conf` should use `hostssl` (not `host`) for PHI databases. Test with
`psql "sslmode=disable"` — must be rejected.

## E5: "FHIR endpoint returns all resources without patient scope filtering"

**Symptom:** GET /fhir/Observation returns all observations across all
patients — no patient-level filtering. **Root cause:** Missing OAuth scope
enforcement in API. SMART on FHIR requires `patient/Observation.rs` scope.
**Resolution:** Enforce patient-compartment scoping in FHIR server.
Validate OAuth `patient` claim matches `subject` parameter. Reject requests
with `patient/*` wildcard scopes. Audit all FHIR endpoints for scope gaps.

## E6: "Telemedicine consult recorded to consumer cloud storage"

**Symptom:** Zoom/Teams telehealth session recordings stored in vendor's
default consumer cloud storage (Zoom Cloud, OneDrive consumer) without BAA.
**Root cause:** Default recording destination is consumer tier. **Resolution:**
Configure recording destination to HIPAA-compliant storage (S3 with BAA,
Azure with BAA). Verify BAA covers recording storage. Disable local recording
on clinician devices. Set auto-deletion policy for recordings per retention
schedule.

## E7: "De-identification uses pseudonymization only — no standard cited"

**Symptom:** Architecture document says "We pseudonymize patient data by
replacing MRN with a hash." No reference to Safe Harbor or Expert
Determination. **Root cause:** Pseudonymization is NOT a HIPAA-recognized
de-identification method. **Resolution:** Cite the standard: Safe Harbor
(removal of all 18 identifiers with no actual knowledge) or Expert
Determination (statistical certification). Pseudonymization alone produces
PHI — the mapping between hash and MRN is itself a regulated identifier.
