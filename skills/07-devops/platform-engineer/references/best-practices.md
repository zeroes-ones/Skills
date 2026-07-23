# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
<!-- DEEP: 10+min -->
- **Platform as product, not project**: maintain a public roadmap, collect NPS, prioritize based on developer-hours-saved. The platform competes for adoption — make it the path of least resistance.
- **Golden paths cover 80%, not 100%**: build paved roads for common patterns; teams can leave the path for specialized needs but own the consequences.
- **Thinnest viable platform**: ship the smallest thing that removes developer toil. A 10-line reusable workflow deployed today beats a full portal launched in 6 months.
- **Self-service by default, concierge for emergencies**: every capability must be consumable without a ticket. Reserve human interaction for design reviews and incidents.
- **Dogfood your own platform**: the platform team deploys the platform using the platform. If the golden path is painful for you, it's unbearable for others.
- **Policy at the platform layer, not in documentation**: enforce security, compliance, and cost controls in templates and pipelines — docs are aspirational; gates are real.
- **Measure what matters**: time-to-first-deploy, deployment frequency, platform NPS, and template adoption rate. Not vanity metrics like "number of templates created."
- **Deprecate with empathy**: minimum 90 days notice, automated migration tooling where possible, and a human to help stuck teams. Killing features builds trust if done well.
- **Platform is a product — staff it like one**: a platform team without a PM is an infrastructure team that takes tickets. Add PM, UX, and DevRel as you scale.
- **Avoid the "platform team as bottleneck" trap**: if every deploy requires platform team approval, you've built a gate, not a platform. Self-service means no human in the loop.
