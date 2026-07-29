# CRM Integration Playbook
> Reference: Salesforce NPSP, Blackbaud RE, DonorPerfect integration patterns

## Common CRM Data Model

| CRM Entity | Maps To | Key Fields |
|-----------|---------|------------|
| Contact | Donor | email, first_name, last_name, address, phone |
| Account | Household | name, primary_contact, household_email |
| Opportunity | Donation | amount, close_date, stage, campaign, fund |
| RecurringDonation | Subscription | amount, frequency, status, payment_method |

## Deduplication Rules

1. **Exact email match** → Merge contacts (newer data wins on conflicts)
2. **Email + fuzzy name (Levenshtein ≤2)** → Flag for manual review
3. **Same address + same last name** → Flag as possible household

## Sync Webhook Flow

```
payment.success → CRM API
├── upsert Contact (email match, else create)
├── upsert Account (household match, else create)
├── create Opportunity (linked to Contact + Account)
├── if subscription_id: create RecurringDonation
└── store webhook_id for idempotency
```

## Migration Checklist
1. Export full data from source CRM
2. Run deduplication (matching rules above)
3. Map fields: source → target schema
4. Dry-run import to staging
5. Validate: record counts match, totals match, spot-check 50 records
6. Full import with import metadata (source, timestamp)
7. Archive pre-migration snapshot for 12 months

Version: 1.0
