# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
1. **Never run your first chaos experiment in production:** Always staging first. Production readiness requires staging GameDay with clear learnings and proven abort mechanisms.
2. **Verify observability before every experiment:** Inject the fault in staging for 30 seconds. If you can't see it on dashboards within 2 minutes, fix observability before proceeding — running chaos without observability is just breaking things.
3. **Start with the smallest possible blast radius:** Single pod, 1% traffic, 5-minute window. Expand only after N successful runs (N=3 for infra faults, N=5 for stateful faults).
4. **Define abort conditions with specific numeric thresholds:** "Error rate > 5% for 30 seconds" not "if things look bad." Auto-termination must be tool-enforced, not human-dependent.
5. **Test failures you've actually experienced first:** Prioritize experiments based on real postmortems, not hypothetical scenarios. The best failure mode to test is the one that already caused an incident.
6. **Run experiments during low-traffic windows with on-call aware:** Schedule experiments 1-4 AM or weekends. Notify on-call 24+ hours in advance with expected symptoms and abort command.
7. **Every experiment needs a documented rollback:** One command, one feature flag flip, one script — tested in staging before production. If rollback fails, you have a production incident.
8. **Track MTTR per failure mode:** Recovery time is as important as resilience. If the system recovers in 30 seconds vs 5 minutes, that difference matters to users.
9. **Integrate chaos into CI/CD:** Run automated experiments on every merge to main in staging. Catch resilience regressions like functional bugs — before they reach production.
10. **GameDay debrief must produce tracked action items:** Every finding gets an owner, severity, ticket number, and due date. Learning without action is wasted effort.
