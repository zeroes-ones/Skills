# Spreadsheet Modelling

A workbook that a human will edit is a model, not a data dump. Types, references, and formulas are
the contract.

## Rules

1. **Type every value.** A date written as a string breaks sort, filter, and pivot.
2. **Use number formats, not formatted strings.** `$1,234.00` is a string; `1234` with a currency
   format is a number.
3. **Name ranges.** Positional references (`B2:B47`) break on the first inserted row.
4. **Use tables for tabular data.** A table auto-expands; a range does not.
5. **Decide formulas vs values explicitly.** A live model recalculates; a snapshot does not.
   Guessing wrong produces a file that is quietly wrong for its whole life.
6. **Do not let a library recalculate.** `openpyxl` writes formulas; it does not evaluate them.
   Nothing computes until a spreadsheet application opens the file.

## Failure modes of spreadsheet work

- **String dates.** Every downstream pivot silently returns zero rows.
- **Frozen values where formulas belonged.** The model stops responding to its own inputs.
- **Positional references.** One row insert re-points every formula.
- **Wrong library for a deliverable.** `pandas.to_excel` drops formulas, formats, and styling.
- **No reconciliation.** Rows in equal rows out is the cheapest correctness check and the first skipped.
