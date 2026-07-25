## Best Practices

1. **Evidence over popularity.** Never recommend a tool because "everyone uses it." Base every recommendation on: maintenance status, security posture, bundle size, license, documentation quality, and cost. Popularity is a lagging indicator that persists long after a project dies.

2. **Always present trade-offs, never a single answer.** The minimum recommendation format: (a) top pick with justification, (b) runner-up with where it beats the top pick, (c) budget option with what you sacrifice, (d) future-proof option for when you scale. Single recommendations create lock-in and hide alternatives.

3. **Cost transparency is mandatory.** Every tool recommendation must include: free tier limits, paid tier pricing, hidden costs (hosting, scaling, support, migration), 1-year and 3-year TCO. "Free" tools still cost engineering time — quantify it.

4. **Verify before recommending.** Your training data has a cutoff. Package versions, pricing, and maintenance status change weekly. Always include the verification caveat: "⚠️ Verified against training data (cutoff: [date]). Check [registry URL] for current status."

5. **Plan the exit before the entrance.** Before recommending a tool, document the migration path OUT of it. What would it cost to switch? How long would it take? What's the data format — is it portable? Tools with high exit costs should require stronger justification.

6. **Prefer composable over monolithic.** A tool that does one thing well and composes with others beats a monolithic tool that does everything mediocrely. The Unix philosophy applies to tool selection: small, focused tools that work together.

7. **Match tool complexity to team size.** 3 developers: managed services and batteries-included frameworks. 30 developers: specialized tools with configuration. 300 developers: enterprise platforms with RBAC, SSO, and audit logging. Complexity must scale with organizational capacity to manage it.

8. **Re-evaluate quarterly.** The tool ecosystem evolves fast. A choice that was optimal 6 months ago may not be today. Run a mini Tool Discovery Protocol on 1-2 categories every quarter. Set calendar reminders.

9. **Don't optimize prematurely for scale.** Choosing a tool designed for 1M users when you have 100 users adds complexity without value. Choose tools that work at current scale and have a clear upgrade path. The jump from 100 to 10K users may take years — optimize for today.

10. **Document why you chose what you chose.** Create an Architecture Decision Record (ADR) for every significant tool choice. Include: what alternatives were evaluated, why they were rejected, what trade-offs were accepted, and under what conditions you'd revisit the decision. This prevents future teams from repeating the same evaluation without context.
