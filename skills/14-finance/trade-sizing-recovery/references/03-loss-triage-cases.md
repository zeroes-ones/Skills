# Loss Triage — Worked Cases

Companion to `SKILL.md` Decision Tree 2.

## Case A — "−55%, 60 DTE, liquid, thesis intact"

- Numbers: cost $3.00, mark $1.35, spread 8%, OI 4,000, underlying above its invalidation level.
- Disposition: **HOLD-WITH-TP** at 2× mark ($2.70). Level-based SL unchanged (underlying close below the line ⇒ cut).
- Why: 60 DTE leaves time for the level to work; liquidity means the exit exists later too. No adds. No roll.
- What would flip it to CUT: underlying closes below the line for two sessions, or spread widens past 15% with OI collapsing.

## Case B — "−55%, 9 DTE, thin, thesis broken"

- Numbers: cost $2.20, mark $0.95, spread 26%, OI 210, underlying below the level.
- Disposition: **CUT into the next bounce**; if no bounce in two sessions, exit at market and accept the spread.
- Why: 9 DTE leaves no time for recovery; the spread donates value daily. Rolling forward pays theta twice and doubles the position count — count it as new risk, not a rescue.
- Executable check: if bid < $0.20, "cut" is unexecutable → reclassify **WRITE-OFF**.

## Case C — "−85%, 400 DTE, bid $0.06"

- Disposition: **WRITE-OFF.** Exit fees and spread exceed salvage.
- Actions: flag "no-TP by construction"; remove from the attention set (no daily checks); let expire; write the one-line lesson (usually: "lottery strike on a weak-RS name — never again").
- Why: attention is capital. A dead ticket scanned daily is a tax on positions that can still win.

## One-line disposition test

> "If this were cash today, would I buy this exact position?"
> No → CUT or WRITE-OFF. Yes → HOLD-WITH-TP, with the level named.
> "I'd buy something smaller/cheaper" → that *something* is the next trade; this one still resolves to cut/hold per the matrix.
