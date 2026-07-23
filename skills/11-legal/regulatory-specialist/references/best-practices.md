# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- In a software context, "validation" does NOT mean testing the software works — it means producing documented evidence that the software meets user needs and intended uses in a production-equivalent environment.
- Build your QMS to be audit-ready at all times, not just when an inspection is announced. An auditor should find the evidence they need without anyone hunting for it.
- Every design output must trace back to a design input, and every design input must trace forward to verification. Maintain this traceability matrix from day one — retrofitting it is painful.
- Start the risk management process during requirements gathering, not after implementation. Hazards identified late require expensive redesigns.
- Part 11 audit trails must be tamper-resistant — store them in append-only tables or immutable logs. The audit trail itself must be auditable.
- Never validate a production system with production data that contains PHI — use synthetic or de-identified test data.
- The Predicate Device analysis for 510(k) is the single most scrutinized part of your submission — invest the time to make the substantial equivalence argument airtight.
