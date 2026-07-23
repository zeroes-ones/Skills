# Is This Overkill? Checklist

| Scenario | Overkill Unless... |
|----------|-------------------|
| Multi-cloud for < $50M ARR | You have $100K+ in credits from GCP/Azure |
| Service mesh for < 10 services | You need strict mTLS for compliance |
| Multi-region active-active for < 100K DAU | 99.99% SLA is a contractual requirement |
| KMS with external HSM for < 100 secrets | You're in fintech/healthcare with regulatory mandate |
| Custom VPC with Transit Gateway for 1 app | You have on-prem hybrid connectivity requirements |
| Provisioned concurrency for all Lambdas | P99 latency > 500ms for customer-facing endpoints |
