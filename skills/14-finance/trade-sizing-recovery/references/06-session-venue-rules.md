# Session & Venue Rules (Execution Reality)

## Sessions (US equities/options, ET)

| Label | Window | What it means for orders |
|---|---|---|
| PRE | 04:00–09:30 | Thin books; RTH-only orders do NOT fill. Gap-risk information only. |
| RTH | 09:30–16:00 | The only window where standard orders execute. |
| AFTER | 16:00–20:00 | Reduced liquidity; special session tags required to fill. |
| OVER | 20:00–04:00 | Overnight sessions exist at some venues; most orders sit. |

**Rule:** a level cross outside an order's eligible session is information, never an execution. Restate the eligibility whenever reporting a cross.

## Venue capability classes

| Class | Behavior | How the skill adapts |
|---|---|---|
| Agentic (agent may trade) | Orders place directly (GTC TPs pre-authorized on existing positions; entries need explicit approval) | Place standing TPs; keep review→place discipline |
| Instruction-based (broker app confirmation) | Orders are instructions pending user confirmation | Output the exact spec; state that it needs app approval |
| Read-only / manual | Agent cannot place | Output ready-to-place spec (symbol, side, type, price, TIF, session) for one-word approval |
| Bridged (local proxy) | Reachable read-only by policy | Read state only; orders go through native tools after user connects them |

## Thin-book execution notes

- Spread > 25% or OI < 300 ⇒ "cut" may be **unexecutable** — reclassify as WRITE-OFF (Decision Tree 2).
- Stop orders become market orders into wide spreads; use level-based exits instead.
- Round-number rungs fill more reliably; check the book at the exact strike before committing the rung.

## Event gaps

- A GTC TP does nothing through an earnings gap or a macro shock. Pre-event exits are separate decisions with their own orders.
- No new risk into binary macro prints (rate decisions, auctions) or earnings inside the DTE window; size is zero when the gate is closed.
