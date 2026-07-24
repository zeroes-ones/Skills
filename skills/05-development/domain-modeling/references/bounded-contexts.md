# Bounded Contexts

A bounded context is a boundary within which a specific domain model applies. Inside the boundary, all terms have precise, unambiguous meaning.

## Identification Checklist
- [ ] Does a single term ("Account", "User", "Order") mean different things to different stakeholders?
- [ ] Are there implicit boundaries because different teams own adjacent functionality?
- [ ] Would merging two contexts force a compromise that satisfies no one?
- [ ] Does data flow between contexts via well-defined interfaces or ad-hoc database queries?

## Designing Bounded Contexts
1. Map the current implicit boundaries by interviewing stakeholders
2. Name each context with a clear, stakeholder-recognized label
3. Define the ubiquitous language within each context
4. Specify integration patterns between contexts (API, events, shared kernel)
5. Document in CONTEXT.md under "Bounded Contexts" table

## Common Mistakes
- One bounded context per database table (too fine-grained)
- One bounded context per microservice (too coarse — a microservice may contain multiple contexts)
- Ignoring the organizational structure when drawing boundaries
