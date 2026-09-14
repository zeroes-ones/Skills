# Verification Guardrails

The checks that must run before a document is called done.

## The pre-ship gates

1. **Reopen and assert.** Read the file back; assert representative content.
2. **Reconcile counts.** Rows, pages, slides — compare both sides of every transform.
3. **Confirm formula vs value.** Ask the consumer; do not infer.
4. **Inspect every conversion.** Page count, fonts, table widths.
5. **Verify types.** Dates are dates; numbers are numbers.
6. **Check accessibility structure.** Headings, alt text, language.
7. **Strip metadata.** Especially before an external send.
8. **Confirm the consumer can open it.** The real target application, not a viewer.

## Guardrail placement

The verification belongs **in the script**, not in a reviewer's attention. A check that depends on
someone remembering to look is a check that fails exactly when someone is busy.

## Failure modes of verification

- **Write-only pipeline.** Nothing reads the output back, so generated is assumed correct.
- **Manual-only checks.** The gate exists in a checklist nobody runs.
- **Assumed conversion fidelity.** The file is shipped unseen.
- **Unreconciled transform.** A silent drop looks exactly like success.
- **Verified in the wrong application.** It opens in a viewer and breaks in Word.
