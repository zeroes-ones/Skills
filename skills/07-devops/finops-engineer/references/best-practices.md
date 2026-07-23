# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
<!-- DEEP: 10+min -->
- **Tag or die**: untagged resources are invisible costs. Enforce tags via policy; auto-shutdown resources that remain untagged after 24 hours. > 95% compliance is non-negotiable.
- **RI/SP coverage targets 60-80%, not 100%**: 100% coverage means you're committed for every workload — no flexibility. Keep 20-40% on-demand for variable workloads and new services.
- **Right-size before you commit**: never buy a 3-year RI for an instance that's 80% idle. Right-size first, then commit to the optimized size.
- **Spot is free money (with engineering investment)**: spot instances save 60-90% but require interruption handling. Invest in spot-compatible architecture once; save forever.
- **Storage has infinite gravity**: data grows, access patterns decay, but storage costs compound. Lifecycle policies are the highest-ROI, lowest-effort optimization.
- **Data transfer costs hide in plain sight**: cross-AZ traffic is hard to see but easy to accumulate. Use AZ-aware service discovery and VPC endpoints to keep traffic local.
- **Cost is a feature**: every PR that adds a resource should estimate its monthly cost. CI/CD integration (Infracost, Terraform cost estimation) makes cost visible at design time.
- **Showback before chargeback**: start by showing teams their costs without charging them. Build cost awareness before adding financial accountability. Chargeback too early breeds resentment.
- **FinOps is cultural, not a tool**: tools provide visibility; the culture of cost awareness drives savings. Engineers who see their costs optimize them; engineers who don't, don't.
- **GreenOps is the next frontier**: carbon-aware scheduling and region selection often align with cost optimization (low-carbon regions tend to be cheaper). Track carbon alongside cost.
