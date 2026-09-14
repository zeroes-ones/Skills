# Worked Example — Cross-Service Feature

**Spec:** Add saved payment methods to checkout. Two services (checkout, billing) and one schema.

## State changes

1. A payment method can be stored against a customer.
2. Checkout can display stored methods.
3. Checkout can charge a stored method.
4. Existing saved cards must be usable during rollout.

## Decomposition

| id | Deliverable | acceptance | verify | blocked_by | wave | collision_surface |
|---|---|---|---|---|---|---|
| T1 | Walking skeleton: one hard-coded method renders at checkout | Renders for a test customer | `npm test -- checkout` | — | 0 | `checkout/src/Checkout.tsx` |
| T2 | Schema: `payment_methods` table + migration | Migration applies and rolls back | `pytest tests/test_migration.py` | — | 0 | `billing/migrations/*` |
| T3 | Store a method for a customer (API) | POST persists and is readable | `pytest tests/test_methods_api.py` | T2 | 1 | `billing/api/methods.py` |
| T4 | Checkout lists stored methods | List renders real stored methods | `npm test -- methods-list` | T1, T3 | 2 | `checkout/src/Checkout.tsx` ← collides with T1 |
| T5 | Charge a stored method | Test charge succeeds | `pytest tests/test_charge_saved.py` | T3 | 2 | `billing/api/charge.py` |
| T6 | Rollout flag: saved methods behind a flag | Flag off = old path unchanged | `npm test -- flag-off` | T4, T5 | 3 | `checkout/src/flags.ts` |
| T7 | Backfill: existing stored cards reconciled | Counts match source | `pytest tests/test_backfill_counts.py` | T2 | 1 | `billing/jobs/backfill.py` |
| T8 | Cutover + observe | Error rate flat for 24h | dashboard check | T6, T7 | 4 | none (ops) |
| T9 | Remove old path + delete flag | Flag gone, tests green | `rg 'SAVED_METHODS' → 0` | T8 | 5 | `checkout/src/flags.ts`, `checkout/src/legacy/` |

## Waves

- **Wave 0:** T1, T2 — surface checked: no shared files
- **Wave 1:** T3, T7 — surface checked: different files, no shared resource
- **Wave 2:** T4, T5 — surface checked: different files (`Checkout.tsx` vs `charge.py`)
- **Wave 3:** T6 · **Wave 4:** T8 · **Wave 5:** T9

## Critical path

`T2 → T3 → T4 → T6 → T8 → T9` (6 hops). T1 is off-path; adding people to T1 does not shorten delivery.

## Forgotten work, made explicit

- Migration: T2 ✅ · Backfill: T7 ✅ · Rollout: T6 ✅ · Rollback: T6 (flag off) ✅ · Cleanup: T9 ✅
