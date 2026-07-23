# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Build what differentiates, buy everything else**: your engineering talent should work on things that create competitive advantage. Auth? Buy. Payments? Buy. Your secret sauce? Build.
- **Team design dictates architecture**: if you want loosely coupled services, create loosely coupled teams. Conway's Law is not negotiable.
- **Architecture decisions are reversible or irreversible**: reversible decisions (language choice within a service) → delegate to team. Irreversible decisions (database choice for core data, API contracts) → review broadly.
- **Technical debt is a financial instrument**: taken wisely, it accelerates delivery. Taken recklessly, it bankrupts velocity. Use the interest-rate framework.
- **Innovation doesn't happen by accident**: ring-fence time, create the funnel, celebrate shipping (not just building).
- **The best vendor evaluation is a working PoC**: RFP documents lie. Two weeks of integration reveals more than six months of sales calls.
