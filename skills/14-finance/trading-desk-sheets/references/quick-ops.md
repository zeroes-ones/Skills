# Quick Ops - reference implementation commands

> These are the reference implementation's exact commands (a desk using gspread + a snapshot JSON).
> Another implementation will differ in names, not in order: snapshot -> render -> verify -> stamp.

## The close (after every session)

```bash
# 1) refresh the snapshot (venue reads -> snapshot JSON; stamp `generated`)
# 2) one-command close: render -> invalid-cell check -> full audit
py -3 sheets_eod.py            # must print its green verdict, e.g. "EOD: ALL GREEN"
```

## Individual steps (when the close fails)

```bash
py -3 sheets_render.py         # render only (idempotent)
py -3 _dv_check.py             # per-cell REAL validation coverage - must read 0 mismatches
py -3 _audit.py                # full workbook audit - 0 fails expected
```

## The four traps - repair recipes

1) **Stale validation (red triangles)** - clear-then-apply:
   - REMOVE: `setDataValidation` over the whole column with NO `rule` key.
   - RE-APPLY: tight range ending at the table boundary (data + total row; never headers).
2) **Format bleed after row shifts** - reset-then-reapply:
   - `repeatCell` over the used block -> numberFormat `General`, bold `false`.
   - Re-apply currency / percent / bold ranges.
3) **Broadcast trap (#N/A)**:
   - last match: `=INDEX(range, SUMPRODUCT(MAX(cond*ROW(range)))-base)`
   - first match: `=INDEX(range, MATCH(TRUE, ARRAYFORMULA(range<>""), 0))`
   - NEVER: `LOOKUP(2,1/(...))`, range-based `XLOOKUP`.
4) **Grid caps ("exceeds grid limits")**:
   - `updateSheetProperties.gridProperties.rowCount/columnCount` BEFORE the values write.

## Day stamping

```bash
py -3 pnl_set.py <YYYY-MM-DD> ACCOUNT=value ...   # manual correction only - logged
```

## Manual checks worth keeping

- Spot-read three cells of every changed range after a render.
- Confirm user zones (fill columns, checkboxes, notes) are unchanged.
- Diff the snapshot's `generated` stamp against the report's timestamp.
