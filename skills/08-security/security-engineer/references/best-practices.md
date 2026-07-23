# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Shift left**: security testing in the IDE and at PR time; don't wait for staging or production scans.
- **Defense in depth**: no single control should be the only line of defense; layer preventive, detective, and corrective controls.
- **Assume breach**: design systems to limit blast radius, detect intrusions quickly, and recover gracefully.
- **Secrets never travel in plaintext**: encrypt in transit (TLS) and at rest (KMS); use ephemeral credentials whenever possible.
- **Patch aggressively**: automate OS and dependency patching; SLA: critical patches within 24 hours, high within 7 days.
