# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You configure security groups with `0.0.0.0/0` "temporarily for debugging" and forget to remove them | Every network resource you provision is in Terraform/Pulumi with security group referencing (not CIDR ranges), NACL defense-in-depth, and VPC Flow Logs enabled — and you haven't touched the AWS console in 6 months | You design a multi-region, multi-cloud network architecture that survives a full region failure with under 60 seconds of packet loss — and you've tested it by actually pulling the plug on a region during business hours |
| You think DNS is "just A records and CNAMEs" and you've never configured split-horizon or a private hosted zone | You design DNS with split-horizon (public + private zones), health-check-based failover records with 60-second TTLs, and DNSSEC — and you can diagnose a DNS resolution failure from `dig +trace` output in under 5 minutes | A network outage happens and you're the person everyone in the incident call waits for before making a decision — your diagnosis is trusted because your last 10 diagnoses were all correct |
| You assign CIDR ranges by picking a random `/16` and hoping it doesn't overlap with anything | You maintain a CIDR allocation register across all VPCs, accounts, and on-prem networks — with 3-year growth projections and no overlaps — updated every quarter | You lead a merger where two companies with overlapping 10.0.0.0/8 networks are consolidated into a single routable network with zero application re-IP'ing — the network merge completes in 6 weeks instead of the industry-typical 18 months |

**The Litmus Test:** Can you design and deploy a production VPC — public subnets, private subnets with NAT, security groups with least privilege, VPC endpoints, flow logs, and Transit Gateway attachment — entirely in Terraform, in under 2 hours, and have it pass a penetration test?
