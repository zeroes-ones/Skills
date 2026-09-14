# Estimation Boundary

This skill decomposes and orders. It does not price. The boundary matters because conflating the
two produces commitments the plan cannot support.

## What belongs here

- Task identity, deliverable, criteria, verification
- Dependencies and ordering
- Waves, collisions, critical path
- Right-sizing (demonstrable in one sitting)

## What belongs elsewhere

| Question | Correct skill |
|---|---|
| How long will this take? | `software-project-estimator` |
| What will it cost the client? | `services-engagement-pricing` |
| What should we charge / package? | `consulting-effort-estimator` |
| What is the ongoing support cost? | `software-maintenance-support-estimator` |

## Why the boundary exists

A plan is a hypothesis about *structure*; an estimate is a claim about *duration*. They fail
differently and are validated differently. Mixing them means a scheduling error silently becomes a
pricing error.

## Practical rule

If asked for a duration while planning, produce the plan first, then hand it to the estimator. The
plan makes the estimate better; the estimate must not shape the plan's decomposition.

## Failure modes at the boundary

- **Sizing in hours.** False precision; invites negotiation and destroys the "demonstrable in one sitting" rule.
- **Committing to dates from the plan.** The critical path is not a delivery promise.
- **Shrinking the plan to fit an estimate.** The worst outcome — decomposition is bent to hit a number.
- **No plan, only an estimate.** The estimate has nothing to be checked against.
